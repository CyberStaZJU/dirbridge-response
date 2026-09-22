# E4 (R3-2): Profile-coupled delay experiment — design, configuration, and audited results

> **Interpretation correction (supersedes the historical wording below):** This file records a controlled data–system coupling experiment driven by real FedScale device-capability profiles. It is not evidence of naturally observed label–latency coupling or measured end-to-end latency. The statistical and resource corrections in `revision_audit_non_e2/E4_REANALYSIS.md` supersede older narrative claims in this document, including “higher more often,” cross-dataset monotonicity, and unsupported persistent-memory explanations.

## 1. Purpose

Reviewer question R3-2 asks whether DirBridge's gains depend on the *specific* way data
heterogeneity and delay heterogeneity are coupled. To answer this, we replaced the
original Dir-Skew group-to-speed mapping with a **data-driven, profile-only coupling**
built from real FedScale device profiles, and re-ran the full 7-algorithm × 5-seed
matrix on FEMNIST and GSpeech.

This document is the authoritative record of the coupling design, exact run
configuration, code identity, and the audited 5-seed results. All runs were executed on
the desktop GPU host (NVIDIA GeForce RTX 5090 D, 32 GB; CUDA), one dataset at a time.

## 2. Coupling design

Implemented in `code/fedscale_profile_coupling.py` (imported by `utils/fedscale_trace.py`
when `--fedscale_profile_coupling label_group` is set).

1. **Profile features.** Load the FedScale client-device-capacity profile (500,000
   valid records). Keep records with finite, positive `computation` (ms/sample) and
   `communication` (bandwidth). Features are `[log(computation), log(communication)]`,
   standardized to zero mean and unit variance.
2. **Clustering.** Custom Lloyd K-means, `k=3`, seeded by the run's RNG seed (deterministic
   per seed). Cluster identity is **profile-only**: no label information enters this step.
3. **Class ordering.** Sort the three clusters by the median FedScale completion-time
   proxy `3.0 * batch_size * local_steps * computation / 1000 + (upload+download)/communication`
   (fast → slow), so "class 0" is the fastest profile group.
4. **Group-to-class bijection.** A seed-controlled random permutation
   (`numpy.default_rng(seed + 104729)`) maps label direction groups {0,1,2} to profile
   classes. This preserves the experiment's requirement that the coupling be
   *reproducible but not hand-designed*: any label group can be matched to fast, mid, or
   slow profiles depending on the seed.
5. **Within-class assignment.** Clients whose data belongs to label group *g* receive
   profiles from the mapped class, assigned in increasing per-profile completion-time
   order (sorted pairing). When a class has fewer profiles than clients in its mapped
   group, profiles are reused cyclically and the reuse count is recorded.

The mapping (per client: label group → profile id, class, duration, cycled flag) is
computed once at trace initialization and embedded in the run metadata
(`fedscale_profile_coupling` field), so every run carries a full record of its actual
data–delay coupling.

**Distinction from the original Dir-Skew:** the original mode couples label groups to
*speed groups* through a seed-controlled permutation over synthesized speed groups. The
new mode replaces the synthesized speed groups with clusters discovered from real
FedScale profiles (log-compute, log-bandwidth), and selects actual profile rows
(including their communication component) rather than only a speed tier.

## 3. Exact run configuration

Common to both datasets (all 7 algorithms × 5 seeds × 2 datasets = 70 runs):

```
--distribution noniid --alpha 0.5 --random_cost fedscale_trace
--num_users 1000 --concurrency 400 --buffer_size 100 --total_rounds 500
--interval 1
--fedscale_client_profile_path fedscale_device_info/client_device_capacity
--fedscale_profile_coupling label_group
```

Per-dataset differences:

| | FEMNIST | GSpeech |
|---|---|---|
| model | `cnn` | `melcnn` |
| lr | `0.01` | `0.2` |
| local_bs | `50` | `6` |
| local_period | `10` | `10` |

Algorithms: `DirBridge CA2FL FADAS FedBuff CASA FedBuffMALight FedASMU` (DirBridge adds
`--dirbridge_sketch_dim 2048`). Seeds: 1 2 3 4 5. `--concurrency 400` is the FedScale
training parameter (matches the paper's reference matrices); the scheduler's job
parallelism (1–8 concurrent processes on one GPU) is a host-level throughput knob only
and does not enter any training computation.

Note: GSpeech uses the same settings as the paper's GSpeech matrix, including its
known early-round behavior (an initial accuracy plateau around 1.4993 and a transient
NaN test-loss window) which is present in the paper's own reference runs and is not
introduced by the profile coupling.

## 4. Code identity

Desktop working tree is not a git checkout; identity is recorded by file hash:

- `utils/fedscale_profile_coupling.py` md5 `f852d981b40070027e71dce2378e0eae` (full
  copy in `code/`)
- `utils/fedscale_trace.py` md5 `b15869596b25446bc98d7e57d2b4cd36`
  (integration points: lines 10, 492–498, 633 — builds the coupling at trace
  initialization, replaces `client_ids` with mapped profile ids, embeds the mapping in
  metadata)
- `utils/options.py` line 442: `--fedscale_profile_coupling` choice {`''`, `label_group`}
- `builders/dataset_builder.py` lines 46, 81, 471, 650: attaches Dirichlet direction
  groups when coupling is active
- Baseline-fairness guards: `algorithm/ca2fl.py`, `algorithm/fedbuff.py` cap buffer
  construction at the number of positive-cost clients (no `min()` on empty sequences)
- Python: `python`; single RTX 5090 D (32 GB)

`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` was set for the launcher; each job
used 1 CPU thread (`OMP/MKL/OPENBLAS/NUMEXPR_NUM_THREADS=1`).

## 5. Audited results

### 5.1 Audit standard

Every run was required to have: exactly 500 accuracy lines (one per round), all values
finite, a metrics CSV covering rounds 1–500 uniquely, and no `Traceback`/OOM/`Killed`
in its scheduler log. All 70 runs (35 FEMNIST + 35 GSpeech) have complete 500-row accuracy files and corresponding metrics files in the audited external result tree. GSpeech logs contain the numerical-health limitation documented in `revision_audit_non_e2/e4_final/E4_NUMERICAL_HEALTH.csv`; completeness of accuracy does not imply fully finite evaluation loss.

### 5.2 GSpeech 5-seed summary

Final-round accuracy (mean ± sd over seeds 1–5), best-round accuracy, tail-50 mean,
and tail-10 mean:

| Algorithm | final | best | tail-50 | tail-10 |
|---|---|---|---|---|
| **DirBridge** | **61.33** | **64.37** | — | **53.25 ± 9.91** |
| FedASMU | 37.84 | 42.41 | — | 36.60 ± 2.11 |
| FADAS | 14.86 | 18.04 | — | 14.59 ± 12.05 |
| FedBuffMALight | 9.75 | 9.82 | — | 9.76 ± 6.85 |
| CASA | 1.50 | 17.68 | — | 2.93 ± 2.22 |
| FedBuff | 1.50 | 14.48 | — | 1.50 ± 0.00 |
| CA2FL | 1.50 | 5.86 | — | 1.50 ± 0.00 |

Per-seed tail-10:

| Algorithm | s1 | s2 | s3 | s4 | s5 |
|---|---|---|---|---|---|
| DirBridge | 61.43 | 44.59 | 63.27 | 55.73 | 41.25 |
| FedASMU | 35.66 | 35.91 | 39.47 | 37.91 | 34.05 |
| FADAS | 20.90 | 1.50 | 25.12 | 23.95 | 1.50 |
| FedBuffMALight | 17.46 | 4.36 | 17.00 | 5.66 | 4.30 |
| CASA | 3.62 | 1.50 | 6.54 | 1.50 | 1.50 |
| FedBuff | 1.50 | 1.50 | 1.50 | 1.50 | 1.50 |
| CA2FL | 1.50 | 1.50 | 1.50 | 1.50 | 1.50 |

DirBridge's tail-10 exceeds FedASMU by a mean paired difference of **+16.656 points** (SD 8.494; two-sided paired 95% t interval [+6.110, +27.202]); it wins all five paired seeds. The GSpeech logs nevertheless contain non-finite test loss in multiple methods, including DirBridge, and the existing records do not log parameters, logits, or BatchNorm buffers around those events. The numerical pathology is therefore unresolved; finite accuracy must not be described as proof of stable numerical learning.

### 5.3 FEMNIST 5-seed summary

| Algorithm | final (mean ± sd) | best (mean ± sd) | tail-50 | tail-10 |
|---|---|---|---|---|
| **DirBridge** | **76.49 ± 6.55** | **80.21 ± 1.12** | 72.19 | **73.60 ± 5.22** |
| FedBuff | 74.72 ± 1.34 | 76.32 ± 1.95 | 70.99 | 73.28 ± 2.18 |
| CASA | 72.87 ± 4.84 | 75.12 ± 3.22 | 69.72 | 71.16 ± 3.44 |
| FADAS | 68.34 ± 0.84 | 69.05 ± 1.06 | 67.53 | 68.40 ± 1.10 |
| CA2FL | 66.48 ± 8.22 | 70.43 ± 7.83 | 61.77 | 66.41 ± 8.25 |
| FedASMU | 57.08 ± 4.71 | 57.35 ± 4.76 | 55.26 | 56.85 ± 4.86 |
| FedBuffMALight | 12.52 ± 15.39 | 12.52 ± 15.39 | 12.04 | 12.41 ± 15.15 |

Per-seed tail-10:

| Algorithm | s1 | s2 | s3 | s4 | s5 |
|---|---|---|---|---|---|
| DirBridge | 72.32 | 73.53 | 75.61 | 80.46 | 66.10 |
| FedBuff | 73.03 | 73.93 | 75.49 | 74.24 | 69.71 |
| CASA | 74.40 | 66.71 | 74.88 | 70.15 | 69.68 |
| FADAS | 69.30 | 67.57 | 69.85 | 67.45 | 67.82 |
| CA2FL | 73.62 | 61.74 | 75.69 | 65.09 | 55.90 |
| FedASMU | 54.05 | 55.74 | 52.34 | 64.90 | 57.21 |
| FedBuffMALight | 5.72 | 5.72 | 5.39 | 39.52 | 5.72 |

Reading (tail-10 emphasizes the *converged* regime rather than the final round):

1. DirBridge has the highest mean tail-10 in this matrix, but the margin is small relative to seed variation and must be reported with paired uncertainty.
2. FedBuff's tail-10 is close to DirBridge's on FEMNIST. The per-seed comparison is mixed: DirBridge wins 2 seeds and FedBuff wins 3. We do not claim that DirBridge wins more often, has a uniformly higher ceiling, or is always better.
3. CASA is seed-sensitive (74.40 on s1 versus 66.71 on s2), and CA2FL is also variable (75.69 versus 55.90). FADAS is lower in this recorded matrix.
4. FedBuffMALight fails to learn on FEMNIST under profile coupling in four of five seeds; this is reported as a recorded failure mode, not generalized beyond this configuration.
5. GSpeech separates the methods more strongly in this recorded matrix, but the dataset, model, local learning rate, batch size, and task difficulty differ from FEMNIST. We do not interpret the cross-dataset difference as a monotonic coupling-strength result.

### 5.4 Provenance notes

- FEMNIST seeds 2–4 were first run under an overlapping-dispatch mistake (two schedulers
  writing the same files). Those outputs were detected, **deleted without backup**, and
  rerun from scratch by a single scheduler; the audit above applies to the rerun.
- FEMNIST seed 5 for FedBuffMALight and FedASMU was rerun sequentially after its
  interrupted first attempt; the audited files are single-writer.
- GSpeech's 35 runs were completed in one clean pass with no reruns.
- Raw per-round accuracy files and metrics CSVs remain on the desktop host under
  `$DIRBRIDGE_STATE_ROOT/e4_runs/profile_coupled_valid/fedscale_correct/{femnist,gspeech}/`
  and are not copied into this repository (size policy).

## 6. Reproducing

```bash
# FEMNIST (35 runs)
python main_fed.py --dataset femnist --algo <ALGO> --distribution noniid --alpha 0.5 \
  --random_cost fedscale_trace --num_users 1000 --concurrency 400 --buffer_size 100 \
  --total_rounds 500 --model cnn --lr 0.01 --local_bs 50 --local_period 10 --interval 1 \
  --seed <SEED> --fedscale_client_profile_path fedscale_device_info/client_device_capacity \
  --fedscale_profile_coupling label_group

# GSpeech: same, with --model melcnn --lr 0.2 --local_bs 6
```

The coupling is deterministic given the seed; the embedded per-run metadata records the
exact mapping used.
