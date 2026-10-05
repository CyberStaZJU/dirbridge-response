# Final reply to Reviewer 2, Comment 2

We thank the reviewer for the careful reading. We audited the full manuscript
against this comment, and the reviewer's examples are confirmed with one
precision: within the manuscript the group count is written $K$ throughout,
and the variant $K_0$ appears in our supplementary experimental material; the
$d$/$d_s$ split, however, is real inside the manuscript itself. The audit
found the following concrete instances, all of which will be fixed in the
revision.

## (1) Symbols used before definition

Definition 1 (Direction Skew) uses $\mathcal{G}_k$ and $K$ in its equation,
while the groups are formally introduced only afterwards ("Let
$\mathcal{G}_1,\ldots,\mathcal{G}_K$ denote the direction groups"). We will
move this introduction before Definition 1 and apply the same
define-before-use check to every symbol in the formal sections.

## (2) Two symbols for the sketch dimension

The main text and the Algorithm 1 header use $d$ for the sketch dimension; the
complexity section declares $d$ in its inline symbol list; the
asymptotic-overhead section re-declares the same quantity as $d_s$; and the
reproducibility configuration table reverts to $d=2048$. The root cause is
that the manuscript carries two local glossaries that were never reconciled.
We will use $d_s$ everywhere, reserving $d$ for quantities where the
manuscript needs a generic dimension, and replace both inline glossaries with
pointers to the single notation table proposed in our response to Comment 1.

## (3) One symbol per concept, one glossary

The number of groups will be $K_0$ in the revised manuscript and in all
supplementary material. Beyond consistency with our experimental records, this
removes two overloads of the bare $K$: "spherical $K$-means", where $K$ is the
clustering algorithm's own parameter, and the baselines' cluster count
$K_{\mathrm{cl}}$. The reclustering interval keeps the manuscript's existing
$R$, the valid-buffer size keeps $b_t$, and the group, aggregate-direction,
and norm-bound symbols ($\mathcal{G}_k$, $G_t$, $G$) will be checked for
overloading in the same pass.

## (4) Harmonizing our own response material

Our experimental responses introduced $r_k$ for the arrival probability and
$\lambda_k$ for the group-dependent arrival rate, which clash with the
manuscript's $r_k(t)$ (refresh count) and $\lambda_{t,k}$ (blending
coefficient). In the revision these response-side quantities will be renamed
($a_k$ for the arrival probability, $\nu_k$ for the arrival rate), the
affected response text will be updated to match, and every response-introduced
symbol will be added to the notation table with its first-use location so that
the manuscript and the table remain the single reference.
