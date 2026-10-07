# Exercise

1. Explain why one global semantic-version threshold is invalid across the four maintained release lines.
2. Add a regression case where `go.sum` declares a patched library but the running binary loads the previous affected library.
3. Decide whether an unknown future line should pass, warn, or fail. Defend the choice for an automated production gate.
4. Extend the model with an explicit advisory revision identifier so a stale matrix is detectable.
5. Describe which evidence, beyond version strings, you would retain for an upgrade audit.
