import unittest
from model import forwarded,execute
class Tests(unittest.TestCase):
    def test_negative_control(self):
        self.assertEqual(execute(6400,6400,vulnerable=True),6300)
    def test_correct_rejects(self):
        with self.assertRaises(ValueError): execute(6400,6400)
    def test_exact_minimum(self):
        with self.assertRaises(ValueError): execute(6500,6400)
        self.assertEqual(execute(6501,6400),6400)
    def test_floor_boundaries(self):
        self.assertEqual([forwarded(n,1000) for n in (0,63,64,65)], [0,63,63,64])
    def test_request_below_cap(self):
        self.assertEqual(forwarded(10000,500),500)
    def test_bad_inputs(self):
        for n in (-1,True,1.5):
            with self.assertRaises(ValueError): forwarded(n,1)
            with self.assertRaises(ValueError): forwarded(1,n)
    def test_child_failure_separate(self):
        with self.assertRaises(ValueError): execute(6501,6400,child_ok=False)
    def test_exhaustive_small_allocations(self):
        for a in range(1025):
            for r in (0,1,63,64,100,1000,2000):
                d=forwarded(a,r)
                self.assertTrue(0<=d<=r and d<=a-a//64)
                self.assertEqual(d,min(r,a-a//64))
