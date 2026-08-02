"""Perron-Frobenius / transfer operator for machine 1's mantissa density (pure Python).
Build the empirical Markov operator on binned m=frac(log2 D), find the stationary
density by power iteration, compare to the direct histogram, quantify mixing."""
import sys, math
sys.path.insert(0,"/Users/tomzahavy/Documents/Claude/collatz/machine1")
import onedim

def mant(D):
    b=D.bit_length(); top=D>>max(0,b-64)
    return (math.log2(top)+(b-top.bit_length())-(b-1))%1.0

D=17; N=40000; ms=[]
for _ in range(N):
    ms.append(mant(D)); D=onedim.F(D)[0]

B=60
P=[[0.0]*B for _ in range(B)]; hist=[0.0]*B
for k in range(len(ms)-1):
    i=min(B-1,int(ms[k]*B)); j=min(B-1,int(ms[k+1]*B))
    P[i][j]+=1; hist[i]+=1
hist[min(B-1,int(ms[-1]*B))]+=1
for i in range(B):
    rs=sum(P[i]) or 1.0
    P[i]=[x/rs for x in P[i]]

# stationary by power iteration: pi <- pi P
pi=[1.0/B]*B
gaps=[]
for it in range(2000):
    nxt=[0.0]*B
    for i in range(B):
        pv=pi[i]
        if pv:
            row=P[i]
            for j in range(B): nxt[j]+=pv*row[j]
    s=sum(nxt); nxt=[x/s for x in nxt]
    diff=sum(abs(nxt[j]-pi[j]) for j in range(B))
    if it>0: gaps.append(diff)
    pi=nxt
    if diff<1e-14: break

emp=[h/sum(hist) for h in hist]
l1=sum(abs(pi[j]-emp[j]) for j in range(B))
print(f"transfer-operator stationary vs direct histogram: L1 = {l1:.4f}  (small => same measure)")
# mixing: ratio of successive correction norms ~ second eigenvalue modulus
if len(gaps)>10:
    ratios=[gaps[i+1]/gaps[i] for i in range(5,15) if gaps[i]>0]
    lam2=sum(ratios)/len(ratios)
    print(f"power-iteration contraction ratio ~ |lambda_2| = {lam2:.3f}  => spectral gap = {1-lam2:.3f}")

bp=math.log2(5/4)
below=[pi[i]*B for i in range(B) if (i+0.5)/B<bp]
above=[pi[i]*B for i in range(B) if (i+0.5)/B>=bp]
print(f"\ndensity (stationary, uniform=1), breakpoint log2(5/4)={bp:.4f}:")
print(f"  mean BELOW breakpoint {sum(below)/len(below):.3f}   ABOVE {sum(above)/len(above):.3f}"
      f"   ratio {(sum(below)/len(below))/(sum(above)/len(above)):.3f}")
bi=int(bp*B)
print(f"  across the breakpoint: bins ...{pi[bi-2]*B:.2f} {pi[bi-1]*B:.2f} | {pi[bi]*B:.2f} {pi[bi+1]*B:.2f}...")
