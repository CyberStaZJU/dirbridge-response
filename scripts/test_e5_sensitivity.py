"""Deterministic E5 threshold and K0=1 aggregation checks."""
from types import SimpleNamespace
import torch

from algorithm.dirbridge import _build_ema_group_updates, _buffer_delay_limit, grouped_buffered_aggregation


def _sd(value):
    return {'weight': torch.tensor([float(value)], dtype=torch.float64)}


def test_threshold_override_changes_membership():
    state = {
        'iterations': 4,
        'num_groups': 1,
        'stamp': [0, 2, 4],
        'group_ids': [0, 0, 0],
        'group_counts': [3],
        'group_weights': [1.0],
        'delta': [_sd(1), _sd(2), _sd(3)],
        'w_glob': _sd(0),
        'group_cache_stamp': [-1],
        'group_cache': [_sd(0)],
        'group_cache_delay': [0.0],
    }
    base = dict(num_groups=1, buffer_size=2, concurrency=40, dirbridge_buffer_delay_limit=None)
    args_default = SimpleNamespace(**base)
    args_override = SimpleNamespace(**{**base, 'dirbridge_buffer_delay_limit': 1.5})
    assert _buffer_delay_limit(args_default) == 20.0
    assert _buffer_delay_limit(args_override) == 1.5
    _build_ema_group_updates(state, args_override, [1, 2])
    assert state['last_valid_buffer_list'] == [2]
    assert state['last_invalid_buffer_list'] == [1]


def test_k1_matches_mean_buffer_for_two_steps():
    state = {
        'iterations': 0,
        'num_groups': 1,
        'stamp': [0, 0, 0],
        'group_ids': [0, 0, 0],
        'group_counts': [3],
        'group_weights': [1.0],
        'delta': [_sd(1), _sd(3), _sd(5)],
        'group_cache_stamp': [-1],
        'group_cache': [_sd(0)],
        'group_cache_delay': [0.0],
    }
    args = SimpleNamespace(num_groups=1, buffer_size=3, concurrency=40,
                           dirbridge_buffer_delay_limit=100.0, dirbridge_cache_beta=0.9)
    for buffer in ([0, 1, 2], [1, 2, 0]):
        selected = _build_ema_group_updates(state, args, list(buffer))
        got = grouped_buffered_aggregation(selected, _sd(0))['weight']
        expected = torch.tensor([sum(state['delta'][i]['weight'] for i in buffer) / 3.0])
        assert torch.allclose(got, expected)
        state['iterations'] += 1


if __name__ == '__main__':
    test_threshold_override_changes_membership()
    test_k1_matches_mean_buffer_for_two_steps()
    print('e5_sensitivity=PASS')
