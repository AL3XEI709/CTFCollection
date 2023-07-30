'''from pwn import * 
import string 
import itertools 
from hashlib import sha256 
ALPHABET = string.ascii_letters + string.digits 

rec = remote('122.9.153.69', 23333) 
m=rec.recvuntil(b'Give me XXXX:')  
tail, h = m[12:28], m[33:97].decode() 
for i in itertools.product(ALPHABET, repeat=4):
    prefix = ''.join(i)
    guess = prefix.encode() + tail 
    if sha256(guess).hexdigest() == h: 
        rec.sendline(prefix.encode()) 
        break 
rec.interactive()'''
import random 
import string 
# from tqdm import tqdm 
t2= '\W93VnRHs<CU#GI!d^7;\'Lyfo`qt68&Y=Pr(b)O2[|mc0z}BvKkh5~lJeXM-iNgaTZ]*4F?upw>A,x@DQ.Sj:_$E/%"+{1'
cipher= '&I1}ty~A:bR>)Q/;6:*6`1;bum?8i[LL*t`1;bum?8i[LL?Ia`1;bum?8i[LL72;xl:mvHF"z4_/DD+c:mvHF"z4_/DDzbZ:mvHF"z4_/DDr}vS?'

characters = string.printable[:-6]
digits = string.digits
ascii_letters = string.ascii_letters
'''assert len(characters) == len(map_string2)
for rseed in tqdm(range(1000)): 
    random.seed(rseed*2) 
    random_sequence = random.sample(characters, len(characters))
    t = "".join(random_sequence) 
    if t == map_string2:
        break '''
def str_xor(s: str, k: str, index: int):
    return ''.join(chr((ord(a) + index) ^ (ord(b) + index)) for a, b in zip(s, k))
rseed = 1334//2
random.seed(rseed)
random_sequence = random.sample(characters, len(characters))
map_string1 = ''.join(random_sequence)

random.seed(rseed * 2)
random_sequence = random.sample(characters, len(characters))
map_string2 = ''.join(random_sequence)
assert t2 == map_string2
random.seed(rseed * 3)
random_sequence = random.sample(characters, len(characters))
map_string3 = ''.join(random_sequence)


def util(flag):
    return flag[9: -1]

def util1(c):
    return map_string3.index(c) 


def crypto_final(list):
    str=""
    for i in list[::-1]:
        str += i
    return str


def crypto_final_rev(list):
    return crypto_final(list) 

def crypto_phase3(list):
    newlist = []
    for i in list:
        str = ""
        for j in i:
            str += map_string2[util1(j)] #return map_string3.index(c)  
            
        newlist.append(str)
    return newlist 

def crypto_phase3_rev(list): 
    newlist = [] 
    for i in list:
        str = "" 
        for j in i: 
            str += map_string3[map_string2.index(j)] 
        
        newlist.append(str) 
    return newlist 


def crypto_phase2(list):
    newlist = []
    for i in list:
        str = ""
        for j in i:
            str += map_string1[util1(j)]
           
        newlist.append(str)
    return newlist


def crypto_phase2_rev(list): 
    newlist = [] 
    for i in list:
        str = "" 
        for j in i: 
            str += map_string3[map_string1.index(j)] 
        
        newlist.append(str) 
    return newlist 
def Ran_str(seed : int, origin: str):
    random.seed(seed)
    random_sequence = random.sample(origin, len(origin))
    return ''.join(random_sequence)

def mess_sTr(s : str, index : int):
   
    map_str = Ran_str(index, ascii_letters + digits)
    new_str = str_xor(s, map_str[index])
    
    if not characters.find(new_str) >= 0:
        new_str = "CrashOnYou??" + s
    
    return new_str, util1(map_str, s)
    

def crypto_phase1(flag):
    flag_list1 = util(flag).split('_')
    newlist1 = []
    newlist2 = []
    index = 1
    k = 0
    for i in flag_list1:
        if len(i) % 2 == 1:
            i1 = ""
            for j in range(len(i)):
                p, index = mess_sTr(i[j], index)
                i1 += p
           
            p, index = mess_sTr(i[0], index)
            i1 += p
            
            i1 += str(k)
            k += 1
            newlist1.append(i1)
        
        else:
            i += str(k)
            k += 1
            newlist2.append(i)
    
    return newlist1, newlist2

# crypto_phase3(crypto_phase2(flaglist1) + flaglist1) + crypto_phase2(crypto_phase3(flaglist2))

cipher = cipher[::-1] # rev final 
for i in range(len(cipher)): 
    t1,t2 = cipher[:i],cipher[i:] 
    t1 = "".join(crypto_phase3_rev([_ for _ in t1]))
    for j in range(len(t1)): 
        t11,t12 = t1[:j],t1[j:] 
        tmp = "".join(crypto_phase2_rev([_ for _ in t11])) 
        if tmp == t12:
            print('find!')
            flaglist1 = t12 
            flaglist2 = "".join(crypto_phase3_rev(crypto_phase2_rev([_ for _ in t2]))) 
            print(flaglist1,flaglist2) 
            #break 

"0>aDT??uoYnOhsarC3wn??uoYnOhsarCRF??uoYnOhsarC 1Dn1F23m0s4nl5OtP7Rc"