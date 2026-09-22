# Response to Reviewer 3, Comment 1

We thank the reviewer for pointing out that the original DirBridge initialization procedure appeared to require a full pass over all clients before the asynchronous stream began. We re-audited the implementation and separated three issues that were previously conflated: online execution, population-weight estimation, and numerical-health reporting.

## Online execution and corrected event semantics

We added an explicit in-flight state. A dispatched client update and its direction feature are kept in `state['inflight']` and are not copied into the server-visible delta, feature, group, cache, or weight state until the simulated arrival event. The initial online wave uses the same dispatch path as later waves. A result is materialized exactly once; duplicate materialization raises an error.

The audit also found a separate edge case for a reclustering interval greater than one: a newly arrived client could remain at group ID `-1` until the next reclustering pass. Because aggregation iterates over valid group IDs, such an update could be omitted from a non-reclustering buffer. We corrected this by assigning newly observed clients immediately to the nearest existing centroid, updating membership and group counts, and refreshing the current weight estimate without forcing a full K-means pass.

The corrected behavior is covered by deterministic regression tests for in-flight isolation, first-wave materialization, non-reclustering first arrival, duplicate IDs, short buffers, and insufficient/empty reference states. The tests pass in the reference environment.

## What the ten repaired runs establish

We verified the original records for two separately identified five-seed comparisons on CIFAR-100 (`alpha=0.5`, mild label-correlated hierarchical delay, 100 clients, concurrency 40, buffer 10, ResNet, local learning rate 0.01, server learning rate 1.0, sketch dimension 2048, 500 rounds):

- online initialization with unique observed-client weights;
- same-code full-warm initialization with full-count weights.

All ten accuracy files contain 500 finite values and all ten processes reach round 500 without traceback, out-of-memory, or killed-process evidence. The online runs therefore support the narrower, configuration-specific statement that DirBridge can execute the specified stream without a full-client initialization pass. This is execution evidence, not a universal claim about all datasets, delay processes, or deployment environments.

The reported paired differences are:

| Metric | Online − full-warm | 95% CI |
|---|---:|---:|
| Final accuracy | +0.858 pp | [-1.571, +3.287] pp |
| Tail-10 accuracy | +0.028 pp | [-1.301, +1.356] pp |
| Tail-50 accuracy | -0.132 pp | [-1.156, +0.891] pp |

The intervals do not show a clearly detected accuracy difference at five seeds, but they do not establish strict equivalence and should not be read as evidence that the unique-client estimator is unbiased.

## Numerical-health qualification

The original stdout logs contain repeated `Test loss nan` records in both arms. They begin at rounds 2–3 and end by rounds 24–52; no such record appears in the tail-50 or tail-10 windows. The accuracy files remain finite, but the historical runs did not save per-batch input/logit/loss diagnostics, model checkpoints, or BatchNorm running-statistic snapshots. Thus, the historical evidence does not identify whether the non-finite losses came from logits, a loss computation path, or model/BatchNorm state.

We do not delete affected seeds, replace NaN with zero, drop batches, clamp BatchNorm statistics, or claim fully healthy finite training. We retain the accuracy traces as finite prediction summaries with this explicit limitation. The evaluator now records finite-input, finite-logit, finite-loss, and prediction-validity flags for future runs, and these fields are written to the same-round system-metrics CSV.

The implementation exports BatchNorm `running_mean` and `running_var` in the synchronized state while excluding `num_batches_tracked`. This behavior was inspected directly; no historical checkpoint exists that would permit a retrospective parameter or BatchNorm-health verdict.

## Population weights and oracle limitation

The repaired ten-run comparison is an A-versus-D comparison: it changes both initialization information and the weight source. It therefore cannot isolate population-weight estimation.

The new records contain no repaired B arm (`online + oracle`) or C arm (`online + arrival-frequency`). We do not substitute the earlier 60-run matrix because it has a different code identity and is explicitly historical. The minimum missing experiment is a five-seed repaired B comparison with the same configuration and `--e2_init_mode online --e2_weight_source oracle`; C is an optional secondary control for repeated-arrival bias.

We also refined the terminology. The current oracle is a **reference-snapshot oracle**: it uses a full-population direction snapshot and assigns that snapshot to the current representatives. It is a non-deployable measurement control, not automatically the exact population assignment of a later training-time grouping. If the compatible reference snapshot is unavailable, the implementation reports an undefined value or raises for an oracle training arm; it does not silently use uniform weights.

For the deployable estimators, we distinguish:

- population-weight estimation error;
- raw/valid buffer-mixture error;
- distinct-client coverage and unseen-client ratio;
- assigned-client coverage and cache readiness.

The coverage expression `2(1 - N_seen/N)` is reported only as the client-uniform coverage bound for a matching group rule and observed set. It is not applied to stale weights from an earlier group version, and it does not imply finite-time unbiasedness.

## Scope and remaining work

The historical 60-run matrix, repaired ten-run A/D comparison, numerical-health qualification, and repaired oracle comparison are now separate evidence classes. The repaired oracle comparison remains pending. No new complete matrix was launched during this audit; the minimum additional training needed for the central oracle-versus-estimated question is five B runs, subject to confirming the reference-snapshot definition and running the new diagnostics.
