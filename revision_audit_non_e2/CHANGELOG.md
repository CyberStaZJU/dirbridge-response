# Non-E2 Audit Changelog

## Code changes

- Repaired CA2FL cache accounting in `algorithm/ca2fl.py` with a maintained client-cache mean and O(BP) calibration.
- Preserved duplicate buffer-event multiplicity and updated the running mean after selected cache replacement.

## Analysis and tests

- Added `scripts/test_non_e2_update_wiring.py` for FedBuff/DirBridge server-step wiring, CA2FL equivalence, cache-mean replacement, and FADAS formula checks.
- Added `scripts/audit_non_e2_records.py` for lightweight E4/E5 accuracy-file audits.
- Added this directory's E1/E3/E4/E5/E6 audit records and conservative rerun plan.

## Commands run

- Local Python compilation for modified and new Python files: passed.
- Local `git diff --check`: passed.
- Remote PyTorch execution of `scripts/test_non_e2_update_wiring.py`: `non_e2_update_wiring=PASS`.
- E1 command audit: CIFAR 60 submitted / 60 unique; FEMNIST 60 submitted / 47 unique / 13 repeats; final CA2FL 5 / 5.

## Unresolved

- Local Mac environment lacks PyTorch, so the substantive test was run in the authorized remote PyTorch environment.
- E3 remains paused without endpoint diagnostics.
- E4/GSpeech lower-level numerical-health cause is unresolved.
- E5 K0=1 equivalence and Phi/coverage null calibration remain targeted follow-up tests/reanalysis.
- No standalone E6 training matrix exists.
- E2 was deliberately excluded from this audit and was not modified by these deliverables.
