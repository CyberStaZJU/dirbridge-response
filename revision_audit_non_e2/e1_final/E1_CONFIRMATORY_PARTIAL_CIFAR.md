# E1 confirmatory evaluation — partial CIFAR-10 result

The frozen validation-selected CIFAR-10 configuration was evaluated for all five seeds for FedBuff and DirBridge. FEMNIST formal evaluation was not completed and is excluded from this partial result.

Configuration for both methods: local learning rate 0.03, server learning rate 0.5, 500 rounds, seeds 1–5.

## Tail-10 test accuracy

| Seed | FedBuff | DirBridge | DirBridge − FedBuff |
|---:|---:|---:|---:|
| 1 | 77.622 | 80.236 | +2.614 |
| 2 | 81.676 | 80.944 | −0.732 |
| 3 | 81.487 | 81.047 | −0.440 |
| 4 | 81.563 | 80.502 | −1.061 |
| 5 | 79.436 | 77.493 | −1.943 |
| **Mean ± SD** | **80.357 ± 1.789** | **80.044 ± 1.464** | **−0.312 ± 1.730** |

Paired 95% t interval for the difference: `[-2.461, +1.836]` percentage points. DirBridge wins 1 seed and loses 4.

## Final-round accuracy

FedBuff: `80.616 ± 1.648%`.

DirBridge: `80.250 ± 1.120%`.

Paired final-round difference: `−0.366` percentage points; 95% paired t interval `[-2.374, +1.642]`.

## Numerical-health boundary

All ten CIFAR accuracy files and system-metrics files contain 500 rows. The final metrics rows report finite evaluation loss and logits for all ten runs. This is the complete CIFAR partial result, not a 20-run E1 conclusion. FEMNIST must not be replaced by its development validation values.
