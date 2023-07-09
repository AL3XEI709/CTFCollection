def reseed(s):
	return s * 214013 + 2531011
al = [243,136 ,55, 80, 66] 
for i in range(0,2**32): 
    j=i
    tmp=[] 
    for _ in range(5): 
        j = reseed(j) 
        tmp.append((j>>16)&0xff) 
    if tmp == al:
        print(i) 
        break # 10364460 

from Crypto.Util.number import * 
import random 
from z3 import * 
def reseed(s):
	return s * 214013 + 2531011
enc = 0xb0cb631639f8a5ab20ff7385926383f89a71bbc4ed2d57142e05f39d434fce 
enc = [_ for _ in long_to_bytes(enc)] 
pt = [_ for _ in b'CCTF{'] 
for i in range(5):
    print(enc[i]^pt[i],end=" ")
seed = 10364460 
for i in range(len(enc)):
    seed = reseed(seed) 
    m = chr(enc[i]^ ((seed>>16)&0xff)) 
    print(m,end="")

