# E1 confirmatory development result status

## Execution status

The validation-path development matrix is complete for both principal settings:

- CIFAR-10: 24/24 verified runs, 12 common learning-rate configurations × FedBuff/DirBridge;
- FEMNIST: 24/24 verified runs, 12 common learning-rate configurations × FedBuff/DirBridge.

Every run has 150 metric rows, return code 0, and a populated validation tail-10. The validation subset is derived from training data only; the test set is not used for configuration selection. The exact external run roots and source identity are recorded in the experiment handoff, while compact result tables are committed here.

## Validation-selected configurations

| Setting | FedBuff | DirBridge |
|---|---|---|
| CIFAR-10 | local LR 0.03, server LR 0.5, validation tail-10 63.662 | local LR 0.03, server LR 0.5, validation tail-10 66.002 |
| FEMNIST | local LR 0.05, server LR 1.0, validation tail-10 82.686 | local LR 0.05, server LR 1.0, validation tail-10 82.777 |

The configurations are selected independently by validation tail-10 within the same 12-candidate grid. These are frozen development selections. They are not final test claims because the common five-seed evaluation has not yet been launched.

## Interpretation boundary

The complete response surfaces show that server learning rate materially changes behavior and that several FedBuff settings are near chance, especially CIFAR-10 at server LR 1.0. Low accuracy is retained as an observed configuration outcome; it is not automatically labeled numerical collapse without corresponding health evidence.

At the validation-selection stage, DirBridge is higher by 2.340 points on CIFAR-10 and 0.091 points on FEMNIST. These are single-development-seed validation differences and must not be presented as significance or generalization. Final conclusions require the frozen five-seed evaluation.

Historical E1 test-guided tuning remains exploratory and is not merged with this validation-selected surface.
