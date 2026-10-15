# Solution — Authorization epochs

A rejection consumes nothing. Only the newly granted generation and Bob's unaffected permit remain eligible. Monotonic epochs avoid resurrecting older authorizations; including the epoch in the replay key deliberately allows fresh nonce reuse. Explain why resetting the counter would break the policy.

The corrected path is intentionally narrow. Read the README assumptions before translating the invariant to another execution environment. A green local suite is evidence for these traces, not a security certification.
