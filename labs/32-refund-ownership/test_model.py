import itertools
import unittest
from copy import deepcopy
from model import settle, withdraw
class Tests(unittest.TestCase):
    def state(self): return {"assets": 50, "paid": 0, "refunds": {}}
    def test_whole_balance_negative_control(self):
        s = self.state()
        settle(s, "eve", 10, [(10, True)], vulnerable=True)
        self.assertEqual(withdraw(s, "eve"), 50)
    def test_existing_assets_untouched(self):
        s = self.state()
        settle(s, "alice", 10, [(4, True), (3, False)])
        self.assertEqual(withdraw(s, "alice"), 6)
        self.assertEqual(s["assets"], 50)
    def test_two_payers(self):
        s = self.state()
        settle(s, "alice", 10, [(4, True)])
        settle(s, "bob", 20, [(8, True)])
        self.assertEqual(withdraw(s, "bob"), 12)
        self.assertEqual(withdraw(s, "alice"), 6)
        self.assertEqual(s["assets"], 50)
    def test_withdraw_once(self):
        s = self.state()
        settle(s, "alice", 10, [])
        self.assertEqual(withdraw(s, "alice"), 10)
        self.assertEqual(withdraw(s, "alice"), 0)
    def test_repeated_payer(self):
        s = self.state()
        settle(s, "alice", 5, [])
        settle(s, "alice", 7, [(3, True)])
        self.assertEqual(withdraw(s, "alice"), 9)
    def test_rejection_unchanged(self):
        s = self.state()
        before = deepcopy(s)
        with self.assertRaises(ValueError): settle(s, "alice", 10, [(11, False)])
        self.assertEqual(s, before)
    def test_all_outcome_combinations(self):
        for outcomes in itertools.product([True, False], repeat=3):
            s = self.state()
            settle(s, "a", 12, list(zip([2, 3, 5], outcomes)))
            spent = sum(x for x, ok in zip([2, 3, 5], outcomes) if ok)
            self.assertEqual(withdraw(s, "a") + spent, 12)
            self.assertEqual(s["assets"], 50)
    def test_invalid_inputs(self):
        for payer, incoming, attempts in (("", 1, []), ("a", -1, []), ("a", 1, [(1, 1)])):
            s = self.state()
            with self.assertRaises(ValueError): settle(s, payer, incoming, attempts)
            self.assertEqual(s, self.state())
