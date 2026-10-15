# Solution — Domain-separated permits

Reject every changed domain before consuming anything. Consume the original context nonce exactly once. Two explicitly authorized contexts can legitimately settle independently; domain separation should not invent global single-use semantics.

The corrected path is intentionally narrow. Read the README assumptions before translating the invariant to another execution environment. A green local suite is evidence for these traces, not a security certification.
