"""Synthetic canonical-chain fixture; no consensus verification or RPC."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Event:
    height: int
    block_hash: str
    tx: str
    index: int
    recipient: str
    amount: int

class Ledger:
    def __init__(self):
        self.credits = {}
        self.consumed = set()

    def accept(self, event, canonical, finalized, guarded=True):
        if event.amount <= 0:
            raise ValueError('positive amount required')
        if guarded and (event.height > finalized or canonical.get(event.height) != event.block_hash):
            raise ValueError('not canonical and finalized')
        # The fixture has one chain and emitter; production keys must bind both.
        key = (event.tx, event.index)
        if key in self.consumed:
            raise ValueError('already consumed')
        self.credits[event.recipient] = self.credits.get(event.recipient, 0) + event.amount
        self.consumed.add(key)

