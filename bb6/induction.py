"""Induction rules: the generalisation of a chain step, and the thing a
Lean proof of the inner lemma will actually be built from.

WHY.  Symbolic macro simulation (`symbolic.py`) stalls after five to
seven steps on these machines.  The reason is sharp: a chain step can
cross a block of symbolic length because it consumes the block ENTIRELY
whatever its length, but as soon as the machine consumes a symbolic block
ONE CELL AT A TIME the run branches -- for some x the block survives and
is read again, for others it vanishes and the next block is read.

The classical fix (Marxen-Buntrock; sligocki's proof system) is to look
one level up.  Very often the machine's behaviour on a long block is a
CYCLE: a fixed finite word of macro steps that returns the machine to the
same state and direction, having moved exactly one unit from one block to
another.  If such a cycle exists, then running it n times is a single
symbolic move -- and, crucially, its correctness is an INDUCTION with a
finite base case and a finite step, which is exactly what Lean can check:

    base:  the cycle runs once from the concrete configuration;
    step:  the cycle's effect on counters is a fixed vector, so if it
           applies at count k+1 it applies at count k.

WHAT THIS FILE DOES.  Detects such a cycle from concrete simulation,
states it as a rule (word, counter delta, step cost), and CONFIRMS it at
several block lengths.  A rule that survives confirmation is a candidate
lemma; proving it for all n is the Lean obligation, and the data here is
the certificate that proof would check.

A detected rule is not a theorem.  It is a precisely-stated conjecture
with its hypotheses recorded, which is the most this layer can honestly
produce.
"""
from tm import TM
from macro import MacroSim, L, R


def snapshot(s):
    return (s.skeleton(), s.counters())


def find_cycle(m, blk, st, q, d, max_macro=4000):
    """From a concrete configuration, find the shortest macro-step cycle
    that returns to the same skeleton, state and direction.

    Returns (period, counter delta, step cost, word) or None."""
    s = MacroSim(m, blk)
    s.st = ([list(t) for t in st[L]], [list(t) for t in st[R]])
    s.st = ([tuple(t) for t in s.st[L]], [tuple(t) for t in s.st[R]])
    s.st = ([list(t) for t in s.st[L]], [list(t) for t in s.st[R]])
    s.q, s.d = q, d
    sk0, ct0 = snapshot(s)
    st0 = s.steps
    word = []
    for i in range(max_macro):
        word.append((s.q, s.d, s.st[s.d][-1][0] if s.st[s.d] else 0))
        if not s.step():
            return None
        sk, ct = snapshot(s)
        if sk == sk0 and len(ct) == len(ct0):
            delta = tuple(b - a for a, b in zip(ct0, ct))
            if any(delta):
                return (i + 1, delta, s.steps - st0, list(word))
    return None


def confirm_rule(m, blk, st, q, d, idx, rule, lengths):
    """Re-run the cycle with the idx-th block set to several lengths.

    A rule worth anything is one whose word, counter delta and step cost
    do not depend on how long the block is -- that independence is
    exactly what licenses iterating it n times."""
    per, delta, cost, word = rule
    ok = 0
    for n in lengths:
        st2 = ([list(t) for t in st[L]], [list(t) for t in st[R]])
        order = []
        for side in (L, R):
            for pos in range(len(st2[side]) - 1, -1, -1):
                order.append((side, pos))
        if idx >= len(order):
            return 0
        side, pos = order[idx]
        st2[side][pos] = [st2[side][pos][0], n]
        st2 = ([tuple(t) for t in st2[L]], [tuple(t) for t in st2[R]])
        r = find_cycle(m, blk, st2, q, d)
        if r is None:
            continue
        if r[0] == per and r[1] == delta and r[2] == cost and r[3] == word:
            ok += 1
    return ok


def analyse(code, blk, skel, coord, occurrence=14, budget=2000000):
    """Advance to an occurrence of `skel`, then look for an induction
    rule governing the block at `coord`."""
    m = TM(code)
    s = MacroSim(m, blk)
    prev = True
    hits = 0
    while s.macro < budget:
        e = not s.st[s.d]
        if e and not prev and s.nblocks() <= 40 and s.skeleton() == skel:
            hits += 1
            if hits == occurrence:
                break
        prev = e
        if not s.step():
            return None
    st = ([tuple(t) for t in s.st[L]], [tuple(t) for t in s.st[R]])
    rule = find_cycle(m, blk, st, s.q, s.d)
    if rule is None:
        return {"start": s.counters(), "rule": None}
    ok = confirm_rule(m, blk, st, s.q, s.d, coord, rule,
                      [40, 61, 97, 158, 233, 401])
    return {"start": s.counters(), "rule": rule, "confirmed": ok}


THREE = [(336, "1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE"),
         (555, "1RB1RE_1LC0RA_1RD0LB_1LB1RC_1LF0RD_---0LE"),
         (1002, "1RB1LC_1RC0LD_1LA0RB_1LB1LE_1RF0LA_---0RE")]


if __name__ == "__main__":
    from twolevel import report as tlr
    for line, code in THREE:
        g = tlr(code, (2,), 2000000)[0]
        r = analyse(code, 2, g["skel"], g["coord"])
        print("line %-5d inner x -> %s*x + %s" % (line, g["recur"][0],
                                                  g["recur"][1]))
        if r is None or r["rule"] is None:
            print("    no cycle found  (start %s)"
                  % (str(r["start"])[:60] if r else "n/a"))
            continue
        per, delta, cost, word = r["rule"]
        print("    start counters %s" % (str(r["start"])[:60],))
        print("    CYCLE: %d macro steps, %d base steps, counter delta %s"
              % (per, cost, delta))
        print("    confirmed at %d/6 independent block lengths"
              % r["confirmed"])
