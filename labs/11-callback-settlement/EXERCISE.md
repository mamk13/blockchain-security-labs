# Exercise — Callback settlement ordering

Run the callback attack against both orders. After Alice's callback, can Bob withdraw? Then let Bob's nested withdrawal succeed and make the outer callback fail. What state must survive?

Write the failing assertion before changing the negative control. Check both the returned outcome and every relevant ledger after rejection. Use only the local fixtures; do not connect a wallet or RPC.

Explain it yourself: what trusted input or omitted execution behavior could invalidate this model's conclusion in a deployed system?
