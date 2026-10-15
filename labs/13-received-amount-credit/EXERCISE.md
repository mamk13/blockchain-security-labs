# Exercise — Received-amount credit

Deposit100 with fee_bps=100. Require min_received=100, then99. Compare Alice's debit, vault assets, fees and credits after each attempt. Add a donation before the deposit: should it increase Alice's credit?

Write the failing assertion before changing the negative control. Check both the returned outcome and every relevant ledger after rejection. Use only the local fixtures; do not connect a wallet or RPC.

Explain it yourself: what trusted input or omitted execution behavior could invalidate this model's conclusion in a deployed system?
