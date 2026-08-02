"""WS1 by SAT: automatic non-halting certificates, beyond the enumeration wall.

The brute-force search (search.py) visits every canonical ICDFA, which costs
256 million structures at 7 states and is hopeless past that.  Here the
transition structure itself becomes SAT variables, exactly as bbchallenge's FAR
`mitm_dfa` does for tape languages.

VARIABLES
    T[s][c][t]   delta(s, c) = t          (exactly one t per (s, c))
    A[s]         s is accepting
    R_v[q]       the product state q is reachable in the branch-v product
    P[w][s]      the DFA is in state s after reading the word w from the start

THE PRODUCT.  On branch v the map is y = a k + b with x = 2^{v+1}k + 2^v, so a
DFA run on x and a DFA run on y can be tracked together with the multiply-add
carry.  A product state is (px, c, ry, phase): DFA state on x, carry, DFA state
on y, and a phase distinguishing "reading k's digits" from "flushing the
remaining carry".  Emission happens when the flush empties, giving a pair
(px, ry) whose meaning is: some x in this branch reaches px while F(x) reaches
ry.  The certificate condition F(I) subset of I is then A[px] -> A[ry].

SOUNDNESS OF "UNSAT".  Only the FORWARD closure of R is encoded (start is
reachable; reachable states propagate).  That forces R to contain the true
reachable set but permits R to equal it -- and R = reach does satisfy forward
closure.  So if a certificate exists, an assignment with R = reach satisfies the
formula.  Hence UNSAT implies no certificate exists, which is what the
impossibility theorem needs.  (An over-approximating R would break this: it
would impose the pair implication on unreachable states and could report UNSAT
spuriously.  The forward-only encoding is deliberate.)

CONVENTION.  With `--invariant` the DFA is additionally required to satisfy
A[s] = A[delta(s,0)], i.e. it accepts every representation of its members, not
only the minimal ones.  Every 2-automatic set admits such a DFA, so this is not
a smaller class of sets -- only a different state-count measure.  Without the
flag the general minimal-word convention is used, which needs the extra
"state after the last emitted 1" component and is more expensive.

Usage:  python3 sat_search.py [needle|times4] [nmin] [nmax] [vmax] [--general]
"""
import sys
import time

from dfa_invariant import lsb_word, needle_branch, times4_branch

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
from needle import step1                                   # noqa: E402

from pysat.formula import IDPool                           # noqa: E402
from pysat.solvers import Solver                           # noqa: E402

READ, FLUSH = 0, 1


def orbit(x0, n):
    out, x = [x0], x0
    for _ in range(n - 1):
        x = step1(x)
        assert x != "HALT", "orbit halted"
        out.append(x)
    return out


def carries(a, b):
    """Every carry the branch can produce, by abstract simulation."""
    seen, stack = {b}, [b]
    while stack:
        c = stack.pop()
        for kappa in (0, 1):
            for nc in ((a * kappa + c) >> 1, c >> 1):
                if nc not in seen:
                    seen.add(nc)
                    stack.append(nc)
    return sorted(seen)


class Encoder:
    def __init__(self, n, general):
        self.n, self.general = n, general
        self.pool = IDPool()
        self.cnf = []
        self.NONE = n                       # sentinel for "no 1 emitted yet"

    def T(self, s, c, t):
        return self.pool.id(("T", s, c, t))

    def A(self, s):
        return self.pool.id(("A", s))

    def R(self, v, q):
        return self.pool.id(("R", v, q))

    def add(self, *clause):
        self.cnf.append(list(clause))

    def exactly_one(self, lits):
        self.cnf.append(list(lits))
        for i in range(len(lits)):
            for j in range(i + 1, len(lits)):
                self.add(-lits[i], -lits[j])

    # ---------------------------------------------------------------- setup --
    def transitions(self):
        for s in range(self.n):
            for c in (0, 1):
                self.exactly_one([self.T(s, c, t) for t in range(self.n)])

    def word_state(self, word, memo):
        """One-hot variables for the state reached after `word`; memoised."""
        key = tuple(word)
        if key in memo:
            return memo[key]
        if not word:
            lits = [self.pool.id(("W", (), s)) for s in range(self.n)]
            self.add(lits[0])                          # start state is 0
            for s in range(1, self.n):
                self.add(-lits[s])
            memo[key] = lits
            return lits
        prev = self.word_state(word[:-1], memo)
        b = word[-1]
        lits = [self.pool.id(("W", key, t)) for t in range(self.n)]
        self.exactly_one(lits)
        for s in range(self.n):
            for t in range(self.n):
                self.add(-prev[s], -self.T(s, b, t), lits[t])
        memo[key] = lits
        return lits

    def unit_word(self, word, memo, positive):
        """Force the state after `word` to be accepting / rejecting."""
        lits = self.word_state(word, memo)
        for s in range(self.n):
            self.add(-lits[s], self.A(s) if positive else -self.A(s))

    # -------------------------------------------------------------- product --
    def branch(self, v, a, b):
        """Encode the branch-v product and its pair implications."""
        n, NONE = self.n, self.NONE
        cs = carries(a, b)
        rls = range(n + 1) if self.general else [NONE]

        def q_id(px, c, ry, rl, ph):
            return (px, c, ry, rl, ph)

        # --- the start state: run the prefix 0^v 1, then begin READ ---
        pre = self.word_state([0] * v + [1], {} if False else self.memo)
        for s in range(n):
            self.add(-pre[s], self.R(v, q_id(s, b, 0, NONE, READ)))

        # --- forward closure ---
        for px in range(n):
            for c in cs:
                for ry in range(n):
                    for rl in rls:
                        # READ phase
                        q = self.R(v, q_id(px, c, ry, rl, READ))
                        for kappa in (0, 1):
                            t = a * kappa + c
                            bit, c2 = t & 1, t >> 1
                            # kappa = 1 may END k's minimal word (-> FLUSH) or
                            # the word may continue (-> READ).  BOTH successors
                            # are reachable; only taking FLUSH would restrict k
                            # to a single 1 bit and make the search unsound.
                            phases = (READ, FLUSH) if kappa == 1 else (READ,)
                            for px2 in range(n):
                                for ry2 in range(n):
                                    rl2 = (ry2 if bit else rl) if self.general \
                                        else NONE
                                    for ph2 in phases:
                                        self.add(-q, -self.T(px, kappa, px2),
                                                 -self.T(ry, bit, ry2),
                                                 self.R(v, q_id(px2, c2, ry2,
                                                                rl2, ph2)))
                        # FLUSH phase
                        qf = self.R(v, q_id(px, c, ry, rl, FLUSH))
                        if c:
                            bit, c2 = c & 1, c >> 1
                            for ry2 in range(n):
                                rl2 = (ry2 if bit else rl) if self.general \
                                    else NONE
                                self.add(-qf, -self.T(ry, bit, ry2),
                                         self.R(v, q_id(px, c2, ry2, rl2,
                                                        FLUSH)))
                        else:
                            # flush complete: emit the pair (px, target)
                            tgt = rl if (self.general and rl != NONE) else ry
                            if self.general and rl == NONE:
                                continue      # y >= 1, so some 1 was emitted
                            self.add(-qf, -self.A(px), self.A(tgt))

    def symmetry_break(self):
        """Require BFS-canonical state numbering (the ICDFA canonical form).

        Transitions are ordered (0,0), (0,1), (1,0), (1,1), ...  A state index
        t >= 1 may be the target of slot i only if t-1 is already the target of
        some earlier slot.  Every DFA is isomorphic to exactly one automaton in
        this form, so imposing it loses no certificate and keeps UNSAT sound --
        it only removes the n! relabelling copies of each candidate, which are
        what makes the plain encoding slow.
        """
        slots = [(s, c) for s in range(self.n) for c in (0, 1)]
        # state 0 is discovered from the start, so t = 1 needs no predecessor;
        # for t >= 2 the first appearance of t-1 must precede that of t.
        for i, (s, c) in enumerate(slots):
            for t in range(2, self.n):
                earlier = [self.T(s2, c2, t - 1) for (s2, c2) in slots[:i]]
                self.add(-self.T(s, c, t), *earlier)
        for t in range(1, self.n):                   # every state is used
            self.add(*[self.T(s, c, t) for (s, c) in slots])

    def zero_invariance(self):
        for s in range(self.n):
            for t in range(self.n):
                self.add(-self.T(s, 0, t), -self.A(s), self.A(t))
                self.add(-self.T(s, 0, t), self.A(s), -self.A(t))


def search(which, n, vmax, general, orbit_len=40, verbose=True, basin_bits=0):
    branches = {"needle": needle_branch, "times4": times4_branch}[which]
    orb = orbit(6, orbit_len) if which == "needle" else \
        [6 * 4 ** i for i in range(orbit_len)]

    enc = Encoder(n, general)
    enc.memo = {}
    enc.transitions()
    enc.symmetry_break()
    if not general:
        enc.zero_invariance()
    for x in orb:
        enc.unit_word(lsb_word(x), enc.memo, True)
    # Implied clauses: I is F-closed and misses H, hence misses every
    # F^{-j}(H).  Handing the solver the basin saves it j rounds of product
    # reasoning; the satisfying assignments are unchanged.  See basin.py.
    # basin_bits > 0 uses the full basin below 2^basin_bits; the negative
    # value -B uses ONLY the powers of 2 below 2^B, which separates "more
    # halt values" from "deeper halt values" in the comparison.
    if basin_bits > 0 and which == "needle":
        from basin import basin as halting_basin
        rejects = halting_basin(basin_bits)
    elif basin_bits < 0:
        rejects = [1 << e for e in range(-basin_bits + 1)]
    else:
        rejects = [1 << e for e in range(2 * n + 6)]
    for x in rejects:
        enc.unit_word(lsb_word(x), enc.memo, False)
    for v in range(vmax + 1):
        a, b = branches(v)
        enc.branch(v, a, b)

    t0 = time.time()
    with Solver(name="cadical153", bootstrap_with=enc.cnf) as s:
        sat = s.solve()
        model = set(l for l in s.get_model() if l > 0) if sat else None
    dt = time.time() - t0
    if verbose:
        print(f"  n={n:2d}  vars={enc.pool.top:>9,}  clauses={len(enc.cnf):>10,}  "
              f"{'SAT (certificate found)' if sat else 'UNSAT (no certificate)':<26}"
              f" {dt:7.1f}s")
    if not sat:
        return None
    delta = [[next(t for t in range(n) if enc.T(s, c, t) in model)
              for c in (0, 1)] for s in range(n)]
    acc = [s for s in range(n) if enc.A(s) in model]
    return delta, acc


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "needle"
    nmin = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    nmax = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    vmax = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    general = "--general" in sys.argv
    print(f"machine={which}  branches v=0..{vmax}  "
          f"convention={'minimal words (general)' if general else 'all representations (0-invariant)'}")
    for n in range(nmin, nmax + 1):
        got = search(which, n, vmax, general)
        if got:
            delta, acc = got
            print(f"        delta={delta}  accepting={acc}")
            return
    print("  no certificate at any size tested.")


if __name__ == "__main__":
    main()
