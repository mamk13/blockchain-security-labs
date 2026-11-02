import unittest
from model import Bucket, FixedWindow

class RateTests(unittest.TestCase):
    def test_negative_control_double_refill(self):
        b=Bucket(100,10); b.consume(100,0,False)
        b.consume(10,1,False); b.consume(10,1,False)
        self.assertEqual(b.last,0)

    def test_same_timestamp_no_double_refill(self):
        b=Bucket(100,10); b.consume(100,0); b.consume(10,1)
        with self.assertRaises(ValueError): b.consume(1,1)
        self.assertEqual((b.tokens,b.last),(0,1))

    def test_fixed_window_boundary_burst(self):
        f=FixedWindow(100,10); f.consume(100,9); f.consume(100,10)
        b=Bucket(100,10); b.consume(100,9)
        with self.assertRaises(ValueError): b.consume(100,10)

    def test_idle_refill_is_capped(self):
        b=Bucket(100,10); b.consume(100,1000)
        with self.assertRaises(ValueError): b.consume(1,1000)

    def test_failure_does_not_commit_refill(self):
        b=Bucket(100,10); b.consume(100,0)
        with self.assertRaises(ValueError): b.consume(11,1)
        self.assertEqual((b.tokens,b.last),(0,0))
        b.consume(10,1); self.assertEqual((b.tokens,b.last),(0,1))

    def test_backward_time_rejects(self):
        b=Bucket(100,10,5)
        with self.assertRaises(ValueError): b.consume(1,4)
        self.assertEqual((b.tokens,b.last),(100,5))

    def test_zero_rate_is_finite_budget(self):
        b=Bucket(10,0); b.consume(10,0)
        with self.assertRaises(ValueError): b.consume(1,100000)

    def test_zero_consume_commits_time(self):
        b=Bucket(10,1); b.consume(10,0); b.consume(0,5)
        self.assertEqual((b.tokens,b.last),(5,5))

    def test_invalid_amounts(self):
        for a in [-1,True,0.5]:
            b=Bucket(10,1)
            with self.assertRaises(ValueError): b.consume(a,1)
            self.assertEqual((b.tokens,b.last),(10,0))

    def test_envelope_for_all_observed_intervals(self):
        b=Bucket(17,3); history=[]
        for t in range(30):
            for a in [7,3,1]:
                try: b.consume(a,t); history.append((t,a))
                except ValueError: pass
        for start in range(30):
            for end in range(start,30):
                used=sum(a for t,a in history if start<=t<=end)
                self.assertLessEqual(used,17+3*(end-start))
