# E5 (R1-D4/D6, R2-5): Sensitivity of (B, K₀, dₛ) — design, configuration, and audited results

## 1. Purpose

R1-D4 asks how the buffer size B is set and whether it interacts with the data
distribution; R1-D6 asks how the number of direction groups K₀ is chosen and
whether it affects performance; R2-5 asks for sensitivity over K₀ and the Count
Sketch dimension dₛ. E5 answers all three at the paper's own default operating
point, with the confound controls the questions imply.

## 2. Design

One-factor-at-a-time around the shared default point (B, K₀, dₛ) = (10, 7, 2048):
CIFAR-100, α = 0.5, DIR-SKEW LATENCY (`mild_label_correlated_hierarchical`),
(M_c, B) = (40, 10), resnet, lr 0.01, local_bs 100, local_period 10, 500 rounds,
seeds 1–5 (the paper's seeds).

- **B ∈ {5, 10, 20}**, M_c fixed at 40, **two calibers**:
  - *rule*: staleness threshold = M_c/B (8 / 4 / 2) — the paper's default rule;
  - *fixed*: threshold pinned at 4.0 (`--dirbridge_buffer_delay_limit`) — isolates
    B from the threshold confound (at B = 10 fixed ≡ rule, not duplicated).
- **K₀ ∈ {1, 2, 4, 7, 12, 16}** (7 = ceil(log₂ 100), the code default).
- **dₛ ∈ {128, 512, 2048, 8192}**.
- 13 unique configurations × 5 seeds = **65 runs**.

Diagnostics beyond accuracy (logged every 5 rounds by the algorithm-independent
4-group balanced label-histogram reference monitor, plus E5-added state
diagnostics): buffer Φ_t, group coverage, cache-only group count, group
stability vs previous rebuild, non-empty groups, intra-/inter-group mean cosine
similarity, recluster time, process/device peak memory, simulated wall time.

## 3. Results

### Final-round accuracy (mean ± sd, 5 seeds)

| config | B | K₀ | dₛ | final |
|---|---|---|---|---|
| K₀ sweep | 10 | 1 | 2048 | 19.14 ± 7.15 |
| | 10 | 2 | 2048 | 43.83 ± 1.40 |
| | 10 | 4 | 2048 | 46.25 ± 1.56 |
| | 10 | **7** | 2048 | 47.11 ± 1.00 |
| | 10 | 12 | 2048 | 49.51 ± 0.69 |
| | 10 | 16 | 2048 | 49.03 ± 0.73 |
| B sweep (rule) | 5 | 7 | 2048 | 30.62 ± 3.49 |
| | **10** | 7 | 2048 | 47.11 ± 1.00 |
| | 20 | 7 | 2048 | 54.10 ± 0.53 |
| B sweep (fixed thr 4.0) | 5 | 7 | 2048 | 36.85 ± 1.68 |
| | 20 | 7 | 2048 | 54.59 ± 0.31 |
| dₛ sweep | 10 | 7 | 128 | 47.51 ± 1.53 |
| | 10 | 7 | 512 | 46.50 ± 2.25 |
| | 10 | 7 | 2048 | 47.11 ± 1.00 |
| | 10 | 7 | 8192 | 48.12 ± 0.52 |

### B (R1-D4)

**Decomposition.** With the threshold held at 4.0, raising B 5 → 20 gains 17.7
points: the buffer size itself dominates. Changing only the threshold: at B = 5
loosening 4.0 → 8.0 costs 6.2 points; at B = 20 tightening 4.0 → 2.0 changes
nothing measurable. A stricter threshold does not help once below the
arriving-staleness scale; a looser one hurts by admitting stale updates.

**Equal work reverses the fixed-round ranking.** B = 20 aggregates twice the
client work per round (~2.3× the wall time of B = 10). At matched simulated
work: B = 5 leads up to ~240 s, B = 10 leads near 500 s, B = 20 only overtakes
beyond ~800 s. The default B = 10 with the M_c/B rule is the throughput/accuracy
operating point; B = 20's apparent advantage at fixed rounds is mostly an
accounting effect.

**Variance shrinks monotonically with B** (±3.49 / ±1.00 / ±0.53).

**Mechanism** (direction-skew monitor means): buffer Φ_t 0.138 / 0.068 / 0.030,
group coverage 0.777 / 0.951 / 0.999, cache-only groups 4.77 / 2.37 / 0.54 of 7
for B = 5 / 10 / 20. Small buffers produce the phenomenon the paper targets;
the group memory then does the compensation.

**Distribution dependence.** B is a systems parameter, not algorithm-estimated.
Generally: Pr(group k absent from buffer) ≈ (1 − r_k)^B — larger B narrows the
gap for every group, but no B corrects a systematically wrong arrival mixture;
that is the group memory's and refill rule's job (see E2).

### K₀ (R1-D6)

The default is the closed-form rule K₀ = ceil(log₂ #classes) — CIFAR-10 → 4,
CIFAR-100 → 7, FEMNIST → 6, GSpeech → 6, TinyImageNet → 8 — with **no
per-dataset tuning**. On CIFAR-100 the default 7 sits at the foot of a plateau
(47.11 → 49.51 → 49.03 for 7 → 12 → 16; gains inside the 1–2 point
reproducibility band). The plateau has a mechanism: at K₀ = 12/16, 6.4/10.0 of
the groups are served purely from cache each round (too many groups for the
arrivals to feed), so finer partitions stop paying. At K₀ = 1 the grouping
collapses (stability −0.459, single centroid flips; 5× seed variance) —
diagnosed with the algorithm-independent reference monitor because the method's
own Φ_t is degenerate at K₀ = 1. K₀'s compute cost is negligible: total
recluster time 0.63–5.60 s over 500 rounds (< 0.4 %).

### dₛ (R2-5)

Grouping quality is flat across a 64× compression range: intra-group similarity
0.201 / 0.184 / 0.184 / 0.182, stability 0.791 / 0.781 / 0.778 / 0.778, buffer
Φ_t 0.064–0.070, coverage 0.950–0.958, cache-only 2.34–2.44 of 7 for
dₛ = 128 / 512 / 2048 / 8192 — every diagnostic moves by less than its own seed
noise, and accuracy differences (47.51 / 46.50 / 47.11 / 48.12) are inside the
per-seed spread. Two honest details: dₛ = 128 has the highest intra-group
similarity but the lowest inter-group separation (−0.000 vs 0.022 at 2048) —
compression pulls all directions toward a common one; the intra-minus-inter gap
(0.201 / 0.170 / 0.162 / 0.164) is the meaningful quantity and is not monotone
in dₛ. dₛ = 8192 has the tightest seed spread (±0.58). Conclusion: the sketch
dimension is not a sensitive knob on this workload; the default sits in the
flat region.

### Overhead columns (proxy caution)

Device peak memory rises monotonically with K₀ (5314 → 7302 MiB for K₀ = 1 → 16)
— the actual memory cost of K₀ groups. Process peak RSS stays flat
(~2015–2031 MiB) and **must not** be read as "K₀ costs nothing": the caches live
in accelerator memory (the same column-separation issue R3-4 raises; see E4's
resource audit, where CA2FL's N-model cache appears entirely in device memory).
Round runtimes across configurations were logged under different scheduler
concurrency phases and are comparable only within a phase; matched-work
comparisons use `simulated_wall_time`.

## 4. Configuration and identity

Single scheduler (`execute_by_npu_pool.sh`) on the desktop host; the matrix
survived one host-capacity OOM episode (concurrency 4 × ~7.5 GiB exceeded the
32 GB card; 19 partial runs deleted and rerun at lower concurrency) and one
code-identity split (E2 development was moved to a separate tree mid-run; two
runs started inside the patch window were deleted so every E5 run comes from one
tree). Final audit: 65/65 at 500 rounds, 0 partials, 0 orphans.

Code: main tree pre-E2 identity — `algorithm/dirbridge.py` gains
`--dirbridge_buffer_delay_limit` plus grouping diagnostics; `utils/options.py`
gains that flag; backups of both kept alongside (`*.bak_e5`).
