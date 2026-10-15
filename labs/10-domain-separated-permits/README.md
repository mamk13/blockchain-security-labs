# Lab 10 — Domain-separated permits

**Educational model, not a production patch, standards implementation or exploit replay.**

## Invariant and threat model

A grant for one chain, verifier and schema must not authorize another context. A correct domain still needs local replay consumption.

Consumer with bind_domain=False is the negative control. The corrected Consumer matches the entire (Domain, Order) pair and consumes a nonce scoped to that consumer. Authority is a trusted grant fixture; an untrusted submitter may mutate or replay an Order.

## Reproduce

Pinned runtime: CPython **3.12.14**. Standard library only. No RPC, wallets, credentials or live transactions.

```sh
cd labs/10-domain-separated-permits
python3 --version
python3 -m unittest -v test_domains
```

October15,2026 local validation: **7 tests passed in 0.000s, exit0**, in an isolated suite process. Timing is one observation, not a benchmark. Hosted CI is separate; see [validation](../../docs/VALIDATION.md) and repository Actions.

Read [domains.py](domains.py), then [EXERCISE](EXERCISE.md) and [SOLUTION](SOLUTION.md). Tests include the negative control and state-preservation or conservation checks relevant to this boundary.

## Assumptions and limitations

This uses Python tuple equality, not hashing, signatures, EIP-712 ABI encoding or address validation. It does not prove fork safety, cross-chain synchronization or upgrade safety. Changing a schema version is a policy decision. Constructor inputs and authority grants are trusted; consumers have separate nonce stores.

## Sources and provenance

Primary reference inspected October15,2026: [https://eips.ethereum.org/EIPS/eip-712](https://eips.ethereum.org/EIPS/eip-712). EIP-712 supplies typed-data/domain context; its specification explicitly leaves replay protection to applications. No standard implementation is copied.

Original synthetic model and deterministic tests. Historical validation elsewhere in this collection remains dated as originally run. No affected live deployment, incident transaction, loss or upstream fix is asserted. Repository license remains unselected. Article handoff: see [index](../../docs/ARTICLES.md); no publication URL is invented.
