import gmpy2 as gp 
f = open('CTFs/out.tuo','r').read() 
k = 2^1024 

ct = eval(f) 
cl = len(ct)
x,y = [ct[i][0] for i in range(cl)], [ct[i][1] for i in range(cl)] 
k1=(x[0]-x[2])*((y[0]^2-x[0]^3)-(y[1]^2-x[1]^3))-(x[0]-x[1])*((y[0]^2-x[0]^3)-(y[2]^2-x[2]^3))
k2=(x[0]-x[3])*((y[0]^2-x[0]^3)-(y[1]^2-x[1]^3))-(x[0]-x[1])*((y[0]^2-x[0]^3)-(y[3]^2-x[3]^3)) 
p = gp.gcd(k1,k2) 
p = factor(p)[-1][0] 
assert is_prime(p) 
a = ((y[0]^2-x[0]^3)-(y[1]^2-x[1]^3))*gp.invert(x[0]-x[1],p)%p 
b = (y[0]^2-x[0]^3-a*x[0])%p 
E =EllipticCurve(GF(p),[a,b]) 
assert p == E.order() 

# Lifts a point to the p-adic numbers.
def _lift(E, P, gf):
    x, y = map(ZZ, P.xy())
    for point_ in E.lift_x(x, all=True):
        _, y_ = map(gf, point_.xy())
        if y == y_:
            return point_


def attack(G, P):
    """
    Solves the discrete logarithm problem using Smart's attack.
    More information: Smart N. P., "The discrete logarithm problem on elliptic curves of trace one"
    :param G: the base point
    :param P: the point multiplication result
    :return: l such that l * G == P
    """
    E = G.curve()
    gf = E.base_ring()
    p = gf.order()
    assert E.trace_of_frobenius() == 1, f"Curve should have trace of Frobenius = 1."

    E = EllipticCurve(Qp(p), [int(a) + p * ZZ.random_element(1, p) for a in E.a_invariants()])
    G = p * _lift(E, G, gf)
    P = p * _lift(E, P, gf)
    Gx, Gy = G.xy()
    Px, Py = P.xy()
    return int(gf((Px / Py) / (Gx / Gy))) 

def orthoginal_of_vector_modp(h,p):
    k = 2^1024

    h_v = matrix(ZZ,[h+[p]]).T
    h_v = h_v*k
    Q = diagonal_matrix([1]*len(h_v.columns()[0]))

    m = block_matrix(ZZ,[[h_v,Q]])
    L = m.LLL() #  the orthoginal lattice of h
    l = []
    for each in L[:-1]:
        assert each[0] == 0
        l.append(list(each)[1:])
    return l 

def orthoginal_of_lattce(L):
    mm = block_matrix(ZZ,[[L,1]])
    LL = mm.LLL()
    return LL

G = E.gens()[0] 
h = [] 
print(len(ct)) 
for i in range(len(ct)): 
    print(i,end=" ")  
    h.append(attack(G,E(ct[i]))) 

print('start LLL!') 
l = orthoginal_of_vector_modp(h,p)
ll = (matrix(ZZ,l[:len(l[0])-4]).T)*k
LL = orthoginal_of_lattce(ll)

print("".join(chr(i & 0xff) for i in LL[0][len(l[0])-4:]))
