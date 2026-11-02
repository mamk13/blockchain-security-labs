"""Length-prefixed byte-pair teaching codec, not Solidity ABI or EIP-712."""
from hashlib import sha256

PREFIX=b'intent-pair-v1\x00'
MAX=65535

def fields(a,b):
    if any(type(x) is not bytes or len(x)>MAX for x in (a,b)):
        raise ValueError('bounded bytes required')

def packed(a,b):
    fields(a,b)
    return a+b

def encode(a,b):
    fields(a,b)
    return PREFIX+len(a).to_bytes(2,'big')+a+len(b).to_bytes(2,'big')+b

def decode(data):
    if type(data) is not bytes or not data.startswith(PREFIX):
        raise ValueError('wrong codec domain')
    pos=len(PREFIX); result=[]
    for _ in range(2):
        if pos+2>len(data): raise ValueError('missing length')
        size=int.from_bytes(data[pos:pos+2],'big'); pos+=2
        if pos+size>len(data): raise ValueError('truncated field')
        result.append(data[pos:pos+size]); pos+=size
    if pos!=len(data): raise ValueError('trailing bytes')
    return tuple(result)

class Approval:
    def __init__(self, a,b,guarded=True):
        self.codec=encode if guarded else packed
        self.digest=sha256(self.codec(a,b)).digest()
        self.consumed=False

    def execute(self,a,b):
        if self.consumed or sha256(self.codec(a,b)).digest()!=self.digest:
            raise ValueError('unapproved or consumed')
        self.consumed=True
        return a,b
