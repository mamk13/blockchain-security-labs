import unittest

from oracle_guard import Observation, Rejected, derive_price, vulnerable_derived_price


NOW = 1_800_000_000


class OracleGuardTests(unittest.TestCase):
    def setUp(self):
        self.base = Observation(2_000 * 10**8, 8, NOW - 10)
        self.quote = Observation(1 * 10**6, 6, NOW - 12)

    def derive(self, base=None, quote=None, **overrides):
        policy = {
            "now": NOW,
            "max_age": 60,
            "max_skew": 5,
            "output_decimals": 18,
        }
        policy.update(overrides)
        return derive_price(base or self.base, quote or self.quote, **policy)

    def test_vulnerable_model_misprices_mismatched_decimals(self):
        price = vulnerable_derived_price(self.base, self.quote)
        self.assertEqual(price, 200_000 * 10**18)

    def test_corrected_model_normalizes_each_feed(self):
        self.assertEqual(self.derive(), 2_000 * 10**18)

    def test_fresh_but_skewed_pair_is_rejected(self):
        quote = Observation(10**6, 6, NOW - 30)
        with self.assertRaisesRegex(Rejected, "skew"):
            self.derive(quote=quote)

    def test_skew_boundary_is_inclusive(self):
        quote = Observation(10**6, 6, NOW - 15)
        self.assertEqual(self.derive(quote=quote), 2_000 * 10**18)

    def test_each_feed_has_an_independent_age_check(self):
        stale_base = Observation(self.base.answer, 8, NOW - 61)
        stale_quote = Observation(self.quote.answer, 6, NOW - 61)
        for base, quote in ((stale_base, self.quote), (self.base, stale_quote)):
            with self.subTest(base=base, quote=quote):
                with self.assertRaisesRegex(Rejected, "stale"):
                    self.derive(base=base, quote=quote)

    def test_age_boundary_is_inclusive(self):
        base = Observation(self.base.answer, 8, NOW - 60)
        quote = Observation(self.quote.answer, 6, NOW - 60)
        self.assertEqual(self.derive(base=base, quote=quote), 2_000 * 10**18)

    def test_future_timestamp_is_rejected(self):
        base = Observation(self.base.answer, 8, NOW + 1)
        with self.assertRaisesRegex(Rejected, "future"):
            self.derive(base=base)

    def test_nonpositive_answers_are_rejected(self):
        for answer in (0, -1):
            with self.subTest(answer=answer):
                with self.assertRaises(Rejected):
                    self.derive(base=Observation(answer, 8, NOW - 10))

    def test_unsupported_decimal_range_is_rejected(self):
        for decimals in (-1, 19):
            with self.subTest(decimals=decimals):
                with self.assertRaises(Rejected):
                    self.derive(base=Observation(self.base.answer, decimals, NOW - 10))

    def test_bool_and_malformed_inputs_are_rejected(self):
        invalid = [Observation(True, 8, NOW - 10), {"answer": self.base.answer}]
        for base in invalid:
            with self.subTest(base=base):
                with self.assertRaises(Rejected):
                    self.derive(base=base)

    def test_ratio_rounds_down_in_declared_output_units(self):
        base = Observation(10, 0, NOW - 1)
        quote = Observation(3, 0, NOW - 1)
        self.assertEqual(self.derive(base=base, quote=quote, output_decimals=2), 333)

    def test_invalid_policy_values_are_rejected(self):
        for override in (
            {"max_age": -1},
            {"max_skew": True},
            {"output_decimals": 19},
        ):
            with self.subTest(override=override):
                with self.assertRaises(Rejected):
                    self.derive(**override)


if __name__ == "__main__":
    unittest.main()
