# Call gas forwarding bound

A requested child gas budget is not a delivered budget; check the capped allocation against a required minimum before recording success.

## Run

Pinned runtime: CPython 3.12.14, standard library only. No dependencies.

```sh
cd labs/28-call-gas-forwarding-bound
python3 -m unittest -v test_model
```

Read [exercise](EXERCISE.md), predict the negative control, then inspect [solution](SOLUTION.md).

## Threat model and limits

Arithmetic educational model, not an EVM gas estimator. Input available is gas after call overhead and memory expansion. Zero value only; excludes stipend, cold/warm costs, returned unused gas, execution and returndata. A boolean child-result fixture does not verify effects.

## Sources and provenance

Primary conceptual reference, inspected November 5, 2026: https://eips.ethereum.org/EIPS/eip-150

Original AI-assisted educational implementation for this collection; no upstream code copied. No personal exploit discovery, incident replay, EVM execution or production validation claimed. Repository license remains unselected. See the dated validation note for actual test results; CI is separate.
