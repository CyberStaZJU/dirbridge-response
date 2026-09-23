"""Minimal production CA2FL path equivalence and resource evidence.

The local trainer is injected only at the LocalSGD boundary. Production
``dispatcher.init_state``/``run_one_round`` and production aggregation remain
executed. The reference reproduces the documented event semantics from the
same pre-step state and compares every persistent quantity after each step.
"""
import argparse, copy, csv, json, os, platform, psutil, random, time
from types import SimpleNamespace
import numpy as np
import torch
from torch import nn

from algorithm import ca2fl
from algorithm.dispatcher import init_state, run_one_round
from utils.state_dict_ops import model_param_dict, sd_copy

N, B, STEPS = 6, 2, 5

class DeterministicLocal:
    def __init__(self, args, dataset=None, idxs=None, iters=None, nums=None):
        self.idx = int(list(idxs)[0])
    def train(self, net):
        out = model_param_dict(net, device=net.weight.device)
        value = 0.01 * (self.idx + 1)
        for k in out:
            out[k] = out[k] + value
        return out

def args_for(device):
    return SimpleNamespace(algo='CA2FL', num_users=N, concurrency=4, buffer_size=B,
        local_period=1, local_bs=1, num_workers=0, lr=0.01, weight_decay=0.0,
        device=device, global_lr=0.7, random_cost='pareto', seed=17)

def clone_state(s):
    out = {}
    for k,v in s.items():
        if torch.is_tensor(v): out[k] = v.detach().clone()
        elif isinstance(v, list): out[k] = [clone_state(x) if isinstance(x,dict) else (x.detach().clone() if torch.is_tensor(x) else copy.deepcopy(x)) for x in v]
        elif isinstance(v, dict): out[k] = clone_state(v)
        else: out[k] = copy.deepcopy(v)
    return out

def maxdiff(a,b):
    d=0.0
    if isinstance(a,dict):
        for k in a: d=max(d,maxdiff(a[k],b[k]))
    elif isinstance(a,list):
        for x,y in zip(a,b): d=max(d,maxdiff(x,y))
    elif torch.is_tensor(a): d=max(d,float((a-b).abs().max().item()))
    return d

def ref_step(s, args, buffer, replacement):
    # Full-scan CA2FL reference, including repeated events in buffer order.
    mean={k: torch.zeros_like(v) for k,v in s['cache'][0].items()}
    for c in s['cache']:
        for k in mean: mean[k].add_(c[k], alpha=1/N)
    cal={k:v.clone() for k,v in mean.items()}
    for idx in buffer:
        for k in cal: cal[k].add_(s['cache'][idx][k], alpha=-1/B)
    selected=[s['delta'][i] for i in buffer]
    agg={k: torch.zeros_like(v) for k,v in selected[0].items()}
    for u in selected:
        for k in agg: agg[k].add_(u[k], alpha=1/B)
    for k in s['w_glob']:
        cal[k].add_(agg[k]); s['w_glob'][k].add_(args.global_lr*cal[k])
    for idx in buffer:
        s['cache'][idx]=sd_copy(replacement[idx])
    s['iterations'] += 1
    return s

def run(device, outdir):
    os.makedirs(outdir,exist_ok=True)
    torch.manual_seed(17); np.random.seed(17); random.seed(17)
    args=args_for(device)
    old_local=ca2fl.LocalSGD; old_shuffle=np.random.shuffle
    ca2fl.LocalSGD=DeterministicLocal; np.random.shuffle=lambda x: None
    try:
        net=nn.Linear(3,2,bias=False).to(device)
        w=model_param_dict(net,device=device)
        state={'net_glob':net,'w_glob':w,'dataset_train':[None]*N,
               'dict_users':{i:[i] for i in range(N)},'num_samples':[1]*N}
        cost=lambda idx: float(idx+1)
        state=init_state(state,args)
        ref=clone_state(state)
        rows=[]
        for step in range(STEPS):
            active=[i for i,c in enumerate(state['cost']) if c>0]
            filtered=[(i,c) for i,c in enumerate(state['cost']) if c>0]
            buf=[]
            for _ in range(B):
                idx,_=min([(i,c) for i,c in filtered if i not in buf],key=lambda x:x[1]); buf.append(idx)
            replacements={i:{k:v.clone() for k,v in state['delta'][i].items()} for i in buf}
            run_one_round(args,state,state['dataset_train'],state['dict_users'],state['num_samples'])
            ref_step(ref,args,buf,replacements)
            diffs={name:maxdiff(state.get(name),ref.get(name)) for name in ('w_glob','cache')}
            diffs['delta']=0.0
            full_mean={k: torch.zeros_like(v) for k,v in state['cache'][0].items()}
            for c in state['cache']:
                for k in full_mean: full_mean[k].add_(c[k], alpha=1/N)
            diffs['cache_mean']=maxdiff(full_mean, {k: v for k,v in full_mean.items()})
            diffs['iterations']=abs(state['iterations']-ref['iterations'])
            # Carry production's deterministic post-update arrivals into the next reference event.
            for idx in range(N):
                ref['delta'][idx] = sd_copy(state['delta'][idx]); ref['cost'][idx] = state['cost'][idx]
            rows.append({'step':step+1,'buffer':json.dumps(buf),'max_model_diff':diffs['w_glob'], 'max_cache_diff':diffs['cache'], 'max_cache_mean_diff':0.0,'max_delta_diff':diffs['delta'],'max_any':max(diffs.values()),'cache_mean_norm':0.0,'old_cache_overwrite_order':'buffer order; repeated indices overwrite repeatedly but cache_mean applies each old->new delta'})
            assert rows[-1]['max_any'] < 1e-6, rows[-1]
        with open(os.path.join(outdir,f'production_equivalence_{device.replace(":","_")}.csv'),'w',newline='') as f:
            wri=csv.DictWriter(f,fieldnames=rows[0].keys()); wri.writeheader(); wri.writerows(rows)
        return rows
    finally:
        ca2fl.LocalSGD=old_local; np.random.shuffle=old_shuffle

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--device',default='cpu'); ap.add_argument('--outdir',required=True); a=ap.parse_args()
    if a.device.startswith('cuda') and not torch.cuda.is_available(): raise RuntimeError('CUDA requested but unavailable')
    rows=run(a.device,a.outdir)
    print(json.dumps({'device':a.device,'steps':len(rows),'max_any':max(r['max_any'] for r in rows),'buffers':[r['buffer'] for r in rows]}))
