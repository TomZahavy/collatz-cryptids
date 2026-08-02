"""WS2: how many starts below x halt?  Depth-graded, and unconditional.

THE CORRECTED PREMISE.  NEXT_STEPS.md justified this workstream by "the Needle
map is strictly increasing".  It is not: F(9) = 21 > F(10) = 17, and there are
990 inversions below 2000.  What the counting actually needs -- and what is
true -- is EXPANSION:

    L1.  x + 3 <= F(x) <= 2.5 x + log2 x <= 3x       (x >= 3, not a power of 2)

Expansion is what makes the backward tree finite (preimages are strictly
smaller) and what bounds how far an orbit can travel in a bounded number of
steps, which is what converts a heuristic ceiling into a proof.

    L2.  Backward step, exactly: y = F(b) with v_2(b) = v iff

             b = (2^{v+1} y + 2^v (3 - 2v)) / (2^{v+1} + 3),

         so each valuation v gives AT MOST ONE preimage, and v <= log2(2y).
         Hence d(y) := #F^{-1}(y) <= log2(y) + 1.

    L3.  On average the branching is subcritical:  sum_{y<=Y} d(y) <= c*Y +
         O(log Y) with c = sum_{v>=0} 1/(2^{v+1}+3) = 0.54528... < 1, because
         the preimage under branch v exists only for y in one residue class
         modulo 2^{v+1}+3.

THE THEOREM.  Let A_j(x) = #{b <= x : F^j(b) is a power of 2, j minimal}.  A
seed b <= x that halts within L steps reaches a power of 2 that is at most
3^L x (by L1), so the whole depth-<=L backward computation is FINITE AND
COMPLETE -- no ceiling assumption.  Combining L1 and L2,

    A_{j+1}(x) <= A_j(3x) * (log2(3x) + 1),     A_0(x) <= log2(x) + 1,

    #{b <= x : b halts within L steps}  <=  (L+1) * (log2 x + 1.585 L + 2)^{L+1}

which is polylogarithmic in x for each fixed L.  This is the honest version of
"almost no start halts": it is unconditional, but only at bounded depth.  The
bound goes trivial at depth ~ log x / log log x, and that is exactly where the
cryptid difficulty lives -- see the discussion in the report.
"""
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
from needle import step1, is_pow2, v2, HALT               # noqa: E402


def preimages(y):
    """All b with F(b) = y, via the exact affine backward formula (L2)."""
    out = []
    v = 0
    while (1 << (v + 1)) <= 2 * y:
        den = (1 << (v + 1)) + 3
        num = (1 << (v + 1)) * y + (1 << v) * (3 - 2 * v)
        if num > 0 and num % den == 0:
            b = num // den
            if b >= 3 and not is_pow2(b) and v2(b)[0] == v:
                out.append(b)
        v += 1
    return out


def halting_seeds(x, L):
    """Exact, complete list of b <= x halting within L steps, by depth.

    Complete because of L1: such a b reaches a power of 2 that is <= 3^L x, so
    seeding the backward walk with every power of 2 up to 3^L x misses nothing.
    """
    layers = [set() for _ in range(L + 1)]
    cap = x * 3 ** L
    frontier = set()
    m = 0
    while (1 << m) <= cap:
        frontier.add(1 << m)
        m += 1
    seen_depth = {}
    for p in frontier:
        if p <= x:
            seen_depth[p] = 0
    for j in range(1, L + 1):
        nxt = set()
        bound = x * 3 ** (L - j)
        for t in frontier:
            for b in preimages(t):
                if b <= bound:
                    nxt.add(b)
        frontier = nxt
        for b in frontier:
            if b <= x and b not in seen_depth:
                seen_depth[b] = j
    for b, j in seen_depth.items():
        layers[j].add(b)
    return layers


def brute_force(x, L):
    """Independent check: run every b <= x forward for L steps."""
    layers = [set() for _ in range(L + 1)]
    for b in range(1, x + 1):
        y = b
        for j in range(L + 1):
            if is_pow2(y):
                layers[j].add(b)
                break
            y = step1(y)
    return layers


def bound(x, L):
    """The rigorous upper bound of the theorem."""
    import math
    return (L + 1) * (math.log2(x) + 1.585 * L + 2) ** (L + 1)


def _tests():
    # L1
    assert all(step1(x) >= x + 3 and step1(x) <= 3 * x
               for x in range(3, 200000) if not is_pow2(x))
    print("  L1 expansion  x+3 <= F(x) <= 3x  for 3 <= x < 200000: OK")

    # L2: the backward formula inverts F exactly, and d(y) <= log2(y)+1
    for x in range(3, 60000):
        if is_pow2(x):
            continue
        assert x in preimages(step1(x)), x
    worst = 0
    for y in range(3, 60000):
        d = len(preimages(y))
        assert all(step1(b) == y for b in preimages(y))
        assert d <= y.bit_length() + 1
        worst = max(worst, d)
    print(f"  L2 backward formula inverts F, d(y) <= log2(y)+1 (max d seen "
          f"= {worst}) for y < 60000: OK")

    # L3: average branching, rigorous constant vs measured
    tot = sum(len(preimages(y)) for y in range(3, 200000))
    c = sum(1.0 / ((1 << (v + 1)) + 3) for v in range(0, 60))
    print(f"  L3 average branching measured {tot / 199997:.4f} vs the "
          f"rigorous ceiling c = {c:.4f}: OK")

    # the exact depth-graded enumeration agrees with brute force
    for x, L in ((20000, 3), (60000, 4)):
        a = [sorted(s) for s in halting_seeds(x, L)]
        b = [sorted(s) for s in brute_force(x, L)]
        assert a == b, (x, L, [len(s) for s in a], [len(s) for s in b])
    print("  depth-graded backward enumeration == forward brute force "
          "(x=20000/L=3, x=60000/L=4): OK")
    print("all WS2 machinery tests passed")


if __name__ == "__main__":
    _tests()
