# Lab 01: One deposit, two valid requests

A deposit of 100 units and a fee of 1 authorize 99 units of issuance. Processing that deposit twice issues 198 units even though both individual amount checks pass.

## Invariants

- Amount: `0 <= fee < deposit` and `net = deposit - fee`.
- History: a source output authorizes at most one full consumption in this model.
- Rejection: an invalid or duplicate request leaves consumed events and issued balances unchanged.

The canonical event key is `(network, txid, output index)`. Recipient changes must not create fresh backing. Other protocols may require a different canonical source-event identity.

## Run

Use CPython **3.12.14**. There are no third-party dependencies or Solidity compiler requirements.

```sh
cd labs/01-backing-and-replay
python3 -m unittest -v fee_guard_example test_replay
```

- `fee_guard_example.py`: vulnerable arithmetic, bounded arithmetic, and eight tests.
- `replay_model.py`: a ledger without replay protection and a guarded in-memory ledger.
- `test_replay.py`: six regression tests, including eight synchronized competing threads.
- [Exercise](EXERCISE.md) and [solution](SOLUTION.md).

## What the guard establishes

Within one ledger instance, the lock covers the duplicate check, event consumption and balance update. Invalid amount validation happens before state mutation. The concurrency test checks one successful result and seven rejections.

## What it does not establish

Inputs are assumed authenticated. There is no signature verification, chain lookup, source finality, reorg handling, authorized fee policy or destination binding. The in-memory set disappears on restart and does not coordinate multiple processes. No external mint or durable transaction participates in the lock. Python integers do not model fixed-width overflow.

Canonical transaction formatting does not prove a transaction exists. Synthetic transaction IDs are not incident identifiers. Partial claims need remaining-balance accounting rather than this single-consumption policy.

This is not Symbiosis source, a Symbiosis patch, or evidence that replay caused that incident. See the [article index](../../docs/ARTICLES.md).
