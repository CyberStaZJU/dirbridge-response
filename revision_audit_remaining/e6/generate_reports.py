"""Verify snapshot storage arithmetic and regenerate current summaries."""
import argparse
import csv
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[1]
METHODS = ('FedBuff', 'CA2FL', 'DirBridge', 'FADAS')


def read(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def write(path, rows):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', type=Path, required=True)
    a = p.parse_args()
    rows = sum((read(a.input / f'ledger_{d}.csv') for d in ('cpu', 'cuda')), [])
    runtime = sum((read(a.input / f'runtime_{d}.csv') for d in ('cpu', 'cuda')), [])
    summaries = []
    for device in ('cpu', 'cuda'):
        for method in METHODS:
            for phase in ('init', 'after5'):
                rr = [r for r in rows if (r['run_device'], r['method'], r['phase']) == (device, method, phase)]
                seen = {}
                for r in rr:
                    if r['kind'] != 'tensor':
                        continue
                    key = r['device'], r['storage_ptr']
                    expected = 0 if key in seen else int(r['storage_bytes'])
                    assert int(r['unique_physical_bytes']) == expected, r
                    assert r['alias_of'] == seen.get(key, ''), r
                    seen.setdefault(key, r['path'])
                for owner in ('shared', 'method_owned'):
                    owned = [r for r in rr if r['ownership'] == owner]
                    tensors = [r for r in owned if r['kind'] == 'tensor']
                    summaries.append(dict(method=method, run_device=device, phase=phase,
                        ownership=owner, tensor_rows=len(tensors),
                        logical_bytes=sum(int(r['logical_bytes']) for r in tensors),
                        unique_physical_bytes=sum(int(r['unique_physical_bytes']) for r in tensors),
                        python_list_tuple_shallow_bytes=sum(int(r['python_shallow_bytes']) for r in owned)))
                if method == 'FedBuff':
                    assert summaries[-1]['logical_bytes'] == summaries[-1]['unique_physical_bytes'] == 0
                if method == 'FADAS':
                    assert summaries[-1]['logical_bytes'] == summaries[-1]['unique_physical_bytes'] == 96
    write(D / 'ACTUAL_STATE_LEDGER.csv', rows)
    write(D / 'ACTUAL_STATE_SUMMARY.csv', summaries)
    write(D / 'RUNTIME_MEMORY_METRICS.csv', runtime)
    old_dir = ROOT / 'revision_audit_non_e2/e6_final'
    old = read(old_dir / 'PERSISTENT_STATE_LEDGER.csv')
    published = read(old_dir / 'MEMORY_RUNTIME_METRICS.csv')
    checks = []
    for method in METHODS:
        rr = [r for r in old if r['method'] == method]
        pub = next(r for r in published if r['method'] == method and r['device'] == 'cpu')
        for field, published_field in [('logical_bytes', 'logical_persistent_tensor_bytes'),
                                       ('unique_physical_bytes', 'unique_physical_persistent_tensor_bytes')]:
            actual = sum(int(r[field]) for r in rr)
            claimed = int(pub[published_field])
            try:
                assert actual == claimed, f'{method}: {actual} != {claimed}'
                result = 'PASS'
            except AssertionError:
                result = 'FAIL_EXPECTED'
            checks.append(dict(method=method, field=field, ledger_sum=actual,
                               published=claimed, difference=actual-claimed, result=result))
    assert [r['method'] for r in checks if r['result'] == 'FAIL_EXPECTED'] == ['DirBridge', 'DirBridge']
    write(D / 'OLD_LEDGER_ARITHMETIC.csv', checks)
    text = '# Ledger arithmetic check\n\n'
    text += 'Compared the old ledger to its own published CPU summary at the SAME representative shape: P=10,000, N=100, K0=7, ds=2,048. No small-model values enter this comparison.\n\n'
    text += '| Method | Field | Old ledger sum | Old published | Difference | Assertion |\n|---|---|---:|---:|---:|---|\n'
    for r in checks:
        text += f"| {r['method']} | {r['field']} | {r['ledger_sum']} | {r['published']} | {r['difference']} | {r['result']} |\n"
    text += '\nDirBridge: 280,000 group caches + 819,200 features + 57,344 centroids + 800 assignments + 56 counts + 80,000 int64 buckets + 10,000 int8 signs = **1,247,400 bytes**, not 1,126,400. The old same-shape published value understates the CSV by **121,000 bytes**. The script executes and catches this equality assertion failure; all other old methods pass.\n\n'
    text += 'The corrected old same-shape sum is recorded above and in OLD_LEDGER_ARITHMETIC.csv. ACTUAL_STATE_SUMMARY.csv separately contains current small production measurements, generated from the new ledger. Each method/device/phase resets storage identity, verifies every alias target, and includes explicit zero method-owned FedBuff rows. FADAS owns exactly 96 tensor bytes in every snapshot. PASS: both CPU/CUDA, init/after5 arithmetic checks.\n'
    (D / 'LEDGER_ARITHMETIC_CHECK.md').write_text(text)
    print('PASS: 16 live snapshots; FedBuff zero-owned; FADAS 96 owned bytes; old DirBridge mismatch caught twice')


if __name__ == '__main__':
    main()
