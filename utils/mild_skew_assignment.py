"""Opt-in client-to-delay assignment for the original mild hierarchical bank."""
from __future__ import annotations

import numpy as np


def assign_delay_bank(bank, mode="original", seed=0, direction_scores=None):
    """Return a permutation of an existing bank; never resamples or changes values."""
    values = np.asarray(bank, dtype=float)
    if values.ndim != 1:
        raise ValueError("delay bank must be one-dimensional")
    n = values.size
    if mode == "original":
        order = np.arange(n, dtype=np.int64)
    elif mode == "random":
        order = np.random.default_rng(int(seed)).permutation(n)
    elif mode == "sorted":
        if direction_scores is None:
            raise ValueError("sorted assignment requires fixed reference direction scores")
        scores = np.asarray(direction_scores, dtype=float)
        if scores.shape != (n,):
            raise ValueError("direction scores must match delay bank")
        order = np.argsort(scores, kind="stable")
    else:
        raise ValueError(f"unsupported assignment mode: {mode}")
    assigned = values[order]
    if not np.array_equal(np.sort(assigned), np.sort(values)):
        raise AssertionError("assignment changed the delay multiset")
    return assigned, order


def assert_assignment_invariants(original, assigned, order, expected_size=None):
    original = np.asarray(original)
    assigned = np.asarray(assigned)
    order = np.asarray(order)
    if expected_size is not None and len(original) != int(expected_size):
        raise AssertionError("unexpected bank size")
    if assigned.shape != original.shape or order.shape != original.shape:
        raise AssertionError("assignment shape mismatch")
    if not np.array_equal(np.sort(original), np.sort(assigned)):
        raise AssertionError("delay multiset mismatch")
    if not np.array_equal(assigned, original[order]):
        raise AssertionError("assignment/order mismatch")
    if len(np.unique(order)) != len(order):
        raise AssertionError("assignment is not a permutation")
