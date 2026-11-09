# Batch value budget

Educational model, prepared November 9, 2026. Not an exploit replay, upstream patch, audited library or production component.

## Invariant

The total newly credited allocation never exceeds this call's incoming value. Rejected batches leave both modeled ledgers unchanged.

## Run

Pinned runtime: CPython 3.12.14; standard library only. No compiler/dependencies/network required.

```sh
cd labs/31-batch-value-budget
python3 -m unittest -v test_model
```

Eight tests passed locally on November 9, 2026. The `vulnerable=True` path is an intentional negative control. Tests asserting that it fails the intended property pass by demonstrating the defect. Hosted CI status must be checked separately.

Read [exercise](EXERCISE.md), then [solution](SOLUTION.md). Model and tests are AI-assisted original teaching code, not copied upstream code. No personal discovery or sole-human-authorship claim is made. Repository license status is unchanged.

## Source and scope

Technical reference inspected November 9: https://docs.soliditylang.org/en/v0.8.30/introduction-to-smart-contracts.html#delegatecall-and-libraries

Sequential integer ledger, trusted initial state, correctly shaped lists; no ABI, EVM, uint256 overflow, fees, external callbacks, nested batches or refund ownership. Direct-call entry points require separate guards.

All initial state is trusted and sequential. Supported inputs follow the documented function shapes. These tests do not certify malformed Python object handling or adversarial interpreter behavior. Explain which boundary must be reimplemented and tested in the deployed runtime.
