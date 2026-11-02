import unittest
from model import Intent, Pool

class PriceTests(unittest.TestCase):
    def test_negative_control_adverse_reserves(self):
        p=Pool(2000,500)
        self.assertEqual(p.execute(Intent(100,90,10),5,False),23)

    def test_bound_rejection_preserves_all_ledgers(self):
        p=Pool(2000,500); before=p.state()
        with self.assertRaises(ValueError): p.execute(Intent(100,90,10),5)
        self.assertEqual(p.state(),before)

    def test_exact_minimum_and_deadline_accept(self):
        p=Pool(); self.assertEqual(p.execute(Intent(100,90,10),10),90)
        self.assertEqual(p.state(),(1100,910,0,90))

    def test_one_unit_above_output_rejects(self):
        p=Pool(); before=p.state()
        with self.assertRaises(ValueError): p.execute(Intent(100,91,10),1)
        self.assertEqual(p.state(),before)

    def test_expiration_even_with_good_price(self):
        p=Pool(); before=p.state()
        with self.assertRaises(ValueError): p.execute(Intent(100,80,10),11)
        self.assertEqual(p.state(),before)

    def test_deadline_alone_does_not_protect_price(self):
        self.assertEqual(Pool(2000,500).execute(Intent(100,0,10),5),23)

    def test_rejected_attempt_can_retry(self):
        p=Pool()
        with self.assertRaises(ValueError): p.execute(Intent(100,91,10),5)
        self.assertEqual(p.execute(Intent(100,90,10),5),90)

    def test_conservation_and_product_small_domain(self):
        for x in range(1,12):
            for y in range(1,12):
                for a in range(1,8):
                    p=Pool(x,y,a); p.execute(Intent(a,0,1),1)
                    self.assertEqual(p.x+p.wallet,x+a)
                    self.assertEqual(p.y+p.received,y)
                    self.assertGreaterEqual(p.x*p.y,x*y)

    def test_invalid_fields_preserve_state(self):
        for i in [Intent(True,0,1),Intent(0,0,1),Intent(1,-1,1),Intent(1,0,-1)]:
            p=Pool(); before=p.state()
            with self.assertRaises(ValueError): p.execute(i,0)
            self.assertEqual(p.state(),before)

    def test_insufficient_funds(self):
        p=Pool(); before=p.state()
        with self.assertRaises(ValueError): p.execute(Intent(101,0,1),0)
        self.assertEqual(p.state(),before)
