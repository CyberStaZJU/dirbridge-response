# E2 Post-fix Correctness Audit

The completed B/C follow-up is documented in `RESULTS_BC_CURRENT.md`. All five online+oracle and five online+arrival-frequency runs reached 500 rounds. The oracle arm has severe numerical-health failures in four of five seeds, so it is retained as a diagnostic control rather than clean causal convergence evidence.

Audit basis: public repository HEAD `6c298fc37d74650d5b60b75f6526cfba25e4e2f7` plus the uncommitted changes in this worktree. No push was performed. The ten completed CIFAR-100 runs were read from the authorized desktop state directories and were not rerun.

## Status table

| Issue | Status | Evidence and boundary |
|---|---|---|
| In-flight results became server-visible before arrival | **already_fixed** | `algorithm/dirbridge.py`: `_schedule_new_clients` writes only `state['inflight']`; `_materialize_arrivals` moves the record on completion. `scripts/test_e2_correctness.py` mutates an in-flight delta and confirms server-visible state is unchanged before materialization. |
| Initial online wave lacked a real local result | **already_fixed** | Online `init_state` uses `_schedule_new_clients`; first-wave records contain delta and feature. Regression test covers materialization. |
| Duplicate materialization is silently accepted | **already_fixed** | A second materialization raises `RuntimeError`; regression test covers exactly-once consumption. |
| First arrival on a non-reclustering round could keep `group_id=-1` and be omitted | **confirmed, fixed in this audit** | Before this audit, `_build_ema_group_updates` grouped `-1` but only iterated `0..K-1`. New arrivals are assigned to existing centroids immediately and membership/counts are updated. Regression test uses existing centroids and verifies the update enters a fresh mean. |
| Existing formal ten-run matrix was affected by that interval bug | **refuted for the reported configuration** | The ten commands omitted `--dirbridge_recluster_interval`; the remote parser default for DirBridge is 5, so the run configuration was not the earlier documented interval-1 assumption. However, the exact per-round group IDs were not logged, so the historical runs cannot be retroactively certified for assignment coverage. Treat as a material audit limitation, not as proof of silent loss in every run. |
| Repeated arrivals inflate unique-client weights | **already_fixed / confirmed semantics** | `arrival_count` increments on every raw return; `seen_set` changes only for new IDs; unique-client weights count assigned distinct clients. Regression test covers repeat ID. |
| Weight refresh was only tied to K-means rebuild | **confirmed, fixed in this audit** | New-arrival assignment refreshes weights from the current membership when no rebuild occurs. Arrival-frequency is also refreshed on the same path. The metrics expose weight update round. |
| `uninitialized_group_mass` silently became zero without a reference | **confirmed, fixed in this audit** | It now returns `None` when no population reference is available. The previous normalized-observed-count calculation was not a population-mass estimate. |
| Oracle silently fell back to uniform weights | **confirmed, fixed in this audit** | `source=oracle` now raises if a compatible full-population reference is unavailable. |
| Oracle measurement pass could perturb training RNG | **confirmed, fixed in this audit** | `_populate_oracle_features` is wrapped in a Python/NumPy/Torch/CUDA RNG-preserving context. Regression test checks the random streams. |
| E2 metrics existed only in memory | **confirmed, fixed in this audit** | `main_fed.py` now writes E2 state, event counts, weight-reference status, coverage, initialization timing, and evaluation-health fields to system-metrics CSV after the same-round evaluation. |
| Historical ten-run metrics contain the new E2 fields | **unresolved / absent** | Original CSV headers contain only the old system fields and have 500 rows. No checkpoint or serialized state snapshot was retained. The new fields cannot be reconstructed from accuracy alone. |
| Historical `Test loss nan` is only a formatting bug | **refuted** | Original stdout shows repeated `Test loss nan` interleaved with finite losses and low/variable accuracies, starting at rounds 2–3. The evaluator used standard `F.cross_entropy`; no per-batch finite diagnostics were present. This is not a proven formatter-only issue. |
| Historical non-finite loss proves parameters or BN buffers were non-finite | **unresolved** | No checkpoints or parameter/BN snapshots were retained. Historical logs cannot distinguish non-finite logits, finite logits with non-finite loss accumulation, or BN/state corruption. |
| Historical accuracy is automatically invalid | **unresolved, qualified** | Accuracy files are complete and finite, but historical evaluation did not check logits before argmax. Finite accuracy is usable as an accuracy trace with a numerical-health qualification, not as proof of healthy finite logits/parameters. |
| B/C oracle-vs-estimated comparison exists in the repaired ten runs | **refuted** | The ten commands contain only online+unique and full+full-count. No repaired B (`online+oracle`) or C (`online+arrival_freq`) command/output exists in the authorized run directories. Historical 60-run E2 matrix is a different code identity and cannot fill this gap. |
| Existing E2 oracle is an exact current-training population oracle | **refuted / renamed** | It is a full-population direction snapshot at initialization or an offline reference evaluated against current representatives. It is a non-deployable reference-snapshot oracle, not automatically an exact later-training population assignment. |
| Full-client initialization is required for the algorithm to execute | **refuted for this configuration** | Repaired online runs completed 5/5 seeds and 500 rounds with only first-wave dispatch at initialization. Evidence strength is execution-level and configuration-specific, not a universal deployment guarantee. |

## Numerical timeline from original stdout

All ten runs have 500 accuracy rows and no traceback/OOM/Killed records. Every run has non-finite test-loss rows, beginning at rounds 2 or 3 and ending between rounds 24 and 52; none occurs in tail-50 or tail-10. The exact run-level ranges are in `NUMERICAL_HEALTH.csv`. The original logs contain evaluation loss and accuracy only; train loss, logits, parameters, BN buffers, per-batch losses, and checkpoint states are absent.

The new evaluator records these missing fields for future short diagnostics and does not drop batches, clamp values, or replace NaN with zero.

## Historical result boundary

- Historical 60-run E2 matrix: separate pre-repair identity; do not merge with the repaired ten-run comparison.
- Repaired ten-run comparison: CIFAR-100 only, online+unique versus full+full-count, five paired seeds, 500 rounds; finite accuracy files, shared non-finite test-loss limitation.
- Post-fix code audit: event semantics and metric persistence tested in synthetic/reference-environment regression tests; no new full matrix launched.
- Repaired oracle comparison: pending; no B/C results in the new code identity.
