# Solution and design trade-off

Commit both remaining credit and last-refill time after acceptance. Rejected calls leave the prior checkpoint intact; recomputing from it does not create extra credit because no spend was committed. The token-bucket envelope permits bursts and replenishment, unlike a rolling-window quota. Add governance transitions only with an explicit rule for retaining or clipping old credit.

A passing model is a reproducible boundary argument, not production certification. Keep the negative control: it proves the suite can distinguish the intended failure.

