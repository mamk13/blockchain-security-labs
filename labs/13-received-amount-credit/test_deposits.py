import unittest
from deposits import Token, Vault

class DepositTests(unittest.TestCase):
    def test_fee_negative_control(self):
        bad,good = Vault(Token(100),False),Vault(Token(100))
        self.assertEqual(bad.deposit('alice',100),100)
        self.assertEqual(good.deposit('alice',100),99)
        self.assertGreater(sum(bad.credits.values()),bad.token.balances['vault'])
        self.assertEqual(sum(good.credits.values()),good.token.balances['vault'])

    def test_zero_fee(self):
        v = Vault(Token()); self.assertEqual(v.deposit('alice',100,100),100)

    def test_minimum_reverts_every_ledger(self):
        v = Vault(Token(100)); before = v.token.balances.copy()
        with self.assertRaises(ValueError): v.deposit('alice',100,100)
        self.assertEqual(v.token.balances,before); self.assertFalse(v.credits)

    def test_false_return(self):
        v = Vault(Token(succeeds=False))
        with self.assertRaises(ValueError): v.deposit('alice',100)
        self.assertEqual(v.token.balances['alice'],1000)

    def test_donation_is_not_depositor_credit(self):
        t = Token(100); t.balances['vault']=50; v=Vault(t)
        self.assertEqual(v.deposit('alice',100),99)
        self.assertEqual(t.balances['vault'],149)

    def test_full_fee_rejected(self):
        v=Vault(Token(10000))
        with self.assertRaises(ValueError): v.deposit('alice',100)
        self.assertEqual(v.token.balances['fees'],0)

    def test_rounding_and_conservation(self):
        for fee in (0,1,100,9999):
            for amount in (1,99,100,101):
                t=Token(fee); v=Vault(t); expected=amount-amount*fee//10000
                self.assertEqual(v.deposit('alice',amount),expected)
                self.assertEqual(sum(t.balances.values()),1000)
                self.assertEqual(sum(v.credits.values()),t.balances['vault'])

    def test_invalid_numeric_units(self):
        for amount in (0,-1,True,1.5):
            with self.assertRaises(ValueError): Vault(Token()).deposit('alice',amount)
