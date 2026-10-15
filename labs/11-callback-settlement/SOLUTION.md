# Solution — Callback settlement ordering

Effects-first keeps Bob's backing intact in the successful attack trace. A propagated outer failure restores both nested and outer ledger effects. A caught inner failure restores the inner snapshot only. Explain which real external systems would lie outside this modeled rollback boundary.

The corrected path is intentionally narrow. Read the README assumptions before translating the invariant to another execution environment. A green local suite is evidence for these traces, not a security certification.
