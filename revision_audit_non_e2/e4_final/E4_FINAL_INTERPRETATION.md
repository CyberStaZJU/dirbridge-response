# E4 final interpretation

## Provenance and implementation

E4 is a 70-run matrix: seven algorithms, five seeds, and two datasets (FEMNIST and GSpeech). The audited desktop outputs are external at:

`$DIRBRIDGE_STATE_ROOT/e4_runs/profile_coupled_valid/fedscale_correct/{femnist,gspeech}/`

The archived E4 helper is `e4-profile-coupling/code/fedscale_profile_coupling.py`; it is byte-identical to the current public `utils/fedscale_profile_coupling.py`. The integration path is `utils/fedscale_trace.py`, enabled by `--random_cost fedscale_trace --fedscale_profile_coupling label_group`. The public repository contains both the archived helper and the current integration path at commit `4ac3e06`.

## What E4 supports

- Real FedScale device-capability profiles are used as the source of `computation` and `communication` capability fields.
- Client completion times are profile-driven and computed with the official FedScale numerical convention.
- A controlled association is imposed between dataset-derived direction groups and profile classes through a seed-controlled permutation.
- The experiment tests whether the DirBridge behavior persists when synthetic hand-written delay ranges are replaced by real-profile-driven service durations.
- On the primary tail-10 metric, FEMNIST DirBridge versus FedBuff has mean paired difference `+0.321` percentage points, SD `3.600`, 95% paired t interval `[-4.149, +4.791]`, with 2 wins and 3 losses.
- On GSpeech, DirBridge versus FedASMU has mean paired difference `+16.656` points, SD `8.494`, 95% interval `[+6.110, +27.202]`, with 5 wins and 0 losses.

## What E4 does not support

- It does not show that the original FedScale population naturally exhibits the imposed label–device association.
- FEMNIST writers and GSpeech speakers were not measured on the physical devices represented by the selected profile rows.
- It is not naturally co-observed label–latency coupling in FedScale.
- It is not a measured end-to-end latency trace.
- Cross-dataset FEMNIST/GSpeech differences do not prove a monotonic benefit as direction skew increases.
- The FEMNIST result must not be described as DirBridge winning more seeds than FedBuff.

## Numerical health

Accuracy files are complete and finite. Existing GSpeech logs show non-finite test loss from rounds 1 through 52, including the tail-10 window. Existing logs do not save parameter snapshots, logits, or BatchNorm buffers around the event. The pathology is therefore **unresolved**, not silently classified as evaluation-only or model-state failure. Finite accuracy does not remove this limitation.

## Resource wording

Historical device-peak values remain usable as peak measurements. They do not by themselves prove persistent residency or identify the exact contribution of Count Sketch arrays. Current and persistent allocation require a separate component-level ledger.
