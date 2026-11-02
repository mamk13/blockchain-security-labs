# Solution and design trade-off

Retain the obligation on false, revert, malformed or no-code results. Permit an empty result only under the supported contract behavior assumption. Test false-after-write to show why outer rejection needs rollback of token state too. Do not call this an economic receipt proof; compare Lab13's different balance-delta boundary and its assumptions.

A passing model is a reproducible boundary argument, not production certification. Keep the negative control: it proves the suite can distinguish the intended failure.

