# E1 FEMNIST development provenance

The 24-job FEMNIST validation development matrix completed with 24/24 verified exit records. Every run returned code 0, produced 150 accuracy rows and 150 system-metrics rows, and passed the external wrapper's validation checks.

- Dataset: existing external FEMNIST `femnist_pt` dataset.
- Historical task contract: 1,000 clients, minimum 250 original training samples, CNN, concurrency 400, buffer 100, local batch 50, 10 local steps, FedScale trace.
- Methods: FedBuff and DirBridge.
- Development seed: 100.
- Candidate grid: local learning rate `{0.003, 0.01, 0.03, 0.05}` × server learning rate `{0.1, 0.5, 1.0}`.
- Selection metric: validation tail-10 accuracy only.
- Validation: 31,624 training examples held out from 316,238 original training examples; 284,614 retained for client training; no train/validation overlap; all clients remained nonempty; test data were not used for selection.
- Execution identity: external snapshot based on commit `4660048` plus explicitly acknowledged uncommitted E1 validation changes in the external identity record.
- External raw source: the run root and its `exits/`, `runs/`, `logs/`, split manifests, `identity.json`, and `source.patch` are retained outside Git.
- No final five-seed evaluation has been launched; these are validation-selected development results.

The six-slot transition preserved the first six jobs and launched each remaining job index once. Its external record is `concurrency_change.json`; no output was overwritten.
