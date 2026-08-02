"""The forbidden-branch sieve, in machine-independent form (WS3 transfer sweep).

THE GENERAL THEOREM.  Let a return map F act on branch b as an affine map of a
single integer,

        F(x) = alpha_b x + beta_b,      alpha_b = N_b / D_b  in lowest terms,

with fixed point x*_b = beta_b/(1 - alpha_b) = P_b / Q_b in lowest terms.  Then
for a SINGLE step on branch b,

        D_b (Q_b x_1 - P_b) = N_b (Q_b x_0 - P_b),

and since gcd(N_b, D_b) = 1 this forces

    (*)     N_b  |  Q_b x_1 - P_b .

(The same argument run n times gives N_b^n | Q_b x_n - P_b for a run of length
n; n = 1 already carries the content below and needs no run.)

THE SIEVE.  If the step ENDS IN A HALT then x_1 lies in the halting set H, so a
halt can follow a b-step only if

        there exists h in H with  Q_b h = P_b   (mod N_b).

When H is thin -- a geometric family {c r^m} -- this is a discrete-logarithm
condition and it can be UNSOLVABLE.  Then branch b is FORBIDDEN: no orbit of
the machine, from any start, at any scale, at any time, can halt out of a
b-step.  That is unconditional and infinite-time.

Each machine supplies (i) its branches with (N, D, P, Q) and a frequency, and
(ii) a decision procedure for "is Q h = P mod N solvable over h in H".  The
sieve is otherwise the same computation for every machine.
"""
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/baker")
from runs import dlog                                       # noqa: E402


# --------------------------------------------------------------------------
# halting-set solvers:  does some h in H satisfy  Q h = P (mod mod)?
# --------------------------------------------------------------------------

def geometric_solver(base, coeff=1, mmin=0):
    """H = {coeff * base^m : m >= mmin}.  Solve Q*coeff*base^m = P (mod n).

    The sequence v_m = coeff*base^m mod n is eventually periodic, so scanning m
    until the first repeat of v_m is EXHAUSTIVE: every residue the sequence ever
    takes has appeared by then.  No invertibility of base or Q is needed, so
    this is exact even when gcd(base, n) > 1.
    """
    def solve(P, Q, mod):
        P %= mod
        seen, seq, val = {}, [], coeff % mod
        while val not in seen:                   # rho: tail then cycle
            seen[val] = len(seq)
            seq.append(val)
            val = val * base % mod
        start = seen[val]                        # cycle begins at index `start`
        for m, v in enumerate(seq):
            if (Q * v - P) % mod == 0 and (m >= mmin or m >= start):
                # index m works, or m is in the cycle so it recurs above mmin
                return m
        return None
    return solve


def scan_solver(hgen, limit):
    """H given by an explicit generator of members; scan `limit` of them."""
    def solve(P, Q, mod):
        P %= mod
        for i, h in enumerate(hgen()):
            if i >= limit:
                return None
            if (Q * h - P) % mod == 0:
                return i
        return None
    return solve


# --------------------------------------------------------------------------
# the sieve itself
# --------------------------------------------------------------------------

def sieve(branches, solve, label, show=16):
    """branches: list of (name, N, D, P, Q, weight).  Returns (forbidden, mass)."""
    from math import gcd
    print(f"\n=== {label} ===")
    print(f"{'branch':>12} {'N':>16} {'P mod N':>16} {'freq':>10}   verdict")
    forb, mass, tot = [], 0.0, 0.0
    for i, (name, N, D, P, Q, w) in enumerate(branches):
        assert N > D >= 1 and gcd(N, D) == 1, ("alpha not in lowest terms", name)
        hit = solve(P, Q, N)
        tot += w
        if hit is None:
            forb.append(name)
            mass += w
        if i < show:
            print(f"{str(name):>12} {N:>16,} {P % N:>16,} {w:>10.6f}   "
                  f"{'FORBIDDEN' if hit is None else f'allowed (h index {hit})'}")
    if len(branches) > show:
        print(f"{'...':>12}   ({len(branches) - show} further branches)")
    print(f"  branches examined: {len(branches)};  frequency covered: {tot:.6f}")
    print(f"  FORBIDDEN: {len(forb)} of {len(branches)}, frequency mass "
          f"{mass:.6f}   ({100 * mass:.2f}% of all steps)")
    return forb, mass, tot
