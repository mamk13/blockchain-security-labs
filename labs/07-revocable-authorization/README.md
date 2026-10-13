# Lab 07 — Revocable authorization

**Educational model, not an ERC-1271 implementation, signature verifier or exploit replay.**

A contract wallet's authorization result may depend on current state. This lab compares admission-time caching with execution-time validation under a policy that requires current authority. It does not assert that all systems must invalidate previously accepted commitments.

## Reproduce

Pinned runtime: CPython **3.12.14**. Dependencies: standard library only; no installation, RPC, wallet or network required.

```sh
cd labs/07-revocable-authorization
python3 --version
python3 -m unittest -v test_authorization
```

October 12, 2026 local result: **12 tests passed in 0.001s, exit 0**. Hosted CI is recorded separately in the shared editorial log and Actions page.

## Threat model and invariant

The test fixture grants and revokes an exact immutable Intent/proof pair. An untrusted submitter can retain and resubmit an old proof, alter fields, or retry an intent. The fixture's grant/revoke functions represent trusted authenticated governance; they are not public production authorization APIs.

For the corrected model, settlement requires the domain, deadline, unused nonce, balance and **current wallet decision** to pass. Every rejection preserves balance, consumed nonces and payments. Deadline equality is accepted deliberately. Nonces are scoped to one wallet/consumer instance; there is no multi-wallet registry.

- `CachedConsumer`: vulnerable under this current-authority policy. A cached admission survives later revocation.
- `CurrentConsumer`: validates at execution, then settles without an intervening external call in the model.
- `WalletPolicy`: a set-membership fixture, **not cryptography**. A string called proof is only a test label.

Tests cover revocation, wallet unavailability and recovery, time boundaries, field mutation, different valid intents reusing a nonce, regrant, malformed numeric inputs and insufficient balance. The negative control proves the vulnerable path pays after revocation and the corrected path rejects the same scenario.

Read [EXERCISE](EXERCISE.md) before [SOLUTION](SOLUTION.md).

## Evidence and limitations

[ERC-1271](https://eips.ethereum.org/EIPS/eip-1271) permits context-dependent contract signature validation. [OpenZeppelin SignatureChecker documentation](https://docs.openzeppelin.com/contracts/5.x/api/utils/cryptography#SignatureChecker) explains that results may change across blocks. Sources inspected October 12, 2026; OpenZeppelin is a reference, not a dependency.

No ECDSA, EIP-712 encoding, magic-value decoding, gas, EVM rollback, reentrancy, chain reorganization, durable storage, cross-process atomicity or actual contract-wallet execution is implemented. Checks and settlement are sequential Python operations; the lab provides no concurrency guarantee. A real adapter must validate return data and failure modes and protect its settlement boundary.

Companion article: [Valid Yesterday, Revoked Today: Why Cached Authorization Is Not Execution Permission](https://mamk13.medium.com/valid-yesterday-revoked-today-why-cached-authorization-is-not-execution-permission-29d4030ac1f1), publication reported and URL supplied by the author; cross-link recorded October 13, 2026. Original synthetic code; no third-party source copied. Repository license remains unselected.

