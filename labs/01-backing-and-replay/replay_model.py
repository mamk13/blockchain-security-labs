"""Educational single-process state machine, NOT bridge implementation."""
from dataclasses import dataclass
from threading import Lock
from fee_guard_example import checked_net

@dataclass(frozen=True)
class Event:
    network: str
    txid: str
    output: int

class VulnerableLedger:
    def __init__(self):
        self.issued = 0

    def consume(self, event, deposit, fee):
        amount = checked_net(deposit, fee)
        self.issued += amount
        return amount

class GuardedLedger:
    """Inputs assumed already authenticated; memory survives NO restart.

    Lock makes check/consume/account one local operation. No external calls.
    This models exactly one full consumption per source output.
    """
    def __init__(self):
        self.issued = 0
        self.consumed = set()
        self.lock = Lock()

    def consume(self, event, deposit, fee):
        if not isinstance(event, Event):
            raise TypeError("expected canonical event")
        if event.network not in ("bitcoin-mainnet", "bitcoin-testnet"):
            raise ValueError("unsupported network")
        if (type(event.txid) is not str or len(event.txid) != 64
                or any(c not in "0123456789abcdef" for c in event.txid)):
            raise ValueError("expected canonical lowercase hex txid")
        if type(event.output) is not int or not 0 <= event.output < 2**32:
            raise ValueError("invalid output index")
        amount = checked_net(deposit, fee)
        with self.lock:
            if event in self.consumed:
                raise ValueError("source event already consumed")
            self.consumed.add(event)
            self.issued += amount
        return amount
