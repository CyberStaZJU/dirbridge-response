#!/usr/bin/env python
"""E2 online-initialisation helpers.

Shared helpers for the online (no full-client warm start) DirBridge and CASA
variants, plus the population-weight estimators compared by the E2 control
matrix:

    A  full warm start   + full-client counts
    B  online clustering + oracle population weights
    C  online clustering + arrival-frequency weights
    D  online clustering + unique-observed-client weights

Oracle weights need a direction snapshot of the whole population, which is not
available at deployment time. They are kept as a non-deployable control and as
the measurement reference for the L1 weight error of the online variants.
"""

from __future__ import annotations

from typing import List, Optional, Sequence

import torch

INIT_MODES = ("full", "online")
WEIGHT_SOURCES = ("full_count", "oracle", "arrival_freq", "unique_client")


def _getattr(args, name, default):
    if not hasattr(args, name):
        return default
    value = getattr(args, name)
    return default if value is None else value


def e2_init_mode(args) -> str:
    value = str(_getattr(args, "e2_init_mode", "full")).lower()
    return value if value in INIT_MODES else "full"


def e2_online_init(args) -> bool:
    return e2_init_mode(args) == "online"


def e2_weight_source(args) -> str:
    value = str(_getattr(args, "e2_weight_source", "full_count")).lower()
    return value if value in WEIGHT_SOURCES else "full_count"


def e2_oracle_enabled(args) -> bool:
    """Oracle weights require the population snapshot; the other online
    variants may request it as a measurement reference."""
    return bool(_getattr(args, "e2_oracle_features", False)) or e2_weight_source(args) == "oracle"


def coverage_bound(num_seen: int, num_total: int) -> float:
    """Worst-case L1 gap between the observed-client group frequency and the
    population frequency implied purely by unobserved clients."""
    if num_total <= 0:
        return float("nan")
    seen = max(0, min(int(num_seen), int(num_total)))
    return 2.0 * (1.0 - float(seen) / float(num_total))


def l1_distance(p: Sequence[float], q: Sequence[float]) -> float:
    n = max(len(p), len(q))
    return float(sum(
        abs((float(p[i]) if i < len(p) else 0.0) - (float(q[i]) if i < len(q) else 0.0))
        for i in range(n)
    ))


def normalize_counts(counts: Sequence[float]) -> List[float]:
    values = [max(0.0, float(c)) for c in counts]
    total = float(sum(values))
    if total <= 0.0:
        n = len(values)
        return [1.0 / n] * n if n else []
    return [value / total for value in values]


def group_representatives(
    features: Sequence[Optional[torch.Tensor]],
    group_ids: Sequence[int],
    num_groups: int,
) -> Optional[torch.Tensor]:
    """Mean direction per group over the clients whose direction is known."""
    num_groups = int(num_groups)
    dim = None
    for feature in features:
        if feature is not None:
            dim = int(feature.shape[0])
            break
    if dim is None or num_groups <= 0:
        return None

    sums = torch.zeros((num_groups, dim), dtype=torch.float32)
    counts = torch.zeros(num_groups, dtype=torch.float32)
    for pos, gid in enumerate(group_ids):
        gid = int(gid)
        if not (0 <= gid < num_groups):
            continue
        feature = features[pos]
        if feature is None:
            continue
        sums[gid] += feature.float()
        counts[gid] += 1.0

    for gid in range(num_groups):
        if counts[gid] > 0:
            sums[gid] /= counts[gid]
    norms = torch.norm(sums, dim=1, keepdim=True)
    return sums / torch.clamp(norms, min=1e-12)


def nearest_group(
    features: Sequence[Optional[torch.Tensor]],
    representatives: Optional[torch.Tensor],
) -> List[int]:
    """Nearest-representative assignment used by the oracle weight estimator."""
    if representatives is None or representatives.numel() == 0:
        return [-1] * len(features)
    reps = representatives.float()
    out: List[int] = []
    for feature in features:
        if feature is None:
            out.append(-1)
            continue
        out.append(int(torch.argmax(reps @ feature.float()).item()))
    return out


def oracle_group_weights(
    oracle_features: Sequence[Optional[torch.Tensor]],
    representatives: Optional[torch.Tensor],
    num_groups: int,
) -> Optional[List[float]]:
    """Population group frequencies from a full-population direction snapshot.

    Non-deployable control: it needs the direction of every client, including
    clients whose updates have not arrived.
    """
    if representatives is None:
        return None
    counts = [0.0] * int(num_groups)
    for gid in nearest_group(oracle_features, representatives):
        if 0 <= gid < len(counts):
            counts[gid] += 1.0
    if sum(counts) <= 0.0:
        return None
    return normalize_counts(counts)


def uninitialized_group_mass(
    group_ids: Sequence[int],
    seen_flags: Sequence[bool],
    num_groups: int,
    weights: Optional[Sequence[float]] = None,
) -> float:
    """Population weight held by groups that have no observed client yet."""
    num_groups = int(num_groups)
    counts = [0.0] * num_groups
    for pos, gid in enumerate(group_ids):
        gid = int(gid)
        if 0 <= gid < num_groups and pos < len(seen_flags) and seen_flags[pos]:
            counts[gid] += 1.0

    if weights is None:
        # A group assignment for observed clients is not a population-mass
        # reference. Keep the population quantity undefined until a matching
        # reference snapshot is available.
        return None

    total = float(sum(max(0.0, float(w)) for w in weights[:num_groups]))
    if total <= 0.0:
        return float("nan")
    return float(sum(
        max(0.0, float(weights[gid])) / total
        for gid in range(num_groups)
        if counts[gid] <= 0.0 and gid < len(weights)
    ))


def group_refresh_gap(
    group_members: Sequence[Sequence[int]],
    client_last_arrival: Sequence[int],
    iterations: int,
) -> float:
    """Mean staleness of each non-empty group's freshest observed client.

    Computed from per-client arrival rounds so that it stays well defined when
    group membership is rebuilt.
    """
    gaps = []
    for members in group_members:
        stamps = [
            int(client_last_arrival[idx])
            for idx in members
            if idx < len(client_last_arrival) and int(client_last_arrival[idx]) >= 0
        ]
        if stamps:
            gaps.append(float(int(iterations) - max(stamps)))
    if not gaps:
        return float("nan")
    return float(sum(gaps) / len(gaps))
