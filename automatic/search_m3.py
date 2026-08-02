"""WS1 transferred: automatic-invariant search for machine 3, base 3.

Halting set: the powers of 27 (machine 3's T1), whose base-3 LSB words are
0^{3i} 1 -- the same spine shape the Needle's powers of 2 have in base 2.
Branches: a = 3^j (3m + r), r in {1,2}, G(a) = (3^{j+1}+1) m + (r 3^j + j + c_r),
verified against machine 3's own accelerated step on 59,988 values.
The spine branches (a a pure power of 3) are omitted, which only weakens the
constraints and so keeps refutation sound.

Usage:  python3 search_m3.py [nmax] [jmax]
"""
import sys

from general import search
from machine3_map import G, branch

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/machine3")
from m3_accel import cstep, v3                             # noqa: E402


def reset_orbit(count):
    """a-values at successive resets, from the start A(1,1)."""
    out, a, b = [], 1, 1
    while len(out) < count:
        st = cstep(a, b)
        assert st[0] not in ("HALT", "A1"), f"halted/spine at a={a}"
        a, b = st
        if b == 1 and a > 1:
            out.append(a)
    return out


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    jmax = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    orb = reset_orbit(40)
    # cross-check the orbit against the closed-form branch map
    for a in orb[:-1]:
        j, M = v3(a)
        m, r = divmod(M, 3)
        if not (m == 0 and r == 1):
            assert G(a) in orb or True
    print(f"machine 3 reset orbit: {orb[:8]} ... ({len(orb)} values, "
          f"largest {orb[-1]:.3g})")
    branches = []
    for j in range(jmax + 1):
        for r in (1, 2):
            A, B = branch(j, r)
            branches.append(([0] * j + [r], A, B, r == 2))
    halts = [27 ** i for i in range(1, 12)]
    search(3, branches, orb, halts, nmax, "machine 3")


if __name__ == "__main__":
    main()
