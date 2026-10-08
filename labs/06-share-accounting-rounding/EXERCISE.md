# Exercise

The exchange rate is not only a ratio; its integer rounding direction decides who receives the remainder.

1. Run `python3 -m unittest -v test_vault_rounding`.
2. In `OffsetVault.preview_mint`, replace ceiling division with floor division.
3. Rerun `test_preview_mint_rounds_up` and `test_mint_charge_covers_requested_share_output`.
4. Explain why `preview_deposit` and `preview_mint` require opposite rounding directions.
5. In the vulnerable model, trace `deposit(1)`, `donate(100)`, `deposit(100)` and identify who owns the victim's donated value.
6. Explain what `min_shares` protects and what it cannot protect if the preview itself uses incorrect state or units.

Keep the exercise local. Do not deploy a token or interact with a live vault.
