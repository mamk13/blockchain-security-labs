# Solution: preserve intent at the execution boundary

`VulnerableQueue` discards `approved_action`. It later trusts new data supplied by the executor. The proposal label proves only that some delay elapsed.

`BoundQueue` stores `(approved_action, ready_at)` and compares the full supplied action before applying it. `Action` is frozen and its argument field must be `bytes`; a frozen wrapper containing a mutable list would not provide the same property. The synthetic domain includes chain and executor identifiers. In a real implementation, use the platform's canonical encoding and bind all economically meaningful fields.

The order matters: check roles, pending state, action equality and time before changing any state. The model's effect only appends an action; it cannot fail or reenter. A real external migration must also preserve atomicity and handle failure without losing recovery options.

The tests do not prove that the action is beneficial. `test_delay_does_not_detect_malicious_approved_code` intentionally accepts harmful approved code after readiness. Token-vote capture, governance overrides and malicious implementations require separate defenses.

Explain it yourself: why is full payload binding necessary but insufficient? Which root authority can still replace the guard? When does a cancellation mechanism improve response, and when does it create a censorship or liveness risk?
