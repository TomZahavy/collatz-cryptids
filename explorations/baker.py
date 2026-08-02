"""What's left: the perfect-powers / Baker direction for the multiplicative machines.
Halting = orbit hits q^k. Test whether Baker / S-unit methods can apply, and
extract whatever rigorous partial result is available."""
import sys, math
sys.path.insert(0,"/Users/tomzahavy/Documents/Claude/collatz/needle")
sys.path.insert(0,"/Users/tomzahavy/Documents/Claude/collatz/machine3")
import needle

def factor_small(n, primes=(2,3,5,7,11,13,17,19,23)):
    f={}; 
    for p in primes:
        while n%p==0: f[p]=f.get(p,0)+1; n//=p
    return f, n  # n = remaining cofactor (1 if smooth over `primes`)

# (a) are Space Needle orbit values S-units / smooth? (needed for Baker)
b=6; nonsmooth=None
print("Space Needle orbit factorizations (first 12):")
for i in range(12):
    f,co=factor_small(b)
    smooth = (co==1)
    print(f"  b_{i}={b}: {f}" + ("" if smooth else f" * {co} (NON-SMOOTH prime)"))
    if not smooth and nonsmooth is None: nonsmooth=(i,b,co)
    b=needle.step1(b)
print(f"  => first non-smooth value: b_{nonsmooth[0]}={nonsmooth[1]} has prime factor {nonsmooth[2]}")
print("  => orbit is NOT an S-unit sequence; Baker cannot be applied to the orbit directly.\n")

# (b) the geometric sub-structure: during an ODD run b->(5b-3)/2, we have
#     b_n - 1 = (5/2)^n (b_0 - 1), i.e. 2^n (b_n - 1) = 5^n (b_0 - 1).
print("verify odd-run closed form b_n - 1 = (5/2)^n (b_0-1):")
bad=0
for _ in range(2000):
    import random
    b0=random.randrange(1,10**6)*2+1   # odd
    b=b0; ok=True
    for n in range(1,6):
        if b%2==0: ok=False; break
        b=(5*b-3)//2
        if 2**n*(b-1)!=5**n*(b0-1): bad+=1
print(f"  closed form violations: {bad}")

# (c) LTE constraint: halting b_n=2^k during an odd run of length n needs
#     5^n | (2^k - 1), forcing k >= 4*5^(n-1) (v5(2^k-1)=1+v5(k/4) for 4|k).
print("\nLTE constraint: to halt (b_n=2^k) after an odd run of length n,")
print("  need 5^n | (2^k - 1) => k >= 4*5^(n-1):")
for n in range(1,6):
    kmin=4*5**(n-1)
    # b_n ~ (5/2)^n b_0, so k ~ log2(b_0)+1.32n; need k>=kmin => b_0 huge
    b0_needed = 2**(kmin - int(1.32*n))
    print(f"  n={n}: k >= {kmin};  run must START at b_0 >= ~2^{kmin-int(1.32*n)} "
          f"({'astronomically large' if n>=3 else 'large' if n==2 else 'trivial'})")
print("  => a halt cannot occur in the MIDDLE of a geometric run at moderate scale;")
print("     it must land on a power essentially at a run boundary. (Verified: LTE exact.)")

# verify the LTE valuation formula v5(2^k-1) = 1 + v5(k/4) for 4|k
bad=0
def v5(x):
    v=0
    while x%5==0: x//=5; v+=1
    return v
for k in range(4,4000,4):
    if v5(2**k-1) != 1+v5(k//4): bad+=1
print(f"  LTE v5(2^k-1)=1+v5(k/4) for 4|k: {bad} violations")
