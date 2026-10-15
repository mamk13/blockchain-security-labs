import unittest
from epochs import EpochPolicy, GrantOnlyPolicy, Permit

class EpochTests(unittest.TestCase):
    def test_negative_control(self):
        bad, good = GrantOnlyPolicy(), EpochPolicy()
        for p in (bad, good):
            old = p.grant('alice', 7)
            p.cancel_all('alice')
        bad.execute(old)
        with self.assertRaises(ValueError): good.execute(old)
        self.assertEqual(good.used, set())

    def test_new_generation_same_nonce_does_not_resurrect_old(self):
        p = EpochPolicy(); old = p.grant('alice', 7)
        p.cancel_all('alice'); new = p.grant('alice', 7)
        with self.assertRaises(ValueError): p.execute(old)
        p.execute(new)
        self.assertEqual(p.used, {new})

    def test_replay_current_permit(self):
        p = EpochPolicy(); a = p.grant('alice', 0); p.execute(a)
        with self.assertRaises(ValueError): p.execute(a)

    def test_owner_scope(self):
        p = EpochPolicy(); a = p.grant('alice', 0); b = p.grant('bob', 0)
        p.cancel_all('alice'); p.execute(b)
        with self.assertRaises(ValueError): p.execute(a)

    def test_multiple_advances_never_reopen(self):
        p = EpochPolicy(); permits = []
        for _ in range(4):
            permits.append(p.grant('alice', 0)); p.cancel_all('alice')
        for a in permits:
            with self.assertRaises(ValueError): p.execute(a)
        self.assertFalse(p.used)

    def test_future_generation_cannot_be_forged(self):
        p = EpochPolicy()
        with self.assertRaises(ValueError): p.execute(Permit('alice', 1, 0))

    def test_invalid_nonce(self):
        for n in (-1, True, 1.5):
            with self.assertRaises(ValueError): EpochPolicy().grant('alice', n)
