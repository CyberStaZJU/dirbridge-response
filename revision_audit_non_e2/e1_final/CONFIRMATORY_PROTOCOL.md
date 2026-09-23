# E1 confirmatory protocol

## Selection freeze

Configurations were selected before evaluation from the common 12-point development grid using validation tail-10 accuracy only:

| Dataset | FedBuff | DirBridge |
|---|---|---|
| CIFAR-10 | local LR 0.03, server LR 0.5 | local LR 0.03, server LR 0.5 |
| FEMNIST | local LR 0.05, server LR 1.0 | local LR 0.05, server LR 1.0 |

No evaluation-seed test accuracy is used to change these values.

## Validation/test separation

Validation examples are selected from the training side only. Client training indices exclude held-out validation indices; the final test split remains separate and is not used for configuration selection. The same validation construction and validation seed are used for both methods within each dataset. Development seed is 100. The exact FEMNIST split and client membership manifests are retained in the external run root; the committed `VALIDATION_SPLIT.json` records the construction and audit facts.

## Formal evaluation

The frozen configurations are evaluated for both FedBuff and DirBridge on seeds 1–5 for CIFAR-10 and FEMNIST: 20 runs total. Each run uses the same dataset partition policy, delay setting, model, local work, server-round budget, and evaluation procedure within its dataset. Budget is 500 server rounds. Primary metric is tail-10 test accuracy; final-round test accuracy is secondary. Selection is complete before formal evaluation and no formal result is used for reselection.

## Numerical health

Every formal run retains completion status, per-round accuracy, system metrics, and available finite-loss/logit/prediction diagnostics. Non-finite values are retained and classified; no result is silently replaced or discarded.
