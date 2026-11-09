# Refund ownership after partial failure

Educational model, prepared November 9, 2026. Not an exploit replay, upstream patch, audited library or production component.

## Invariant

Each payer's new refund equals incoming value minus successful allocated expenditure. Prior funds and other payers' refunds never become the latest payer's refund.

## Run

Pinned runtime: CPython 3.12.14; standard library only. No compiler/dependencies/network required.

```sh
cd labs/32-refund-ownership
python3 -m unittest -v test_model
```

Eight tests passed locally on November 9, 2026. The `vulnerable=True` path is an intentional negative control. Tests asserting that it fails the intended property pass by demonstrating the defect. Hosted CI status must be checked separately.

Read [exercise](EXERCISE.md), then [solution](SOLUTION.md). Model and tests are AI-assisted original teaching code, not copied upstream code. No personal discovery or sole-human-authorship claim is made. Repository license status is unchanged.

## Source and scope

Technical reference inspected November 9: https://docs.soliditylang.org/en/v0.8.30/introduction-to-smart-contracts.html#message-calls

Outcomes are trusted side-effect-free fixtures. No actual token/Ether call, recipient rejection, gas cost, reentrancy, sender authentication or relayer policy. Payer identity must come from authenticated funding context in an integration; user-controlled labels are not authentication.

All initial state is trusted and sequential. Supported inputs follow the documented function shapes. These tests do not certify malformed Python object handling or adversarial interpreter behavior. Explain which boundary must be reimplemented and tested in the deployed runtime.
