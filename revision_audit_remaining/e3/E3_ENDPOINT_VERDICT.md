# E3 endpoint verdict

`ENDPOINTS NOT VALID — do not run five-level training`

The earlier host-access block was incorrect: `ssh desktop` succeeded, and the verified runtime was `<REMOTE_PYTHON>` with PyTorch 2.8 / CUDA available. The required external CIFAR-100 and profile paths were also present:

- `<REMOTE_DATA_ROOT>/data/cifar100`
- `<REMOTE_DATA_ROOT>/fedscale_device_info/client_device_capacity`

A bounded production-API attempt was started with the requested CIFAR-100, alpha=0.5, N=100, Mc=40, B=10, ResNet, local batch 100, 10 local steps, and lr=0.01 identity. It imported the production dataset/model/local-update and FedScale sampler APIs and was intended to produce all-100 reference updates plus rho=0/rho=1 scheduler-only replay. It did not complete: `build_dataset` used its hard-coded `./data/cifar100` download/cache location rather than the verified external dataset path, and the remote process entered a slow 169 MB download. The diagnostic was stopped without broad process termination; no endpoint CSVs or reference-update artifact were produced.

Therefore this is no longer a wrong-host verdict, but an execution/integration failure at the production dataset path boundary. No result supports equivalence or separation of rho=0 and rho=1. The five-level rho training matrix remains prohibited until the fixed external CIFAR-100 path is wired through the production API without changing the data, a complete all-100 reference-update computation finishes, and the required endpoint event, decomposition, null, assignment, and identity evidence files are audited.

No code, commit, or push was made. Existing dirty E1 changes were preserved. Partial external state, if any, is under `<REMOTE_STATE_ROOT>/e3_remaining_20260923_1155`; it is not a valid result.
