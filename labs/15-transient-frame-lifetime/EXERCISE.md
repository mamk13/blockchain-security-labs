# Exercise — Transient frame lifetime

Replace Guard with EndOfTransactionOnlyGuard. Verify that reentry fails, then call it twice sequentially inside one transaction. Which test distinguishes a nesting guard from a one-call-per-transaction policy? Add a three-frame trace where the deepest call succeeds but its parent reverts.

Write the failing assertion first. Record the runtime, command and actual result. Explain which assumption your test depends on and which omitted behavior needs an integration test.

