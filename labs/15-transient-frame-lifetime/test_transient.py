import unittest
from transient import Transaction, Guard, EndOfTransactionOnlyGuard, Reverted


class TransientTests(unittest.TestCase):
    def test_negative_control_sequential_calls(self):
        tx = Transaction()
        with tx.transaction():
            bad = EndOfTransactionOnlyGuard(tx)
            bad.call()
            with self.assertRaises(Reverted):
                bad.call()

    def test_correct_sequential_calls(self):
        tx = Transaction()
        with tx.transaction():
            good = Guard(tx)
            for _ in range(5):
                good.call()
                self.assertEqual(tx.read('vault', 'lock'), 0)

    def test_nested_call_rejected_but_outer_recovers(self):
        tx = Transaction()
        with tx.transaction():
            good = Guard(tx)
            def callback():
                with self.assertRaises(Reverted):
                    good.call()
                self.assertEqual(tx.read('vault', 'lock'), 1)
            good.call(callback)
            good.call()

    def test_propagated_revert_restores_lock(self):
        tx = Transaction()
        with tx.transaction():
            good = Guard(tx)
            with self.assertRaises(Reverted):
                good.call(good.call)
            self.assertEqual(tx.read('vault', 'lock'), 0)
            good.call()

    def test_child_revert_preserves_parent_write(self):
        tx = Transaction()
        with tx.transaction(), tx.frame():
            tx.write('a', 'x', 7)
            with self.assertRaises(Reverted), tx.frame():
                tx.write('a', 'x', 8)
                tx.write('b', 'y', 9)
                raise Reverted()
            self.assertEqual(tx.transient, {('a', 'x'): 7})

    def test_parent_revert_undoes_successful_child(self):
        tx = Transaction()
        with tx.transaction():
            with self.assertRaises(Reverted), tx.frame():
                with tx.frame():
                    tx.write('b', 'y', 9)
                raise Reverted()
            self.assertFalse(tx.transient)

    def test_owners_have_separate_locks(self):
        tx = Transaction()
        with tx.transaction():
            a, b = Guard(tx, 'a'), Guard(tx, 'b')
            a.call(b.call)

    def test_same_owner_wrappers_share_lock(self):
        tx = Transaction()
        with tx.transaction():
            a, b = Guard(tx), Guard(tx)
            with self.assertRaises(Reverted):
                a.call(b.call)

    def test_success_resets_at_transaction_end(self):
        tx = Transaction()
        for _ in range(2):
            with tx.transaction():
                self.assertEqual(tx.read('vault', 'lock'), 0)
                EndOfTransactionOnlyGuard(tx).call()
            self.assertEqual(tx.transient, {})

    def test_failure_also_discards_transaction_state(self):
        tx = Transaction()
        with self.assertRaises(Reverted), tx.transaction():
            tx.write('a', 'x', 1)
            raise Reverted()
        self.assertFalse(tx.transient)
        self.assertFalse(tx.active)

    def test_access_requires_transaction(self):
        tx = Transaction()
        with self.assertRaises(RuntimeError): tx.read('a', 'x')
        with self.assertRaises(RuntimeError): tx.write('a', 'x', 1)

    def test_nested_transaction_cannot_reset_lock(self):
        tx = Transaction()
        with tx.transaction():
            tx.write('a', 'x', 1)
            with self.assertRaises(RuntimeError), tx.transaction(): pass
            self.assertEqual(tx.read('a', 'x'), 1)

if __name__ == '__main__': unittest.main()
