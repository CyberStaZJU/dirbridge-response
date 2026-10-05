# Final reply to Reviewer 2, Comment 1

We agree that the manuscript used a growing set of symbols without a central
reference, which hurts readability---particularly because several symbols
($G_k$, $K_0$) were used before being defined, and two pairs of similar
symbols ($d$/$d_s$, $K$/$K_0$) could be confused. We will add a notation table
at the start of Section III (or as an appendix table, whichever the page
budget prefers) and unify the symbols throughout. The planned table is below;
each entry states where the symbol is first used.

## Table: Main symbols and their definitions

| Symbol | Meaning (first use) |
|---|---|
| $N$ | Total number of clients. |
| $C$ | Number of classes. |
| $M_c$ | Client concurrency: the number of clients training in parallel. (Sec. IV-A) |
| $B$ | Buffer size: the number of updates aggregated per server step. (Sec. IV-A) |
| $K_0$ | Number of direction groups, set to $\lceil \log_2 C \rceil$; replaces the draft's bare $K$ wherever the group count is meant. (Sec. III, Def. 1) |
| $d_s$ | Count Sketch dimension; the draft's bare $d$ is reserved for the model parameter dimension. (Sec. IV-B) |
| $G_k$ | Direction group $k$; defined at first use in Definition 1 before any later reference. (Sec. III) |
| $p_k$ | Population mass of direction group $k$ over all $N$ clients. (Sec. III) |
| $\widehat{p}_k$ | DirBridge's online estimate of $p_k$ (unique-client estimator by default). (Sec. IV-C) |
| $\lambda_k$ | Group-dependent arrival rate; $r_k \propto p_k \lambda_k$ characterizes the latency bias of the arrival mixture. (Sec. V, analysis) |
| $r_k$ | Probability that a newly arriving update belongs to group $k$. (Sec. V, analysis) |
| $c_k$ | Centroid of group $k$ in normalized sketch space, $c_k = \bar{v}_k / \lVert \bar{v}_k \rVert$; used for membership and assignment. (Sec. IV-C) |
| $m_k$ | Model-space EMA memory of group $k$, the representative used in aggregation; refreshed by any arriving member. (Sec. IV-C) |
| $\bar{\Delta}_k$ | Parameter-space mean of the valid deltas from group $k$ in the current buffer. (Sec. IV-C) |
| $\beta$ | EMA coefficient of the group memory ($\beta = 0.9$). (Sec. IV-C) |
| $\Phi_t$ | Buffer mixture-mismatch statistic at round $t$; reported with its finite-buffer sampling null. (Sec. V) |
| $N_{\mathrm{seen}}$ | Number of distinct clients observed so far; yields the coverage bound $\lVert \widehat{p}-p \rVert_1 \leq 2(1 - N_{\mathrm{seen}}/N)$. (Sec. IV-C) |
| $T_{\mathrm{rc}}$ | Reclustering interval in rounds (interval 5 in our experiments). (Sec. IV-C) |

Beyond the table itself, we will make three consistency edits in the revision.
First, $K_0$ will be used for the number of groups everywhere, and the bare
$K$ will no longer appear with that meaning. Second, $d_s$ will denote the
sketch dimension everywhere, reserving $d$ for the model parameter dimension.
Third, $G_k$ and $K_0$ will be defined at their first occurrence
(Definition 1) rather than used before definition; the notation table does not
remove the obligation to define symbols at first use, and we will fix the
ordering as well.
