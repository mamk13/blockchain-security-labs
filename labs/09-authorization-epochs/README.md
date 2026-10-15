# Lab 09 — Authorization epochs

**Educational model, not a production patch, standards implementation or exploit replay.**

## Invariant and threat model

Epoch invalidation must permanently exclude older generations, even when a new permit reuses a nonce.

GrantOnlyPolicy is the negative control: it advances the epoch but never checks it. EpochPolicy checks generation membership before consuming the permit. Trusted grant/cancel methods model authenticated owner actions. This is distinct from Lab07: it tests bulk cancellation scope and nonce reuse across monotonically increasing generations, not per-proof revocation.

## Reproduce

Pinned runtime: CPython **3.12.14**. Standard library only. No RPC, wallets, credentials or live transactions.

```sh
cd labs/09-authorization-epochs
python3 --version
python3 -m unittest -v test_epochs
```

October15,2026 local validation: **7 tests passed in 0.001s, exit0**, in an isolated suite process. Timing is one observation, not a benchmark. Hosted CI is separate; see [validation](../../docs/VALIDATION.md) and repository Actions.

Read [epochs.py](epochs.py), then [EXERCISE](EXERCISE.md) and [SOLUTION](SOLUTION.md). Tests include the negative control and state-preservation or conservation checks relevant to this boundary.

## Assumptions and limitations

No signatures, payment fields, EVM, durable storage, multi-process concurrency or integer overflow are modeled. Python integers do not wrap. A production bounded counter must prevent wraparound; access control over epoch changes is assumed here. A generation bump cancels all pending permits for that owner; that broad cancellation policy can be undesirable.

## Sources and provenance

Primary reference inspected October15,2026: [https://eips.ethereum.org/EIPS/eip-1271](https://eips.ethereum.org/EIPS/eip-1271). ERC-1271 provides contextual signature validity as background; it does not prescribe epochs. The epoch mechanism is an original policy exercise.

Original synthetic model and deterministic tests. Historical validation elsewhere in this collection remains dated as originally run. No affected live deployment, incident transaction, loss or upstream fix is asserted. Repository license remains unselected. Article handoff: see [index](../../docs/ARTICLES.md); no publication URL is invented.
