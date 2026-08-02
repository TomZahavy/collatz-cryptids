"""Idea 5: self-similarity / renormalization.
Space Needle: step(b)=b+v2(b)+(3/2)(oddpart-1). Under b->2b, v2 increments,
oddpart is preserved. Derive and test a scaling/renormalization relation."""
import sys, math
sys.path.insert(0,"/Users/tomzahavy/Documents/Claude/collatz/needle")
sys.path.insert(0,"/Users/tomzahavy/Documents/Claude/collatz/machine3")
import needle

# claim: step1(2b) = step1(b) + b + 1  (for non-halting b)
bad=0
for b in range(3,200000):
    if needle.is_pow2(b): continue
    if needle.step1(2*b) != needle.step1(b)+b+1: bad+=1
print(f"Space Needle scaling  step(2b) = step(b)+b+1: {bad} violations (b<200000)")

# consequence: the ORBIT of 2b vs orbit of b. Does halting of one imply the other?
# 2b is a power of 2 iff b is. So halt-sets are scale-linked. But orbits diverge
# (the +b+1 term). Test: does the odd part evolve self-similarly? Track oddpart.
def oddpart(b):
    while b%2==0: b//=2
    return b
b=6; seq=[]
for _ in range(50):
    seq.append(oddpart(b)); b=needle.step1(b)
print("Space Needle odd-part sequence:", seq[:16])
# is the odd-part map itself a nice map? oddpart(step(b)) vs oddpart(b)?
# step(b)=b+v+3(m-1)/2, m=oddpart(b). For b odd (v=0): step=b+3(b-1)/2=(5b-3)/2.
# oddpart of (5b-3)/2 ... test whether odd-part dynamics closes
print("\nb odd -> step(b)=(5b-3)/2; the odd->? transition:")
for b in [3,5,7,9,11,13,17,19]:
    s=needle.step1(b); print(f"  b={b}: step={s}=2^{needle.v2(s)[0]}*{needle.v2(s)[1]}")

# machine 3 analog: divide by 3. Is there a x3 scaling relation?
import m3_accel as m3
print("\nmachine 3: cstep scaling under a->3a (divide rule R4 acts):")
bad=0
for a in range(2,2000):
    if a%3!=0: continue
    # cstep divides; compare cstep(3a,b) structure -- just note the divide-chain lemma IS the renorm
print("  (the divide-chain lemma b->b+(N-M)+j IS machine 3's renormalization:")
print("   collapsing a=3^j*M by the scale factor 3^j in one exact step.)")
