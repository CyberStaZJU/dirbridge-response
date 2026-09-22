# E2 Rerun Plan and Closure

## Completed work

The previously missing B/C controls are complete. Five B runs (`online + oracle`) and five C runs (`online + arrival_freq`) reached 500 rounds under the repaired code identity. Results and limitations are recorded in `RESULTS_BC_CURRENT.md` and summarized in `RESULTS_CURRENT.md` and `REPLY_R3_1.md`.

## No duplicate rerun

Do not launch another five-run B comparison or repeat the C control from this document. The B/C experiment is completed. Its oracle arm is numerically unhealthy in four of five seeds, so another run would be a new numerical-diagnosis experiment, not a completion of missing B/C work.

## Optional future diagnosis

A separate, explicitly approved follow-up may instrument per-batch inputs, logits, losses, parameters, and BatchNorm state to diagnose the B-arm numerical failure. Such a run must use a new output directory and a new code/configuration identity. It must not overwrite or relabel the completed B/C results.
