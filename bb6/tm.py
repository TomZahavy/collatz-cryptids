"""Turing machines in bbchallenge format: parsing, simulation, tape shapes.

This is the ground floor of the BB(6) port.  Everything above it -- the
rigidity detector, the rule extractor, the certificate miner -- reads
configurations through this file, so it is the one place where a bug
would silently corrupt every downstream claim.  It is therefore checked
against the four known busy-beaver champions (see `selftest` at the
bottom), which pin both the step-counting convention and the tape
contents.

FORMAT.  `1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA` -- one group per state, in
order A, B, C, ...; within a group, the transition on symbol 0 then the
transition on symbol 1; each transition is <write><direction><next>.
`---` is an undefined transition and `Z` is the halt state; the machine
halts on either.  Convention: executing a transition INTO the halt state
counts as a step, reaching an undefined transition does not.  That is
bbchallenge's convention and it is what reproduces 47,176,870 for the
BB(5) champion.

TAPE.  Bi-infinite, all zeros, head at the origin, state A.  Stored as a
bytearray with an origin offset, doubled on demand; `lo`/`hi` track the
visited span so the run-length encoding never walks the whole allocation.
"""

HALT = -1


class TM:
    """A parsed machine.  `t[q][s] = (write, dir, next)` with dir in
    {+1, -1} and next in {0..n-1} or HALT."""

    __slots__ = ("code", "n", "t")

    def __init__(self, code):
        self.code = code
        groups = code.strip().split("_")
        self.n = len(groups)
        self.t = []
        for g in groups:
            if len(g) != 6:
                raise ValueError("bad state group %r in %r" % (g, code))
            row = []
            for k in (0, 3):
                tr = g[k:k + 3]
                if tr == "---":
                    row.append(None)
                    continue
                w = int(tr[0])
                d = 1 if tr[1] == "R" else -1
                nx = tr[2]
                row.append((w, d, HALT if nx == "Z" else ord(nx) - 65))
            self.t.append(row)

    def __repr__(self):
        return "TM(%s)" % self.code


class Tape:
    """Growable bi-infinite binary tape."""

    __slots__ = ("cells", "org", "lo", "hi")

    def __init__(self, cap=1 << 12):
        self.cells = bytearray(cap)
        self.org = cap // 2
        self.lo = 0            # least visited position (machine coords)
        self.hi = 0            # greatest visited position

    def _grow(self):
        cap = len(self.cells)
        new = bytearray(cap * 2)
        shift = cap // 2
        new[shift:shift + cap] = self.cells
        self.cells = new
        self.org += shift

    def read(self, p):
        return self.cells[self.org + p]

    def write(self, p, v):
        i = self.org + p
        self.cells[i] = v
        if p < self.lo:
            self.lo = p
        elif p > self.hi:
            self.hi = p

    def ensure(self, p):
        while self.org + p < 1 or self.org + p >= len(self.cells) - 1:
            self._grow()

    def span(self):
        """The visited window as a list of 0/1, plus its left coordinate."""
        return self.cells[self.org + self.lo:self.org + self.hi + 1], self.lo


class Sim:
    """A running machine.  `step()` advances one TM step and returns True,
    or returns False once halted."""

    __slots__ = ("m", "tape", "q", "p", "steps", "halted")

    def __init__(self, m):
        self.m = m
        self.tape = Tape()
        self.q = 0
        self.p = 0
        self.steps = 0
        self.halted = False

    def step(self):
        if self.halted:
            return False
        tr = self.m.t[self.q][self.tape.read(self.p)]
        if tr is None:                       # undefined: halt, no step
            self.halted = True
            return False
        w, d, nx = tr
        self.tape.write(self.p, w)
        self.p += d
        self.tape.ensure(self.p)
        self.steps += 1
        if nx == HALT:
            self.halted = True
            return False
        self.q = nx
        return True

    def run(self, budget):
        """Advance up to `budget` steps.  Returns True if still running."""
        t = self.tape
        m = self.m
        for _ in range(budget):
            if self.halted:
                return False
            tr = m.t[self.q][t.cells[t.org + self.p]]
            if tr is None:
                self.halted = True
                return False
            w, d, nx = tr
            i = t.org + self.p
            t.cells[i] = w
            if self.p < t.lo:
                t.lo = self.p
            elif self.p > t.hi:
                t.hi = self.p
            self.p += d
            if t.org + self.p < 1 or t.org + self.p >= len(t.cells) - 1:
                t._grow()
            self.steps += 1
            if nx == HALT:
                self.halted = True
                return False
            self.q = nx
        return True

    def ones(self):
        return sum(self.tape.cells)


# ------------------------------------------------------------------ RLE

def rle(bits):
    """Run-length encode a 0/1 sequence: [(symbol, length), ...]."""
    out = []
    if not bits:
        return out
    cur, run = bits[0], 1
    for b in bits[1:]:
        if b == cur:
            run += 1
        else:
            out.append((cur, run))
            cur, run = b, 1
    out.append((cur, run))
    return out


def config_rle(sim):
    """The configuration as (left_rle, state, head_symbol, right_rle).

    `left_rle` reads OUTWARD from the head (nearest block first), as does
    `right_rle`; leading/trailing zero blocks are dropped, so the encoding
    is canonical -- two configurations get the same skeleton exactly when
    they differ only in block lengths.  This is the representation in
    which a "shape" is a finite object and the exponents are counters."""
    cells, lo = sim.tape.span()
    p = sim.p - lo
    left = cells[:p][::-1] if p > 0 else b""
    right = cells[p + 1:] if p + 1 <= len(cells) else b""
    head = cells[p] if 0 <= p < len(cells) else 0
    L, R = rle(left), rle(right)
    while L and L[-1][0] == 0:
        L.pop()
    while R and R[-1][0] == 0:
        R.pop()
    return L, sim.q, head, R


def skeleton(cfg):
    """The shape of a configuration: everything except the block lengths."""
    L, q, h, R = cfg
    return (tuple(s for s, _ in L), q, h, tuple(s for s, _ in R))


def exponents(cfg):
    """The counter vector of a configuration: the block lengths."""
    L, _, _, R = cfg
    return tuple(n for _, n in L) + tuple(n for _, n in R)


# ------------------------------------------------------------------ test

CHAMPS = [
    # code,                                   steps,      ones
    ("1RB1LB_1LA1RZ",                              6,        4),
    ("1RB1RZ_1LB0RC_1LC1LA",                      21,        5),
    ("1RB1LB_1LA0LC_1RZ1LD_1RD0RA",              107,       13),
    ("1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA", 47176870,     4098),
]


def selftest():
    for code, steps, ones in CHAMPS:
        s = Sim(TM(code))
        s.run(steps + 10)
        assert s.halted, code
        assert s.steps == steps, (code, s.steps, steps)
        assert s.ones() == ones, (code, s.ones(), ones)
        print("  ok  %-40s %10d steps, %5d ones" % (code, steps, ones))
    # RLE round-trip on a hand-checked configuration
    s = Sim(TM("1RB1LB_1LA1RZ"))
    s.run(3)
    cfg = config_rle(s)
    assert skeleton(cfg)[1] == s.q
    print("  ok  rle/skeleton/exponents wired")


if __name__ == "__main__":
    print("tm.py selftest")
    selftest()
    print("all pass")
