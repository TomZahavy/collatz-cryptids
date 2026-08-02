"""Power calibration for the MSB-first search -- the companion to calibrate.py.

Same instrument, same planted machines G_m (Needle multipliers a_v = 2^{v+1}+3,
additive constant b_v = a_v * inv2 mod m, m PRIME), so I_m = {x : m | x} is
invariant and misses the powers of 2.  Read MSB-first, I_m is recognised by the
residue automaton (state = value mod m, delta(r, d) = 2r + d mod m), which has
exactly m states and already satisfies our leading-zero convention because
delta(0, 0) = 0.  So a certificate provably exists at m MSB states, and the
UNSAT verdicts below m pin the true minimum to exactly m.

Usage:  python3 msb_calibrate.py [kmin] [kmax]
"""
import sys
import time

from calibrate import machine, step                        # noqa: E402
from msb_search import msb_word, search                    # noqa: E402


def residue_dfa_size(m):
    """States of the MSB residue automaton for multiples of m, after merging."""
    trans = [[(2 * r + d) % m for d in (0, 1)] for r in range(m)]
    part = [0 if r == 0 else 1 for r in range(m)]
    while True:
        sig, new = {}, []
        for r in range(m):
            key = (part[r], part[trans[r][0]], part[trans[r][1]])
            new.append(sig.setdefault(key, len(sig)))
        if len(set(new)) == len(set(part)):
            return len(set(new))
        part = new


def verify_planted(m, hi=200000):
    """The residue automaton really is a certificate for G_m: start in it,
    closed under the map, disjoint from the powers of 2."""
    def state(x):
        s = 0
        for d in msb_word(x):
            s = (2 * s + d) % m
        return s
    assert state(m) == 0
    for x in range(m, hi, m):                       # members are closed
        assert state(x) == 0 and state(step(m, x)) == 0, (m, x)
    e = 0
    while (1 << e) < hi:                            # and miss the halt set
        assert state(1 << e) != 0, (m, e)
        e += 1


def main():
    kmin = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    kmax = int(sys.argv[2]) if len(sys.argv) > 2 else 13
    vmax = 1
    print("MSB-first power calibration -- planted certificates of known size")
    print("machine G_m, halt set = powers of 2, convention: leading-zero "
          "invariant")
    print()
    for m in range(3, 400, 2):
        if any(m % d == 0 for d in range(3, int(m ** 0.5) + 1, 2)):
            continue                                 # prime only: see calibrate
        k = residue_dfa_size(m)
        if not (kmin <= k <= kmax):
            continue
        verify_planted(m)
        brs = machine(m, vmax)
        table = {v: (brs[v][1], brs[v][2]) for v in range(vmax + 1)}
        orb, x = [], m
        for _ in range(40):
            orb.append(x)
            x = step(m, x)
        print(f"--- planted k={k} (m={m}) ---")
        t0 = time.time()
        for n in range(2, k + 3):
            got = search(n, vmax, branches=lambda v: table[v], orb=orb)
            if got:
                print(f"      FOUND at n={n} after {time.time()-t0:.1f}s total"
                      f"   delta={got[0]} acc={got[1]}")
                break
        else:
            print(f"      NOT FOUND up to n={k+2} "
                  f"({time.time()-t0:.1f}s) -- planted size was {k}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
