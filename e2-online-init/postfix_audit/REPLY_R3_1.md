# Final reply to Reviewer 3, Comment 1

We thank the reviewer for this suggestion. It led us to separate three concerns
that the original presentation conflated: whether DirBridge can begin without a
full pass over all clients, how the population weights $(p_k)$ can be estimated
online, and how latency bias in the observed stream affects such estimates. We
report the main results in this reorganized form on CIFAR-100 with
$\alpha=0.5$. All settings share the client partition, the delay process, the
random seeds, and the training configuration (100 clients, concurrency
$M_c=40$, buffer size $B=10$, ResNet, local/server learning rates $0.01/1.0$,
$K_0=7$ direction groups, sketch dimension $d_s=2048$, reclustering interval
$5$, $500$ rounds). Every online setting assigns a client to a direction group
only after its asynchronous result becomes observable, and all reported accuracy
traces are complete and finite over the 500 rounds.

## Main results without full-client initialization

| Setting | Final | Tail-10 | Tail-50 |
|---|---:|---:|---:|
| Full-warm reference (exact population weights) | $47.070 \pm 2.021$ | $47.269 \pm 1.164$ | $46.596 \pm 0.936$ |
| Online, arrival-frequency weights | $47.458 \pm 2.173$ | $47.643 \pm 0.999$ | $46.349 \pm 0.665$ |
| Online, unique-client weights | $47.928 \pm 0.327$ | $47.296 \pm 1.185$ | $46.463 \pm 0.812$ |

The full-warm reference and the unique-client variant share one code identity;
the arrival-frequency control was rerun under a repaired identity. All values
are five-seed means $\pm$ sample SD in percent.

## Oracle population weights versus online estimated weights

The full-warm reference is precisely the oracle-weight setting. Observing the
entire client population yields $p_k$ exactly, so its weight estimation error is
zero by construction, and the implementation records a weight $L_1$ error of
exactly $0$ whenever this path is exercised. The online unique-client variant is
the estimated-weight setting. Across five seeds, the paired differences (online
minus full-warm) are $+0.858$ percentage points for final accuracy with a $95\%$
confidence interval of $[-1.571,+3.287]$, $+0.028$ for tail-10 accuracy with
$[-1.301,+1.356]$, and $-0.132$ for tail-50 accuracy with $[-1.156,+0.891]$; all
three intervals include zero. In this configuration, replacing exact population
weights with the online estimator produces no clearly detected accuracy
difference. This comparison couples the weight source with the initialization
mode, which is inherent to the deployment scenario the reviewer describes:
exact population weights presuppose having observed the entire population. The
arrival-frequency control performs on par with the other settings in summary
statistics; because it was run under the repaired code identity, we compare it
without paired claims. These results support configuration-specific online
operation. They do not establish strict equivalence, universal deployment
behavior, or unbiasedness of the estimators, and the revised manuscript states
these boundaries explicitly.

## How DirBridge handles latency bias in the observed stream

DirBridge does not assume that the latency-biased observed stream is an unbiased
estimator of the population. If $r_k$ denotes the probability that an observed
arrival belongs to direction group $k$, then, in general,
$r_k \propto p_k \lambda_k$, where $\lambda_k$ is the group-dependent arrival
rate; raw arrival frequencies recover the arrival mixture rather than the
population mixture, and the arrival-frequency control in the table is precisely
the setting that consumes them. The unique-client estimator removes one specific
component of this bias---repeated arrivals of the same client no longer inflate
its weight---while group-level latency bias within the already-observed set
remains. We quantify the remaining finite-coverage uncertainty explicitly:

$$
\big\lVert \widehat{p}-p \big\rVert_1 \;\leq\;
2\left(1-\frac{N_{\mathrm{seen}}}{N}\right),
$$

where $N_{\mathrm{seen}}$ is the number of distinct observed clients and $N$ the
total number of clients. The implementation separates group assignment from
weight estimation, records the weight source of every run, and tracks
$N_{\mathrm{seen}}$ so that this bound can be evaluated at any round.
Accordingly, our revised claim is limited to configuration-specific online
operation with explicit coverage-dependent uncertainty; the online estimator
bounds and reports its own bias rather than assuming it away.
