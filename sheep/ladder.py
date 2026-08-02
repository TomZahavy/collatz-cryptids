"""The sheep machine's depth ladder: exact preimages of the halting set.

THE POINT.  Depth 1 forbids every branch with v >= 2 (sheep.py, S3); depth 2
forbids every v >= 6 except that v = 5 slips through (depth2.py, SHEEP-D2).
Both survivor sets are finite and explicit.  The question this file answers is
how the ladder behaves as a whole -- how fast the admissible branch WORDS thin
-- because that rate is exactly the quantity the pseudorandom non-halting
heuristic assumes and has never been measured for this family.

THE REPRESENTATION.  Call a set of the shape

        N(i) = (A * 2^(e*i) + b) / c ,      i >= i_min,  c odd

a *geometric family*.  The halting set at depth 0 is the single family
2^i = (1 * 2^(1*i) + 0)/1.  The key fact is that this shape is CLOSED under
taking preimages along a generic branch:

    x = 2^v (2k+1) with k >= 2 satisfies f(x) = N(i)
      <=>  A_v k + B_v = N(i)
      <=>  c (A_v k + B_v) = A * 2^(e i) + b
      <=>  A * 2^(e i)  =  c B_v - b   (mod c A_v)                      (*)

and c A_v is odd, so 2 is invertible and (*) is a discrete-log condition whose
solution set is a union of residue classes i = i_0 (mod P), P = ord(2^e).
Substituting i = i_0 + P t back gives

    x(t) = ( 2^(v+1) A 2^(e i_0) * (2^(e P))^t + b' ) / (c A_v),
    b'   = 2^(v+1) b - c 2^(v+1) B_v + c 2^v A_v,

another geometric family, with e' = e P and c' = c A_v (still odd).  So the
whole ladder is computable exactly, with no search over x.

WHAT IT CANNOT DO.  A depth-d sieve constrains branch WORDS of length d; it
cannot decide the machine, because the surviving words retain positive
probability at every depth.  Its value is the measured thinning rate, and the
finiteness of each depth's survivor set.

THE ANSWER (measured, depths 1-6).  The admissible word mass runs
0.750000, 0.714844, 0.709259, 0.704411, 0.704110, 0.704067 -- a CONVERGENT
product, limit about 0.70406.  The last-step sieve, at any depth, can never
forbid more than about 29.6% of branch words.  Depth is not a resource that
buys arbitrarily much.

The exceptional branch (oddPart = 3) is handled separately and by bounded
search: x = 3*2^a maps to 3*2^a + a + 3, and asking whether that lies in a
geometric family is a mixed exponential-linear (Pillai-type) equation, not a
congruence.  Every depth-d statement below is therefore stated for generic
branches, with the exceptional branch reported alongside.
"""
import sys
from math import gcd

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/census")
from family import HALT                                           # noqa: E402
from sheep import f, is_pow2, v2                                  # noqa: E402


def A_(v):
    return (1 << (v + 1)) + 1


def B_(v):
    return (1 << v) + v


class Fam:
    """N(i) = (2^(al + e*i) + b) / c for i >= imin.

    The leading coefficient is ALWAYS a pure power of two: it starts as
    2^0 = 1 and the recursion multiplies it by 2^(v+1) * 2^(e*i_0).  Storing
    the exponent instead of the integer is what makes deep levels feasible --
    every use of it below is modular, via pow(2, al + e*i, M)."""
    __slots__ = ("al", "b", "c", "e", "imin", "word")

    def __init__(self, al, b, c, e, imin, word=()):
        self.al, self.b, self.c, self.e, self.imin, self.word = al, b, c, e, imin, word

    def val(self, i):
        """Exact value -- only usable while the exponent is small."""
        n = (1 << (self.al + self.e * i)) + self.b
        assert n % self.c == 0, (self, i)
        return n // self.c

    def divides_ok(self, i):
        """c | 2^(al+e*i) + b, checked modularly (exact, any size)."""
        return (pow(2, self.al + self.e * i, self.c) + self.b) % self.c == 0

    def __repr__(self):
        return (f"(2^({self.al}+{self.e}i){self.b:+d})/{self.c} [i>={self.imin}]"
                f" word={self.word}")

    def bits(self):
        return max(self.al, abs(self.b).bit_length(), self.e)


def ord2(M):
    """ord_M(2) for odd M."""
    x, o = 2 % M, 1
    while x != 1 % M:
        x = (x * 2) % M
        o += 1
    return o


SMALL = 4000          # exponent below which exact big-int checks are run


def preimages(fam, v, exact=True):
    """Every geometric family of x with v_2(x) = v, oddPart(x) > 3 and
    f(x) in fam.  Returns [] if branch v cannot reach fam."""
    Av, Bv = A_(v), B_(v)
    M = fam.c * Av                                    # odd
    T = (fam.c * Bv - fam.b) % M
    o = ord2(M)
    P = o // gcd(fam.e, o)                            # ord_M(2^e)
    hits, x = [], pow(2, fam.al + fam.e * fam.imin, M)
    step = pow(2, fam.e, M)
    for t in range(P):
        if x == T:
            hits.append(fam.imin + t)
        x = (x * step) % M
    out = []
    for i0 in hits:
        # k >= 2 (hence oddPart > 3) is automatic once the value is large;
        # only the genuinely small members need shifting.
        while fam.al + fam.e * i0 < 40:
            N = fam.val(i0)
            k, r = divmod(N - Bv, Av)
            assert r == 0, (fam, v, i0)
            if k >= 2:
                break
            i0 += P
        g = Fam(fam.al + fam.e * i0 + v + 1,
                ((1 << (v + 1)) * fam.b - fam.c * (1 << (v + 1)) * Bv
                 + fam.c * (1 << v) * Av),
                fam.c * Av, fam.e * P, 0, fam.word + (v,))
        assert g.divides_ok(0) and g.divides_ok(1), (g, fam, v)
        if exact and g.al < SMALL:
            # full big-integer check that the family really is a preimage
            for i in (0, 1):
                x0 = g.val(i)
                assert v2(x0) == v and (x0 >> v) > 3, (g, i)
                assert f(x0) == fam.val(i0 + P * i), (g, i)
        out.append(g)
    return out


if __name__ == "__main__":
    import time
    t0 = time.time()
    P_ = lambda *a: print(*a, flush=True)
    P_("=" * 74)
    P_("THE SHEEP MACHINE: THE DEPTH LADDER")
    P_("=" * 74)

    VMAX = 48
    # DEPTH 6 is the practical wall: each depth costs about 15x the last
    # (depth 4 ~1s, depth 5 ~80s, depth 6 ~6.4h), because ord_M(2) is computed
    # by a linear scan and M = c*A_v accumulates prime factors.  Depth 7 would
    # be ~4 days.  Reaching depth 8-9 needs the order via a factorisation of M
    # (which we know: M is always a product of A_v = 2^(v+1)+1) plus
    # Pohlig-Hellman for the discrete log.  Not needed for the conclusion.
    DEPTH = 6
    level = [Fam(0, 0, 1, 1, 0)]                       # H^0 = {2^i}
    mass_prod = 1.0
    table = []
    for d in range(1, DEPTH + 1):
        nxt, surv = [], set()
        for fam in level:
            for v in range(VMAX):
                got = preimages(fam, v)
                if got:
                    surv.add(v)
                    nxt.extend(got)
        m = sum(2.0 ** -(v + 1) for v in sorted(surv))
        mass_prod *= m
        table.append((d, sorted(surv), len(nxt), m, mass_prod))
        P_(f"\ndepth {d}:  survivors {sorted(surv)}")
        P_(f"          families carried forward: {len(nxt)}"
           f"   (largest exponent {max((g.al for g in nxt), default=0)}, "
           f"largest c {max((g.c.bit_length() for g in nxt), default=0)} bits)")
        P_(f"          branch mass at this depth {m:.6f}; "
           f"admissible words of length {d}: {mass_prod:.6f}"
           f"   [{time.time() - t0:5.1f}s]")
        if not nxt:
            break
        level = nxt

    # ---- ground truth at depths 1..3 --------------------------------------
    P_(f"\nGROUND TRUTH (brute force)")
    BOUND = 3_000_000
    for d in (1, 2, 3):
        obs = set()
        n_hit = 0
        for x in range(2, BOUND):
            y, ok = x, True
            for _ in range(d):
                y = f(y)
                if y is HALT:
                    ok = False
                    break
            if not ok or y is HALT:
                continue
            z = f(y)
            if z is HALT or not is_pow2(z):
                continue
            if (x >> v2(x)) > 3:
                obs.add(v2(x))
                n_hit += 1
        pred = table[d][1] if d < len(table) else None
        P_(f"      depth {d}: x < {BOUND} halting in exactly {d + 1} steps: "
           f"{n_hit} values, valuations {sorted(obs)}")
        P_(f"               sieve predicts {pred};  contained: "
           f"{set(obs) <= set(pred) if pred else 'n/a'}")
        assert pred is None or set(obs) <= set(pred)

    # ---- the exceptional branch ------------------------------------------
    P_(f"\nEXCEPTIONAL BRANCH (oddPart = 3), by bounded search")
    lvl = [Fam(0, 0, 1, 1, 0)]
    for d in range(1, 4):
        hitsx = []
        for a in range(0, 900):
            y = 3 * (1 << a) + a + 3
            for fam in lvl:
                for i in range(0, 400):
                    w = fam.val(i)
                    if w == y:
                        hitsx.append((d, a))
                    if w > y:
                        break
        P_(f"      depth {d}: a < 900 with 3*2^a + a + 3 in a depth-{d - 1} "
           f"family: {hitsx}")
        nl = []
        for fam in lvl:
            for v in range(60):
                nl.extend(preimages(fam, v))
        lvl = nl

    # ---- the reading ------------------------------------------------------
    P_(f"\nTHE THINNING RATE")
    P_(f"      {'depth':>6} {'survivors':>28} {'branch mass':>12} "
       f"{'word mass':>11} {'forbidden':>10}")
    for d, surv, nf, m, mp in table:
        ss = str(surv) if len(str(surv)) <= 28 else str(surv)[:25] + "..."
        P_(f"      {d:6d} {ss:>28} {m:12.6f} {mp:11.6f} {1 - mp:10.4%}")
    P_(f"\n[{time.time() - t0:6.1f}s] done")
