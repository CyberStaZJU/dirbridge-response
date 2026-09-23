#!/usr/bin/env python3
"""CPU-only endpoint replay using the production min-arrival scheduler semantics."""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
import numpy as np
from utils.aggregation import build_client_delay_profile, sample_client_delay
from utils.mild_skew_assignment import assign_delay_bank, assert_assignment_invariants


def make_bank(n, seed):
    groups, _ = build_client_delay_profile(n, seed=seed)
    rng = np.random.default_rng(seed + 1)
    return np.asarray([sample_client_delay(groups, i, "mild_label_correlated_hierarchical", rng) for i in range(n)])


def replay(delays, scores, mc, b, rounds, mode, seed):
    assigned, order = assign_delay_bank(delays, mode, seed, scores)
    assert_assignment_invariants(delays, assigned, order)
    active = [(float(assigned[i]), i, 0) for i in range(len(assigned))]
    events=[]
    rng=np.random.default_rng(seed+19)
    for r in range(rounds):
        active.sort()
        batch=active[:b]
        active=active[b:]
        t=max(x[0] for x in batch)
        for arrival, idx, stamp in batch:
            events.append((r, idx, t, r-stamp, float(scores[idx]), mode))
        # production scheduler launches the next unavailable clients after the batch
        for idx in rng.permutation(len(assigned)):
            if len(active) >= mc: break
            if all(idx != x[1] for x in active):
                active.append((t+float(assigned[idx]), int(idx), r+1))
    return events, assigned, order


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out-dir', required=True); p.add_argument('--seed', type=int, default=2)
    p.add_argument('--num-users', type=int, default=100); p.add_argument('--concurrency', type=int, default=40)
    p.add_argument('--buffer-size', type=int, default=10); p.add_argument('--rounds', type=int, default=200)
    p.add_argument('--direction-scores', required=True, help='CSV with client,direction_score from fixed reference updates')
    a=p.parse_args(); out=Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    scores=np.full(a.num_users, np.nan)
    with open(a.direction_scores, newline='') as f:
        for row in csv.DictReader(f): scores[int(row['client'])]=float(row['direction_score'])
    if not np.isfinite(scores).all(): raise SystemExit('direction reference is incomplete')
    delays=make_bank(a.num_users,a.seed)
    allrows=[]
    for mode in ('original','random','sorted'):
        rows, assigned, order=replay(delays,scores,a.concurrency,a.buffer_size,a.rounds,mode,a.seed)
        allrows.extend(rows)
        with open(out/f'assign_{mode}.csv','w',newline='') as f:
            w=csv.writer(f); w.writerow(['client','delay','order']); w.writerows(zip(range(a.num_users),assigned,order))
    with open(out/'events.csv','w',newline='') as f:
        w=csv.writer(f); w.writerow(['round','client','arrival','staleness','direction_score','assignment']); w.writerows(allrows)
    with open(out/'identity.json','w') as f: json.dump(vars(a),f,indent=2)

if __name__=='__main__': main()
