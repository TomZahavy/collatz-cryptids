"""WS5 census: the one-schema VAL(2) family, and its per-machine analysis kit.

WHY THIS FAMILY.  WS4 ended by asking whether the one-schema valuation class is
Turing-complete, and noted it is the only two-sided bet the program still holds.
That class is also exactly where both flagship machines live.  So a census of it
does double duty: it populates the class whose power is open, and it is the
first thing this program has built that produces machines rather than consuming
them.

THE SYNTAX.  A machine is five integers (alpha, beta, gamma, delta, epsilon).
Write x = 2^v * m with m odd, v = v_2(x).  If m = 1 the machine HALTS (x is a
pure power of two).  Otherwise m = 2k+1 with k >= 1, so x = 2^(v+1) k + 2^v, and

    F(x) = A_v * k + B_v,     A_v = alpha*2^(v+1) + beta
                              B_v = gamma*2^v + delta*v + epsilon

This is the branch-affine normal form the whole program is built on, with the
coefficients left free.  The Space Needle is (1, 3, 1, 1, 0); machine 3 is its
base-3 sibling.  As a function of x the branch is affine with

    slope   A_v / 2^(v+1)  ->  alpha        intercept  B_v - A_v/2

so alpha is the asymptotic multiplier: alpha >= 2 doubles at every branch and
runs away, alpha = 1 is the weakly-expanding Collatz-like regime.  That is a
prediction the census can check rather than assume.

WHAT THE KIT COMPUTES, per machine.  Everything the program has built, applied
automatically: drift, the backward branching ceiling, the WS3 forbidden-branch
sieve, and the WS4 congruence sweep.  The last two can each DECIDE a machine --
if every branch is sieved out, or a separating congruence exists, the machine
provably never halts.  That is the point of the census.
"""
from fractions import Fraction
from math import gcd, log2
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/baker")

HALT = "HALT"


class Machine:
    __slots__ = ("a", "b", "g", "d", "e")

    def __init__(self, alpha, beta, gamma, delta, epsilon):
        self.a, self.b, self.g, self.d, self.e = alpha, beta, gamma, delta, epsilon

    def __repr__(self):
        return f"({self.a},{self.b},{self.g},{self.d},{self.e})"

    # ---------------------------------------------------------------- dynamics
    def A(self, v):
        return self.a * (1 << (v + 1)) + self.b

    def B(self, v):
        return self.g * (1 << v) + self.d * v + self.e

    def step(self, x):
        v = (x & -x).bit_length() - 1
        m = x >> v
        if m == 1:
            return HALT
        return self.A(v) * (m >> 1) + self.B(v)

    def well_defined(self, hi=4000):
        """F(x) must be a positive integer for every non-halting x < hi.

        Integrality is automatic; positivity is not, and a machine that can
        emit 0 or a negative value is not a machine on the positive integers.
        """
        for x in range(2, hi):
            y = self.step(x)
            if y is not HALT and y < 1:
                return False
        return True

    def run(self, x0, cap, size_cap=1 << 20000):
        """Returns (verdict, steps, trace_tail).  Verdicts: HALT, CYCLE, GROW."""
        x, seen, n = x0, {}, 0
        while n < cap:
            if x.bit_length() < 64:              # cycles can only live down here
                if x in seen:
                    return "CYCLE", seen[x], n - seen[x]
                seen[x] = n
            y = self.step(x)
            if y is HALT:
                return "HALT", n, x
            if y > size_cap:
                return "GROW", n, y.bit_length()
            x, n = y, n + 1
        return "GROW", n, x.bit_length()

    # ------------------------------------------------------------- statistics
    def drift(self, vmax=200):
        """Expected log2 growth per step under P(v_2 = v) = 2^-(v+1)."""
        return sum(2.0 ** -(v + 1) * log2(self.A(v) / 2.0 ** (v + 1))
                   for v in range(vmax))

    def ceiling(self, vmax=200):
        """sum_v 1/A_v -- the mean number of preimages of a uniform target."""
        return sum(1.0 / self.A(v) for v in range(vmax) if self.A(v) > 0)

    # ----------------------------------------------------------------- WS3
    def branch_sieve_data(self, v):
        """(N, D, P, Q, weight) for the WS3 sieve on branch v.

        On this branch F is affine in x with slope A_v/2^(v+1) and intercept
        B_v - A_v/2; the sieve needs both in lowest terms, plus the fixed point.
        """
        A, twov = self.A(v), 1 << (v + 1)
        gA = gcd(A, twov)
        N, D = A // gA, twov // gA
        if N <= D:                    # not expanding on this branch: no fixed-point
            return None               # argument, so the sieve says nothing
        inter = Fraction(self.B(v)) - Fraction(A, 2)
        star = inter / (1 - Fraction(A, twov))
        return N, D, star.numerator, star.denominator, 2.0 ** -(v + 1)
