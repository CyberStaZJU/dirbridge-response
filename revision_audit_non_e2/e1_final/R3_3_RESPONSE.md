# R3-3 response: fair tuning and baseline diagnosis

We agree that the original E1 tuning record should not be presented as a confirmatory fair-tuning study. The historical development jobs used a separate development seed, but selected hyperparameters with tail-10 **test accuracy**. We now label those results exploratory/test-guided rather than validation-selected. The historical search also did not give DirBridge the same fresh search opportunity as the baselines.

We therefore freeze a confirmatory protocol rather than silently relabeling old runs. A deterministic server-side validation subset will be created from training data only, with its indices recorded and the final test set untouched. FedBuff and DirBridge will receive the same 12 local/server learning-rate candidates:

```text
local_lr ∈ {0.003, 0.01, 0.03, 0.05}
server_lr ∈ {0.1, 0.5, 1.0}
```

Configuration selection will use validation accuracy only on development seed(s). The selected configuration will be frozen before five common evaluation seeds are run. The final report will include the complete response surface, paired five-seed differences with 95% paired t intervals, and threshold sensitivity rather than a threshold chosen to favor DirBridge.

`revision_audit_non_e2/e1_final/E1_REQUIRED_RUNS.csv` lists every missing common-grid development run. No large matrix was launched in this task. The current file marks the validation split and confirmatory statistics as not yet available, which is intentional: a test-guided historical result is not converted into a validation result by wording.

The existing CA2FL and FADAS diagnostics remain configuration diagnostics. CA2FL's original server-step setting can produce near-chance behavior, while the exposed server step changes calibration magnitude and observed training behavior. FADAS shows slow movement at very small adaptive steps and instability at larger steps in the recorded search. We do not infer an unmeasured mechanism, delete failed configurations, or claim that these observations prove intrinsic baseline inferiority.

Until the frozen protocol is executed, the defensible E1 conclusion is conditional: the historical gaps are configuration-specific, and no confirmatory universal DirBridge advantage is claimed.
