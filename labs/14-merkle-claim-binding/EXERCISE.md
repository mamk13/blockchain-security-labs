# Exercise — Merkle claim binding and root rotation

Build a tree for Alice10 and Bob20. Substitute Eve for Alice under the omitted-account leaf. Repeat with the bound leaf. Then rotate Bob's allocation to30 while keeping Alice's consumed index.

Write the failing assertion before changing the negative control. Check both the returned outcome and every relevant ledger after rejection. Use only the local fixtures; do not connect a wallet or RPC.

Explain it yourself: what trusted input or omitted execution behavior could invalidate this model's conclusion in a deployed system?
