# Exercise

Assume both observations individually satisfy a 60-second age limit. Is that sufficient for a derived price?

1. Run `python3 -m unittest -v test_oracle_guard`.
2. Temporarily remove the cross-feed skew rejection from `derive_price`.
3. Rerun `test_fresh_but_skewed_pair_is_rejected` and explain why two fresh values can still represent different market moments.
4. Change the quote feed from 6 decimals to 8 without changing its economic value. Predict which implementation changes its answer.
5. Explain why an application-specific `max_age` is still required even though `updatedAt` is returned.

Do not add a live RPC or real feed address. The goal is to reason about units and temporal policy in a deterministic model.
