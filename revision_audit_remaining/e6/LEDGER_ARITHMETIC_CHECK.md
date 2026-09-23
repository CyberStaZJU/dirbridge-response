# Ledger arithmetic check

Compared the old ledger to its own published CPU summary at the SAME representative shape: P=10,000, N=100, K0=7, ds=2,048. No small-model values enter this comparison.

| Method | Field | Old ledger sum | Old published | Difference | Assertion |
|---|---|---:|---:|---:|---|
| FedBuff | logical_bytes | 40000 | 40000 | 0 | PASS |
| FedBuff | unique_physical_bytes | 40000 | 40000 | 0 | PASS |
| CA2FL | logical_bytes | 4040000 | 4040000 | 0 | PASS |
| CA2FL | unique_physical_bytes | 4040000 | 4040000 | 0 | PASS |
| DirBridge | logical_bytes | 1247400 | 1126400 | 121000 | FAIL_EXPECTED |
| DirBridge | unique_physical_bytes | 1247400 | 1126400 | 121000 | FAIL_EXPECTED |
| FADAS | logical_bytes | 120000 | 120000 | 0 | PASS |
| FADAS | unique_physical_bytes | 120000 | 120000 | 0 | PASS |

DirBridge: 280,000 group caches + 819,200 features + 57,344 centroids + 800 assignments + 56 counts + 80,000 int64 buckets + 10,000 int8 signs = **1,247,400 bytes**, not 1,126,400. The old same-shape published value understates the CSV by **121,000 bytes**. The script executes and catches this equality assertion failure; all other old methods pass.

The corrected old same-shape sum is recorded above and in OLD_LEDGER_ARITHMETIC.csv. ACTUAL_STATE_SUMMARY.csv separately contains current small production measurements, generated from the new ledger. Each method/device/phase resets storage identity, verifies every alias target, and includes explicit zero method-owned FedBuff rows. FADAS owns exactly 96 tensor bytes in every snapshot. PASS: both CPU/CUDA, init/after5 arithmetic checks.
