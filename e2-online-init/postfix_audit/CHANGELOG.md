# E2 Post-fix Audit Changelog

## Code changes in this worktree

- Added explicit numerical-health diagnostics to image evaluation: finite input, finite logits, finite batch loss, and prediction-validity flags. Existing two-value `test_img` callers remain compatible.
- Added same-round E2 and evaluation-health fields to system-metrics CSV output. Rows are written after evaluation so health fields align with the same round.
- Added process-wall initialization timing, online bootstrap timing, and oracle-measurement timing fields with explicit scope labels.
- Assigned newly observed clients to existing centroids immediately when a periodic reclustering pass is not due. Updated membership/counts and refreshed weight estimates from the current membership.
- Counted raw arrivals and unique observed clients separately; duplicate materialization remains an error.
- Changed population-mass diagnostics to return `NA`/`None` without a compatible reference instead of returning zero.
- Made missing oracle references fail explicitly rather than silently falling back to uniform weights.
- Preserved Python, NumPy, Torch, and CUDA RNG states around oracle-only measurement.
- Added `scripts/test_e2_correctness.py` covering in-flight isolation, exactly-once arrival consumption, non-reclustering first arrival, duplicate IDs, weight refresh, unknown population mass, oracle isolation, evaluation-health diagnostics, CSV persistence, and BatchNorm state exchange.

## Tests run

- Local Python syntax compilation and `git diff --check`: passed.
- Remote reference environment:
  - `scripts/test_flag_wiring.py`: `public_flag_wiring=PASS`.
  - `scripts/test_e2_correctness.py`: `e2_correctness_regression=PASS`.
- Historical log audit on authorized desktop:
  - 10/10 accuracy files: 500 rows and finite accuracy values.
  - 10/10 logs: no traceback, OOM, or killed-process evidence.
  - 10/10 logs: repeated non-finite test-loss rows; no historical per-batch or parameter-health fields.
  - 10/10 system-metrics files: 500 rows but old schema without the new E2 fields.

## Publication boundary

This worktree remains uncommitted and unpushed by instruction. No historical result file was overwritten, no checkpoint was deleted, and no new full training matrix was started.
