"""Zero-fee integer AMM fixture, not a router or EVM implementation."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Intent:
    amount_in: int
    min_out: int
    deadline: int

class Pool:
    def __init__(self, x=1000, y=1000, wallet=100):
        if any(type(v) is not int or v <= 0 for v in (x, y, wallet)):
            raise ValueError('positive integer fixture required')
        self.x, self.y, self.wallet, self.received = x, y, wallet, 0

    def state(self):
        return self.x, self.y, self.wallet, self.received

    def execute(self, intent, now, guarded=True):
        a, minimum, deadline = intent.amount_in, intent.min_out, intent.deadline
        if any(type(v) is not int or v < 0 for v in (a, minimum, deadline, now)) or a == 0:
            raise ValueError('invalid intent')
        if a > self.wallet:
            raise ValueError('insufficient wallet input')
        out = a * self.y // (self.x + a)
        if guarded and (now > deadline or out < minimum):
            raise ValueError('expired or outside output bound')
        # All acceptance checks precede the selected state transition.
        self.x += a
        self.y -= out
        self.wallet -= a
        self.received += out
        return out
