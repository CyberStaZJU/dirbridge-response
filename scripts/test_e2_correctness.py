#!/usr/bin/env python3
"""Focused E2 correctness, numerical-health, and metric-persistence tests."""

import csv
import math
import random
import tempfile
from argparse import Namespace
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import TensorDataset

from algorithm import dirbridge
from main_fed import build_system_metrics_path, log_system_metrics
from models.test import test_img
from utils.e2_online import coverage_bound, uninitialized_group_mass
from utils.state_dict_ops import load_param_dict_, model_param_dict


def _args(**overrides):
    values = dict(
        num_users=8,
        num_groups=2,
        concurrency=4,
        buffer_size=2,
        dirbridge_buffer_delay_limit=4.0,
        dirbridge_cache_beta=0.9,
        e2_init_mode="online",
        e2_weight_source="unique_client",
        e2_oracle_features=False,
        device="cpu",
        bs=2,
        num_workers=0,
        verbose=False,
        algo="DirBridge",
        dataset="synthetic",
        alpha=0.5,
        random_cost="synthetic",
        seed=1,
        run_tag="test",
    )
    values.update(overrides)
    return Namespace(**values)


def _state():
    zeros = {"weight": torch.zeros(2)}
    state = {
        "delta": [dict(zeros) for _ in range(8)],
        "client_features": [None] * 8,
        "client_embeds": [None] * 8,
        "group_ids": [0, 1, 0, 1, -1, -1, -1, -1],
        "group_members": [[0, 2], [1, 3]],
        "group_counts": [2, 2],
        "group_centroids": torch.tensor([[1.0, 0.0], [0.0, 1.0]]),
        "group_cache": [dict(zeros), dict(zeros)],
        "group_cache_stamp": [0, 0],
        "group_cache_delay": [0.0, 0.0],
        "group_weights": [0.5, 0.5],
        "num_groups": 2,
        "w_glob": zeros,
        "stamp": [0, 0, 0, 0, 1, -1, -1, -1],
        "iterations": 1,
        "delays": [0.0] * 8,
        "seen_set": {0, 1, 2, 3},
        "arrival_count": [1, 1, 1, 1, 0, 0, 0, 0],
        "e2_client_last_arrival": [0, 0, 0, 0, -1, -1, -1, -1],
        "e2_clustered_clients": 4,
        "last_group_rebuild": 0,
        "recluster_count": 1,
        "oracle_features": [None] * 8,
        "e2_oracle_weights": None,
        "e2_last_weight_source": "unique_client",
        "e2_weight_source": "unique_client",
        "group_proj_dim": 2,
        "inflight": {},
    }
    for idx, feature in enumerate(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 0.0],
            [0.0, 1.0],
        ]
    ):
        state["client_features"][idx] = torch.tensor(feature)
        state["client_embeds"][idx] = torch.tensor(feature)
    return state


def test_inflight_isolation_and_exactly_once_materialization():
    state = _state()
    private = {"weight": torch.tensor([7.0, 8.0])}
    private_feature = torch.tensor([1.0, 0.0])
    state["inflight"] = {4: {"delta": private, "feature": private_feature, "stamp": 1}}
    assert state["delta"][4]["weight"].equal(torch.zeros(2))
    assert state["client_features"][4] is None
    state["inflight"][4]["delta"]["weight"].fill_(9.0)
    assert state["delta"][4]["weight"].equal(torch.zeros(2))
    dirbridge._materialize_arrivals(state, [4])
    assert state["delta"][4]["weight"].equal(torch.full((2,), 9.0))
    assert state["client_features"][4] is private_feature
    try:
        dirbridge._materialize_arrivals(state, [4])
    except RuntimeError:
        pass
    else:
        raise AssertionError("duplicate materialization was silently accepted")


def test_first_arrival_without_recluster_is_assigned_and_used():
    state = _state()
    args = _args()
    state["delta"][4] = {"weight": torch.tensor([1.0, 2.0])}
    state["client_features"][4] = torch.tensor([1.0, 0.0])
    newly_seen = dirbridge._record_arrivals(state, [4])
    assigned = dirbridge._assign_arrivals_to_existing_groups(state, newly_seen)
    assert newly_seen == [4]
    assert assigned == [4]
    assert state["group_ids"][4] == 0
    assert state["group_counts"] == [3, 2]
    selected = dirbridge._build_ema_group_updates(state, args, [4])
    assert state["last_unassigned_valid_count"] == 0
    assert sum(item["member_count"] for item in selected) == 1

    state["group_ids"][4] = -1
    state["seen_set"].add(4)
    empty_selected = dirbridge._build_ema_group_updates(state, args, [4])
    assert empty_selected
    assert state["last_unassigned_valid_count"] == 1
    assert all(item["member_count"] == 0 for item in empty_selected)


def test_duplicate_events_and_weight_refresh_semantics():
    state = _state()
    args = _args(e2_weight_source="unique_client")
    state["client_features"][4] = torch.tensor([1.0, 0.0])
    assert dirbridge._record_arrivals(state, [4]) == [4]
    dirbridge._assign_arrivals_to_existing_groups(state, [4])
    dirbridge._refresh_group_weights_from_current_assignments(state, args)
    before = list(state["group_weights"])
    assert dirbridge._record_arrivals(state, [4]) == []
    assert state["arrival_count"][4] == 2
    dirbridge._refresh_group_weights_from_current_assignments(state, args)
    assert state["group_weights"] == before
    assert coverage_bound(5, 8) == 0.75


def test_unknown_population_mass_is_not_zero_without_reference():
    assert uninitialized_group_mass([0, 1], [True, False], 2, None) is None
    assert uninitialized_group_mass([0, 1], [True, False], 2, [0.5, 0.5]) == 0.5


def test_oracle_rng_isolation_and_strict_missing_reference():
    random.seed(10)
    np.random.seed(10)
    torch.manual_seed(10)
    expected = (random.random(), float(np.random.rand()), float(torch.rand(1)))
    random.seed(10)
    np.random.seed(10)
    torch.manual_seed(10)
    with dirbridge._preserve_measurement_rng():
        random.random()
        np.random.rand()
        torch.rand(1)
    after = (random.random(), float(np.random.rand()), float(torch.rand(1)))
    assert expected == after

    args = _args(e2_weight_source="oracle")
    state = _state()
    state["oracle_features"] = [None] * 8
    try:
        dirbridge._update_e2_group_weights(
            state, args, [0, 1], [0, 1], state["group_centroids"]
        )
    except RuntimeError:
        pass
    else:
        raise AssertionError("missing oracle reference did not fail")


def test_eval_health_diagnostics_and_metric_row():
    class NaNOnSecondBatch(nn.Module):
        def __init__(self):
            super().__init__()
            self.calls = 0

        def forward(self, x):
            self.calls += 1
            out = torch.zeros((x.shape[0], 2), dtype=x.dtype)
            if self.calls == 2:
                out.fill_(float("nan"))
            return out

    dataset = TensorDataset(torch.ones(4, 1), torch.zeros(4, dtype=torch.long))
    args = _args()
    accuracy, loss, diagnostics = test_img(
        NaNOnSecondBatch(), dataset, args, return_diagnostics=True
    )
    assert math.isfinite(accuracy)
    assert not diagnostics["eval_loss_finite"]
    assert diagnostics["eval_nonfinite_logit_batches"] == 1
    assert not diagnostics["eval_predictions_valid"]

    with tempfile.TemporaryDirectory() as tmp:
        output = str(Path(tmp) / "run-test_acc.txt")
        args.system_metrics_log_dir = tmp
        metrics_path = build_system_metrics_path(args, output)
        state = _state()
        state["e2_init_mode"] = "online"
        state["e2_last_weight_source"] = "unique_client"
        state["e2_metrics"] = {
            "seen_clients": 5,
            "seen_ratio": 0.625,
            "clustered_clients": 5,
            "coverage_bound": 0.75,
            "weight_l1_status": "reference_unavailable",
            "uninit_group_mass": None,
        }
        state["last_eval_diagnostics"] = diagnostics
        log_system_metrics(args, state, metrics_path, 0.0, 0.1)
        with open(metrics_path, newline="") as handle:
            row = next(csv.DictReader(handle))
        assert row["e2_init_mode"] == "online"
        assert row["e2_weight_source"] == "unique_client"
        assert row["e2_seen_clients"] == "5"
        assert row["e2_eval_loss_finite"] == "False"
        assert row["e2_eval_predictions_valid"] == "False"


def test_bn_buffers_are_synced_but_batch_counter_is_not():
    model = nn.Sequential(nn.BatchNorm1d(2))
    exported = model_param_dict(model)
    assert "0.running_mean" in exported
    assert "0.running_var" in exported
    assert "0.num_batches_tracked" not in exported
    exported["0.running_var"].fill_(3.0)
    load_param_dict_(model, exported)
    assert torch.allclose(model[0].running_var, torch.full((2,), 3.0))


if __name__ == "__main__":
    test_inflight_isolation_and_exactly_once_materialization()
    test_first_arrival_without_recluster_is_assigned_and_used()
    test_duplicate_events_and_weight_refresh_semantics()
    test_unknown_population_mass_is_not_zero_without_reference()
    test_oracle_rng_isolation_and_strict_missing_reference()
    test_eval_health_diagnostics_and_metric_row()
    test_bn_buffers_are_synced_but_batch_counter_is_not()
    print("e2_correctness_regression=PASS")
