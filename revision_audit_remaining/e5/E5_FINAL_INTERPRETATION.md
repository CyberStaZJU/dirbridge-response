# E5 final interpretation

The canonical raw manifest contains 13 configurations × 5 seeds = 65 complete runs, each with 500 accuracy rows and finite final/tail accuracy. The requested paired summaries use raw per-seed tail-10 values, mean and sample SD, paired differences against the stored baseline, a two-sided 95% t interval with df=4, and wins/losses/ties. They are exploratory and use no multiplicity correction.

K0 is materially sensitive in this setting: K0=1 is substantially below K0=7, while K0=12 and K0=16 have higher stored means than the pre-specified heuristic K0=7. This supports an accuracy–memory/refresh trade-off, not a claim that K0=7 is empirically optimal. Sketch dimension is comparatively robust over ds=128–8192; deviations from ds=2048 are small relative to the K0=1 effect.

Finite-buffer sampling remains a null-compatible explanation for nonzero per-round skew statistics. The existing sampling-null and Phi-decomposition evidence separates persistent mixture bias from round-to-round finite-buffer fluctuation, but does not establish persistent latency-induced selection. Combined with incomplete accepted-update accounting, E5 supports sensitivity and finite-buffer conclusions only; it does not support an equal-work superiority or causal persistence claim.
