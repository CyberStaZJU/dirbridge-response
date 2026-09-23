"""Build the deterministic server-side CIFAR training validation manifest."""
import hashlib
import json
from pathlib import Path
import numpy as np


def main():
    count = 5000
    seed = 20260922
    rng = np.random.default_rng(seed)
    indices = sorted(rng.choice(50000, size=count, replace=False).tolist())
    payload = {
        'dataset': 'CIFAR-10 train split',
        'source_size': 50000,
        'validation_size': count,
        'fraction': count / 50000,
        'construction': 'server-side deterministic subset of training indices; client partitions unchanged; test set untouched',
        'seed': seed,
        'indices': indices,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()
    payload['manifest_sha256'] = hashlib.sha256(encoded).hexdigest()
    out = Path('revision_audit_non_e2/e1_final/VALIDATION_SPLIT.json')
    out.write_text(json.dumps(payload, indent=2) + '\n')
    print(out, payload['manifest_sha256'], len(indices))


if __name__ == '__main__':
    main()
