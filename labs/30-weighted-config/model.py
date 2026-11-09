"""Atomic weighted-quorum configuration, with trusted administrator input."""
MAX = 2**64 - 1
def validate(weights, threshold):
    if (not weights or any(not isinstance(k, str) or not k for k in weights)
        or any(type(w) is not int or not 1 <= w <= MAX for w in weights.values())
        or type(threshold) is not int or not 1 <= threshold <= sum(weights.values()) <= MAX):
        raise ValueError("invalid configuration")
class Config:
    def __init__(self, weights, threshold):
        validate(weights, threshold)
        self.weights, self.threshold = dict(weights), threshold
    def replace(self, weights, threshold, *, vulnerable=False):
        if vulnerable:
            self.weights, self.threshold = dict(weights), threshold
            validate(self.weights, self.threshold)
        else:
            validate(weights, threshold)
            self.weights, self.threshold = dict(weights), threshold
    def approves(self, verified_signers):
        if len(verified_signers) != len(set(verified_signers)):
            return False
        if any(s not in self.weights for s in verified_signers):
            return False
        return sum(self.weights[s] for s in verified_signers) >= self.threshold
