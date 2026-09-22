# Supplemental Results and Scope Update (2026-09-21)

This document supplements the earlier E1-E5 records in this repository. It records later experiments from the desktop development tree and separates audited results, controls, interrupted runs, and unfinished work.

## Shared comparison protocol

Unless stated otherwise, the image-dataset comparisons use:

```text
local_bs = 100
local_period = 10
num_users = 100
concurrency = 40
buffer_size = 10
model = resnet
formal rounds = 500
formal seeds = 1,2,3,4,5
dev rounds = 150
dev seed = 100
primary metric = tail-10 mean accuracy
secondary metrics = tail-50 mean and final accuracy
```

The later development-grid protocol uses:

```text
local_lr  in {0.003, 0.01, 0.03, 0.05}
global_lr in {0.1, 0.5, 1.0}
```

A development result is used for selection only when all requested rounds are present and the run passes the numerical-health audit. Formal test seeds are not used to select hyperparameters.

## E1: fair tuning and baseline diagnosis

### Later five-seed comparisons

| Dataset/profile | local_lr | global_lr | Method | Final | Tail-10 | Tail-50 |
|---|---:|---:|---|---:|---:|---:|
| CIFAR-10, alpha=0.5, mild | 0.03 | 0.5 | FedBuff | 80.238 +/- 1.817 | 80.287 +/- 0.815 | 80.022 +/- 0.429 |
| CIFAR-10, alpha=0.5, mild | 0.03 | 0.5 | DirBridge | 81.060 +/- 0.831 | 81.056 +/- 0.825 | 80.588 +/- 1.061 |
| CIFAR-10, alpha=0.1, mild | 0.03 | 0.5 | FedBuff | 65.220 +/- 4.838 | 66.758 +/- 3.205 | 65.478 +/- 2.141 |
| CIFAR-10, alpha=0.1, mild | 0.03 | 0.5 | DirBridge | 66.130 +/- 2.830 | 66.000 +/- 3.933 | 65.910 +/- 2.036 |
| CIFAR-100, alpha=0.5, mild | 0.05 | 0.5 | FedBuff | 56.864 +/- 1.171 | 56.975 +/- 0.488 | 56.329 +/- 0.524 |
| CIFAR-100, alpha=0.5, mild | 0.05 | 0.5 | DirBridge | 55.484 +/- 0.841 | 55.434 +/- 0.545 | 54.826 +/- 0.682 |
| CIFAR-10, alpha=0.1, high | 0.03 | 0.5 | FedBuff | 69.428 +/- 3.822 | 67.459 +/- 2.745 | 68.092 +/- 1.813 |
| CIFAR-10, alpha=0.1, high | 0.03 | 0.5 | DirBridge | 68.618 +/- 1.597 | 67.524 +/- 2.129 | 67.020 +/- 1.361 |

These are conditional comparisons, not universal rankings. On the mild CIFAR-10 settings, the methods are close after choosing a stable server step. On CIFAR-100 under the stated configuration, FedBuff is higher. Under high-skew CIFAR-10, the tail-10 means are effectively indistinguishable at this sample size.

### DirBridge development search

CIFAR-10 alpha=0.1 mild, development seed 100, 150 rounds, all 12 trials completed. The best tail-10 candidate was:

```text
local_lr = 0.03
global_lr = 0.5
tail-10 = 51.241
```

The complete grid is recorded in the workspace status and should be copied into the final response tables rather than reporting only the selected point.

### Interrupted FedBuff development search

A matching CIFAR-10 alpha=0.1 mild FedBuff grid was started but explicitly stopped before completion. The first submission used an invalid loop-based command file; the corrected retry used 12 independent commands, but the final two trials were terminated before completion. These partial files are not valid tuning results and are not used for selection or claims.

Therefore, the later workspace evidence does not yet establish a complete independently tuned FedBuff-versus-DirBridge comparison on this exact CIFAR-10 alpha=0.1 mild setting.

### Reviewer-facing interpretation

The evidence supports a narrower claim: a tuned FedBuff can match DirBridge on several settings, while FedBuff can be highly sensitive to the effective asynchronous server step. An unstable FedBuff configuration must not be presented as evidence of intrinsic baseline inferiority. DirBridge should be described as a conditional correction for latency-induced direction-representation mismatch, not as a method that must improve final accuracy on every workload.

## E2: online initialization and current code audit

The earlier E2 record contains an audited control matrix for full initialization, online grouping with oracle weights, arrival-frequency weights, and unique-client weights. That record remains a separate code identity and result set.

The repaired online five-seed run and same-code full-warm control both completed 500 rounds for seeds 1–5. Accuracy files were complete and finite in all ten runs. Both groups nevertheless contained logged `Test loss nan` rows, so these are accuracy comparisons with an explicit numerical-diagnostic limitation, not fully clean convergence evidence.

| Initialization | final mean±std | tail-10 mean±std | tail-50 mean±std |
|---|---:|---:|---:|
| Online + unique observed clients | 47.928±0.327 | 47.296±1.185 | 46.463±0.812 |
| Full warm + full counts | 47.070±2.021 | 47.269±1.164 | 46.596±0.936 |

Paired difference (`online - full-warm`, percentage points; seeds 1–5) was `+0.858` with 95% CI `[-1.571, +3.287]` for final accuracy, `+0.028` with CI `[-1.301, +1.356]` for tail-10, and `-0.132` with CI `[-1.156, +0.891]` for tail-50. With five seeds, these intervals support a statement of no detected practically clear difference under this configuration, not strict equivalence. The shared NaN-loss rows remain an unresolved numerical-health limitation and are disclosed rather than hidden.

The public parser and execution-path port for the historical supplemental flags is independently documented in `PUBLIC_ENTRYPOINT_AUDIT_20260922.md` and tested by `scripts/test_flag_wiring.py`.

## E3: stronger profile experiment

E3 was paused after the original quota/coupling proposal was rejected because it manually selected clients by direction group. No valid E3 result is added here. A future E3 must use a natural label-cost coupling and must not choose clients by group to satisfy quotas.

## E4: profile coupling

The earlier E4 record contains the audited 70-run profile-coupling matrix on FEMNIST and GSpeech, including the profile-only clustering, seed-controlled group-to-profile mapping, resource audit, and per-seed results. Those results remain the authoritative E4 record in `e4-profile-coupling/`.

## E5: sensitivity

The earlier E5 record contains the audited 65-run sensitivity matrix for buffer size, direction-group count, and sketch dimension, including fixed-threshold controls, matched-work interpretation, accelerator-memory accounting, and configuration identity. Those results remain the authoritative E5 record in `e5-sensitivity/`.

## E6: resource accounting status

No independent E6 experiment was completed. The existing E4 resource audit provides partial evidence about device-memory accounting, including the distinction between process RSS and accelerator memory and the CA2FL cache footprint. This evidence is referenced rather than relabeled as a completed E6 matrix.

## Publication boundary

The public response artifact must distinguish:

- audited completed results;
- partial or interrupted runs;
- code fixes that have only passed syntax checks;
- experiments that remain paused or not started.

No raw datasets, long logs, checkpoints, private host paths, or unreviewed partial outputs belong in this repository.
