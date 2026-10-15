import unittest
from domains import Authority, Consumer, Domain, Order

class DomainTests(unittest.TestCase):
    def setUp(self):
        self.d = Domain(1, 'vault-A', 'pay-v1')
        self.a = Authority(); self.o = Order('alice', 10, 0)
        self.a.grant(self.d, self.o)

    def test_unbound_negative_control(self):
        other = Domain(2, 'vault-B', 'pay-v2')
        bad = Consumer(other, self.a, False); bad.execute(self.o)
        self.assertEqual(bad.credits, {'alice': 10})
        good = Consumer(other, self.a)
        with self.assertRaises(ValueError): good.execute(self.o)
        self.assertEqual((good.used, good.credits), (set(), {}))

    def test_each_domain_dimension(self):
        for d in (Domain(2,'vault-A','pay-v1'), Domain(1,'vault-B','pay-v1'), Domain(1,'vault-A','pay-v2')):
            with self.subTest(d=d):
                c = Consumer(d, self.a)
                with self.assertRaises(ValueError): c.execute(self.o)

    def test_domain_does_not_replace_nonce(self):
        c = Consumer(self.d, self.a); c.execute(self.o)
        with self.assertRaises(ValueError): c.execute(self.o)
        self.assertEqual(c.credits, {'alice': 10})

    def test_each_payload_dimension(self):
        for o in (Order('eve',10,0), Order('alice',11,0), Order('alice',10,1)):
            with self.assertRaises(ValueError): Consumer(self.d,self.a).execute(o)

    def test_explicit_second_domain_grant(self):
        d = Domain(2,'vault-A','pay-v1'); self.a.grant(d,self.o)
        Consumer(self.d,self.a).execute(self.o)
        Consumer(d,self.a).execute(self.o)

    def test_same_nonce_different_order_rejected(self):
        c = Consumer(self.d,self.a); c.execute(self.o)
        o = Order('bob',20,0); self.a.grant(self.d,o)
        with self.assertRaises(ValueError): c.execute(o)

    def test_numeric_type(self):
        o = Order('alice', True, 1); self.a.grant(self.d,o)
        with self.assertRaises(ValueError): Consumer(self.d,self.a).execute(o)
