# Solution

Use OR for idempotent invalidation; check unused before consuming. Split nonce into word=nonce>>8 and bit=nonce&255. Namespace by owner. Failed validation must leave the bitmap unchanged.
