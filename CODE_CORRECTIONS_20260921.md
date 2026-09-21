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

The repair introduces an `state['inflight']` map:

- dispatch computes the result and stores it only in `inflight`;
- the scheduler cost remains available only for event ordering;
- arrival first moves the record from `inflight` into server-visible `delta` and `client_features`;
- only then does the code update `seen_set`, rebuild groups, compute weights, and aggregate;
- the initial online wave uses the same dispatch path;
- full warm-start keeps a compatibility record so the existing control path is not broken.

The exact patch was deployed to the desktop development tree with a rollback copy and passed Python syntax compilation using the reference environment. A behavioral smoke and a post-fix multi-seed online audit were not completed before this document was written. This correction must therefore be labeled **syntax-checked, behaviorally pending** until those tests pass.

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
