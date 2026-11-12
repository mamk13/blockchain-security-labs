# Proposal-bound voting weights

Educational model, prepared November 12, 2026. Not an exploit replay, deployed patch or allegation about a referenced library.

## Invariant and threat model

Every accepted vote reads the same proposal-selected historical timepoint, only after it is closed and using matching clock units. Each voter is counted once per proposal. Source/weight/tally failures leave both tally and voter markers unchanged.

The adversary can choose operation inputs and timing within the documented model. Trusted state and source hooks are not attacker-controlled unless a test explicitly says so.

## Negative control and correction

Per-address duplicate protection alone permits reuse of current weight: Alice votes with 100, the fixture moves current weight to Bob, and Bob votes with the same 100. The negative control totals 200.

Read `model.py`; deliberately vulnerable behavior is separately named. The tests exercise both the counterexample and the corrected boundary.

## Reproduce

Pinned runtime: CPython **3.12.14**, standard library only; no external dependencies or compiler.

```sh
cd labs/36-proposal-vote-snapshot
python3 --version
python3 -m unittest -v test_model
```

Ten tests; reuse negative control, stable snapshot across current-weight changes, independent proposals, duplicate voter, activation boundary/retry, mismatched clocks, missing historical data/retry, invalid weights and tally overflow.

Local validation November 12: ten tests passed, process exit 0. Hosted CI status is recorded separately in the editorial delivery; a local pass is not hosted CI.

## Exercise

See [EXERCISE.md](EXERCISE.md), then [SOLUTION.md](SOLUTION.md). Explain the invariant in your own words and identify a property the tests do not establish.

## Limits

Historical delegated weights are trusted immutable fixtures, not computed token checkpoints. The model does not verify conservation, transfers, delegation, quorum, voting duration, signatures, governance execution, flash-loan resistance or snapshot fairness. The proposal snapshot is trusted configuration; Python object internals are not a security boundary. Rejecting zero weight is an explicit teaching policy, not an ERC requirement.

## Sources and provenance

- Primary conceptual reference inspected November 12: https://eips.ethereum.org/EIPS/eip-5805
- Additional references: https://eips.ethereum.org/EIPS/eip-5805 and https://eips.ethereum.org/EIPS/eip-6372 (historical voting and clock semantics); https://docs.soliditylang.org/en/v0.8.30/types.html (arithmetic semantics).
- Original synthetic Python model and tests prepared with AI assistance for this collection. No upstream implementation copied. OpenZeppelin reference code is MIT licensed and Math credits Remco Bloemen/Uniswap; ERC texts carry CC0 notices. Those licenses do not automatically license this repository; no project license has been selected.
- Article handoff is manual publication only; no new Medium URL is claimed. See [article index](../../docs/ARTICLES.md).

