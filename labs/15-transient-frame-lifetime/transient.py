"""Selected transient-state semantics; no bytecode, gas or chain execution."""
from contextlib import contextmanager
from copy import deepcopy


class Reverted(Exception):
    pass


class Transaction:
    def __init__(self):
        self.transient = {}
        self.active = False

    @contextmanager
    def transaction(self):
        if self.active:
            raise RuntimeError('nested transaction')
        self.active = True
        try:
            yield self
        finally:
            self.transient.clear()
            self.active = False

    @contextmanager
    def frame(self):
        if not self.active:
            raise RuntimeError('outside transaction')
        checkpoint = deepcopy(self.transient)
        try:
            yield
        except Exception:
            # A reverted parent must also undo successful descendant writes.
            self.transient = checkpoint
            raise

    def read(self, owner, slot):
        if not self.active:
            raise RuntimeError('outside transaction')
        return self.transient.get((owner, slot), 0)

    def write(self, owner, slot, value):
        if not self.active:
            raise RuntimeError('outside transaction')
        self.transient[owner, slot] = value


class Guard:
    def __init__(self, tx, owner='vault', clear_on_return=True):
        self.tx, self.owner = tx, owner
        self.clear_on_return = clear_on_return

    def call(self, callback=lambda: None):
        with self.tx.frame():
            if self.tx.read(self.owner, 'lock'):
                raise Reverted('nested entry')
            self.tx.write(self.owner, 'lock', 1)
            callback()
            if self.clear_on_return:
                self.tx.write(self.owner, 'lock', 0)


class EndOfTransactionOnlyGuard(Guard):
    """Negative control: blocks legitimate sequential calls in a multicall."""
    def __init__(self, tx, owner='vault'):
        super().__init__(tx, owner, clear_on_return=False)
