import unittest
from model import Token, Escrow, accepted, TRUE, FALSE

class ReturnTests(unittest.TestCase):
    def test_negative_control_false_clears_obligation(self):
        t=Token('false'); e=Escrow(t); e.pay(100,False)
        self.assertEqual((e.owed,t.balances['Alice']),(0,0))

    def test_false_rejected_with_obligation_retained(self):
        t=Token('false'); e=Escrow(t)
        with self.assertRaises(ValueError): e.pay(100)
        self.assertEqual((e.owed,t.balances),(100,{'escrow':100,'Alice':0}))

    def test_true_success(self):
        t=Token(); e=Escrow(t); e.pay(40)
        self.assertEqual((e.owed,t.balances),(60,{'escrow':60,'Alice':40}))

    def test_empty_contract_result_supported(self):
        t=Token('empty'); e=Escrow(t); e.pay(100)
        self.assertEqual((e.owed,t.balances['Alice']),(0,100))

    def test_empty_noncontract_rejected(self):
        e=Escrow(Token('no-code'))
        with self.assertRaises(ValueError): e.pay(100)
        self.assertEqual(e.owed,100)

    def test_malformed_reverts_selected_token_writes(self):
        t=Token('malformed'); e=Escrow(t)
        with self.assertRaises(ValueError): e.pay(100)
        self.assertEqual((e.owed,t.balances),(100,{'escrow':100,'Alice':0}))

    def test_false_after_write_rollback(self):
        t=Token('false-after-write'); e=Escrow(t)
        with self.assertRaises(ValueError): e.pay(100)
        self.assertEqual(t.balances,{'escrow':100,'Alice':0})

    def test_revert_retry(self):
        t=Token('revert'); e=Escrow(t)
        with self.assertRaises(ValueError): e.pay(100)
        t.mode='true'; e.pay(100)
        with self.assertRaises(ValueError): e.pay(1)

    def test_strict_fixture_return_matrix(self):
        for code in [False,True]:
            for ok in [False,True]:
                for data in [b'',TRUE,FALSE,b'\x01',(2).to_bytes(32,'big'),TRUE+b'x']:
                    self.assertEqual(accepted(code,ok,data),code and ok and data in (b'',TRUE))

    def test_limit_true_does_not_prove_receipt(self):
        t=Token('liar'); e=Escrow(t); e.pay(100)
        self.assertEqual((e.owed,t.balances['Alice']),(0,0))
