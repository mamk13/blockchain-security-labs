import itertools
import unittest
from model import batch
class Tests(unittest.TestCase):
    def test_reused_value_negative_control(self):
        s = {"assets": 0, "credits": 0}
        batch(s, 10, [10, 10], vulnerable=True)
        self.assertEqual(s, {"assets": 10, "credits": 20})
    def test_overallocation_atomic(self):
        s = {"assets": 50, "credits": 20}
        with self.assertRaises(ValueError): batch(s, 10, [7, 4])
        self.assertEqual(s, {"assets": 50, "credits": 20})
    def test_exact_split(self):
        s = {"assets": 0, "credits": 0}
        self.assertEqual(batch(s, 10, [3, 7]), 0)
        self.assertEqual(s, {"assets": 10, "credits": 10})
    def test_donation_not_budget(self):
        s = {"assets": 100, "credits": 0}
        with self.assertRaises(ValueError): batch(s, 1, [2])
        self.assertEqual(s["assets"], 100)
    def test_residual(self):
        s = {"assets": 0, "credits": 0}
        self.assertEqual(batch(s, 10, [3]), 7)
    def test_zero_and_empty(self):
        s = {"assets": 0, "credits": 0}
        self.assertEqual(batch(s, 0, []), 0)
        self.assertEqual(batch(s, 0, [0, 0]), 0)
    def test_bad_inputs(self):
        for incoming, amounts in ((-1, []), (True, []), (1, [-1]), (1, [True])):
            with self.assertRaises(ValueError): batch({"assets": 0, "credits": 0}, incoming, amounts)
    def test_exhaustive_allocations(self):
        for value in range(6):
            for xs in itertools.product(range(6), repeat=3):
                s = {"assets": 9, "credits": 2}
                if sum(xs) <= value:
                    self.assertEqual(batch(s, value, xs), value - sum(xs))
                    self.assertEqual(s["assets"] - s["credits"], 7 + value - sum(xs))
                else:
                    with self.assertRaises(ValueError): batch(s, value, xs)
                    self.assertEqual(s, {"assets": 9, "credits": 2})
