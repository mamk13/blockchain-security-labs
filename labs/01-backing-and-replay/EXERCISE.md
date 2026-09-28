# Exercise: What does a valid request prove?

Before reading `SOLUTION.md`, answer these questions and run the existing tests.

1. Submit `Event("bitcoin-mainnet", "a" * 64, 0)` with deposit `100` and fee `1` twice to `VulnerableLedger`. Predict both return values and the final `issued` balance.
2. Repeat using `GuardedLedger`. Which state must remain unchanged after rejection?
3. Why does including a recipient in the consumption key risk accepting the same deposit twice? The current model intentionally has no recipient field.
4. Create two separate `GuardedLedger` instances and consume the same event in each. Does either lock provide a global guarantee?
5. How would restarting the process affect duplicate detection? Explain why serializing a set without a transaction is not a complete crash-recovery design.

Optional test extension: verify that malformed event input leaves both `issued` and `consumed` unchanged. Keep the suite offline and use synthetic events.

Review target: explain both the correction and the boundary where its guarantee stops. A passing example is insufficient if its assumptions do not match the deployed system.
