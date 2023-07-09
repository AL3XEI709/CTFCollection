from Crypto.Util.number import * 
from random import randint 
import gmpy2 as gp 
from pwn import * 
from sympy import nextprime 
def abs(m):
    if m<0:
        return -m 
    return m 


def get(b1,b2):
    for m in range(2**((b1+1)//3),2**((b2+1)//3)): 
        if isPrime(1+9*m**3): 
            break 
    print((1 + 9*m**3)**3  +  (9*m**4)**3  +  (-9*m**4 - 3*m)**3  ==  1 ) 
    p,q,r = (1 + 9*m**3),9*m**4,-9*m**4 - 3*m 
    print(min(abs(p).bit_length(),abs(q).bit_length(),abs(r).bit_length())) 
    res = str(p)+","+str(q)+","+str(r) 
    return res.encode()

rec = remote('05.cr.yp.toc.tf',11137) 
while True:
    r = rec.recvline() 
    print(r) 
    if b'almost' in r:
        
        _ = r[r.index(b'('):r.index(b')')+1]  
        _ = eval(_) 
        b1,b2 = _ 
        res = get(b1,b2) 
        rec.sendline(res)