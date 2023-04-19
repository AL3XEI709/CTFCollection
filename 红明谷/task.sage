from sage.all import *
from Crypto.Util.number import *
from os import urandom
from secret import flag

n = 16
bound = 2^15

A = [ZZ.random_element(-bound, bound) for _ in range(n*n)]
A = Matrix(ZZ, n, n, A)
        
B = [ZZ.random_element(-bound, bound) for _ in range(n*n)]
B = Matrix(ZZ, n, n, B)

res = []
for i in range(5):
    bound = 2^15
    S = [ZZ.random_element(-bound, bound) for _ in range(n*n)]
    S = Matrix(ZZ, n, n, S)
    
    tmp = []
    for i in range(0, 60):
        S = S*A+B
        bound = 2^(int(S[0, 0]).bit_length())
        if i % 3 == 2:
            tmp.append(Matrix(ZZ,n,n,[ZZ.random_element(-bound, bound) for _ in range(n*n)]))
            continue
        tmp.append(S)
    res.append(tmp)
    
e = A.LLL().determinant()

p = getPrime(512)
q = getPrime(512)
n = p * q
m = bytes_to_long(urandom(int(n).bit_length() // 8 - len(flag) - 1) + flag)
c = pow(m, e, n)
h1 = pow(p+q, e, n)
h2 = pow(p-q, e, n)

f = open('双人成行.txt', 'w')
f.writelines(str(res)+'\n')
f.writelines(str(n)+'\n')
f.writelines(str(c)+'\n')
f.writelines(str(h1)+'\n')
f.writelines(str(h2)+'\n')
f.close()
