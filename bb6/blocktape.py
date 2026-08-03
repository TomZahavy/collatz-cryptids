"""Block-tape simulation: the acceleration that makes BB(6) legible.

WHY THIS EXISTS.  A cell-at-a-time simulator run for two million steps on
a BB(6) holdout sees the head visit about fifty new cells.  Fifty.  The
structure these machines have lives at a scale a raw simulator cannot
reach, which is why the raw rigidity scan came back 70% "too few phases".
This is the same wall `fractran_accel.py` hit and solved for FRACTRAN,
and it has the same fix: stop counting steps the machine is not thinking
during.

THE MODEL.  The tape is two stacks of run-length blocks with the head
between them, facing a direction:

        left blocks ...  <q, d>  ... right blocks

Facing `d`, the head reads the nearest cell on side `d`.  One step pops a
cell from that side, writes, and pushes the written cell to the side it
came from -- because after moving in direction `dd`, the cell just
written is behind the head:

    pop s from stack[d];  (w, dd, q') = delta(q, s);
    push w onto stack[-dd];  d := dd;  q := q'

THE ACCELERATION (a "chain step", Marxen-Buntrock).  If

    delta(q, s) = (w, d, q)

-- same state, same direction as the head is already travelling -- then
the head crosses an ENTIRE block of s's without ever consulting anything
else.  A block of length k is then one macro step worth k real steps.
This is exact, not approximate: the certificate is the number k, and the
step counter is advanced by exactly k.

That single rule is what converts these machines from opaque to
readable, because a machine that builds long uniform runs -- which is
what "rigid" means on a tape -- is precisely a machine that spends
almost all of its steps inside chain steps.

WHAT IS AND IS NOT HERE.  Chain steps only.  The next rung of the ladder
is Marxen-Buntrock induction rules ("this word maps to that word,
provably, for every exponent"), which accelerate the bouncing that chain
steps leave behind.  Section events -- the moments the head runs off the
end of the written tape -- come out of this model for free, in O(1), and
they are the phase boundaries the detector needs.

CORRECTNESS.  Every claim downstream rests on this being step-exact, so
it is checked against `tm.py` -- an independent, dumb, cell-at-a-time
simulator -- on the busy-beaver champions and on thousands of random
machines, comparing step counts, halting, and the full final tape.
"""
from tm import TM, Sim, HALT

L, R = 0, 1          # stack indices; direction -1 -> L, +1 -> R


class BlockSim:
    """A machine on the block tape.  `steps` is the exact number of base
    TM steps performed."""

    __slots__ = ("m", "st", "q", "d", "steps", "halted", "macro")

    def __init__(self, m):
        self.m = m
        self.st = ([], [])       # st[L], st[R]: blocks, nearest head LAST
        self.q = 0
        self.d = R               # the head first reads cell 0, to its right
        self.steps = 0
        self.macro = 0
        self.halted = False

    # -- stack helpers ---------------------------------------------------
    @staticmethod
    def _push(stk, sym, n):
        if n == 0:
            return
        if stk and stk[-1][0] == sym:
            stk[-1] = (sym, stk[-1][1] + n)
        else:
            stk.append((sym, n))

    def step(self):
        """One macro step.  Returns False once halted."""
        if self.halted:
            return False
        near = self.st[self.d]
        sym = near[-1][0] if near else 0
        tr = self.m.t[self.q][sym]
        if tr is None:
            self.halted = True
            return False
        w, dd, nx = tr
        dd_i = R if dd == 1 else L
        # chain step: same state, same direction -> cross the whole block
        if nx == self.q and dd_i == self.d and near:
            s, k = near.pop()
            self._push(self.st[1 - self.d], w, k)
            self.steps += k
            self.macro += 1
            return True
        # ordinary single step
        if near:
            s, k = near[-1]
            if k == 1:
                near.pop()
            else:
                near[-1] = (s, k - 1)
        self._push(self.st[1 - dd_i], w, 1)
        self.d = dd_i
        self.steps += 1
        self.macro += 1
        if nx == HALT:
            self.halted = True
            return False
        self.q = nx
        return True

    # -- observation -----------------------------------------------------
    def at_edge(self):
        """True when the head faces unwritten tape: a record event."""
        return not self.st[self.d]

    def skeleton(self):
        """Block symbols outward from the head on each side, plus state
        and facing.  Trailing zero blocks are dropped so the encoding is
        canonical."""
        out = []
        for side in (self.st[L], self.st[R]):
            b = [s for s, _ in reversed(side)]
            while b and b[-1] == 0:
                b.pop()
            out.append(tuple(b))
        return (out[0], self.q, self.d, out[1])

    def counters(self):
        """Block lengths, in the same order as `skeleton`."""
        out = []
        for side in (self.st[L], self.st[R]):
            b = list(reversed(side))
            while b and b[-1][0] == 0:
                b.pop()
            out.extend(n for _, n in b)
        return tuple(out)

    def tape_bits(self):
        """The written tape as (bits, head index) -- for cross-checking
        against the cell simulator."""
        bits = []
        for s, n in self.st[L]:
            bits.extend([s] * n)
        # st[L] is stored nearest-head-last, so it is already left-to-right
        idx = len(bits)
        right = []
        for s, n in reversed(self.st[R]):
            right.extend([s] * n)
        return bits + right, idx


def run(m, budget_steps, budget_macro=10 ** 7):
    s = BlockSim(m)
    while not s.halted and s.steps < budget_steps and s.macro < budget_macro:
        s.step()
    return s


# ---------------------------------------------------------------- checking

def cross_check(code, nsteps):
    """Run both simulators `nsteps` base steps and compare everything."""
    a = Sim(TM(code))
    b = BlockSim(TM(code))
    a.run(nsteps)
    while not b.halted and b.steps < a.steps:
        b.step()
    if b.steps != a.steps:
        # the block sim can overshoot inside a chain step; rerun the cell
        # sim to the same point so the comparison is at a common time
        a = Sim(TM(code))
        a.run(b.steps)
    if a.halted and not b.halted:
        # an undefined transition halts without consuming a step, so the
        # block sim is at the halting configuration but has not looked at
        # it yet.  One more macro step must observe the halt and must not
        # advance the clock.
        b.step()
    assert a.steps == b.steps, (code, a.steps, b.steps)
    assert a.halted == b.halted, (code, a.halted, b.halted)
    bits, idx = b.tape_bits()
    cells, lo = a.tape.span()
    # compare the written region, ignoring padding zeros at either end
    ca = list(cells)
    ha = a.p - lo
    # normalise both to (left of head, head cell, right of head).  The
    # head can sit just outside the written span, since `Tape` records a
    # cell only when something is written to it, so ha may be -1 or
    # len(ca); a raw negative slice would split the tape in the wrong
    # place and make this check vacuous.
    if ha < 0:
        la, hda, ra = [], 0, list(ca)
    elif ha >= len(ca):
        la, hda, ra = list(ca), 0, []
    else:
        la, hda, ra = ca[:ha], ca[ha], ca[ha + 1:]
    hb = idx if b.d == R else idx - 1
    if hb < 0:
        lb, hdb, rb = [], 0, list(bits)
    elif hb >= len(bits):
        lb, hdb, rb = list(bits), 0, []
    else:
        lb, hdb, rb = bits[:hb], bits[hb], bits[hb + 1:]
    la = list(la)
    lb = list(lb)
    while la and la[0] == 0:
        la.pop(0)
    while lb and lb[0] == 0:
        lb.pop(0)
    ra = list(ra)
    rb = list(rb)
    while ra and ra[-1] == 0:
        ra.pop()
    while rb and rb[-1] == 0:
        rb.pop()
    assert (la, hda, ra) == (lb, hdb, rb), \
        (code, b.steps, (la, hda, ra), (lb, hdb, rb))
    return b.steps, b.macro


def selftest():
    import random
    from tm import CHAMPS
    for code, steps, ones in CHAMPS:
        b = BlockSim(TM(code))
        while not b.halted and b.steps < steps + 10:
            b.step()
        assert b.halted and b.steps == steps, (code, b.steps, steps)
        bits, _ = b.tape_bits()
        assert sum(bits) == ones, (code, sum(bits), ones)
        print("  ok  %-40s %10d steps in %8d macro (x%.0f)"
              % (code, b.steps, b.macro, b.steps / max(b.macro, 1)))
    # step-exactness against the cell simulator on real holdouts
    codes = [ln.strip() for ln in
             open("../bbf/bb6_holdouts_1064.txt")][:60]
    for c in codes:
        cross_check(c, 200000)
    print("  ok  60 holdouts cross-checked to 200k steps, tape-identical")
    # and on random machines, where the corner cases live
    random.seed(7)
    dirs, syms = "LR", "01"
    ok = 0
    for _ in range(3000):
        g = []
        for i in range(6):
            tr = []
            for _ in range(2):
                if random.random() < 0.06:
                    tr.append("---")
                else:
                    tr.append(random.choice(syms) + random.choice(dirs) +
                              random.choice("ABCDEF"))
            g.append("".join(tr))
        code = "_".join(g)
        cross_check(code, 3000)
        ok += 1
    print("  ok  %d random 6-state machines cross-checked to 3k steps" % ok)


if __name__ == "__main__":
    print("blocktape.py selftest")
    selftest()
    print("all pass")
