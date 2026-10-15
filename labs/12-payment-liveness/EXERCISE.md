# Exercise — Payment liveness and failure isolation

Try a batch containing Alice, a rejecting Eve, and Bob. Then claim each independently. Add receiver recovery and verify that an earlier failure did not burn the allocation.

Write the failing assertion before changing the negative control. Check both the returned outcome and every relevant ledger after rejection. Use only the local fixtures; do not connect a wallet or RPC.

Explain it yourself: what trusted input or omitted execution behavior could invalidate this model's conclusion in a deployed system?
