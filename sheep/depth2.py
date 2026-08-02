"""The sheep machine at depth 2: which branch can be second-to-last?

Depth 1 (sheep.py, S3) asked which branch v can produce a power of two, and
answered v in {0,1}.  Depth 2 asks which branch v can produce a value that is
itself a one-step halt predecessor, i.e. a member of

    H_0 = {(2^(2j+1) + 1)/3 : j >= 2}      (the v = 0 halting family)
    H_1 = {2(2^(4j) - 1)/5  : j >= 2}      (the v = 1 halting family)

THE CRITERIA.  Write N for the family member.  Since 3*N = 2^(2j+1) + 1 and
5*N = 2^(4j+1) - 2 identically, "N = B_v (mod A_v)" clears denominators into

    D2-H0(v):   2^(2j+1) = 3*B_v - 1   (mod 3*A_v)   for some j
    D2-H1(v):   2^(4j+1) = 5*B_v + 2   (mod 5*A_v)   for some j

with no side condition on gcd(3, A_v) or gcd(5, A_v) -- clearing denominators
into the larger modulus handles both uniformly.  (3 does divide A_v whenever v
is even, so the naive reduction mod A_v would be wrong half the time.)

Branch v survives depth 2 iff D2-H0(v) or D2-H1(v) holds.  The right-hand
sides range over the COSETS

    2*<4>  (mod 3*A_v)        and        2*<16>  (mod 5*A_v),

and these are thin for the same reason the depth-1 group was: A_v =
2^(v+1) + 1 forces the order of 2 to stay O(v) while the modulus grows like
2^v.  So the depth-2 sieve is again a listable-group gap problem -- the shape
that closed machine 3's depth-2 question (M3-N2).

WHAT THIS CAN AND CANNOT DO.  A depth-d sieve forbids branch WORDS; it cannot
decide the machine, because the surviving branches carry positive mass at
every depth.  What it can do is measure how fast the surviving word set
thins, which is the quantity the pseudorandom heuristic assumes and has never
been measured for this family.
"""
import sys
from math import gcd

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/census")
from family import Machine, HALT                                  # noqa: E402
from sheep import f, is_pow2, v2, H0, H1, survives                # noqa: E402

MACH = Machine(1, 1, 1, 1, 0)


def A(v):
    return (1 << (v + 1)) + 1


def B(v):
    return (1 << v) + v


def coset(base, step, M, cap=None):
    """{ base * step^i mod M : i >= 0 } -- the coset base*<step>."""
    out, x = set(), base % M
    while x not in out:
        out.add(x)
        x = (x * step) % M
        if cap and len(out) > cap:
            break
    return out


def d2_h0(v):
    """Can branch v land on H_0?  2^(2j+1) = 3B_v - 1 (mod 3A_v)."""
    M = 3 * A(v)
    return (3 * B(v) - 1) % M in coset(2, 4, M)


def d2_h1(v):
    """Can branch v land on H_1?  2^(4j+1) = 5B_v + 2 (mod 5A_v)."""
    M = 5 * A(v)
    return (5 * B(v) + 2) % M in coset(2, 16, M)


def d2(v):
    return d2_h0(v) or d2_h1(v)


def exceptional_d2(a):
    """The oddPart = 3 branch at depth 2: is 3*2^a + a + 3 in H_0 u H_1?"""
    y = 3 * (1 << a) + a + 3
    if y % 2 == 1:                       # candidate for H_0
        return (3 * y - 1) & (3 * y - 2) == 0 and (3 * y - 1) > 0
    return False


def in_H0(n):
    """n in H_0 = {(2^(2j+1)+1)/3 : j >= 2}.  The j >= 2 floor matters: j = 1
    gives 3, whose oddPart is 3, so it takes the EXCEPTIONAL branch and is not
    a halt predecessor at all (f(3) = 6, not 4).  2^(2j+1) has even
    bit_length 2j+2, so j >= 2 is bit_length >= 6."""
    t = 3 * n - 1
    return (t > 0 and (t & (t - 1)) == 0 and t.bit_length() % 2 == 0
            and t.bit_length() >= 6)


def in_H1(n):
    """n in H_1 = {2(2^(4j)-1)/5 : j >= 2}.  Same floor: j = 1 gives 6, again
    oddPart 3 (f(6) = 10, not 8).  bit_length of 2^(4j+1) is 4j+2, so j >= 2
    is bit_length >= 10."""
    t = 5 * n + 2
    return (t > 0 and (t & (t - 1)) == 0 and t.bit_length() % 4 == 2
            and t.bit_length() >= 10)


if __name__ == "__main__":
    import time
    t0 = time.time()
    P = lambda *a: print(*a, flush=True)
    P("=" * 74)
    P("THE SHEEP MACHINE AT DEPTH 2")
    P("=" * 74)

    # ---- 0. the membership tests, against the generators -----------------
    bad = 0
    for j in range(2, 60):
        if not in_H0(H0(j)):
            bad += 1
        if not in_H1(H1(j)):
            bad += 1
    for n in range(2, 400000):
        if in_H0(n) != any(H0(j) == n for j in range(2, 12)):
            bad += 1
        if in_H1(n) != any(H1(j) == n for j in range(2, 8)):
            bad += 1
    assert bad == 0
    P(f"\n0.  membership tests in_H0 / in_H1 agree with the generators "
      f"(j <= 60, and every n < 400000): {bad} mismatches")

    # ---- 1. the depth-2 survivor set -------------------------------------
    VMAX = 400
    s0 = [v for v in range(VMAX) if d2_h0(v)]
    s1 = [v for v in range(VMAX) if d2_h1(v)]
    surv2 = sorted(set(s0) | set(s1))
    P(f"\n1.  depth-2 sieve, v < {VMAX}")
    P(f"      branches that can reach H_0: {s0}")
    P(f"      branches that can reach H_1: {s1}")
    P(f"      SURVIVING at depth 2: {surv2}")
    P(f"      (depth 1 survivors, for comparison: "
      f"{[v for v in range(VMAX) if survives(v)]})")

    # ---- 2. ground truth --------------------------------------------------
    BOUND = 4_000_000
    hits = []
    for x in range(2, BOUND):
        y = f(x)
        if y is HALT:
            continue
        z = f(y)
        if z is not HALT and is_pow2(z):
            hits.append((x, v2(x), (x >> v2(x)), y))
    P(f"\n2.  brute force, x < {BOUND}: values halting in exactly two steps")
    for x, v, m, y in hits:
        fam = "H_0" if in_H0(y) else ("H_1" if in_H1(y) else "?")
        P(f"      x = {x:9d}  v_2 = {v}  oddPart = {m:9d}  -> y = {y:9d} "
          f"({fam}) -> halt")
    obs = sorted({v for _, v, m, _ in hits if m > 3})
    P(f"      generic-branch valuations observed: {obs}")
    assert set(obs) <= set(surv2), (obs, surv2)
    P(f"      every observed valuation is predicted by the sieve: "
      f"{set(obs) <= set(surv2)}")

    # ---- 3. the exceptional branch at depth 2 -----------------------------
    exc = [a for a in range(0, 4000)
           if in_H0(3 * (1 << a) + a + 3) or in_H1(3 * (1 << a) + a + 3)]
    P(f"\n3.  exceptional branch (oddPart = 3) at depth 2: "
      f"3*2^a + a + 3 in H_0 u H_1 for a < 4000? {exc}")
    P(f"      (a = 0 gives 6, which satisfies the raw family formula at j = 1 "
      f"but is exactly the excluded oddPart-3 member: f(6) = 10, not 8.  The "
      f"j >= 2 floor in in_H0/in_H1 removes it.)")
    P(f"\n    NOTE on d2_h0 / d2_h1: those criteria range over ALL j, "
      f"including the excluded j = 0, 1.  They are therefore an "
      f"OVER-approximation of the survivor set, which only strengthens the "
      f"non-existence theorem in section 6; ladder.py recomputes the same "
      f"survivor set with the j floor enforced exactly and agrees.")

    # ---- 4. how thin is it? ----------------------------------------------
    P(f"\n4.  what the two depths buy (geometric branch law P(v) = "
      f"2^-(v+1))")
    m1 = sum(2.0 ** -(v + 1) for v in range(VMAX) if survives(v))
    m2 = sum(2.0 ** -(v + 1) for v in surv2)
    P(f"      depth 1: surviving mass {m1:.6f}  (forbidden {1 - m1:.6f})")
    P(f"      depth 2: surviving mass {m2:.6f}  (forbidden {1 - m2:.6f})")
    P(f"      mass of admissible LAST-TWO-STEP words = "
      f"{m2:.6f} * {m1:.6f} = {m2 * m1:.6f}")
    P(f"      i.e. {1 - m1 * m2:.4%} of consecutive branch pairs can never "
      f"be the last two steps before a halt")

    # ---- 5. the group sizes, which is why it is thin ---------------------
    P(f"\n5.  why: the target cosets are thin (|coset| / modulus)")
    P(f"      {'v':>4} {'3A_v':>10} {'|2<4>|':>8} {'ratio':>10}   "
      f"{'5A_v':>10} {'|2<16>|':>8} {'ratio':>10}")
    for v in list(range(0, 9)) + [12, 16, 20, 30, 40]:
        M0, M1 = 3 * A(v), 5 * A(v)
        c0, c1 = len(coset(2, 4, M0)), len(coset(2, 16, M1))
        P(f"      {v:4d} {M0:10d} {c0:8d} {c0 / M0:10.6f}   "
          f"{M1:10d} {c1:8d} {c1 / M1:10.6f}")

    # ---- 6. THE PROOF ----------------------------------------------------
    P(f"\n6.  SHEEP-D2 [proved]: no branch v >= 6 can be second-to-last")
    P(f"      Reduce each criterion modulo A_v (a necessary condition), using")
    P(f"      2^(v+1) = -1, so <2> = {{2^i}}_(i<=v) u {{A_v - 2^i}}_(i<=v), and the")
    P(f"      exponent parity of each element is well defined because")
    P(f"      2^(v+1) = -1 forces ord_(A_v)(2) to be EVEN.")
    P(f"        H_0 target:  3B_v - 1 = 3*2^v + 3v - 1 = 2^v + 3v - 2  (mod A_v)")
    P(f"        H_1 target:  5B_v + 2 = 5*2^v + 5v + 2 = 2^v + 5v      (mod A_v)")
    P(f"      (using 3*2^v = 2^(v+1) + 2^v = 2^v - 1 and 5*2^v = 2^(v+2) + 2^v")
    P(f"       = 2^v - 2.)  Each target must be +-2^i, giving two gap cases:")
    P(f"        H_0 case A:  2^v + 3v - 2 = 2^i    -- impossible for v >= 4,")
    P(f"                     since 2^v < 2^v + 3v - 2 < 2^(v+1)")
    P(f"        H_0 case B:  2^i = 2^v - 3v + 3    -- impossible for v >= 5,")
    P(f"                     since 2^(v-1) < 2^v - 3v + 3 < 2^v")
    P(f"        H_1 case A:  2^v + 5v = 2^i        -- impossible for v >= 5")
    P(f"        H_1 case B:  2^i = 2^v - 5v + 1    -- impossible for v >= 6;")
    P(f"                     v = 5 gives 32 - 25 + 1 = 8 = 2^3, a REAL hit")
    P(f"      so v >= 6 is excluded and v <= 5 is finite, checked directly.")
    bad = 0
    for v in range(4, 6000):
        t0h = (1 << v) + 3 * v - 2
        if (t0h & (t0h - 1)) == 0:
            bad += 1                              # H_0 case A must never fire
        r = (1 << v) - 3 * v + 3
        if v >= 5 and r > 0 and (r & (r - 1)) == 0:
            bad += 1                              # H_0 case B, v >= 5
    for v in range(5, 6000):
        t1h = (1 << v) + 5 * v
        if (t1h & (t1h - 1)) == 0:
            bad += 1                              # H_1 case A
        r = (1 << v) - 5 * v + 1
        if v >= 6 and r > 0 and (r & (r - 1)) == 0:
            bad += 1                              # H_1 case B, v >= 6
    assert bad == 0
    P(f"      gap inequalities re-checked for every v < 6000: {bad} violations")
    P(f"      v = 5 exception confirmed: 2^5 - 5*5 + 1 = "
      f"{(1 << 5) - 25 + 1} = 2^3")
    big = [v for v in range(400, 3000) if d2(v)]
    P(f"      and the criteria themselves, 400 <= v < 3000: survivors {big}")
    assert big == []
    P(f"\n      THEOREM.  The depth-2 survivor set is exactly {{0,1,2,3,5}}.")
    P(f"      Compare depth 1, exactly {{0,1}} (S3).  Both are finite and")
    P(f"      explicit; machine 3's M3-N2 gave the analogous statement only as")
    P(f"      'v_3 = 1 for the last two steps'.")

    P(f"\n[{time.time() - t0:6.1f}s] done")
