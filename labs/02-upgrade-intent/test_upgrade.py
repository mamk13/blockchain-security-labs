import copy
import unittest
from dataclasses import replace

from upgrade_model import Action, BoundQueue, Rejected, VulnerableQueue


class UpgradeTests(unittest.TestCase):
    def setUp(self):
        self.a = Action("lab-chain", "upgrade-gate", "vault", "code-A", b"{}", 1)
        self.q = BoundQueue()
        self.q.queue("governor", "p1", self.a, 100)

    def reject_without_change(self, call):
        before = copy.deepcopy(vars(self.q))
        with self.assertRaises(Rejected):
            call()
        self.assertEqual(before, vars(self.q))

    def test_vulnerable_payload_substitution(self):
        q = VulnerableQueue()
        q.queue("p1", self.a, 100, 10)
        changed = replace(self.a, code="code-B")
        q.execute("p1", changed, 110)
        self.assertNotEqual(q.applied[0], self.a)

    def test_every_bound_field_rejects_substitution(self):
        changes = dict(chain="other-chain", executor="other-gate", target="other-vault",
                       code="code-B", arguments=b'{"recipient":"other"}', nonce=2)
        for field, value in changes.items():
            with self.subTest(field=field):
                self.reject_without_change(lambda: self.q.execute(
                    "executor", "p1", replace(self.a, **{field: value}), 110))

    def test_early_execution_rejected(self):
        self.reject_without_change(lambda: self.q.execute("executor", "p1", self.a, 109))

    def test_exact_readiness_executes_original_once(self):
        self.q.execute("executor", "p1", self.a, 110)
        self.assertEqual(self.q.applied, [self.a])
        self.reject_without_change(lambda: self.q.execute("executor", "p1", self.a, 111))

    def test_duplicate_queue_cannot_overwrite(self):
        self.reject_without_change(lambda: self.q.queue(
            "governor", "p1", replace(self.a, code="code-B"), 101))

    def test_cancellation_removes_execution_authority(self):
        self.q.cancel("guardian", "p1")
        self.reject_without_change(lambda: self.q.execute("executor", "p1", self.a, 110))
        self.reject_without_change(lambda: self.q.queue("governor", "p1", self.a, 110))

    def test_roles_are_distinct(self):
        for call in (
            lambda: self.q.queue("executor", "p2", self.a, 100),
            lambda: self.q.execute("governor", "p1", self.a, 110),
            lambda: self.q.cancel("governor", "p1"),
        ):
            self.reject_without_change(call)

    def test_foreign_domain_cannot_enter_queue(self):
        self.reject_without_change(lambda: self.q.queue(
            "governor", "p2", replace(self.a, chain="foreign"), 100))

    def test_mutable_arguments_rejected(self):
        self.reject_without_change(lambda: self.q.queue(
            "governor", "p2", replace(self.a, arguments=bytearray(b"{}")), 100))

    def test_invalid_time_rejected(self):
        for now in (-1, True, 110.0):
            self.reject_without_change(lambda: self.q.execute("executor", "p1", self.a, now))

    def test_missing_proposal_rejected(self):
        self.reject_without_change(lambda: self.q.execute("executor", "missing", self.a, 110))

    def test_delay_does_not_detect_malicious_approved_code(self):
        bad = replace(self.a, code="malicious-but-approved", nonce=2)
        self.q.queue("governor", "p2", bad, 100)
        self.q.execute("executor", "p2", bad, 110)
        self.assertEqual(self.q.applied, [bad])


if __name__ == "__main__":
    unittest.main()
