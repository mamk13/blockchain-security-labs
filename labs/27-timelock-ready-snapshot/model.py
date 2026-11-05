"""Ready-time policy model, not a governance controller."""
class Timelock:
    def __init__(self,delay=10,vulnerable=False):
        self.delay=delay; self.vulnerable=vulnerable
        self.pending={}; self.done=set(); self.now=0
    def tick(self,now):
        if type(now) is not int or now<self.now: raise ValueError("clock")
        self.now=now
    def set_delay(self,delay):
        if type(delay) is not int or delay<0: raise ValueError("delay")
        self.delay=delay
    def schedule(self,op):
        if op in self.pending or op in self.done: raise ValueError("duplicate")
        self.pending[op]=(self.now,self.now+self.delay)
    def cancel(self,op):
        if op not in self.pending: raise ValueError("missing")
        del self.pending[op]
    def execute(self,op):
        if op not in self.pending: raise ValueError("missing")
        queued,ready=self.pending[op]
        if self.vulnerable: ready=queued+self.delay
        if self.now<ready: raise ValueError("early")
        del self.pending[op]; self.done.add(op)
