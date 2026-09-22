# CA2FL incremental equivalence result

The five-step deterministic CPU test `test_ca2fl_multistep_equivalence.py` passed:

```text
ca2fl_multistep_equivalence=PASS
```

## Test coverage

- five consecutive server aggregations;
- N=5 client caches and B=3 events per buffer;
- repeated identities in every buffer, including `[0,1,0]` and `[2,4,2]`;
- old cache used in each innovation/calibration before replacement;
- running cache mean checked against a full scan at every step;
- incremental calibrated aggregate checked against full-scan calibration at every step;
- every per-client cache checked after each replacement;
- CPU path completed successfully;
- CUDA path was not available in the authorized test environment.

The implementation updates the running mean after aggregation, in event order:

```text
cache_mean += (new_cache - old_cache) / N
cache[idx] = new_cache
```

Repeated client identities are intentionally processed as repeated events. The test verifies exact equality at tolerance `rtol=0`, `atol=1e-12` for the two-coordinate float64 state.

## Complexity result

CA2FL retains N client caches, so persistent algorithmic state is O(NP), plus one O(P) running mean. Once the running mean exists, calibration subtracts the selected B old cache entries and is O(BP). Historical full-scan runtime measurements are not attributed to this repaired implementation.
