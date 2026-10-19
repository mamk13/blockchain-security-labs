# Lab 16 — Code and storage context

**Educational model, not EVM execution, a deployed fix or an exploit replay.**

## Invariant and distinct objective

A delegated write changes the selected execution owner's storage, not the implementation's storage; sender identity and static context are tracked separately.

This is an execution-context regression exercise, not Lab08's first-initialization policy. A direct call and a delegate-style call can both return successfully while mutating different accounts.

## Threat model and reproduction

Untrusted operations exercise the broken paths. Frame construction, schema inputs and governance are trusted fixtures except where tests intentionally mutate them.

Pinned runtime: CPython **3.12.14**. Standard library only; no RPC, wallets, dependencies or live transactions.

```sh
cd labs/16-code-storage-context
python3 --version
python3 -m unittest -v test_context
```

October19,2026 local validation: **11 tests passed in 0.001s, exit0**. Timing is not a benchmark. Hosted CI is separate; see [validation](../../docs/VALIDATION.md).

Read [source](context.py), [tests](test_context.py), [exercise](EXERCISE.md) and [solution](SOLUTION.md).

## Assumptions and limits

Frames are explicit trusted fixtures. No opcodes, ABI, msg.value, balances, gas, precompiles, EIP-7702 authorization or actual proxy bytecode. Diagnostic traces retain failed frames; they are not receipt logs. Callers must pass static context explicitly for nested CALL in this toy API.

## Sources and provenance

Primary references inspected October19,2026:

- https://eips.ethereum.org/EIPS/eip-7
- https://eips.ethereum.org/EIPS/eip-1153

Original synthetic fixtures/tests; no implementation copied. References motivate the boundary, not certify the model. License remains unselected. No incident discovery, sole human authorship or production safety claim. [Article index](../../docs/ARTICLES.md).

