"""Hashable authorization fixtures; deliberately not EIP-712 encoding."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Domain:
    chain: int
    verifier: str
    schema: str

@dataclass(frozen=True)
class Order:
    recipient: str
    amount: int
    nonce: int

class Authority:
    def __init__(self): self.grants = set()
    def grant(self, domain, order): self.grants.add((domain, order))

class Consumer:
    def __init__(self, domain, authority, bind_domain=True):
        self.domain, self.authority = domain, authority
        self.bind_domain = bind_domain
        self.used, self.credits = set(), {}

    def execute(self, order):
        if not order.recipient or type(order.amount) is not int or order.amount <= 0:
            raise ValueError('bad transfer')
        if type(order.nonce) is not int or order.nonce < 0 or order.nonce in self.used:
            raise ValueError('bad nonce')
        allowed = (self.domain, order) in self.authority.grants
        if not self.bind_domain:
            allowed = any(o == order for _, o in self.authority.grants)
        if not allowed: raise ValueError('wrong authority context')
        self.used.add(order.nonce)
        self.credits[order.recipient] = self.credits.get(order.recipient, 0) + order.amount
