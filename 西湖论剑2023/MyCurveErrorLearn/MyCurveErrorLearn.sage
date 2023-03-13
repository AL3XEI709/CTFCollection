from Crypto.Util.number import *
import os

flag = os.getenv('DASFLAG')

p = getPrime(1024)
a = getPrime(200)
b = getPrime(200)
E = EllipticCurve(GF(p), [a, b])
R = E.random_element()
P = E.random_element()

def XennyOracle(t):
    O = P + t*R
    return int(O[0]) - getPrime(163)


def task():
    for _ in range(30):
        op = int(input())
        if op == 1:
            XennyOracle(int(input()))
        elif op == 2:
            ss = int(input())

            if ss == P[0]:
                print('flag: ', flag)

try:
    task()
except Exception:
    print("Error. try again.")
