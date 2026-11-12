import unittest
from model import MAX, checked_intermediate, mul_div, vulnerable_wrapped


class Tests(unittest.TestCase):
    def test_wrapping_negative_control(self):
        x = 1 << 200
        self.assertEqual(vulnerable_wrapped(x, 1 << 100, 1 << 100), 0)
        self.assertEqual(mul_div(x, 1 << 100, 1 << 100), x)

    def test_checked_intermediate_rejects_representable_result(self):
        with self.assertRaises(ValueError):
            checked_intermediate(1 << 200, 1 << 100, 1 << 100)

    def test_exact_max_result(self):
        self.assertEqual(mul_div(MAX, MAX, MAX), MAX)
        self.assertEqual(mul_div(MAX, MAX, MAX, round_up=True), MAX)

    def test_result_overflow(self):
        with self.assertRaises(ValueError):
            mul_div(MAX, MAX, 1)

    def test_ceiling_only_overflow(self):
        # (MAX-1)^2 / (MAX-2) = MAX + 1/(MAX-2).
        self.assertEqual(mul_div(MAX-1, MAX-1, MAX-2), MAX)
        with self.assertRaises(ValueError):
            mul_div(MAX-1, MAX-1, MAX-2, round_up=True)

    def test_zero(self):
        self.assertEqual(mul_div(0, MAX, 1, round_up=True), 0)
        with self.assertRaises(ValueError):
            mul_div(0, 0, 0)

    def test_invalid_inputs(self):
        for value in (-1, MAX+1, True, 1.0):
            for args in ((value, 1, 1), (1, value, 1), (1, 1, value)):
                with self.assertRaises(ValueError):
                    mul_div(*args)
        with self.assertRaises(ValueError):
            mul_div(1, 1, 1, round_up=1)

    def test_small_domain_inequalities(self):
        for x in range(17):
            for y in range(17):
                for d in range(1, 17):
                    product = x*y
                    floor = mul_div(x, y, d)
                    ceil = mul_div(x, y, d, round_up=True)
                    self.assertLessEqual(floor*d, product)
                    self.assertLess(product, (floor+1)*d)
                    self.assertGreaterEqual(ceil*d, product)
                    self.assertLess((ceil-1)*d, product)
                    self.assertIn(ceil-floor, (0, 1))

    def test_divide_first_loses_precision(self):
        self.assertEqual((7//3)*5, 10)
        self.assertEqual(mul_div(7, 5, 3), 11)

    def test_wide_boundaries(self):
        for x in (1 << 128, 1 << 200, MAX):
            for y in (1, 3, MAX):
                self.assertEqual(mul_div(x, y, y), x)
