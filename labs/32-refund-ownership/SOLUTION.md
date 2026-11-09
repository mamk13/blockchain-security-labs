# Solution

Alice owns a 6-unit refund, while 50 remain outside her allocation. Record that claim rather than assigning the whole asset balance. Clear the claim when the model withdraws it, so a second withdrawal pays zero.

## Explain it yourself

1. Which identity or unit is being counted?
2. What state is preserved on rejection?
3. Which trusted fixture would need independent validation in production?

Outcomes are trusted side-effect-free fixtures. No actual token/Ether call, recipient rejection, gas cost, reentrancy, sender authentication or relayer policy. Payer identity must come from authenticated funding context in an integration; user-controlled labels are not authentication.
