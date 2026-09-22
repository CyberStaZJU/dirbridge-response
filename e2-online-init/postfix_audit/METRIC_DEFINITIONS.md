# E2 Post-fix Metric Definitions

## Version boundary

These definitions apply to the post-fix public runtime changes in the current worktree. The ten completed CIFAR-100 runs were produced by the authorized desktop tree before this audit's metric-persistence patch; their historical system-metrics files therefore do not contain the new E2 columns. Their raw accuracy and stdout records remain usable as separately identified evidence.

## Event and assignment quantities

- **Raw arrivals**: number of completed tasks materialized in the current buffer, including repeat returns from the same client.
- **Valid updates**: raw arrivals that pass the configured staleness filter.
- **Used updates**: observed members included in group fresh means for the current aggregation. This excludes unassigned clients and invalid updates.
- **Seen clients**: distinct client IDs in `seen_set`, regardless of whether a later update is stale-filtered.
- **Assigned clients**: clients with a non-negative training group ID. In online mode this can exceed the reclustering set because newly arrived clients are assigned immediately to existing centroids.
- **Clustered clients**: clients used by the most recent K-means rebuild.

## Weight and population quantities

- **Unique-client weight**: normalized count of distinct assigned observed clients by current training group.
- **Arrival-frequency weight**: normalized count of raw accepted arrival events by current training group; repeated clients count repeatedly.
- **Oracle/reference weight**: normalized assignment of a full-population direction snapshot to the current group representatives. It is a non-deployable reference-snapshot control, not automatically the exact population weights of a later training-time grouping.
- **Population-weight L1**: L1 distance between the actual estimator weights and the matching oracle/reference weights. It is `NA` with reason `reference_unavailable` if no compatible full-population reference exists. It must not be replaced by buffer-mixture L1.
- **Unseen-client ratio**: `1 - N_seen/N`.
- **Coverage bound**: `2(1 - N_seen/N)` for the same client-uniform population and group-assignment rule. It is not valid as an error bound for stale weights from an earlier membership version unless that version is explicitly reported.
- **Uninitialized group mass**: reference population mass of groups with no observed member. Without a reference population weight vector, the value is `NA`; zero is not used as a substitute.
- **Buffer-mixture error**: L1 distance between a raw or valid buffer's measurement-monitor group mixture and the monitor population mixture. This is a separate diagnostic from population-weight estimation error.

## Numerical-health quantities

The evaluation helper records per-evaluation-batch finite checks for inputs, logits, and cross-entropy loss. An integer argmax can remain superficially finite when logits are non-finite; `eval_predictions_valid=False` marks that accuracy as numerically unqualified. No batch is dropped and no NaN is replaced.

The existing model state exchange exports floating parameters and buffers, including BatchNorm `running_mean` and `running_var`, while excluding `num_batches_tracked`. The audit does not infer parameter or BatchNorm health for historical runs without checkpoints or per-round state diagnostics.

## Timing quantities

- `e2_init_time_sec`: process wall time from dataset/model construction through `init_state`; it is not simulated time.
- `e2_online_bootstrap_time_sec`: time spent dispatching the initial online wave; local task execution is performed synchronously by this simulator and is included in the measured process time.
- `e2_oracle_measurement_time_sec`: extra full-population reference pass when explicitly enabled.

These fields are written after evaluation for the same round, so evaluation-health fields are aligned with the accuracy row for that round. Existing ten-run metrics lack these fields and cannot be retrofitted from accuracy alone.
