import unittest
from model import Config, MAX
class Tests(unittest.TestCase):
    def setUp(self): self.c = Config({"a": 3, "b": 2}, 4)
    def test_weight_not_count(self):
        self.assertFalse(self.c.approves(["a"]))
        self.assertTrue(self.c.approves(["a", "b"]))
    def test_duplicate_weight(self): self.assertFalse(self.c.approves(["b", "b"]))
    def test_failed_update_preserves_state(self):
        with self.assertRaises(ValueError): self.c.replace({"a": 3}, 4)
        self.assertEqual((self.c.weights, self.c.threshold), ({"a": 3, "b": 2}, 4))
        self.assertTrue(self.c.approves(["a", "b"]))
    def test_negative_control_mutates_before_rejection(self):
        with self.assertRaises(ValueError): self.c.replace({"a": 3}, 4, vulnerable=True)
        self.assertFalse(self.c.approves(["a"]))
        self.assertEqual(self.c.threshold, 4)
    def test_atomic_reduction(self):
        self.c.replace({"a": 3}, 3)
        self.assertTrue(self.c.approves(["a"]))
        self.assertFalse(self.c.approves(["b"]))
    def test_uint64_bounds(self):
        for weights, threshold in (({"a": MAX, "b": 1}, 1), ({"a": 0}, 1), ({"a": 1}, 0), ({"a": True}, 1)):
            with self.assertRaises(ValueError): self.c.replace(weights, threshold)
        self.assertEqual(self.c.weights, {"a": 3, "b": 2})
    def test_exact_maximum(self):
        c = Config({"a": MAX}, MAX)
        self.assertTrue(c.approves(["a"]))
    def test_removal_readdition_no_stale_weight(self):
        self.c.replace({"b": 2}, 2)
        self.c.replace({"a": 1, "b": 2}, 2)
        self.assertFalse(self.c.approves(["a"]))
        self.assertTrue(self.c.approves(["b"]))
