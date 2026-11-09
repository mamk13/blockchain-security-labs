import itertools
import unittest
from model import accepted
class Tests(unittest.TestCase):
    members = {"alice", "bob", "carol"}
    def a(self, who, digest="pay", valid=True): return (who, digest, valid)
    def test_duplicate_negative_control(self):
        xs = [self.a("alice")] * 2
        self.assertTrue(accepted(self.members, 2, xs, "pay", vulnerable=True))
        self.assertFalse(accepted(self.members, 2, xs, "pay"))
    def test_equal_threshold(self):
        self.assertTrue(accepted(self.members, 2, [self.a("alice"), self.a("bob")], "pay"))
    def test_below_threshold(self):
        self.assertFalse(accepted(self.members, 2, [self.a("alice")], "pay"))
    def test_unknown_signer(self):
        self.assertFalse(accepted(self.members, 2, [self.a("alice"), self.a("eve")], "pay"))
    def test_digest_and_validity(self):
        for a in (self.a("bob", "other"), self.a("bob", valid=False)):
            self.assertFalse(accepted(self.members, 2, [self.a("alice"), a], "pay"))
    def test_permutations(self):
        for xs in itertools.permutations(self.members):
            self.assertTrue(accepted(self.members, 2, [self.a(x) for x in xs], "pay"))
    def test_empty_and_bad_threshold(self):
        self.assertFalse(accepted(self.members, 2, [], "pay"))
        for threshold in (0, 4, True):
            with self.assertRaises(ValueError): accepted(self.members, threshold, [], "pay")
    def test_exhaustive_small_domain(self):
        for n in range(5):
            for xs in itertools.product(self.members, repeat=n):
                expected = len(xs) == len(set(xs)) and n >= 2
                self.assertEqual(expected, accepted(self.members, 2, [self.a(x) for x in xs], "pay"))
