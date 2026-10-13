import unittest
from dataclasses import replace
from authorization import Intent, WalletPolicy, CachedConsumer, CurrentConsumer, Rejected


class AuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.i = Intent('chain1:consumer1', 'bob', 10, 0, 100)
        self.w = WalletPolicy()
        self.w.grant(self.i, 'proof-A')
        self.c = CurrentConsumer(self.i.domain, self.w)

    def state(self):
        return self.c.balance, self.c.used.copy(), self.c.payments.copy()

    def rejected_unchanged(self, intent=None, proof='proof-A', now=50):
        before = self.state()
        with self.assertRaises(Rejected):
            self.c.execute(intent or self.i, proof, now)
        self.assertEqual(before, self.state())

    def test_negative_control_cached_approval_survives_revocation(self):
        bad = CachedConsumer(self.i.domain, self.w)
        bad.admit(self.i, 'proof-A')
        self.w.revoke(self.i, 'proof-A')
        bad.execute(self.i, 'proof-A', 50)
        self.assertEqual(10, bad.payments['bob'])
        self.rejected_unchanged()

    def test_current_authorization_succeeds_without_cached_admission(self):
        self.c.execute(self.i, 'proof-A', 50)
        self.assertEqual((90, {0}, {'bob': 10}), self.state())

    def test_wallet_failure_does_not_consume_nonce(self):
        self.w.available = False
        self.rejected_unchanged()

    def test_recovery_after_unavailability(self):
        self.w.available = False
        self.rejected_unchanged()
        self.w.available = True
        self.c.execute(self.i, 'proof-A', 50)
        self.assertEqual(90, self.c.balance)

    def test_deadline_boundaries(self):
        for now in (99, 100, 101):
            self.c = CurrentConsumer(self.i.domain, self.w)
            if now > 100:
                self.rejected_unchanged(now=now)
            else:
                self.c.execute(self.i, 'proof-A', now)
                self.assertEqual(90, self.c.balance)

    def test_changed_intent_fields_reject(self):
        for field, value in dict(domain='other', recipient='eve', amount=11, nonce=1, deadline=101).items():
            with self.subTest(field=field):
                self.rejected_unchanged(replace(self.i, **{field: value}))

    def test_wrong_proof(self):
        self.rejected_unchanged(proof='proof-B')

    def test_nonce_replay_with_distinct_valid_intent(self):
        self.c.execute(self.i, 'proof-A', 50)
        other = replace(self.i, recipient='carol')
        self.w.grant(other, 'proof-B')
        self.rejected_unchanged(other, 'proof-B')

    def test_regrant_is_policy_decision(self):
        self.w.revoke(self.i, 'proof-A')
        self.rejected_unchanged()
        self.w.grant(self.i, 'proof-A')
        self.c.execute(self.i, 'proof-A', 50)
        self.assertEqual(90, self.c.balance)

    def test_insufficient_balance(self):
        self.c.balance = 9
        self.rejected_unchanged()

    def test_invalid_clock(self):
        for now in (-1, True, 1.0):
            self.rejected_unchanged(now=now)

    def test_input_boundaries(self):
        for field, value in [('amount', 0), ('amount', True), ('nonce', -1), ('deadline', -1), ('domain', ''), ('recipient', '')]:
            with self.subTest(field=field, value=value), self.assertRaises(Rejected):
                replace(self.i, **{field: value})


if __name__ == '__main__':
    unittest.main()
