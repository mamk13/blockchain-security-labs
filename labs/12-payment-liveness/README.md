# Lab 12 — Payment liveness and failure isolation

**Educational model, not a production patch, standards implementation or exploit replay.**

## Invariant and threat model

One rejecting recipient must not prevent another recipient from collecting an independent allocation.

push_all is the all-or-nothing negative control. Independent claim calls allow Alice and Bob to collect even when Eve rejects. A rejection retains Eve's pending allocation, enabling a later retry. Cash equals the sum of unpaid claims.

## Reproduce

Pinned runtime: CPython **3.12.14**. Standard library only. No RPC, wallets, credentials or live transactions.

```sh
cd labs/12-payment-liveness
python3 --version
python3 -m unittest -v test_payments
```

October15,2026 local validation: **6 tests passed in 0.000s, exit0**, in an isolated suite process. Timing is one observation, not a benchmark. Hosted CI is separate; see [validation](../../docs/VALIDATION.md) and repository Actions.

Read [payments.py](payments.py), then [EXERCISE](EXERCISE.md) and [SOLUTION](SOLUTION.md). Tests include the negative control and state-preservation or conservation checks relevant to this boundary.

## Assumptions and limitations

The accepts callback is a trusted, side-effect-free fixture returning receiver acceptance; it is not an untrusted external call and must not reenter or mutate the distributor. See Lab11 for callback ordering. This lab models no gas limits, recipient authentication, token behavior, keeper incentives, expiry or production transaction engine. Pull payments shift execution cost and activity to recipients and do not force a permanently rejecting recipient to collect.

## Sources and provenance

Primary reference inspected October15,2026: [https://docs.soliditylang.org/en/latest/common-patterns.html#withdrawal-from-contracts](https://docs.soliditylang.org/en/latest/common-patterns.html#withdrawal-from-contracts). Solidity's withdrawal pattern motivates separation of recipient failures. The dictionary model is original and does not implement a contract.

Original synthetic model and deterministic tests. Historical validation elsewhere in this collection remains dated as originally run. No affected live deployment, incident transaction, loss or upstream fix is asserted. Repository license remains unselected. Article handoff: see [index](../../docs/ARTICLES.md); no publication URL is invented.
