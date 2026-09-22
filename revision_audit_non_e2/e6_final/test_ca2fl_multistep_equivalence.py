"""Five-step full-scan versus incremental CA2FL reference test."""
import copy
import torch
from types import SimpleNamespace
from algorithm.ca2fl import (
    _cache_mean_full_scan, _ca2fl_calibration_full_scan,
    _ca2fl_calibration_incremental,
)
from utils.state_dict_ops import sd_copy


def sd(value, device):
    return {'weight': torch.tensor([value, -2 * value], dtype=torch.float64, device=device)}


def add_(dst, src, alpha=1.0):
    for k in dst: dst[k].add_(src[k], alpha=alpha)


def run(device):
    N, B = 5, 3
    cache_i = [sd(i + 1.0, device) for i in range(N)]
    inc = {'cache': [sd_copy(x) for x in cache_i], 'cache_mean': _cache_mean_full_scan(cache_i, N)}
    full = {'cache': [sd_copy(x) for x in cache_i]}
    buffers = [[0, 1, 0], [2, 4, 2], [1, 3, 4], [0, 4, 0], [3, 2, 1]]
    for step, buf in enumerate(buffers):
        full_mean = _cache_mean_full_scan(full['cache'], N)
        inc_mean = _cache_mean_full_scan(inc['cache'], N)
        for k in inc_mean: torch.testing.assert_close(inc['cache_mean'][k], inc_mean[k], rtol=0, atol=1e-12)
        full_cal = _ca2fl_calibration_full_scan(full['cache'], buf, N, B)
        inc_cal = _ca2fl_calibration_incremental(inc, buf, N, B)
        for k in full_cal: torch.testing.assert_close(inc_cal[k], full_cal[k], rtol=0, atol=1e-12)
        # Apply the same server update, then replace events in temporal order.
        for k in full_cal:
            full_mean[k].add_(full_cal[k])
            inc_mean[k].add_(inc_cal[k])
        for idx in buf:
            new = sd(10.0 + step + idx, device)
            old_full = full['cache'][idx]
            old_inc = inc['cache'][idx]
            for k in inc['cache_mean']:
                inc['cache_mean'][k].add_(new[k] - old_inc[k], alpha=1.0 / N)
            full['cache'][idx] = sd_copy(new)
            inc['cache'][idx] = sd_copy(new)
        full_mean_after = _cache_mean_full_scan(full['cache'], N)
        for k in full_mean_after:
            torch.testing.assert_close(inc['cache_mean'][k], full_mean_after[k], rtol=0, atol=1e-12)
        for idx in range(N):
            for k in inc['cache'][idx]:
                torch.testing.assert_close(inc['cache'][idx][k], full['cache'][idx][k], rtol=0, atol=1e-12)
    return True


if __name__ == '__main__':
    run('cpu')
    if torch.cuda.is_available(): run('cuda')
    print('ca2fl_multistep_equivalence=PASS')
