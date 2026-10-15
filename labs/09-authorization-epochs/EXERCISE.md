# Exercise — Authorization epochs

Grant two permits for Alice and one for Bob. Cancel Alice, reissue her nonce under the new epoch, then try every old permit. Which state should a rejected old permit consume?

Write the failing assertion before changing the negative control. Check both the returned outcome and every relevant ledger after rejection. Use only the local fixtures; do not connect a wallet or RPC.

Explain it yourself: what trusted input or omitted execution behavior could invalidate this model's conclusion in a deployed system?
