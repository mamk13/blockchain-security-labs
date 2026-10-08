# Lab 06 · Share accounting and rounding

## Learning objective

Test the invariant: **share previews use the correct rounding direction, caller bounds are enforced before mutation, and an empty-vault exchange rate is not left entirely to the first depositor**.

The vulnerable model permits a direct donation to change the exchange rate until a later deposit rounds to zero shares. The corrected educational model adds virtual assets and shares, higher share precision, explicit round-down/round-up previews, and caller-provided bounds.

This model is inspired by ERC-4626 accounting but is not a compliant token vault, audited implementation, deployed patch, or exploit replay.

## Runtime

- CPython 3.12.14
- Python standard library only
- No Solidity compiler, token, RPC, wallet, network request, or live transaction

## Run

```sh
cd labs/06-share-accounting-rounding
python3 -m unittest -v test_vault_rounding
```

Read [EXERCISE.md](EXERCISE.md) before [SOLUTION.md](SOLUTION.md).

## Evidence boundary

EIP-4626 requires `convertToShares` and `convertToAssets` to round down, and constrains preview functions so deposits do not promise too many shares while mints do not understate required assets. OpenZeppelin's ERC-4626 guide documents the empty-vault donation/inflation risk and a defense using virtual assets, virtual shares, and a decimals offset.

Primary references:

- [ERC-4626 specification](https://eips.ethereum.org/EIPS/eip-4626)
- [OpenZeppelin ERC-4626 security guide](https://docs.openzeppelin.com/contracts/5.x/erc4626)

The lab omits fees, withdrawals, redemptions, token transfers, fee-on-transfer and rebasing assets, reentrancy, access control, overflow limits, asynchronous strategies and integrator behavior. Its assertions establish only the modeled integer arithmetic.
