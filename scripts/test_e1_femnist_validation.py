"""Check the actual FEMNIST training holdout without running federation."""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from builders.dataset_builder import build_dataset


def main():
    root, output = sys.argv[1:]
    previous = None
    for method in ('FedBuff', 'DirBridge'):
        args = SimpleNamespace(dataset='femnist', femnist_data_dir=root,
                               num_users=1000, femnist_min_samples_per_client=250,
                               validation_fraction=0.1, validation_seed=20260922,
                               output_dir=output, run_tag=method, random_cost='fedscale_trace')
        train, test, users, counts, meta = build_dataset(args)
        held = set(meta['validation_indices'])
        assigned = [int(i) for indices in users.values() for i in indices]
        assert len(users) == 1000 and min(counts) > 0
        assert min(len(x) for x in train.get_dict_clients().values()) >= 250
        assert len(assigned) == len(set(assigned))
        assert not held.intersection(assigned)
        assert held.union(assigned) == set(range(len(train)))
        assert meta['validation'].dataset is train and train.train and not test.train
        expected = sorted(torch.randperm(len(train), generator=torch.Generator().manual_seed(20260922)).tolist()[:round(len(train) * 0.1)])
        assert meta['validation_indices'] == expected
        for index in (0, len(held) // 2, len(held) - 1):
            first, target = meta['validation'][index]
            second, second_target = meta['validation'][index]
            assert torch.equal(first, second) and target == second_target
            assert first.shape == (1, 28, 28) and 0 <= target < 62
        manifest = json.loads((Path(output) / f'{method}_validation_split.json').read_text())
        if previous is not None:
            assert manifest == previous
        previous = manifest
        print(json.dumps({'method': method, 'train_source': len(train), 'train_retained': len(assigned),
                          'validation': len(held), 'test': len(test), 'clients': len(users),
                          'minimum_retained': int(min(counts)), 'status': 'PASS'}))


if __name__ == '__main__':
    main()
