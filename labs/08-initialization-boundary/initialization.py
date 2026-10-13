"""Synthetic deployment lifecycle; no EVM storage, delegatecall or transactions."""
from dataclasses import dataclass


class Rejected(ValueError):
    pass


@dataclass
class Storage:
    owner: str | None = None
    initialized: bool = False


class Implementation:
    def __init__(self, locked=True, has_code=True):
        self.locked, self.has_code = locked, has_code
        self.storage = Storage()

    def initialize(self, storage, owner, direct=False):
        if not self.has_code:
            return  # Models an apparent successful call with no initialization effect.
        if direct and self.locked:
            raise Rejected('implementation locked')
        if storage.initialized or not isinstance(owner, str) or not owner.strip():
            raise Rejected('already initialized or invalid owner')
        storage.owner, storage.initialized = owner, True


class Proxy:
    def __init__(self, implementation):
        self.implementation = implementation
        self.storage = Storage()

    def initialize(self, owner):
        self.implementation.initialize(self.storage, owner)


class TwoStepFactory:
    """Vulnerable: an externally usable instance is registered before initialization."""
    def __init__(self):
        self.instances = {}

    def deploy(self, name, implementation):
        if name in self.instances:
            raise Rejected('duplicate instance')
        proxy = Proxy(implementation)
        self.instances[name] = proxy
        return proxy


class AtomicFactory(TwoStepFactory):
    """Corrected educational publication boundary, with a trusted intended owner input."""
    def deploy_initialized(self, name, implementation, intended_owner):
        if name in self.instances or not implementation.has_code or not implementation.locked:
            raise Rejected('duplicate or unsuitable implementation')
        candidate = Proxy(implementation)
        candidate.initialize(intended_owner)
        # A successful call is insufficient: verify the required storage result.
        if not candidate.storage.initialized or candidate.storage.owner != intended_owner:
            raise Rejected('initialization postcondition')
        self.instances[name] = candidate
        return candidate

    def deploy(self, name, implementation):
        raise Rejected('use deploy_initialized')
