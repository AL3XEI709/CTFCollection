from Crypto.Util.number import * 
import gmpy2 as gp 
import random 
p = getPrime(1024)

print('mod =', p)
secret = random.randint(1, p-1)

def XennyOracle():
    t = getPrime(512)
    e = getPrime(328) 
    h = gp.invert(secret+t, p) - e 
    return t, h, e 

tl,hl,el = [], [], [] 
n, eb = 15, 328 
for i in range(n): 
    t,h,e = XennyOracle() 
    tl.append(t) 
    hl.append(h)   
    el.append(e) 
t0, h0, e0 = tl[0], hl[0], el[0] 
tl, hl, el = tl[1:], hl[1:], el[1:]  
print(el[0])
n -= 1 
assert len(tl) == n

m = matrix(QQ,3*n+2) 

m[0,0] = 1 
al, bl, cl, dl = [], [], [], [] 
for i in range(n): 
    al.append(t0 - tl[i]) 
    bl.append(hl[i]*(t0-tl[i])+1) 
    cl.append(h0*(t0-tl[i])-1)  
    dl.append(hl[i]*h0*(t0-tl[i])+h0-hl[i])  

assert (al[0]*e0*el[0] + bl[0]*e0 + cl[0]*el[0] + dl[0]) % p == 0  

m[0,0] = 1 
for i in range(1,n+2): 
    m[i,i] = 2^(-eb) 

for i in range(n+2,2*n+2): 
    m[i,i] = 2^(-eb*2)  

for i in range(2*n+2,3*n+2):
    assert m[i,i] == 0 
    m[i,i] = p 

for i in range(n):
    assert m[0,2*n+2+i] == 0 
    m[0,2*n+2+i] = dl[i] 

for i in range(n):
    assert m[i+1,2*n+2+i] == 0
    m[i+1,2*n+2+i] = cl[i] 

for i in range(n):
    assert m[n+1,2*n+2+i] == 0 
    m[n+1,2*n+2+i] = bl[i] 

for i in range(n):
    assert m[n+2+i,2*n+2+i] == 0
    m[n+2+i,2*n+2+i] = al[i] 

L = m.LLL()
test_el = [] 
f = open("F:\\360MoveData\\Users\\Admin\\Desktop\\python sage\\output.txt",'w')
for i in range(3*n+2):
    if int(L[i,0]) == 1:
        if int(L[i,1]*(2^eb)) == int(el[0]):
            mye = int(L[i,1]*(2^eb)) 
            mysec = (inverse_mod(mye+hl[0],p)-tl[0])%p 
            print(mysec == secret) 
        
    f.write(str(L.row(i))+'\n')   
    
f.close()
'''
mod = xxx
xxx
True
'''
