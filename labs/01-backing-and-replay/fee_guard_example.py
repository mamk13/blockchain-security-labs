"""Original educational arithmetic model; not Symbiosis production code."""
import unittest
import random

MAX_SATOSHIS = 21_000_000 * 100_000_000

def vulnerable_net(deposit_sats, fee_sats):
    # Deliberately unsafe: models one failure class, not the full incident.
    return deposit_sats - fee_sats

def checked_net(deposit_sats: int, fee_sats: int) -> int:
    """Same-unit integer inputs. Zero-value mints are rejected by policy.

    deposit_sats MUST come from independently verified source-chain output
    data. This function neither authenticates that data nor authorizes fees.
    """
    if type(deposit_sats) is not int or type(fee_sats) is not int:
        raise TypeError("satoshi amounts must be integers, excluding bool")
    if not 0 < deposit_sats <= MAX_SATOSHIS:
        raise ValueError("invalid deposit amount")
    if not 0 <= fee_sats < deposit_sats:
        raise ValueError("fee must be nonnegative and below deposit")
    net = deposit_sats - fee_sats
    if not 0 < net <= deposit_sats:
        raise ValueError("mint amount violates backing bound")
    return net

class FeeGuardTests(unittest.TestCase):
    def test_negative_fee_regression(self):
        self.assertEqual(vulnerable_net(100, -1), 101)
        with self.assertRaises(ValueError):
            checked_net(100, -1)

    def test_fee_above_deposit_regression(self):
        self.assertEqual(vulnerable_net(100, 101), -1)
        with self.assertRaises(ValueError):
            checked_net(100, 101)

    def test_zero_fee_and_regular_fee(self):
        self.assertEqual(checked_net(100, 0), 100)
        self.assertEqual(checked_net(100, 7), 93)

    def test_zero_mint_rejected(self):
        with self.assertRaises(ValueError):
            checked_net(100, 100)

    def test_deposit_bounds(self):
        for deposit in (-1, 0, MAX_SATOSHIS + 1):
            with self.subTest(deposit=deposit), self.assertRaises(ValueError):
                checked_net(deposit, 0)
        self.assertEqual(checked_net(MAX_SATOSHIS, 0), MAX_SATOSHIS)

    def test_types(self):
        for bad in (True, False, 1.0, "1", None):
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError):
                    checked_net(bad, 0)
                with self.assertRaises(TypeError):
                    checked_net(100, bad)

    def test_exhaustive_small_domain(self):
        for deposit in range(1, 101):
            for fee in range(-2, deposit + 3):
                if 0 <= fee < deposit:
                    net = checked_net(deposit, fee)
                    self.assertEqual(net + fee, deposit)
                    self.assertTrue(0 < net <= deposit)
                else:
                    with self.assertRaises(ValueError):
                        checked_net(deposit, fee)

    def test_seeded_large_domain(self):
        rng = random.Random(20260920)
        for _ in range(10_000):
            deposit = rng.randint(1, MAX_SATOSHIS)
            fee = rng.randrange(deposit)
            net = checked_net(deposit, fee)
            self.assertEqual(net + fee, deposit)
            self.assertTrue(0 < net <= deposit)

if __name__ == "__main__":
    unittest.main(verbosity=2)
