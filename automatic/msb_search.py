"""WS1 read from the other end: MSB-first automatic non-halting certificates.

WHY.  Every WS1 bound so far is on the state count of an automaton reading x
LEAST-significant bit first.  An MSB automaton for the same set can be
exponentially smaller, so "no certificate at <= 10 LSB states" bounds almost
nothing about small MSB ones -- and the structure this program independently
found to govern these machines (the mantissa backbone, the log2(5/4) circle map
of Section 8) is a LEADING-digit phenomenon, exactly the kind an LSB automaton
cannot express compactly.  This is the one place a positive WS1 result could
still be hiding.

THE ENCODING, AND WHY THE PLANNED OBSTACLE IS NOT THERE.  NEXT_STEPS listed
MSB-first as blocked because "the branch relation is not MSB-synchronous".  It
is.  On branch v, x = 2^{v+1} k + 2^v and y = a_v k + b_v, so eliminating k:

    2^{v+1} * y  -  a_v * x  =  2^{v+1} b_v - a_v 2^v  =:  C_v,          (*)

a fixed constant.  Read x and y MSB-first in parallel, left-padded to a common
length, and track R_i = 2^{v+1} y_i - a_v x_i over the prefixes.  Then

    R_i = 2 R_{i-1} + 2^{v+1} e_i - a_v d_i,        R_final = C_v,

and R is BOUNDED along any pair that can still reach C_v: the unread suffix
contributes at most (2^{v+1} + a_v)(2^{N-i} - 1), so |R_i| <= M_v with
M_v = |C_v| + 2^{v+1} + a_v, and any R outside that box doubles away and can
never return.  So the branch relation is a synchronous (letter-to-letter)
transduction with finitely many states -- no lookahead, no delay.  The only
genuinely end-anchored condition is v_2(x) = v, i.e. x ends in 1 0^v, which a
shift register of the last v+1 digits of x settles at the emission point.

Product state: (DFA state on x, DFA state on y, R, last v+1 digits of x).

CONVENTION.  Left padding forces leading-zero invariance, imposed as
delta(q0, 0) = q0.  This is WLOG as a class: for any MSB-recognisable set of
integers, the minimal DFA of 0*L has that property, because the residual of
0*L by 0 is 0*L itself.  As with the two LSB conventions it is a different SIZE
measure, not a different class of sets.

SOUNDNESS OF "UNSAT" is inherited from sat_search.py: only the FORWARD closure
of the product is encoded, so R = reach satisfies the formula and a real
certificate always yields a satisfying assignment.

Usage:  python3 msb_search.py [nmin] [nmax] [vmax]
"""
import sys
import time

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
from needle import step1                                    # noqa: E402

from dfa_invariant import needle_branch, times4_branch      # noqa: E402
from pysat.formula import IDPool                            # noqa: E402
from pysat.solvers import Solver                            # noqa: E402


def msb_word(x):
    return [int(c) for c in bin(x)[2:]]


def const_and_bound(v, a, b):
    """C_v of (*) and the box M_v outside which R can never return."""
    C = (1 << (v + 1)) * b - a * (1 << v)
    return C, abs(C) + (1 << (v + 1)) + a


class MsbEncoder:
    def __init__(self, n):
        self.n = n
        self.pool = IDPool()
        self.cnf = []
        self.memo = {}

    def T(self, s, d, t):
        return self.pool.id(("T", s, d, t))

    def A(self, s):
        return self.pool.id(("A", s))

    def R(self, v, q):
        return self.pool.id(("R", v, q))

    def add(self, *cl):
        self.cnf.append(list(cl))

    def exactly_one(self, lits):
        self.cnf.append(list(lits))
        for i in range(len(lits)):
            for j in range(i + 1, len(lits)):
                self.add(-lits[i], -lits[j])

    def transitions(self):
        for s in range(self.n):
            for d in (0, 1):
                self.exactly_one([self.T(s, d, t) for t in range(self.n)])
        self.add(self.T(0, 0, 0))              # leading-zero invariance

    def symmetry_break(self):
        slots = [(s, d) for s in range(self.n) for d in (0, 1)]
        for i, (s, d) in enumerate(slots):
            for t in range(2, self.n):
                self.add(-self.T(s, d, t),
                         *[self.T(s2, d2, t - 1) for (s2, d2) in slots[:i]])
        for t in range(1, self.n):
            self.add(*[self.T(s, d, t) for (s, d) in slots])

    def word_state(self, word):
        key = tuple(word)
        if key in self.memo:
            return self.memo[key]
        if not word:
            lits = [self.pool.id(("W", (), s)) for s in range(self.n)]
            self.add(lits[0])
            for s in range(1, self.n):
                self.add(-lits[s])
            self.memo[key] = lits
            return lits
        prev = self.word_state(word[:-1])
        d = word[-1]
        lits = [self.pool.id(("W", key, t)) for t in range(self.n)]
        self.exactly_one(lits)
        for s in range(self.n):
            for t in range(self.n):
                self.add(-prev[s], -self.T(s, d, t), lits[t])
        self.memo[key] = lits
        return lits

    def unit(self, word, positive):
        for s, lit in enumerate(self.word_state(word)):
            self.add(-lit, self.A(s) if positive else -self.A(s))

    def reachable_shape(self, v, a, b):
        """(R, shift) pairs reachable inside the box -- the product skeleton,
        computed once without reference to the DFA."""
        C, M = const_and_bound(v, a, b)
        mask = (1 << (v + 1)) - 1
        seen, stack = {(0, 0)}, [(0, 0)]
        while stack:
            r, sh = stack.pop()
            for d in (0, 1):
                for e in (0, 1):
                    r2 = 2 * r + (1 << (v + 1)) * e - a * d
                    if abs(r2) > M:
                        continue
                    nxt = (r2, ((sh << 1) | d) & mask)
                    if nxt not in seen:
                        seen.add(nxt)
                        stack.append(nxt)
        return sorted(seen), C, mask

    def branch(self, v, a, b):
        n = self.n
        shape, C, mask = self.reachable_shape(v, a, b)
        self.add(self.R(v, (0, 0, 0, 0)))          # q0, q0, R = 0, shift = 0
        for (r, sh) in shape:
            for px in range(n):
                for py in range(n):
                    q = self.R(v, (px, py, r, sh))
                    for d in (0, 1):
                        for e in (0, 1):
                            r2 = 2 * r + (1 << (v + 1)) * e - a * d
                            if abs(r2) > const_and_bound(v, a, b)[1]:
                                continue
                            sh2 = ((sh << 1) | d) & mask
                            for px2 in range(n):
                                for py2 in range(n):
                                    self.add(-q, -self.T(px, d, px2),
                                             -self.T(py, e, py2),
                                             self.R(v, (px2, py2, r2, sh2)))
                    if r == C and sh == (1 << v):
                        # this prefix pair IS a complete (x, F(x)) with
                        # v_2(x) = v: impose the closure implication
                        self.add(-q, -self.A(px), self.A(py))


def orbit(x0, n):
    out, x = [x0], x0
    for _ in range(n - 1):
        x = step1(x)
        assert x != "HALT"
        out.append(x)
    return out


def search(n, vmax, which="needle", orbit_len=40, verbose=True,
           branches=None, orb=None):
    """branches/orb override `which`, for calibration on planted machines."""
    if branches is None:
        branches = {"needle": needle_branch, "times4": times4_branch}[which]
    if orb is None:
        orb = orbit(6, orbit_len) if which == "needle" else \
            [6 * 4 ** i for i in range(orbit_len)]
    enc = MsbEncoder(n)
    enc.transitions()
    enc.symmetry_break()
    for x in orb:
        enc.unit(msb_word(x), True)
    for e in range(2 * n + 6):
        enc.unit(msb_word(1 << e), False)
    for v in range(vmax + 1):
        a, b = branches(v)
        enc.branch(v, a, b)
    t0 = time.time()
    with Solver(name="cadical153", bootstrap_with=enc.cnf) as s:
        sat = s.solve()
        model = set(l for l in s.get_model() if l > 0) if sat else None
    dt = time.time() - t0
    if verbose:
        print(f"  n={n:2d}  vars={enc.pool.top:>9,}  clauses={len(enc.cnf):>11,}  "
              f"{'SAT (certificate found)' if sat else 'UNSAT (no certificate)':<26}"
              f" {dt:8.1f}s")
    if not sat:
        return None
    delta = [[next(t for t in range(n) if enc.T(s, d, t) in model)
              for d in (0, 1)] for s in range(n)]
    return delta, [s for s in range(n) if enc.A(s) in model]


def main():
    nmin = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    vmax = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    which = "times4" if "--times4" in sys.argv else "needle"
    print(f"MSB-first automatic invariant search: {which}, branches v=0..{vmax}")
    for n in range(nmin, nmax + 1):
        got = search(n, vmax, which)
        if got:
            print(f"        delta={got[0]}  accepting={got[1]}")
            return got
    print("  no certificate at any size tested.")


if __name__ == "__main__":
    main()
