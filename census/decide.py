"""Decision procedures applied automatically to every census machine.

Two of the program's own theorems can DECIDE a machine outright, and the census
is the first place they get run on anything but the two flagship machines.

1. THE EXACT CONGRUENCE TEST (stronger than WS4's sweep).  WS4 checked a
   NECESSARY condition -- do the orbit's residues avoid H's residues -- because
   a finite orbit prefix is all one has.  Here the test is exact and finite.

   On branch v, x = 2^(v+1)k + 2^v and F(x) = A_v k + B_v.  For odd m the factor
   2^(v+1) is invertible, and in general, as k runs over Z_m the pair
   (source, target) traces the graph of ONE affine map phi_v on Z_m.  Both A_v
   and B_v mod m depend on v only through (2^v mod m, v mod m), a state space of
   size m^2, so the sequence of maps phi_v is eventually periodic in v and
   iterating v until that state repeats enumerates EVERY branch.

   So the relation R_m = union_v graph(phi_v) is exactly computable, the orbit's
   residues are contained in the R_m-closure of x0 mod m, and if that closure
   misses H's residues then the machine PROVABLY never halts.  Complete for
   this certificate class: it finds a separating congruence iff one exists.

   (The closure is taken over all k including k = 0, i.e. over halting x too.
   That only adds edges, which only enlarges the closure, so a negative answer
   -- "closure misses H" -- stays sound.)

2. THE WS3 FORBIDDEN-BRANCH SIEVE.  A halt out of a branch-v step requires a
   solvable discrete-logarithm condition. If EVERY branch fails it, no orbit of
   the machine from any start can ever halt -- also a proof.
"""
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/baker")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/census")

from sieve import geometric_solver                          # noqa: E402


def halt_residues(m, base=2):
    """Every residue mod m taken by base^e, e >= 0 (pre-period included: here
    we need ANY halt, not an arbitrarily large one, so the pre-period counts)."""
    seen, x = set(), 1 % m
    while x not in seen:
        seen.add(x)
        x = x * base % m
    return seen


def branch_maps(mach, m):
    """The affine maps phi_v on Z_m, one per branch, enumerated exhaustively.

    Returns a list of (mul, add) with phi_v(c) = mul*c + add (mod m) when
    2^(v+1) is invertible, else an explicit edge list for that branch.
    """
    maps, edges, seen = [], [], set()
    v = 0
    while True:
        key = (pow(2, v, m), v % m)
        if key in seen:
            break
        seen.add(key)
        A, B = mach.A(v) % m, mach.B(v) % m
        p = pow(2, v + 1, m)
        try:
            inv = pow(p, -1, m)
            maps.append(((A * inv) % m, (B - A * inv * pow(2, v, m)) % m))
        except ValueError:                       # 2^(v+1) not invertible mod m
            for k in range(m):
                edges.append(((p * k + pow(2, v, m)) % m, (A * k + B) % m))
        v += 1
        if v > 4 * m * m + 8:                    # guard; the state space is m^2
            raise AssertionError("branch enumeration failed to close")
    return maps, edges


def congruence_proof(mach, x0, mmax=64):
    """Smallest modulus m <= mmax whose closure separates the orbit from H,
    or None.  A returned m is a PROOF that the machine never halts from x0."""
    for m in range(2, mmax + 1):
        H = halt_residues(m)
        c0 = x0 % m
        if c0 in H:
            continue
        maps, edges = branch_maps(mach, m)
        adj = {}
        for s, t in edges:
            adj.setdefault(s, set()).add(t)
        reach, frontier, bad = {c0}, [c0], False
        while frontier and not bad:
            c = frontier.pop()
            nxt = {(mul * c + add) % m for mul, add in maps} | adj.get(c, set())
            for t in nxt:
                if t in H:
                    bad = True
                    break
                if t not in reach:
                    reach.add(t)
                    frontier.append(t)
        if not bad:
            return m, sorted(reach)
    return None


def sieve_proof(mach, vmax=40):
    """True if EVERY branch v <= vmax is forbidden by the WS3 sieve, i.e. no
    halt can follow any step -- a proof of non-halting from any start.

    Returns (all_forbidden, n_forbidden, n_tested, mass) with mass the frequency
    of the forbidden branches under P(v) = 2^-(v+1)."""
    solve = geometric_solver(2)
    forb = mass = tested = 0
    for v in range(vmax + 1):
        data = mach.branch_sieve_data(v)
        if data is None:
            continue
        N, D, P, Q, w = data
        tested += 1
        if solve(P, Q, N) is None:
            forb += 1
            mass += w
    return (forb == tested and tested > 0), forb, tested, mass
