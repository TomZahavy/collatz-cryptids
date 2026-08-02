"""Two diagnostics: (a) is the skew visible in the residues themselves, at every
depth?  (b) does the same order-arithmetic predict machine 3's root branching?"""
import sys, random
from collections import Counter
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/machine3")
import tree_deficit as td
from machine3_map import branch

# ---- (a) residue distribution of tree nodes, by depth, mod 5 and mod 7 ------
def profile(roots, mod, maxdepth=3):
    out = []
    frontier = list(roots)
    for d in range(maxdepth + 1):
        if not frontier:
            break
        cnt = Counter(y % mod for y in frontier)
        out.append((d, len(frontier), [cnt.get(r, 0) for r in range(mod)]))
        frontier = [b for y in frontier for b in td.preimages_needle(y)]
    return out

td.preimages_needle = __import__("density").preimages
pows = [1 << m for m in range(3190)]
rng = random.Random(7)
rand = [rng.randrange(1 << 1599, 1 << 1600) for _ in range(3190)]

for mod in (5, 7):
    print(f"\n=== node residues mod {mod}  (uniform would be ~1/{mod} each) ===")
    print(f"  target class c(v) for v with A(v)={mod}: "
          f"{td.c(0) % 5 if mod == 5 else td.c(1) % 7}")
    for name, roots in (("powers of 2", pows), ("random", rand)):
        print(f"  {name}:")
        for d, n, cnt in profile(roots, mod):
            frac = "  ".join(f"{k/n:.3f}" for k in cnt)
            print(f"    depth {d}  n={n:>5}   {frac}")

# ---- (b) machine 3: same order argument at the root ------------------------
print("\n=== machine 3: branching off a power of 27, predicted ===")
tot_pred = tot_int = 0.0
rows = []
for j in range(14):
    for r in (1, 2):
        A, B = branch(j, r)
        tgt = B % A
        # order of 27 mod A, and whether tgt lies in <27>
        o, t, dens = 1, 27 % A, 0.0
        seen = {t}
        while True:
            if t == tgt:
                dens = None          # fill after we know the order
                break
            t = (t * 27) % A
            if t in seen:
                break
            seen.add(t); o += 1
        # recompute true order
        o2, t2 = 1, 27 % A
        while t2 != 1 % A and o2 <= A:
            t2 = (t2 * 27) % A; o2 += 1
        hit = any_hit = False
        t3 = 1 % A
        for _ in range(o2):
            if t3 == tgt:
                any_hit = True; break
            t3 = (t3 * 27) % A
        dens = 1.0 / o2 if any_hit else 0.0
        tot_pred += dens; tot_int += 1.0 / A
        if j < 7:
            rows.append((j, r, A, tgt, o2, dens, 1.0 / A))
print("      j  r      A      B mod A   ord_A(27)    density    vs 1/A")
for j, r, A, tgt, o, d, inv in rows:
    flag = "   IMPOSSIBLE" if d == 0 else ""
    print(f"  {j:>5}  {r}  {A:>8}  {tgt:>10}  {o:>9}   {d:>8.5f}  {inv:>8.5f}{flag}")
print(f"  predicted root branching {tot_pred:.4f}   interval model {tot_int:.4f}")
