'''
第一部：原题，套exp解
'''

def decrypt(enc, private):
    sum = 0
    prod = reduce(lambda a, b: a*b, private)
    for a_i, n_i in zip(enc, private):
        p = prod // n_i
        sum += a_i * pow(p, -1, n_i) * p
    return sum % prod

p = gp.gcd(g1-1,N) 
enc = [c1,c2] 
m1 = decrypt(enc,[p,1]) 

pre = '0123456789abcdefghijklmnopqrstuvwxyz-' 
for a in pre:
    for b in pre:
        for c in pre:
            for d in pre:
                    mask = bytes_to_long((a+b+c+d+'}').encode()+long_to_bytes(0x1b)*11 ) 
                    print(a+b+c+d+'}')
                    if int(pow((A[1] * mask ** 2 + B[1] * mask + C[1]), 5, N1)) == Cs[1]:
                        exit()    
'''
第二部：注意到填充的格式，最后一block完全由flag长度决定，而由于第一部分解出来了所以flag长度知道，而第二个block未知字串只有四个（最后一个字串是flag结尾‘}’），所以无脑爆破即可
'''
