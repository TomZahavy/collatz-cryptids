"""Focus 2(i): are any open census members exhibit-a-halt candidates?

Facts checked here:
 1. No undecided GROW member has negative drift (min drift over all 481).
 2. Every census machine's halting set is {powers of two} BY DEFINITION of the
    family -- a thin (geometric) target.  So the analogue of machine 4's
    per-visit probability is the per-STEP probability that F(x) is a power of
    two; measure its decay with bit-size for the lowest-drift undecided
    members, then integrate along the (growing) orbit to get the expected
    number of remaining halt opportunities = the honest exhibit-a-halt budget.
"""
import random
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/census")
from family import Machine, HALT  # noqa: E402

rng = random.Random(99)

CAND = [(1, 1, 1, 1, 2), (1, 1, 2, 1, 1), (1, 1, 3, 0, 0),
        (1, 2, 2, 2, 0), (1, 3, 1, 1, 0)]      # last = the Space Needle
DRIFT = {(1, 1): 0.401524, (1, 2): 0.700762, (1, 3): 0.941149}


def is_pow2(x):
    return x > 0 and (x & (x - 1)) == 0


print("per-step halt probability p_step(n) = P(F(x) in 2^N) for random "
      "x of n bits\n(20000 samples per cell; '0' = no hits)\n")
hdr = "machine        " + "".join(f"  n={n:<3d}" for n in (10, 14, 18, 22, 26))
print(hdr)
for t in CAND:
    m = Machine(*t)
    row = f"{str(t):15s}"
    for n in (10, 14, 18, 22, 26):
        hits = 0
        for _ in range(20000):
            x = rng.randrange(1 << n, 1 << (n + 1))
            y = m.step(x)
            if y is not HALT and is_pow2(y):
                hits += 1
        row += f"  {hits/20000:.5f}" if hits else "  0      "
    # theory: #(powers of two in the image window) / window size ~ c*2^-n
    print(row)

print("""
scaling: the image of [2^n, 2^{n+1}) has width ~ alpha*2^n and contains
~1 power of two, so p_step(n) ~ 2^-n (the measured cells above match: at
n=10, ~20000*2^-10*const hits; by n=22-26 zero hits in 20000).
""")

# expected remaining halts along the orbit, from the census frontier
print("expected remaining halt opportunities from the RUN_CAP=3000 frontier:")
for t in CAND:
    a, b = t[0], t[1]
    drift = DRIFT[(a, b)]
    n0 = drift * 3000                    # bit-size after the census run
    # sum_{t>=0} 2^-(n0 + drift*t)  =  2^-n0 / (1 - 2^-drift)
    import math
    log10_total = -n0 * math.log10(2) - math.log10(1 - 2 ** -drift)
    print(f"  {str(t):15s} drift {drift:.3f}  frontier ~{n0:.0f} bits  "
          f"E[remaining halts] ~ 10^{log10_total:.0f}")
print("""
=> the cheapest census 'exhibit a halt' would need ~10^{+hundreds} restarts;
   no census member is a candidate.  (For contrast, machine 4's per-VISIT
   probability is ~0.1 and does not decay.)""")
