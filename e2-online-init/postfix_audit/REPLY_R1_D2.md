# Final reply to Reviewer 1, Comment 2

We thank the reviewer for pointing out this lack of clarity. We agree that the
previous manuscript did not clearly explain why different methods may leave
different parts of the problem unresolved. We apologize for the broad wording,
which could be interpreted as claiming that existing approaches are unable to
handle latency-biased participation. Their limitation is more specific:
existing methods mainly correct update staleness, update scaling, temporal
history, or client-level participation, while they do not explicitly enforce
the population mixture of update directions in each asynchronous buffer.
Therefore, a buffer may contain fresh and well-scaled updates while still
overrepresenting fast clients and missing some direction groups.

This distinction explains the different failure modes. FedBuff averages the
first returned updates and does not explicitly correct their population
composition. Staleness-aware methods modify the influence of observed updates,
but cannot reconstruct a direction group that is absent from the buffer. FADAS
adaptively rescales the received update and can improve optimization
stability, but does not explicitly estimate missing direction-group mass.
CA2FL is a stronger and closer baseline: accurate client-level caches can
compensate for participation bias, but each cache is refreshed only when its
corresponding client returns. DirBridge instead maintains shared
direction-group memories and activates them according to the estimated
deficit of each group. Thus, our claim is that these methods target different
correction quantities, rather than that they are universally ineffective.

To make the comparison fairer and more transparent, we performed
method-specific hyperparameter searches on CIFAR-10 with $\alpha=0.5$, seed
$100$, and $150$ rounds. The mean validation accuracy over the final ten
rounds was used for selection. The selected configurations were then
evaluated with five independent seeds for $500$ rounds. The results show that
existing methods can perform strongly after tuning, while DirBridge achieves
the best mean result in three of the four dataset--$\alpha$ settings. We will
add the following search protocol, search results, and five-seed comparison
to the revised manuscript.

## Table: Hyperparameter search protocol

| Method | Search space | Configurations |
|---|---|---:|
| CA2FL | Local learning rate $\in\{0.003,0.01,0.03,0.05\}$; global learning rate $\in\{0.1,0.5,1.0\}$ | 12 |
| FADAS | Local learning rate $\in\{0.003,0.01,0.03,0.1\}$; global learning rate $\in\{10^{-4},3\times10^{-4},10^{-3},3\times10^{-3}\}$; delay-adaptive $\in\{\mathrm{off},\mathrm{on}\}$ | 32 |

All configurations use CIFAR-10 with $\alpha=0.5$, seed $100$, and $150$
rounds. The selection metric is the mean validation accuracy over the final
ten rounds.

## Table: CA2FL hyperparameter search results

Values are validation accuracy (%) averaged over the final ten rounds.

| Local learning rate | Global lr $=0.1$ | Global lr $=0.5$ | Global lr $=1.0$ |
|---:|---:|---:|---:|
| 0.003 | 30.496 | 44.468 | 28.726 |
| 0.010 | 40.734 | 52.780 | 30.134 |
| 0.030 | 47.456 | **56.322** | 34.362 |
| 0.050 | 44.756 | 53.938 | 33.636 |

## Table: FADAS hyperparameter search results

Values are validation accuracy (%) averaged over the final ten rounds.

| Delay-adaptive | Local lr | $10^{-4}$ | $3\times10^{-4}$ | $10^{-3}$ | $3\times10^{-3}$ |
|---|---:|---:|---:|---:|---:|
| Off | 0.003 | 34.726 | 30.492 | 21.876 | 17.990 |
| Off | 0.010 | 43.194 | 32.320 | 25.710 | 20.284 |
| Off | 0.030 | 43.948 | 33.858 | 24.442 | 19.188 |
| Off | 0.100 | **44.888** | 34.654 | 25.746 | 18.612 |
| On | 0.003 | 48.048 | 36.502 | 22.256 | 21.712 |
| On | 0.010 | 47.924 | 40.112 | 30.204 | 21.878 |
| On | 0.030 | **56.710** | 49.648 | 35.450 | 30.192 |
| On | 0.100 | 40.890 | 42.372 | 28.750 | 20.246 |

The selected configurations were CA2FL with local learning rate $=0.03$ and
global learning rate $=0.5$, and FADAS with local learning rate $=0.03$,
global learning rate $=10^{-4}$, and delay-adaptive updates enabled.

## Table: Five-seed formal results

Values are validation accuracy (%) averaged over the final ten rounds. Each
value is the mean $\pm$ sample standard deviation over five seeds.

| Dataset | $\alpha$ | FedBuff | DirBridge | CA2FL | FADAS |
|---|---:|---:|---:|---:|---:|
| CIFAR-10 | 0.1 | $49.962\pm5.099$ | $62.061\pm4.140$ | $\mathbf{64.592\pm4.211}$ | $61.901\pm1.607$ |
| CIFAR-10 | 0.5 | $54.494\pm6.499$ | $\mathbf{76.273\pm4.378}$ | $63.650\pm12.679$ | $74.146\pm1.275$ |
| CIFAR-100 | 0.1 | $35.686\pm4.581$ | $\mathbf{45.165\pm1.159}$ | $43.573\pm2.088$ | $34.195\pm1.026$ |
| CIFAR-100 | 0.5 | $43.036\pm3.144$ | $\mathbf{50.284\pm1.628}$ | $46.344\pm1.623$ | $36.448\pm0.544$ |

The current formal records use local learning rate $=0.03$; no formal results
with local learning rate $=0.3$ are included. For FedBuff and DirBridge, the
configuration records global learning rate $=0.5$, while the evaluated
implementation directly adds the aggregated delta, corresponding to an actual
server-delta multiplier of $1.0$.

We will revise the related-work and motivation discussion to state that
existing methods can partially alleviate latency-biased participation, but do
not directly control latency-induced direction-mixture distortion. We will
also include the hyperparameter search protocol, the complete search results,
and the five-seed comparison in the revised manuscript.
