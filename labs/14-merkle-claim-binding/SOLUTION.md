# Solution — Merkle claim binding and root rotation

Only the omitted-account tree accepts recipient substitution. The corrected leaf rejects it without consuming the index. Rotation preserves Alice's spent marker while Bob's unchanged allocation identity can claim the updated amount. Explain why clearing used on every root update creates a second payment opportunity.

The corrected path is intentionally narrow. Read the README assumptions before translating the invariant to another execution environment. A green local suite is evidence for these traces, not a security certification.
