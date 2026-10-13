# Exercise

Before opening the solution:

1. Run the suite and identify the test that demonstrates the vulnerable effect.
2. Add a failing test in which a valid guest write is followed by a forbidden host operation. The first write must not survive.
3. Explain why validating each action immediately before applying it would violate that property.
4. Name three boundaries absent from this model that a real WebAssembly runtime must enforce.
5. Explain why restricting new contract uploads cannot neutralize attacker-controlled code that is already stored.

Do not extend this exercise into native-code execution or a chain exploit. The goal is to reason about the invariant and rejection semantics, not reproduce CWA-2026-006.
