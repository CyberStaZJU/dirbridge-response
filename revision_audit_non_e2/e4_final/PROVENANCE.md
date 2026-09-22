# E4 provenance freeze

- Public repository: `CyberStaZJU/dirbridge-response`
- Audit revision: `4ac3e06`
- Worktree status at audit start: `main...origin/main`, clean
- E4 implementation used by the archived run: `e4-profile-coupling/code/fedscale_profile_coupling.py`
- Current public integration: `utils/fedscale_trace.py` → `utils/fedscale_profile_coupling.py`
- Archived helper and public helper are byte-identical at this revision.
- E4 launch configurations: `configs/fedscale_femnist_mc400_b100.yaml`, `configs/fedscale_gspeech_mc400_b100.yaml`; reproducible shell entry points: `scripts/run_fedscale_femnist.sh`, `scripts/run_fedscale_gspeech.sh`; the exact seven-algorithm/five-seed profile-coupled command pattern is reproduced in `e4-profile-coupling/DESIGN_AND_RESULTS.md`.
- Exact raw outputs/logs: external desktop state under `$DIRBRIDGE_STATE_ROOT/e4_runs/profile_coupled_valid/fedscale_correct/{femnist,gspeech}/`, with `acc/`, `metrics/`, and `scheduler_logs/` subdirectories. Raw outputs are intentionally not committed.
- Matrix: 7 algorithms × 5 seeds × 2 datasets = 70 runs; audited accuracy and metrics files are complete.
- The archived desktop code was not a main-entry-point checkout. This is recorded as provenance, not treated as an invalidation reason. The public repository now contains the archived helper and the corresponding main integration path.
