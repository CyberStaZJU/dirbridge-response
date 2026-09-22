# E2 B/C Results: Repaired Online Oracle and Arrival-Frequency Controls

## Completed matrix

The authorized desktop run completed all ten runs: five seeds for B (`online + oracle`) and five seeds for C (`online + arrival_freq`). Each accuracy file has 500 rows and each metrics CSV has 500 data rows. The scheduler exited successfully.

Shared configuration: CIFAR-100, alpha 0.5, non-IID, `mild_label_correlated_hierarchical`, 100 clients, concurrency 40, buffer 10, ResNet, local learning rate 0.01, global learning rate 1.0, K0=7, sketch dimension 2048, recluster interval 5, 500 rounds.

## Accuracy summary

| Arm | Final mean ± SD | Tail-10 mean ± SD | Tail-50 mean ± SD |
|---|---:|---:|---:|
| B: online + oracle | 8.522 ± 10.599 | 8.540 ± 10.525 | 10.458 ± 6.386 |
| C: online + arrival frequency | 47.458 ± 2.173 | 47.643 ± 0.999 | 46.349 ± 0.665 |
| B − C paired mean ± SD | −38.936 ± 12.298 | −39.102 ± 10.480 | −35.890 ± 6.666 |

Per-seed final accuracy:

- B: `[1.00, 23.34, 1.00, 16.27, 1.00]`
- C: `[49.95, 44.15, 48.55, 47.82, 46.82]`

Per-seed tail-10 means:

- B: `[1.000, 22.736, 1.000, 16.966, 1.000]`
- C: `[48.929, 47.491, 47.504, 48.093, 46.197]`

The B oracle arm is substantially worse in this run identity. This is an observed configuration-specific result, not evidence that oracle population weights are intrinsically harmful: B and C differ in weight source, and the run diagnostics also show severe numerical-health problems in several B seeds.

## Weight-source diagnostics

All B metrics identify `e2_weight_source=oracle`, `e2_weight_l1_status=available`, and `e2_weight_l1_oracle=0.0`. This confirms that the oracle reference was present and that the measured group-weight comparison reached zero L1 error in the recorded metric.

All C metrics identify `e2_weight_source=arrival_freq` and `e2_weight_l1_status=reference_unavailable`. This is expected: arrival frequency estimates the arrival mixture and no compatible population reference was supplied for the deployable control. C must not be described as population-weight accurate or unbiased.

## Numerical-health boundary

The B logs contain repeated `Test loss nan` rows for seeds 1, 2, 3, and 5; B seed 4 is the only B seed whose final metrics row reports finite evaluation loss and logits. C seeds 1–5 have finite final evaluation loss and logits in their metrics rows, and their accuracy files are finite. No traceback, OOM, or killed-process evidence was found in the completed jobs.

Therefore the B accuracy collapse is associated with an unresolved numerical-health limitation in most B runs. The records do not contain per-batch input/logit/loss diagnostics, parameter snapshots, BatchNorm snapshots, or checkpoints sufficient to establish the root cause. The B results should be retained as a failed/diagnostically limited control, not used as clean evidence that oracle weighting worsens optimization.

## Claim boundary

The repaired B/C experiment answers the measurement question that was missing from A/D: the online oracle reference can be wired and measured without silently falling back, while the arrival-frequency arm explicitly reports that a population reference is unavailable. It does not provide a clean causal estimate of oracle versus estimated population-weight error because the oracle arm is numerically unhealthy in four of five seeds and B/C have different estimator semantics. A clean follow-up would require diagnosing and repairing the numerical failure before rerunning B, not relabeling these traces as healthy convergence evidence.
