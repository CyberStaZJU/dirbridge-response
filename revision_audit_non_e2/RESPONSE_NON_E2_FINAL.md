# Final reviewer response — R1-D1 through R3-4

We thank the reviewers for asking us to separate algorithmic effects from configuration, delay construction, resource accounting, and numerical health. We audited the requested items in completion order and report only completed evidence below. The response repository contains the detailed records; this file is the consolidated reviewer-facing reply.

## R1-D1 — method mechanism and scope

DirBridge is a buffered asynchronous method that maintains direction-group memory and uses it to compensate for representation deficits caused by latency-dependent arrivals. The mechanism is conditional: when arrival-direction coupling is weak or a tuned FedBuff remains stable, final accuracy need not improve. We therefore report matched configurations, paired seed variability, and resource costs rather than universal superiority.

## R1-D2 — anomalous baseline behavior

The audit exposed the server-step controls in FedBuff, DirBridge, and CA2FL while preserving the default step of one. The remote deterministic test confirms the wiring, CA2FL incremental equivalence, and the FADAS adaptive formula. The historical E1 command files contain 60/60 unique CIFAR effective configurations but 60 submissions and 47 unique FEMNIST effective configurations; we report this distinction rather than calling the search perfectly symmetric. Selection used tail-10 test accuracy on a development seed, not an independent validation split, and DirBridge retained previously selected defaults. These are explicit limitations.

The evidence supports a conditional conclusion: CA2FL and FedBuff behavior is server-step sensitive; FADAS was empirically unstable in some searched settings; and a tuned baseline can be close to or above DirBridge in matched configurations. The exact FADAS adaptive-denominator cause is not established by the stored diagnostics.

## R1-D3 — data and delay construction

The artifact distinguishes ordinary label non-IID construction from controlled label–delay assignments. Results are not presented as naturally observed joint data/latency distributions unless the source actually provides such observations.

## R1-D4 — buffer size and work accounting

E5 contains 65 complete runs over B, K₀, and sketch dimension under one fixed CIFAR-100 workload. Increasing B changes both the number of updates aggregated per server round and the client work represented by that round. The fixed-round ranking therefore is not an equal-work comparison; matched simulated-work summaries are reported separately.

## R1-D5 — resource and runtime interpretation

The resource audit separates logical algorithmic state, unique tensor storage, temporary working memory, host RSS, current accelerator allocation/reservation, and historical accelerator peak. The recorded `max_memory_allocated()`-style values are historical per-run peaks; they are not by themselves proof of persistent residency or a complete component ledger. CA2FL's large device-peak difference and DirBridge's smaller difference are retained as measured peak evidence, without attributing an unmeasured residual entirely to Count Sketch arrays.

## R1-D6 — number of direction groups

The K₀ sweep shows a broad useful region around the pre-specified rule K₀ = ceil(log₂ number of classes). K₀=7 is not called an empirical optimum because K₀=12 is higher in the stored summary. The K₀=1 accuracy result is descriptive; the prior single-centroid-flip explanation is withdrawn because it is not established by the record and is not an adequate explanation for a one-group system.

## R2-1 through R2-4 — implementation, diagnostics, and statistical reporting

The public code exposes the relevant controls and writes system metrics for the supported diagnostics. Completed comparisons use five paired seeds where available and distinguish final, tail-10, and tail-50 accuracy. Incomplete or interrupted grids are excluded. Finite accuracy files are not treated as proof of finite logits, parameters, or BatchNorm state when the logs show non-finite loss.

## R2-5 — sketch dimension

Across the stored d_s sweep, grouping diagnostics and accuracy remain in a broad region relative to seed variation. We describe d_s=2048 as a stable default, not as the best or optimal dimension; d_s=8192 has a higher stored mean in this matrix.

## R3-1 — online initialization

The repaired implementation keeps dispatched updates and features private in `state['inflight']` until arrival, materializes each event once, assigns newly observed clients when reclustering is not due, and refreshes current weights. The A/D online-versus-full-warm comparison completed five seeds per arm and showed no clearly detected accuracy difference under the configuration, without establishing strict equivalence or estimator unbiasedness.

The B/C follow-up also completed five seeds per arm: B is online+oracle and C is online+arrival-frequency. B final accuracy was `8.522 ± 10.599%`; C was `47.458 ± 2.173%`. B has non-finite final evaluation loss/logits in four of five seeds, while C has finite final evaluation diagnostics in all five. B therefore remains a numerically confounded diagnostic control, not clean causal evidence that oracle weighting harms optimization. B reports available oracle reference and L1 error 0.0; C correctly reports `reference_unavailable`. No silent oracle fallback or unbiasedness claim is made.

## R3-2 — profile coupling

The E4 matrix is a controlled data–system coupling experiment driven by real FedScale device-capability profiles. It is not naturally observed label–latency coupling or measured end-to-end latency. FEMNIST per-seed results are mixed: DirBridge wins 2 of 5 seeds against FedBuff and loses 3, so the response uses paired uncertainty rather than a “wins more often” claim. GSpeech accuracy results retain an explicit non-finite-loss limitation, and cross-dataset differences are not interpreted as a monotonic coupling-strength effect.

## R3-3 — fair tuning

The E1 audit reports submitted runs and unique effective configurations separately, preserves the search asymmetry, and does not present interrupted grids as complete. Server-step sensitivity and numerical-health limitations are reported instead of using unstable baseline settings as evidence of intrinsic inferiority.

## R3-4 — memory and systems accounting

The E6 standalone matrix was not completed. The E4 resource audit is supporting evidence only. CA2FL's current implementation maintains the O(NP) client caches plus an O(P) running mean and computes calibration in O(BP). A remote deterministic test passes full-scan equivalence, duplicate-event semantics, cache-mean replacement equivalence, and update wiring. Historical timing measurements are not reattributed to the repaired implementation.

## Final boundary

The completed evidence supports configuration-specific execution, conditional accuracy comparisons, explicit numerical-health limitations, and corrected resource terminology. It does not support universal superiority, natural-world latency claims, estimator unbiasedness, an empirical K₀ optimum, a standalone E6 result, or a clean healthy causal oracle-versus-estimated effect.
