# GSpeech NaN diagnosis

Raw scheduler logs establish an evaluation-loss failure, typically beginning at round 2 or 3, with affected runs continuing through parts or all of the 500-round tail. Accuracy files remain finite. The logs contain no logits, parameter snapshots, BatchNorm buffers, optimizer state, or checkpoint at the first non-finite event. Consequently the cause cannot be classified as data, logits, model state, or evaluation-only failure from existing evidence. No large rerun was launched; a bounded diagnostic would not retroactively identify the historical state.
