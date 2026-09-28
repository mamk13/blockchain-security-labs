# Solution notes

1. The vulnerable ledger returns `99` twice and records `198`. Per-request arithmetic does not account for earlier consumption.
2. The guarded ledger returns `99` once, then raises `ValueError`. Its balance remains `99`, and its consumed set still contains exactly one event.
3. A recipient is an authorization attribute, not fresh source backing. A new signed request for another recipient must still contend for the same underlying source event. Systems supporting multiple allocations need a conserved remaining-balance model.
4. Both independent instances can accept the event. Their locks and sets are separate. The model guarantees exclusion only within one instance.
5. Restarting clears the set. A production design needs durable, globally coordinated allocation, immutable authorization data and reconciliation with destination execution. Persisting a flag and minting are not automatically one transaction; failure between them needs explicit handling.

The key review question is: where does the system establish that this backing has not already been allocated, including during retries, concurrency, restarts and destination timeouts?

The existing suite tests arithmetic and local state behavior. It does not validate any proposed distributed or durable implementation.
