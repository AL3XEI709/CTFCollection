# nc/9999->tcp.cloud.dasctf.com:28523 

from Crypto.Util.number import *
import random, os
from gmpy2 import *
flag = os.getenv('DASFLAG')

p = random.getrandbits(1024)

print('> mod =', p)
secret = random.randint(1, p-1)

def XennyOracle():
    r = getPrime(512)
    d = gmpy2.invert(secret+r, p) - getPrime(246)
    print('> r =', r)
    print('> d =', d)
    

def task():
    for _ in range(3):
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
