#!/usr/bin/env python3
import os
from Crypto.Util.number import getPrime, getRandomRange

def isSquare(a, p):
    return pow(a, (p-1)//2, p) != p-1

class SquareRNG(object):
    def __init__(self, p, sa, sb):
        assert sa != 0 and sb != 0
        (self.p, self.sa, self.sb) = (p, sa, sb)
        self.x = 0

    def int(self, nbits):
        v, s = 0, 1
        for _ in range(nbits):
            self.x = (self.x + 1) % p
            s += pow(self.sa, self.x, self.p) * pow(self.sb, self.x, self.p)
            s %= self.p
            v = (v << 1) | int(isSquare(s, self.p))
        return v

    def bool(self):
        self.x = (self.x + 1) % self.p
        t = (pow(self.sa, self.x, self.p) + pow(self.sb, self.x, self.p))
        t %= self.p
        return isSquare(t, self.p)

p = getPrime(256)

sb1 = int(input("Bob's seed 1: ")) % p
sb2 = int(input("Bob's seed 2: ")) % p
for _ in range(77):
    sa = getRandomRange(1, p)
    r1 = SquareRNG(p, sa, sb1)
    m1 = r1.int(32)
    print("Random 1:", hex(m1))
    r2 = SquareRNG(p, sa, sb2)
    m2 = r2.int(32)
    print("Random 2:", hex(m2))
    x = r1.bool() 
    print(int(x),m1.bit_length(),m2.bit_length())
    guess = int(input("Guess next bool [0 or 1]: "))
    if guess == int(x):
        print("OK!")
    else:
        print("NG...")
        break
else:
    print("Congratz!")

