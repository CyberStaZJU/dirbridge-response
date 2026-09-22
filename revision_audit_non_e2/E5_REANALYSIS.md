# E5 Reanalysis: B, K0, and Count Sketch dimension

## Configuration identity

The intended design is 13 unique configurations times five seeds: B in {5,10,20} with rule and fixed-threshold controls, K0 in {1,2,4,7,12,16}, and sketch dimension in {128,512,2048,8192}, with the shared CIFAR-100 alpha=0.5, 500-round setting. The source document reports 65/65 complete, finite runs and preserves the pre-E2 code identity.

## What the existing results support

The B sweep shows a strong fixed-server-round dependence on B, but B changes the amount of client work per round. The source record itself reports that matched simulated work reverses the fixed-round ranking. Therefore fixed-round accuracy must not be called equal-work evidence. Report server rounds, returned updates, and simulated time separately wherever the raw files support them.

The K0 means increase from 7 to 12 in the stored summary (47.11 to 49.51), with K0=16 at 49.03. The correct wording is that K0=7 is a pre-specified heuristic that lies in a broad performance region, not that it is the empirical optimum. K0=8192 is also higher than 2048 in the stored d_s means, so d_s=2048 should be described as a stable default in a broad region, not as optimal.

## K0=1 equivalence requirement

The existing explanation invokes centroid flipping. That cannot explain a one-group implementation by itself because there is no alternate group assignment. A deterministic test is required comparing K0=1 against a FedBuff-style gated aggregate using the same valid buffer, server learning rate, and state-dict treatment. Until that test is run, the K0=1 mechanism remains unresolved.

## Phi and coverage

The stored Phi and coverage values may be compatible with ordinary finite-buffer sampling variation. They are not, by themselves, evidence of persistent latency-selected representation skew. The appropriate reanalysis uses actual population group proportions and the finite-population null, then separates persistent mixture bias from round-to-round fluctuation. No new training is needed for this calculation if the raw monitor rows are available.

## Fixed-threshold control

The current public parser and DirBridge implementation expose and consume `dirbridge_buffer_delay_limit`. Historical E5 runs must nevertheless retain their pre-E2 code identity; they must not be silently relabeled as current-tree runs. The control isolates one threshold confound but does not make the complete B comparison an equal-work experiment.

## Revised conclusion

E5 supports sensitivity and systems-cost statements under the stated workload. It does not by itself establish persistent latency-induced skew, an empirical K0 optimum, or equal-work superiority for any B.
