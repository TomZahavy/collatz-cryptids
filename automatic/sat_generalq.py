"""WS1 by SAT in any base -- the base-q counterpart of sat_search.py.

Matches general.py's semantics exactly (minimal-word convention, per-branch
`allow_empty` for the empty tail), so the two can be cross-validated wherever
the enumeration can still run.  See sat_search.py for the encoding and for why
encoding only the FORWARD closure of the product keeps "UNSAT" sound.
"""
import time

from general import lsb_word
from pysat.formula import IDPool
from pysat.solvers import Solver

READ, FLUSH = 0, 1


class QEncoder:
    def __init__(self, n, q):
        self.n, self.q = n, q
        self.pool = IDPool()
        self.cnf = []
        self.NONE = n
        self.memo = {}

    def T(self, s, d, t):
        return self.pool.id(("T", s, d, t))

    def A(self, s):
        return self.pool.id(("A", s))

    def R(self, i, q):
        return self.pool.id(("R", i, q))

    def add(self, *cl):
        self.cnf.append(list(cl))

    def exactly_one(self, lits):
        self.cnf.append(list(lits))
        for i in range(len(lits)):
            for j in range(i + 1, len(lits)):
                self.add(-lits[i], -lits[j])

    def transitions(self):
        for s in range(self.n):
            for d in range(self.q):
                self.exactly_one([self.T(s, d, t) for t in range(self.n)])

    def symmetry_break(self):
        slots = [(s, d) for s in range(self.n) for d in range(self.q)]
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
        lits = self.word_state(word)
        for s in range(self.n):
            self.add(-lits[s], self.A(s) if positive else -self.A(s))

    def carries(self, A, B):
        seen, stack = {B}, [B]
        while stack:
            c = stack.pop()
            for d in range(self.q):
                for nc in ((A * d + c) // self.q, c // self.q):
                    if nc not in seen:
                        seen.add(nc)
                        stack.append(nc)
        return sorted(seen)

    def branch(self, idx, prefix, A, B, allow_empty):
        n, q, NONE = self.n, self.q, self.NONE
        cs = self.carries(A, B)
        pre = self.word_state(list(prefix))
        for s in range(n):                                  # start of the tail
            self.add(-pre[s], self.R(idx, (s, B, 0, NONE, READ)))
            if allow_empty:                                 # the tail may be m=0
                self.add(-pre[s], self.R(idx, (s, B, 0, NONE, FLUSH)))
        for px in range(n):
            for c in cs:
                for ry in range(n):
                    for rl in range(n + 1):
                        q_read = self.R(idx, (px, c, ry, rl, READ))
                        for d in range(q):
                            t = A * d + c
                            dig, c2 = t % q, t // q
                            phases = (READ, FLUSH) if d else (READ,)
                            for px2 in range(n):
                                for ry2 in range(n):
                                    rl2 = ry2 if dig else rl
                                    for ph in phases:
                                        self.add(-q_read,
                                                 -self.T(px, d, px2),
                                                 -self.T(ry, dig, ry2),
                                                 self.R(idx, (px2, c2, ry2,
                                                              rl2, ph)))
                        q_fl = self.R(idx, (px, c, ry, rl, FLUSH))
                        if c:
                            dig, c2 = c % q, c // q
                            for ry2 in range(n):
                                rl2 = ry2 if dig else rl
                                self.add(-q_fl, -self.T(ry, dig, ry2),
                                         self.R(idx, (px, c2, ry2, rl2, FLUSH)))
                        elif rl != NONE:
                            self.add(-q_fl, -self.A(px), self.A(rl))


def search_sat(n, q, branches, orbit, halt_values, verbose=True):
    enc = QEncoder(n, q)
    enc.transitions()
    enc.symmetry_break()
    for x in orbit:
        enc.unit(lsb_word(x, q), True)
    for h in halt_values:
        enc.unit(lsb_word(h, q), False)
    for i, (prefix, A, B, ae) in enumerate(branches):
        enc.branch(i, prefix, A, B, ae)
    t0 = time.time()
    with Solver(name="cadical153", bootstrap_with=enc.cnf) as s:
        sat = s.solve()
        model = set(l for l in s.get_model() if l > 0) if sat else None
    dt = time.time() - t0
    if verbose:
        print(f"  n={n:2d}  vars={enc.pool.top:>10,}  clauses={len(enc.cnf):>11,}  "
              f"{'SAT (certificate)' if sat else 'UNSAT (no certificate)':<24}"
              f" {dt:8.1f}s")
    if not sat:
        return None
    delta = [[next(t for t in range(n) if enc.T(s, d, t) in model)
              for d in range(q)] for s in range(n)]
    return delta, [s for s in range(n) if enc.A(s) in model]
