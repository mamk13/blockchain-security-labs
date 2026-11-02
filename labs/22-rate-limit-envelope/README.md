# Lab 22 — Rate-limit envelopes and refill checkpoints

Educational model, not a deployed patch, audit result or incident replay.

## Invariant

Tokens stay within [0,capacity]. Each successful consume accounts for elapsed time once and atomically commits token balance plus timestamp. Accepted volume over an interval is bounded by capacity + rate × elapsed time, not a fixed rolling cap.

## Threat model and negative control

Callers may split requests and repeat timestamps; clock and configuration are trusted. Omitting last=now is the negative control: the same elapsed interval refills twice. A fixed-window comparator accepts100 at time9 and100 at time10 for width10; this is expected fixed-window behavior, not evidence of a broken implementation.

## Reproduce

Pinned runtime: CPython **3.12.14**, standard library only. From repository root:

```sh
python3 --version
python3 -m unittest discover -s labs/22-rate-limit-envelope -v
```

November 2, 2026 local result: **10 tests passed in 0.001s, exit0**. Each suite ran in a separate process. Timing is not a benchmark. Hosted CI is recorded separately against the publication commit.

Read [model](model.py), [tests](test_model.py), [exercise](EXERCISE.md), and [solution](SOLUTION.md).

## Limits

Integer time and integer units only; no governance changes, decimal conversion, timestamps supplied by an attacker, concurrency, persistent storage, reorgs or economic calibration. One bucket only; per-user buckets do not imply a global cap. No CCIP or production limiter is implemented. FixedWindow is a narrow trusted-input counterexample, not a hardened alternative.

## Sources and provenance

Primary references inspected November 2, 2026:

- https://www.rfc-editor.org/rfc/rfc3290.html#appendix-A.4

Sources establish concepts, not certification of this model. Original synthetic code/tests prepared with AI assistance for Mohammad Khezer's maintained educational collection; no upstream implementation copied, no sole-human-authorship or original-discovery claim. No installed third-party dependency, RPC, wallet or live transaction. License remains unselected. [Article index](../../docs/ARTICLES.md).

