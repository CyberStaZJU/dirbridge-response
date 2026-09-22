#!/usr/bin/env python3
"""Re-analyze lightweight E1/E4/E5 records when external state is mounted."""

from __future__ import annotations

import argparse
import csv
import math
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path


def read_accuracy(path: Path) -> list[float]:
    return [float(line) for line in path.read_text().splitlines() if line.strip()]


def mean(values):
    return statistics.mean(values) if values else float("nan")


def sample_sd(values):
    return statistics.stdev(values) if len(values) > 1 else 0.0


def audit_e5(root: Path) -> list[dict]:
    acc_root = root / "e5_runs/cifar100/acc"
    rows = []
    for path in sorted(acc_root.glob("*-test_acc.txt")):
        match = re.search(r"-(e5_[^-]+)-test_acc\.txt$", path.name)
        if not match:
            continue
        values = read_accuracy(path)
        rows.append({
            "file": path.name,
            "config": match.group(1),
            "rows": len(values),
            "finite": all(math.isfinite(value) for value in values),
            "final": values[-1] if values else None,
            "tail10": mean(values[-10:]),
            "tail50": mean(values[-50:]),
        })
    return rows


def audit_e4(root: Path) -> list[dict]:
    rows = []
    for dataset in ("femnist", "gspeech"):
        acc_root = root / f"e4_runs/profile_coupled_valid/fedscale_correct/{dataset}/acc"
        for path in sorted(acc_root.glob("*-test_acc.txt")):
            values = read_accuracy(path)
            rows.append({
                "dataset": dataset,
                "file": path.name,
                "rows": len(values),
                "finite": all(math.isfinite(value) for value in values),
                "final": values[-1] if values else None,
                "tail10": mean(values[-10:]),
            })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    e5 = audit_e5(args.state_root)
    e4 = audit_e4(args.state_root)
    with args.out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["section", "dataset", "file", "config", "rows", "finite", "final", "tail10", "tail50"])
        writer.writeheader()
        for row in e5:
            writer.writerow({"section": "E5", "dataset": "cifar100", **row})
        for row in e4:
            writer.writerow({"section": "E4", "config": "", "tail50": "", **row})
    print(f"records={len(e5) + len(e4)}")
    print(f"e5_unique_configs={len({row['config'] for row in e5})}")
    print(f"e5_complete={sum(row['rows'] == 500 and row['finite'] for row in e5)}/{len(e5)}")
    print(f"e4_complete={sum(row['rows'] == 500 and row['finite'] for row in e4)}/{len(e4)}")


if __name__ == "__main__":
    main()
