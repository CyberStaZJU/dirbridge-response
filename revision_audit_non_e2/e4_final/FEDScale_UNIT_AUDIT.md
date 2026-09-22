# E4 FedScale completion-time unit audit

## Provenance

Audit revision: `4ac3e06`. 

The E4 experiment used the archived helper `e4-profile-coupling/code/fedscale_profile_coupling.py`, whose content is byte-identical to the public `utils/fedscale_profile_coupling.py`. The archived helper was used by the E4 desktop code snapshot; the current public integration is `utils/fedscale_trace.py`, which contains the same profile-duration formula and calls the public helper when `--fedscale_profile_coupling label_group` is enabled. The archived desktop code was not a reason to invalidate the runs; its identity is recorded in `e4-profile-coupling/DESIGN_AND_RESULTS.md`.

Tracked implementation identities at this revision:

- `e4-profile-coupling/code/fedscale_profile_coupling.py`: SHA-256 `5839f37a168055d7cfbf27bb51ca6ca099ada7849761670d0c0673ed7efb582f7`
- `utils/fedscale_profile_coupling.py`: same SHA-256
- `utils/fedscale_trace.py`: SHA-256 `66517ddede0a4980868f7409c9b0aa199f220e06c36a98ceabeb53b46608e437`

## Official FedScale call chain

The public FedScale call chain is:

`fedscale/cloud/client_manager.py::ClientManager.get_completion_time`
→ `fedscale/cloud/internal/client_metadata.py::ClientMetadata.get_completion_time`.

`ClientMetadata.__init__` assigns:

```text
compute_speed = speed['computation']
bandwidth = speed['communication']
```

The official completion calculation is:

```text
computation_time = 3.0 * batch_size * local_steps * computation / 1000.0
communication_time = (upload_size + download_size) / communication
completion_time = computation_time + communication_time
```

The implementation and caller use completion time in seconds. `computation` is the device inference latency in milliseconds per sample. `communication` is the numeric bandwidth in megabytes per second for the payload convention used by the simulator. Upload and download sizes are numeric megabytes. The division by 1000 converts milliseconds to seconds.

The official source comments contain some parameter-label wording inconsistencies in the lognormal helper, but the actual caller/callee calculation above is unambiguous and is the convention used for this audit.

## DirBridge implementation

Both the archived E4 helper and current `utils/fedscale_trace.py` use:

```text
3.0 * local_bs * local_period * computation / 1000.0
+ (upload_size + download_size) / communication
```

The E4 defaults are `upload_size=1.0` and `download_size=1.0`. Numerically, each is one unit of the payload size used by the bandwidth field, i.e. one MB under the FedScale profile convention. They are not model-parameter byte counts. Consequently, the E4 communication term is a 2 MB transfer divided by the profile bandwidth.

## Deterministic equivalence test

A synthetic profile with `computation=12.5`, `communication=25.0`, `batch_size=8`, `local_steps=10`, `upload_size=1.0`, and `download_size=2.0` gives:

```text
FedScale computation = 3*8*10*12.5/1000 = 3.000000 s
FedScale communication = (1+2)/25 = 0.120000 s
FedScale total = 3.120000 s
DirBridge total = 3.120000 s
absolute difference = 0.0 s
```

The deterministic unit test is included in `scripts/test_e4_fedscale_units.py` and asserts exact equality within floating-point tolerance. It also asserts that the archived helper and current profile-duration path produce the same value for the same synthetic profile.

## Result

No FedScale/DirBridge completion-time unit mismatch was found. The historical `upload_size=1.0` and `download_size=1.0` convention is numerically compatible with the official calculation. Therefore an old/new timing replay is not required, and no `E4_EVENT_REPLAY.csv` is created.
