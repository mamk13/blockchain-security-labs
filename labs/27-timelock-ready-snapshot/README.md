# Timelock readiness snapshots

Changing the delay for future operations must not retroactively accelerate an already scheduled operation.

## Run

Pinned runtime: CPython 3.12.14, standard library only. No dependencies.

```sh
cd labs/27-timelock-ready-snapshot
python3 -m unittest -v test_model
```

Read [exercise](EXERCISE.md), predict the negative control, then inspect [solution](SOLUTION.md).

## Threat model and limits

Trusted monotonic integer clock and administrator fixture; no roles, governance voting, predecessors, hashes, callbacks or production TimelockController emulation. Operation IDs stand for immutable actions; cancellation makes an ID reusable in this teaching policy.

## Sources and provenance

Primary conceptual reference, inspected November 5, 2026: https://docs.openzeppelin.com/contracts/5.x/api/governance#TimelockController

Original AI-assisted educational implementation for this collection; no upstream code copied. No personal exploit discovery, incident replay, EVM execution or production validation claimed. Repository license remains unselected. See the dated validation note for actual test results; CI is separate.
