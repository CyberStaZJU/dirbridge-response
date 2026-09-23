# CA2FL production-path equivalence status

The earlier `test_ca2fl_production_path_equivalence.py` is retained as historical evidence but is **not** used for the corrected resource ledger claim. It executed a different desktop checkout and did not independently compare the maintained CA2FL cache mean after each event; therefore it is inadequate as a current production equivalence qualification.

The corrected resource run uses a new isolated external snapshot of the authoritative Mac code and executes production `dispatcher.init_state` plus five `dispatcher.run_one_round` events for CA2FL, DirBridge, FADAS, and FedBuff. Only deterministic local training and delay generation are injected. Production aggregation and algorithm update code are not replaced. CPU and CUDA both completed all four methods and both initialization/after-five-event captures.

The resource evidence is valid for actual production state creation and runtime accounting. It is not a substitute for a fresh independent full-scan CA2FL equivalence test. Such a test should compare the complete maintained cache mean, calibrated server vector, model, cache, and all event metadata after every production event, including repeated event IDs and post-update replacement arrivals. No claim of that stronger equivalence is made here.
