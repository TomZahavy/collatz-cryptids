"""WS2 counts: exact A_j(x) at astronomical x, against the rigorous bound.

Every number printed here is an EXACT count, not a sample: by L1 the depth-<=L
backward walk from the powers of 2 below 3^L x is complete, so the enumeration
misses no seed.  That is what replaces the heuristic ceiling in
explorations/backward.py.
"""
import math

from density import bound, halting_seeds

XS = [10 ** 6, 10 ** 12, 10 ** 24, 10 ** 48, 10 ** 96, 10 ** 192]
L = 5

print(f"exact counts A_j(x) = #{{b <= x : F^j(b) is a power of 2, j minimal}}, "
      f"depth j <= {L}\n")
head = "        x |" + "".join(f"  A_{j}" for j in range(L + 1)) + \
       "  |  total |   rigorous bound  | log2 x"
print(head)
print("-" * len(head))
rows = []
for x in XS:
    layers = halting_seeds(x, L)
    counts = [len(s) for s in layers]
    tot = sum(counts)
    rows.append((x, counts, tot))
    print(f" 10^{len(str(x)) - 1:>3} |" + "".join(f" {c:>4}" for c in counts) +
          f"  | {tot:>6} | {bound(x, L):>17.3g} | {math.log2(x):8.1f}")

print("\ngrowth: the total is fitted against powers of log2(x)")
for i in range(1, len(rows)):
    x0, _, t0 = rows[i - 1]
    x1, _, t1 = rows[i]
    if t0 and t1:
        e = math.log(t1 / t0) / math.log(math.log2(x1) / math.log2(x0))
        print(f"  10^{len(str(x0)) - 1} -> 10^{len(str(x1)) - 1}: "
              f"total scales like (log2 x)^{e:.2f}")

x = rows[-1][0]
print(f"\nfor comparison, x^c would need c = "
      f"{math.log(rows[-1][2]) / math.log(x):.2e} -- the halting seeds are "
      f"polylogarithmic, not merely of density zero")

print("\nsmallest halting seeds by depth (x = 10^6):")
for j, s in enumerate(halting_seeds(10 ** 6, L)):
    print(f"  depth {j}: {sorted(s)[:8]}{' ...' if len(s) > 8 else ''}")
