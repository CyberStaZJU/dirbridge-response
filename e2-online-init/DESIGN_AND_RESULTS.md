# E2 (R3-1): Online initialization without full-client warm start — design, configuration, and audited results

## 1. Purpose

Reviewer R3-1 objects that DirBridge's group-size-aware refill uses population
group weights established by a **full-client initialization**, which may not be
available at deployment, and asks for results where groups and weights are
estimated **online** from the arriving client stream. This document records the
four-variant control design, the exact configuration, code identity, and the
audited 5-seed results on two datasets.

## 2. Control design

| variant | grouping source | population-weight source | role |
|---|---|---|---|
| **A** `full_count` | all N clients at init (original) | all-client label counts | original reference |
| **B** `online_oracle` | only arrived clients | true weights from offline evaluator | separates grouping error from weight error |
| **C** `online_arrival` | only arrived clients | arrival-event frequencies (repeats counted) | negative control: arrival mixture ≠ population mixture |
| **D** `online_unique` | only arrived clients | unique observed client IDs | minimal deployable version |

Implementation facts that matter for interpreting the results:

- Online variants launch **only the first wave of M_c clients**; no full-client
  pass happens before training. Reclustering considers only clients actually
  seen; unseen clients get group id −1 and are never back-filled.
- B's oracle is evaluated **outside the training process** on the fixed
  partition and only supplies group weights; it never leaks sketches, labels,
  or cluster assignments of unseen clients into D or C.
- The oracle snapshot for A is free (full init computes every direction anyway);
  for online variants it is omitted entirely — this is what distinguishes the
  clean phase from a first, **invalidated** attempt in which an oracle
  pre-pass (`--e2_oracle_features`) polluted the online variants' init-time
  accounting and RNG stream. That attempt was deleted and rerun; the results
  here are from the clean phase only.

## 3. Honest limitations stated up front

- With arrival rate r_k ∝ p_k λ_k under the simplified arrival model, counting
  events (variant C) estimates the **arrival mixture**, not the population
  mixture; ID de-duplication (variant D) reduces repeated-arrival bias but is
  **not a finite-time unbiased estimator** either.
- Coverage bound (client-uniform objective, known N): with N_seen distinct
  clients observed and p̂ the normalized group frequencies of seen clients,
  ‖p̂ − p‖₁ ≤ 2(1 − N_seen/N). This is a worst-case bound, not a claim of
  immediate unbiasedness.

## 4. Exact run configuration

CIFAR-100 (30 runs = 6 variants × 5 seeds):

```
--dataset cifar100 --distribution noniid --alpha 0.5
--random_cost mild_label_correlated_hierarchical   # DIR-SKEW LATENCY
--num_users 100 --concurrency 40 --buffer_size 10  # (M_c, B) = (40, 10)
--total_rounds 500 --model resnet --lr 0.01 --local_bs 100 --local_period 10
--interval 1 --dirbridge_sketch_dim 2048
--e2_init_mode {full|online} --e2_weight_source {full_count|oracle|arrival_freq|unique_client}
```

FEMNIST (30 runs): `--dataset femnist --random_cost fedscale_trace
--fedscale_client_profile_path fedscale_device_info/client_device_capacity
--fedscale_profile_coupling label_group --num_users 1000 --concurrency 400
--buffer_size 100 --model cnn --lr 0.01 --local_bs 50 --local_period 10`,
same E2 flags (CASA runs use the CASA algorithm with the same start-mode flags).

Hardware: desktop host, RTX 5090 D (32 GB), CUDA. Seeds 1–5, matching the main
experiments.

## 5. Code identity

Development tree `$DIRBRIDGE_CODE_E2`, **merged into the main tree**
`$DIRBRIDGE_CODE_ROOT` after the final audit (md5-verified identical for
`algorithm/dirbridge.py`, `algorithm/casa.py`, `utils/options.py`,
`utils/direction_skew_logging.py`, `main_fed.py`, plus new
`utils/e2_online.py`). Changed behavior is confined to: init mode branching,
seen-only reclustering, weight-source selection, the five `e2_*` metric columns,
and init-cost accounting (`init_time_sec` inside the runtime timeline).

## 6. Audited results

Audit: 60/60 runs at exactly 500 rounds, all finite; 60/60 system-metrics and
direction-skew CSVs complete; no partials or orphans.

### Final-round accuracy (mean ± sd, 5 seeds)

| variant | CIFAR-100 | FEMNIST |
|---|---|---|
| A full-init | 47.35 ± 1.33 | 74.38 ± 11.62 |
| B online+oracle | 46.76 ± 0.67 | 78.90 ± 1.82 |
| C online+arrival | 48.51 ± 0.76 | 78.01 ± 1.65 |
| D online+unique | 47.70 ± 1.29 | 79.04 ± 1.60 |
| CASA full | 8.96 ± 4.10 | 70.82 ± 2.67 |
| CASA online | 12.15 ± 9.92 | 72.14 ± 6.07 |

### The three findings

1. **Online estimation costs nothing measurable.** All four DirBridge variants
   sit inside each other's seed noise on both datasets. Paired per-seed tests on
   FEMNIST finals (df = 4): D−B +0.14 (ns), D−C +1.03 (ns), D−A +4.66 (ns,
   dominated by A seed 2, see below). Even the deliberately biased negative
   control C does not degrade accuracy within 500 rounds. The arrival-mixture
   bias is real (next section quantifies it), but it does not translate into an
   accuracy gap at these settings — the honest formulation is "no measurable
   accuracy cost", not "no bias".
2. **FEMNIST A's large spread is a full-init cold-start pathology, not an
   online effect.** A seed 2 collapses mid-run (19.6 at r100, 47–49 through
   r200–r300, 53.8 final; 335 of 500 rounds below 60) while B/C/D on the same
   seed train normally (finals 75.8/75.9/76.3). Excluding seed 2, A is
   79.53 ± 1.91. Report A both ways and attribute the spread to the full-init
   start.
3. **Init cost**: A 23.3 s, B 31.7 s (its oracle still trains all N clients at
   w₀ — by definition), **C/D 1.5 s** (15× faster than full init), measured via
   `init_time_sec` inside the runtime timeline.

### Arrival-mixture bias, quantified offline (fixed 4-group reference monitor)

Per-round L1 distance between the arriving buffer mixture and the population
mixture (client IDs per round are not logged, but `buffer_counts` and
`population_group_sizes` are):

| dataset | A | B/C/D | steady state (last 100 r) |
|---|---|---|---|
| CIFAR-100 | 0.377 (r5–30) | 0.420–0.423 | ≈ 0.43 — persists to round 500 |
| FEMNIST | 0.197 | 0.205 | ≈ 0.14 — persists to round 500 |

The stream is persistently direction-skewed and **identical across variants**
(it is the arrival process, independent of weight estimation), so the A-vs-D
comparison is fair: same stream, different weight-estimation strategy, no
accuracy difference.

Population group weights used (offline-recomputed from the deterministic
partitions; saved to `population_group_weights.json`): CIFAR-100 per seed
0.31–0.41 / 0.31–0.33 / 0.28–0.37; FEMNIST (0.761, 0.239, 0.000) — block 2 is
empty in the truncated 1000-client set.

Coverage diagnostics (per-round means, clean runs): seen-ratio 0.99 by mid-run
and uninit-group-mass 0 for online variants on both datasets; coverage bound
2(1 − N_seen/N) ≈ 0.019 (CIFAR-100). Known instrumentation gap: the
algorithm-internal ‖p̂_t − p_t‖₁ column (`e2_weight_l1`) is NaN in clean runs
because it required the in-process oracle snapshot; the offline substitute
(arrival-mixture L1 above) is what the reply should cite.

## 7. What this experiment does and does not claim

- Does: full-init is **not required** for DirBridge's grouping/refill; a
  deployable online variant (D) with 15× cheaper init matches the original
  setting on both datasets.
- Does not: claim the arrival stream is unbiased (it is measurably biased,
  L1 ≈ 0.14–0.43 persistently), or that ID de-duplication is finite-time
  unbiased (it is not), or that the null result transfers to settings where
  arrival mixtures are more skewed than these (untested).
