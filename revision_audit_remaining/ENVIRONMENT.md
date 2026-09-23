# Remaining-audit environment freeze

- Date: 2026-09-23
- Repository: `CyberStaZJU/dirbridge-response`
- Branch: `main`
- Commit at freeze: `388a79b`
- Worktree: dirty; uncommitted E1 validation implementation and local status/plan edits are present. They are outside this remaining-audit publication unless separately reviewed.
- E2: completed and frozen; excluded from this task.
- E1: validation-selected development matrices complete for CIFAR-10 and FEMNIST; no final five-seed evaluation launched in this task.
- Remote Python: `/home/jczn2/.conda/envs/yibo/bin/python`; exact PyTorch/CUDA runtime version was not re-read in this resumed process.
- GPU: desktop GPU0 was available during the E1 FEMNIST run; current live allocation must be checked before any diagnostic launch.
- E4 raw results/logs: external `$DIRBRIDGE_STATE_ROOT/e4_runs/profile_coupled_valid/fedscale_correct/{femnist,gspeech}`; accuracy, metrics, and scheduler logs are available.
- E5 raw results/logs: external E5 CIFAR state tree used for the 65-run manifest; compact audit tables are in `revision_audit_non_e2/e5_final/`.
- E6: current repository contains the prior CPU representative ledger and CA2FL equivalence evidence under `revision_audit_non_e2/e6_final/`; an actual production-state ledger remains to be verified in this task.
- Raw logging boundary: E4/E5 have accuracy and summary/system CSVs plus scheduler logs; logits, parameters, and BN snapshots are generally absent. E1 raw run trees remain external.
- E3 profile source: external FedScale device profile and behavior-trace files under the established desktop state; a scheduler-only endpoint replay has not yet been executed.
