from time import time
 
def genpseudoprime(eta,etamin=211):
  if eta<=(2*etamin):
    return random_prime(2^eta,False,2^(eta-1))
  else:
    return random_prime(2^etamin,False,2^(etamin-1))*genpseudoprime(eta-etamin)
 
def genParams(n=10,m=20,nx0=100):
  #print "Generation of x0",
  t=time()
  x0=genpseudoprime(nx0)
  #print time()-t 
 
  # We generate the alpha_i's
  a=vector(ZZ,n)
  for i in range(n):
    a[i]=mod(ZZ.random_element(x0),x0)
 
  # The matrix X has m rows and must be of rank n
  while True:
    X=Matrix(ZZ,m,n)
    for i in range(m):
      for j in range(n):
        X[i,j]=ZZ.random_element(2)
    if X.rank()==n: break
 
  # We generate an instance of the HSSP: b=X*a
  c=vector(ZZ,[0 for i in range(m)])
  s=ZZ.random_element(x0)
  b=X*a
  for i in range(m):
    b[i]=mod(b[i],x0)
 
  return x0,a,X,b 
 
# We generate the lattice of vectors orthogonal to b modulo x0
def orthoLattice(b,x0):
  m=b.length()
  M=Matrix(ZZ,m,m)
 
  for i in range(1,m):
    M[i,i]=1
  M[1:m,0]=-b[1:m]*inverse_mod(b[0],x0)
  M[0,0]=x0
 
  for i in range(1,m):
    M[i,0]=mod(M[i,0],x0)
 
  return M
 
def allones(v):
  if len([vj for vj in v if vj in [0,1]])==len(v):
    return v
  if len([vj for vj in v if vj in [0,-1]])==len(v):
    return -v
  return None
 
def recoverBinary(M5):
  lv=[allones(vi) for vi in M5 if allones(vi)]
  n=M5.nrows()
  for v in lv:
    for i in range(n):
      nv=allones(M5[i]-v)
      if nv and nv not in lv:
        lv.append(nv)
      nv=allones(M5[i]+v)
      if nv and nv not in lv:
        lv.append(nv)
  return Matrix(lv)
 
def allpmones(v):
  return len([vj for vj in v if vj in [-1,0,1]])==len(v)
 
# Computes the right kernel of M using LLL.
# We assume that m>=2*n. This is only to take K proportional to M.height()
# We follow the approach from https://hal.archives-ouvertes.fr/hal-01921335/document
def kernelLLL(M):
  n=M.nrows()
  m=M.ncols()
  if m<2*n: return M.right_kernel().matrix()
  K=2^(m//2)*M.height()
  
  MB=Matrix(ZZ,m+n,m)
  MB[:n]=K*M
  MB[n:]=identity_matrix(m)
  
  MB2=MB.T.LLL().T
  
  assert MB2[:n,:m-n]==0
  Ke=MB2[n:,:m-n].T
 
  return Ke
 
# This is the Nguyen-Stern attack, based on BKZ in the second step
def NSattack(n=60):
  m=int(max(2*n,16*log(n,2)))
  print ("n=",n,"m=",m)
 
  iota=0.035
  nx0=int(2*iota*n^2+n*log(n,2))
  print ("nx0=",nx0)
 
  x0,a,X,b=genParams(n,m,nx0)
 
  M=orthoLattice(b,x0)
 
  t=cputime()
  M2=M.LLL()
  print ("LLL step1: %.1f" % cputime(t))
 
  assert sum([vi==0 and 1 or 0 for vi in M2*X])==m-n
  MOrtho=M2[:m-n]
 
  print ("  log(Height,2)=",int(log(MOrtho.height(),2)))
 
  t2=cputime()
  ke=kernelLLL(MOrtho)
  
  print ("  Kernel: %.1f" % cputime(t2))
  print ("  Total step1: %.1f" % cputime(t))
 
  if n>170: return
 
  beta=2
  tbk=cputime()
  while beta<n:
    if beta==2:
      M5=ke.LLL()
    else:
      M5=M5.BKZ(block_size=beta)
    
    # we break when we only get vectors with {-1,0,1} components
    if len([True for v in M5 if allpmones(v)])==n: break
 
    if beta==2:
      beta=10
    else:
      beta+=10
  
  print ("BKZ beta=%d: %.1f" % (beta,cputime(tbk)))
  t2=cputime()
  MB=recoverBinary(M5)
  print ("  Recovery: %.1f" % cputime(t2))
  print ("  Number of recovered vector=",MB.nrows())
  nfound=len([True for MBi in MB if MBi in X.T])
  print ("  NFound=",nfound)
  
  NS=MB.T
  invNSn=matrix(Integers(x0),NS[:n]).inverse()
  ra=invNSn*b[:n]
  nrafound=len([True for rai in ra if rai in a])
  print ("  Coefs of a found=",nrafound,"out of",n)
  print ("  Total step2: %.1f" % cputime(tbk))
  print ("  Total time: %.1f" % cputime(t))
 
    
def statNS():
  for n in range(70,190,20)+range(190,280,30):
    NSattack(n)
    print
 
def matNbits(M):
  return max([M[i,j].nbits() for i in range(M.nrows()) for j in range(M.ncols())])
 
# Matrix rounding to integers
def roundM(M):
  M2=Matrix(ZZ,M.nrows(),M.ncols())
  for i in range(M.nrows()):
    for j in range(M.ncols()):
      M2[i,j]=round(M[i,j])
  return M2
 
def orthoLatticeMod(b,n,x0):
  m=b.length()
  assert m>=3*n
  assert m % n==0
  M=Matrix(ZZ,m,3*n)
  M[:2*n,:2*n]=identity_matrix(2*n)
  for i in range(2,m/n):
    M[i*n:(i+1)*n,2*n:3*n]=identity_matrix(n)
  
  M[1:,0]=-b[1:]*inverse_mod(b[0],x0)
  M[0,0]=x0
 
  for i in range(1,m):
    M[i,0]=mod(M[i,0],x0)
  return M
 
def NZeroVectors(M):
  return sum([vi==0 and 1 or 0 for vi in M])
 
 
# This is our new multivariate attack
def multiAttack(n=16):
  if n % 2==1:
    m=n*(n+3)/2 # n is odd
  else:
    m=n*(n+4)/2 # n is even
  k=4
 
  print ("n=",n,"m=",m,"k=",k)
 
  iota=0.035
  nx0=int(2*iota*n^2+n*log(n,2))
  print ("nx0=",nx0)
 
  x0,a,X,b=genParams(n,m,nx0) # x0:p; a:1*n random n ; X:m*n random 2 ;b=X*a;
 
  M=orthoLatticeMod(b,n,x0)
 
  print( "Step 1",)
  t=cputime()
 
  M[:n//k,:n//k]=M[:n//k,:n//k].LLL()
  
  M2=M[:2*n,:2*n].LLL()
  tprecomp=cputime(t)
  print( "  LLL:%.1f" % tprecomp)
 
  RF=RealField(matNbits(M))
 
  M4i=Matrix(RF,M[:n//k,:n//k]).inverse()
  M2i=Matrix(RDF,M2).inverse()
 
  ts1=cputime()
  while True:
    flag=True
    for i in range((m/n-2)*k):
      indf=2*n+n//k*(i+1)
      if i==(m/n-2)*k-1:
        indf=m
        
      mv=roundM(M[2*n+n//k*i:indf,:n//k]*M4i)
      if mv==0: 
        continue
      flag=False
      M[2*n+n//k*i:indf,:]-=mv*M[:n//k,:]
    if flag: break
  print( "  Sred1:%.1f" % cputime(ts1))
 
  M[:2*n,:2*n]=M2
 
  ts2=cputime()
  while True:
    #print "  matNBits(M)=",matNbits(M[2*n:])
    mv=roundM(M[2*n:,:2*n]*M2i)
    if mv==0: break
    M[2*n:,:]-=mv*M[:2*n,:]
  print ("  Sred2:%.1f" % cputime(ts2))
 
  # The first n vectors of M should be orthogonal
  northo=NZeroVectors(M[:n,:2*n]*X[:2*n])
 
  for i in range(2,m/n):
    northo+=NZeroVectors(M[i*n:(i+1)*n,:2*n]*X[:2*n]+X[i*n:(i+1)*n])
 
  print ("  #ortho vecs=",northo,"out of",m-n)
 
  # Orthogonal of the orthogonal vectors
  # We compute modulo 3
  MO=Matrix(GF(3),n,m)
  
  tk=cputime()
  MO[:,:2*n]=kernelLLL(M[:n,:2*n])
  print( "  Kernel LLL: %.1f" % cputime(tk))
 
  for i in range(2,m/n):
    MO[:,i*n:(i+1)*n]=-(M[i*n:(i+1)*n,:2*n]*MO[:,:2*n].T).T
  #print "Total kernel computation",cputime(tk)
  print ("  Total Step 1: %.1f" % cputime(t))
 
  print ("Step 2")
  t2=cputime()
  xt23=Matrix(GF(3),[(-x).list()+[x[i]*x[j]*((i==j) and 1 or 2) for i in range(n) for j in range(i,n)] for x in MO.T])
  ke3=xt23.right_kernel().matrix()
  print ("  Kernel: %.1f" % cputime(t2))
 
  assert xt23.nrows()==m
  assert xt23.ncols()==n*(n+1)/2+n
 
  ke23=Matrix(GF(3),n,n*n)
  ind=n
  for i in range(n):
    for j in range(i,n):
      ke23[:,i*n+j]=ke3[:,ind]
      ke23[:,j*n+i]=ke3[:,ind]
      ind+=1
 
  tei=cputime()
  # We will compute the list of eigenvectors
  # We start with the full space.
  # We loop over the coordinates. This will split the eigenspaces.
  li=[Matrix(GF(3),identity_matrix(n))]    
  for j in range(n):       # We loop over the coordinates of the wi vectors.
    #print "j=",j
    M=ke23[:,j*n:(j+1)*n]   # We select the submatrix corresponding to coordinate j
    li2=[]                 # We initialize the next list
    for v in li:
      if v.nrows()==1:     # We are done with this eigenvector 
        li2.append(v)
      else:     # eigenspace of dimension >1
        #print "eigenspace of dim:",v.nrows()
        A=v.solve_left(v*M)  # v*M=A*v. When we apply M on the right, this is equivalent to applying the matrix A.
                              # The eigenvalues of matrix A correspond to the jth coordinates of the wi vectors in that
                              # eigenspace
        for e,v2 in A.eigenspaces_left():    # We split the eigenspace according to the eigenvalues of A.
          vv2=v2.matrix()
          #print "  eigenspace of dim:",(vv2*v).nrows()
          li2.append(vv2*v)                   # The new eigenspaces 
 
    li=li2
  
  #print "Eigenvectors computation",cputime(tei)
 
  NS=Matrix([v[0] for v in li])*MO
  for i in range(n):
    if any(c==2 for c in NS[i]): NS[i]=-NS[i]
 
  print ("  Number of recovered vectors:",NS.nrows())
 
  nfound=len([True for NSi in NS if NSi in X.T])
  print ("  NFound=",nfound,"out of",n)
 
  NS=NS.T
 
  # b=X*a=NS*ra
  invNSn=matrix(Integers(x0),NS[:n]).inverse()
  ra=invNSn*b[:n]
  nrafound=len([True for rai in ra if rai in a])
 
  print ("  Coefs of a found=",nrafound,"out of",n)
  print ("  Total step2: %.1f" % cputime(t2))
  print ("  Total runtime: %.1f" % cputime(t) )
  print
 
def statMulti():
  for n in range(70,210,20)+[220,250]:
    multiAttack(n)
    print

multiAttack() # x0:p; a:1*n random n ; X:m*n random 2 ;b=X*a;
'''
n= 16 m= 160 k= 4
nx0= 81
Step 1
  LLL:0.2
  Sred1:0.0
  Sred2:0.0
  #ortho vecs= 144 out of 144
  Kernel LLL: 0.3
  Total Step 1: 0.4
Step 2
  Kernel: 0.0
  Number of recovered vectors: 16
  NFound= 16 out of 16
  Coefs of a found= 16 out of 16
  Total step2: 0.2
  Total runtime: 0.6
'''
