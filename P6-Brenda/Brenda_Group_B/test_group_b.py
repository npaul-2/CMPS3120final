"""Group B correctness tests."""
import hashlib
import json
import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'starter'))
from group_b_solutions import solve_merge, solve_counting
from problem import load_instance


class GroupBTests(unittest.TestCase):
    def check(self, delays, expected):
        inst = {'n': len(delays), 'ids': [f'F{i}' for i in range(len(delays))],
                'delay': list(delays)}
        for solver in (solve_merge, solve_counting):
            with self.subTest(algorithm=solver.__name__):
                self.assertEqual(solver(inst), expected)
                self.assertEqual(inst['delay'], delays)
                self.assertEqual(inst['ids'], [f'F{i}' for i in range(len(delays))])

    def test_empty(self):
        self.check([], [])

    def test_single(self):
        self.check([5], ['F0'])

    def test_ties(self):
        self.check([12, -5, 12, 30], ['F3', 'F0', 'F2', 'F1'])
        self.check([12]*5, ['F0', 'F1', 'F2', 'F3', 'F4'])

    def test_boundaries(self):
        self.check([-60, 900, -1, 0, 900, -60],
                   ['F1', 'F4', 'F3', 'F2', 'F0', 'F5'])

    def test_input_orders(self):
        self.check([30, 12, 12, 0, -5], ['F0', 'F1', 'F2', 'F3', 'F4'])
        self.check([-5, 0, 12, 12, 30], ['F4', 'F2', 'F3', 'F1', 'F0'])

    def test_three_seeds(self):
        for seed in (1, 2, 3):
            rng = random.Random(seed)
            delays = [rng.randint(-60, 900) for _ in range(1000)]
            # Reference check only.
            order = sorted(range(len(delays)), key=lambda i: -delays[i])
            self.check(delays, [f'F{i}' for i in order])

    def test_supplied_references(self):
        manifest = json.loads((ROOT / 'data/manifest.json').read_text())
        for dataset in manifest['datasets']:
            inst = load_instance(ROOT / 'data' / dataset['file'])
            for solver in (solve_merge, solve_counting):
                with self.subTest(dataset=dataset['file'], algorithm=solver.__name__):
                    result = solver(inst)
                    digest = hashlib.md5('\n'.join(result).encode()).hexdigest()
                    self.assertEqual(digest, dataset['reference']['md5_of_ids_joined_by_newline'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
