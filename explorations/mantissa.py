"""Machine 1: the stationary density of the mantissa frac(log2 D_k).
Our report flagged this as the 'missing ergodic backbone' (non-uniform, chi^2~162,
but the true density never identified). Attack it directly."""
import sys, math
sys.path.insert(0,"/Users/tomzahavy/Documents/Claude/collatz/machine1")
import onedim
from collections import Counter

# run the F-orbit, collect frac(log2 D) at high resolution
D=17; N=30000; frac=[]
# also collect the branch: n_A (the dominant word exponent) which drives the jump
for _ in range(N):
    b=D.bit_length()
    top=D>>max(0,b-64)
    fl=(math.log2(top)+(b-top.bit_length())-(b-1))%1.0
    frac.append(fl)
    D=onedim.F(D)[0]

B=40; hist=[0]*B
for f in frac: hist[min(B-1,int(f*B))]+=1
exp=len(frac)/B
chi2=sum((h-exp)**2/exp for h in hist)
print(f"mantissa histogram ({B} bins, {N} cycles), chi2={chi2:.0f} (uniform crit ~55):")
# print a compact ASCII profile
mx=max(hist)
for i in range(B):
    bar="#"*int(40*hist[i]/mx)
    print(f"  [{i/B:.3f},{(i+1)/B:.3f}) {hist[i]/exp:5.2f}  {bar}")
