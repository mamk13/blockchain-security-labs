# Canonical and finalized event acceptance

Invariant: only events matching a trusted canonical hash and finalized-height fixture create credit; accepted transaction/log pairs are consumed once. Threat model: submitter can supply stale/orphan event data and duplicate deliveries but cannot alter trusted fixture data. Negative control: guarded=False accepts an orphan.

Run from repository root: `python3 -m unittest discover -s labs/19-canonical-finality -v`. CPython3.12.14, stdlib only. Eight local tests passed October26. No hosted CI.

Limits: single chain/emitter; no consensus, receipt proof, signatures, provider authentication, durable transactions, concurrency or compensation. Python dataclasses are not adversarial ABI validation. Fixtures assume integer heights, string identifiers and valid event shape. A compromised fixture defeats the guard. This is not a bridge implementation.

Source: https://ethereum.org/developers/docs/consensus-mechanisms/pos/attack-and-defense/


Publication validation: October 29, 2026, CPython 3.12.14; eight local tests passed again. The October 26 result above is retained as provenance. Hosted CI is verified separately after publication.
