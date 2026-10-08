import copy
import unittest

from vault_rounding import OffsetVault, Rejected, VulnerableVault


class VaultRoundingTests(unittest.TestCase):
    def test_vulnerable_donation_can_round_victim_to_zero(self):
        vault = VulnerableVault()
        vault.deposit(1)
        vault.donate(100)
        self.assertEqual(vault.deposit(100), 0)
        self.assertEqual(vault.total_assets, 201)
        self.assertEqual(vault.total_shares, 1)

    def test_virtual_offset_keeps_same_victim_deposit_nonzero(self):
        vault = OffsetVault(decimals_offset=3)
        vault.deposit(1)
        vault.donate(100)
        self.assertEqual(vault.deposit(100), 1_960)

    def test_zero_share_output_is_rejected_before_mutation(self):
        vault = OffsetVault(decimals_offset=3)
        vault.donate(10**9)
        before = copy.deepcopy(vault.__dict__)
        with self.assertRaisesRegex(Rejected, "bound"):
            vault.deposit(1)
        self.assertEqual(vault.__dict__, before)

    def test_preview_deposit_rounds_down(self):
        vault = OffsetVault(decimals_offset=0)
        vault.deposit(2)
        vault.donate(1)
        self.assertEqual(vault.preview_deposit(2), 1)

    def test_preview_mint_rounds_up(self):
        vault = OffsetVault(decimals_offset=0)
        vault.deposit(2)
        vault.donate(1)
        self.assertEqual(vault.preview_mint(2), 3)

    def test_deposit_matches_same_state_preview(self):
        vault = OffsetVault(decimals_offset=3)
        expected = vault.preview_deposit(37)
        self.assertEqual(vault.deposit(37, min_shares=expected), expected)

    def test_mint_matches_same_state_preview(self):
        vault = OffsetVault(decimals_offset=3)
        expected = vault.preview_mint(1_501)
        self.assertEqual(vault.mint(1_501, max_assets=expected), expected)

    def test_caller_deposit_bound_rejects_slippage(self):
        vault = OffsetVault(decimals_offset=3)
        expected = vault.preview_deposit(10)
        before = copy.deepcopy(vault.__dict__)
        with self.assertRaisesRegex(Rejected, "bound"):
            vault.deposit(10, min_shares=expected + 1)
        self.assertEqual(vault.__dict__, before)

    def test_caller_mint_bound_rejects_slippage(self):
        vault = OffsetVault(decimals_offset=3)
        expected = vault.preview_mint(10_001)
        before = copy.deepcopy(vault.__dict__)
        with self.assertRaisesRegex(Rejected, "bound"):
            vault.mint(10_001, max_assets=expected - 1)
        self.assertEqual(vault.__dict__, before)

    def test_donation_does_not_mint_shares(self):
        vault = OffsetVault()
        vault.deposit(10)
        shares = vault.total_shares
        vault.donate(50)
        self.assertEqual(vault.total_shares, shares)

    def test_initial_offset_defines_share_precision(self):
        vault = OffsetVault(decimals_offset=3)
        self.assertEqual(vault.preview_deposit(1), 1_000)

    def test_larger_deposit_never_previews_fewer_shares(self):
        vault = OffsetVault(decimals_offset=3)
        vault.deposit(7)
        vault.donate(11)
        previews = [vault.preview_deposit(assets) for assets in range(1, 20)]
        self.assertEqual(previews, sorted(previews))

    def test_mint_charge_covers_requested_share_output(self):
        vault = OffsetVault(decimals_offset=2)
        vault.deposit(13)
        vault.donate(5)
        for shares in (1, 17, 101):
            assets = vault.preview_mint(shares)
            self.assertGreaterEqual(vault.preview_deposit(assets), shares)

    def test_invalid_types_and_offsets_are_rejected(self):
        for offset in (-1, True, 19):
            with self.subTest(offset=offset):
                with self.assertRaises(Rejected):
                    OffsetVault(offset)
        vault = OffsetVault()
        for assets in (0, -1, True):
            with self.subTest(assets=assets):
                with self.assertRaises(Rejected):
                    vault.preview_deposit(assets)


if __name__ == "__main__":
    unittest.main()
