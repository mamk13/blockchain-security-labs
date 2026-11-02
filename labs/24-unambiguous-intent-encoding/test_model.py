import itertools
import unittest
from model import Approval, encode, decode, packed, PREFIX

class EncodingTests(unittest.TestCase):
    def test_negative_control_same_bytes_different_fields(self):
        self.assertEqual(packed(b'a',b'bc'),packed(b'ab',b'c'))
        self.assertEqual(Approval(b'a',b'bc',False).execute(b'ab',b'c'),(b'ab',b'c'))

    def test_boundary_substitution_rejects_without_consumption(self):
        a=Approval(b'a',b'bc')
        with self.assertRaises(ValueError): a.execute(b'ab',b'c')
        self.assertFalse(a.consumed)
        self.assertEqual(a.execute(b'a',b'bc'),(b'a',b'bc'))

    def test_empty_boundaries_distinct(self):
        self.assertNotEqual(encode(b'',b'a'),encode(b'a',b''))

    def test_embedded_delimiter_roundtrip(self):
        pair=(b'a\x00|b',b'\x00|')
        self.assertEqual(decode(encode(*pair)),pair)

    def test_small_domain_injective_and_roundtrip(self):
        values=[bytes(p) for n in range(4) for p in itertools.product(range(3),repeat=n)]
        seen={}
        for pair in itertools.product(values,repeat=2):
            data=encode(*pair)
            self.assertEqual(decode(data),pair)
            self.assertNotIn(data,seen); seen[data]=pair

    def test_truncation_rejected(self):
        data=encode(b'abc',b'def')
        for n in range(len(data)):
            with self.assertRaises(ValueError): decode(data[:n])

    def test_trailing_and_wrong_version_rejected(self):
        for data in [encode(b'a',b'b')+b'x',b'other'+encode(b'a',b'b')]:
            with self.assertRaises(ValueError): decode(data)

    def test_max_length_roundtrip(self):
        pair=(b'a'*65535,b'')
        self.assertEqual(decode(encode(*pair)),pair)
        with self.assertRaises(ValueError): encode(b'a'*65536,b'')

    def test_types_are_explicit(self):
        with self.assertRaises(ValueError): encode('a',b'b')

    def test_encoding_alone_does_not_stop_replay(self):
        a=Approval(b'a',b'b'); a.execute(b'a',b'b')
        with self.assertRaises(ValueError): a.execute(b'a',b'b')
        # A separate consumer still accepts: no global replay policy is claimed.
        self.assertEqual(Approval(b'a',b'b').execute(b'a',b'b'),(b'a',b'b'))
