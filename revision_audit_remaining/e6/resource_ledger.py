"""Measure live production states; storage identity never crosses snapshots."""
import argparse
import csv
import gc
import json
import random
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
import psutil
import torch
from torch import nn
from algorithm import ca2fl, dirbridge, fadas, fedbuff, dispatcher
from utils.state_dict_ops import model_param_dict

METHODS = {'FedBuff': fedbuff, 'CA2FL': ca2fl, 'DirBridge': dirbridge, 'FADAS': fadas}
SHARED = {'net_glob', 'w_glob', 'dataset_train', 'dict_users', 'num_samples',
          'delta', 'stamp', 'cost', 'delays', 'global_cost', 'iterations'}


class Local:
    def __init__(self, args, dataset=None, idxs=None, **kwargs):
        self.idx = int(list(idxs)[0])

    def train(self, net):
        out = model_param_dict(net)
        return {k: v + .001 * (self.idx + 1) for k, v in out.items()}


def walk(obj, path, rows, seen, context, ownership):
    base = dict(context, path=path, ownership=ownership, kind='', shape='', dtype='',
                device='', storage_ptr='', storage_offset='', storage_bytes=0,
                logical_bytes=0, unique_physical_bytes=0, alias_of='', python_shallow_bytes=0)
    if torch.is_tensor(obj):
        storage = obj.untyped_storage()
        key = (str(obj.device), storage.data_ptr())
        base.update(kind='tensor', shape=str(tuple(obj.shape)), dtype=str(obj.dtype),
                    device=str(obj.device), storage_ptr=storage.data_ptr(),
                    storage_offset=obj.storage_offset(), storage_bytes=storage.nbytes(),
                    logical_bytes=obj.numel() * obj.element_size(),
                    unique_physical_bytes=0 if key in seen else storage.nbytes(),
                    alias_of=seen.get(key, ''))
        seen.setdefault(key, path)
        rows.append(base)
    elif isinstance(obj, nn.Module):
        for key, value in obj.state_dict().items():
            walk(value, f'{path}.{key}', rows, seen, context, ownership)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            walk(value, f'{path}.{key}', rows, seen, context, ownership)
    elif isinstance(obj, (list, tuple)):
        base.update(kind=type(obj).__name__ + '_metadata', python_shallow_bytes=sys.getsizeof(obj))
        rows.append(base)
        for i, value in enumerate(obj):
            walk(value, f'{path}[{i}]', rows, seen, context, ownership)


def args_for(method, device):
    return SimpleNamespace(algo=method, num_users=6, concurrency=4, buffer_size=2,
        local_period=1, local_bs=1, num_workers=0, lr=.01, weight_decay=0.,
        device=device, global_lr=.1, random_cost='dir-skew', seed=19,
        dirbridge_num_groups=2, dirbridge_sketch_dim=8, dirbridge_kmeans_iters=2,
        dirbridge_feature_mode='count_sketch', dirbridge_count_sketch_seed=21)


def reset(device):
    if device.startswith('cuda'):
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()


def capture(state, method, device, phase, rows, runtime):
    if device.startswith('cuda'):
        torch.cuda.synchronize()
    context = dict(method=method, run_device=device, phase=phase)
    # Shared allocations are attributed first; subsequent references are aliases.
    seen = {}
    for shared in (True, False):
        for key, value in state.items():
            is_shared = key in SHARED or key.startswith('last_')
            if is_shared == shared:
                walk(value, 'state.' + key, rows, seen, context,
                     'shared' if shared else 'method_owned')
    runtime.append(dict(context, rss_bytes=psutil.Process().memory_info().rss,
        cuda_allocated_bytes=torch.cuda.memory_allocated() if device.startswith('cuda') else '',
        cuda_reserved_bytes=torch.cuda.memory_reserved() if device.startswith('cuda') else '',
        cuda_max_allocated_bytes=torch.cuda.max_memory_allocated() if device.startswith('cuda') else '',
        cuda_max_reserved_bytes=torch.cuda.max_memory_reserved() if device.startswith('cuda') else '',
        peak_interval='reset before model/init' if phase == 'init' else 'reset before five events',
        sync='before reset and capture' if device.startswith('cuda') else 'not applicable'))


def alias_regression(device):
    x = torch.arange(8, device=device)
    rows = []
    walk({'base': x, 'offset_view': x[2:]}, 'probe', rows, {}, {}, 'probe')
    assert sum(r['unique_physical_bytes'] for r in rows) == x.untyped_storage().nbytes()
    assert rows[1]['storage_offset'] == 2 and rows[1]['alias_of'] == 'probe.base'
    fresh = []
    walk(x, 'independent_snapshot', fresh, {}, {}, 'probe')
    assert fresh[0]['unique_physical_bytes'] == x.untyped_storage().nbytes()


def write_csv(path, rows):
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--outdir', type=Path, required=True)
    parser.add_argument('--device', choices=['cpu', 'cuda'], required=True)
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    if args.device == 'cuda':
        assert torch.cuda.is_available(), 'CUDA requested but unavailable'
    alias_regression(args.device)
    rows, runtime = [], []
    for method, module in METHODS.items():
        gc.collect()
        reset(args.device)
        torch.manual_seed(19)
        random.seed(19)
        np.random.seed(19)
        net = nn.Linear(4, 2, bias=False).to(args.device)
        config = args_for(method, args.device)
        state = dict(net_glob=net, w_glob=model_param_dict(net), dataset_train=[None]*6,
                     dict_users={i: [i] for i in range(6)}, num_samples=[1]*6, global_cost=0)
        with patch.object(module, 'LocalSGD', Local), patch.object(
                dispatcher, '_random_cost', lambda *a: lambda idx: float(idx+1)):
            state = dispatcher.init_state(state, config)
            capture(state, method, args.device, 'init', rows, runtime)
            reset(args.device)
            for _ in range(5):
                dispatcher.run_one_round(config, state, state['dataset_train'],
                                         state['dict_users'], state['num_samples'])
            capture(state, method, args.device, 'after5', rows, runtime)
        del state, net
    write_csv(args.outdir / f'ledger_{args.device}.csv', rows)
    write_csv(args.outdir / f'runtime_{args.device}.csv', runtime)
    print(json.dumps(dict(device=args.device, methods=list(METHODS), phases=['init', 'after5'],
                          tensor_rows=sum(r['kind']=='tensor' for r in rows),
                          alias_regression='PASS', torch=torch.__version__, cuda=torch.version.cuda)))


if __name__ == '__main__':
    main()
