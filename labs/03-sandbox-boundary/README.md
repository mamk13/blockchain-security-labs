# Lab 03 · Sandbox boundary

## Learning objective

Test the invariant: **untrusted guest execution cannot create a host-privileged effect**.

The vulnerable model puts a host-only mint operation in a dispatch table selected by guest input. The corrected model exposes only a namespaced write capability, validates the whole batch before mutation, and checks that rejected batches preserve all host state.

This is a deliberately small Python model inspired by the security boundary discussed in CWA-2026-006. It does not reproduce Wasmer code generation, native instruction execution, CosmWasm token accounting, consensus, or the upstream patch. It contains no deployable exploit.

## Runtime

- CPython 3.12.14
- Python standard library only
- No RPC, wallet, compiler toolchain, network request, or live transaction

## Run

```sh
cd labs/03-sandbox-boundary
python3 -m unittest -v test_sandbox
```

Read [EXERCISE.md](EXERCISE.md) first. Compare your reasoning with [SOLUTION.md](SOLUTION.md) after running the tests.

## Security boundary

The corrected model proves only the properties encoded by its ten tests. A production WebAssembly runtime must enforce memory, control-flow, import, syscall, JIT/compiler, and host-function boundaries at a much lower level. The verified upstream remediation is to upgrade to the patched `wasmd`/`wasmvm` release pair described by the official advisory; this lab is not an alternative.

## Scope and sources

This model assumes serialized execution, no concurrent mutation of the input list or public Python state, ordinary typed data, and successful in-memory writes. The guest/ prefix is a dictionary-key convention, not a filesystem path or per-contract identity boundary. Validation rejection is checked for unchanged state; memory exhaustion and unexpected failures during application are not transactional.

[Companion article](https://medium.com/@mamk13/a-smart-contract-sandbox-is-only-as-strong-as-its-compiler-boundary-e48ed3c01e61) · [Official CWA-2026-006 advisory](https://github.com/CosmWasm/advisories/blob/main/CWAs/CWA-2026-006.md).

Prepared October 5, 2026; publication prepared October 6. Original educational model, with AI assistance, maintained by Mohammad Khezer. No upstream source copied. See the repository provenance and validation records.
