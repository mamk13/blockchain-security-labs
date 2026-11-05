"""Bitmap state model; not Permit2 or signature verification."""
MAX=(1<<256)-1
class Bitmap:
    def __init__(self):
        self.words={}
    def locate(self,owner,nonce):
        if not isinstance(owner,str) or not owner or type(nonce) is not int or not 0<=nonce<=MAX:
            raise ValueError("input")
        return (owner,nonce>>8),1<<(nonce&255)
    def invalidate(self,owner,nonce,vulnerable=False):
        key,mask=self.locate(owner,nonce)
        old=self.words.get(key,0)
        self.words[key]=(old^mask) if vulnerable else (old|mask)
    def consume(self,owner,nonce,valid=True):
        key,mask=self.locate(owner,nonce)
        if not valid or self.words.get(key,0)&mask:
            raise ValueError("invalid or consumed")
        self.words[key]=self.words.get(key,0)|mask
