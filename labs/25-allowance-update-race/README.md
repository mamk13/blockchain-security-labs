# Allowance update race

A stale allowance replacement must not silently create a fresh spending budget after an intervening spend.

## Run

Pinned runtime: CPython 3.12.14, standard library only. No dependencies.

```sh
cd labs/25-allowance-update-race
python3 -m unittest -v test_model
```

Read [exercise](EXERCISE.md), predict the negative control, then inspect [solution](SOLUTION.md).

## Threat model and limits

A compare-and-set extension is not ERC-20 approve. It detects a changed current value, not every intervening history (ABA). No mempool, signatures, fees or token callbacks are modeled.

## Sources and provenance

Primary conceptual reference, inspected November 5, 2026: https://eips.ethereum.org/EIPS/eip-20

Original AI-assisted educational implementation for this collection; no upstream code copied. No personal exploit discovery, incident replay, EVM execution or production validation claimed. Repository license remains unselected. See the dated validation note for actual test results; CI is separate.
