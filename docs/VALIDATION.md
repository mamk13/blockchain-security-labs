# Validation record

## September 28, 2026: upgrade-intent extension

- CPython 3.12.14, standard library only; isolated local execution.
- `cd labs/02-upgrade-intent && python3 -m unittest -v test_upgrade`: **12 passed in 0.001s, exit 0**.
- `cd labs/01-backing-and-replay && python3 -m unittest -v fee_guard_example test_replay`: **14 passed in 0.017s, exit 0**. Original Lab 01 Python source retained.
- New tests cover action binding (six changed fields), readiness, cancellation, duplicate queueing, replay, role checks, domains, immutable arguments and invalid times. A separate test establishes that harmful approved code can still execute.
- No historical exploit replay or deployed remediation verified. No live financial transaction.
- A pinned-action CI workflow is included in this change. Its presence is not a successful hosted run. Consult the actual run tied to this commit; results observed later are recorded separately in the editorial action log.

Checkout v4.2.2 and setup-python v5.6.0 tag-to-commit references were read from their official GitHub repositories on September 28. CPython is pinned; the hosted runner image may change. No repository secrets are required. No tagged release created.

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
