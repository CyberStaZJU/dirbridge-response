# Minimal Non-E2 Rerun Plan

## Category A: no training rerun required

- Recalculate E1 command uniqueness and report submitted versus effective configurations.
- Correct E1 reviewer language around test-guided development selection, tuning asymmetry, FedBuff server scaling, and FADAS mechanism certainty.
- Recalculate E4 paired FEMNIST/GSpeech statistics from existing per-seed values.
- Reclassify E4 as controlled real-profile coupling rather than naturally observed latency coupling.
- Recalculate E5 finite-buffer nulls, persistent-versus-fluctuation decomposition, and paired K0/d_s summaries if the stored monitor CSVs are available.
- Correct E6 memory terminology and retain the current CA2FL incremental implementation.

## Category B: targeted smoke or deterministic test

- Run the K0=1 versus gated FedBuff equivalence test with identical valid-buffer and server-step state.
- Run a deterministic FedScale duration unit test for known computation, bandwidth, batch, local-step, and payload values.
- If raw E4/GSpeech diagnostics are available, run a representative numerical-health probe for logits, parameters, and BatchNorm state.
- Run an endpoint-only E3 rho=0/rho=1 diagnostic that verifies actual profile assignment and realized arrival statistics before any formal matrix.

## Category C: targeted formal rerun

No formal rerun is mandated by the current audit alone. A rerun becomes necessary only if:

1. an existing result is shown to have used a different duration unit than the documented FedScale formula;
2. the historical fixed-threshold E5 code cannot be recovered or shown to consume the override;
3. the reviewer requires a completed E3 coupling-strength answer after endpoint separation;
4. a clean FADAS causal diagnosis is required rather than the conservative empirical statement.

Any such rerun should specify exact configurations and seeds first. Do not restart a full E1-E6 matrix merely to improve presentation.
