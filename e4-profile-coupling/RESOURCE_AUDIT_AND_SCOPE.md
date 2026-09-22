# E4 (R3-2) addendum: resource audit, honest scope, and what remains

## 1. Scope correction: device-capability profiles, not a latency trace

The data source (`fedscale_device_info/client_device_capacity`, 500,000 records)
holds per-device **capability samples** (`computation`, `communication`), not
end-to-end latency time series and not RTT. Per-client durations are derived
with the standard compute-plus-transfer model

```
L_i = 3.0 · local_bs · local_period · computation_i / 1000 + (S↑ + S↓) / communication_i
```

Both transport sizes were left at the default 1 MB (actual models: cnn
444,062 params = 1.69 MiB fp32; melcnn 97,411 = 0.37 MiB). The communication
term is negligible: measured against the three realized speed tiers
(FEMNIST bs=50, lp=10), its share of total duration is 0.0012 % / 0.00014 % /
0.00018 % (fast/mid/slow). For communication to reach even 1 % of the compute
term the model payload would need to be 1.6–14.4 GB. **The three speed tiers are
ordered entirely by compute capability.**

Wording: say *real FedScale device-capability profiles, with per-client service
durations derived by the standard compute-plus-transfer model*. Do not say
"real latency trace" or "measured end-to-end latency". A true observed-latency
source (FCC MBA, RIPE Atlas — named in the planning document) is not covered by
this experiment and remains open; the desktop host has no outbound HTTPS, so
such data would have to be brought in over the laptop path.

## 2. Resource audit over all 70 runs (process peak / device peak / runtime)

Aggregated from per-run system-metrics CSVs (500 rows each), 7 algorithms ×
5 seeds × 2 datasets. Peak = max over rounds; MiB.

### FEMNIST (N=1000, model 1.694 MiB fp32)

| algo | process peak | device peak | dev − FedBuff | final acc | runtime (s) |
|---|---|---|---|---|---|
| FedBuff | 3513 ± 1 | 1871 ± 6 | +0 | 74.72 ± 1.34 | 6262 ± 185 |
| FedBuffMALight | 3514 ± 1 | 1879 ± 8 | +8 | 12.52 ± 15.39 | 6386 ± 277 |
| FADAS | 3513 ± 1 | 1883 ± 9 | +12 | 68.34 ± 0.84 | 6295 ± 175 |
| FedASMU | 3514 ± 1 | 1871 ± 22 | +0 | 57.08 ± 4.71 | 6724 ± 280 |
| CASA | 3514 ± 1 | 1908 ± 25 | +37 | 72.87 ± 4.84 | 6922 ± 180 |
| CA2FL | 3513 ± 3 | **3537 ± 13** | **+1666** | 66.48 ± 8.22 | 6297 ± 153 |
| **DirBridge** | 3513 ± 3 | 1949 ± 25 | **+78** | **76.49 ± 6.55** | 6417 ± 136 |

### GSpeech (N=1000, model 0.372 MiB fp32)

| algo | process peak | device peak | dev − FedBuff | final acc | runtime (s) |
|---|---|---|---|---|---|
| FedBuff | 3142 ± 12 | 902 ± 0 | +0 | 1.50 ± 0.00 | 1390 ± 5 |
| FedBuffMALight | 3144 ± 8 | 896 ± 0 | −6 | 9.75 ± 6.84 | 1366 ± 27 |
| FADAS | 3234 ± 27 | 897 ± 0 | −5 | 14.86 ± 12.27 | 1399 ± 14 |
| FedASMU | 3022 ± 36 | 900 ± 4 | −2 | 37.84 ± 2.80 | 2401 ± 59 |
| CASA | 3147 ± 8 | 900 ± 2 | −2 | 1.50 ± 0.00 | 1984 ± 20 |
| CA2FL | 3225 ± 14 | **1242 ± 0** | **+340** | 1.50 ± 0.00 | 1513 ± 13 |
| **DirBridge** | 3119 ± 11 | 898 ± 0 | **−4** | **61.33 ± 1.76** | 1458 ± 18 |

### This resolves R3-4's memory puzzle quantitatively

CA2FL's N × model client cache appears **entirely in device memory, not in
process RSS**: process-peak difference vs FedBuff is −0.5 MiB (FEMNIST) and
+82.9 MiB (GSpeech) — essentially zero — while the device-peak difference is
+1666.1 and +340.3 MiB against predictions of 1694.0 and 371.6 MiB
(ratios 0.984 and 0.916; GSpeech's shortfall is consistent with lazy cache
population, do not present as exact). The paper's Table VI reported the wrong
column.

DirBridge's own device-peak overhead is +78.1 MiB on FEMNIST and indistinguishable from zero on GSpeech in this multi-job measurement. The observation is compatible with group caches and sketch-related allocations, but the CSV peak alone does not identify the exact allocation by component. We therefore do not attribute the full ~68 MiB residual to sketch arrays without a direct persistent-state ledger.

**Headline comparison**: the measured FEMNIST device-peak difference was +1666 MiB for CA2FL versus +78 MiB for DirBridge. These are historical per-run peaks, not by themselves a proof of persistent state or a complete logical-memory decomposition.

**Methodological warning for Table VI**: process peak is within 1–3 MiB across
all seven algorithms on both datasets (FEMNIST: 3513–3514 for every algorithm),
so it carries no information about algorithm state; device peak separates them.
E5 independently shows the same split (device peak rises 5314 → 7302 MiB with
K₀ while process RSS stays at ~2015–2031). Device peak is the
algorithm-state-bearing column.

### Runtime caveats

DirBridge costs +2.5 % (FEMNIST) / +4.9 % (GSpeech) wall clock over FedBuff. On
GSpeech quote the comparison against the runner-up FedASMU instead (FedBuff
collapsed to the 1.50 plateau): DirBridge +23.5 points at 1458 s vs FedASMU's
2401 s — more accurate and 39 % faster. `runtime_sec` is host wall clock under
multi-job concurrency (up to 7 jobs on FEMNIST): comparable across algorithms
within a dataset, not single-job latency. `simulated_wall_time` varies > 3×
across seeds on the same algorithm here (sampler draw sensitivity) and must not
be used for matched-work comparisons in this matrix (unlike E5).

The reported values are per-run maxima from the system-metrics CSVs. A flat historical peak does not by itself prove current persistent residency; current allocation, reserved allocation, and logical state must be measured separately. The public audit therefore treats these values as historical device-peak evidence, not a complete persistence ledger.
