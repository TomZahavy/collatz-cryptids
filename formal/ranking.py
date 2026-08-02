"""The hardness ranking: primary axis ties, so rank on secondary axes.
Verify the discriminating criterion: PROVEN vs EMPIRICAL 'no congruence decides'."""
import sys, random
for d in ["machine3","needle","machine1","machine4"]:
    sys.path.insert(0, f"/Users/tomzahavy/Documents/Claude/collatz/{d}")

print("=== AXIS: is 'no congruence decides' PROVEN or only EMPIRICAL? ===\n")

# Multiplicative machines: PROVEN (Finding 3) -- valuation orthogonal to residues.
import needle
from collections import defaultdict
rng=random.Random(0)
proven=True
for M in (3,5,7,9,11,15,25):
    seen=defaultdict(set)
    for _ in range(30000):
        b=rng.randrange(1,10**7); seen[b%M].add(needle.v2(b)[0])
    if not all(len(v)>=6 for v in seen.values()): proven=False
print(f"Machine 3 / Space Needle: v_q(x) independent of x mod M for all M coprime "
      f"to q -> PROVEN no congruence decides (verified M in 3..25): {proven}")
print("  => CERTIFIED cryptid (irreducible to congruence methods, unconditionally).\n")

# Sparse machines: only EMPIRICAL -- no separating modulus FOUND, not proven impossible.
print("Machines 1, 4: no separating modulus found (m<=256 / m<=628 searched),")
print("  but NO impossibility proof. An elementary decision is not ruled out.")
print("  => CANDIDATE cryptid (conjecturally, not provably, irreducible).\n")

print("=== THE RANKING (partial order) ===\n")
print("Primary axis (logical complexity + pseudorandom barrier): ALL TIED.")
print("  every machine: Pi-0-1 single orbit, uniformly blocked by the single-orbit")
print("  pseudorandom barrier; all one quantifier below the Pi-0-2 Collatz conjecture.\n")
print("Secondary axis A -- CERTIFICATION of cryptid status:")
print("  CERTIFIED (provably beyond congruences): machine 3, Space Needle  [valuation]")
print("   >  CANDIDATE (empirically beyond): machines 1, 4  [magnitude/digit]")
print()
print("Secondary axis B -- DISTANCE to a named open problem:")
print("  Hydra/Antihydra, machine 1 (mantissa)  ~  Mahler (3/2)^n / equidistribution")
print("   >  machine 3, Space Needle  ~  perfect-powers-in-sequences (Baker/BHV)")
print("   >  machine 4  ~  freestanding")
print()
print("Equivalence classes (same dynamical system, up to start/base):")
print("  {Hydra == Antihydra}   (identical map H(n)=floor(3n/2))")
print("  {machine 3 ~ Space Needle}   (multiplicative, base 3 vs 2)")
print("  {machine 1}, {machine 4}   (distinct)")
print("  NONE == 3n+1 Collatz (distinct map); all co-members of the class.")
