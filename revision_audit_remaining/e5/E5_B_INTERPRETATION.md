# E5 B work accounting interpretation

This accounting is reconstructed from the existing 65-run E5 manifest; no training was rerun. Every retained B comparison has 500 logged server rounds. Protocol-derived returned updates are therefore `B × 500`: 2,500 for B=5, 5,000 for B=10, and 10,000 for B=20 per seed. Historical logs do not contain a complete accepted-valid-update ledger, so that field is `NA`, not zero. Simulated wall time is reported only where logged.

The B results are consequently fixed-server-round comparisons, not equal-work comparisons. B changes both the number of protocol-returned updates and the finite-buffer aggregation cadence; the B=5/B=20 accuracy and time differences cannot be attributed to buffer size alone under equal local-update work. Fixed-threshold controls isolate the threshold rule only partially: they still do not equalize returned work, accepted updates, or simulated time.
