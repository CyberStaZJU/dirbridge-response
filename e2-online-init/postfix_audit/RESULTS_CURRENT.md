# E2 Results and Evidence Boundary

## Completed repaired comparisons

Two repaired E2 comparisons are complete and must be read in chronological order:

1. **A/D comparison**: online + unique-client versus full-warm + full-count, five seeds each.
2. **B/C follow-up**: online + oracle versus online + arrival-frequency, five seeds each.

All twenty runs across these two comparisons are separate five-seed groups; no raw logs or runtime outputs are stored in this repository.

## A/D: online execution control

The earlier D values were generated before the first-arrival assignment and same-round unique-client weight-refresh fixes. They are retained only as historical provenance and are not used as the final D control.

The final frozen-code D rerun is reported in `RESULTS_D_REPAIRED_FINAL.md`:

| Variant | Final | Tail-10 | Tail-50 |
|---|---:|---:|---:|
| Final repaired online + unique-client, seeds 1–5 | 47.362 ± 2.231 | 46.601 ± 0.936 | 46.138 ± 0.822 |
| Full warm + full counts, historical control | 47.070 ± 2.021 | 47.269 ± 1.164 | 46.596 ± 0.936 |

The historical paired online-minus-full differences are not a valid final A/D comparison because the historical D arm predates the two fixes. The final D rerun is the authoritative online control; a paired comparison against full-warm would require a same-code full-warm rerun, which was not performed here.

## B/C: completed weight-source controls

B (`online + oracle`) and C (`online + arrival_freq`) each completed five 500-round runs. Their results are:

| Arm | Final mean ± SD | Tail-10 mean ± SD | Tail-50 mean ± SD |
|---|---:|---:|---:|
| B: online + oracle | 8.522 ± 10.599 | 8.540 ± 10.525 | 10.458 ± 6.386 |
| C: online + arrival frequency | 47.458 ± 2.173 | 47.643 ± 0.999 | 46.349 ± 0.665 |
| B − C paired mean ± SD | −38.936 ± 12.298 | −39.102 ± 10.480 | −35.890 ± 6.666 |

Per-seed final accuracy:

- B: `[1.00, 23.34, 1.00, 16.27, 1.00]`
- C: `[49.95, 44.15, 48.55, 47.82, 46.82]`

All B metrics report `e2_weight_source=oracle`, `e2_weight_l1_status=available`, and oracle L1 error `0.0`. All C metrics report `e2_weight_source=arrival_freq` and `e2_weight_l1_status=reference_unavailable`, as expected without a compatible population reference.

The B arm has repeated non-finite evaluation loss/logits in four of five seeds. C has finite final evaluation loss/logits in all five seeds. Thus the large B-C accuracy gap is a numerically confounded diagnostic result, not a clean causal estimate that oracle weights harm optimization. The completed B/C result is fully reported in `RESULTS_BC_CURRENT.md`.

## Numerical qualification shared by the historical A/D runs

The original A/D stdout logs contain repeated `Test loss nan` records in both arms, beginning at rounds 2–3 and ending by rounds 24–52. Accuracy files are complete and finite, but the historical runs did not save per-batch diagnostics, model checkpoints, or BatchNorm snapshots. We retain the accuracy traces as qualified prediction summaries and do not claim fully healthy finite training.

## Final evidence boundary

The repaired code now demonstrates online first-wave execution, exact in-flight materialization, explicit oracle/reference handling, and metric persistence. The A/D comparison supports configuration-specific online execution. The B/C comparison confirms that oracle and arrival-frequency paths are wired and measured without silent fallback, but its oracle arm is numerically unhealthy. Neither comparison establishes estimator unbiasedness, universal deployment behavior, or a clean healthy oracle-versus-estimated accuracy effect.
