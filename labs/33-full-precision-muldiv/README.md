# Full-precision multiply/divide

Educational model, prepared November 12, 2026. Not an exploit replay, deployed patch or allegation about a referenced library.

## Invariant and threat model

For valid uint256 inputs and nonzero d, the accepted floor q satisfies q*d <= x*y < (q+1)*d. Ceiling has the corresponding upward bound. Reject if the selected result, not merely the intermediate product, exceeds uint256.

The adversary can choose operation inputs and timing within the documented model. Trusted state and source hooks are not attacker-controlled unless a test explicitly says so.

## Negative control and correction

Wrapping the product discards high bits. A checked 256-bit intermediate instead rejects some representable quotients. Dividing before multiplying loses remainder information.

Read `model.py`; deliberately vulnerable behavior is separately named. The tests exercise both the counterexample and the corrected boundary.

## Reproduce

Pinned runtime: CPython **3.12.14**, standard library only; no external dependencies or compiler.

```sh
cd labs/33-full-precision-muldiv
python3 --version
python3 -m unittest -v test_model
```

Ten tests; 4,624 small-domain triples, wide products, exact maximum result, zero denominator, divide-first precision loss and a ceiling-only overflow boundary.

Local validation November 12: ten tests passed, process exit 0. Hosted CI status is recorded separately in the editorial delivery; a local pass is not hosted CI.

## Exercise

See [EXERCISE.md](EXERCISE.md), then [SOLUTION.md](SOLUTION.md). Explain the invariant in your own words and identify a property the tests do not establish.

## Limits

Python arbitrary-precision arithmetic serves as the specification oracle. No 512-by-256 implementation, EVM, gas, Solidity compiler, fixed-point units, fees or economic policy is modeled. Selecting floor or ceiling is the caller's policy, not a universal safety rule.

## Sources and provenance

- Primary conceptual reference inspected November 12: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v5.4.0/contracts/utils/math/Math.sol
- Additional references: https://eips.ethereum.org/EIPS/eip-5805 and https://eips.ethereum.org/EIPS/eip-6372 (historical voting and clock semantics); https://docs.soliditylang.org/en/v0.8.30/types.html (arithmetic semantics).
- Original synthetic Python model and tests prepared with AI assistance for this collection. No upstream implementation copied. OpenZeppelin reference code is MIT licensed and Math credits Remco Bloemen/Uniswap; ERC texts carry CC0 notices. Those licenses do not automatically license this repository; no project license has been selected.
- Article handoff is manual publication only; no new Medium URL is claimed. See [article index](../../docs/ARTICLES.md).

