"""Synthetic upgrade queue; not Neutron code or a deployed patch."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    chain: str
    executor: str
    target: str
    code: str
    arguments: bytes
    nonce: int


class Rejected(ValueError):
    pass


def validate(action):
    if type(action) is not Action:
        raise Rejected("invalid action")
    if any(type(v) is not str or not v for v in
           (action.chain, action.executor, action.target, action.code)):
        raise Rejected("invalid identity")
    if type(action.arguments) is not bytes:
        raise Rejected("arguments must be immutable bytes")
    if type(action.nonce) is not int or action.nonce < 0:
        raise Rejected("invalid nonce")


class VulnerableQueue:
    """Readiness is attached to a label, with no binding to the reviewed action."""

    def __init__(self):
        self.ready = {}
        self.applied = []

    def queue(self, proposal, approved_action, now, delay):
        self.ready[proposal] = now + delay

    def execute(self, proposal, supplied_action, now):
        if now < self.ready[proposal]:
            raise Rejected("too early")
        del self.ready[proposal]
        self.applied.append(supplied_action)


class BoundQueue:
    """Corrects payload substitution within a single-threaded teaching model."""

    def __init__(self, chain="lab-chain", executor="upgrade-gate", delay=10):
        if type(delay) is not int or delay <= 0:
            raise Rejected("positive delay required")
        self.chain, self.executor, self.delay = chain, executor, delay
        self.pending = {}
        self.used = set()
        self.applied = []

    @staticmethod
    def _time(now):
        if type(now) is not int or now < 0:
            raise Rejected("invalid time")

    def queue(self, caller, proposal, approved_action, now):
        self._time(now)
        validate(approved_action)
        if caller != "governor":
            raise Rejected("not proposer")
        if type(proposal) is not str or not proposal:
            raise Rejected("invalid proposal")
        if (approved_action.chain, approved_action.executor) != (self.chain, self.executor):
            raise Rejected("wrong execution domain")
        if proposal in self.used:
            raise Rejected("proposal already used")
        # Keep the full immutable action so the label cannot authorize new bytes.
        self.pending[proposal] = (approved_action, now + self.delay)
        self.used.add(proposal)

    def execute(self, caller, proposal, supplied_action, now):
        self._time(now)
        validate(supplied_action)
        if caller != "executor":
            raise Rejected("not executor")
        record = self.pending.get(proposal)
        if record is None:
            raise Rejected("not pending")
        approved, ready_at = record
        if supplied_action != approved:
            raise Rejected("action changed")
        if now < ready_at:
            raise Rejected("too early")
        # The synthetic effect cannot call back or fail after this point.
        del self.pending[proposal]
        self.applied.append(approved)

    def cancel(self, caller, proposal):
        if caller != "guardian" or proposal not in self.pending:
            raise Rejected("cannot cancel")
        del self.pending[proposal]
