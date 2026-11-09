# Solution

Count unique authorized identities, not signature entries. This model rejects duplicate-containing bundles rather than silently deduplicating them. Different valid signatures from the same key still represent one identity.

## Explain it yourself

1. Which identity or unit is being counted?
2. What state is preserved on rejection?
3. Which trusted fixture would need independent validation in production?

Cryptography, key encoding/canonicalization, domain separation, nonce replay, contract-wallet dynamic validity and signer independence are outside this model. Member strings and validity booleans are trusted fixtures.
