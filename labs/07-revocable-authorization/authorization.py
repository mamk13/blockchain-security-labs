"""Synthetic authorization lifecycle model; not ERC-1271 or cryptography."""
from dataclasses import dataclass


class Rejected(ValueError):
    pass


@dataclass(frozen=True)
class Intent:
    domain: str
    recipient: str
    amount: int
    nonce: int
    deadline: int

    def __post_init__(self):
        if not self.domain or not self.recipient:
            raise Rejected('empty identity')
        if any(type(x) is not int for x in (self.amount, self.nonce, self.deadline)):
            raise Rejected('exact integers required')
        if self.amount <= 0 or self.nonce < 0 or self.deadline < 0:
            raise Rejected('invalid bound')


class WalletPolicy:
    """Trusted test fixture. grant/revoke stand in for authenticated wallet governance."""
    def __init__(self):
        self.grants = set()
        self.available = True

    def grant(self, intent, proof):
        self.grants.add((intent, proof))

    def revoke(self, intent, proof):
        self.grants.discard((intent, proof))

    def valid_now(self, intent, proof):
        if not self.available:
            raise Rejected('wallet unavailable')
        return (intent, proof) in self.grants


class CachedConsumer:
    """Vulnerable: admission-time validity becomes permanent execution authority."""
    def __init__(self, domain, wallet, balance=100):
        self.domain, self.wallet, self.balance = domain, wallet, balance
        self.cache, self.used, self.payments = set(), set(), {}

    def admit(self, intent, proof):
        if not self.wallet.valid_now(intent, proof):
            raise Rejected('invalid authorization')
        self.cache.add((intent, proof))

    def check(self, intent, now):
        if type(now) is not int or now < 0:
            raise Rejected('invalid clock')
        if intent.domain != self.domain or now > intent.deadline:
            raise Rejected('domain or deadline')
        if intent.nonce in self.used or intent.amount > self.balance:
            raise Rejected('nonce or balance')

    def execute(self, intent, proof, now):
        self.check(intent, now)
        if (intent, proof) not in self.cache:
            raise Rejected('not admitted')
        self.settle(intent)

    def settle(self, intent):
        # No external call occurs between these changes in this local model.
        self.used.add(intent.nonce)
        self.balance -= intent.amount
        self.payments[intent.recipient] = self.payments.get(intent.recipient, 0) + intent.amount


class CurrentConsumer(CachedConsumer):
    """Corrected for a policy requiring authorization at execution time."""
    def execute(self, intent, proof, now):
        self.check(intent, now)
        if not self.wallet.valid_now(intent, proof):
            raise Rejected('authorization no longer valid')
        self.settle(intent)
