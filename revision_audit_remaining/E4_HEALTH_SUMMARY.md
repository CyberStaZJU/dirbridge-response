# E4 numerical-health clean audit

The canonical clean table contains 70 unique dataset/method/seed rows (35 FEMNIST + 35 GSpeech). 0 duplicate raw accuracy files were excluded and listed with provenance. Every retained accuracy file has 500 finite accuracy rows. GSpeech scheduler logs show non-finite test loss beginning at round 2 or 3 in affected runs; tail rounds 491–500 were checked. Parameters, logits, and BN buffers were not logged, therefore affected runs are **unresolved**, not healthy. Finite accuracy alone does not establish numerical health.
