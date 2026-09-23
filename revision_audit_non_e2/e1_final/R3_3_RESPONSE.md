# R3-3 response: validation-selected E1 development phase

We completed the common validation-based development phase for the two principal datasets rather than relabeling the historical test-guided search.

The matrix contains 12 identical local/server learning-rate candidates for FedBuff and DirBridge: local LR `{0.003, 0.01, 0.03, 0.05}` crossed with server LR `{0.1, 0.5, 1.0}`. Each method-setting pair used one development seed and 150 rounds. Configuration selection used tail-10 accuracy on a deterministic server-side subset drawn from training data only; the final test set was not used for selection.

All 24 CIFAR-10 and all 24 FEMNIST development jobs passed the 150-row and validation-metric checks. The validation-selected configurations are:

- CIFAR-10: FedBuff `(0.03, 0.5)` at 63.662%; DirBridge `(0.03, 0.5)` at 66.002%.
- FEMNIST: FedBuff `(0.05, 1.0)` at 82.686%; DirBridge `(0.05, 1.0)` at 82.777%.

These are validation observations from one development seed, not five-seed final test results. The apparent gaps are therefore descriptive and do not establish a statistically significant DirBridge advantage. The frozen configurations must now be evaluated on five common seeds without re-selection.

The response surface also confirms that server-step choice is consequential. Several FedBuff settings reach near-chance accuracy, while neighboring settings learn well; those outcomes are retained as configuration results and are not used to claim intrinsic baseline incapacity. The historical test-guided E1 search remains exploratory and is reported separately.
