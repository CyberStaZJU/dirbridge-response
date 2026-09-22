# E4 Reanalysis: controlled coupling using real FedScale profiles

## Scope

The 70-run FEMNIST/GSpeech matrix uses profile-only clustering of FedScale device-capability records, followed by a seed-controlled assignment of label-derived groups to profile classes. Per-client service durations are derived from compute capability and a fixed upload/download payload. This is a **real-FedScale-profile-driven controlled coupling experiment**. It is not naturally observed label–latency data, an end-to-end latency trace, or proof that the original runs came from a real-world owner/device deployment.

## Code and unit provenance

The current public parser exposes `--fedscale_profile_coupling label_group`, and `utils/fedscale_trace.py` consumes it. The duration path is:

`3 * batch_size * local_steps * computation / 1000 + (upload_size + download_size) / communication`.

The resource audit records `computation` as ms/sample and `communication` as bandwidth, with fixed payload defaults. The payload convention and capability-derived formula must be stated whenever these results are cited. They should not be called measured network latency.

## Statistical correction

For FEMNIST tail-10 values recomputed from the raw accuracy files:

- DirBridge: 72.3225395, 73.5250546, 75.6065880, 80.4615349, 66.0978619
- FedBuff: 73.0320976, 73.9321587, 75.4946404, 74.2444305, 69.7062454

The paired differences have mean `+0.3208012`, SD `3.5999996`, two-sided paired 95% t interval `[-4.1491887, +4.7907912]`, with DirBridge winning 2 seeds and losing 3. The correct summary is a small, uncertain mean difference, not “higher more often” or an always-higher claim. The final response reports paired differences and confidence intervals rather than best-round values.

For GSpeech, the strongest valid baseline by tail-10 is FedASMU. The raw paired differences (DirBridge minus FedASMU) have mean `+16.6560655`, SD `8.4936203`, two-sided paired 95% t interval `[+6.1098429, +27.2022880]`, with 5 wins and 0 losses. This result remains subject to the unresolved GSpeech non-finite-loss limitation. Finite accuracy files are usable as a constrained accuracy summary; they do not establish fully numerically healthy training.

## Correct interpretation

The matrix supports the claim that DirBridge can remain effective under one controlled assignment built from real device-capability profiles. It does not isolate association from every change in the selected profile multiset, and it does not establish naturally occurring label–latency coupling. Cross-dataset differences must not be described as a monotonic effect of coupling strength because the datasets, models, learning rates, and task difficulty also differ.
