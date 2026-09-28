# Blockchain Security Labs

Practical blockchain security exercises maintained by Mohammad Khezer. Each lab connects a security invariant to a small executable model, a deliberately vulnerable implementation, a correction, and regression tests.

These are educational models. They are not audited production components, deployed protocol patches, or historical exploit reproductions unless a lab explicitly establishes that evidence.

## Start here

| Lab | Question | Runtime |
| --- | --- | --- |
| [01 · Backing and replay](labs/01-backing-and-replay/README.md) | Can two valid mint requests consume the same deposit? | CPython 3.12.14; standard library only |
| [02 · Upgrade intent](labs/02-upgrade-intent/README.md) | Does execution preserve the exact queued action? | CPython 3.12.14; standard library only |

```sh
cd labs/01-backing-and-replay
python3 -m unittest -v fee_guard_example test_replay
```

September 28, 2026: Lab 01 passed 14 local tests; Lab 02 passed 12. See [validation](docs/VALIDATION.md) for the exact scope. A local pass is not a GitHub Actions result. The `Educational labs` workflow runs both suites without chain RPC, wallets or financial transactions; check the Actions tab for its actual status.

## Learn by changing a test

Read the [exercise](labs/01-backing-and-replay/EXERCISE.md), predict the result, run the suite, then compare your reasoning with the [solution](labs/01-backing-and-replay/SOLUTION.md). Explain why the model still fails across restarts before proposing production use.

## Articles and discussion

- [Article index and evidence boundaries](docs/ARTICLES.md)
- [Medium](https://medium.com/@mamk13)
- [LinkedIn](https://www.linkedin.com/in/mamk13/)

Each published article should reference an exact repository commit. New lessons will extend this collection with small, testable examples rather than duplicate projects.

## Contributing

Useful contributions include a failing regression test, a correction backed by primary evidence, or a clearer explanation of an assumption. Include your runtime, command, expected result and actual result. Use synthetic data and local execution; do not submit credentials or live attack instructions.

See [provenance](docs/PROVENANCE.md) and [security scope](SECURITY.md). An open-source license has not yet been selected; public visibility alone does not grant unrestricted reuse rights.
