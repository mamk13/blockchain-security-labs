# Weighted quorum configuration

Educational model, prepared November 9, 2026. Not an exploit replay, upstream patch, audited library or production component.

## Invariant

Every accepted configuration has positive uint64 weights, a positive reachable threshold and a total weight within uint64. Rejection preserves the previous entire configuration.

## Run

Pinned runtime: CPython 3.12.14; standard library only. No compiler/dependencies/network required.

```sh
cd labs/30-weighted-config
python3 -m unittest -v test_model
```

Eight tests passed locally on November 9, 2026. The `vulnerable=True` path is an intentional negative control. Tests asserting that it fails the intended property pass by demonstrating the defect. Hosted CI status must be checked separately.

Read [exercise](EXERCISE.md), then [solution](SOLUTION.md). Model and tests are AI-assisted original teaching code, not copied upstream code. No personal discovery or sole-human-authorship claim is made. Repository license status is unchanged.

## Source and scope

Technical reference inspected November 9: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v5.4.0/contracts/utils/cryptography/signers/MultiSignerERC7913Weighted.sol

Trusted administrator; no governance access control, signatures, transaction rollback, concurrent calls or actual key availability. The API replaces the whole configuration, unlike upstream incremental methods.

All initial state is trusted and sequential. Supported inputs follow the documented function shapes. These tests do not certify malformed Python object handling or adversarial interpreter behavior. Explain which boundary must be reimplemented and tested in the deployed runtime.
