# E2 D rerun: final repaired online + unique-client control

## Purpose

The earlier D five-seed results were generated before the fixes that assign a newly arriving client immediately when reclustering is not due and refresh the unique-client weight state in the same round. Those earlier D values are therefore historical and are not used as the final D control.

This rerun uses the final frozen public code and the corrected event path.

## Configuration and completion

- Code identity: public repository commit `4ac3e06` (the final D run was staged from this frozen revision; the repository now records the result in the subsequent publication commit)
- Dataset: CIFAR-100, alpha 0.5, non-IID
- Delay mode: `mild_label_correlated_hierarchical`
- Clients: 100
- Concurrency: 40
- Buffer size: 10
- Model: ResNet
- Local learning rate: 0.01
- Server learning rate: 1.0
- Local batch size: 100
- Local period: 10
- Interval: 1
- Direction groups: K0=7
- Sketch dimension: 2048
- Reclustering interval: 5
- Rounds: 500
- Seeds: 1–5
- Initialization: `online`
- Weight source: `unique_client`

All five runs completed 500 rounds. Each accuracy file and each system-metrics CSV contains 500 rows. No traceback, out-of-memory, killed-process, or runtime-error record was found in the D scheduler logs.

## Accuracy

| Seed | Final | Tail-10 | Tail-50 |
|---:|---:|---:|---:|
| 1 | 45.890 | 47.032 | 47.188 |
| 2 | 48.660 | 45.580 | 45.409 |
| 3 | 49.030 | 46.626 | 46.448 |
| 4 | 49.080 | 47.911 | 46.443 |
| 5 | 44.150 | 45.855 | 45.200 |
| **Mean ± SD** | **47.362 ± 2.231** | **46.601 ± 0.936** | **46.138 ± 0.822** |

## Coverage and weight diagnostics

At the final row of every seed:

- `e2_weight_source=unique_client`
- `e2_seen_clients=100`
- `e2_assigned_clients=100`
- `e2_seen_ratio=1.0`
- `e2_unseen_client_ratio=0.0`
- `e2_weight_l1_status=reference_unavailable`
- `e2_coverage_bound=0.0`
- `e2_eval_loss_finite=True`
- `e2_eval_logits_finite=True`
- `e2_eval_inputs_finite=True`
- `e2_eval_predictions_valid=True`
- `e2_eval_nonfinite_loss_batches=0`
- `e2_eval_nonfinite_logit_batches=0`

The full per-round coverage and weight fields remain in the external metrics CSVs; only compact summaries are committed here.

## Evidence boundary

This D rerun replaces the earlier pre-fix D accuracy summary for any final A/D comparison. It establishes the behavior of the final corrected implementation under the stated configuration. It does not establish population-weight unbiasedness because the unique-client estimator has no compatible population reference in this run.
