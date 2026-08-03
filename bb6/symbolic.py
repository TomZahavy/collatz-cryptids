"""Symbolic macro simulation: block counts as expressions, not integers.

WHAT THIS IS FOR.  To prove "the machine follows the map F" we need a
lemma of the form

    from a configuration whose counter is x, the machine reaches a
    configuration whose counter is 2x + c, in T(x) steps,

FOR ALL x -- not for the particular values a numeric simulator happens to
visit.  That is a statement about a symbolic configuration, so it needs a
simulator whose block counts are expressions.  This is that simulator,
and it is the shared prerequisite for obligations 1-4 in RESULTS.md.  It
is also what produces the certificate a Lean proof would check: the
output is a list of stages with symbolic counts and the guards each
stage needs, which is exactly the data `bbf/lean/Check.lean` consumes.

THE REPRESENTATION.  A count is `a + b*x` with integer a, b and a single
symbolic variable x.  That suffices because within one inner unit the
only thing varying is the counter being doubled; the outer level is
handled by iterating the lemma, not by widening the expression class.

GUARDS.  A macro step that consumes one block from a stack needs that
block to be non-empty, and a chain step consumes a whole block whose
count may be symbolic.  Every such requirement is RECORDED rather than
assumed: `guards` collects the inequalities `a + b*x >= 1` that the run
depends on.  A caller that discharges those guards (they are affine, so
eventual positivity decides them) has a proof for all x in range.

WHAT IS NOT HERE.  No proof.  This produces a certificate -- a claim
about all x, with its hypotheses made explicit.  Checking it is a
separate job, done numerically by `verify_against_concrete` below and
ultimately in Lean.
"""
from tm import TM, HALT
from macro import inner, OK, HALT_IN, INF_IN, L, R


class Lin:
    """`a + b*x` with integer coefficients."""

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a, self.b = a, b

    def __add__(self, o):
        o = o if isinstance(o, Lin) else Lin(o)
        return Lin(self.a + o.a, self.b + o.b)

    def __sub__(self, o):
        o = o if isinstance(o, Lin) else Lin(o)
        return Lin(self.a - o.a, self.b - o.b)

    def __mul__(self, k):
        return Lin(self.a * k, self.b * k)

    def __eq__(self, o):
        o = o if isinstance(o, Lin) else Lin(o)
        return (self.a, self.b) == (o.a, o.b)

    def __hash__(self):
        return hash((self.a, self.b))

    def at(self, x):
        return self.a + self.b * x

    def is_const(self):
        return self.b == 0

    def __repr__(self):
        if self.b == 0:
            return str(self.a)
        s = "x" if self.b == 1 else ("-x" if self.b == -1 else "%dx" % self.b)
        return s if self.a == 0 else "%s%+d" % (s, self.a)


class SymSim:
    """The macro simulator with symbolic block counts.

    Mirrors `macro.MacroSim` step for step; the only difference is that
    counts are `Lin` and that consuming a block records a guard."""

    __slots__ = ("m", "b", "st", "q", "d", "steps", "macro", "halted",
                 "infinite", "tbl", "guards", "trace", "stuck")

    def __init__(self, m, b, st, q, d):
        self.m, self.b = m, b
        self.st = ([list(t) for t in st[L]], [list(t) for t in st[R]])
        self.q, self.d = q, d
        self.steps = Lin()
        self.macro = 0
        self.halted = self.infinite = self.stuck = False
        self.tbl = {}
        self.guards = []          # (Lin, ">=1") requirements
        self.trace = []           # (q, d, symbol, kind, count)

    def _trans(self, q, d, word):
        key = (q, d, word)
        r = self.tbl.get(key)
        if r is None:
            r = self.tbl[key] = inner(self.m, self.b, q, d, word)
        return r

    @staticmethod
    def _push(stk, sym, n):
        if isinstance(n, Lin) and n == Lin(0):
            return
        if stk and stk[-1][0] == sym:
            stk[-1][1] = stk[-1][1] + n
        else:
            stk.append([sym, n if isinstance(n, Lin) else Lin(n)])

    def step(self):
        if self.halted or self.infinite or self.stuck:
            return False
        near = self.st[self.d]
        word = near[-1][0] if near else 0
        r = self._trans(self.q, self.d, word)
        if r[0] == INF_IN:
            self.infinite = True
            return False
        if r[0] == HALT_IN:
            self.halted = True
            return False
        _, nw, xd, nq, cost = r
        if nq == self.q and xd == self.d and near:
            # chain step: the whole block goes, however long it is
            sym, cnt = near.pop()
            self.guards.append((cnt, ">=1"))
            self._push(self.st[1 - self.d], nw, cnt)
            self.steps = self.steps + cnt * cost
            self.trace.append((self.q, self.d, sym, "chain", cnt))
            self.macro += 1
            return True
        if near:
            sym, cnt = near[-1]
            if not cnt.is_const():
                # Taking ONE cell from a symbolic block would need to
                # know whether the block is now empty, and that depends
                # on x: for some x the block survives and the head reads
                # it again, for others it vanishes and the head reads the
                # NEXT block instead.  The two cases are different runs.
                # A symbolic engine that guesses here is not simulating
                # the machine, it is simulating one branch of it -- which
                # is exactly how this file first "worked".  Stop instead;
                # only chain steps, which consume a whole block whatever
                # its length, may cross a symbolic count.
                self.stuck = True
                return False
            self.guards.append((cnt, ">=1"))
            if cnt.a <= 0:
                self.stuck = True
                return False
            if cnt.a == 1:
                near.pop()
            else:
                near[-1][1] = cnt - 1
            self.trace.append((self.q, self.d, sym, "one", Lin(1)))
        else:
            self.trace.append((self.q, self.d, 0, "blank", Lin(1)))
        self._push(self.st[1 - xd], nw, 1)
        self.d, self.q = xd, nq
        self.steps = self.steps + cost
        self.macro += 1
        return True

    def config(self):
        return ([tuple(t) for t in self.st[L]], self.q, self.d,
                [tuple(t) for t in self.st[R]])

    def skeleton(self):
        out = []
        for side in (self.st[L], self.st[R]):
            w = [s for s, _ in reversed(side)]
            while w and w[-1] == 0:
                w.pop()
            out.append(tuple(w))
        return (out[0], self.q, self.d, out[1])

    def counters(self):
        out = []
        for side in (self.st[L], self.st[R]):
            w = list(reversed(side))
            while w and w[-1][0] == 0:
                w.pop()
            out.extend(n for _, n in w)
        return tuple(out)


def from_concrete(msim, sym_index):
    """Take a live `MacroSim` and lift one block count to the symbol x.

    `sym_index` indexes the counters as `MacroSim.counters()` reports
    them, so the symbolic run starts from an observed configuration with
    exactly one coordinate generalised."""
    st = ([list(t) for t in msim.st[L]], [list(t) for t in msim.st[R]])
    order = []
    for side in (L, R):
        blocks = list(reversed(st[side]))
        w = list(blocks)
        while w and w[-1][0] == 0:
            w.pop()
        for j in range(len(w)):
            order.append((side, len(st[side]) - 1 - j))
    for k, (side, pos) in enumerate(order):
        sym, cnt = st[side][pos]
        st[side][pos] = [sym, Lin(0, 1) if k == sym_index else Lin(cnt)]
    return SymSim(msim.m, msim.b, st, msim.q, msim.d)


def verify_against_concrete(code, blk, sym_index, xs, budget=4000):
    """Run the symbolic simulator, then check its claim at concrete x.

    The symbolic run is a claim about every x; this substitutes actual
    values and re-runs the ordinary simulator to the same macro count,
    demanding identical configurations and step counts.  A symbolic
    engine that has not been confronted with ground truth is worth
    nothing, and this is the confrontation."""
    from macro import MacroSim
    m = TM(code)
    checked = 0
    for x in xs:
        # build the concrete start from the symbolic start at this x
        base = MacroSim(m, blk)
        while base.macro < 400 and not base.halted:
            base.step()
        sym = from_concrete(base, sym_index)
        # Materialise at this x.  Nothing is dropped and nothing merged:
        # every count except the lifted one comes from a real
        # configuration and is already >= 1, and the lifted one is >= 1
        # by the choice of x.  Dropping or merging here would change the
        # block boundaries and the two runs would diverge for a reason
        # that has nothing to do with the machine.
        if any(c.at(x) < 1 for side in (L, R) for _, c in sym.st[side]):
            continue
        conc = MacroSim(m, blk)
        conc.st = ([(s, c.at(x)) for s, c in sym.st[L]],
                   [(s, c.at(x)) for s, c in sym.st[R]])
        conc.q, conc.d = sym.q, sym.d
        s2 = SymSim(m, blk, sym.st, sym.q, sym.d)
        n = 0
        while n < budget and s2.step():
            n += 1
        for _ in range(n):
            if not conc.step():
                break
        assert conc.macro == n, (code, x, conc.macro, n)
        assert conc.steps == s2.steps.at(x), \
            ("step count", code, x, conc.steps, s2.steps.at(x))
        cs = tuple((s, c) for s, c in conc.st[L]), tuple(
            (s, c) for s, c in conc.st[R])
        ss = (tuple((s, c.at(x)) for s, c in s2.st[L]),
              tuple((s, c.at(x)) for s, c in s2.st[R]))
        assert cs == ss, ("config", code, x, cs, ss)
        checked += 1
    return checked


if __name__ == "__main__":
    print("symbolic.py selftest")
    a = Lin(3, 2)
    assert (a + 4).at(5) == 17 and (a * 3).at(2) == 21
    assert repr(Lin(0, 1)) == "x" and repr(Lin(-1, 2)) == "2x-1"
    print("  ok  Lin arithmetic")
    THREE = ["1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE",
             "1RB1RE_1LC0RA_1RD0LB_1LB1RC_1LF0RD_---0LE",
             "1RB1LC_1RC0LD_1LA0RB_1LB1LE_1RF0LA_---0RE"]
    tot = 0
    for code in THREE:
        for idx in (0, 1):
            tot += verify_against_concrete(code, 2, idx,
                                           [7, 12, 23, 40, 91, 150])
    print("  ok  %d symbolic runs confirmed against the concrete simulator"
          % tot)
    print("all pass")
