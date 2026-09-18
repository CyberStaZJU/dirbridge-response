# Reply to R3-3 (and the R1-D2 failure-mode discussion): fair tuning and baseline diagnosis

Draft for the response letter. Tone: acknowledge first, report exactly what was
measured, and state every remaining limitation before any claim of advantage.
Numbers come from `e1-fair-tuning/DESIGN_AND_RESULTS.md`.

---

## Response text (R3-3)

> **We agree with the reviewer, and we thank them for pressing on this point.**
> The concern is that the baselines may look weak because they were not tuned
> with the same care as our method. We therefore gave each baseline an
> explicit, equal tuning budget and re-ran the comparison. Two findings are
> unambiguous, one is genuinely inconclusive, and we report all three.
>
> **(a) Equal budget.** Each baseline received 20 pre-registered configurations
> per dataset (120 dev runs in total), selected on a separate development seed
> (seed 100, never used for evaluation), with a common search over local
> learning rate and a method-specific search over the quantities that actually
> govern each method: server step for CA2FL, adaptive step and delay-adaptive
> variant for FADAS. FedBuff received the same budget as a reference, so the
> anomalous baselines are not the only ones that were tuned. Failed and
> diverged trials are reported in full; none were removed. Locked
> configurations were then evaluated at 500 rounds on evaluation seeds 1–5.
>
> **(b) The two anomalies are configuration effects, with identified
> mechanisms.** For CA2FL, the server step was hardcoded to 1.0 in our code
> with no interface to change it — a defect of our harness rather than of
> CA2FL, and one the reviewer's question exposed. With that step the
> cache-correction term reaches 48× the magnitude of the aggregated update, and
> the BatchNorm running variance is driven negative; the model does not
> diverge, it stalls at chance. Setting the server step to 0.5 restores healthy
> behaviour (peak ratio 1.6–9.8, positive BN variance) and CA2FL trains
> normally. For FADAS, the default adaptive step of 1e-4 leaves the model with
> almost no displacement over 500 rounds, while larger steps make the update
> norm grow by 3–10 orders of magnitude because the second-moment accumulator
> cannot track the change — so the original setting is in fact the only stable
> one we found. We report this as "the configuration space does not contain a
> better setting that we could find", not as a claim that none exists.
>
> **(c) After fair tuning, the mean advantage persists but is not statistically
> established.** On CIFAR-10 (α=0.5, DIR-SKEW, M_c=40, B=10), tuned CA2FL
> reaches 49.47 ± 19.73 across seeds 1–5 versus DirBridge 72.14 ± 3.58; the
> original CA2FL configuration gave 10.00 on all five seeds. The paired
> difference (DirBridge − CA2FL) is +22.67 with a 95% confidence interval of
> [−4.43, +49.77] (t = 2.32, df = 4), which **crosses zero**. The interval is
> wide not because the gap is small but because tuned CA2FL is unstable across
> seeds: it reaches 77.45 on one seed and 32.7–37.2 on three others. We
> therefore make **no claim of statistical significance** on this setting, and
> we report the instability itself as a finding: the seed-to-seed spread of
> tuned CA2FL is 5.5× that of DirBridge.
>
> **We also withdraw one earlier observation.** In a shorter development view
> we had the impression that DirBridge escapes the chance-level plateau several
> times faster than the baselines. In the full 500-round runs the escape rounds
> are comparable (CA2FL 12–38, DirBridge 17–33, with CA2FL earlier on two
> seeds), so this is not a valid argument for our method and we do not use it.
>
> **Limitations we state openly.** (i) The formal re-evaluation currently
> covers one method on one setting (CA2FL on CIFAR-10); FEMNIST finals and the
> FedBuff/FADAS finals are not yet complete, so we do not claim that *all*
> baselines remain behind DirBridge after tuning. (ii) Our FedBuff search
> covered local learning rate, batch size and local period only; all 20
> configurations remained at chance level, but a broader search (optimiser,
> momentum, warm-up) might succeed where ours did not. (iii) DirBridge was not
> re-tuned in this experiment and keeps the defaults chosen during the original
> work; this asymmetry favours our method and we flag it rather than hide it.
> (iv) The DirBridge numbers are taken from the original matrix and have not
> yet been re-verified under the current code tree.
>
> **What we would revise in the paper.** The main table will report the tuned
> baselines alongside the original ones, with per-seed differences and
> confidence intervals as the reviewer requests. Where a difference is not
> significant we will say so. The mechanism discussion in Section IV will be
> rephrased so that failure modes are attributed to *what each method changes*
> (averaging, staleness weighting, adaptive scaling, momentum accumulation,
> client-level cache calibration) rather than to the baselines being
> deficient, and we will state explicitly that CA2FL's cache calibration is
> capable in principle of cancelling participation bias when its cache is
> accurate — our observed failure was a step-size configuration, not a refutation
> of that mechanism.

---

## Response text (R1-D2, failure modes)

> We have reframed this discussion by correction target rather than by verdict
> on each baseline. FedBuff averages returned updates and does not restore the
> target population mixture; staleness weighting or filtering does not
> guarantee representation for missing directions (filtering may even reduce
> coverage); FADAS adapts the scale of the server update without constraining
> the group mixture; momentum methods accumulate history that may itself lack
> the missing groups; CA2FL performs client-level cached calibration, and the
> meaningful comparison with DirBridge is cache granularity, refresh quality
> and storage cost rather than whether caching exists.
>
> For CA2FL in particular, writing r_i for the probability that a random buffer
> slot belongs to client i, `E[G_CA] − (1/N)ΣΔ_i = Σ_i (r_i − 1/N)(Δ_i − c_i)`:
> when the cache is accurate, CA2FL can cancel participation bias, and residual
> error survives only when the cache is inaccurate *and* the innovation is
> still sampled with bias. This is a mechanism statement, and we have separated
> it from the accidental finding that our original server step made the
> correction term dominate.
>
> We have also corrected two literature statements: FedStaleWeight is not an
> example of merely down-weighting slow updates (it performs fairness-oriented
> re-weighting to *increase* slow clients' influence), and ClusterFedVARP
> already contains a grouped design that reduces cache cost, so our contribution
> is not "the first group-level cache". We thank the reviewer for both
> corrections.

---

## Notes for whoever finalises this

- Every number above is traceable: dev trials in
  `e1_runs/{cifar,femnist}/commands_dev.sh`, formal runs in
  `e1_runs/cifar/commands_final_ca2fl.sh`, diagnostics in `*-e1_diag.csv`.
- If more seeds are feasible, they are the single highest-value addition: with
  five seeds the CI crosses zero, and a reviewer is entitled to treat the
  advantage as unproven until it does not.
- Do not add escape-time or wall-clock arguments to this response; the first is
  withdrawn and the second is not part of E1.
