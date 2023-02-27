from random import randrange
from Crypto.Cipher import AES

p = 193387944202565886198256260591909756041

i = lambda x: pow(x, p-2, p)

def add(A, B):
    (u, v), (w, x) = A, B
    assert u != w or v == x
    if u == w: m = (3*u*w + 4*u + 1) * i(v+x)
    else: m = (x-v) * i(w-u)
    y = m*m - u - w - 2
    z = m*(u-y) - v
    return y % p, z % p

def mul(t, A, B=0):
    if not t: return B
    return mul(t//2, add(A,A), B if not t&1 else add(B,A) if B else A)

x = randrange(p)
aes = AES.new(x.to_bytes(16, 'big'), AES.MODE_CBC, bytes(16))
flag = open('flag.txt').read().strip()
cipher = aes.encrypt(flag.ljust((len(flag)+15)//16*16).encode())
print(*mul(x, (4, 10)), cipher.hex(), file=open('flag.enc', 'w'))
# 65639504587209705872811542111125696405 125330437930804525313353306745824609665 b3669dc657cef9dc17db4de5287cd1a1e8a48184ed9746f4c52d3b9f8186ec046d6fb1b8ed1b45111c35b546204b68e0
