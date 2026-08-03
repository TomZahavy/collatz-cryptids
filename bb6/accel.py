"""Rule-based acceleration: apply the induction rule at run time.

THE POINT.  The three cryptid candidates stalled at ten to twelve outer
steps, because the outer orbit grows by a factor of ~3 and the work per
step grows with it.  But `induction.py` showed the inner loop is a fixed
five-macro-step unit with a constant counter delta and an affine cost.
A simulator that RECOGNISES that unit does not have to walk it: it can
compute how many times the unit fits before a guard fails and jump the
whole way in one move.

That is what this file does, and it does two jobs at once:

  * it breaks the cost wall, so the outer orbits can be extended far
    enough to test the cryptid criteria seriously;
  * the jump it performs IS the closed form -- the composition of
    prologue, n units and epilogue that obligation 4 asks for.

DETECTION, AT RUN TIME AND WITHOUT ASSUMING ANYTHING.  At each macro
step, look ahead for a return to the same skeleton, state and direction
within a short window.  If the counters move by a fixed vector on two
consecutive repetitions, and the per-repetition cost is the same or grows
by a constant, treat it as a rule and jump.  n is chosen as the largest
number of repetitions keeping every counter that the delta decreases at
or above 1 -- one short of any guard failing, so the jump never crosses a
branch.

SOUNDNESS IS NOT ASSUMED.  A jump is a claim that n repetitions behave
like the two that were observed. `verify` below re-runs the unaccelerated
simulator and demands identical configurations and identical base-step
counts, which is the only reason to believe any number this file
produces.
"""
from tm import TM
from macro import MacroSim, L, R

MAXP = 12          # longest unit (in macro steps) we look for
MINJUMP = 4        # never bother jumping fewer repetitions than this


def _snap(s):
    return (s.skeleton(), s.q, s.d, s.counters())


class AccelSim:
    """A `MacroSim` that recognises and jumps induction rules."""

    def __init__(self, m, blk):
        self.s = MacroSim(m, blk)
        self.jumps = 0
        self.jumped_units = 0

    # -- pass-through -----------------------------------------------------
    @property
    def steps(self):
        return self.s.steps

    @property
    def macro(self):
        return self.s.macro

    @property
    def halted(self):
        return self.s.halted or self.s.infinite

    def _clone(self):
        c = MacroSim(self.s.m, self.s.b)
        c.st = ([list(t) for t in self.s.st[L]],
                [list(t) for t in self.s.st[R]])
        c.q, c.d, c.steps, c.macro = self.s.q, self.s.d, self.s.steps, \
            self.s.macro
        c.tbl = self.s.tbl
        return c

    def _find_rule(self):
        """Look ahead for a unit that repeats twice with a fixed delta."""
        base = _snap(self.s)
        probe = self._clone()
        marks = []
        for i in range(1, 3 * MAXP + 1):
            if not probe.step():
                return None
            sn = _snap(probe)
            if sn[0] == base[0] and sn[1] == base[1] and sn[2] == base[2] \
                    and len(sn[3]) == len(base[3]):
                marks.append((i, sn[3], probe.steps))
                if len(marks) >= 2:
                    break
        if len(marks) < 2:
            return None
        (i1, c1, s1), (i2, c2, s2) = marks[0], marks[1]
        if i2 != 2 * i1:
            return None
        d1 = tuple(b - a for a, b in zip(base[3], c1))
        d2 = tuple(b - a for a, b in zip(c1, c2))
        if d1 != d2 or not any(d1):
            return None
        cost1 = s1 - self.s.steps
        cost2 = s2 - s1
        return (i1, d1, cost1, cost2 - cost1)

    def _max_reps(self, delta):
        """Largest n keeping every decreasing counter >= 1."""
        ct = self.s.counters()
        best = None
        for c, d in zip(ct, delta):
            if d < 0:
                n = (c - 1) // (-d)
                best = n if best is None else min(best, n)
        return best

    def step(self):
        r = self._find_rule()
        if r is not None:
            per, delta, cost1, dcost = r
            n = self._max_reps(delta)
            if n is not None and n >= MINJUMP:
                # counters move by n*delta; cost is cost1 per unit plus a
                # constant increment per unit, so the total is quadratic
                tot = n * cost1 + dcost * (n * (n - 1) // 2)
                self._apply(delta, n, tot, per)
                self.jumps += 1
                self.jumped_units += n
                return True
        return self.s.step()

    def _apply(self, delta, n, tot, per):
        s = self.s
        order = []
        for side in (L, R):
            blocks = list(reversed(s.st[side]))
            w = list(blocks)
            while w and w[-1][0] == 0:
                w.pop()
            for j in range(len(w)):
                order.append((side, len(s.st[side]) - 1 - j))
        for k, (side, pos) in enumerate(order):
            if k < len(delta) and delta[k]:
                sym, cnt = s.st[side][pos]
                s.st[side][pos] = (sym, cnt + delta[k] * n)
        s.st = ([list(t) for t in s.st[L]], [list(t) for t in s.st[R]])
        s.st = ([tuple(t) for t in s.st[L]], [tuple(t) for t in s.st[R]])
        s.st = ([list(t) for t in s.st[L]], [list(t) for t in s.st[R]])
        s.steps += tot
        s.macro += n * per

    def skeleton(self):
        return self.s.skeleton()

    def counters(self):
        return self.s.counters()

    def nblocks(self):
        return self.s.nblocks()


def verify(code, blk, nsteps):
    """Accelerated vs unaccelerated: same configuration, same clock.

    Runs the accelerated simulator until it passes `nsteps` base steps,
    then runs the ordinary one to exactly the same base-step count and
    demands the configurations agree."""
    m = TM(code)
    a = AccelSim(m, blk)
    while not a.halted and a.steps < nsteps:
        if not a.step():
            break
    b = MacroSim(m, blk)
    while not (b.halted or b.infinite) and b.steps < a.steps:
        b.step()
    assert b.steps == a.steps, (code, blk, b.steps, a.steps)
    assert b.skeleton() == a.skeleton(), (code, blk, b.skeleton(),
                                          a.skeleton())
    assert b.counters() == a.counters(), (code, blk, b.counters(),
                                          a.counters())
    return a.steps, a.macro, b.macro, a.jumps, a.jumped_units


THREE = [(336, "1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE"),
         (555, "1RB1RE_1LC0RA_1RD0LB_1LB1RC_1LF0RD_---0LE"),
         (1002, "1RB1LC_1RC0LD_1LA0RB_1LB1LE_1RF0LA_---0RE")]

if __name__ == "__main__":
    print("accel.py selftest -- accelerated vs unaccelerated")
    for line, code in THREE:
        for nst in (200000, 2000000):
            st, am, bm, j, u = verify(code, 2, nst)
            print("  ok  line %-5d steps=%-12d macro %d vs %d  (%d jumps, "
                  "%d units skipped, x%.0f)"
                  % (line, st, am, bm, j, u, bm / max(am, 1)))
    print("all pass")
