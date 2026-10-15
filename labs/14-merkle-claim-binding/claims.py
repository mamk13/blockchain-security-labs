"""Two-leaf SHA-256 teaching tree. Not an Ethereum Merkle encoding."""
from dataclasses import dataclass
from hashlib import sha256
import json

@dataclass(frozen=True)
class Claim:
    campaign: str
    index: int
    account: str
    amount: int

def leaf(c, bind_account=True):
    fields = [c.campaign,c.index,c.account,c.amount] if bind_account else [c.campaign,c.index,c.amount]
    return sha256(b'leaf:' + json.dumps(fields,separators=(',',':')).encode()).digest()

def parent(a,b):
    # Separate leaf and internal-node domains; pair ordering is canonical.
    return sha256(b'node:' + b''.join(sorted((a,b)))).digest()

class Distributor:
    def __init__(self, campaign, root, bind_account=True):
        self.campaign,self.root,self.bind_account = campaign,root,bind_account
        self.used,self.paid = set(),{}

    def rotate_root(self, root):
        # Trusted campaign administration; rotation must not reset consumed indices.
        self.root = root

    def claim(self,c,sibling):
        if c.campaign != self.campaign or not c.account: raise ValueError('context')
        if type(c.index) is not int or c.index < 0 or type(c.amount) is not int or c.amount <= 0:
            raise ValueError('invalid claim')
        if c.index in self.used: raise ValueError('already claimed')
        if parent(leaf(c,self.bind_account),sibling) != self.root: raise ValueError('bad proof')
        self.used.add(c.index)
        # Relayers are allowed, but payment always goes to the bound account.
        self.paid[c.account] = self.paid.get(c.account,0)+c.amount
