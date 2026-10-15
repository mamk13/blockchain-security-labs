# Lab 11 — Callback settlement ordering

**Educational model, not a production patch, standards implementation or exploit replay.**

## Invariant and threat model

At a recipient callback, the same claim must no longer be payable. A propagated failure restores the entire modeled ledger.

Vault(effects_first=False) is the negative control. The callback withdraws Alice's claim twice, spending cash that backs Bob. The corrected order clears the claim before transfer/callback. Tests also separate caught inner failure from propagated outer failure.

## Reproduce

Pinned runtime: CPython **3.12.14**. Standard library only. No RPC, wallets, credentials or live transactions.

```sh
cd labs/11-callback-settlement
python3 --version
python3 -m unittest -v test_settlement
```

October15,2026 local validation: **6 tests passed in 0.001s, exit0**, in an isolated suite process. Timing is one observation, not a benchmark. Hosted CI is separate; see [validation](../../docs/VALIDATION.md) and repository Actions.

Read [settlement.py](settlement.py), then [EXERCISE](EXERCISE.md) and [SOLUTION](SOLUTION.md). Tests include the negative control and state-preservation or conservation checks relevant to this boundary.

## Assumptions and limitations

This is sequential Python, not the EVM. Snapshot restoration is implemented explicitly and covers only claims, cash and received dictionaries; arbitrary callback side effects outside this ledger are not rolled back. It is not a general reentrancy guard or cross-function proof. Each owner name is a trusted identity fixture; no caller authorization is implemented.

## Sources and provenance

Primary reference inspected October15,2026: [https://docs.soliditylang.org/en/latest/security-considerations.html#reentrancy](https://docs.soliditylang.org/en/latest/security-considerations.html#reentrancy). Solidity security guidance motivates checks-effects-interactions. The model and rollback ledger are original teaching code, not Solidity execution.

Original synthetic model and deterministic tests. Historical validation elsewhere in this collection remains dated as originally run. No affected live deployment, incident transaction, loss or upstream fix is asserted. Repository license remains unselected. Article handoff: see [index](../../docs/ARTICLES.md); no publication URL is invented.
