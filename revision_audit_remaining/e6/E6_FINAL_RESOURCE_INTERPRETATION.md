# E6 actual-state resource interpretation

## Scope and source

The corrected ledger measures the authoritative Mac production algorithms copied unchanged into `<REMOTE_STATE_ROOT>/e6_ledger_fix_20260923_125333/code`. The desktop is execution-only; results remain in its sibling `results/` directory. This run does not use the older `<REMOTE_CODE_ROOT>` implementation used by the earlier probe. Only local training and delay generation are injected. Production dispatcher initialization, five events, state creation, and aggregation execute unchanged.

The model is `torch.nn.Linear(4,2,bias=False)`: P=8 float32 coordinates, N=6, concurrency=4, B=2, server LR=0.1, K0=2, sketch dimension=8. The local deterministic workload adds a client-specific perturbation; it is not a convergence or realistic local-optimizer memory benchmark. CPU and CUDA each execute four methods and capture initialization plus after five production events: **16 live snapshots**, 296 tensor-reference rows. Environment: Python `<REMOTE_PYTHON>`, Torch 2.8.0+cu128, CUDA 12.8.

## Correct live-snapshot accounting

Storage identity is `(tensor.device, tensor.untyped_storage().data_ptr())` and its map is reset at every method/device/phase. It never spans independent object lifetimes. Storage offsets are reported but are not part of the deduplication key: overlapping or offset views share the underlying storage. Storage bytes are the full untyped storage size, while logical bytes are `numel * element_size`. An executable regression checks an offset-2 view and a fresh independent snapshot. Both CPU and CUDA pass.

The state is held live while traversed, including model parameters, nested dictionaries, lists, tuples, and actual CountSketch plans. Shared storage is attributed first; method-owned references to that same live storage contribute logical bytes but zero additional unique bytes. Aliases are validated against an earlier path within that exact snapshot. FADAS is never deduplicated against an earlier method. The three moments own **96 bytes**, and its complete state owns **352 bytes**, on both devices at both phases.

Shared/common state includes the model, exported global state, client delta slots, and scheduler fields. Method-owned tensors include CA2FL caches/mean, DirBridge features/group caches/plans/diagnostics, and FADAS moments. FedBuff has an explicit **zero method-owned persistent tensor** summary row at every snapshot and a real runtime row; its common live state is not zero. List/tuple shallow Python bytes are separate, exclude referent/scalar/dict sizes, and are not a total or deduplicated Python heap estimate.

## Verified byte totals

CPU and CUDA totals agree. Each method has 256 shared logical/unique tensor bytes. Below, unique method-owned bytes are additional to that shared storage.

| Method | Phase | Method-owned logical | Method-owned unique | Complete logical | Complete unique |
|---|---|---:|---:|---:|---:|
| FedBuff | init / after5 | 0 | 0 | 256 | 256 |
| CA2FL | init | 224 | 224 | 480 | 480 |
| CA2FL | after5 | 224 | 160 | 480 | 416 |
| DirBridge | init | 1,096 | 840 | 1,352 | 1,096 |
| DirBridge | after5 | 1,096 | 1,096 | 1,352 | 1,352 |
| FADAS | init / after5 | 96 | 96 | 352 | 352 |

CA2FL's after5 reduction reflects two real cache/delta aliases, not allocator reuse. DirBridge initialization likewise has real within-snapshot aliases. CountSketch stays on **CPU**, including during the CUDA run: eight `torch.int64` bucket entries (64 bytes) and eight `torch.int8` signs (8 bytes). No plan is fabricated or moved to CUDA for accounting.

## Runtime measurements

`RUNTIME_MEMORY_METRICS.csv` contains current `psutil.Process().memory_info().rss`, CUDA allocated/reserved/max allocated/max reserved, one row for every method/device/phase. CUDA synchronizes before peak reset and before each capture. Initialization peaks are reset before model/state construction; five-event peaks are reset immediately before those events. CPU CUDA fields are blank/not applicable, not a claim that CUDA is unavailable.

| Method | CUDA after5 allocated | CUDA after5 reserved | Five-event max allocated | CUDA-process after5 RSS |
|---|---:|---:|---:|---:|
| FedBuff | 4,096 | 2,097,152 | 6,656 | 708,116,480 |
| CA2FL | 6,656 | 2,097,152 | 10,240 | 708,116,480 |
| DirBridge | 7,168 | 2,097,152 | 11,264 | 714,903,552 |
| FADAS | 5,632 | 2,097,152 | 8,192 | 831,639,552 |

RSS ranged from 520,187,904 to 528,916,480 bytes in the CPU process and 693,485,568 to 831,639,552 in the CUDA process. Allocator rounding, reserved pools, Python/native libraries, and transient work explain why runtime memory is not the tensor-byte sum. Methods execute sequentially in each process; RSS and reserved pools retain prior allocator/library history. Peak reset does not empty the CUDA pool. Transient local models and aggregation intermediates are absent from persistent snapshots; interval allocator peaks include their live allocations but do not separately attribute them by object or method category.

## Arithmetic evidence and limits

`generate_reports.py` revalidates every snapshot alias and sum, asserts FedBuff zero-owned tensor state and FADAS 96 owned bytes, and generates all CSV summaries. It also compares the **old same-shape** ledger with the old published CPU summary: DirBridge sums to **1,247,400**, versus published **1,126,400**, an understatement of **121,000 bytes**. Executed equality assertions fail as expected for both logical and unique fields; other methods pass. The old evidence is left unchanged.

This corrects the resource accounting; it does not upgrade the earlier CA2FL equivalence test. In particular, that earlier test used a different desktop source, omitted a genuine maintained-mean comparison, and must not be treated as qualification of the authoritative incremental implementation. A full production-path independent equivalence qualification remains separate. These small resource measurements are not a training matrix, full-model memory comparison, speedup, convergence result, or universal resource bound. No commits, production changes, or parent status edits were made.
