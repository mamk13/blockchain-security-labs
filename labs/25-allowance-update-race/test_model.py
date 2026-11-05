import unittest
from model import Allowance
class Tests(unittest.TestCase):
    def test_negative_control(self):
        a=Allowance(); a.spend(100); a.replace(50); a.spend(50)
        self.assertEqual(a.received,150)
    def test_stale_reject_preserves_state(self):
        a=Allowance(); a.spend(100); before=vars(a).copy()
        with self.assertRaises(ValueError): a.replace(50,expected=100)
        self.assertEqual(vars(a),before)
    def test_fresh_replacement(self):
        a=Allowance(); a.replace(50,expected=100); a.spend(50)
        self.assertEqual((a.allowance,a.received),(0,50))
    def test_spend_after_update_rejects_old_limit(self):
        a=Allowance(); a.replace(50,expected=100)
        with self.assertRaises(ValueError): a.spend(100)
        self.assertEqual(a.balance,1000)
    def test_partial_spend_rejects(self):
        a=Allowance(); a.spend(1)
        with self.assertRaises(ValueError): a.replace(50,expected=100)
    def test_revoke_and_retry(self):
        a=Allowance(); a.replace(0,expected=100)
        with self.assertRaises(ValueError): a.spend(1)
        a.replace(50,expected=0); a.spend(50)
        self.assertEqual(a.balance+a.received,1000)
    def test_invalid_amounts(self):
        a=Allowance()
        for n in [-1,True,1.5]:
            with self.assertRaises(ValueError): a.replace(n)
        self.assertEqual(a.allowance,100)
    def test_aba_limitation(self):
        a=Allowance(); a.spend(100); a.replace(100)
        a.replace(50,expected=100); a.spend(50)
        self.assertEqual(a.received,150)
