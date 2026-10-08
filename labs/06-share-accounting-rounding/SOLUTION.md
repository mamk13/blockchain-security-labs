# Solution

`preview_deposit` rounds down because it must not promise more shares than the deposit can mint. `preview_mint` rounds up because it must not quote fewer assets than are required to mint the requested shares. Replacing ceiling division with floor division makes the mint quote undercharge for some ratios, and the coverage test fails.

In the vulnerable trace, the first depositor owns one share, the donation moves the exchange rate, and the victim's 100-asset deposit rounds to zero shares. The assets still enter the vault, benefiting the existing shareholder.

Virtual assets and shares anchor the empty-vault rate and cause the donor to own only a fraction of the effective share supply. Higher share precision reduces the chance that ordinary deposits round to zero. A caller's `min_shares` or `max_assets` bound then turns an unexpected quote into a rejection before state changes.

These controls do not make every ERC-4626 integration safe. Production code must also handle the omitted token behaviors, fees, reentrancy, strategy accounting and preview/execution consistency.
