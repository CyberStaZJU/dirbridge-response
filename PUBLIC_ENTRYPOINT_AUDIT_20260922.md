# Public Entry-Point Argument Audit (2026-09-22)

This audit verifies the five arguments that appeared in supplemental experiment commands. The port is now present in the public checkout rather than only in a desktop snapshot.

| Argument/profile | Parser | Execution path | Verification |
|---|---|---|---|
| `mild_label_correlated_hierarchical` | Accepted by `utils/options.py` | `builders/dataset_builder.py` attaches label-derived groups; `algorithm/dispatcher.py` maps them to Small/Medium/Large delay ranges; `utils/aggregation.py` samples the selected profile | Passed profile-construction check in `scripts/test_flag_wiring.py` |
| `--e2_init_mode` | Accepted with `full`/`online` choices | `algorithm/dirbridge.py` selects full warm-start or first-wave online dispatch; online results remain in `state['inflight']` until arrival | Parser and in-flight materialization checks passed |
| `--e2_weight_source` | Accepted with `full_count`, `oracle`, `arrival_freq`, and `unique_client` choices | DirBridge resolves the selected source in `_update_e2_group_weights`; online `full_count` is rejected because it requires unseen-client directions | Parser and helper-path checks passed |
| `--fedscale_profile_coupling` | Accepted with `label_group` choice | Dataset construction attaches label groups; `FedScaleTraceSampler` builds and records the label-group/profile mapping | Coupling sampler check passed with a temporary profile payload |
| `--dirbridge_buffer_delay_limit` | Accepted as an optional float | DirBridge `_buffer_delay_limit` uses the override and otherwise retains `concurrency / buffer_size` | Override check passed |

## Verification boundary

The following checks were completed:

1. Local Python syntax compilation for all modified runtime files.
2. `scripts/test_flag_wiring.py` in the desktop reference environment, returning `public_flag_wiring=PASS`.
3. The test covered parser acceptance, mild profile construction, E2 mode/weight selection, in-flight arrival materialization, delay-limit override, and FedScale label-group coupling.

The public repository has not been claimed to reproduce a full CIFAR training run from this Mac environment because PyTorch and the raw datasets are not installed locally. The exact repaired desktop online five-seed run and the same-code full-warm five-seed control both completed externally; their accuracy summaries and the shared NaN-loss diagnostic are recorded in `SUPPLEMENTAL_RESULTS_20260921.md`.
