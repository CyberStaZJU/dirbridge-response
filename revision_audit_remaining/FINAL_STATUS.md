# Remaining hard-task final status

## E1

The FEMNIST validation development matrix is complete: 24/24 verified runs, with validation-selected development configurations recorded in `revision_audit_non_e2/e1_final/`. No final five-seed evaluation was launched in the remaining-hard-task work. E1 is development-complete but not final-evaluation-complete.

## E4

The existing E4 results remain usable as a real-FedScale-profile-driven controlled data–system coupling experiment. The remaining audit contains a canonical 70-row health table, duplicate audit, clean paired statistics, unit-chain report, and rerun decision. The official physical payload chain remains limited by unavailable official source/caller artifacts and browser verification. GSpeech non-finite-loss causes remain unresolved because logits, parameters, BN buffers, and checkpoints were not logged around the events. No E4 training rerun was launched.

## E5

The existing 65 runs remain usable for sensitivity analysis. The remaining audit adds paired exploratory confidence intervals and B work accounting. B comparisons are fixed-server-round results and do not establish equal-work superiority. K0=7 is a pre-specified heuristic rather than an empirical optimum; K0=12/16 are higher in the stored setting. Sketch dimension is robust over the tested range. Finite-buffer sampling and the Phi decomposition prevent nonzero Phi from being treated as proof of persistent latency-induced skew.

## CA2FL

The production dispatcher path equivalence test passed on CPU and CUDA with five deterministic event steps, repeated-event scheduling, nonzero server learning rate, independent full-scan reference state, and strict comparisons of aggregate, model, cache, and running mean. The exact event overwrite/stamp semantics are documented.

## E6

The corrected actual-state ledger was generated from production `dispatcher.init_state` and post-event snapshots on CPU and CUDA. Method-owned tensor totals are reported separately from shared/common state, logical bytes are separated from unique physical storage, and storage-pointer deduplication is scoped to each independent live snapshot. The old DirBridge same-shape summary omitted 121,000 bytes; this arithmetic failure is recorded. CA2FL maintains client-level persistent cache state O(NP), one O(P) running mean, and O(BP) calibration work. Historical RSS and peak device memory are not treated as persistent algorithm state.

## E3

`ENDPOINTS NOT VALID — do not run five-level training` remains the verdict. The corrected desktop and PyTorch/CUDA runtime were available, but the bounded endpoint run failed at the production dataset boundary: `build_dataset` hard-coded a local CIFAR-100 path and attempted a download instead of consuming the verified external cache. No valid reference groups, profile assignments, event replay, or endpoint CSVs were produced. No five-level rho training was launched. This is a diagnostic execution blocker, not evidence that rho=0 and rho=1 are scientifically equivalent.

## Rerun boundary

No E2, E4 70-run, E5 65-run, E1 full fair-tuning, or E3 five-level training rerun was launched in the remaining-hard-task audit. The targeted CA2FL/E6 tests and actual state measurements ran only bounded deterministic workloads. E3 requires a targeted dataset-path correction and rerun of the scheduler-only endpoint diagnostic before any training decision.
