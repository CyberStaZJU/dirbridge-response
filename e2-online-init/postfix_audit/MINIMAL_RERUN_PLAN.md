# Minimal E2 Rerun Plan

No new full matrix was launched in this audit.

## Required missing comparison

Run only repaired B (`online + oracle`) on CIFAR-100 with seeds 1–5, matching the existing online D commands exactly except:

```text
--e2_init_mode online --e2_weight_source oracle --e2_oracle_features
```

This is the minimum new training required to separate the weight-source control from the existing A/D comparison. It requires 5 runs, not a new E1–E6 matrix.

Before launch:

1. Use the current post-fix code identity, not the uncommitted desktop tree used for the historical ten runs.
2. Confirm the full-population reference definition and record that it is a non-deployable reference-snapshot oracle.
3. Confirm the corrected evaluator and system-metrics CSV fields are enabled.
4. Record the exact command, resolved defaults, code identity, and external output directory.
5. Run the existing synthetic/reference-environment regression tests first.

## Optional C control

Run repaired C (`online + arrival_freq`) on the same five seeds only if the response needs a direct demonstration that repeated arrival frequency differs from unique-client estimation. This is useful but secondary; it is not needed to establish the minimum oracle-versus-estimated comparison.

## No rerun authorized by this document

Do not rerun the historical 60-run matrix, the full-warm A control, or the online D control solely to refresh their values. If the metric-persistence or numerical-health changes are treated as changing training semantics rather than recording-only changes, then the affected A/D results must be regenerated as a separate versioned comparison.
