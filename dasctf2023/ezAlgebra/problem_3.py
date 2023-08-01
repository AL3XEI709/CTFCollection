from Crypto.Util.number import getPrime, bytes_to_long

def YiJiuJiuQiNian(Wo, Xue, Hui, Le, Kai):
    Qi = 1997
    Che = Wo+Hui if Le==1 else Wo*Hui
    while(Xue):
        Qi += (pow(Che, Xue, Kai)) % Kai
        Xue -= 1
    return Qi
    
l = 512
m = bytes_to_long(flag)
p = getPrime(l)
q = getPrime(l//2)
r = getPrime(l//2)
n = p * q * r
t = getrandbits(32)
c1 = YiJiuJiuQiNian(t, 4, p, 1, n)
c2 = YiJiuJiuQiNian(m, 19, t, 0, q)
c3 = YiJiuJiuQiNian(m, 19, t, 1, q)
print(f"n = {n}")
print(f"c1 = {c1}")
print(f"c2 = {c2}")
print(f"c3 = {c3}")