"""Sequential callback model with an explicit ledger transaction boundary."""
class Vault:
    def __init__(self, effects_first=True):
        self.claims = {'alice': 10, 'bob': 10}
        self.cash, self.received, self.depth = 20, {}, 0
        self.effects_first = effects_first

    def withdraw(self, owner, callback=lambda: None):
        amount = self.claims.get(owner, 0)
        if amount <= 0 or amount > self.cash: raise ValueError('no payable claim')
        snapshot = (self.claims.copy(), self.cash, self.received.copy())
        self.depth += 1
        try:
            if self.effects_first: self.claims[owner] = 0
            # Transfer is represented inside the same rollback ledger.
            self.cash -= amount
            self.received[owner] = self.received.get(owner, 0) + amount
            callback()
            if not self.effects_first: self.claims[owner] = 0
        except Exception:
            self.claims, self.cash, self.received = snapshot
            raise
        finally:
            self.depth -= 1
