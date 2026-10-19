# Lab 17 — Packed layout compatibility

**Educational model, not EVM execution, a deployed fix or an exploit replay.**

## Invariant and distinct objective

Every preexisting flat unsigned field keeps its slot, bit offset and width across an accepted schema extension, using stable field names as identity.

This lab tests data interpretation across versions rather than authorization to install code. Keeping the same number of storage words is not enough.

## Threat model and reproduction

Untrusted operations exercise the broken paths. Frame construction, schema inputs and governance are trusted fixtures except where tests intentionally mutate them.

Pinned runtime: CPython **3.12.14**. Standard library only; no RPC, wallets, dependencies or live transactions.

```sh
cd labs/17-packed-layout-compatibility
python3 --version
python3 -m unittest -v test_layout
```

October19,2026 local validation: **12 tests passed in 0.001s, exit0**. Timing is not a benchmark. Hosted CI is separate; see [validation](../../docs/VALIDATION.md).

Read [source](layout.py), [tests](test_layout.py), [exercise](EXERCISE.md) and [solution](SOLUTION.md).

## Assumptions and limits

Only sequential flat uint fields in byte-multiple widths are supported. No compiler parsing, inheritance, structs, arrays, mappings, signed values, storage gaps, ERC-7201 namespaces or custom base slots. Renames are conservatively rejected, although a reviewed semantic rename can be storage-compatible. This is not a production upgrade validator.

## Sources and provenance

Primary references inspected October19,2026:

- https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html
- https://docs.openzeppelin.com/upgrades-plugins/writing-upgradeable
- https://eips.ethereum.org/EIPS/eip-1967

Original synthetic fixtures/tests; no implementation copied. References motivate the boundary, not certify the model. License remains unselected. No incident discovery, sole human authorship or production safety claim. [Article index](../../docs/ARTICLES.md).

