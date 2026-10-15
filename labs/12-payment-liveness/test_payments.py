import unittest
from payments import Distributor

class PaymentTests(unittest.TestCase):
    def test_batch_blocked_by_one_recipient(self):
        d = Distributor({'alice':10,'eve':5,'bob':7})
        with self.assertRaises(ValueError): d.push_all(lambda who:who!='eve')
        self.assertEqual((d.cash,d.received), (22,{}))
        self.assertEqual(d.pending, {'alice':10,'eve':5,'bob':7})

    def test_pull_isolates_rejection(self):
        d = Distributor({'alice':10,'eve':5,'bob':7})
        accept = lambda who:who!='eve'
        with self.assertRaises(ValueError): d.claim('eve',accept)
        d.claim('alice',accept); d.claim('bob',accept)
        self.assertEqual((d.cash,d.pending['eve']), (5,5))
        self.assertEqual(d.received, {'alice':10,'bob':7})

    def test_recovery(self):
        d = Distributor({'alice':10})
        with self.assertRaises(ValueError): d.claim('alice',lambda _:False)
        d.claim('alice',lambda _:True)
        self.assertEqual((d.cash,d.received),(0,{'alice':10}))

    def test_repeated_failure_preserves_claim(self):
        d = Distributor({'alice':10})
        for _ in range(3):
            with self.assertRaises(ValueError): d.claim('alice',lambda _:False)
        self.assertEqual(d.pending['alice'],10)

    def test_no_double_payment(self):
        d = Distributor({'alice':10}); d.claim('alice',lambda _:True)
        with self.assertRaises(ValueError): d.claim('alice',lambda _:True)

    def test_permutations_preserve_conservation(self):
        import itertools
        for order in itertools.permutations(['a','b','c']):
            d = Distributor({'a':1,'b':2,'c':3})
            for who in order:
                d.claim(who,lambda _:True)
                self.assertEqual(d.cash, sum(d.pending.values()))
                self.assertEqual(d.cash+sum(d.received.values()),6)
