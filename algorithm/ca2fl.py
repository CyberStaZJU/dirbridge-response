# algorithms/ca2fl_algo.py
import copy
import numpy as np
import torch
try:
    import torch_npu
except ImportError:
    pass
import random
from models.local_update import LocalSGD
from utils.aggregation import buffered_aggregation
from utils.state_dict_ops import (
    sd_copy,
    sd_sub,
    load_param_dict_,
    model_param_dict,
    sd_zero_like,
)


def _cache_mean_full_scan(cache, num_users):
    """Reference cache mean used for initialization and equivalence tests."""
    mean = sd_zero_like(cache[0])
    for client_cache in cache:
        for key in mean:
            mean[key].add_(client_cache[key], alpha=1.0 / float(num_users))
    return mean


def _ensure_cache_mean(state, num_users):
    """Return the maintained h_t, backfilling it for legacy state objects."""
    if state.get('cache_mean') is None:
        state['cache_mean'] = _cache_mean_full_scan(state['cache'], num_users)
    return state['cache_mean']


def _ca2fl_calibration_full_scan(cache, buffer_list, num_users, buffer_size):
    """Original full-scan calibration reference for deterministic tests."""
    calibrated = _cache_mean_full_scan(cache, num_users)
    for idx in buffer_list:
        for key in calibrated:
            calibrated[key].add_(cache[idx][key], alpha=-1.0 / float(buffer_size))
    return calibrated


def _ca2fl_calibration_incremental(state, buffer_list, num_users, buffer_size):
    """Compute CA2FL calibration from h_t in O(BP), retaining event multiplicity."""
    calibrated = sd_copy(_ensure_cache_mean(state, num_users))
    for idx in buffer_list:
        for key in calibrated:
            calibrated[key].add_(state['cache'][idx][key], alpha=-1.0 / float(buffer_size))
    return calibrated


def init_state(state, args, random_cost):
    state['delta'] = [sd_zero_like(state["w_glob"]) for _ in range(args.num_users)]
    state['cache'] = [sd_zero_like(state["w_glob"]) for _ in range(args.num_users)]
    state['cache_mean'] = sd_zero_like(state["w_glob"])
    state['cost'] = [-1 for _ in range(args.num_users)]
    state['iterations'] = 0
    
    def local_train_delta(idx):
        net = copy.deepcopy(state['net_glob']).to(args.device)
        w_start = model_param_dict(state['net_glob'], device=args.device)
        local = LocalSGD(
            args=args,
            dataset=state['dataset_train'],
            idxs=state['dict_users'][idx],
            iters=args.local_period,
            nums=state['num_samples'][idx],
        )
        w_local = local.train(net=net)
        delta = sd_sub(w_local, w_start)
        del w_start, w_local, net

        return delta

    sampled_idx = random.sample(range(args.num_users), args.concurrency)
    for idx in sampled_idx:
        state['delta'][idx] = local_train_delta(idx)
        state['cost'][idx] = random_cost(idx)
    
    return state


def run_round(state, args, dataset_train, dict_users, num_samples, random_cost):
    cost = state["cost"]
    buffer_list = []
    eta = float(args.global_lr if args.global_lr is not None else 1.0)
    num_users = int(args.num_users)
    server_v = _ca2fl_calibration_incremental(
        state, [], num_users, int(args.buffer_size)
    )

    active_list = [i for i, c in enumerate(cost) if c > 0]

    for _ in range(args.buffer_size):
        filtered_costs = [(i, c) for i, c in enumerate(cost) if i not in buffer_list and c > 0]
        idx, _ = min(filtered_costs, key=lambda x: x[1])
        buffer_list.append(idx)

    state["global_cost"] = cost[buffer_list[-1]]

    for idx in buffer_list:
        cost[idx] = -1
    state['last_buffer_list'] = list(buffer_list)
    state['last_valid_buffer_list'] = list(buffer_list)
    state['last_invalid_buffer_list'] = []
    state['last_selected_item_summary'] = []
    state['last_regrouped'] = False

    # Use the old cache values for this update, before replacing selected caches.
    server_v = _ca2fl_calibration_incremental(
        state, buffer_list, num_users, int(args.buffer_size)
    )
    weights = [1.0 / int(args.buffer_size) for _ in range(args.buffer_size)]
    selected_updates = [state["delta"][i] for i in buffer_list]
    aggregated_diff = buffered_aggregation(weights, selected_updates, state["w_glob"])

    with torch.no_grad():
        for key in aggregated_diff.keys():
            server_v[key] += aggregated_diff[key]
            state["w_glob"][key] += eta * server_v[key]

    load_param_dict_(state["net_glob"], state["w_glob"])

    for idx in buffer_list:
        old_cache = state['cache'][idx]
        new_cache = state['delta'][idx]
        for key in state['cache_mean']:
            state['cache_mean'][key].add_(
                new_cache[key] - old_cache[key],
                alpha=1.0 / float(num_users),
            )
        state['cache'][idx] = new_cache

    state["iterations"] += 1

    sampled_idx = [i for i in range(args.num_users) if i not in active_list]
    np.random.shuffle(sampled_idx)
    sampled_idx = sampled_idx[:args.buffer_size]

    for idx in sampled_idx:
        net = copy.deepcopy(state["net_glob"]).to(args.device)
        w_start = model_param_dict(state['net_glob'], device=args.device)

        local = LocalSGD(
            args=args,
            dataset=dataset_train,
            idxs=dict_users[idx],
            iters=args.local_period,
            nums=num_samples[idx]
        )
        w = local.train(net=net)

        state["delta"][idx] = sd_sub(w, w_start)
        cost[idx] = state["global_cost"] + random_cost(idx)

        del w_start, w, net

    state["cost"] = cost

    return state
