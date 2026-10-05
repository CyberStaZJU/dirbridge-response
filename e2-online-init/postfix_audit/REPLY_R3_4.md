# Final reply to Reviewer 3, Comment 4

We thank the reviewer for catching this. The reviewer's reading is correct:
the published Table VI could not verify the complexity claims, because it
reported whole-process peaks, and the apparent CA2FL "missing" ${\sim}4.3$ GiB
has a concrete technical explanation. We have redone the measurement as the
reviewer recommends, with two separated tables (algorithm-specific persistent
state, and whole-process/device peaks), and we will replace Table VI in the
revision. We also found and corrected an accounting error in our own method's
favor. Three points explain the inconsistency.

## (1) The ${\sim}4.3$ GiB estimate is real but lives on the compute device

CA2FL's client caches are created with the model's device; in our runs the
model is on the accelerator, so the $N$ model-sized caches occupy device
memory while the Python process RSS (which Table VI reported) stays nearly
flat. Converting the paper's own numbers consistently in MiB ($42.6$\,MiB per
model $\times\,100$ clients $= 4260$\,MiB $\approx 4.16$\,GiB; the draft's
"${\sim}4.3$\,GiB" mixed GiB and parameter-count conventions, which we will
fix), the overhead is where the complexity analysis says it is---in the
device-memory column, not the process column. The new whole-process table
therefore reports CPU process RSS and device allocated/reserved peaks as
separate columns, and we will present both.

## (2) The new algorithm-specific state table measures what each method actually caches

We instrumented the authoritative production implementations and audit every
live tensor by storage identity, so shared storage is attributed once and
aliases are detected rather than double-counted; the audit executes on CPU
and CUDA and is regression-checked against offset-view aliasing. In the audit
configuration, CA2FL's method-owned persistent state is the $N$ per-client
cached updates plus the maintained mean, exactly as the complexity analysis
states; FedBuff owns zero persistent tensors beyond the shared model/buffer
state; FADAS owns its first/second-moment (and max-second-moment) state; and
DirBridge owns its group EMA memories, client sketch features, centroids,
group assignments, and the Count Sketch plan. The table reports
logical-versus-unique bytes so that a cache aliasing a client delta is not
billed twice, a distinction the old table could not make.

## (3) Our own earlier accounting understated DirBridge's sketch plan

The draft described the sketch metadata as $832$\,KiB, but the production
plan stores an explicit bucket coordinate and sign per parameter coordinate,
which at the paper's parameter count is ${\sim}95.9$\,MiB---about $118\times$
the stated figure. The revision fixes the ledger (or, alternatively, we will
regenerate the plan implicitly and re-measure; either way the table will
match the implementation). This correction is in DirBridge's disfavor, and we
report it because the measurement must validate the complexity analysis
rather than flatter our method.

## Revised Table VI

The revised Table VI will contain (i) the per-method persistent-state table
with explicit state inventories, devices, and unique-storage bytes, and (ii)
the whole-process/device peak table as separate columns, with the note that
allocator rounding, reserved pools, and transient aggregation buffers keep
runtime peaks from equaling tensor-byte sums. We will also state explicitly
what each baseline caches, as the reviewer requests.
