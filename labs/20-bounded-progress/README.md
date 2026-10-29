# Bounded progress and checkpoint commits

Invariant: cursor and total represent exactly the committed prefix; each call processes at most min(limit,budget) fixed-cost jobs. Threat model: excessive backlog, caller-supplied invalid bounds and injected processing failure. Jobs are immutable nonnegative integer values. Negative control: all_at_once stalls when the remaining list exceeds budget.

Run from repository root: `python3 -m unittest discover -s labs/20-bounded-progress -v`. CPython3.12.14, stdlib only. Eight local tests passed October26. No hosted CI.

Limits: budget is abstract work units, not gas. No external callbacks, concurrent writers, durable storage, growing queue or keeper economics. A permanently failing job still blocks later jobs; the limitation test makes this explicit. Caller and job validation outside the stated fixture is not production-ready.

Source: https://docs.soliditylang.org/en/latest/security-considerations.html#gas-limit-and-loops


Publication validation: October 29, 2026, CPython 3.12.14; eight local tests passed again. The October 26 result above is retained as provenance. Hosted CI is verified separately after publication.
