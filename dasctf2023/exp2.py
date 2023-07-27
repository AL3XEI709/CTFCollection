import gmpy2
from Crypto.Util.number import getPrime
import random
from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import sha256 

def gen_prime(digit):
    primes = []
    pri = 1
    while(len(primes)<100):
        pri = gmpy2.next_prime(pri)
        primes.append(int(pri))
    while True:
        count = 2
        while count < 2**digit:
            count *= random.choice(primes)
        count += 1
        if(gmpy2.is_prime(count)):
            return count

'''p = gen_prime(1024) 
G = GF(P) 
g_ = G(g) 
ac_ = G(ac) 
alice = int(discrete_log(ac_,g_)) 
print(alice)


'''

alice = 1046382552755992811457982912694618414872058936337177684338202569822370210620216903105219207397545099396117900950990663819206744964944899595012911402477464329708104871889963814612755420606417426402402131901720127104652472541002317267138113556214527301245557009631475388100000836750737255081835356782751153367 
P = 335347423405170083398559193700458873250569626299973646883438047064926777811449508027635784322795263459385528095096950146720369849218673184537518905837461553332860863341898712720955258188662619459370538150944015362912381662926695555870098124952507918358330303676192552193204581458968503798256226692794489522821
ac,bc=223676019829477985645895853282768682560855850770933122577933519525057883850366435365443483994163940231382663968887215078379264068697081085889130204146863047561895606804119130512046059900944330438737166140524383141720020490696090144841644182519896300804491684305301848398654866801293171153005854449806177065769, 175861293669891528934345252748997792066936662405310572915942032646583833324927754007720831902026700146884820356166597766296538489029268404074802240969314519015975193008206638659010499894115919252744649609865797973520881153393357369190942129525709128275570322882970502645366664567710272801953146630381233539658
ct = b'a\x01\xe1\x0f\x03\xdd\xb2\x88wn\xear\xac&\xbf\x8aP\xb1\xc3C\xc6\xfb\xe1\xfa\x8b\x98\xc9\xee;B\xef\x19y\xc2\x1c\xfb!\x16\xdd/f\x82+f\x81\xee;\x16'
g = 2 


key = sha256(long_to_bytes(pow(bc, alice, P))).digest()
iv = b"dasctfdasctfdasc"
aes = AES.new(key, AES.MODE_CBC, iv)
enc = aes.decrypt(ct)
print(enc)