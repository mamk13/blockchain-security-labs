# Lab 15 — Transient frame lifetime

**Educational model, not EVM execution, a deployed fix or an exploit replay.**

## Invariant and distinct objective

Reject nested entry while allowing a later independent call in the same transaction. Reverted frames restore their entry checkpoint, including descendant writes.

Lab11 concerns payment settlement order. This lab instead models transaction-wide scratch state, nested checkpoints, shared-owner locks and multicall composability.

## Threat model and reproduction

Untrusted operations exercise the broken paths. Frame construction, schema inputs and governance are trusted fixtures except where tests intentionally mutate them.

Pinned runtime: CPython **3.12.14**. Standard library only; no RPC, wallets, dependencies or live transactions.

```sh
cd labs/15-transient-frame-lifetime
python3 --version
python3 -m unittest -v test_transient
```

October19,2026 local validation: **12 tests passed in 0.001s, exit0**. Timing is not a benchmark. Hosted CI is separate; see [validation](../../docs/VALIDATION.md).

Read [source](transient.py), [tests](test_transient.py), [exercise](EXERCISE.md) and [solution](SOLUTION.md).

## Assumptions and limits

Only transient dictionaries are modeled. No bytecode, gas, persistent balance ledger, STATICCALL implementation or opcode execution. Owner names are trusted inputs; this lab does not derive them from real call instructions. Frame snapshots trade memory for clarity and are not an efficient client implementation.

## Sources and provenance

Primary references inspected October19,2026:

- https://eips.ethereum.org/EIPS/eip-1153
- https://docs.soliditylang.org/en/v0.8.28/contracts.html#transient-storage

Original synthetic fixtures/tests; no implementation copied. References motivate the boundary, not certify the model. License remains unselected. No incident discovery, sole human authorship or production safety claim. [Article index](../../docs/ARTICLES.md).

