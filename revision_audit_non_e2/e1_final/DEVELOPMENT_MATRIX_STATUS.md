# E1 development matrix status — 2026-09-23

## Verified execution status

The development scheduler has ended. All 24 CIFAR-10 runs have 150 accuracy rows and 150 system-metrics rows. The 24 FEMNIST commands failed before training because the isolated snapshot could not locate the FEMNIST dataset. The outer launch command's zero exit status does not establish matrix success.

Outputs and logs remain in the external `e1_confirmatory_20260922_211545` state directory, under `runs_dev3` and `logs_dev3`. Failed runs are retained, not excluded as poor configurations.

## CIFAR-10 recorded validation tail-10 surface

Percent accuracy; development seed 100; 150 rounds. These are development observations, not five-seed confirmatory test results.

| Local LR | Server LR | FedBuff | DirBridge |
|---:|---:|---:|---:|
| .003 | .1 | 31.218 | 30.440 |
| .003 | .5 | 43.166 | 44.138 |
| .003 | 1 | 10.404 | 42.464 |
| .01 | .1 | 39.728 | 37.516 |
| .01 | .5 | 56.738 | 58.046 |
| .01 | 1 | 10.032 | 43.066 |
| .03 | .1 | 47.330 | 46.866 |
| .03 | .5 | 63.662 | 66.002 |
| .03 | 1 | 10.100 | 55.330 |
| .05 | .1 | 44.848 | 45.086 |
| .05 | .5 | 61.484 | 63.300 |
| .05 | 1 | 10.100 | 37.136 |

Both recorded validation maxima occur at local LR .03 and server LR .5. Configuration selection is not yet finalized: the split provenance and executable validation path require reconciliation before these can be called confirmatory results. Low validation accuracy alone does not establish numerical divergence.

## Unresolved validation and protocol issues

- The manifest generator uses NumPy sampling, whereas the runtime subset implementation uses Torch `randperm`. Their recorded indices must not be assumed identical.
- The manifest's original claim of unchanged client partitions conflicts with runtime removal of held-out indices. The actual partition reduction and index disjointness need to be recorded from the run snapshot.
- FEMNIST validation integration and model configuration were not qualified by the CIFAR-only smoke.
- Development execution also evaluated the test set; the selection policy must remain validation-only, and test observations must not be used to revise the search.
- The snapshot contains uncommitted E1 implementation changes; a base Git revision alone does not identify the executed tree.

No final five-seed evaluation has been launched. E1 is not resolved. This publication preserves the partial development results and failed-run status without reclassifying them as a completed confirmatory comparison. E2 and other experiment results are unchanged.
