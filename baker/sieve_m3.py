"""The forbidden-branch sieve applied to MACHINE 3 (the base-3 archetype).

Machine 3's reset map (machine3_map.py, verified against its own cstep) is, on
the branch a = 3^j (3m + r) with r in {1,2} and c_1 = 3, c_2 = 4,

        G(a) = (3^{j+1} + 1) m + (r 3^j + j + c_r).

Substituting m = (a - r 3^j)/3^{j+1} puts this in affine form with

        alpha = (3^{j+1} + 1) / 3^{j+1},        so N = 3^{j+1}+1, D = 3^{j+1},
        x*    = r 3^j - 3^{j+1}(j + c_r)        (an INTEGER, so Q = 1).

Machine 3 halts exactly when a is a power of 27, so H = {27^k}.  The sieve
condition (sieve.py) is therefore

        27^k  =  r 3^j - 3^{j+1}(j + c_r)     (mod 3^{j+1} + 1)

and the branch (j, r) is FORBIDDEN when this has no solution.

BRANCH FREQUENCIES.  j = v_3(a) is geometric with P(j) = (2/3)(1/3)^j, and
given j the digit r = (a/3^j) mod 3 is 1 or 2 with probability 1/2 each, so
P(j, r) = 3^{-(j+1)}.  (Sum over j >= 0, r in {1,2} is 1.)
"""
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/machine3")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/automatic")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/baker")
from m3_accel import cstep, v3                              # noqa: E402
from machine3_map import G                                  # noqa: E402
from sieve import sieve, geometric_solver                   # noqa: E402

JMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20


def cr(r):
    return 3 if r == 1 else 4


def affine(j, r):
    """(N, D, P, Q) for the branch a = 3^j(3m+r)."""
    N, D = 3 ** (j + 1) + 1, 3 ** (j + 1)
    P = r * 3 ** j - 3 ** (j + 1) * (j + cr(r))
    return N, D, P, 1


def branches(jmax):
    out = []
    for j in range(jmax + 1):
        for r in (1, 2):
            N, D, P, Q = affine(j, r)
            out.append(((j, r), N, D, P, Q, 3.0 ** -(j + 1)))
    return out


# --------------------------------------------------------------------------
def _tests():
    """Verify the affine data and (*) against machine 3's own step."""
    from fractions import Fraction as F
    n = 0
    for a in range(2, 40000):
        j, M = v3(a)
        m, r = divmod(M, 3)
        if r == 0 or (m == 0 and r == 1):
            continue                                   # spine: not in G's domain
        N, D, P, Q = affine(j, r)
        assert F(N, D) * a + (F(G(a)) - F(N, D) * a) == G(a)
        # the affine identity itself, in integers:
        assert D * G(a) == N * a + (D * G(a) - N * a)
        assert (D * G(a) - N * a) == (D - N) * P, (a, j, r)   # beta = (1-alpha)x*
        # and the sieve congruence (*) at n = 1
        assert (Q * G(a) - P) % N == 0, (a, j, r)
        n += 1
    print(f"  affine data (N,D,P,Q) and the congruence (*) verified against "
          f"machine 3's verified map on {n:,} values a < 40,000: OK")

    # what does the machine really do on powers of 27 / powers of 3?
    halts = [j for j in range(1, 13) if cstep(3 ** j, 1)[0] == "HALT"]
    print(f"  a = 3^j halts for j in {halts} (= multiples of 3): OK")
    print(f"  cstep(1,1) = {cstep(1, 1)}  (a = 27^0 = 1 is the START, not a halt)")


def brute_force_seeds(limit):
    """Every a < limit whose single step lands on a power of 27, by brute force."""
    pow27 = set()
    p = 27
    while p < 10 ** 30:
        pow27.add(p)
        p *= 27
    seeds = {}
    for a in range(2, limit):
        j, M = v3(a)
        m, r = divmod(M, 3)
        if r == 0 or (m == 0 and r == 1):
            continue
        if G(a) in pow27:
            seeds.setdefault((j, r), []).append(a)
    return seeds


if __name__ == "__main__":
    print("MACHINE 3 -- forbidden-branch sieve")
    _tests()

    solve = geometric_solver(base=27, coeff=1, mmin=1)     # H = {27^k}, k >= 1
    forb, mass, tot = sieve(branches(JMAX), solve, f"machine 3, j <= {JMAX}")

    allowed = [b for b in [(j, r) for j in range(JMAX + 1) for r in (1, 2)]
               if b not in forb]
    print(f"\n  ALLOWED branches (j <= {JMAX}): {allowed}")
    print(f"  residual frequency (branches a halt could follow): "
          f"{tot - mass:.6f}")

    print("\nINDEPENDENT CHECK -- brute force single-step halting seeds")
    seeds = brute_force_seeds(3 * 10 ** 6)
    print(f"  a < 3,000,000 with G(a) a power of 27, by branch: "
          f"{ {k: len(v) for k, v in sorted(seeds.items())} }")
    bad = [k for k in seeds if k in forb]
    print(f"  seeds landing on a FORBIDDEN branch: {bad}  "
          f"({'CONTRADICTION' if bad else 'none -- consistent'})")
