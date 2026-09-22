# R3-4 response: CA2FL persistent state and memory accounting

We thank the reviewer for identifying the ambiguity between algorithmic persistent state and process-level memory measurements.

CA2FL does maintain one model-sized cache for each of the N clients. Its logical persistent client-cache state is therefore O(NP), plus one O(P) running mean. We now maintain that mean incrementally. For each returned event, calibration uses the old client cache in `delta_i - h_i`; only after aggregation is the cache replaced and the running mean updated by `(new_cache - old_cache)/N`. Repeated client identities are processed in event order rather than silently deduplicated. A deterministic five-step test with repeated identities verifies the running mean, calibrated aggregate, model state, and all client caches against a full-scan reference at `rtol=0`, `atol=1e-12`.

The running mean changes the extra calibration computation, not the persistent cache requirement. It avoids recomputing the sum over all N caches on every buffer: calibration is O(BP), while persistent cache storage remains O(NP). Historical runtime measurements from the older full-scan implementation are not attributed to the repaired implementation.

We also added a direct tensor-storage ledger. It records tensor shape, dtype, device, logical bytes, storage pointer, storage offset, unique physical storage bytes, aliases, and persistence/category labels. For a representative P=10,000, N=100, K0=7, d_s=2048 CPU state, the measured algorithm-owned persistent tensor bytes are:

- FedBuff: 40,000 bytes for the representative method-specific aggregate/update state;
- CA2FL: 4,040,000 bytes for 100 client caches plus one running mean;
- DirBridge: 1,126,400 bytes including group caches, client features, centroids, assignments, and explicit Count Sketch bucket/sign tensors;
- FADAS: 120,000 bytes for first moment, second moment, and AMSGrad maximum.

The Count Sketch plan is not treated as an implicit map: the ledger counts one explicit int64 bucket and one int8 sign per model coordinate. Logical and unique physical storage are reported separately so aliases cannot hide logical state, while shared storage is not double-counted physically.

Table VI process RSS was not a direct measurement of algorithm-specific cache state. Process RSS and historical accelerator peak are therefore no longer used to infer persistent algorithm memory. The revised accounting separates logical persistent state, measured unique tensor storage, temporary work, process RSS, current device allocation, reserved memory, and historical peak. CUDA values are marked unavailable when the accounting environment has no CUDA device.

We apologize for the incorrect CA2FL extra-computation entry. We revise it from O(NP) to O(BP), while its persistent client-cache state remains O(NP).
