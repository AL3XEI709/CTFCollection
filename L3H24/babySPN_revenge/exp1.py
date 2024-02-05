import random
import time
from hashlib import sha256
from Crypto.Util.number import *

def bin_to_list(r, bit_len):
    list = [r >> d & 1 for d in range(bit_len)][::-1]
    return list

def list_to_int(list):
    return int("".join(str(i) for i in list), 2)

Pbox=[1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]
rePbox = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
Sbox=[14, 13, 11, 0, 2, 1, 4, 15, 7, 10, 8, 5, 9, 12, 3, 6]
reSbox=[3, 5, 4, 14, 6, 11, 15, 8, 10, 12, 9, 2, 13, 1, 0, 7]


def round_func(X,r,K):
    kstart=4*r - 4
    XX = [0] * 16
    for i in range(16):
        XX[i] = X[i] ^ K[kstart+i]
    for i in range(4):
        value = list_to_int(XX[4*i:4*i+4])
        s_value = Sbox[value]
        s_list = bin_to_list(s_value, 4)
        XX[4*i],XX[4*i+1],XX[4*i+2],XX[4*i+3] = s_list[0],s_list[1],s_list[2],s_list[3]

    Y=[0] * 16
    for i in range(16):
        Y[Pbox[i]-1]=XX[i]
    return Y

def re_round_func4(X,K):
    Y = [0]*16  
    for i in range(16):
        Y[rePbox[i]]=X[i]

    for i in range(4):
        value = list_to_int(Y[4*i:4*i+4])
        s_value = reSbox[value]
        s_list = bin_to_list(s_value, 4)
        Y[4*i],Y[4*i+1],Y[4*i+2],Y[4*i+3] = s_list[0],s_list[1],s_list[2],s_list[3]
    kstart =  0
    for i in range(16):
        Y[i] = Y[i] ^ K[kstart+i]
    return Y

def re_round_func3(X):
    Y = [0]*16  
    for i in range(16):
        Y[rePbox[i]]=X[i]

    for i in range(4):
        value = list_to_int(Y[4*i:4*i+4])
        s_value = reSbox[value]
        s_list = bin_to_list(s_value, 4)
        Y[4*i],Y[4*i+1],Y[4*i+2],Y[4*i+3] = s_list[0],s_list[1],s_list[2],s_list[3]

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




ss = [[0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
[0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
[0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
[0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1]]

for index in range(4):
    FLAG = set()
    XX = [0]*16
    XX[index*4] = 1

    A = dict()
    from tqdm import *

    for j in trange(900000,910000):
        K = bin_to_list(j,20)
        Y = round_func(XX,1,K)
        Y = round_func(Y,2,K)
        kstart=8
        #XX = [0] * 16
        for i in range(12):
            Y[i] = Y[i] ^ K[kstart+i]
        A[str(Y[:12])] = K 
 
        
        
        #break

    XX = ss[index]

    flag = set()
    for j in trange(2**20):
        XXX = XX.copy()
        K = bin_to_list(j,20)
        kstart = 4
        for i in range(16):
            XXX[i] = XXX[i]^K[kstart+i]

        Y = re_round_func4(XXX,K)
        Y = re_round_func3(Y)

        
        if str(Y[:12]) in A:
            tmpk = A[str(Y[:12])]+K[-12:]
            #print(tmpk)
            if enc([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],tmpk) ==  [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1] and \
                enc([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],tmpk) == [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0] and \
                enc([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],tmpk) == [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1] and \
                enc([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],tmpk) == [0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1]:
                print("[++]",tmpk)
                exit()

