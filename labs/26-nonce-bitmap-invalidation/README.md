# Monotone nonce bitmap invalidation

Invalidating a nonce repeatedly must never make it usable again; neighboring words and owners remain independent.

## Run

Pinned runtime: CPython 3.12.14, standard library only. No dependencies.

```sh
cd labs/26-nonce-bitmap-invalidation
python3 -m unittest -v test_model
```

Read [exercise](EXERCISE.md), predict the negative control, then inspect [solution](SOLUTION.md).

## Threat model and limits

Trusted owner argument and a boolean validation fixture replace real authentication. No signatures, token transfer or Permit2 implementation is provided. Python integers are explicitly bounded to uint256 for nonce and masks.

## Sources and provenance

Primary conceptual reference, inspected November 5, 2026: https://developers.uniswap.org/docs/protocols/permit2/concepts/signature-transfer

Original AI-assisted educational implementation for this collection; no upstream code copied. No personal exploit discovery, incident replay, EVM execution or production validation claimed. Repository license remains unselected. See the dated validation note for actual test results; CI is separate.
