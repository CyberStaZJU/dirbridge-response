# E1 (R3-3, R1-D2): Fair tuning budget and anomalous-baseline diagnosis

## 1. What the reviewer asked, and what we did

R3-3 asks that every method receive the **same tuning opportunity and budget**,
that seeds be paired with confidence intervals, and that the CA2FL-near-random
and FADAS-high-variance behaviours be explained rather than exploited. R1-D2
asks for the failure modes to be described by *what each method changes*, with
the mechanism separated from the accident of a particular configuration.

Protocol actually used (identical for every baseline, DirBridge excepted — see
§6):

- **20 pre-registered trials per method per dataset**, listed in
  `commands_dev.sh`; no trial was dropped or hidden, including diverged ones.
- **Independent dev seed (100)**, distinct from the evaluation seeds 1–5.
- **150 rounds** for selection, tail-10 mean as the criterion.
- Common search over local LR; method-semantic search over server LR
  (CA2FL) and adaptive step / delay-adaptive flag (FADAS); FedBuff included as
  a reference so the tuned methods are not the only ones receiving attention.
- Locked configurations then run at **500 rounds × seeds 1–5**, with paired
  per-seed differences and 95% CIs (t, df = 4).
- Divergence and NaN recorded, not removed.

## 2. Code facts established before tuning

- **CA2FL**: the update formula matches the paper
  (`G_CA = (1/N)Σc_i − (1/B)Σ_{i∈B}c_i + agg(Δ_B)`), but the server step
  `eta` was **hardcoded to 1.0** with no CLI control. There was therefore no
  way to tune the server step at all, in our code or in the experiments as
  originally run. We added `--global_lr` (default `None` → eta = 1.0, i.e.
  bit-identical to previous behaviour) so that the server step became tunable.
  **We do not claim this as an improvement to CA2FL** — it is a repair of our
  harness that the reviewer's question exposed.
- **FADAS**: the adaptive step is `global_lr · m/√v̂`, and the non-text default
  is `global_lr = 1e-4`.
- **FedBuff**: `w += mean(Δ_B)`, local LR only, no server scaling.

## 3. Diagnostic instrumentation

A recording-only patch (`utils/e1_diagnostics.py`, plus a few lines in
`ca2fl.py` / `fadas.py`, all try/except guarded) writes `<name>-e1_diag.csv`
alongside the system metrics: update norm, model norm, first non-finite round,
buffer mean delay, and per-method columns — CA2FL cache-correction norm,
aggregate norm, their ratio, BN running-var min/max; FADAS effective step,
v̂ median, m norm, max delay. It changes no update formula.

## 4. Results

### 4.1 Dev selection (150 rounds, dev seed 100)

**CIFAR-10 (α=0.5, DIR-SKEW, (M_c,B)=(40,10), resnet)** — best 4 of 20:

| method | best trial | tail-10 |
|---|---|---|
| FedBuff | lr=0.003, bs=50 | **11.11** (all 20 trials 10.0–11.1; best-ever 28.1) |
| CA2FL | **lr=0.03, eta=0.5** | **57.06** (best 65.03) |
| FADAS | lr=0.03, glr=1e-4 (original) | 11.83 (best-ever 43.45; 17/20 trials at 10.0) |

**FEMNIST (FedScale profile coupling, (400,100), cnn)** — best of 20:

| method | best trial | tail-10 |
|---|---|---|
| FedBuff | lr=0.05, bs=100, period=10 | **82.46** |
| CA2FL | lr=0.05, eta=1.0 (original) | **82.16** |
| FADAS | lr=0.03, glr=1e-4 (original) | **51.01** (150 rounds, not yet converged) |

### 4.2 Formal run (500 rounds × seeds 1–5)

Only the scenario the user prioritised was run formally:
**CIFAR-10, CA2FL at lr=0.03, eta=0.5**.

| seed | CA2FL (tuned) | DirBridge | CA2FL (original config) |
|---|---|---|---|
| 1 | 37.17 | 70.17 | 10.00 |
| 2 | 63.06 | 67.98 | 10.00 |
| 3 | 32.66 | 77.47 | 10.00 |
| 4 | 77.45 | 71.71 | 10.00 |
| 5 | 37.02 | 73.36 | 10.00 |

- CA2FL tuned: **49.47 ± 19.73**; DirBridge: **72.14 ± 3.58**; CA2FL original:
  10.00 on all five seeds.
- Paired DirBridge − CA2FL: mean **+22.67**, sd 21.83,
  **95% CI [−4.43, +49.77]**, t = 2.32 → **not significant** at df = 4.

### 4.3 Diagnosis of the two anomalies

**CA2FL — configuration, with one implementation-sensitivity that is a
consequence rather than an independent cause.**

- With `eta = 1.0` (the hardcoded original) the ratio
  ‖cache correction‖ / ‖aggregate‖ reaches a **peak of 48.4** (a healthy value
  is ≲ 1) and ends around 0.59–0.76, and **BN running variance goes negative**
  (−46.4, −46.1, −48.2) — but *only* in the eta = 1.0 trials. With eta = 0.5 the
  peak ratio drops to 1.6–9.8 and BN variance stays positive (0.006–0.010).
- No trial produced a non-finite weight: this is directional stalling, not a
  numerical blow-up.
- The opposite failure also appears, symmetrically: eta = 0.05/0.01 leave the
  ratio at 0.01–0.04 and the model barely moves. eta is the single governing
  knob.
- **After tuning, CA2FL is no longer broken**: 10.00 → 49.47 mean, with one
  seed reaching 77.45.

**FADAS — configuration, and the search shows why no better setting exists.**

- At `global_lr = 1e-4` the effective step is ~1e-4·sign per round (v̂ median
  ~1e-11, denominator ≈ ε); the model cannot accumulate enough displacement in
  500 rounds.
- Raising `global_lr` to 0.01 / 0.1 / 1.0 makes the **update norm explode**:
  38.7 → 3.6e4 → 8.4e6 → 9.6e11. v̂ is an EMA with long memory and cannot track
  the sudden large gradients, so the denominator does not grow and the step
  amplification destroys the model. This is the mechanism behind the "one seed
  climbs to 70 then collapses" pattern in the original matrix.
- Consequently the **only stable configuration is the original one**, and we
  report FADAS as under-tuning-friendly rather than as a method we successfully
  rescued.

**FedBuff on CIFAR-10 — not rescued by tuning, and we state this cautiously.**
All 20 trials (local LR 0.003–0.1 × batch/period combinations) stay at
10.0–11.1. We regard this as evidence that this setting is intrinsically hard
for uncompensated aggregation, but we do **not** claim to have exhausted
FedBuff's hyperparameter space: our search covered local LR, batch size and
local period only, and a broader search (optimiser, momentum, warm-up) might
find a working configuration. We report the search space explicitly so the
reader can judge the strength of this evidence.

## 5. What E1 supports, and what it does not

Supported:

- The CA2FL and FADAS anomalies on CIFAR-10 DIR-SKEW are **configuration
  effects**, with concrete mechanisms (server step magnitude; adaptive
  denominator failure under amplified steps). Neither required an
  implementation fix to the update rule; the CA2FL change was exposing a
  previously untunable knob.
- After fair tuning, CA2FL recovers from 10.00 to a functioning method, but
  DirBridge remains ahead by 22.67 points in the mean **with a CI that crosses
  zero**, because CA2FL's seed spread (±19.7) is 5.5× DirBridge's (±3.6).

Not supported, and explicitly not claimed:

- **Not statistically significant.** With five seeds the paired CI is
  [−4.43, +49.77]. A reviewer is entitled to read the advantage as unproven on
  this setting; more seeds would be needed to tighten it.
- **Escape-time is not a valid advantage argument.** In the 500-round runs
  CA2FL leaves the plateau at rounds 12–38 and DirBridge at 17–33 — they are
  comparable, and CA2FL is earlier on two seeds. An earlier impression that
  DirBridge escapes ~4× faster came from a 150-round single-seed dev view and
  **is withdrawn**.
- **Only one formal scenario was run.** FEMNIST finals and CIFAR-10 FedBuff /
  FADAS finals were not executed, so no claim is made about CA2FL on FEMNIST,
  nor about whether *all* baselines remain behind DirBridge after tuning.
- **DirBridge figures come from the original paper matrix.** The current tree
  now also carries the E2 changes (which touch initialisation paths only, not
  the training maths of this setting), and the code identity has not been
  re-verified by a rerun under the current tree. This should be done before
  these numbers are quoted as final.

## 6. Note on symmetry

DirBridge itself was **not** tuned in E1 — it uses the paper's defaults, which
were selected during the original work. This is the asymmetry the reviewer is
right to worry about, and we state it plainly: giving the baselines a tuning
budget while DirBridge keeps its previously chosen settings is favourable to
DirBridge. The honest mitigation is that the paper's DirBridge defaults were
also arrived at by search, and that the CA2FL result above shows the tuned
baseline can beat DirBridge on individual seeds.
