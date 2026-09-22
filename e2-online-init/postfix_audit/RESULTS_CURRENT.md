# Current E2 Results and Evidence Boundary

## Verified repaired ten-run comparison

The authorized desktop directories contain:

- online + unique-client, seeds 1–5;
- same-code full-warm + full-count, seeds 1–5;
- CIFAR-100, alpha 0.5, non-IID, `mild_label_correlated_hierarchical`;
- 100 clients, concurrency 40, buffer 10, ResNet, local learning rate 0.01, server learning rate 1.0, sketch dimension 2048, 500 rounds.

The commands omitted `--dirbridge_recluster_interval`, so the parser's DirBridge default was 5. They also did not set `--dirbridge_num_groups`, so the CIFAR-100 default resolution was K0=7. The exact commands are preserved only on the authorized desktop host; this repository includes a lightweight provenance table, not the raw logs.

| Variant | Final | Tail-10 | Tail-50 |
|---|---:|---:|---:|
| Online + unique observed clients | 47.928 ± 0.327 | 47.296 ± 1.185 | 46.463 ± 0.812 |
| Full warm + full counts | 47.070 ± 2.021 | 47.269 ± 1.164 | 46.596 ± 0.936 |

Paired online-minus-full differences are:

- Final: `+0.858` percentage points, 95% CI `[-1.571, +3.287]`;
- Tail-10: `+0.028` percentage points, 95% CI `[-1.301, +1.356]`;
- Tail-50: `-0.132` percentage points, 95% CI `[-1.156, +0.891]`.

These support “no clearly detected accuracy difference under this configuration,” not strict equivalence and not unbiasedness of the unique-client estimator.

## Numerical qualification

All ten accuracy files contain 500 finite values and all ten logs reach round 500 without traceback, OOM, or killed-process evidence. All ten logs also contain repeated `Test loss nan` rows, beginning at rounds 2–3 and ending by rounds 24–52. No non-finite loss row appears in the tail-50 or tail-10 window.

The original runs did not record per-batch input/logit/loss checks, parameter snapshots, BatchNorm running statistics, or checkpoints. Therefore:

- the accuracy traces are retained as finite prediction summaries;
- the loss and training-state health of the historical runs is unresolved;
- no claim of fully healthy finite training is made;
- the new evaluator and CSV diagnostics are available for future runs and short tests.

## B/C follow-up

The repaired B/C experiment is complete and is reported separately in `RESULTS_BC_CURRENT.md`. B (`online + oracle`) and C (`online + arrival_freq`) each contain five 500-round runs. B has final accuracy mean `8.522 ± 10.599%`, while C has `47.458 ± 2.173%`; however, four of five B seeds have non-finite final evaluation loss/logits, so this large gap is diagnostically confounded and must not be interpreted as a clean causal effect of oracle weights.

## Population-weight evidence

The new ten-run comparison is A versus D: it changes both initialization information and weight source. It does not isolate population-weight estimation.

No repaired B (`online + oracle`) or C (`online + arrival_freq`) output exists in the authorized run directories. The historical 60-run matrix is not substituted because it has a different code identity and is explicitly retained as historical. Consequently, the repaired oracle-versus-estimated comparison required by R3-1 is pending.

The current code labels the oracle as a reference-snapshot oracle, requires a compatible full-population reference, preserves measurement RNG streams, and reports `NA` when the reference is unavailable.

## What the ten runs support

They support a configuration-specific execution claim: DirBridge can start with only an online first wave and complete the specified CIFAR-100 stream without a full-client initialization pass. They do not establish universal deployment behavior, estimator unbiasedness, exact population-weight recovery, or numerical-health equivalence to a finite-state healthy run.
