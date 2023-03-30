import time
from Crypto.Util.number import getPrime, inverse, bytes_to_long
from secret import flag
import signal

BITS = 512

def gen(BITS):
    p = 0
    q = 0
    while p.bit_length() < BITS:
        p = getPrime(BITS)

    while q.bit_length() < BITS:
        q = getPrime(BITS)

    if p < q:
        p, q = q, p # p > q 
    n = p * q
    e = 65537
    d = inverse(e, (p - 1) * (q - 1))
    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = inverse(q, p)
    return n, p, q, d, e, dp, dq, qinv

def decrypt(c, p, q, dp, dq, qinv):
    start = time.time_ns()
    m1 = modExp(c, dp, p)
    end = time.time_ns()
    time1 = end - start

    start = time.time_ns()
    m2 = modExp(c, dq, q)
    end = time.time_ns()
    time2 = end - start
    h = (qinv * (m1 - m2)) % p
    m = m2 + h * q
    return m, time1, time2

def modExp(a, e, n):
    karatsuba = 10
    normal = 100
    montgomery = 2000
    if a < n:
        delay = karatsuba + montgomery
    else:
        delay = normal + 200
    time.sleep(delay/10000)
    return pow(a, e, n)

n, p, q, d, e, dp, dq, qinv = gen(BITS)
signal.alarm(600)
menu = '''
1.get flag
2.decrypt
'''
print(n)
flag = bytes_to_long(flag)
enc_flag = pow(flag, e, n)
for i in range(555):
    print(menu)
    op = int(input(">").strip())
    if op == 1:
        start = time.time_ns()
        enc_flag = pow(flag, e, n)
        end = time.time_ns()
        print(f"This is your flag: {enc_flag}, use {end - start} ns.")
    elif op == 2:
        ct = int(input("your ct:").strip())
        if ct == enc_flag:
            print("bye~")
            exit()
        else:
            try:
                pt, time1, time2 = decrypt(ct, p, q, dp, dq, qinv)
                print(f"This is your pt: {pt}, step1 use {time1} ns, step2 use {time2} ns.")
            except:
                print("Something went wrong, bye~")
                exit()
    else:
        exit()
