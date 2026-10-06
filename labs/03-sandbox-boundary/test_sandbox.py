import copy
import unittest

from sandbox_model import (
    CapabilityBoundary,
    GuestAction,
    Rejected,
    VulnerableBoundaryModel,
)


class SandboxBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.runtime = CapabilityBoundary()

    def reject_without_change(self, actions):
        before = copy.deepcopy(self.runtime.state)
        with self.assertRaises(Rejected):
            self.runtime.execute(actions)
        self.assertEqual(before, self.runtime.state)

    def test_vulnerable_dispatch_reaches_host_mint(self):
        runtime = VulnerableBoundaryModel()
        runtime.execute([GuestAction("host_mint", "bank", 500)])
        self.assertEqual(runtime.state.bank_supply, 1_000_500)

    def test_corrected_boundary_rejects_host_effect(self):
        self.reject_without_change([GuestAction("host_mint", "bank", 500)])

    def test_allowed_guest_write_preserves_bank_supply(self):
        self.runtime.execute([GuestAction("guest_write", "guest/counter", 7)])
        self.assertEqual(self.runtime.state.guest_store, {"guest/counter": 7})
        self.assertEqual(self.runtime.state.bank_supply, 1_000_000)

    def test_host_namespace_is_not_guest_writable(self):
        self.reject_without_change([GuestAction("guest_write", "host/bank", 7)])

    def test_unknown_operation_is_rejected(self):
        self.reject_without_change([GuestAction("native_jump", "guest/x", 1)])

    def test_batch_rejection_is_atomic(self):
        actions = [
            GuestAction("guest_write", "guest/first", 1),
            GuestAction("host_mint", "bank", 2),
        ]
        self.reject_without_change(actions)

    def test_invalid_action_type_is_rejected(self):
        self.reject_without_change([{"operation": "guest_write"}])

    def test_mutable_outer_batch_is_accepted_but_not_retained(self):
        actions = [GuestAction("guest_write", "guest/x", 1)]
        self.runtime.execute(actions)
        actions.append(GuestAction("guest_write", "guest/y", 2))
        self.assertNotIn("guest/y", self.runtime.state.guest_store)

    def test_invalid_values_are_rejected(self):
        for value in (-1, True, 1.5):
            with self.subTest(value=value):
                self.reject_without_change(
                    [GuestAction("guest_write", "guest/x", value)]
                )

    def test_non_batch_input_is_rejected(self):
        self.reject_without_change(GuestAction("guest_write", "guest/x", 1))


if __name__ == "__main__":
    unittest.main()
