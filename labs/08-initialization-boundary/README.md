# Lab 08 — Initialization publication boundary

**Educational lifecycle model, not a proxy, factory or deployed patch.**

Distinct learning objective: distinguish a one-time initializer guard from deploying an instance that is already initialized, and test initialization postconditions before registration. This is separate from Lab 02's queued upgrade payload binding.

## Reproduce

Pinned runtime: CPython **3.12.14**; standard library only.

```sh
cd labs/08-initialization-boundary
python3 --version
python3 -m unittest -v test_initialization
```

October 12, 2026 local result: **12 passed in 0.001s, exit 0**. No network, RPC, wallet or financial transaction.

## Invariant and examples

Every instance published in AtomicFactory.instances must already have the intended owner and an initialized flag. A rejected deployment leaves the registry unchanged. Implementation storage and proxy storage are modeled separately; locking the former does not initialize the latter.

- Vulnerable `TwoStepFactory` registers an uninitialized proxy; an attacker can win the first initialization call.
- Corrected `AtomicFactory` constructs privately, initializes, checks owner/flag, then registers. It rejects the inherited two-step entrypoint.
- Empty-code and no-op fixtures show why “the call returned successfully” is not an initialization postcondition.

The intended owner is a trusted input. The model does not authenticate who may select it: a real factory must define that policy. `locked` and `has_code` are fixture flags, not attestations of implementation safety. Malicious code can satisfy these narrow postconditions and remain malicious.

See [exercise](EXERCISE.md) and [solution](SOLUTION.md). Tests cover takeover, duplicate initialization, separate storage, missing code, no-op success, wrong owner, invalid owner, duplicate names and disabling the unsafe entrypoint.

## Sources and limits

[OpenZeppelin Initializable and proxy documentation](https://docs.openzeppelin.com/contracts/5.x/api/proxy#Initializable), inspected October 12, 2026, explains initializing a proxy during construction, locking implementation initializers, and clone calls to addresses without code. This model does not implement OpenZeppelin contracts or assume all release versions have identical constructor defaults. No OpenZeppelin dependency is installed.

No Solidity compilation, delegatecall, storage-slot verification, CREATE2, mempool race, actual chain transaction, upgrades or reinitializers are exercised. “Atomic” here means no registry-visible intermediate object in a sequential Python operation. It is not a database, thread-safety, crash recovery or EVM-wide rollback proof. Candidate-local mutation can occur before rejection; only the registry invariant is claimed.
