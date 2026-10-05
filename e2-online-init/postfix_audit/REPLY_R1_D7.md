# Final reply to Reviewer 1, Comment D7

We thank the reviewer for these questions. They concern (i) how the three
label blocks are formed and attached to clients, (ii) whether the latency
simulation is a realistic stand-in for deployment, and (iii) where our
advantage should be claimed. We answer each in turn.

## (i) How the three blocks are formed

The partition is constructed in three deterministic steps. First, the label
set of the dataset is sorted and split into three contiguous, equal-width
blocks by class index (for CIFAR-100's 100 classes: classes 0--33, 34--66,
67--99); the blocks are defined on the \emph{label space}, before any client
exists. Second, each client's local training set is scored by how many of its
samples fall into each block, and the client is assigned to the block in
which it holds the most samples (dominant block; ties broken toward the lower
block index). This yields a label-heterogeneous partition in which each
client's data is concentrated in one of three direction blocks. Third, the
three blocks are coupled to latency: the delay multiset is drawn from three
uniform ranges---Small $U(1,2)$, Medium $U(3,5)$, Large $U(5,8)$ (in units of
the client-selection period)---with a balanced client count per tier, and a
seed-controlled random permutation maps blocks to tiers, so the coupling is
reproducible but not hand-designed: any block can be fast, medium, or slow
depending on the seed. The full per-client mapping (block, tier, delay) is
computed once at initialization and recorded in the run metadata. The same
three-block construction also supplies the population counts $p_k$ that
DirBridge's weights target.

## (ii) Is the simulation practical?

We are explicit that the three-block/uniform-range construction is a
\emph{controlled} simulation: it lets us vary the direction--latency coupling
while holding the delay multiset fixed, which is the setting in which the
method's mechanism can be isolated. It is a construction, and we do not
present it as a measurement of real end-to-end latency. To address
practicality directly, the revision adds an experiment driven by real
device-capability profiles from the FedScale measurement set (500,000 records
of per-device computation and communication capability): clients are
clustered by their profile features into three classes sorted by a
completion-time proxy, and the label blocks are coupled to these
\emph{measured} profile classes by the same seed-controlled-permutation rule.

On this profile-coupled setting (FEMNIST, 1,000 clients, buffer 100, five
seeds), DirBridge attains a mean tail-10 accuracy of $73.60\pm5.22\%$, the
highest in the seven-algorithm matrix, ahead of FedBuff ($73.28\pm2.18$),
CASA ($71.16\pm3.44$), and FADAS ($68.40\pm1.10$); on Google Speech the
separation is wider, with DirBridge's tail-10 at $53.25\pm9.91\%$ versus the
next best method at $36.60\pm2.11\%$. We report these comparisons with their
seed variance and per-seed outcomes rather than as uniform wins, and we note
where baselines fail to learn under the profile coupling.

## (iii) Where the advantage lies

The mechanism that the three-block construction exposes---and that the
profile-coupled experiment reproduces---is the following: when fast clients
are concentrated in a subset of direction blocks, the first-arriving updates
that fill an asynchronous buffer overrepresent those blocks, so the aggregate
drifts toward a biased direction mixture even though every individual update
is fresh. Methods that act on the age of updates or on which clients
participate leave this \emph{composition} bias in place. DirBridge's
advantage is precisely here: it estimates each direction group's population
mass, compares it with the mass present in the buffer, and supplies the
missing mass from group memories refreshed by any arriving member. The
three-block construction is the instrument that makes this bias large and
controllable; the profile-coupled results show the same mechanism operating
under measured device heterogeneity. We will present the two settings side by
side in the revised manuscript, with the simulation described as a controlled
instrument and the profile-driven experiment as the deployment-oriented
evidence.
