# E5 numerical gate and K0=1 tests

The corrected test `scripts/test_e5_sensitivity.py` executed successfully in an isolated CPU PyTorch environment against the public DirBridge functions:

```text
k1_two_steps_cache_and_displacement=PASS
e5_sensitivity=PASS
```

Earlier test-fixture failures were not algorithm failures and did not establish equivalence. The successful test now supplies the full required state.

## Tested behavior

- B=5,10,20 rule gates are 8,4,2. Delays 1,2,3,4,5,8,9 test both sides and equality at each threshold.
- Override 4 accepts precisely delays <=4 for each B.
- Two consecutive K0=1 steps include an invalid update and share exactly the same valid buffer with the FedBuff `sd_average` function.
- Both steps use server LR 0.37 and identical initial model state.
- The production cache-update function runs after step one; step two uses an existing nonzero cache and different client deltas.
- Aggregates and cumulative model displacement agree within absolute tolerance 1e-12, with zero relative tolerance.
- Cache fill remains zero because the sole group has no representation deficit.

This verifies the current public aggregation functions, not an entire training trajectory or a recovered historical executable. Historical code identity remains a separate provenance question. No training run was launched and no E2 file was changed.
