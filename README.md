# Blockchain Security Labs

Practical blockchain security exercises maintained by Mohammad Khezer. Each lab connects a security invariant to a small executable model, a deliberately vulnerable implementation, a correction, and regression tests.

These are educational models. They are not audited production components, deployed protocol patches, or historical exploit reproductions unless a lab explicitly establishes that evidence.

## Start here

| Lab | Question | Runtime |
| --- | --- | --- |
| [01 · Backing and replay](labs/01-backing-and-replay/README.md) | Can two valid mint requests consume the same deposit? | CPython 3.12.14; standard library only |
| [02 · Upgrade intent](labs/02-upgrade-intent/README.md) | Does execution preserve the exact queued action? | CPython 3.12.14; standard library only |
| [03 · Sandbox boundary](labs/03-sandbox-boundary/README.md) | Can guest-controlled execution reach a host-privileged effect? | CPython 3.12.14; standard library only |
| [04 · Runtime version gate](labs/04-runtime-version-gate/README.md) | Does deployment prove the correct patched pair is actually loaded? | CPython 3.12.14; standard library only |
| [05 · Oracle age, skew and units](labs/05-oracle-age-skew-units/README.md) | Are derived-price inputs fresh, synchronized and normalized? | CPython 3.12.14; standard library only |
| [06 · Share accounting and rounding](labs/06-share-accounting-rounding/README.md) | Do previews, rounding and empty-vault accounting protect the caller? | CPython 3.12.14; standard library only |
| [07 · Revocable authorization](labs/07-revocable-authorization/README.md) | Can cached approval outlive current wallet authority? | CPython 3.12.14; standard library only |
| [08 · Initialization boundary](labs/08-initialization-boundary/README.md) | Is an instance fully initialized before it becomes available? | CPython 3.12.14; standard library only |

```sh
cd labs/01-backing-and-replay
python3 -m unittest -v fee_guard_example test_replay
```

See [validation](docs/VALIDATION.md) for dated commands, results, and limits. A local pass is not a GitHub Actions result. The `Educational labs` workflow runs all published suites without chain RPC, wallets or financial transactions; check the Actions tab for its actual status.

## Learn by changing a test

Read the [exercise](labs/01-backing-and-replay/EXERCISE.md), predict the result, run the suite, then compare your reasoning with the [solution](labs/01-backing-and-replay/SOLUTION.md). Explain why the model still fails across restarts before proposing production use.

## Articles and discussion

- [Article index and evidence boundaries](docs/ARTICLES.md)
- [Medium](https://medium.com/@mamk13)
- [LinkedIn](https://www.linkedin.com/in/mamk13/)

Each published article should reference an exact repository commit. New lessons will extend this collection with small, testable examples rather than duplicate projects.

## Contributing

Useful contributions include a failing regression test, a correction backed by primary evidence, or a clearer explanation of an assumption. Include your runtime, command, expected result and actual result. Use synthetic data and local execution; do not submit credentials or live attack instructions.

See [provenance](docs/PROVENANCE.md) and [security scope](SECURITY.md). An open-source license has not yet been selected; public visibility alone does not grant unrestricted reuse rights.



## Additional boundary exercises — October15,2026

| Lab | Learning objective |
|---|---|
| [09 — Authorization epochs](labs/09-authorization-epochs/README.md) | Epoch invalidation must permanently exclude older generations, even when a new permit reuses a nonce. |
| [10 — Domain-separated permits](labs/10-domain-separated-permits/README.md) | A grant for one chain, verifier and schema must not authorize another context. A correct domain still needs local replay consumption. |
| [11 — Callback settlement ordering](labs/11-callback-settlement/README.md) | At a recipient callback, the same claim must no longer be payable. A propagated failure restores the entire modeled ledger. |
| [12 — Payment liveness and failure isolation](labs/12-payment-liveness/README.md) | One rejecting recipient must not prevent another recipient from collecting an independent allocation. |
| [13 — Received-amount credit](labs/13-received-amount-credit/README.md) | Deposit credit must equal the observed positive vault balance increase, subject to the depositor's minimum, under the supported token assumptions. |
| [14 — Merkle claim binding and root rotation](labs/14-merkle-claim-binding/README.md) | The proven leaf must bind campaign, allocation index, recipient and amount; root rotation must preserve consumed indices within the campaign. |

## Execution and upgrade boundaries — October19,2026

| Lab | Learning objective |
|---|---|
| [15 — Transient frame lifetime](labs/15-transient-frame-lifetime/README.md) | Reject nested entry while allowing a later independent call in the same transaction. Reverted frames restore their entry checkpoint, including descendant writes. |
| [16 — Code and storage context](labs/16-code-storage-context/README.md) | A delegated write changes the selected execution owner's storage, not the implementation's storage; sender identity and static context are tracked separately. |
| [17 — Packed layout compatibility](labs/17-packed-layout-compatibility/README.md) | Every preexisting flat unsigned field keeps its slot, bit offset and width across an accepted schema extension, using stable field names as identity. |
| [18 — Atomic upgrade migration](labs/18-atomic-upgrade-migration/README.md) | On migration rejection the complete modeled proxy state is unchanged; on success the new implementation and version agree while owner, balances and total are preserved. |

## Event acceptance and bounded progress — October 29, 2026

- [19 — Canonical finality](labs/19-canonical-finality/README.md): distinguish observed events from trusted canonical/finalized eligibility before consuming replay keys.
- [20 — Bounded progress](labs/20-bounded-progress/README.md): bounded work and atomic prefix checkpoints; permanent poison jobs remain an explicit limitation.

These two models were prepared October 26 and first published October 29; do not count the rerun as two additional labs.
