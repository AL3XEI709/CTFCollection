from Crypto.Util.number import *
import random, os
from gmpy2 import *
flag = os.getenv('FLAG')

p = random.getrandbits(1024)

print('> mod =', p)
secret = random.randint(1, p-1)

def XennyOracle():
    r = getPrime(512)
    d = invert(secret+r, p) - getPrime(328)
    print('> r =', r)
    print('> d =', d)

def task():
    for _ in range(16):
        op = int(input())
        if op == 1:
            XennyOracle()
        elif op == 2:
            ss = int(input())

            if ss == secret:
                print('flag: ', flag)

try:
    task()
except Exception:
    print("Error. try again.")
