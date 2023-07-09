from Crypto.Util.number import * 
import sympy 
import gmpy2 as gp 




r, nbit = 8, 128
PKEY = 55208723145458976481271800608918815438075571763947979755496510859604544396672
ENC = 127194641882350916936065994389482700479720132804140137082316257506737630761
n_, e_ = bin(PKEY)[2:-8], bin(PKEY)[-8:]


'''n_ = int(n_,2) 
n_ = n_<<8
nl=[]
for i in range(2**8): 
    nt = n_+i 
    if nt.bit_length() <= 256 and nt%2 == 1:
        print(nt)'''


el=[]
et = 2**15 
while et<2**16: 
    et = sympy.nextprime(et) 
    if bin(et)[2:-r] == e_: 
        el.append(et) 


p = 188473222069998143349386719941755726311
q = 292926085409388790329114797826820624883
n = p*q 
phi = (p-1)*(q-1) 
c = ENC<<8 
for i in range(2**8): 
    ct = c+i 
    for et in el: 
        d = gp.invert(et,phi) 
        mt = long_to_bytes(gp.powmod(ct,d,n)) 
        if len(mt)!=32 and len(mt)!=31:
            print(mt)