"""Numerical E5 gate and cached K0=1 aggregation checks; no training."""
from types import SimpleNamespace
import torch
from algorithm.dirbridge import (
    _build_ema_group_updates, _buffer_delay_limit,
    _update_ema_group_cache, grouped_buffered_aggregation,
)
from utils.state_dict_ops import sd_average


def sd(value):
    return {'weight': torch.tensor([value, -value], dtype=torch.float64)}


def state_for(delays):
    return dict(iterations=10, num_groups=1, stamp=[10-d for d in delays],
                group_ids=[0]*len(delays), group_counts=[len(delays)],
                group_weights=[1.0], delta=[sd(i+1) for i in range(len(delays))],
                w_glob=sd(0), group_cache_stamp=[-1], group_cache=[sd(99)],
                group_cache_delay=[0.0])


def test_threshold_override_changes_membership():
    for b, expected_rule in [(5, 8), (10, 4), (20, 2)]:
        state = state_for([1, 2, 3, 4, 5, 8, 9])
        args = SimpleNamespace(buffer_size=b, concurrency=40,
                               dirbridge_buffer_delay_limit=None)
        assert _buffer_delay_limit(args) == expected_rule
        _build_ema_group_updates(state, args, list(range(7)))
        assert state['last_valid_buffer_list'] == [
            i for i, d in enumerate([1, 2, 3, 4, 5, 8, 9]) if d <= expected_rule]
        args.dirbridge_buffer_delay_limit = 4.0
        _build_ema_group_updates(state, args, list(range(7)))
        assert state['last_valid_buffer_list'] == [0, 1, 2, 3]


def test_k1_matches_mean_buffer_for_two_steps():
    state = state_for([0, 2, 5])
    args = SimpleNamespace(buffer_size=3, concurrency=40,
                           dirbridge_buffer_delay_limit=4.0,
                           dirbridge_cache_beta=0.9, global_lr=0.37)
    reference_model = sd(0)
    for step in range(2):
        state['delta'] = [sd((step+1)*(i+1)) for i in range(3)]
        selected = _build_ema_group_updates(state, args, [0, 1, 2])
        valid = state['last_valid_buffer_list']
        assert valid == [0, 1]
        assert selected[0]['cache_fill_count'] == 0.0
        # sd_average is the actual FedBuff aggregation function.
        expected = sd_average([state['delta'][i] for i in valid])
        actual = grouped_buffered_aggregation(selected, state['w_glob'])
        for key in actual:
            torch.testing.assert_close(actual[key], expected[key], rtol=0, atol=1e-12)
            state['w_glob'][key] += args.global_lr * actual[key]
            reference_model[key] += args.global_lr * expected[key]
            torch.testing.assert_close(state['w_glob'][key], reference_model[key], rtol=0, atol=1e-12)
        _update_ema_group_cache(state, args, selected)
        assert state['group_cache_stamp'][0] >= 0
        state['iterations'] += 1
    print('k1_two_steps_cache_and_displacement=PASS')


if __name__ == '__main__':
    test_threshold_override_changes_membership()
    test_k1_matches_mean_buffer_for_two_steps()
    print('e5_sensitivity=PASS')
