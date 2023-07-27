from Crypto.Util.number import *

n = 83410392685813224685786027640778560521035854332627839979281105731457044069408118952629284089869335506983096270269822559619624906180108256504440296527471536363057103101146262613593336072556587341466840510200003498265457285439149541137127199088938421905041387224795918868443175561632999479925818053898100117419
c1 = 69307306970629523181683439240748426263979206546157895088924929426911355406769672385984829784804673821643976780928024209092360092670457978154309402591145689825571209515868435608753923870043647892816574684663993415796465074027369407799009929334083395577490711236614662941070610575313972839165233651342137645009
c2 = 46997465834324781573963709865566777091686340553483507705539161842460528999282057880362259416654012854237739527277448599755805614622531827257136959664035098209206110290879482726083191005164961200125296999449598766201435057091624225218351537278712880859703730566080874333989361396420522357001928540408351500991

def attack(c1, c2, e, n,le,h):
    PR.<x>=PolynomialRing(Zmod(n))
    g1 = x^e - c1
    g2 = (h*2^(le+8)+x*2^8+125)^e - c2
    def gcd(g1, g2):
        while g2:
            g1, g2 = g2, g1 % g2
        return g1.monic()
    return -gcd(g1, g2)[0]

e=11
h = b"dasctf{"
b = b'}'
h = bytes_to_long(h)
b = bytes_to_long(b)
print(b)
for le in range(1,300):
    try:
        t = attack(c1,c2,e,n,le,h)
        print(long_to_bytes(int(t)).decode())
    except:
        continue