# Lab 21 — Execution-time price bounds

Educational model, not a deployed patch, audit result or incident replay.

## Invariant

A deadline is not an output bound. For a chosen input, accept only if now <= deadline and modeled output >= the caller's minimum. On rejection all four ledgers remain unchanged.

## Threat model and negative control

The adversary can alter the reserve fixture between quoting and execution; intent fields, pool identity, token units and the caller's authorization are trusted. guarded=False is the negative control. A 100-unit input against (1000,1000) returns90; against (2000,500) returns23. A fixed minimum90 rejects the latter.

## Reproduce

Pinned runtime: CPython **3.12.14**, standard library only. From repository root:

```sh
python3 --version
python3 -m unittest discover -s labs/21-execution-price-bounds -v
```

November 2, 2026 local result: **10 tests passed in 0.002s, exit0**. Each suite ran in a separate process. Timing is not a benchmark. Hosted CI is recorded separately against the publication commit.

Read [model](model.py), [tests](test_model.py), [exercise](EXERCISE.md), and [solution](SOLUTION.md).

## Limits

Zero-fee constant-product integer arithmetic only. No token calls, signatures, routers, fee-on-transfer behavior, reserve provenance, mempool simulation, MEV guarantee, oracle or EVM. Zero min_out intentionally provides no meaningful price protection. Positive input can round to zero output if the caller allows zero. Python integers do not model uint256 overflow.

## Sources and provenance

Primary references inspected November 2, 2026:

- https://github.com/Uniswap/v2-periphery/blob/master/contracts/UniswapV2Router02.sol

Sources establish concepts, not certification of this model. Original synthetic code/tests prepared with AI assistance for Mohammad Khezer's maintained educational collection; no upstream implementation copied, no sole-human-authorship or original-discovery claim. No installed third-party dependency, RPC, wallet or live transaction. License remains unselected. [Article index](../../docs/ARTICLES.md).

