
from hashlib import sha256
from Crypto.Util.number import *


def bin_to_list(r, bit_len):
    list = [r >> d & 1 for d in range(bit_len)][::-1]
    return list

def list_to_int(list):
    return int("".join(str(i) for i in list), 2)

P=[1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]
S=[14, 13, 11, 0, 2, 1, 4, 15, 7, 10, 8, 5, 9, 12, 3, 6]

def round_func(X,r,K):
    kstart=4*r - 4 
    XX = [0] * 16
    for i in range(16):
        XX[i] = X[i] ^ K[kstart+i]
    for i in range(4): 
        value = list_to_int(XX[4*i:4*i+4])
        s_value = S[value]
        s_list = bin_to_list(s_value, 4)
        XX[4*i],XX[4*i+1],XX[4*i+2],XX[4*i+3] = s_list[0],s_list[1],s_list[2],s_list[3]
    Y=[0] * 16 
    for i in range(16):
        Y[P[i]-1]=XX[i]
    return Y

def enc(X,K):
    Y = round_func(X,1,K)
    Y = round_func(Y,2,K)
    Y = round_func(Y,3,K)
    Y = round_func(Y,4,K)
    kstart=4*5 - 4
    for i in range(16):
        Y[i] ^= K[kstart+i]
    return Y

K = [0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0]

assert len(K) == 32
for i in K:
    assert i == 0 or i == 1
hash_value = sha256(long_to_bytes(list_to_int(K))).hexdigest()
print(hash_value)
