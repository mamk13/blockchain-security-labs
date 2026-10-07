# Lab 04 · Runtime version gate

## Learning objective

Turn a security advisory's release matrix into a fail-closed deployment check.

The vulnerable gate compares every component against one global minimum. That is wrong for parallel maintained release lines: `0.70.3` and `3.0.7` both appear numerically newer than the oldest safe pair while remaining affected according to CWA-2026-006.

The corrected gate verifies:

1. the `wasmd` line appears in the advisory matrix;
2. `wasmd` meets that line's patched floor;
3. `wasmvm` belongs to the required line and meets its floor; and
4. the library loaded at runtime exactly matches the declared dependency.

## Runtime

- CPython 3.12.14
- Python standard library only
- Advisory matrix transcribed from CWA-2026-006 as published September 28, 2026

## Run

```sh
cd labs/04-runtime-version-gate
python3 -m unittest -v test_version_gate
```

This is an educational deployment-policy model, not an updater, package scanner, Wasmer patch, or proof that a node is secure. Production operators should follow the official advisory and query the actual runtime with their chain binary.

## Scope and sources

The gate evaluates only the supplied version manifest against the advisory matrix. It does not inspect a binary, verify package provenance, attest a running process, or prove that every dependency is patched.

[Companion article](https://medium.com/@mamk13/a-smart-contract-sandbox-is-only-as-strong-as-its-compiler-boundary-e48ed3c01e61) · [Official CWA-2026-006 advisory](https://github.com/CosmWasm/advisories/blob/main/CWAs/CWA-2026-006.md).

Prepared October 5, 2026; published October 7, 2026. Original educational model, with AI assistance, maintained by Mohammad Khezer. No upstream source copied.
