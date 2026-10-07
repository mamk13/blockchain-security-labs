# Solution notes

Release lines have different patched floors and different `wasmvm` pairings. A comparison against the oldest safe version answers the wrong question. The gate must select the node's maintained line first, then apply that line's pair.

Declared dependencies are build intent. The loaded-library check is runtime evidence. A stale static library can leave the running binary affected even when source metadata looks correct.

This model fails closed on unknown lines because the bundled matrix cannot establish their status. A real gate should refresh from a reviewed advisory source, retain the advisory revision and artifact checksums, and require an explicit policy update for a new line.

Useful audit evidence includes the source commit, dependency lock file, build command, compiler/toolchain version, binary checksum, signature, runtime query output, rollout height, validator adoption, and rollback decision.
