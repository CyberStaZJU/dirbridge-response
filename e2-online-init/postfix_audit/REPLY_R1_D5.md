# Final reply to Reviewer 1, Comment D5

We thank the reviewer for asking us to make this definition precise. The
original Section IV.C described the group representative only at a high level;
we will rewrite that passage with the explicit two-level definition below. The
representative of a direction group $k$ is determined at two levels: a
\emph{grouping level}, which decides which clients belong to $k$ and provides
the geometric reference for assigning newly observed updates, and a
\emph{memory level}, which maintains a usable model-space representative of
$k$ even in rounds where no member of $k$ arrives.

## Grouping level

Each client's latest update direction is compressed by a Count Sketch into a
normalized $d_s$-dimensional feature. Clients are clustered by spherical
K-means over these normalized features, and the \emph{representative
direction} of group $k$ is the centroid
$c_k = \bar{v}_k / \lVert \bar{v}_k \rVert$, where $\bar{v}_k$ is the mean of
the normalized member features. Group assignments and centroids are refreshed
every $T_{\mathrm{rc}}$ rounds (interval 5 in our experiments). A newly
observed client is assigned to the group whose centroid has the largest cosine
similarity with its feature; between reclustering passes this
nearest-centroid rule is applied immediately upon arrival, without waiting for
the next global reclustering.

## Memory level

The representative used in aggregation is the group's EMA model memory $m_k$,
maintained in model-parameter space. Whenever members of group $k$ are present
among the valid (staleness-passing) updates in round $t$, the group's base
update is the parameter-space mean of its members' deltas, and the memory is
refreshed as

$$
m_k \leftarrow \beta\, m_k + (1-\beta)\, \bar{\Delta}_k,
\qquad \beta = 0.9,
$$

with the first observation initializing $m_k$ directly. In rounds where group
$k$ has no valid arriving member, the stored $m_k$ serves as the
representative; the stored delay is reset to $0$ at each refresh and the
memory is only consumed for groups whose target population mass exceeds their
current buffer share, so the memory compensates for underrepresented
directions and is not applied indiscriminately.

## Two clarifications we will add

First, the two levels are deliberately different: the centroid $c_k$ lives in
normalized sketch space and is used for \emph{membership and assignment},
while the memory $m_k$ lives in model parameter space and is used for
\emph{aggregation}; the original text did not separate them clearly. Second,
any returning member of group $k$ can refresh $m_k$---the memory is shared at
the group level, so a slow group's representative is refreshed by whichever of
its members arrives, without waiting for a specific client. This is the
property that distinguishes DirBridge's group-level memory from client-level
caches (e.g., CA2FL), where a cache is refreshed only by its own client. When
the grouping itself is refreshed, existing memories are remapped to the new
groups by member overlap so that no memory is lost or silently reassigned.
