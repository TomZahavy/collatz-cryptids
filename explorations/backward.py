"""Idea 4: backward reachability from the halting set (Space Needle).
Halting <=> orbit reaches a power of 2. Enumerate the HALTING SET (all b whose
orbit reaches a power of 2) by backward BFS from the powers of 2, up to N.
Measure its density and structure; check whether the start b=6 or the forward
orbit can be separated from it."""
import sys, math
sys.path.insert(0,"/Users/tomzahavy/Documents/Claude/collatz/needle")
import needle
from collections import deque

def preimages(t):
    """all b with step1(b)=t (b>=3, not a power of 2)."""
    out=[]
    # odd branch: (5b-3)/2 = t
    if (2*t+3)%5==0:
        b=(2*t+3)//5
        if b>=3 and b%2==1 and not needle.is_pow2(b): out.append(b)
    # even branch: 2^v * m + v + 3(m-1)/2 = t, m odd>=1, v>=1
    v=1
    while 2**v <= 2*t:
        num=2*t-2*v+3; den=2**(v+1)+3
        if num>0 and num%den==0:
            m=num//den
            if m>=1 and m%2==1:
                b=2**v*m
                if b>=3 and not needle.is_pow2(b): out.append(b)
        v+=1
    return out

N=2_000_000
CEIL=2**44           # allow orbits that halt at 2^k up to CEIL (completeness)
halting=set(); q=deque()
k=2
while 2**k<=CEIL:                   # seed from ALL powers of 2 up to CEIL
    q.append(2**k); k+=1
while q:
    t=q.popleft()
    for b in preimages(t):
        if b<=CEIL and b not in halting:   # allow intermediates up to CEIL
            halting.add(b); q.append(b)
halting={b for b in halting if b<=N}       # record only seeds <= N
print(f"halting set (backward-reachable from powers of 2) below {N}: {len(halting)} values")
print(f"  density = {len(halting)/N:.2e}")
sm=sorted(halting)[:20]
print(f"  smallest halting seeds: {sm}")
print(f"  is start b=6 in the halting set? {6 in halting}")
# density by dyadic scale
print("  density by scale [2^k,2^{k+1}):")
for k in range(3,21):
    lo,hi=2**k,2**(k+1)
    c=sum(1 for x in halting if lo<=x<hi)
    print(f"    2^{k:2d}: {c:5d}  ({c/(hi-lo):.2e})")
