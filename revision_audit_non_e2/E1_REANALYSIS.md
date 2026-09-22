# E1 Reanalysis: Tuning, server steps, and baseline diagnosis

## Current verdict

E1 supports a conditional, configuration-specific comparison. It does not support universal DirBridge superiority or a claim that every baseline received a perfectly symmetric effective search.

## Tuning-budget audit

The stored development command files contain:

| command file | submitted | unique effective configurations | repeated effective configurations |
|---|---:|---:|---:|
| `commands_dev_cifar.sh` | 60 | 60 | 0 |
| `commands_dev_femnist.sh` | 60 | 47 | 13 |
| `commands_final_ca2fl.sh` | 5 | 5 | 0 |

Run tags, output paths, and GPU arguments were excluded from configuration identity. Therefore the older phrase “20 configurations per method per dataset” is not literally true for the FEMNIST command file: it describes intended method-level budget, while the file contains 13 repeated effective configurations. The audit should report both submission counts and unique effective configurations.

DirBridge was not retuned in the old E1 formal comparison; it retained prior defaults while baselines received a response-stage search. This asymmetry is a limitation and must remain visible.

## Learning-rate wiring

The current public code exposes `global_lr` in FedBuff, DirBridge, and CA2FL. FedBuff and DirBridge apply the server multiplier to the aggregated update. CA2FL applies it to the calibrated update, preserving default step 1.0. FADAS uses `global_lr` as the adaptive step multiplier and applies the moment-normalized update.

The remote deterministic test `scripts/test_non_e2_update_wiring.py` passed as `non_e2_update_wiring=PASS`. It covers source-level server-step wiring, CA2FL full-scan versus incremental equivalence with duplicate buffer IDs, cache-mean replacement equivalence, and the FADAS adaptive formula.

## Validation/test separation

The E1 selection metric is tail-10 **test accuracy** on a development seed. This is test-guided development selection, not an independent validation split. The seed separation is useful for avoiding reuse of the formal seeds, but it does not turn the test set into validation data. Reviewer-facing text must use “development/test-guided selection”.

## CA2FL

The old hard-coded server step was a harness limitation, not evidence that CA2FL cannot be tuned. The current record supports the narrower conclusion that the original step can produce a large correction-to-aggregate ratio and poor behavior, while a smaller selected step can improve the observed run. The existing diagnostic prose reports negative BatchNorm running variance under some settings, but the available record does not establish a complete causal chain from the first invalid buffer to test-loss failure. Do not describe the mechanism more strongly than the stored per-round diagnostics allow.

## FADAS

The update order in `algorithm/fadas.py` is: aggregate update, update first and second moments, update running maximum `vhat`, form `sqrt(vhat)+eps`, and apply the adaptive update. Since `sqrt(1e-11)` is approximately `3.16e-6`, the statement that the denominator is approximately epsilon is not generally valid. The safe conclusion is empirical: larger server-step settings were unstable in the recorded implementation, while the exact adaptive-state mechanism requires denominator and applied-displacement distributions for confirmation.

## Later matched comparisons

The later supplemental record reports close conditional comparisons on several CIFAR settings and FedBuff higher on the stated CIFAR-100 configuration. These results are useful as matched-configuration evidence, not as a complete independent re-tuning study. The interrupted FedBuff alpha=0.1 development grid must not be used as a completed surface.

## Revised conclusion

After exposing the server-step controls, the evidence no longer supports calling baseline failures intrinsic. The defensible claim is that asynchronous server-step choice is consequential, CA2FL can recover under a selected step in the recorded setting, FADAS is empirically sensitive in the searched configurations, and DirBridge's advantage is workload- and configuration-dependent. A broader or perfectly symmetric tuning study remains future work rather than a fact about the existing evidence.
