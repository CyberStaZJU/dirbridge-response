# E5 final interpretation

## Reconstruction and provenance

The external E5 tree contains exactly 65 accuracy files: 13 unique configurations × 5 seeds, all with 500 accuracy rows and corresponding metrics. The 13 configurations are:

- K0 ∈ {1, 2, 4, 7, 12, 16} at B=10, d_s=2048;
- d_s ∈ {128, 512, 2048, 8192} at B=10, K0=7;
- B=5, 10, 20 controls, with rule and fixed-threshold variants where applicable.

No missing or duplicated `(configuration, seed)` pair was found in `E5_RUN_MANIFEST.csv`. The archived E5 identity is pre-E2. The command manifests explicitly contain `--dirbridge_buffer_delay_limit 4.0` for B=5 and B=20 fixed controls. The public parser and `algorithm/dirbridge.py::_buffer_delay_limit` implement the override, and `scripts/test_e5_sensitivity.py` tests membership at the threshold boundary.

## B: buffer size and work accounting

Tail-10 results:

- B=5 rule: `29.486 ± 3.494`
- B=5 fixed threshold 4: `37.081 ± 1.557`
- B=10 default: `47.423 ± 0.790`
- B=20 rule: `54.152 ± 0.747`
- B=20 fixed threshold 4: `54.457 ± 0.464`

The fixed gate removes the B-dependent threshold change but does not equalize aggregation frequency, returned-client work, accepted updates, or simulated time. Historical CSVs provide 500 server rounds, simulated wall time, and runtime, but not a complete per-round completed-returned-update or accepted-valid-update ledger. `E5_B_WORK_ACCOUNTING.csv` marks those fields missing. Thus B=20's fixed-round advantage is not equal-work superiority, and equal simulated time must not be called equal local-update work.

## K0: group count

Raw tail-10 values:

- K0=1: `23.114 ± 6.999`
- K0=2: `42.705 ± 1.771`
- K0=4: `46.528 ± 0.940`
- K0=7: `47.423 ± 0.790`
- K0=12: `48.928 ± 0.983`
- K0=16: `48.697 ± 0.727`

`E5_K0_PAIRED_STATS.csv` contains every seed-level difference versus K0=7. K0=12 is higher than K0=7 in this setting; K0=7 is the pre-specified heuristic default, not an empirical optimum. The historical direction-skew metrics provide nonempty-group, cache-only-group, similarity, and reclustering fields, but they do not establish a monotonic accuracy mechanism.

The deterministic two-step K0=1 test compares the sole-group DirBridge aggregate with the arithmetic mean of the same valid buffer and verifies equality. With one group, there is no alternative cluster assignment; the old centroid-flip explanation is not used.

## d_s: sketch dimension

Raw tail-10 values:

- d_s=128: `46.992 ± 2.166`
- d_s=512: `46.610 ± 0.731`
- d_s=2048: `47.423 ± 0.790`
- d_s=8192: `47.258 ± 0.592`

`E5_DS_STATS.csv` contains seed-level differences versus d_s=2048. The results support robustness over 128–8192, not optimality of 2048. Historical metrics contain grouping similarity and reclustering time; a complete unique sketch-state memory ledger is not available.

## Sampling null and Phi decomposition

The saved monitoring partition is four balanced groups with population sizes `[25,25,25,25]`. `E5_SAMPLING_NULL.csv` computes, for each B, the without-replacement null expectation:

```text
E0[Phi] = (N-B)/(B*(N-1)) * (1-sum(p_k^2))
E0[coverage] = mean_k [1 - C(N-N_k,B)/C(N,B)]
```

The table compares these values with observed logged means. Nonzero Phi is expected under finite-buffer sampling and is not, by itself, evidence of persistent latency-induced skew.

`E5_PHI_DECOMPOSITION.csv` reconstructs the persistent-mixture-bias and round-to-round-fluctuation terms from the periodic `buffer_counts` and `valid_counts` rows where available. These are logged monitor samples, not a hidden full-resolution trajectory; status and sampling cadence are retained in the table.

## Final conclusion

E5 shows that B materially affects fixed-server-round accuracy and variance, but work accounting prevents an equal-work claim. K0 materially affects accuracy: K0=1 is much lower, while K0=12/16 exceed the pre-specified K0=7 mean in this setting, indicating an accuracy–memory/refresh trade-off. Sketch dimension is comparatively robust across the tested range. The sampling null and decomposition prevent ordinary finite-buffer variation from being presented as proof of persistent latency-selection bias. No training rerun is required by the reconstructed provenance or deterministic tests.
