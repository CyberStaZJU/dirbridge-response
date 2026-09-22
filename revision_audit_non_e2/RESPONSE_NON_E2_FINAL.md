# Reviewer Response Draft — Non-E2 Items

We thank the reviewers for asking us to separate algorithmic effects from configuration, resource accounting, and the particular construction of the delay process. We audited E1, E3, E4, E5, and E6 separately from the E2 online-initialization analysis.

## E1: tuning and baseline diagnosis

We exposed and audited the server-step parameter in the FedBuff, DirBridge, and CA2FL paths. The default remains one, preserving prior behavior, while `global_lr` now changes the server update where applicable. A deterministic remote test confirms the wiring and verifies the CA2FL incremental state update.

The audit also found that submitted development jobs and unique effective configurations are not identical: the CIFAR command file contains 60 unique effective configurations, whereas the FEMNIST file contains 60 submissions but 47 unique effective configurations. We therefore no longer describe the command files as a perfectly symmetric set of 20 unique configurations per method without qualification. In addition, the earlier E1 baseline search used tail-10 test accuracy on a development seed rather than an independent validation split, and DirBridge retained previously selected defaults. We present these as limitations.

The defensible empirical conclusion is conditional. CA2FL is sensitive to the exposed server step and its earlier chance-level behavior should not be interpreted as proof that the method is intrinsically incapable. FADAS was empirically unstable at larger searched server steps, but the exact adaptive-state mechanism is not fully established because the denominator and applied-displacement distributions were not retained at sufficient resolution. A tuned FedBuff can be close to DirBridge in several matched configurations, and FedBuff is higher in the stated CIFAR-100 comparison. We do not claim universal accuracy superiority for DirBridge.

## E3: coupling-strength scan

No completed E3 result is included. The earlier quota-based proposal was paused because it manually selected clients by direction group. A valid future E3 should keep client data and the delay/profile multiset fixed, change only the client-to-profile assignment, and first verify rho=0 and rho=1 through actual profile assignment, service duration, finish order, and buffer composition. Until that endpoint diagnostic separates realized arrival-direction statistics, a five-level scan is not justified.

## E4: FedScale profile coupling

The E4 matrix is best described as a controlled data–system coupling experiment driven by real FedScale device-capability profiles. It is not naturally observed label–latency coupling and not measured end-to-end latency. The service duration is derived from the recorded computation and communication capability fields plus a fixed payload convention.

The 70 runs remain useful as an audited controlled experiment, subject to this scope correction. For FEMNIST, the stored tail-10 values show DirBridge wins 2 of 5 seeds against FedBuff and loses 3; we therefore report paired differences and uncertainty rather than saying it is higher more often. GSpeech accuracy files are complete and finite, but transient non-finite test-loss rows remain a numerical-health limitation. We do not infer monotonic coupling-strength effects by comparing FEMNIST and GSpeech because their datasets, models, learning rates, and task difficulty differ.

## E5: B, K0, and sketch dimension

The 65-run E5 matrix is complete under its archived configuration identity. The B comparison is a fixed-server-round sensitivity study; larger B also performs more client work per server round, so it is not an equal-work comparison. The stored matched-work analysis must remain separate from fixed-round accuracy.

The K0 results show a broad useful region, but K0=7 is a pre-specified heuristic rather than an empirical optimum; K0=12 is higher in the stored summary. Likewise, d_s=2048 is a stable default in a broad region, not the best observed value because d_s=8192 is higher in the stored mean. The existing Phi and coverage values cannot alone establish persistent latency-induced representation skew because ordinary finite-buffer sampling can produce similar variation. A finite-population null and persistent-versus-fluctuation decomposition are the appropriate follow-up analysis. The K0=1 mechanism requires a direct equivalence test against a gated FedBuff-style aggregate before attributing its behavior to centroid dynamics.

## E6: resources and CA2FL state

We did not complete an independent E6 training matrix. The E4 resource audit is supporting evidence only. Its resource terminology must distinguish logical state, unique tensor storage, temporary working memory, host RSS, current accelerator allocation/reservation, and historical accelerator peak. In particular, `max_memory_allocated()` is a historical peak, not a direct persistent-memory measurement.

We repaired CA2FL's cache accounting by maintaining a running mean of the N client caches. Calibration now uses the running mean and selected old cache entries in O(BP) time, while retaining the O(NP) client-cache state. Duplicate event identities remain counted with multiplicity, and the mean is updated after cache replacement. A remote deterministic PyTorch test passes full-scan equivalence and post-replacement cache-mean equivalence. Historical runtime measurements are not attributed to this repaired implementation without a new benchmark.

## Remaining limits

The non-E2 audit leaves E3 incomplete, does not establish a standalone E6 result, and does not provide a complete causal numerical diagnosis for the GSpeech loss pathology or the FADAS adaptive denominator. These boundaries are retained rather than filled with stronger claims.
