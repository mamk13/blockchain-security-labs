# Lab 18 — Atomic upgrade migration

**Educational model, not EVM execution, a deployed fix or an exploit replay.**

## Invariant and distinct objective

On migration rejection the complete modeled proxy state is unchanged; on success the new implementation and version agree while owner, balances and total are preserved.

Lab02 binds queued intent; Lab08 handles publishing initialized instances. This exercise starts with a live, populated v1 ledger and tests atomic upgrade-plus-migration, retries, and per-account preservation.

## Threat model and reproduction

Untrusted operations exercise the broken paths. Frame construction, schema inputs and governance are trusted fixtures except where tests intentionally mutate them.

Pinned runtime: CPython **3.12.14**. Standard library only; no RPC, wallets, dependencies or live transactions.

```sh
cd labs/18-atomic-upgrade-migration
python3 --version
python3 -m unittest -v test_migration
```

October19,2026 local validation: **10 tests passed in 0.000s, exit0**. Timing is not a benchmark. Hosted CI is separate; see [validation](../../docs/VALIDATION.md).

Read [source](migration.py), [tests](test_migration.py), [exercise](EXERCISE.md) and [solution](SOLUTION.md).

## Assumptions and limits

A synthetic v1-to-v2 policy, not UUPS/transparent-proxy code or arbitrary governance safety. Access control and code identity are string fixtures. Callback mutations outside proxy.state are not rolled back, demonstrated by a test. No EVM execution, concurrent access, reentrancy guard, event rollback or proof that malicious migration code is safe.

## Sources and provenance

Primary references inspected October19,2026:

- https://docs.openzeppelin.com/upgrades-plugins/writing-upgradeable
- https://eips.ethereum.org/EIPS/eip-1967

Original synthetic fixtures/tests; no implementation copied. References motivate the boundary, not certify the model. License remains unselected. No incident discovery, sole human authorship or production safety claim. [Article index](../../docs/ARTICLES.md).

