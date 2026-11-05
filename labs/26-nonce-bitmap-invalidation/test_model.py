import unittest
from model import Bitmap,MAX
class Tests(unittest.TestCase):
    def test_negative_control(self):
        b=Bitmap(); b.invalidate("a",255,True); b.invalidate("a",255,True)
        b.consume("a",255)
    def test_idempotent_invalidation(self):
        b=Bitmap(); b.invalidate("a",255); before=b.words.copy(); b.invalidate("a",255)
        self.assertEqual(b.words,before)
        with self.assertRaises(ValueError): b.consume("a",255)
    def test_word_boundary(self):
        b=Bitmap(); b.consume("a",255); b.consume("a",256)
        self.assertEqual(b.words,{("a",0):1<<255,("a",1):1})
    def test_owner_isolation(self):
        b=Bitmap(); b.consume("a",7); b.consume("b",7)
        self.assertEqual(len(b.words),2)
    def test_replay_preserves(self):
        b=Bitmap(); b.consume("a",0); before=b.words.copy()
        with self.assertRaises(ValueError): b.consume("a",0)
        self.assertEqual(b.words,before)
    def test_invalid_signature_retry(self):
        b=Bitmap()
        with self.assertRaises(ValueError): b.consume("a",1,False)
        self.assertEqual(b.words,{})
        b.consume("a",1)
    def test_uint256_bounds(self):
        b=Bitmap(); b.consume("a",MAX)
        for n in [-1,MAX+1,True]:
            with self.assertRaises(ValueError): b.consume("a",n)
    def test_all_bits_and_reverse_order(self):
        b=Bitmap()
        for n in reversed(range(512)): b.consume("a",n)
        self.assertEqual(b.words,{("a",0):MAX,("a",1):MAX})
