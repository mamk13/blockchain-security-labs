"""Trusted policy fixture: generation-scoped grants, not signatures."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Permit:
    owner: str
    epoch: int
    nonce: int

class EpochPolicy:
    def __init__(self, enforce_epoch=True):
        self.epochs, self.grants, self.used = {}, set(), set()
        self.enforce_epoch = enforce_epoch

    def grant(self, owner, nonce):
        if not owner or type(nonce) is not int or nonce < 0:
            raise ValueError('invalid grant')
        permit = Permit(owner, self.epochs.get(owner, 0), nonce)
        self.grants.add(permit)
        return permit

    def cancel_all(self, owner):
        # Trusted owner action; generations never decrease or wrap in this model.
        self.epochs[owner] = self.epochs.get(owner, 0) + 1

    def execute(self, permit):
        if permit not in self.grants or permit in self.used:
            raise ValueError('unknown or consumed')
        if self.enforce_epoch and permit.epoch != self.epochs.get(permit.owner, 0):
            raise ValueError('cancelled generation')
        self.used.add(permit)

class GrantOnlyPolicy(EpochPolicy):
    """Negative control: cancellation advances state but execution ignores it."""
    def __init__(self):
        super().__init__(enforce_epoch=False)
