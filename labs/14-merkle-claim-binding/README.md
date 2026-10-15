# Lab 14 — Merkle claim binding and root rotation

**Educational model, not a production patch, standards implementation or exploit replay.**

## Invariant and threat model

The proven leaf must bind campaign, allocation index, recipient and amount; root rotation must preserve consumed indices within the campaign.

The negative control omits account from the leaf and allows the submitter to redirect the allocation. The corrected two-leaf tree binds all four fields. Relaying is allowed, but payment always goes to the bound account. Root administration is trusted.

## Reproduce

Pinned runtime: CPython **3.12.14**. Standard library only. No RPC, wallets, credentials or live transactions.

```sh
cd labs/14-merkle-claim-binding
python3 --version
python3 -m unittest -v test_claims
```

October15,2026 local validation: **7 tests passed in 0.001s, exit0**, in an isolated suite process. Timing is one observation, not a benchmark. Hosted CI is separate; see [validation](../../docs/VALIDATION.md) and repository Actions.

Read [claims.py](claims.py), then [EXERCISE](EXERCISE.md) and [SOLUTION](SOLUTION.md). Tests include the negative control and state-preservation or conservation checks relevant to this boundary.

## Assumptions and limitations

This is a two-leaf SHA-256 tree with explicit leaf/node prefixes and JSON arrays, not Ethereum Keccak, ABI encoding, an OpenZeppelin MerkleProof implementation or a multiproof. The model records credits without real token transfers or funding checks. Arbitrary-depth proofs, duplicate-allocation validation, root governance, callbacks and concurrency are outside scope. Indices identify allocations permanently within one campaign; administrators must preserve that meaning across rotations.

## Sources and provenance

Primary reference inspected October15,2026: [https://docs.openzeppelin.com/contracts/5.x/api/utils/cryptography#MerkleProof](https://docs.openzeppelin.com/contracts/5.x/api/utils/cryptography#MerkleProof). OpenZeppelin documentation provides Merkle verification/encoding cautions as background. No source was copied and no OpenZeppelin package is installed.

Original synthetic model and deterministic tests. Historical validation elsewhere in this collection remains dated as originally run. No affected live deployment, incident transaction, loss or upstream fix is asserted. Repository license remains unselected. Article handoff: see [index](../../docs/ARTICLES.md); no publication URL is invented.
