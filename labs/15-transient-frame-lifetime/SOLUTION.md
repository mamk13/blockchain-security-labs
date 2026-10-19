# Solution — Transient frame lifetime

Clear the lock after a successful guarded call, not only at transaction end. A reverted inner call restores the parent-held lock; propagated failure restores the earlier unlocked state. A successful child is not final if an ancestor later reverts. Clearing on successful return does not allow nested reentry because the callback runs while the lock is set.

Read the README limits before translating the pattern. Passing these traces is not a general safety proof.

