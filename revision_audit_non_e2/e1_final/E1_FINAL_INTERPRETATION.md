# E1 final interpretation and confirmatory protocol

## Existing E1 evidence

The historical E1 tuning is exploratory, not confirmatory. It used development seed 100 but selected configurations using tail-10 **test accuracy**. A different seed does not turn the test set into a validation set. Historical CIFAR command files contain 20 unique configurations per method; the FEMNIST command file contains 20 submitted entries per method in the intended design, but the broader audit found repeated effective configurations in other command sets. DirBridge retained previous defaults rather than receiving the same fresh search.

The existing formal CA2FL result is useful as a diagnosis of server-step sensitivity, not as a clean claim that a tuned baseline cannot compete. CA2FL with its original server step is a configuration-specific failure; the exposed server step substantially changes the observed behavior. FADAS low-step stalling and larger-step instability are empirical observations; the exact adaptive-state mechanism is not claimed beyond the recorded diagnostics.

## Confirmatory protocol now frozen as a plan

No new formal runs were launched in this task. A server-side validation split must first be constructed deterministically from training data only, with test data untouched and split indices recorded. The split must preserve the original client training task; if client-local splitting would materially alter the task, use a common server-side validation subset and document that choice.

For each principal setting, FedBuff and DirBridge receive the same 12 local/server learning-rate configurations:

```text
local_lr ∈ {0.003, 0.01, 0.03, 0.05}
server_lr ∈ {0.1, 0.5, 1.0}
```

Selection uses validation accuracy only on development seed(s). The selected configuration is then frozen and evaluated on five common seeds at 500 rounds. No evaluation-seed test accuracy is used to reselect a configuration.

CA2FL and FADAS require a separately approved equal-budget method-specific extension if they are included in the confirmatory comparison. They are not silently granted extra trials.

## Required work before formal execution

`E1_REQUIRED_RUNS.csv` enumerates the missing common-grid development runs. The file is a plan only: all rows are `planned_not_launched`. The confirmatory validation split is also not yet created, so no historical result is relabeled as validation-selected.

The complete validation-selected test response surface, paired seed confidence intervals, and threshold sensitivity curve are intentionally marked unavailable until the protocol is executed. This is preferable to presenting test-guided historical tuning as a resolved fair comparison.

## Claim boundary

Current E1 evidence supports: baseline behavior is sensitive to server-step configuration; CA2FL's original near-chance behavior is not evidence of intrinsic incapacity; FADAS shows a measured stability/speed trade-off; and existing DirBridge gaps are conditional on the tested configurations. It does not support a confirmatory claim that DirBridge beats a uniformly and validation-tuned FedBuff.
