# Solution

Validate the proposed complete configuration before committing it. Reachability is arithmetic only: lost keys and correlated signers can still make an arithmetically valid quorum unavailable.

## Explain it yourself

1. Which identity or unit is being counted?
2. What state is preserved on rejection?
3. Which trusted fixture would need independent validation in production?

Trusted administrator; no governance access control, signatures, transaction rollback, concurrent calls or actual key availability. The API replaces the whole configuration, unlike upstream incremental methods.
