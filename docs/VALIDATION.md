# Validation record

## September 28, 2026: publication preparation

- Runtime: CPython 3.12.14.
- Dependencies: Python standard library only.
- Working directory: `labs/01-backing-and-replay`.
- Command: `python3 -m unittest -v fee_guard_example test_replay`.
- Result: **14 tests passed in 0.021 seconds; exit code 0**.
- Execution: isolated local workspace; no live-chain transactions, RPC or wallet access.

Eight arithmetic tests include an exhaustive small domain and 10,000 seeded valid cases. Six replay tests cover duplicate inflation, rejection without state changes, invalid amounts before consumption, distinct outputs, malformed event identifiers and eight competing threads with one successful consumption.

This rerun does not establish signature validity, historical exploit reproduction, durable recovery, multi-process exclusion, distributed mint atomicity or production security. No GitHub Actions run is claimed for this publication.

## Original record

The September 21, 2026 artifact recorded 14 local passing tests in 0.017 seconds. The three Python files in this initial repository import retain those source bytes. Documentation and exercises were added for public navigation on September 28.
