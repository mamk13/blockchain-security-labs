import unittest
from dataclasses import replace
from claims import Claim, Distributor, leaf, parent

class ClaimTests(unittest.TestCase):
    def setUp(self):
        self.a,self.b = Claim('sale',0,'alice',10),Claim('sale',1,'bob',20)
        self.sibling=leaf(self.b)
        self.root=parent(leaf(self.a),self.sibling)

    def test_recipient_substitution_negative_control(self):
        sibling=leaf(self.b,False)
        bad=Distributor('sale',parent(leaf(self.a,False),sibling),False)
        bad.claim(replace(self.a,account='eve'),sibling)
        self.assertEqual(bad.paid,{'eve':10})
        good=Distributor('sale',self.root)
        with self.assertRaises(ValueError): good.claim(replace(self.a,account='eve'),self.sibling)
        self.assertEqual((good.used,good.paid),(set(),{}))

    def test_each_field_is_bound(self):
        for c in (replace(self.a,campaign='other'),replace(self.a,index=2),replace(self.a,amount=11)):
            with self.assertRaises(ValueError): Distributor('sale',self.root).claim(c,self.sibling)

    def test_valid_both_leaves(self):
        d=Distributor('sale',self.root); d.claim(self.a,self.sibling); d.claim(self.b,leaf(self.a))
        self.assertEqual(d.paid,{'alice':10,'bob':20})

    def test_root_rotation_keeps_consumption(self):
        d=Distributor('sale',self.root); d.claim(self.a,self.sibling)
        b2=replace(self.b,amount=30); sibling=leaf(b2)
        d.rotate_root(parent(leaf(self.a),sibling))
        with self.assertRaises(ValueError): d.claim(self.a,sibling)
        d.claim(b2,leaf(self.a)); self.assertEqual(d.paid,{'alice':10,'bob':30})

    def test_bad_proof_does_not_burn_index(self):
        d=Distributor('sale',self.root)
        with self.assertRaises(ValueError): d.claim(self.a,b'wrong')
        self.assertFalse(d.used); d.claim(self.a,self.sibling)

    def test_duplicate_index_allocation_cannot_pay_twice(self):
        other=replace(self.b,index=0)
        d=Distributor('sale',parent(leaf(self.a),leaf(other)))
        d.claim(self.a,leaf(other))
        with self.assertRaises(ValueError): d.claim(other,leaf(self.a))

    def test_separate_campaigns_have_separate_consumption(self):
        a,b=replace(self.a,campaign='second'),replace(self.b,campaign='second')
        d=Distributor('second',parent(leaf(a),leaf(b))); d.claim(a,leaf(b))
        self.assertEqual(d.paid,{'alice':10})
