from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import sha256
from random import randbytes, getrandbits
from flag import flag
def diffie_hellman(g, p, flag):
    alice = getrandbits(1024)
    bob = getrandbits(1024)
    alice_c = pow(g, alice, p)
    bob_c = pow(g, bob, p)
    print(alice_c , bob_c)
    key = sha256(long_to_bytes(pow(bob_c, alice, p))).digest()
    iv = b"dasctfdasctfdasc"
    aes = AES.new(key, AES.MODE_CBC, iv)
    enc = aes.encrypt(flag)
    print(enc)

def getp():
    p = int(input("P = "))
    assert isPrime(p)
    assert p.bit_length() >= 1024 and p.bit_length() <= 2048
    g = 2
    diffie_hellman(g, p, flag)

getp()