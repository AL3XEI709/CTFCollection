from sage.modules.free_module_integer import IntegerLattice
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from hashlib import sha256
from random import choices
from secret import flag
import string
import signal

def gen(n, m, r, N):
    t1 = [ZZ.random_element(-2^15, 2^15) for _ in range(n*m)]
    t2 = [ZZ.random_element(N) for _ in range(r*n)]
    t3 = [ZZ.random_element(-2^20, 2^20) for _ in range(r*m)]
    B = matrix(ZZ, n, m, t1)
    L = IntegerLattice(B)
    A = matrix(ZZ, r, n, t2)
    X = matrix(ZZ, r, m, t3)
    C = (A * B + X) % N
    return L, C

signal.alarm(1800)
n = 75
m = 150
r = 56
N = 126633165554229521438977290762059361297987250739820462036000284719563379254544315991201997343356439034674007770120263341747898897565056619503383631412169301973302667340133958109
L, C = gen(n, m, r, N)
print(C)

key = sha256(str(L.reduced_basis[0]).encode()).digest()
aes = AES.new(key, AES.MODE_ECB)
pt = "".join(choices(string.ascii_letters + string.digits, k=32)).encode()
ct = aes.encrypt(pt)
print(b64encode(ct).decode())
s = b64decode(input("pt = ").strip())
if s == pt:
    print(flag)
