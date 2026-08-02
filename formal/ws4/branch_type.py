"""WS4.2 -- the fault line, made checkable.

The decidability literature for one-dimensional piecewise-affine maps (PAM)
assumes two things that our machines are claimed to violate:

  (H1) FINITELY MANY PIECES, cut out by intervals;
  (H2) INJECTIVITY (the hypothesis under which 1D PAM reachability was shown
       decidable, LICS 2023).

"Claimed" is not good enough for a hardness write-up, so both are settled here
by computation against the machines' own verified step functions.

What is proved here (each also machine-verified over a stated range):

  P1  The Needle map is affine on each valuation branch with slope
          s_v = (2^(v+1) + 3) / 2^(v+1) = 1 + 3*2^-(v+1)
      and intercept  v - 3/2.  The slopes are pairwise distinct and accumulate
      at 1, so the slope SET IS INFINITE and no finite-piece refinement exists:
      a map with finitely many affine pieces has finitely many slopes.
      Machine 3: slope 1 + 3^-(j+1), intercept  j + c_r - r/3.

  P2  Neither map is injective: explicit collisions are exhibited.

So the two hypotheses fail independently, and (H1) fails for a structural
reason rather than a presentational one.  Note the direction: the slopes tend
to 1, i.e. the high-valuation branches are nearly the identity -- the map is
expanding on average but its pieces are individually almost neutral.

Run: python3 branch_type.py
"""
from fractions import Fraction
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/machine3")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/automatic")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/density")

import needle                                              # noqa: E402
import machine3_map                                        # noqa: E402


# ---------------------------------------------------------------- P1, Needle
def needle_affine(v):
    """(slope, intercept) claimed for the branch v_2(x) = v."""
    return Fraction(2 ** (v + 1) + 3, 2 ** (v + 1)), Fraction(2 * v - 3, 2)


def check_needle_affine(hi=200000):
    """F(x) = s_v * x + t_v exactly, for every non-halting x < hi."""
    bad = 0
    seen = set()
    for x in range(2, hi):
        if needle.is_pow2(x):
            continue
        y = needle.step1(x)
        v, _ = needle.v2(x)
        s, t = needle_affine(v)
        if s * x + t != y:
            bad += 1
        seen.add(v)
    return bad, max(seen)


# --------------------------------------------------------------- P1, machine 3
def m3_affine(j, r):
    c_r = 3 if r == 1 else 4
    return Fraction(3 ** (j + 1) + 1, 3 ** (j + 1)), Fraction(3 * (j + c_r) - r, 3)


def check_m3_affine(hi=200000):
    bad = 0
    seen = set()
    for a in range(2, hi):
        j, M = machine3_map.v3(a)
        m, r = divmod(M, 3)
        if r == 0 or (m == 0 and r == 1):
            continue                                   # not in the map's domain
        y = machine3_map.G(a)
        s, t = m3_affine(j, r)
        if s * a + t != y:
            bad += 1
        seen.add(j)
    return bad, max(seen)


# ------------------------------------------------------------------------ P2
def first_collision(step, hi, skip):
    """Smallest y with two distinct preimages < hi under `step`."""
    hit = {}
    for x in range(2, hi):
        if skip(x):
            continue
        y = step(x)
        if y in hit:
            return hit[y], x, y
        hit[y] = x
    return None


def main():
    print("WS4.2  BRANCH TYPE AND THE TWO FAILED HYPOTHESES\n")

    print("P1  affine-per-branch form, verified against the machines' own steps")
    bad, vmax = check_needle_affine()
    print(f"  Needle    F(x) = (1 + 3/2^(v+1)) x + (v - 3/2)   on v_2(x) = v")
    print(f"            mismatches over 2 <= x < 200,000: {bad}   (branches v = 0..{vmax})")
    bad3, jmax = check_m3_affine()
    print(f"  machine 3 G(a) = (1 + 3^-(j+1)) a + (j + c_r - r/3) on v_3(a) = j")
    print(f"            mismatches over 2 <= a < 200,000: {bad3}   (branches j = 0..{jmax})")
    print()
    print("  slopes (exact, distinct, accumulating at 1):")
    print("    Needle    " + ", ".join(str(needle_affine(v)[0]) for v in range(6)) + ", ... -> 1")
    print("    machine 3 " + ", ".join(str(m3_affine(j, 1)[0]) for j in range(6)) + ", ... -> 1")
    ns = {needle_affine(v)[0] for v in range(400)}
    ms = {m3_affine(j, 1)[0] for j in range(400)}
    print(f"    distinct slopes among the first 400 branches: "
          f"Needle {len(ns)}, machine 3 {len(ms)}  (i.e. all of them)")
    print("  => the slope set is infinite; a finitely-piecewise-affine map has a")
    print("     finite slope set; so (H1) fails and no refinement can repair it.\n")

    print("P2  injectivity")
    c = first_collision(needle.step1, 200000, needle.is_pow2)
    print(f"  Needle    F({c[0]}) = F({c[1]}) = {c[2]}"
          if c else "  Needle    no collision below 200,000")
    if c:
        v0, _ = needle.v2(c[0])
        v1, _ = needle.v2(c[1])
        print(f"            v_2 = {v0} and {v1}: two different branches land on one value.")

    def m3_skip(a):
        j, M = machine3_map.v3(a)
        m, r = divmod(M, 3)
        return r == 0 or (m == 0 and r == 1)

    c3 = first_collision(machine3_map.G, 200000, m3_skip)
    print(f"  machine 3 G({c3[0]}) = G({c3[1]}) = {c3[2]}"
          if c3 else "  machine 3 no collision below 200,000")
    if c3:
        print(f"            v_3 = {machine3_map.v3(c3[0])[0]} and "
              f"{machine3_map.v3(c3[1])[0]}.")
    print("  => (H2) fails too; the injective-PAM decidability route is blocked")
    print("     independently of the piece-count obstruction.")


if __name__ == "__main__":
    main()
