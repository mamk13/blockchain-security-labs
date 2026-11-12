# Closed checkpoint history

Educational model, prepared November 12, 2026. Not an exploit replay, deployed patch or allegation about a referenced library.

## Invariant and threat model

For a closed timepoint t, lookup returns the last value whose checkpoint key is <=t, or zero before any checkpoint. Writes use a trusted nondecreasing clock, coalesce within a tick and cannot change already closed historical answers.

The adversary can choose operation inputs and timing within the documented model. Trusted state and source hooks are not attacker-controlled unless a test explicitly says so.

## Negative control and correction

Selecting the first checkpoint at or after a query leaks a later value into an earlier interval. Checkpoints (3,10),(7,90) queried at 5 must give 10, not 90.

Read `model.py`; deliberately vulnerable behavior is separately named. The tests exercise both the counterexample and the corrected boundary.

## Reproduce

Pinned runtime: CPython **3.12.14**, standard library only; no external dependencies or compiler.

```sh
cd labs/35-checkpoint-history
python3 --version
python3 -m unittest -v test_model
```

Ten tests; gap/exact boundaries, same-tick replacement, current/future rejection, backward-clock rejection with unchanged state and recovery, zero/empty history, 41 lookup comparisons and uint48/uint208 boundaries.

Local validation November 12: ten tests passed, process exit 0. Hosted CI status is recorded separately in the editorial delivery; a local pass is not hosted CI.

## Exercise

See [EXERCISE.md](EXERCISE.md), then [SOLUTION.md](SOLUTION.md). Explain the invariant in your own words and identify a property the tests do not establish.

## Limits

advance and set are trusted fixture hooks, not authorized public contract methods. Sequential Python only; no chain finality, delegation, balances, consensus, gas or storage packing. Python private attributes are conventional, not an adversarial isolation boundary. A value of zero does not distinguish no checkpoint from a stored zero.

## Sources and provenance

- Primary conceptual reference inspected November 12: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v5.4.0/contracts/utils/structs/Checkpoints.sol
- Additional references: https://eips.ethereum.org/EIPS/eip-5805 and https://eips.ethereum.org/EIPS/eip-6372 (historical voting and clock semantics); https://docs.soliditylang.org/en/v0.8.30/types.html (arithmetic semantics).
- Original synthetic Python model and tests prepared with AI assistance for this collection. No upstream implementation copied. OpenZeppelin reference code is MIT licensed and Math credits Remco Bloemen/Uniswap; ERC texts carry CC0 notices. Those licenses do not automatically license this repository; no project license has been selected.
- Article handoff is manual publication only; no new Medium URL is claimed. See [article index](../../docs/ARTICLES.md).

