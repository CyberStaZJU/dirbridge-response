#!/usr/bin/env python3
"""Minimal public-entrypoint wiring checks for supplemental experiment flags."""

import os
import pickle
import sys
import tempfile
from argparse import Namespace

from algorithm import dirbridge
from algorithm import dispatcher
from utils.e2_online import e2_online_init, e2_weight_source
from utils.fedscale_trace import FedScaleTraceSampler
from utils.options import args_parser


def parse_flags():
    original = sys.argv
    sys.argv = [
        "main_fed.py",
        "--algo", "DirBridge",
        "--random_cost", "mild_label_correlated_hierarchical",
        "--e2_init_mode", "online",
        "--e2_weight_source", "unique_client",
        "--fedscale_profile_coupling", "label_group",
        "--dirbridge_buffer_delay_limit", "2.5",
    ]
    try:
        return args_parser()
    finally:
        sys.argv = original


def check_parser():
    args = parse_flags()
    assert args.random_cost == "mild_label_correlated_hierarchical"
    assert args.e2_init_mode == "online"
    assert args.e2_weight_source == "unique_client"
    assert args.fedscale_profile_coupling == "label_group"
    assert args.dirbridge_buffer_delay_limit == 2.5
    assert e2_online_init(args)
    assert e2_weight_source(args) == "unique_client"


def check_delay_profile():
    args = Namespace(
        random_cost="mild_label_correlated_hierarchical",
        num_users=6,
        label_correlated_group_ids=[0, 1, 2, 0, 1, 2],
        label_correlated_num_groups=3,
        seed=7,
        delay_seed=7,
    )
    groups = dispatcher._ensure_client_delay_profile(args, {})
    assert len(groups) == 6
    assert set(groups) == {"Small", "Medium", "Large"}


def check_delay_limit():
    args = Namespace(
        concurrency=40,
        buffer_size=10,
        dirbridge_buffer_delay_limit=2.5,
    )
    assert dirbridge._buffer_delay_limit(args) == 2.5


def check_inflight_materialization():
    feature = object()
    delta = {"weight": object()}
    state = {
        "delta": [None, None],
        "client_features": [None, None],
        "stamp": [-1, -1],
        "inflight": {1: {"delta": delta, "feature": feature, "stamp": 3}},
    }
    dirbridge._materialize_arrivals(state, [1])
    assert state["delta"][1] is delta
    assert state["client_features"][1] is feature
    assert state["stamp"][1] == 3
    assert 1 not in state["inflight"]


def check_fedscale_coupling():
    records = {
        str(idx): {"computation": float(idx + 1), "communication": float(idx + 2)}
        for idx in range(6)
    }
    with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as handle:
        path = handle.name
        pickle.dump(records, handle)
    try:
        args = Namespace(
            fedscale_client_profile_path=path,
            fedscale_availability_trace_path="",
            fedscale_time_scale=1.0,
            fedscale_min_duration=1e-6,
            fedscale_no_trace_wrap=False,
            fedscale_trace_exhausted_penalty=3600.0,
            fedscale_profile_sample="sorted",
            fedscale_profile_coupling="label_group",
            label_correlated_group_ids=[0, 1, 2, 0, 1, 2],
            num_users=6,
            local_bs=10,
            local_period=2,
            fedscale_upload_size_mb=1.0,
            fedscale_download_size_mb=1.0,
            seed=1,
            delay_seed=1,
            fedscale_batch_size=0,
            fedscale_local_steps=0,
            fedscale_augmentation_factor=3.0,
            fedscale_default_duration=1.0,
        )
        sampler = FedScaleTraceSampler(args)
        assert sampler.profile_coupling is not None
        assert len(sampler.profile_coupling["mapping"]) == 6
        assert sampler.metadata()["fedscale_profile_coupling"] is not None
    finally:
        os.unlink(path)


if __name__ == "__main__":
    check_parser()
    check_delay_profile()
    check_delay_limit()
    check_inflight_materialization()
    check_fedscale_coupling()
    print("public_flag_wiring=PASS")
