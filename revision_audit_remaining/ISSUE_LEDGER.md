# Remaining hard-task issue ledger

| Item | Status | Evidence / limitation |
|---|---|---|
| E1 FEMNIST validation development | DONE WITH LIMITATION | 24/24 verified; provenance and compact results committed. Final five-seed evaluation was not launched. |
| E4 clean 70-row numerical-health table | DONE WITH LIMITATION | Existing compact E4 table was corrected earlier; logits/parameters/BN are not logged, so health is unresolved where loss is non-finite. A fresh remaining-scope 70-row regeneration is still required for the requested schema. |
| E4 paired statistics | DONE WITH LIMITATION | Prior E4 paired statistics exist; remaining-scope cleaned-table output must be regenerated from one canonical 70-row table. |
| E4 physical FedScale unit chain | DONE WITH LIMITATION | Formula equivalence and a local deterministic test exist; physical payload-unit provenance and an official end-to-end caller test remain incomplete. |
| E4 event replay | NOT APPLICABLE pending unit result | No replay is justified until the physical unit chain is resolved; no training rerun has been launched. |
| E4 GSpeech diagnosis | BLOCKED BY MISSING LOGS | Existing logs lack logits, parameters, buffers, and checkpoints around NaN events; a short reproduction may be required if a causal classification is needed. |
| E5 paired K0/d_s summaries | DONE WITH LIMITATION | Existing E5 tables contain per-seed values and prior pairwise tables; remaining-scope canonical paired-summary CSVs still need generation. |
| E5 B work accounting | DONE WITH LIMITATION | Server rounds, protocol-derived returned updates, and available simulated time can be reported; accepted-valid counts are not complete in historical logs. |
| E5 Phi interpretation | DONE WITH LIMITATION | Sampling null and decomposition tables exist; interpretation is finite-buffer-sensitive and not proof of persistent skew. |
| CA2FL production-path equivalence | DONE WITH LIMITATION | Five-step helper/state-path test passed, but remaining-scope production-entry-path test must be added and run. |
| E6 actual algorithm-state ledger | REQUIRES TARGETED RERUN | Prior ledger used representative tensors; actual production initialization and state traversal are still required. No large training matrix is needed. |
| E3 endpoint scheduler diagnostic | BLOCKED BY MISSING LOGS | The authorized desktop and runtime were inaccessible in this resumed session; no CIFAR-100 client/profile artifacts were available locally and no endpoint CSVs were generated. Full rho training remains prohibited. |
| E2 modifications | NOT APPLICABLE | Explicitly excluded and untouched. |
| E4 70-run rerun | NOT APPLICABLE | Existing results are not automatically rerun. |
| E5 65-run rerun | NOT APPLICABLE | Existing results are not automatically rerun. |
| E1 full fair-tuning rerun | NOT APPLICABLE | E1 development work is complete; final evaluation remains a separate decision. |
