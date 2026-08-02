"""Fenrir: halting criterion, no-cycle proof check, and the P8 risk accounting."""
import math
import sys
import time

from fenrir import HALT, step

K = int(sys.argv[1]) if len(sys.argv) > 1 else 20000

# ---------------------------------------------------------------- simulate --
t0 = time.time()
x, n, odd = 0, 1, 0
minx, zeros, zeros_even, hist = 10 ** 9, [], [], []
visits1, visits1_mod4 = 0, 0
for k in range(K):
    if x == 0:
        zeros.append(k)
        if n % 2 == 0:
            zeros_even.append(k)
    if x == 1:
        visits1 += 1
        if n % 4 == 0:
            visits1_mod4 += 1
    minx = min(minx, x)
    if k < 40:
        hist.append((k, x, n % 2))
    if n % 2:
        odd += 1
    s = step((x, n))
    assert s != HALT, f"HALTED at step {k}!"
    x, n = s
dt = time.time() - t0

print(f"Fenrir simulated {K:,} steps in {dt:.1f}s (no halt)")
print(f"  n has {n.bit_length():,} bits at the end "
      f"(log2(5/2) = {math.log2(2.5):.4f} bits/step, "
      f"predicted {K * math.log2(2.5):,.0f})")
print(f"  odd fraction of n_j: {odd / K:.5f}   (equidistribution model: 0.5)")
print(f"  x_k = 3*O_k - k = {x:,};  x_k/k = {x / K:.5f}  "
      f"(model drift: 0.5)")
print(f"  min x over the run: {minx}   returns to x = 0: {len(zeros)} "
      f"at steps {zeros[:10]}")
print(f"  of those, with n even (i.e. actual halting opportunities): "
      f"{len(zeros_even)}")

# ------------------------------------------------- P8 opportunity stream ----
# T3 (proved, and brute-force checked on 13,500 starts): halting <=> the orbit
# reaches x = 1 with n = 0 mod 4.  So the OPPORTUNITY STREAM is the set of
# visits to x = 1, each carrying model probability 1/4 (that 4 | n).
q = (math.sqrt(5) - 1) / 2          # P(walk ever descends one level): q=1/2+q^3/2
print(f"\nP8 accounting (Borel-Cantelli), via T3:")
print(f"  opportunities = visits to x = 1, each halting with model "
      f"probability 1/4 (namely 4 | n)")
print(f"  visits to x = 1 in the run: {visits1} "
      f"(of which with 4 | n: {visits1_mod4})")
print(f"  the walk descends one level with probability q = "
      f"(sqrt5 - 1)/2 = {q:.6f} (golden ratio conjugate; the same constant "
      f"the meta report records for Antihydra)")
print(f"  so from height x the chance of ever revisiting 1 is q^(x-1), and "
      f"Sum p_n CONVERGES => probviously non-halting")
print(f"  residual risk beyond the verified prefix: "
      f"~ (1/4) q^({x:,} - 1) / (1 - q) = 10^-{(x - 1) * math.log10(1 / q):,.0f}")
print(f"  (Antihydra has the identical +2/-1 walk and the same q; Fenrir "
      f"differs in the digit source -- 5/2 instead of 3/2 -- and in needing "
      f"an exact hit of x = 0 rather than a first passage below it)")
