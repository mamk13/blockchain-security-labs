# Lab 13 — Received-amount credit

**Educational model, not a production patch, standards implementation or exploit replay.**

## Invariant and threat model

Deposit credit must equal the observed positive vault balance increase, subject to the depositor's minimum, under the supported token assumptions.

Vault(measure_received=False) credits the requested amount and is the negative control. A 100-unit request with a 1% fixture fee receives99 but credits100. The corrected path credits99. It also checks false returns, donation exclusion and minimum-received failure.

## Reproduce

Pinned runtime: CPython **3.12.14**. Standard library only. No RPC, wallets, credentials or live transactions.

```sh
cd labs/13-received-amount-credit
python3 --version
python3 -m unittest -v test_deposits
```

October15,2026 local validation: **8 tests passed in 0.000s, exit0**, in an isolated suite process. Timing is one observation, not a benchmark. Hosted CI is separate; see [validation](../../docs/VALIDATION.md) and repository Actions.

Read [deposits.py](deposits.py), then [EXERCISE](EXERCISE.md) and [SOLUTION](SOLUTION.md). Tests include the negative control and state-preservation or conservation checks relevant to this boundary.

## Assumptions and limitations

This token is a transparent, non-rebasing, synchronous integer-unit fixture. Balance readings are honest; no callbacks, concurrent transfers, elastic supply, malicious balanceOf, ERC-777 hooks or outbound fees are supported. This is not SafeERC20 and does not claim support for every token bearing an ERC-20 interface. Rollback explicitly restores the fixture balances and vault credits; Python exceptions alone do not provide blockchain atomicity.

## Sources and provenance

Primary reference inspected October15,2026: [https://eips.ethereum.org/EIPS/eip-20](https://eips.ethereum.org/EIPS/eip-20). ERC-20 requires callers to handle false returns. Fee-on-transfer is an explicit synthetic extension here, not a claim that standard compliance guarantees this behavior.

Original synthetic model and deterministic tests. Historical validation elsewhere in this collection remains dated as originally run. No affected live deployment, incident transaction, loss or upstream fix is asserted. Repository license remains unselected. Article handoff: see [index](../../docs/ARTICLES.md); no publication URL is invented.
