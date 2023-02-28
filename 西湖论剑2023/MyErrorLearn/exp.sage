import itertools 
import gmpy2 as gp 
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

N = 

r1 = 
d1 = 
r2 = 
d2 =
sec = 
PR.<e1,e2> = PolynomialRing(Zmod(N))
e1,e2 = PR.gens()  
bounds = (2 ^ 245, 2 ^ 246)
f1 = d1+e1-d2-e2 
f2 = r2*(d2+e2)-r1*(d1+e1) 
f = f2*(d1+e1)+f1*(r1*(d1+e1)-1) 
x1,x2 = small_roots(f,bounds)[0] 
print(x1,x2)
# s_ = ((d1+e1)-r1)%N 
x1 = int(x1) 
s_ = (gp.invert(d1+x1,N)-r1)%N 
print(s_ == sec) 
# True
