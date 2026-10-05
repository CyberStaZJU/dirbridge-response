# Final reply to Reviewer 1, Comment D6

We thank the reviewer for these questions. The number of direction groups
$K_0$ determines both the granularity of the direction partition and the
number of group-level memories, so it trades off representation resolution
against per-group refresh frequency and memory cost. We answer the three
questions in turn; the answers rest on a controlled sensitivity sweep
($K_0 \in \{1,2,4,7,12,16\}$ on CIFAR-100 with $\alpha=0.5$, five seeds per
configuration, 500 rounds, all other factors at the paper's default operating
point), which we will add to the revised manuscript.

## What is the number of groups?

$K_0$ is a method hyperparameter, fixed before training. Our default is the
closed-form rule

$$
K_0 = \lceil \log_2 C \rceil,
$$

where $C$ is the number of classes: $K_0=4$ for CIFAR-10, $7$ for CIFAR-100,
$6$ for FEMNIST and Google Speech, and $8$ for TinyImageNet. This rule is
applied uniformly across all datasets with no per-dataset tuning. Note the
distinction between the requested number of groups and the number of
\emph{populated} groups at any round: with online initialization, only groups
containing at least one observed client are populated, and the count of
non-empty groups grows as the observed client set grows.

## How to set it?

The closed-form default is the recommended setting procedure: it requires only
the class count, needs no validation run, and places $K_0$ in the same order
as the effective heterogeneity granularity of our label-skewed partitions. If
deployment allows a small validation budget, $K_0$ can be swept exactly as we
did here; the sweep below shows the default sits in a flat, well-behaved
region rather than a fragile one.

## Does $K_0$ affect performance?

Yes, with a clear structure. Final accuracy on CIFAR-100 ($\alpha=0.5$, five
seeds) is $19.14\pm7.15$, $43.83\pm1.40$, $46.25\pm1.56$, $47.11\pm1.00$,
$49.51\pm0.69$, and $49.03\pm0.73$ for $K_0 = 1, 2, 4, 7, 12, 16$,
respectively. Three observations follow.

First, a single group ($K_0=1$) collapses the method's core mechanism---there
is no direction partition and hence no group memory to compensate
underrepresented directions---and the large accuracy drop and the large seed
variance both reflect this.

Second, accuracy rises steeply from $K_0=1$ to the default and then flattens:
the default $K_0=7$ sits at the foot of a plateau, with $K_0=12$ and $16$
adding $1$--$2.4$ points, a range comparable to our per-seed reproducibility
band. We therefore do not claim that the closed-form default is empirically
optimal; we claim it is a robust, tuning-free choice near the plateau.

Third, the cost of larger $K_0$ is real but bounded: the group memories live
in accelerator memory, whose peak grows monotonically with $K_0$
($5314 \rightarrow 7302$ MiB for $K_0 = 1 \rightarrow 16$ in our measurement),
while the recorded reclustering cost stays below $0.4\%$ of training time
($0.63$--$5.60$\,s over 500 rounds). This yields an explicit accuracy--memory
trade-off: increasing $K_0$ refines direction resolution and can improve
accuracy modestly, at linear growth in the number of group memories.

## Summary

$K_0$ is set by $K_0=\lceil \log_2 C \rceil$ with no per-dataset tuning; it
does affect performance, primarily through the presence or absence of the
direction-partition mechanism at small $K_0$ and through a flat plateau near
the default at larger $K_0$; and its memory cost grows linearly with $K_0$
while its compute cost is negligible. The revised manuscript will report the
full sweep and this trade-off explicitly.
