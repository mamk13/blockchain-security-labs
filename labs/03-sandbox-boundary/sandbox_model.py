"""Synthetic sandbox-boundary model; not Wasmer, wasmvm, or exploit code."""

from dataclasses import dataclass, field


class Rejected(ValueError):
    pass


@dataclass(frozen=True)
class GuestAction:
    operation: str
    target: str
    value: int


@dataclass
class HostState:
    bank_supply: int = 1_000_000
    guest_store: dict[str, int] = field(default_factory=dict)
    audit: list[str] = field(default_factory=list)


class VulnerableBoundaryModel:
    """Guest-selected dispatch accidentally includes a host-only effect."""

    def __init__(self):
        self.state = HostState()
        self._dispatch = {
            "guest_write": self._guest_write,
            "host_mint": self._host_mint,
        }

    def execute(self, actions):
        for action in actions:
            self._dispatch[action.operation](action)

    def _guest_write(self, action):
        self.state.guest_store[action.target] = action.value

    def _host_mint(self, action):
        self.state.bank_supply += action.value


class CapabilityBoundary:
    """Exposes one narrow guest capability and validates before mutation."""

    def __init__(self):
        self.state = HostState()

    @staticmethod
    def _validate(action):
        if type(action) is not GuestAction:
            raise Rejected("invalid action")
        if action.operation != "guest_write":
            raise Rejected("operation is outside the guest capability set")
        if type(action.target) is not str or not action.target.startswith("guest/"):
            raise Rejected("target is outside the guest namespace")
        if type(action.value) is not int or action.value < 0:
            raise Rejected("invalid value")

    def execute(self, actions):
        if type(actions) not in (list, tuple):
            raise Rejected("actions must be a fixed batch")
        # Validate the complete batch so a later rejection cannot leave a partial effect.
        for action in actions:
            self._validate(action)
        for action in actions:
            self.state.guest_store[action.target] = action.value
            self.state.audit.append(f"write:{action.target}")
