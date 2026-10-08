# Lab 05 · Oracle age, skew and units

## Learning objective

Test the invariant: **a derived price is accepted only when every input is valid in its own units and the observations are temporally compatible**.

The vulnerable function divides two integer answers as though their decimals and update times match. The corrected model validates positive answers, explicit decimal ranges, future and stale timestamps, cross-feed update skew, and deterministic output scaling before returning a ratio.

This is an educational Python model. It is not a Chainlink adapter, deployed protocol patch, oracle recommendation, incident reconstruction, or proof that a price is economically safe.

## Runtime

- CPython 3.12.14
- Python standard library only
- No RPC, wallet, external feed, network request, or live transaction

## Run

```sh
cd labs/05-oracle-age-skew-units
python3 -m unittest -v test_oracle_guard
```

Read [EXERCISE.md](EXERCISE.md) before [SOLUTION.md](SOLUTION.md).

## Evidence boundary

Chainlink's EVM guide exposes `decimals()` and `latestRoundData()`, whose response includes `updatedAt`, and shows that two feeds can be combined to derive another denomination. The guide does not choose a universal maximum age or cross-feed skew for every protocol. Those are application policies that must reflect the feed, chain, market, fallback behavior, and consequence of rejection.

Primary reference: [Using Data Feeds on EVM Chains](https://docs.chain.link/data-feeds/using-data-feeds).

The lab does not model heartbeat/deviation configuration, phase transitions, L2 sequencer checks, market status, circuit breakers, fallback oracles, governance, or feed-address selection. Its `0..18` decimal limit is a deliberately narrow local policy, not a statement that all feeds use that range.
