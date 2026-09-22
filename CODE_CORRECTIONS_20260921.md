# Code Corrections and Verification Status (2026-09-21)

This file records code changes that affected the later experiments or were identified during the online-mode audit. It is deliberately explicit about whether each item was verified end to end.

## 1. Server learning-rate exposure

The artifact code now exposes the server step in the three relevant baseline/method paths:

- `algorithm/fedbuff.py`: applies `global_lr`, defaulting to `1.0`;
- `algorithm/dirbridge.py`: applies `global_lr`, defaulting to `1.0`;
- `algorithm/ca2fl.py`: maps `global_lr` to the previously hard-coded `eta`, defaulting to `1.0`.

These edits preserve the previous default behavior while making the server step auditable and tunable. The desktop development tree used the same semantic correction for the later experiments.

### FedBuff

The desktop development implementation was changed from an implicit unit server step to:

```python
server_lr = float(getattr(args, 'global_lr', None) or 1.0)
w_global += server_lr * aggregated_diff
```

The default remains `1.0`, preserving the previous FedBuff behavior. This change is required before interpreting `global_lr` sweeps as actual FedBuff server-learning-rate sweeps.

### DirBridge

DirBridge was changed analogously so an explicit `global_lr` scales the aggregated update while the default remains `1.0`.

### CA2FL

The E1 diagnostic work exposed a previously hard-coded CA2FL server step. The harness now exposes the applicable step as `global_lr` while preserving `eta=1.0` as the default. This is a harness repair and parameter exposure, not a claim that the CA2FL algorithm was improved.

## 2. High-skew CIFAR group attachment

The CIFAR non-IID data-builder path previously attached label-derived groups for the mild hierarchical profile but not for `label_correlated_hierarchical`. The desktop development tree was patched so both hierarchical profiles attach the required label groups before delay-profile construction. A one-round smoke passed before the high-skew matrix was restarted.

The high-skew result and this correction must be interpreted together: the first failed launch was an unavailable code path, not a failed high-skew training result. The restarted 10-run high-skew matrix completed and is documented in `SUPPLEMENTAL_RESULTS_20260921.md`.

## 3. E1 diagnostic instrumentation

`e1-fair-tuning/code/e1_diagnostics.py` records update norms, model norms, first non-finite round, buffer delay, CA2FL cache-correction and aggregate norms, BatchNorm running-variance bounds, and FADAS effective-step/moment diagnostics. The instrumentation is recording-only and does not change the update formula.

## 4. Online in-flight state separation

### Problem

Before the current repair, `_schedule_new_clients()` computed a local delta and feature at dispatch and wrote them directly to `state['delta']` and `state['client_features']`, even though the simulated completion time had not been reached. The online first wave also scheduled costs without creating the corresponding local result.

### Minimal repair

The exact repaired implementation is now included as:

```text
e2-online-init/code/dirbridge_online_repaired.py
e2-online-init/code/e2_online_repaired.py
```

The repaired implementation is now integrated into the public runtime entry point and is also preserved as the exact desktop experiment snapshot in:

```text
e2-online-init/code/dirbridge_online_repaired.py
e2-online-init/code/e2_online_repaired.py
```

The public port includes the E2 helper module, in-flight/server-visible state separation, online first-wave dispatch, arrival materialization, and the five-argument parser/profile integration documented in `PUBLIC_ENTRYPOINT_AUDIT_20260922.md`. The snapshot files remain useful for comparing the public artifact with the desktop experiment identity.

The public port passed the deterministic in-flight visibility test and the five-argument wiring test in the desktop reference environment. The repaired online five-seed run also completed without OOM, traceback, killed-process, or scheduler-failure evidence. The full-warm control is audited separately because its later seeds showed numerical instability.

## 5. Code identity boundary

The desktop development tree and this public response artifact are not byte-identical repositories. The desktop tree contains additional algorithms, runtime helpers, and experiment-specific changes. The response artifact records the correction intent, affected code paths, and verification status; it must not claim that every desktop result is reproducible from the current artifact checkout until the relevant patch is integrated and tested here.

## 6. Verification checklist

Before using the online correction as a final reviewer claim:

- run a five-client deterministic event test;
- assert an in-flight feature is absent from server-visible state before arrival;
- assert the same feature appears after arrival;
- assert the first online wave has a real nonzero local result;
- assert unseen clients have group id `-1` and do not enter centroids or weights;
- run a short CIFAR-10 online smoke;
- rerun the selected multi-seed online matrix;
- audit exact rounds, finite metrics, and no scheduler errors.
