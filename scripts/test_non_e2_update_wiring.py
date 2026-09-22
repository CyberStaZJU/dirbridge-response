#!/usr/bin/env python3
"""Deterministic non-E2 server-step, CA2FL, and FADAS checks."""

from argparse import Namespace
import inspect

import torch
import torch.nn as nn

from algorithm import ca2fl, dirbridge, fadas, fedbuff


class _OneParameterModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.weight = nn.Parameter(torch.zeros(1, dtype=torch.float64))


def _args(global_lr=0.5):
    return Namespace(
        global_lr=global_lr,
        lr=0.01,
        fadas_beta1=0.0,
        fadas_beta2=0.0,
        fadas_eps=1e-8,
        fadas_delay_adaptive=False,
        fadas_tau_c=1,
    )


def _state_dict(value):
    return {"weight": torch.tensor([value], dtype=torch.float64)}


def check_server_learning_rate_wiring():
    for module in (fedbuff, dirbridge):
        source = inspect.getsource(module.run_round)
        assert "server_lr" in source
        assert "server_lr * aggregated_diff[key]" in source or "server_lr * aggregated_diff" in source


def check_ca2fl_incremental_equivalence():
    cache = [_state_dict(1.0), _state_dict(3.0), _state_dict(5.0), _state_dict(7.0)]
    state = {"cache": cache, "cache_mean": ca2fl._cache_mean_full_scan(cache, 4)}
    buffer = [1, 1, 3]
    full = ca2fl._ca2fl_calibration_full_scan(cache, buffer, 4, 3)
    inc = ca2fl._ca2fl_calibration_incremental(state, buffer, 4, 3)
    assert torch.allclose(full["weight"], inc["weight"])
    replacement = _state_dict(11.0)
    old = state["cache"][2]
    with torch.no_grad():
        state["cache_mean"]["weight"].add_(
            replacement["weight"] - old["weight"], alpha=0.25
        )
    state["cache"][2] = replacement
    rebuilt = ca2fl._cache_mean_full_scan(state["cache"], 4)
    assert torch.allclose(state["cache_mean"]["weight"], rebuilt["weight"])


def check_fadas_formula():
    state = {
        "w_glob": _state_dict(0.0),
        "net_glob": _OneParameterModel(),
        "fadas_m": _state_dict(0.0),
        "fadas_v": _state_dict(0.0),
        "fadas_vhat": _state_dict(0.0),
        "fadas_param_keys": {"weight"},
    }
    args = _args(0.5)
    delta = _state_dict(2.0)
    fadas._update_adaptive_moments(state, args, delta)
    fadas._apply_adaptive_update(state, args, 0.5, delta)
    expected = 0.5 * 2.0 / (4.0 ** 0.5 + args.fadas_eps)
    assert abs(float(state["w_glob"]["weight"]) - expected) < 1e-9


if __name__ == "__main__":
    check_server_learning_rate_wiring()
    check_ca2fl_incremental_equivalence()
    check_fadas_formula()
    print("non_e2_update_wiring=PASS")
