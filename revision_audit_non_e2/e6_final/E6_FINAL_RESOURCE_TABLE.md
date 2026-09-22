# E6 final resource table

Representative direct ledger: P=10,000 float32 coordinates; N=100 clients; K0=7; d_s=2,048. Bytes below are algorithm-owned persistent tensors only, not the simulator, model, dataset, event queue, or temporary aggregation allocations.

| Method | Logical persistent state | Measured unique persistent tensor bytes | Per-buffer extra computation |
|---|---|---:|---|
| FedBuff | common buffer/update state only; no method-specific cache ledger in this probe | 40,000 | O(BP) aggregation |
| CA2FL | N client caches + one running mean: O(NP)+O(P) | 4,040,000 | O(BP) calibration after running-mean maintenance |
| DirBridge | K0 model caches + client feature/sketch metadata + centroids/assignments + explicit sketch plan: O(K0P+(N+K0)d_s) plus plan storage | 1,126,400 | group aggregation plus feature encoding/reclustering as scheduled |
| FADAS | first moment + second moment + max second moment: O(P) | 120,000 | O(P) moment/update work |

## Direct state details

- CA2FL: 100 client cache tensors plus one running mean. At P=10,000 float32 coordinates this is `(100+1)*10,000*4 = 4,040,000` bytes.
- DirBridge: 7 group cache tensors, 100×2048 client features, 7×2048 centroids, 100 assignments, 7 counts, and one explicit int64 bucket plus int8 sign plan per model coordinate. The ledger records each tensor shape, dtype, device, storage pointer, offset, logical bytes, unique storage bytes, and alias relationship.
- FADAS: three P-sized float32 tensors, 120,000 bytes.
- FedBuff: the representative row is a single P-sized aggregate/update tensor; common simulator state is excluded.

## Memory interpretation

The CPU ledger measured unique storage directly. The authorized test environment did not expose CUDA, so CUDA allocated/reserved/peak values are recorded as unavailable rather than inferred. Process RSS is a process-level measurement and is not used as a substitute for the algorithm ledger. Historical `max_memory_allocated()` values, where present in old experiment CSVs, are historical peaks and do not prove persistent residency.
