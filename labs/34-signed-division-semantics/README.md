# Signed division semantics

Educational model, prepared November 12, 2026. Not an exploit replay, deployed patch or allegation about a referenced library.

## Invariant and threat model

The checked int256 quotient truncates toward zero; a=q*b+r, abs(r)<abs(b), and nonzero r has a's sign. Reject division by zero and MIN/-1. Mathematical floor is a separate explicitly selected policy.

The adversary can choose operation inputs and timing within the documented model. Trusted state and source hooks are not attacker-controlled unless a test explicitly says so.

## Negative control and correction

Python floor division is not Solidity signed division. For -5/2, Python gives quotient -3/remainder 1; the truncating model gives -2/-1.

Read `model.py`; deliberately vulnerable behavior is separately named. The tests exercise both the counterexample and the corrected boundary.

## Reproduce

Pinned runtime: CPython **3.12.14**, standard library only; no external dependencies or compiler.

```sh
cd labs/34-signed-division-semantics
python3 --version
python3 -m unittest -v test_model
```

Ten tests; all 6,480 nonzero-divisor pairs in [-40,40], all sign combinations, MIN/-1, int256 bounds, and large values that must not pass through floating point.

Local validation November 12: ten tests passed, process exit 0. Hosted CI status is recorded separately in the editorial delivery; a local pass is not hosted CI.

## Exercise

See [EXERCISE.md](EXERCISE.md), then [SOLUTION.md](SOLUTION.md). Explain the invariant in your own words and identify a property the tests do not establish.

## Limits

This models selected checked Solidity 0.8.30 integer semantics; it is not a compiler or differential test. No unchecked MIN/-1 wrapping, signed multiply/divide, decimal scaling, funding-rate accounting or economic fairness guarantee. Validating semantic agreement does not choose an application's rounding policy.

## Sources and provenance

- Primary conceptual reference inspected November 12: https://docs.soliditylang.org/en/v0.8.30/types.html#division
- Additional references: https://eips.ethereum.org/EIPS/eip-5805 and https://eips.ethereum.org/EIPS/eip-6372 (historical voting and clock semantics); https://docs.soliditylang.org/en/v0.8.30/types.html (arithmetic semantics).
- Original synthetic Python model and tests prepared with AI assistance for this collection. No upstream implementation copied. OpenZeppelin reference code is MIT licensed and Math credits Remco Bloemen/Uniswap; ERC texts carry CC0 notices. Those licenses do not automatically license this repository; no project license has been selected.
- Article handoff is manual publication only; no new Medium URL is claimed. See [article index](../../docs/ARTICLES.md).

