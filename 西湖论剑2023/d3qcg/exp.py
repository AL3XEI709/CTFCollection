import itertools 

def small_roots(f, bounds, m=1, d=None):
    if not d:
        d = f.degree()

    R = f.base_ring()
    N = R.cardinality()

    f /= f.coefficients().pop(0)
    f = f.change_ring(ZZ)

    G = Sequence([], f.parent())
    for i in range(m + 1):
        base = N ^ (m - i) * f ^ i
        for shifts in itertools.product(range(d), repeat=f.nvariables()):
            g = base * prod(map(power, f.variables(), shifts))
            G.append(g)

    B, monomials = G.coefficient_matrix()
    monomials = vector(monomials)

    factors = [monomial(*bounds) for monomial in monomials]
    for i, factor in enumerate(factors):
        B.rescale_col(i, factor)
    B = B.dense_matrix().LLL()

    B = B.change_ring(QQ)
    for i, factor in enumerate(factors):
        B.rescale_col(i, 1 / factor)

    H = Sequence([], f.parent().change_ring(QQ))
    for h in filter(None, B * monomials):
        H.append(h)
        I = H.ideal()
        if I.dimension() == -1:
            H.pop()
        elif I.dimension() == 0:
            roots = []
            for root in I.variety(ring=ZZ):
                root = tuple(R(root[var]) for var in f.variables())
                roots.append(root)
            return roots

    return []

a = 3591518680290719943596137190796366296374484536382380061852237064647969442581391967815457547858969187198898670115651116598727939742165753798804458359397101
c = 6996824752943994631802515921125382520044917095172009220000813718617441355767447428067985103926211738826304567400243131010272198095205381950589038817395833
p = 7386537185240346459857715381835501419533088465984777861268951891482072249822526223542514664598394978163933836402581547418821954407062640385756448408431347
h1,h2 = 67523583999102391286646648674827012089888650576715333147417362919706349137337570430286202361838682309142789833, 70007105679729967877791601360700732661124470473944792680253826569739619391572400148455527621676313801799318422
h1,h2 = h1<<146,h2<<146
bounds = (2 ^ 145, 2 ^ 146)
PR.<l1,l2> = PolynomialRing(Zmod(p)) 
l1,l2 = PR.gens() 
f = a*(h1+l1)^2 + c - (h2 + l2) 
l1,l2 = small_roots(f,bounds,m=3,d=4)[0]
print(l1,l2)  

sec2 = (h1+l1-c)*inverse_mod(a,p)%p 
print(sec2)

###-----------------exp2-----------------###
import hashlib 
from Crypto.Util.number import * 
x1,x2 = 3345361405203462981041847914374453868599106060665812229784462734764742247048957655005612474587555839753748604882708741687926147536458567411789178129398205, 4041175780036883478815867467461047550933982405318965631484489156717330002773568568536902190010839138410185231519872805730895806870604072973967270279033142 

# enc = bytes_to_long(hashlib.sha512(b'%d'%(x1)).digest())^bytes_to_long(flag)
enc = 6176615302812247165125832378994890837952704874849571780971393318502417187945089718911116370840334873574762045429920150244413817389304969294624001945527125
p = 7386537185240346459857715381835501419533088465984777861268951891482072249822526223542514664598394978163933836402581547418821954407062640385756448408431347
print(long_to_bytes(bytes_to_long(hashlib.sha512(b'%d'%(x1)).digest())^enc)) 
# Here_is_ur_flag!:)d3ctf{th3_c0oppbpbpbp3rsM1th_i5_s0_1ntr35ting}
