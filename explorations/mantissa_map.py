"""The mantissa m_k = frac(log2 D_k) evolves by an explicit circle map.
F(D) = 16D - 240*2^n + 32n + 169 (dominant word), n = n_A(1,D). Leading:
log2 F(D) = 4 + log2 D + log2(1 - 15*2^n / D + ...), so
  m -> m + log2(1 - 15 * 2^(n - log2 D))  (mod 1),
a circle map driven by the fractional relation of 2^n to D (i.e. by m itself).
Characterize the map and its transition."""
import sys, math
sys.path.insert(0,"/Users/tomzahavy/Documents/Claude/collatz/machine1")
import onedim

D=17; pairs=[]; N=40000
for _ in range(N):
    b=D.bit_length(); top=D>>max(0,b-64)
    m=(math.log2(top)+(b-top.bit_length())-(b-1))%1.0
    n=onedim.n_A(1,D)                       # dominant-word exponent
    # relation of n to bits(D): measure the offset
    off = n - (b-1)                          # how n sits vs floor(log2 D)
    D2=onedim.F(D)[0]
    b2=D2.bit_length(); top2=D2>>max(0,b2-64)
    m2=(math.log2(top2)+(b2-top2.bit_length())-(b2-1))%1.0
    pairs.append((m,m2,off))
    D=D2

# where is the map discontinuous? bin m, look at mean m2 and the offset n-floor(log2 D)
from collections import defaultdict
bins=defaultdict(list); offs=defaultdict(list)
for m,m2,off in pairs:
    bins[int(m*24)].append(m2); offs[int(m*24)].append(off)
print("m-bin   mean m'   n-floor(log2 D) offset (mode)")
for k in sorted(bins):
    import statistics
    mo=statistics.mode(offs[k])
    print(f"  [{k/24:.3f},{(k+1)/24:.3f})  m'={statistics.mean(bins[k]):.3f}  offset={mo}  (share off={mo}: {offs[k].count(mo)/len(offs[k]):.2f})")

# find the exact m where the offset n-floor(log2 D) jumps
xs=sorted((m,off) for m,m2,off in pairs)
prev=None
print("\noffset transitions (mantissa where n - floor(log2 D) changes):")
seen=set()
for m,off in xs:
    if off!=prev and prev is not None:
        print(f"   near m={m:.4f}: offset {prev} -> {off}")
    prev=off
