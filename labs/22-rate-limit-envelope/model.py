"""Integer token bucket; trusted monotonic time, fixed configuration."""
class Bucket:
    def __init__(self, capacity, rate, now=0):
        if any(type(v) is not int or v < 0 for v in (capacity,rate,now)) or capacity == 0:
            raise ValueError('invalid configuration')
        self.capacity, self.rate = capacity, rate
        self.tokens, self.last = capacity, now

    def consume(self, amount, now, guarded=True):
        if any(type(v) is not int or v < 0 for v in (amount,now)) or now < self.last:
            raise ValueError('invalid amount or clock')
        available=min(self.capacity,self.tokens+(now-self.last)*self.rate)
        if amount > available: raise ValueError('rate limit')
        self.tokens=available-amount
        # Omitting this update counts the same elapsed interval again.
        if guarded: self.last=now

class FixedWindow:
    """Negative comparison: per-window bounds are not rolling-window bounds."""
    def __init__(self, capacity, width):
        self.capacity,self.width=capacity,width
        self.window,self.used=-1,0

    def consume(self, amount, now):
        window=now//self.width
        used=self.used if window == self.window else 0
        if amount > self.capacity-used: raise ValueError('window full')
        self.window,self.used=window,used+amount
