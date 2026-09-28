# Lab 02: bind the upgrade to the reviewed action

Runtime: **CPython 3.12.14**, standard library only. No Solidity compiler or CosmWasm dependency is used.

This is an original educational state-machine model, not a Neutron exploit replay, protocol implementation or upstream patch. The September 22, 2026 Neutron governance incident motivates reviewing administrative authority; **payload substitution has not been established as its root cause**.

## Threat model and invariant

The toy governor submits an already-approved action; an executor may try to substitute its target, code, arguments, nonce or execution domain. Callers and time are trusted harness inputs standing in for authenticated chain context. The model assumes serialized execution and no direct edits to its Python fields.

An executed action must equal the queued action, its review delay must have elapsed, and the proposal must remain pending. Rejection must leave every field unchanged.

`VulnerableQueue` keeps only a proposal label and readiness time. `BoundQueue` stores a frozen action containing immutable bytes. It checks full equality before changing state. Production contracts usually use a domain-separated commitment over canonical encoded data instead; this model deliberately avoids claiming compatibility with an ABI or signature scheme.

## Run locally

```sh
cd labs/02-upgrade-intent
python3 --version
python3 -m unittest -v test_upgrade
```

September 28, 2026: **12 tests passed in 0.001s; exit 0**, CPython 3.12.14. See [validation](../../docs/VALIDATION.md) for other suites and hosted CI status.

The tests reproduce the deliberately vulnerable behavior and validate the correction for changed fields, readiness boundary, cancellation, replay, role separation, invalid time and mutable arguments. One test deliberately shows malicious approved code still executing after the delay. That test passes because it documents a limitation, not because the code became safe.

## Limits and design trade-offs

- No token voting, snapshotting, quorum, signatures, actual bytecode, balances, external calls, chain RPC, wallets or historic fork.
- No persistence, parallel execution, reentrancy, transaction rollback or crash recovery. Python strings are not authentication and the caller supplies time.
- No delay reconfiguration, role changes or emergency bypass. Adding any creates new authority paths requiring review.
- A malicious governor can still approve harmful operations. A guardian can censor operations. A delay needs functioning monitoring and a feasible response or exit route.
- Proposal IDs cannot be reused, including after cancellation. A new reviewed attempt needs a fresh ID. Production replay domains and operation identities require explicit design.

## Read and explain

[Exercise](EXERCISE.md) · [Solution](SOLUTION.md)

Primary background: [Cosmos Labs response update, Sep 25](https://forum.cosmos.network/t/neutron-governance-attack-cosmos-hub-response-and-recovery-update/17369) and [OpenZeppelin access control documentation](https://docs.openzeppelin.com/contracts/5.x/access-control). These sources inform the discussion, but their code was not copied into this model. OpenZeppelin is not a dependency. New Medium article: draft delivered September 28; published URL pending. Existing [article index](../../docs/ARTICLES.md).

Code authored for this educational collection on September 28, 2026. Maintained by Mohammad Khezer. No claim of discovering this failure in a deployed system. Repository license remains unselected; retain attribution.
