# Final reply to Reviewer 2, Comment 5

We thank the reviewer for this suggestion. We ran a controlled sensitivity
study covering both quantities ($K_0 \in \{1,2,4,7,12,16\}$ and
$d_s \in \{128,512,2048,8192\}$ on CIFAR-100 with $\alpha=0.5$, five seeds per
configuration, 500 rounds, all other factors at the paper's default operating
point; 65 runs in total). We will add the full sweep to the revised
manuscript. The two parameters behave very differently, and we summarize each
in turn.

## The number of direction groups $K_0$: a structured, mechanism-bearing effect

Final accuracy is $19.14\pm7.15$, $43.83\pm1.40$, $46.25\pm1.56$,
$47.11\pm1.00$, $49.51\pm0.69$, and $49.03\pm0.73$ for
$K_0 = 1,2,4,7,12,16$. A single group ($K_0=1$) removes the direction
partition and hence the group memory that compensates underrepresented
directions; the collapse to $19.14\%$ with seed spread $\pm7.15$ reflects
this structural loss. Accuracy then rises steeply to the default and
flattens: the closed-form default $K_0=\lceil\log_2 C\rceil=7$ sits at the
foot of a plateau, with $K_0=12$ and $16$ adding $1$--$2.4$ points, a range
comparable to the per-seed reproducibility band. We therefore do not claim
the default is empirically optimal; we claim it is a robust, tuning-free
choice near the plateau.

The cost side is explicit: device peak memory grows monotonically with $K_0$
($5314\rightarrow7302$\,MiB for $K_0=1\rightarrow16$) because each group owns
a model-sized memory, while the recorded reclustering cost stays below
$0.4\%$ of training time. Setting $K_0$ therefore trades representation
resolution against linear memory growth, and the default rule makes the
trade-off without per-dataset tuning.

## The sketch dimension $d_s$: a flat, non-sensitive knob

Grouping quality is essentially unchanged across a $64\times$ compression
range: the intra-group mean cosine similarity is
$0.201/0.184/0.184/0.182$ for $d_s=128/512/2048/8192$, reclustering stability
is $0.791/0.781/0.778/0.778$, the buffer mixture-mismatch statistic $\Phi_t$
stays within $0.064$--$0.070$, and coverage within $0.950$--$0.958$; every
diagnostic moves by less than its own seed-level spread.

Final accuracy is $47.51\pm1.71$, $46.50\pm2.52$, $47.11\pm1.12$, and
$48.12\pm0.58$; the tail-10 paired differences against the default
$d_s=2048$ are $-0.43$ with $95\%$ CI $[-2.71,+1.85]$, $-0.81$ with
$[-1.59,-0.04]$, and $-0.17$ with $[-0.86,+0.53]$ for $d_s=128/512/8192$.
Only the $d_s=512$ interval excludes zero, and its $0.8$-point magnitude sits
at the edge of the reproducibility band; with no multiplicity correction
across the three comparisons, we read the sweep as flat.

Two details are worth recording. First, $d_s=128$ attains the highest
intra-group similarity but the lowest inter-group separation ($-0.000$ versus
$0.022$ at $d_s=2048$): aggressive compression pulls all directions toward a
common one, so intra-group similarity alone is a misleading quality signal;
the intra-minus-inter gap ($0.201/0.170/0.162/0.164$) is the meaningful
quantity and is not monotone in $d_s$. Second, the tightest seed spread occurs
at $d_s=8192$ ($\pm0.58$), consistent with reduced sketch noise, but the gain
lies inside the reproducibility band. We therefore keep $d_s=2048$ as a
robust default.

## Summary

$K_0$ is a structured hyperparameter whose default $\lceil\log_2 C\rceil$
sits at the foot of an accuracy plateau at linear memory cost, while $d_s$ is
a flat hyperparameter whose default lies inside a seed-noise-wide flat region
at negligible cost. The revised manuscript will report both sweeps with their
paired intervals and this reading of which knob is sensitive and which is
not.
