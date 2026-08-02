"""The halting basin as implied clauses for the WS1 search.

WS1's own finding was that the obstruction is dynamical: at n = 3,4,5 there are
structures that separate the orbit from H, and closure kills every one at the
FIRST step, because some x sharing a state with an orbit element has F(x) a
power of 2.  In other words a certificate must avoid the whole halting basin

    Basin = union_{j >= 0} F^{-j}(H),

not just H.  WS2 enumerates that basin exactly and cheaply (preimages are
strictly smaller than their image, so the backward tree below any cap is finite
and complete).  So we can hand the solver what it would otherwise have to
derive through j rounds of product reasoning.

SOUNDNESS.  "x in Basin => x not in I" is IMPLIED by the constraints already
present: I is F-closed and misses H, so by induction it misses every F^{-j}(H).
Adding implied clauses cannot turn UNSAT into SAT or SAT into UNSAT -- the set
of satisfying assignments is unchanged.  The theorem proved at each size is
therefore exactly the same theorem; only the solver's work changes.
"""
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/density")
from needle import is_pow2                                  # noqa: E402
from density import preimages                               # noqa: E402


def basin(cap_bits, include_powers=True):
    """Every x <= 2^cap_bits in the halting basin, as a sorted list.

    Complete below the cap: F expands (F(x) >= x + 3), so every preimage of a
    value <= 2^cap_bits is itself <= 2^cap_bits and the backward walk from the
    powers of 2 below the cap misses nothing.
    """
    cap = 1 << cap_bits
    seeds = [1 << e for e in range(cap_bits + 1)]
    out = set(seeds) if include_powers else set()
    frontier = seeds
    while frontier:
        nxt = []
        for y in frontier:
            for b in preimages(y):
                if b <= cap and b not in out:
                    out.add(b)
                    nxt.append(b)
        frontier = nxt
    return sorted(out)


def strata(cap_bits):
    """The basin split by depth, for reporting."""
    cap = 1 << cap_bits
    layer = [1 << e for e in range(cap_bits + 1)]
    seen, out = set(layer), [layer]
    while True:
        nxt = []
        for y in out[-1]:
            for b in preimages(y):
                if b <= cap and b not in seen:
                    seen.add(b)
                    nxt.append(b)
        if not nxt:
            return out
        out.append(sorted(nxt))


if __name__ == "__main__":
    for bits in (26, 40, 64, 128):
        s = strata(bits)
        tot = sum(len(l) for l in s)
        print(f"cap 2^{bits:<4} basin {tot:>5} elements  "
              f"({len(s[0])} powers of 2 + {tot - len(s[0])} proper preimages)"
              f"  depths {[len(l) for l in s]}")
    print()
    b = basin(40)
    print("proper (non-power-of-2) basin elements below 2^40:")
    print("  ", [x for x in b if not is_pow2(x)])
