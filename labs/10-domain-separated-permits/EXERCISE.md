# Exercise — Domain-separated permits

Authorize an order for chain1/vault-A/pay-v1. Change only one domain dimension at a time. Then replay it in the original context. Explain why a nonce alone cannot protect a separate consumer with fresh storage.

Write the failing assertion before changing the negative control. Check both the returned outcome and every relevant ledger after rejection. Use only the local fixtures; do not connect a wallet or RPC.

Explain it yourself: what trusted input or omitted execution behavior could invalidate this model's conclusion in a deployed system?
