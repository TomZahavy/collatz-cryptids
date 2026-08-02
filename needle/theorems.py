"""Space Needle through the toolkit.

T1 (halting criterion).  The one-variable orbit from b = 6 halts iff it reaches
   an exact power of 2.  This is the MULTIPLICATIVE-coincidence type of the
   collection's taxonomy -- the archetype our machine 3 mirrors with powers of
   3 instead of 2.

T2 (no cycles: b is its own potential).  For any non-halting b, the odd part
   m >= 3, so b -> b + v(b) + 3(m-1)/2 increases b by at least 3.  Hence b is
   strictly increasing and the machine cannot cycle: it halts or escapes to
   infinity.  (Even simpler than machine 3, whose a was not monotone and needed
   Phi = a + b; here the single state variable is the potential, as for the
   Hydra family.)

T3 (branch statistic).  The branch is v(b), the 2-adic valuation of b.  Under
   the uniform-low-bits heuristic P(v = k) = 2^-(k+1); measured, it matches --
   the same geometric valuation law as machine 3 (base 3) and the
   Collatz shortcut.

T4 (growth / the divergent-cryptid heuristic).  When b is odd (v = 0, half the
   time) b -> ~5b/2; averaging over the valuation law the per-step log-growth
   is a constant ~0.652 (so b ~ 1.92^n), matching the wiki.  Powers of 2 are
   spaced by x2 while b grows by ~x1.92 per step, so the orbit passes about one
   power-of-2 scale per step; the chance of landing EXACTLY on one decays like
   1/b, a convergent sum.  Probviously non-halting, of divergent type -- the
   same shape as machine 3 and (by construction) its namesake.
"""
from needle import step1, v2, is_pow2, HALT
import math
from collections import Counter


if __name__ == "__main__":
    # ---- T1 / T2: monotonicity and the halt gateway ----
    b = 6
    prev = b
    for _ in range(200000):
        nb = step1(b)
        if nb == HALT:
            print("halted (unexpected):", b)
            break
        assert nb > prev, (b, nb)
        prev = b = nb
    assert not any(is_pow2(x) for x in [b])           # still not a power of 2
    # increment >= 3 for all non-halting b
    mn = min(step1(x) - x for x in range(3, 300000) if not is_pow2(x))
    assert mn >= 3
    print(f"T2  b strictly increases (min increment {mn}); no cycles: OK")

    # ---- T3: valuation distribution ----
    b = 6
    val = Counter()
    logs = []
    N = 200000
    for _ in range(N):
        v, m = v2(b)
        val[v] += 1
        nb = step1(b)
        if nb == HALT:
            break
        logs.append(math.log(nb) - math.log(b))
        b = nb
    tot = sum(val.values())
    print("T3  v(b) distribution vs 2^-(k+1):")
    for k in range(6):
        print(f"      v={k}: {val[k] / tot:.4f}   model {2 ** -(k + 1):.4f}")

    # ---- T4: growth constant ----
    avg = sum(logs) / len(logs)
    print(f"\nT4  mean per-step log-growth = {avg:.6f} "
          f"(wiki 0.652355; e^avg = {math.exp(avg):.5f}, wiki 1.92006)")
    print(f"     b reached {b.bit_length()} bits in {N} steps; "
          f"max valuation seen = {max(val)}; power of 2 hit: "
          f"{'YES' if is_pow2(b) else 'no'}")
