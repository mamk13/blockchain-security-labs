import unittest
from settlement import Vault

class CallbackTests(unittest.TestCase):
    def attack(self, v):
        def again():
            try: v.withdraw('alice')
            except ValueError: pass
        v.withdraw('alice', again)

    def test_same_owner_reentry_negative_control(self):
        bad, good = Vault(False), Vault()
        self.attack(bad); self.attack(good)
        self.assertEqual(bad.received['alice'],20)
        self.assertEqual(good.received['alice'],10)
        self.assertLess(bad.cash, sum(bad.claims.values()))
        self.assertEqual(good.cash, sum(good.claims.values()))

    def test_other_owner_remains_payable(self):
        v = Vault(); self.attack(v); v.withdraw('bob')
        self.assertEqual(v.received, {'alice':10,'bob':10})

    def test_propagated_callback_failure_restores_state(self):
        v = Vault(); before = (v.claims.copy(),v.cash,v.received.copy())
        def fail(): raise RuntimeError('recipient rejects')
        with self.assertRaises(RuntimeError): v.withdraw('alice', fail)
        self.assertEqual((v.claims,v.cash,v.received),before)
        self.assertEqual(v.depth,0)
        v.withdraw('alice')

    def test_nested_success_then_outer_failure_rolls_back_both(self):
        v = Vault()
        def outer():
            v.withdraw('bob')
            raise RuntimeError('outer fails')
        with self.assertRaises(RuntimeError): v.withdraw('alice', outer)
        self.assertEqual((v.cash,v.received,v.claims), (20,{}, {'alice':10,'bob':10}))

    def test_caught_nested_failure_does_not_cancel_outer(self):
        v = Vault()
        def outer():
            try: v.withdraw('bob', lambda: (_ for _ in ()).throw(RuntimeError()))
            except RuntimeError: pass
        v.withdraw('alice', outer)
        self.assertEqual(v.received,{'alice':10})
        self.assertEqual(v.claims['bob'],10)

    def test_duplicate_and_unknown_claim(self):
        v = Vault(); v.withdraw('alice')
        for who in ('alice','eve'):
            with self.assertRaises(ValueError): v.withdraw(who)
