"""Sequential integer allowance model, not an ERC-20 implementation."""
class Allowance:
    def __init__(self):
        self.balance = 1000
        self.received = 0
        self.allowance = 100

    def spend(self, amount):
        if type(amount) is not int or amount <= 0:
            raise ValueError("amount")
        if amount > min(self.allowance, self.balance):
            raise ValueError("insufficient")
        self.allowance -= amount
        self.balance -= amount
        self.received += amount

    def replace(self, amount, expected=None):
        if type(amount) is not int or amount < 0:
            raise ValueError("amount")
        # An expected value detects stale state, not an ABA history.
        if expected is not None and self.allowance != expected:
            raise ValueError("stale")
        self.allowance = amount
