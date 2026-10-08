# Validation record

## October 8, 2026: Lab 05 preparation

CPython 3.12.14; standard library only; isolated local execution.

- Command: `cd labs/05-oracle-age-skew-units && python3 -m unittest -v test_oracle_guard`.
- Result: **12 passed in 0.001s, exit 0**.
- Full pre-publication rerun: Lab 01 **14 passed in 0.021s**; Lab 02 **12 passed in 0.001s**; Lab 03 **10 passed in 0.001s**; Lab 04 **10 passed in 0.001s**; Lab 05 **12 passed in 0.001s**. Every command exited 0.
- Scope: synthetic observations only; no RPC, wallet, live feed, network request or transaction.
- Limit: the model tests declared age, pairwise skew and decimal policies. It does not establish economic correctness, feed suitability or production safety.

## October 7, 2026: Lab 04 publication rerun

CPython 3.12.14; standard library only; isolated local execution.

- Lab 01: `cd labs/01-backing-and-replay && python3 -m unittest -v fee_guard_example test_replay`: **14 passed in 0.023s, exit 0**.
- Lab 02: `cd labs/02-upgrade-intent && python3 -m unittest -v test_upgrade`: **12 passed in 0.010s, exit 0**.
- Lab 03: `cd labs/03-sandbox-boundary && python3 -m unittest -v test_sandbox`: **10 passed in 0.001s, exit 0**.
- Lab 04: `cd labs/04-runtime-version-gate && python3 -m unittest -v test_version_gate`: **10 passed in 0.002s, exit 0**.
- Original October 5 Lab 04 validation: **10 passed in 0.001s**, CPython 3.12.14. The Python source is unchanged in this publication.
- Lab 04 covers all four patched advisory pairs, all four immediately affected pairs, declared-versus-loaded parity, wrong and unknown release lines, malformed versions, and the deliberately unsafe global-minimum comparison.
- The release-pair matrix was rechecked against the official CWA-2026-006 advisory at publication time.
- No Wasmer, wasmvm or wasmd compiler execution, binary attestation, native sandbox escape, RPC call, wallet interaction, historical exploit replay or live transaction occurred. This is an educational deployment-policy model, not an updater or upstream patch.
- The workflow includes Lab 04. Hosted CI is a separate result to verify against the exact published commit.

## October 6, 2026: Lab 03 publication rerun

CPython 3.12.14; standard library only; isolated local execution.

- Lab 01: `cd labs/01-backing-and-replay && python3 -m unittest -v fee_guard_example test_replay`: **14 passed in 0.016s, exit 0**.
- Lab 02: `cd labs/02-upgrade-intent && python3 -m unittest -v test_upgrade`: **12 passed in 0.001s, exit 0**.
- Lab 03: `cd labs/03-sandbox-boundary && python3 -m unittest -v test_sandbox`: **10 passed in 0.000s (reported timer precision), exit 0**.
- Original October 5 Lab 03 validation: **10 passed in 0.001s**, CPython 3.12.14. Its Python source is unchanged in this publication.
- Lab 03 tests privileged dispatch, allowed writes, namespace rejection, unknown operations, mixed-batch rejection preserving state, and invalid input/value types.
- No native sandbox escape, compiler execution, RPC call, wallet interaction, historical replay, or live transaction occurred. This is not an upstream patch.
- The workflow now includes Lab 03. Hosted CI is a separate result, to be verified against the published commit.

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
