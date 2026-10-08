# Solution

An independent age check is necessary but not sufficient. Two observations can each be recent relative to `now` while still being far apart from one another. A derived pair then combines different market moments.

The corrected model therefore enforces both:

- `now - updated_at <= max_age` for each input; and
- `abs(base.updated_at - quote.updated_at) <= max_skew` for the pair.

It also rescales each answer using that feed's declared decimals before division. Removing the skew gate should make `test_fresh_but_skewed_pair_is_rejected` fail. Ignoring decimals should make the six-decimal quote produce a result 100 times larger than the normalized result.

The trade-off is availability: tighter age and skew bounds reject more observations. A production design must define when to pause, use a validated fallback, or fail closed. This lab deliberately does not choose that policy for another protocol.
