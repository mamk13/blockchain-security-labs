import unittest
from model import Batch

class BatchTests(unittest.TestCase):
    def test_negative_control_stalls(self):
        b=Batch(range(100))
        for _ in range(3):
            with self.assertRaises(ValueError): b.all_at_once(10)
        self.assertEqual((b.cursor,b.total),(0,0))

    def test_bounded_progress(self):
        b=Batch(range(100))
        for _ in range(10): b.step(10,10)
        self.assertEqual((b.cursor,b.total),(100,4950))

    def test_budget_caps_requested_limit(self):
        b=Batch([1]*20); b.step(100,3)
        self.assertEqual((b.cursor,b.total),(3,3))

    def test_failure_preserves_checkpoint(self):
        b=Batch([2,3,5]); b.step(1,1)
        with self.assertRaises(ValueError): b.step(2,2,fail_at=2)
        self.assertEqual((b.cursor,b.total),(1,2))
        b.step(2,2)
        self.assertEqual((b.cursor,b.total),(3,10))

    def test_completed_retry_no_duplicate(self):
        b=Batch([7]); b.step(2,2); b.step(2,2)
        self.assertEqual((b.cursor,b.total),(1,7))

    def test_empty(self):
        b=Batch([]); b.step(1,1)
        self.assertEqual((b.cursor,b.total),(0,0))

    def test_invalid_bound_no_change(self):
        for limit,budget in [(0,1),(1,0),(-1,2),(True,1)]:
            b=Batch([1])
            with self.assertRaises(ValueError): b.step(limit,budget)
            self.assertEqual((b.cursor,b.total),(0,0))

    def test_permanent_poison_is_not_fixed(self):
        b=Batch([1,2,3]); b.step(1,1)
        for _ in range(2):
            with self.assertRaises(ValueError): b.step(1,1,fail_at=1)
        self.assertEqual(b.cursor,1)

if __name__ == '__main__': unittest.main()
