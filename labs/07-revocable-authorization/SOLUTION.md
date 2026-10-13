# Solution

The vulnerable consumer pays 10 and falls to 90; the corrected consumer retains 100 after revocation. The cache records what was valid at admission, not what is authorized at execution. CurrentConsumer checks the wallet again and rejects before consuming a nonce or changing accounting.

To solve exercise 4: revoke (intent, proof-A), grant (intent, proof-B), snapshot accounting, assert A rejects unchanged, execute B, then assert a B retry rejects unchanged. The used nonce applies to the intent's execution, not the proof bytes.

Regrant is deliberately allowed before execution: a wallet can decide that the same pair is valid again. If revocation must be permanent, it needs a separate cancellation/epoch rule. Rechecking a boolean cannot invent that policy.

Trade-off: live validation preserves current authority but adds wallet availability as an execution dependency. An irrevocable accepted-order design may be legitimate; it needs explicit commitment semantics and tests, rather than accidentally obtaining that behavior from a stale cache.

This solution is a local teaching correction. It does not prove the safety of a deployed consumer or of external calls after validation.

