import unittest
from model import Event, Ledger

class FinalityTests(unittest.TestCase):
    def setUp(self):
        self.e = Event(10, 'A', 'tx1', 0, 'Alice', 70)
        self.l = Ledger()

    def test_negative_control_orphan_credit(self):
        self.l.accept(self.e, {10:'B'}, 10, guarded=False)
        self.assertEqual(self.l.credits, {'Alice':70})

    def test_pending_rejected_without_consumption(self):
        with self.assertRaises(ValueError): self.l.accept(self.e, {10:'A'}, 9)
        self.assertEqual((self.l.credits,self.l.consumed), ({},set()))

    def test_height_alone_not_sufficient(self):
        with self.assertRaises(ValueError): self.l.accept(self.e, {10:'B'}, 10)
        self.assertEqual(self.l.credits,{})

    def test_unknown_block_rejected(self):
        with self.assertRaises(ValueError): self.l.accept(self.e, {}, 10)

    def test_finalized_retry_then_duplicate(self):
        with self.assertRaises(ValueError): self.l.accept(self.e, {10:'A'}, 9)
        self.l.accept(self.e, {10:'A'}, 10)
        with self.assertRaises(ValueError): self.l.accept(self.e, {10:'A'}, 10)
        self.assertEqual(self.l.credits, {'Alice':70})

    def test_reinclusion_after_orphan_rejection(self):
        with self.assertRaises(ValueError): self.l.accept(self.e, {10:'B'}, 10)
        replacement=Event(11,'C','tx1',0,'Alice',70)
        self.l.accept(replacement,{10:'B',11:'C'},11)
        self.assertEqual(self.l.credits,{'Alice':70})

    def test_distinct_log_index(self):
        self.l.accept(self.e,{10:'A'},10)
        self.l.accept(Event(10,'A','tx1',1,'Bob',30),{10:'A'},10)
        self.assertEqual(self.l.credits,{'Alice':70,'Bob':30})

    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.l.accept(Event(10,'A','tx2',0,'Alice',-1),{10:'A'},10)
        self.assertEqual(self.l.consumed,set())

if __name__ == '__main__': unittest.main()
