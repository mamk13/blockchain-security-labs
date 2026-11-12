"""Proposal policy over trusted historical-weight fixtures, not a token system."""
from types import MappingProxyType


class Proposal:
    def __init__(self, snapshot, *, clock_mode="blocknumber"):
        if type(snapshot) is not int or snapshot < 0:
            raise ValueError("invalid snapshot")
        if clock_mode not in ("blocknumber", "timestamp"):
            raise ValueError("unsupported clock")
        self.snapshot = snapshot
        self.clock_mode = clock_mode
        self.voted = set()
        self.total = 0

    def cast(self, voter, source, now):
        if type(now) is not int or now <= self.snapshot:
            raise ValueError("snapshot is not closed")
        if source.clock_mode != self.clock_mode:
            raise ValueError("clock mismatch")
        if voter in self.voted:
            raise ValueError("already voted")
        weight = source.past(voter, self.snapshot)
        # No marker is consumed until the trusted source supplied a valid weight.
        if type(weight) is not int or not 0 < weight < (1 << 256):
            raise ValueError("invalid or zero weight")
        if self.total + weight >= (1 << 256):
            raise ValueError("tally overflow")
        self.voted.add(voter)
        self.total += weight
        return weight


class VulnerableCurrent(Proposal):
    def cast(self, voter, source, now):
        if voter in self.voted:
            raise ValueError("already voted")
        weight = source.current[voter]
        self.voted.add(voter)
        self.total += weight
        return weight


class WeightFixture:
    def __init__(self, historical, current, clock_mode="blocknumber"):
        self._historical = MappingProxyType(dict(historical))
        self.current = dict(current)
        self.clock_mode = clock_mode

    def past(self, voter, snapshot):
        # Missing history is a source failure, not evidence of zero weight.
        return self._historical[(voter, snapshot)]
