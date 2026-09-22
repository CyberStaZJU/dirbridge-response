# E6 Resource Ledger

## Status

No independent E6 training matrix was completed. The E4 resource audit is supporting evidence only and must not be relabeled as a standalone E6 result.

## Memory categories

Resource claims must distinguish:

1. logical algorithmic persistent state;
2. unique physical tensor storage;
3. temporary aggregation working memory;
4. host process RSS;
5. current accelerator allocated/reserved memory;
6. historical accelerator peak.

The current `main_fed.py` field `device_peak_memory_mb` is based on `torch.cuda.max_memory_allocated()` when CUDA is used. It is a historical peak since the last reset, not a direct measurement of current allocation or persistent residency. The existing E4 resource table therefore needs this terminology correction.

## Logical state accounting

For a model with P floating-point coordinates:

- CA2FL retains N client caches, plus current client deltas and one running cache mean after the repair: logical cache state O(NP), incremental calibration state O(P).
- DirBridge retains K0 model-sized group caches, client features/sketch outputs, centroids, assignments, and explicit Count Sketch bucket/sign plans. The explicit CPU plan storage must be counted rather than replaced by an implicit theoretical estimate.
- FADAS retains first moment, second moment, and running maximum second moment.
- FedBuff has no method-specific cache of the CA2FL or DirBridge scale, apart from common simulator state.

Logical bytes and unique storage bytes should be reported separately where aliases/views exist.

## CA2FL repair

`algorithm/ca2fl.py` now maintains `state['cache_mean'] = (1/N) sum_i cache[i]`. Calibration uses a copied running mean and subtracts selected old cache entries in O(BP), preserving duplicate event multiplicity. After each selected cache replacement, the running mean is updated by `(new_cache - old_cache)/N` before the new cache becomes the maintained state.

The remote PyTorch test `scripts/test_non_e2_update_wiring.py` passed as `non_e2_update_wiring=PASS`. It compares incremental calibration with a full-scan reference and verifies cache-mean equivalence after replacement. Old runtime measurements must not be attributed to this repaired implementation without a new benchmark.

## Correct complexity table

| method | per-buffer calibration work | persistent method-specific state |
|---|---:|---:|
| CA2FL | O(BP) after running-mean maintenance | O(NP) client caches + O(P) running mean |
| DirBridge | group-memory aggregation plus amortized reclustering | group-level model caches, client features, sketch metadata |
| FADAS | O(P) moment update | O(P) first/second/max moments |
| FedBuff | O(BP) aggregation | no client-cache population state |

This table describes the current implementation after the repair; it does not retroactively change historical E4/E5 timings.
