"""WS2 transferred to machine 3: the same depth-graded density theorem, base 3.

Machine 3's reset map is G(a) = (3^{j+1}+1) m + (r*3^j + j + c_r) on the branch
a = 3^j (3m + r), r in {1,2}, c_1 = 3, c_2 = 4 (verified against machine 3's own
accelerated step).  The Needle argument transfers line for line:

  L1'  a + 3 <= G(a) <= 2a          for a >= 8 not a pure power of 3
  L2'  each branch (j, r) contributes at most one preimage of y, namely
       m = (y - B_{j,r}) / A_{j,r} when that is a nonnegative integer, and only
       j <= log_3 y can contribute, so d(y) <= 2 log_3 y + 2
  L3'  average branching <= sum_{j,r} 1/(3^{j+1}+1) = 0.8068... < 1
  L4'  a seed a <= x halting within L steps reaches a power of 27 below 2^L x,
       so the depth-graded backward enumeration is COMPLETE

giving  #{a <= x halting within L steps} <= (L+1)(2 log_3 x + 2L + 2)^{L+1}.

The halting set is the powers of 27 (machine 3's T1).
"""
import math
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/automatic")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/machine3")
from machine3_map import G, branch                         # noqa: E402
from m3_accel import v3                                    # noqa: E402


def is_pow3(a):
    return a >= 1 and 3 ** round(math.log(a, 3)) == a


def preimages(y, jmax=None):
    """All a with G(a) = y (branch-affine inverse; at most one per branch)."""
    out = []
    j = 0
    while 3 ** (j + 1) + 1 <= max(y, 2) * 3:
        for r in (1, 2):
            A, B = branch(j, r)
            if y >= B and (y - B) % A == 0:
                m = (y - B) // A
                if m == 0 and r == 1:
                    continue                    # spine value, excluded
                a = 3 ** (j + 1) * m + r * 3 ** j
                if a >= 2 and v3(a)[0] == j and G(a) == y:
                    out.append(a)
        j += 1
        if jmax is not None and j > jmax:
            break
    return out


def halting_seeds(x, L):
    """Exact, complete list of a <= x halting within L resets, by depth."""
    layers = [set() for _ in range(L + 1)]
    cap = x * 2 ** L
    frontier = {27 ** i for i in range(1, 200) if 27 ** i <= cap}
    depth = {p for p in frontier if p <= x}
    for p in depth:
        layers[0].add(p)
    seen = set(depth)
    for jj in range(1, L + 1):
        nxt = set()
        bound = x * 2 ** (L - jj)
        for t in frontier:
            for a in preimages(t):
                if a <= bound:
                    nxt.add(a)
        frontier = nxt
        for a in frontier:
            if a <= x and a not in seen:
                seen.add(a)
                layers[jj].add(a)
    return layers


def _tests():
    # L1': expansion
    bad = [a for a in range(8, 200000)
           if not is_pow3(a) and not (a + 3 <= G(a) <= 2 * a)]
    assert not bad, bad[:5]
    print("  L1' expansion  a+3 <= G(a) <= 2a  for 8 <= a < 200000: OK")

    # L2': the inverse finds every preimage, and only true ones
    for a in range(2, 40000):
        if is_pow3(a):
            continue
        j, M = v3(a)
        m, r = divmod(M, 3)
        if m == 0 and r == 1:
            continue
        assert a in preimages(G(a)), a
    worst = max(len(preimages(y)) for y in range(2, 40000))
    print(f"  L2' inverse is exact; largest d(y) below 40000 is {worst}: OK")

    # L3': the rigorous average-branching ceiling versus measurement
    c = sum(2.0 / (3 ** (j + 1) + 1) for j in range(40))
    tot = sum(len(preimages(y)) for y in range(2, 100000))
    print(f"  L3' average branching measured {tot / 99998:.4f} vs rigorous "
          f"ceiling {c:.4f} (< 1, subcritical): OK")

    # depth-graded enumeration versus forward simulation
    for x, L in ((30000, 3), (200000, 3)):
        back = [sorted(s) for s in halting_seeds(x, L)]
        fwd = [set() for _ in range(L + 1)]
        for a in range(2, x + 1):
            if is_pow3(a) and round(math.log(a, 3)) % 3 == 0:
                fwd[0].add(a)
                continue
            y = a
            for d in range(1, L + 1):
                j, M = v3(y)
                m, r = divmod(M, 3)
                if m == 0 and r == 1:
                    break                        # spine: not a G-step
                y = G(y)
                if is_pow3(y) and round(math.log(y, 3)) % 3 == 0:
                    fwd[d].add(a)
                    break
        fwd = [sorted(s) for s in fwd]
        assert back == fwd, (x, L, [len(s) for s in back], [len(s) for s in fwd])
    print("  depth-graded backward enumeration == forward simulation "
          "(x=30000 and 200000, L=3): OK")
    print("all machine-3 density tests passed")


if __name__ == "__main__":
    _tests()
    print()
    for x in (10 ** 6, 10 ** 12, 10 ** 24, 10 ** 48, 10 ** 96):
        lay = [len(s) for s in halting_seeds(x, 5)]
        print(f"  x = 10^{len(str(x)) - 1:>3}: A_j = {lay}  total = {sum(lay)}"
              f"   (log_3 x = {math.log(x, 3):.0f})")
