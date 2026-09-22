# E4 Reanalysis: controlled coupling using real FedScale profiles

## Scope

The 70-run FEMNIST/GSpeech matrix uses profile-only clustering of FedScale device-capability records, followed by a seed-controlled assignment of label-derived groups to profile classes. Per-client service durations are derived from compute capability and a fixed upload/download payload. This is a **real-FedScale-profile-driven controlled coupling experiment**. It is not naturally observed label–latency data, an end-to-end latency trace, or proof that the original runs came from a real-world owner/device deployment.

## Code and unit provenance

The current public parser exposes `--fedscale_profile_coupling label_group`, and `utils/fedscale_trace.py` consumes it. The duration path is:

`3 * batch_size * local_steps * computation / 1000 + (upload_size + download_size) / communication`.

The resource audit records `computation` as ms/sample and `communication` as bandwidth, with fixed payload defaults. The payload convention and capability-derived formula must be stated whenever these results are cited. They should not be called measured network latency.

## Statistical correction

For FEMNIST tail-10 values listed in the source record:

- DirBridge: 72.32, 73.53, 75.61, 80.46, 66.10
- FedBuff: 73.03, 73.93, 75.49, 74.24, 69.71

DirBridge wins 2 of 5 seeds and loses 3. The correct summary is a small positive mean difference with seed-level uncertainty, not “higher more often” or an always-higher claim. The final response should report paired differences and confidence intervals rather than best-round values.

GSpeech shows a large separation in the recorded tail-10 summary, but it also contains transient non-finite test-loss rows. Finite accuracy files are usable as a constrained accuracy summary; they do not establish fully numerically healthy training. The cause of the loss pathology remains unresolved without lower-level logits, parameter, and BatchNorm snapshots.

## Correct interpretation

The matrix supports the claim that DirBridge can remain effective under one controlled assignment built from real device-capability profiles. It does not isolate association from every change in the selected profile multiset, and it does not establish naturally occurring label–latency coupling. Cross-dataset differences must not be described as a monotonic effect of coupling strength because the datasets, models, learning rates, and task difficulty also differ.
