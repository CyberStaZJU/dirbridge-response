import csv
import os as _os
import torch as _torch


_E1_FIELDNAMES = [
    "round", "delta_norm", "w_norm", "buffer_mean_delay", "first_nonfinite_round",
    "cache_correction_norm", "agg_norm", "correction_to_agg_ratio",
    "bn_running_var_max", "bn_running_var_min",
    "effective_lr", "vhat_median", "m_norm", "max_delay",
]


def e1_diag_path(system_metrics_path):
    if not system_metrics_path:
        return None
    base = _os.path.basename(system_metrics_path)
    if base.endswith("-system_metrics.csv"):
        base = base[: -len("-system_metrics.csv")] + "-e1_diag.csv"
    else:
        base = base + "-e1_diag.csv"
    return _os.path.join(_os.path.dirname(system_metrics_path), base)


def e1_init_diag_csv(state, args, system_metrics_path):
    path = e1_diag_path(system_metrics_path)
    state["e1_diag_path"] = path
    state["e1_first_nonfinite_round"] = ""
    if path:
        with open(path, "w", newline="") as handle:
            import csv as _csv
            _csv.DictWriter(handle, fieldnames=_E1_FIELDNAMES).writeheader()


def e1_row(state, **values):
    path = state.get("e1_diag_path")
    if not path:
        return
    row = {k: "" for k in _E1_FIELDNAMES}
    row["round"] = state.get("iterations", 0)
    for k, v in values.items():
        if k in row and v is not None:
            row[k] = v
    row["first_nonfinite_round"] = state.get("e1_first_nonfinite_round", "")
    try:
        with open(path, "a", newline="") as handle:
            import csv as _csv
            _csv.DictWriter(handle, fieldnames=_E1_FIELDNAMES).writerow(row)
    except OSError:
        pass


def _sd_norm(sd):
    total = 0.0
    for v in sd.values():
        if _torch.is_tensor(v) and v.is_floating_point():
            total += float(v.detach().float().pow(2).sum())
    return total ** 0.5


def _check_nonfinite(state, w_glob):
    if state.get("e1_first_nonfinite_round"):
        return
    for v in w_glob.values():
        if _torch.is_tensor(v) and not bool(_torch.isfinite(v.detach().float()).all()):
            state["e1_first_nonfinite_round"] = state.get("iterations", 0)
            return


def _bn_var_range(net):
    vmax, vmin = "", ""
    for m in net.modules():
        if isinstance(m, _torch.nn.modules.batchnorm._BatchNorm):
            var = m.running_var.detach().float()
            vmax = float(var.max())
            vmin = float(var.min())
            break
    return vmax, vmin
