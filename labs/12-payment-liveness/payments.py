"""Pull-versus-batch settlement; receiver acceptance is a side-effect-free fixture."""
class Distributor:
    def __init__(self, allocations):
        if not allocations or any(not k or type(v) is not int or v <= 0 for k,v in allocations.items()):
            raise ValueError('invalid allocation')
        self.pending = dict(allocations)
        self.cash, self.received = sum(allocations.values()), {}

    def claim(self, owner, accepts):
        amount = self.pending.get(owner,0)
        if amount == 0: raise ValueError('nothing pending')
        if not accepts(owner): raise ValueError('receiver rejected')
        self.pending[owner] = 0
        self.cash -= amount
        self.received[owner] = self.received.get(owner,0) + amount

    def push_all(self, accepts):
        # All recipients share one transaction in this negative control.
        snapshot = (self.pending.copy(),self.cash,self.received.copy())
        try:
            for owner,amount in list(self.pending.items()):
                if amount: self.claim(owner, accepts)
        except Exception:
            self.pending,self.cash,self.received = snapshot
            raise
