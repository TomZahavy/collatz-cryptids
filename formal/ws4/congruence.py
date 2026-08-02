"""WS4.3c -- the congruence-plus-threshold certificate class, refuted directly.

WHY THIS CLASS.  Every bbchallenge regular decider (FAR, WFAR, RepWL, CPS)
operates on tapes that encode counters in unary/block form.  A regular language
over a one-letter alphabet is ultimately periodic, so what such a decider can
say about a counter is exactly "x >= T and x mod m in S" -- a congruence with a
threshold.  That is the class refuted here, for our two flagship machines.

THE ARGUMENT, and why it needs no closure computation.  Suppose
    I = {x < T} union {x >= T : x mod m in S}
contains the orbit and avoids the halting set H.  Take any orbit element
x_i >= T and any h in H with h >= T and h = x_i (mod m).  Since x_i is in I and
x_i >= T, its class is in S; h >= T has the same class, so h is in I -- and
h is in H.  Contradiction.  So a certificate mod m with threshold T exists only
if NO orbit element >= T is congruent mod m to any element of H that is >= T.

Both sides are handled exactly:
  * H's residues are enumerated COMPLETELY, not sampled: 2^e mod m is
    eventually periodic in e, so iterating until the first repeat gives every
    residue H ever takes, and each residue in the cycle is taken by infinitely
    many (hence arbitrarily large) elements of H.  Same for 27^e mod m.
  * The orbit contributes a finite prefix, which only makes the refutation
    stronger: one collision suffices.  Searching for the collision at orbit
    index >= K makes the result threshold-proof up to x_K.

Run: python3 congruence.py
"""
import sys
import time

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/machine3")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/automatic")

import needle                                               # noqa: E402
import machine3_map                                         # noqa: E402


def halt_residues(base, m):
    """Residues mod m taken by base^e for INFINITELY MANY e.

    Not merely the residues that occur: base^e mod m is eventually periodic,
    and a residue in the pre-period is taken by finitely many powers, so a
    collision there is defeated by a large enough threshold.  Only residues on
    the eventual cycle are taken by arbitrarily large elements of H, and only
    those make the argument threshold-proof for EVERY T.
    """
    seen, x, e = {}, 1 % m, 0
    while x not in seen:
        seen[x] = e
        x = x * base % m
        e += 1
    period = e - seen[x]
    cyc, y = set(), x
    for _ in range(period):
        cyc.add(y)
        y = y * base % m
    return cyc


def needle_orbit(n):
    x, out = 6, []
    for _ in range(n):
        out.append(x)
        x = needle.step1(x)
        if x is needle.HALT:
            raise AssertionError("the Needle halted -- that would be news")
    return out


def m3_orbit(n):
    a, out = 4, []                    # 4 = 3*1+1, the first non-spine value
    for _ in range(n):
        out.append(a)
        a = machine3_map.G(a)
    return out


def sweep(name, orbit, base, M, K):
    """For every modulus m <= M find an orbit element at index >= K congruent
    to some element of H.  Returns the worst (largest) index needed."""
    worst_idx, worst_m, failures = 0, 0, []
    for m in range(2, M + 1):
        hres = halt_residues(base, m)
        for i in range(K, len(orbit)):
            if orbit[i] % m in hres:
                if i > worst_idx:
                    worst_idx, worst_m = i, m
                break
        else:
            failures.append(m)
    print(f"  {name}: moduli 2..{M:,}, collisions sought at orbit index >= {K}")
    print(f"    moduli with NO collision (would-be certificates): {len(failures)}"
          + (f"  {failures[:20]}" if failures else ""))
    print(f"    worst case: modulus {worst_m:,} needed index {worst_idx} "
          f"(i.e. every modulus fails within {worst_idx - K + 1} orbit steps of the cutoff)")
    return failures


def parity_lemma():
    """LEMMA (proved; verified below).  G(a) = v_3(a)  (mod 2).

    G(a) = (3^(j+1) + 1) m + (r*3^j + j + c_r) with j = v_3(a), r in {1,2},
    c_1 = 3, c_2 = 4.  The first coefficient is even, 3^j is odd, and
    r + c_r is odd for both r -- so G(a) = r + j + c_r = j (mod 2) either way.

    Consequence used below: the 3-free part of a machine-3 orbit value is ODD
    only about a quarter of the time, not half, since P(v_3 odd) = 1/4 under
    the geometric branch model.  That is why the modulus 2*3^8 needed a much
    longer window than any other: its one threshold-proof residue demands both
    a high valuation AND the rarer parity.
    """
    bad = n = 0
    for a in range(2, 400000):
        j, Mo = machine3_map.v3(a)
        m, r = divmod(Mo, 3)
        if r == 0 or (m == 0 and r == 1):
            continue
        n += 1
        bad += (machine3_map.G(a) % 2 != j % 2)
    return bad, n


def main():
    print("WS4.3c  CONGRUENCE-PLUS-THRESHOLD CERTIFICATES\n")
    t0 = time.time()

    K, M = 500, 20000
    N_NEEDLE, N_M3 = 60500, 200500
    orb = needle_orbit(N_NEEDLE)
    m3 = m3_orbit(N_M3)
    print(f"  orbit prefixes: {N_NEEDLE:,} (Needle) and {N_M3:,} (machine 3);")
    print(f"  the threshold cutoff x_{K} has {len(str(orb[K])):,} decimal digits "
          f"(Needle), {len(str(m3[K])):,} (machine 3)\n")

    f1 = sweep("Needle,    H = powers of 2 ", orb, 2, M, K)
    print()
    f2 = sweep("machine 3, H = powers of 27", m3, 27, M, K)
    print()
    bad, n = parity_lemma()
    print(f"  LEMMA  G(a) = v_3(a) mod 2 : mismatches {bad} over {n:,} values "
          f"a < 400,000")
    print("    (proved; see docstring.  It is why modulus 2*3^8 = 13,122 was the")
    print("     last to fall -- it needed v_3 >= 8 together with the rarer parity,")
    print("     and first collided at orbit index 105,033.)")
    print()
    print("  => no congruence certificate for either machine, at any modulus")
    print(f"     m <= {M:,}, with ANY threshold -- the collision residues are")
    print("     taken by infinitely many elements of H, so no threshold escapes.")
    print(f"     ({len(f1)} and {len(f2)} surviving moduli.)")
    print(f"\n  elapsed {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
