# Lab 24 — Unambiguous intent field boundaries

Educational model, not a deployed patch, audit result or incident replay.

## Invariant

The selected byte-pair codec must be injective before hashing: distinct supported field pairs have distinct encodings. Decode accepts exactly two bounded fields with the declared prefix and no trailing bytes.

## Threat model and negative control

An attacker shifts bytes between two fields. packed(a,b) is the negative control: (a,bc) and(ab,c) become identical bytes. The corrected format is a constant version prefix plus two-byte lengths and raw byte fields. SHA-256 is only a digest fixture, not Ethereum Keccak or a signature implementation.

## Reproduce

Pinned runtime: CPython **3.12.14**, standard library only. From repository root:

```sh
python3 --version
python3 -m unittest discover -s labs/24-unambiguous-intent-encoding -v
```

November 2, 2026 local result: **10 tests passed in 0.005s, exit0**. Each suite ran in a separate process. Timing is not a benchmark. Hosted CI is recorded separately against the publication commit.

Read [model](model.py), [tests](test_model.py), [exercise](EXERCISE.md), and [solution](SOLUTION.md).

## Limits

Not Solidity ABI, EIP-712, cryptographic signature validation, a proof of hash collision resistance, chain/verifier domain separation, authorization or global replay protection. Fields are bytes, not normalized text. The length bound65535 is instructional. One local consumed flag provides single use only in that Approval instance.

## Sources and provenance

Primary references inspected November 2, 2026:

- https://docs.soliditylang.org/en/latest/abi-spec.html#non-standard-packed-mode
- https://eips.ethereum.org/EIPS/eip-712

Sources establish concepts, not certification of this model. Original synthetic code/tests prepared with AI assistance for Mohammad Khezer's maintained educational collection; no upstream implementation copied, no sole-human-authorship or original-discovery claim. No installed third-party dependency, RPC, wallet or live transaction. License remains unselected. [Article index](../../docs/ARTICLES.md).

