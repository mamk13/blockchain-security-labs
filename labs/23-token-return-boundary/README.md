# Lab 23 — Transfer-result acceptance and retained obligations

Educational model, not a deployed patch, audit result or incident replay.

## Invariant

Under the supported token fixture, an accepted payout must have an accepted transfer result. Rejected results preserve both the claim and the selected token ledger. Low-level call success is not application-level success.

## Threat model and negative control

The fixture returns true, false, empty, malformed or reverted outcomes. The negative control checks only call_ok, clearing an obligation after a false return without paying. The corrected path also requires code and either empty bytes or exactly a32-byte true word. The liar fixture intentionally returns true without moving funds, exposing the remaining trust assumption.

## Reproduce

Pinned runtime: CPython **3.12.14**, standard library only. From repository root:

```sh
python3 --version
python3 -m unittest discover -s labs/23-token-return-boundary -v
```

November 2, 2026 local result: **10 tests passed in 0.001s, exit0**. Each suite ran in a separate process. Timing is not a benchmark. Hosted CI is recorded separately against the publication commit.

Read [model](model.py), [tests](test_model.py), [exercise](EXERCISE.md), and [solution](SOLUTION.md).

## Limits

Not ABI decoding, EVM call execution, SafeERC20 parity or a universal token adapter. The strict return shape may differ from specific library releases. No callbacks, fees, rebases, allowances, arbitrary exceptions or malicious balanceOf. Selected dictionaries are explicitly restored; external side effects and actual transaction semantics are not modeled. A true result alone cannot establish receipt.

## Sources and provenance

Primary references inspected November 2, 2026:

- https://eips.ethereum.org/EIPS/eip-20
- https://docs.openzeppelin.com/contracts/5.x/api/token/erc20#SafeERC20

Sources establish concepts, not certification of this model. Original synthetic code/tests prepared with AI assistance for Mohammad Khezer's maintained educational collection; no upstream implementation copied, no sole-human-authorship or original-discovery claim. No installed third-party dependency, RPC, wallet or live transaction. License remains unselected. [Article index](../../docs/ARTICLES.md).

