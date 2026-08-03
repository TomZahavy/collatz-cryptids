"""Macro machines: the acceleration that actually bites.

THE MEASUREMENT THAT FORCED THIS.  Chain steps (`blocktape.py`) cross a
whole run of identical cells in one move, but only when the machine has a
transition delta(q, s) = (w, d, q) -- a self-loop that keeps both the
state and the direction.  Measured on the BB(6) holdout list, that buys a
factor of about 1.2.  Useless.  These machines do not sit still; they
bounce.

THE FIX (Marxen-Buntrock).  Cut the tape into blocks of b cells and treat
each block as one symbol of a new machine.  Entering a block from one
side in TM state q, the head bounces around INSIDE the block for a while
and then leaves -- so the macro machine's transition is

    (q, direction, block word)  ->  (new word, exit direction, new state,
                                     exact number of base steps)

computed once, by simulating inside the block.  A self-loop of the MACRO
machine -- enter left in state q, leave right in state q -- is a common
event even when the base machine has none, because all the bouncing is
now hidden inside one macro transition.  Chain steps then fire, and the
speedup is the length of a uniform block run rather than nothing.

TWO DECISIONS FOR FREE.  Simulating inside a block terminates in one of
three ways, and two of them settle the machine on the spot:

  * the head leaves      -- an ordinary macro transition;
  * the machine halts    -- HALTS;
  * neither, past the pigeonhole bound |Q| * b * 2^b -- the head is
    trapped in a bounded region forever, so the machine NEVER HALTS.
    This is a proof, not a heuristic: a configuration must repeat.

CHOOSING b.  There is no best block size; b is a representation, and a
machine invisible at one b can be transparent at another.  We try a range
and keep the reading that shows the most structure, which is a search,
not a gamble -- every b gives exact base-step counts, so nothing
downstream depends on the choice being right.

CORRECTNESS.  As with `blocktape.py`, everything downstream assumes
step-exactness, so it is cross-checked against `tm.py` -- the dumb
cell-at-a-time simulator -- for every block size, on the champions, on
the holdout list, and on thousands of random machines.
"""
from tm import TM, Sim, HALT

L, R = 0, 1

OK, HALT_IN, INF_IN = 0, 1, 2


def inner(m, b, q, d, word):
    """Simulate inside one block.

    The block is `b` cells, bit i of `word` being cell i (cell 0
    leftmost).  The head enters at the left edge travelling right when
    d == R, at the right edge travelling left when d == L.

    Returns (OK, new word, exit direction, new state, base steps) or
    (HALT_IN, new word, steps) or (INF_IN,)."""
    cells = [(word >> i) & 1 for i in range(b)]
    p = 0 if d == R else b - 1
    steps = 0
    limit = m.n * b * (1 << b) + 8      # pigeonhole: |Q| * positions * words
    while 0 <= p < b:
        tr = m.t[q][cells[p]]
        if tr is None:
            return (HALT_IN, sum(c << i for i, c in enumerate(cells)), steps)
        w, dd, nx = tr
        cells[p] = w
        p += dd
        steps += 1
        if nx == HALT:
            return (HALT_IN, sum(c << i for i, c in enumerate(cells)), steps)
        q = nx
        if steps > limit:
            return (INF_IN,)
    return (OK, sum(c << i for i, c in enumerate(cells)),
            R if p >= b else L, q, steps)


class MacroSim:
    """The block-tape simulator, run over macro symbols.

    Identical in shape to `blocktape.BlockSim` -- two stacks of
    run-length blocks with the head between them -- except that a
    "symbol" is a b-cell word and a "step" is a whole macro transition.
    `steps` remains the exact base-TM step count."""

    __slots__ = ("m", "b", "st", "q", "d", "steps", "macro", "halted",
                 "infinite", "tbl")

    def __init__(self, m, b):
        self.m = m
        self.b = b
        self.st = ([], [])
        self.q = 0
        self.d = R
        self.steps = 0
        self.macro = 0
        self.halted = False
        self.infinite = False
        self.tbl = {}

    def trans(self, q, d, word):
        key = (q, d, word)
        r = self.tbl.get(key)
        if r is None:
            r = inner(self.m, self.b, q, d, word)
            self.tbl[key] = r
        return r

    @staticmethod
    def _push(stk, sym, n):
        if n == 0:
            return
        if stk and stk[-1][0] == sym:
            stk[-1] = (sym, stk[-1][1] + n)
        else:
            stk.append((sym, n))

    def step(self):
        if self.halted or self.infinite:
            return False
        near = self.st[self.d]
        word = near[-1][0] if near else 0
        r = self.trans(self.q, self.d, word)
        if r[0] == INF_IN:
            self.infinite = True          # trapped in one block forever
            return False
        if r[0] == HALT_IN:
            # the head stopped inside the block, so the block never left
            # the tape: put its final contents back, or the last writes
            # before halting would be lost
            if near:
                s, k = near[-1]
                if k == 1:
                    near.pop()
                else:
                    near[-1] = (s, k - 1)
            self._push(near, r[1], 1)
            self.steps += r[2]
            self.macro += 1
            self.halted = True
            return False
        _, nw, xd, nq, cost = r
        # chain step: same state out as in, and the head keeps going the
        # way it was already going -- so it crosses the entire run
        if nq == self.q and xd == self.d and near:
            _, k = near.pop()
            self._push(self.st[1 - self.d], nw, k)
            self.steps += cost * k
            self.macro += 1
            return True
        if near:
            s, k = near[-1]
            if k == 1:
                near.pop()
            else:
                near[-1] = (s, k - 1)
        self._push(self.st[1 - xd], nw, 1)
        self.d = xd
        self.q = nq
        self.steps += cost
        self.macro += 1
        return True

    # -- observation -----------------------------------------------------
    def at_edge(self):
        return not self.st[self.d]

    def nblocks(self):
        return len(self.st[L]) + len(self.st[R])

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

    def tape_bits(self):
        """Expand to base cells: (bits, head index)."""
        bits = []
        for s, n in self.st[L]:
            for _ in range(n):
                bits.extend((s >> i) & 1 for i in range(self.b))
        idx = len(bits)
        for s, n in reversed(self.st[R]):
            for _ in range(n):
                bits.extend((s >> i) & 1 for i in range(self.b))
        return bits, idx


# ---------------------------------------------------------------- checking

def cross_check(code, b, nsteps):
    """Compare against the cell simulator at a common base-step count."""
    m = TM(code)
    a = Sim(TM(code))
    s = MacroSim(m, b)
    while not (s.halted or s.infinite) and s.steps < nsteps:
        s.step()
    if s.infinite:
        # the pigeonhole verdict is a proof, but a wrong bound would be
        # invisible, so confront it with the base simulator
        a.run(300000)
        assert not a.halted, ("claimed trapped but halts", code, b, a.steps)
        return None
    a.run(s.steps)
    assert a.steps == s.steps, (code, b, a.steps, s.steps)
    if s.halted:
        chk = Sim(TM(code))
        chk.run(s.steps + 16)
        assert chk.halted and chk.steps == s.steps, \
            ("halt step mismatch", code, b, chk.steps, s.steps, chk.halted)
    bits, idx = s.tape_bits()
    cells, lo = a.tape.span()
    ha = a.p - lo
    ca = list(cells)
    if s.halted:
        # the head stopped somewhere INSIDE a block, and the two-stack
        # model does not record where: it only ever places the head
        # between blocks.  The tape contents are still fully determined,
        # so compare those and leave the head out of it.
        x, y = list(bits), list(ca)
        for v in (x, y):
            while v and v[0] == 0:
                v.pop(0)
            while v and v[-1] == 0:
                v.pop()
        assert x == y, (code, b, s.steps, x, y)
        return s.steps, s.macro
    # the head may sit just outside the written span -- `Tape` records a
    # cell only once something is written to it -- so ha can be -1 or
    # len(ca).  Slicing with a negative index would silently split the
    # tape in the wrong place, which is how this check first "passed".
    if ha < 0:
        la, hda, ra = [], 0, list(ca)
    elif ha >= len(ca):
        la, hda, ra = list(ca), 0, []
    else:
        la, hda, ra = ca[:ha], ca[ha], ca[ha + 1:]
    hb = idx if s.d == R else idx - 1
    if hb < 0:
        lb, hdb, rb = [], 0, list(bits)
    elif hb >= len(bits):
        lb, hdb, rb = list(bits), 0, []
    else:
        lb, hdb, rb = bits[:hb], bits[hb], bits[hb + 1:]
    for v in (la, lb):
        while v and v[0] == 0:
            v.pop(0)
    for v in (ra, rb):
        while v and v[-1] == 0:
            v.pop()
    assert (la, hda, ra) == (lb, hdb, rb), \
        (code, b, s.steps, (la, hda, ra), (lb, hdb, rb))
    return s.steps, s.macro


def selftest():
    import random
    from tm import CHAMPS
    for b in (1, 2, 3, 4, 5):
        for code, steps, ones in CHAMPS:
            m = TM(code)
            s = MacroSim(m, b)
            while not (s.halted or s.infinite) and s.steps < steps + 10:
                s.step()
            assert s.halted and s.steps == steps, (code, b, s.steps, steps)
            bits, _ = s.tape_bits()
            assert sum(bits) == ones, (code, b, sum(bits), ones)
    print("  ok  champions exact at every block size b = 1..5")

    m = TM(CHAMPS[-1][0])
    for b in (1, 2, 3, 4, 5, 6, 8):
        s = MacroSim(m, b)
        while not (s.halted or s.infinite):
            s.step()
        print("      BB(5) b=%d: %8d macro steps (x%.0f)"
              % (b, s.macro, s.steps / s.macro))

    codes = [ln.strip() for ln in
             open("../bbf/bb6_holdouts_1064.txt")][:40]
    for c in codes:
        for b in (1, 2, 3, 4, 5):
            cross_check(c, b, 100000)
    print("  ok  40 holdouts x 5 block sizes cross-checked, tape-identical")

    random.seed(11)
    n = 0
    for _ in range(1200):
        g = []
        for _ in range(6):
            tr = []
            for _ in range(2):
                if random.random() < 0.06:
                    tr.append("---")
                else:
                    tr.append(random.choice("01") + random.choice("LR") +
                              random.choice("ABCDEF"))
            g.append("".join(tr))
        code = "_".join(g)
        for b in (2, 3, 4):
            if cross_check(code, b, 4000) is not None:
                n += 1
    print("  ok  %d random machine/block-size pairs cross-checked" % n)


if __name__ == "__main__":
    print("macro.py selftest")
    selftest()
    print("all pass")
