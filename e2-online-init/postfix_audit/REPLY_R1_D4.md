# Final reply to Reviewer 1, Comment D4

We thank the reviewer for this question. It prompted us to run a controlled
buffer-size sensitivity study (five seeds per configuration, 500 rounds,
CIFAR-100 with $\alpha=0.5$), which we summarize below and will add to the
revised manuscript.

## How $B$ is set

$B$ is a systems parameter of the deployment, not a quantity the algorithm
estimates from data. It interacts with the staleness threshold, which our
default rule sets to $M_c/B$: changing $B$ alone therefore confounds two
effects. We thus swept $B\in\{5,10,20\}$ with the concurrency $M_c=40$ fixed
under two calibers---the default rule (threshold $8/4/2$) and a threshold
pinned at $4.0$ to isolate $B$ itself. With the threshold held fixed, raising
$B$ from 5 to 20 improves final accuracy by $17.7$ percentage points
($36.85\pm1.68 \rightarrow 54.59\pm0.31$), so the buffer size itself dominates.
Varying only the threshold shows the opposite direction: loosening $4.0$ to
$8.0$ at $B=5$ costs $6.2$ points, while tightening $4.0$ to $2.0$ at $B=20$
changes nothing measurable. A threshold stricter than the arriving-staleness
scale does not help; a looser one hurts by admitting stale updates.

## The fixed-round comparison is an accounting effect

$B=20$ aggregates twice the client work per round and takes ${\sim}2.3\times$
the wall time of $B=10$. Under matched simulated work, $B=5$ leads up to
${\sim}240$\,s, $B=10$ leads near $500$\,s, and $B=20$ only overtakes beyond
${\sim}800$\,s. The default $B=10$ with the $M_c/B$ rule is therefore the
throughput/accuracy operating point we recommend, and $B=20$'s apparent
advantage at a fixed round count is mostly an accounting effect rather than a
per-unit-work advantage. Seed variance also shrinks monotonically with $B$
($\pm3.49/\pm1.00/\pm0.53$).

## Effect of distributions

Yes---and we quantify this rather than leave it qualitative. Let $a_k$ denote
the probability that an arriving update belongs to direction group $k$; under
approximately independent arrivals,

$$
\Pr(\text{group } k \text{ absent from the buffer}) \;\approx\; (1-a_k)^B,
$$

so larger $B$ narrows the coverage gap for every group. The mechanism is
visible in our monitor: raising $B$ from 5 to 20 raises average group coverage
from $0.777$ to $0.999$ and reduces cache-only groups from $4.77$ to $0.54$ of
$7$. However, no value of $B$ corrects a \emph{systematically} wrong arrival
mixture: increasing $B$ reduces the sampling variance of the buffer composition
around the arrival mixture, while the bias between the arrival mixture and the
population mixture persists. Correcting that bias is precisely the role of the
group memory and the refill rule (quantified in our response to Reviewer 3,
Comment 1). The data-distribution dimension is likewise not universal: our
results are specific to this setting, and the revised manuscript reports the
sensitivity study rather than claiming distribution-independent behavior.

## Summary

$B$ should be set as a systems parameter together with the staleness threshold
(our default $B=10$, $M_c=40$ with the $M_c/B$ rule); larger $B$ improves
coverage and stability with a proportional work cost; and the buffer
composition is affected by the distribution and latency process in a way that
$B$ alone cannot remove---which is the problem DirBridge's direction-group
memory is designed to address.
