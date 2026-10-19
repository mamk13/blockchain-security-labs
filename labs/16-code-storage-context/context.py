"""Explicit code/storage identities, not an EVM or an EIP-7702 implementation."""
from dataclasses import dataclass
from copy import deepcopy


@dataclass(frozen=True)
class Frame:
    code: str
    storage: str
    sender: str
    static: bool = False


class World:
    def __init__(self):
        self.slots = {}
        self.trace = []

    def read(self, owner, slot='value'):
        return self.slots.get((owner, slot), 0)

    def call(self, caller, target, program, static=False):
        return self.run(Frame(target, target, caller, static), program)

    def delegate(self, parent, implementation, program):
        return self.run(Frame(implementation, parent.storage, parent.sender,
                              parent.static), program)

    def run(self, frame, program):
        checkpoint = deepcopy(self.slots)
        self.trace.append(frame)
        try:
            return program(self, frame)
        except Exception:
            self.slots = checkpoint
            raise

    def set_value(self, frame, value):
        if frame.static:
            raise ValueError('static write')
        if type(value) is not int or not 0 <= value < 2**256:
            raise ValueError('not a uint256')
        self.slots[frame.storage, 'value'] = value


def write_42(world, frame):
    world.set_value(frame, 42)
    return frame.sender


def call_forwarder(world, frame, implementation):
    """Negative control when the specification requires delegated storage."""
    return world.call(frame.storage, implementation, write_42, frame.static)


def delegate_forwarder(world, frame, implementation):
    return world.delegate(frame, implementation, write_42)
