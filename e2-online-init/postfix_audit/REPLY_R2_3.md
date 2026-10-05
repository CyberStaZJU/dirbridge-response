# Final reply to Reviewer 2, Comment 3

We agree. We will add the following worked example immediately after
Algorithm 1 in the revision. It uses one-dimensional scalar updates so that
every arithmetic step can be checked by hand; all quantities follow the
notation table of our response to Comment 1.

## Setup

$N=10$ clients, $K=2$ direction groups, buffer size $B=4$, concurrency
$M_c=8$ (so the staleness threshold is $M_c/B=2$), server step size
$\eta_t=1$, EMA factor $\beta=0.9$. The population is
$\mathcal{G}_1=\{$3 clients$\}$ and $\mathcal{G}_2=\{$7 clients$\}$, giving
population weights $p_1=0.3$ and $p_2=0.7$. Group 1's cache $m_1$ is empty (no
member has arrived yet); group 2's cache from the previous round is $m_2=1.0$.

## Round $t$: collect and filter

The first four returned updates are $c_1, c_2, c_3, c_4$ with staleness
$\tau=(0,1,4,0)$ and scalar deltas $(1.0,\,2.0,\,0.5,\,3.0)$. Client $c_3$
(assigned to group 1) fails the staleness filter ($\tau_{c_3}=4>2$), so the
valid buffer is $\mathcal{V}_t=\{c_1,c_2,c_4\}$ with $|\mathcal{V}_t|=3$:
$c_1\in\mathcal{G}_1$ and $c_2,c_4\in\mathcal{G}_2$. Hence $n_{t,1}=1$,
$n_{t,2}=2$.

## Targets and refill rule

The population-scaled targets are $q_{t,1}=|\mathcal{V}_t|\,p_1=0.9$ and
$q_{t,2}=3\times0.7=2.1$. Fresh group means are $\bar{\Delta}_{t,1}=1.0$ and
$\bar{\Delta}_{t,2}=(2.0+3.0)/2=2.5$. For group 1,
$n_{t,1}=1\geq q_{t,1}=0.9$: the group is sufficiently represented, so only
the fresh mean is used, $\widetilde{\Delta}_{t,1}=\bar{\Delta}_{t,1}=1.0$.
For group 2, $0<n_{t,2}=2<q_{t,2}=2.1$: the group is underrepresented, so the
cache partially compensates with blending weight
$\lambda_{t,2}=n_{t,2}/q_{t,2}=2/2.1\approx0.952$:

$$
\widetilde{\Delta}_{t,2}
=\lambda_{t,2}\bar{\Delta}_{t,2}+(1-\lambda_{t,2})\,m_2
\approx 0.952\times2.5+0.048\times1.0\approx2.43 .
$$

## Global update and cache refresh

The server applies
$w\leftarrow w+\eta_t(p_1\widetilde{\Delta}_{t,1}+p_2\widetilde{\Delta}_{t,2})
=0.3\times1.0+0.7\times2.43\approx2.00$. Afterwards the caches of groups with
arriving members are refreshed: $m_1$ is initialized directly with its first
observation ($m_1\leftarrow\bar{\Delta}_{t,1}=1.0$), and
$m_2\leftarrow0.9\times1.0+0.1\times2.5=1.15$. The example thus exercises
three lines of the compensation rule---sufficient representation, partial
blending, and first-time cache initialization---in a single round.

## Absent-group case

If instead no group-1 client had passed the filter in a later round
($n_{t,1}=0$) while its cache were ready ($m_1=1.0$), the same rule would set
$\widetilde{\Delta}_{t,1}=m_1=1.0$, and the update would become
$0.3\times1.0+0.7\times\bar{\Delta}_{t,2}$, with $m_1$ left unchanged because
no group-1 member arrived. This shows how a missing direction is bridged by
its group memory at exactly its population mass $p_1=0.3$, rather than being
silently dropped from the aggregation.
