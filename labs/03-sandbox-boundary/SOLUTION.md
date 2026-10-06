# Solution notes

The vulnerable model lets untrusted input choose `host_mint` because privileged and guest operations share one dispatch surface. The correction is an allowlisted capability boundary, not a blocklist of known-dangerous names.

The complete batch is validated before the first write. Therefore a forbidden second action cannot leave the permitted first action behind. The rejection tests compare all modeled state, including supply, guest storage, and audit records.

Missing production boundaries include native control flow, linear-memory isolation, imported host functions, operating-system access, compiler correctness, gas accounting, deterministic execution and consensus behavior. Passing this suite says nothing about those mechanisms.

Upload restrictions reduce reachability for newly supplied contracts, but the official advisory warns that already stored attacker code remains a path. Only the patched runtime removes the disclosed defect.
