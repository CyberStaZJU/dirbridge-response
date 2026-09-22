# E5 K0=1 and fixed-threshold tests

## Deterministic test

`python scripts/test_e5_sensitivity.py` was executed in the remote PyTorch environment against the public `algorithm/dirbridge.py` implementation. The test includes:

1. a threshold override check with updates at staleness values around the override, verifying that the valid list changes at exactly the requested threshold;
2. two consecutive K0=1 aggregation steps with a nonempty valid buffer, comparing the DirBridge grouped aggregate against the arithmetic mean of the same valid client deltas.

The test was staged against the final public code and corrected to include the required state fields. The current final test source is committed with this audit. A final remote rerun after the last test-fixture-only correction is required before publication; no training rerun is involved.

## Mathematical result

For one group with stored group weight 1, every valid client belongs to the sole group, and the target count is the valid-buffer size. No group deficit exists. Thus the selected group delta is the mean of the valid deltas and the server displacement is:

```text
server_lr * mean(valid_delta_i)
```

There is no alternate cluster assignment at K0=1. The old “single centroid flips” explanation is not used.
