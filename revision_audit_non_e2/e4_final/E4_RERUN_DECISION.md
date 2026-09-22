# E4 rerun decision

## Decision

**No training rerun required.**

## Reason

1. The archived E4 helper and the current public implementation use the same FedScale completion-time formula:

   `3 * batch_size * local_steps * computation / 1000 + (upload + download) / communication`.

2. The official FedScale caller/callee uses the same formula and numerical convention. The deterministic synthetic-profile test passes exactly.

3. Therefore there is no historical-versus-corrected timing interpretation to replay. `E4_EVENT_REPLAY.csv` is intentionally absent because no unit correction was required.

4. The existing 70 accuracy runs remain valid as runs of the documented real-profile-driven controlled coupling experiment, subject to corrected statistical interpretation and the logged GSpeech numerical-health limitation.

5. The primary statistical correction is FEMNIST: DirBridge wins 2 of 5 seeds and loses 3 against FedBuff; the mean paired tail-10 difference is small and its 95% interval crosses zero. GSpeech DirBridge versus FedASMU is positive in all five paired seeds, but the same numerical-health caveat applies to the existing GSpeech logs.

No targeted training rerun is necessary from the unit audit. A future numerical diagnostic would be a separate short instrumentation task, not a replacement of the 70-run E4 matrix.
