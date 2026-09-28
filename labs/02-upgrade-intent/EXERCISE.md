# Exercise: the waiting period belongs to which bytes?

Run this synthetic scenario before reading the solution:

```python
from dataclasses import replace
from upgrade_model import Action, VulnerableQueue

approved = Action("lab-chain", "upgrade-gate", "vault", "code-A", b"{}", 1)
q = VulnerableQueue()
q.queue("p1", approved, now=100, delay=10)
q.execute("p1", replace(approved, code="code-B"), now=110)
assert q.applied == [approved]  # Expected to fail in this exercise.
```

1. Why does waiting until 110 fail to protect the reviewed code?
2. Fix the state binding, then test mutation of each field rather than only `code`.
3. Require rejection at 109, success at 110, and rejection of a second execution.
4. Verify the whole state remains unchanged on rejection, not only the output list.
5. Explain why cancellation should not silently reset the same proposal's identity.
6. Can an administrator above this queue replace the executor and bypass it? What evidence would you need to rule that out in a real deployment?

The failing assertion is a reader exercise, not a broken committed regression suite. The suite has a passing test that explicitly demonstrates this vulnerable behavior.
