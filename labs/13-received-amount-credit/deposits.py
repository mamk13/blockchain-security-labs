"""Integer-unit token fixture with an explicit all-ledger rollback boundary."""
class Token:
    def __init__(self, fee_bps=0, succeeds=True):
        if type(fee_bps) is not int or not 0 <= fee_bps <= 10000: raise ValueError('fee')
        self.fee_bps, self.succeeds = fee_bps, succeeds
        self.balances = {'alice':1000,'vault':0,'fees':0}

    def transfer(self, owner, amount):
        if not self.succeeds: return False
        if amount > self.balances.get(owner,0): raise ValueError('insufficient')
        fee = amount * self.fee_bps // 10000
        self.balances[owner] -= amount
        self.balances['vault'] += amount-fee
        self.balances['fees'] += fee
        return True

class Vault:
    def __init__(self, token, measure_received=True):
        self.token, self.measure_received, self.credits = token, measure_received, {}

    def deposit(self, owner, requested, min_received=0):
        if owner in ('vault','fees') or not owner: raise ValueError('invalid depositor')
        if any(type(x) is not int for x in (requested,min_received)) or requested <= 0 or min_received < 0:
            raise ValueError('invalid units')
        snapshot = (self.token.balances.copy(), self.credits.copy())
        before = self.token.balances['vault']
        try:
            if not self.token.transfer(owner,requested): raise ValueError('false transfer')
            received = self.token.balances['vault']-before
            if received <= 0 or received < min_received: raise ValueError('received below minimum')
            credit = received if self.measure_received else requested
            self.credits[owner] = self.credits.get(owner,0)+credit
            return credit
        except Exception:
            self.token.balances,self.credits = snapshot
            raise
