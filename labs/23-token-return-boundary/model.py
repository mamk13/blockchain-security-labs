"""Selected transfer-result semantics. No ABI or EVM execution."""
TRUE=(1).to_bytes(32,'big')
FALSE=bytes(32)

def accepted(has_code, call_ok, data):
    return has_code and call_ok and (data == b'' or data == TRUE)

class Token:
    def __init__(self, mode='true'):
        self.mode=mode
        self.balances={'escrow':100,'Alice':0}

    def transfer(self, amount):
        code=self.mode != 'no-code'
        ok=self.mode != 'revert'
        moves=self.mode in ('true','empty','malformed','false-after-write')
        if moves:
            self.balances['escrow']-=amount
            self.balances['Alice']+=amount
        data={'true':TRUE,'empty':b'','false':FALSE,'malformed':b'\x01',
              'false-after-write':FALSE,'revert':b'','no-code':b'','liar':TRUE}[self.mode]
        return code,ok,data

class Escrow:
    def __init__(self, token):
        self.token=token
        self.owed=100

    def pay(self, amount, guarded=True):
        if type(amount) is not int or not 0 < amount <= self.owed:
            raise ValueError('invalid payout')
        checkpoint=dict(self.token.balances)
        code,ok,data=self.token.transfer(amount)
        success=accepted(code,ok,data) if guarded else ok
        if not success:
            # Explicit fixture rollback; Python exceptions do not do this for us.
            self.token.balances=checkpoint
            raise ValueError('transfer rejected')
        self.owed-=amount
