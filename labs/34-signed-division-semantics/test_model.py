import unittest
from model import MIN, MAX, trunc_divmod, floor_div, vulnerable_floor


class Tests(unittest.TestCase):
    def test_negative_control(self):
        self.assertEqual(vulnerable_floor(-5, 2), (-3, 1))
        self.assertEqual(trunc_divmod(-5, 2), (-2, -1))

    def test_all_signs(self):
        for a, b, expected in ((5, 2, (2, 1)), (-5, 2, (-2, -1)),
                                (5, -2, (-2, 1)), (-5, -2, (2, -1))):
            self.assertEqual(trunc_divmod(a, b), expected)

    def test_exact_division(self):
        for a in (-6, 0, 6):
            for b in (-3, 3):
                self.assertEqual(trunc_divmod(a, b), (a//b, 0))

    def test_minimum(self):
        self.assertEqual(trunc_divmod(MIN, 1), (MIN, 0))
        self.assertEqual(trunc_divmod(MIN, MIN), (1, 0))

    def test_checked_overflow(self):
        with self.assertRaises(ValueError):
            trunc_divmod(MIN, -1)

    def test_zero_divisor(self):
        for a in (MIN, 0, MAX):
            with self.assertRaises(ValueError):
                trunc_divmod(a, 0)

    def test_invalid_inputs(self):
        for value in (MIN-1, MAX+1, True, 0.5):
            for args in ((value, 1), (1, value)):
                with self.assertRaises(ValueError):
                    trunc_divmod(*args)

    def test_exhaustive_identity_and_sign(self):
        for a in range(-40, 41):
            for b in range(-40, 41):
                if b == 0:
                    continue
                q, r = trunc_divmod(a, b)
                self.assertEqual(a, q*b+r)
                self.assertLess(abs(r), abs(b))
                self.assertTrue(r == 0 or (r < 0) == (a < 0))
                self.assertEqual(floor_div(a, b), a//b)

    def test_no_float_conversion(self):
        self.assertEqual(trunc_divmod(MAX, 1), (MAX, 0))
        self.assertEqual(trunc_divmod(-MAX, 1), (-MAX, 0))

    def test_floor_policy_is_separate(self):
        self.assertEqual(trunc_divmod(-5, 2)[0], -2)
        self.assertEqual(floor_div(-5, 2), -3)
        self.assertEqual(floor_div(5, -2), -3)
