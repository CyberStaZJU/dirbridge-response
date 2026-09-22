# Final reply to Reviewer 3, Comment 1

We thank the reviewer for pointing out that the original DirBridge initialization procedure appeared to require a full pass over all clients before the asynchronous stream began. We separated online execution, population-weight estimation, and numerical-health reporting, then audited both controls.

## Online execution and corrected event semantics

The repaired implementation keeps a dispatched client update and direction feature in private `state['inflight']` until the simulated arrival event. Only then are the delta, feature, group membership, cache, and weight state updated. The first online wave uses the same dispatch path as later waves. A result is materialized exactly once; duplicate materialization raises an error.

We also corrected the interval-greater-than-one edge case: a newly arrived client is assigned immediately to the nearest existing centroid when a reclustering pass is not due. Membership, group counts, and current weight estimates are refreshed without forcing a full K-means pass. Deterministic regression tests cover in-flight isolation, first-wave materialization, non-reclustering arrivals, duplicate IDs, short buffers, missing references, oracle RNG isolation, and metrics persistence.

## Completed A/D execution comparison

We completed five-seed comparisons on CIFAR-100 with alpha 0.5, mild label-correlated hierarchical delays, 100 clients, concurrency 40, buffer 10, ResNet, local learning rate 0.01, server learning rate 1.0, K0=7, sketch dimension 2048, reclustering interval 5, and 500 rounds:

- online initialization with unique observed-client weights;
- same-code full-warm initialization with full-count weights.

The online and full-warm accuracy files all contain 500 finite values and the runs reached round 500 without traceback, out-of-memory, or killed-process evidence. The paired online-minus-full differences were +0.858 percentage points for final accuracy (95% CI [-1.571, +3.287]), +0.028 for tail-10 ([-1.301, +1.356]), and -0.132 for tail-50 ([-1.156, +0.891]). These results show no clearly detected accuracy difference under this configuration; they do not establish strict equivalence or unbiasedness.

## Completed B/C weight-source controls

We then completed the missing five-seed B/C comparison under the same configuration:

- B: online + oracle;
- C: online + arrival-frequency.

B reached 8.522 ± 10.599% final accuracy and C reached 47.458 ± 2.173%. The paired B-minus-C differences were -38.936 percentage points for final accuracy, -39.102 for tail-10, and -35.890 for tail-50. However, four of five B seeds have non-finite final evaluation loss/logits, whereas all five C seeds have finite final evaluation loss/logits. The large B-C gap is therefore a numerically confounded diagnostic result, not evidence that oracle weights intrinsically harm optimization.

The metric records confirm the intended semantics: B reports `e2_weight_source=oracle`, an available reference, and oracle L1 error 0.0; C reports `e2_weight_source=arrival_freq` and `reference_unavailable`. Arrival frequency is an arrival-mixture estimator, not a population-mixture oracle, and no unbiasedness claim is made.

## Numerical-health qualification

The historical A/D logs contain repeated `Test loss nan` records in both arms, beginning at rounds 2–3 and ending by rounds 24–52. The B arm additionally has severe evaluation-health failures in four of five seeds. The historical runs did not retain per-batch inputs/logits/losses, checkpoints, or BatchNorm snapshots, so the root cause cannot be identified retrospectively. Accuracy traces are retained as qualified prediction summaries; no claim of fully healthy finite training is made.

## Final conclusion

The completed experiments establish configuration-specific online execution without a full-client initialization pass and confirm that oracle and arrival-frequency controls are explicitly wired and measured without silent fallback. They do not establish universal deployment behavior, estimator unbiasedness, or a clean healthy oracle-versus-estimated accuracy effect. The completed B/C evidence and its numerical limitation are recorded in `RESULTS_BC_CURRENT.md`.
