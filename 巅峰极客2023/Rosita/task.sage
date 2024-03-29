# Problem by rec, without any sleep at all.
from Crypto.Util.number import bytes_to_long as b2l
from hashlib import sha256
from os import urandom
from secret import p, a, b, flag

ECC = EllipticCurve(GF(p), [a, b])
R, E, C = [ECC.random_point() for _ in range(3)]

pad = lambda m: urandom(8) + m + b'\x00' * (ZZ(p).nbits() // 8 - len(m) - 8 - 1)
out = list()
for i in range(len(flag)):
    m = pad(chr(flag[i]).encode())
    nonce = urandom(16)
    sh = sha256(nonce + m).digest()
    
    Q = b2l(m)*R + b2l(nonce)*E + b2l(sh)*C
    out.append(Q.xy())

with open('out.tuo', 'w') as f:
    f.write(str(out))