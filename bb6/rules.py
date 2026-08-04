"""Derive the counter rule set for a two-level machine.

For each machine: find the configuration shape the inner loop turns in,
read off the turn rule and its cost, then check the two things that make
the rule set a SYSTEM rather than a list of observations --

  * the branch condition: how many turns the loop takes before a counter
    is exhausted, predicted as the minimum of the shrinking counters;
  * the cascade rule: how the counters map from one loop to the next.

Every claim is checked against the machine over the whole observed run,
and the counts are reported, because a rule that holds on six instances
and fails on the seventh has been the recurring hazard here.
"""
import sys
from tm import TM
from macro import MacroSim
from twolevel import report as tlr

MACHINES = [
    (106, "1RB0LF_1LC0LD_1RD1LB_---1RE_0RA1RE_1LA0LE"),
    (336, "1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE"),
    (555, "1RB1RE_1LC0RA_1RD0LB_1LB1RC_1LF0RD_---0LE"),
    (990, "1RB0LF_1LC1RA_0RE0RD_---1LE_1LF1RC_1LC1LA"),
    (1002, "1RB1LC_1RC0LD_1LA0RB_1LB1LE_1RF0LA_---0RE"),
]


def observations(code, blk, skel, budget, skip=8):
    """Counter vectors each time the machine is at the given shape."""
    g = tlr(code, (blk,), 1000000)[0]
    s = MacroSim(TM(code), blk)
    prev, hits = True, 0
    while s.macro < 1000000:
        e = not s.st[s.d]
        if e and not prev and s.nblocks() <= 40 and s.skeleton() == g["skel"]:
            hits += 1
            if hits == skip:
                break
        prev = e
        if not s.step():
            return []
    out, steps = [], []
    for _ in range(budget):
        if s.skeleton() == skel:
            out.append((s.counters(), s.steps))
        if not s.step():
            break
    return out


def find_shape(code, blk, budget=400000, skip=8):
    """The shape that recurs most, among those with a small counter
    vector -- that is where the inner loop turns."""
    g = tlr(code, (blk,), 1000000)[0]
    s = MacroSim(TM(code), blk)
    prev, hits = True, 0
    while s.macro < 1000000:
        e = not s.st[s.d]
        if e and not prev and s.nblocks() <= 40 and s.skeleton() == g["skel"]:
            hits += 1
            if hits == skip:
                break
        prev = e
        if not s.step():
            return None
    cnt = {}
    for _ in range(budget):
        sk = s.skeleton()
        if 3 <= len(s.counters()) <= 5:
            cnt[sk] = cnt.get(sk, 0) + 1
        if not s.step():
            break
    if not cnt:
        return None
    return max(cnt, key=lambda k: cnt[k])


def analyse(line, code, blk, budget=3000000):
    skel = find_shape(code, blk)
    if skel is None:
        return None
    obs = observations(code, blk, skel, budget)
    if len(obs) < 40:
        return None
    seq = [c for c, _ in obs]
    n = len(seq[0])
    # the turn rule: the delta seen between the first two observations
    delta = tuple(b - a for a, b in zip(seq[0], seq[1]))
    runs, i = [], 0
    while i < len(seq):
        j = i
        while j + 1 < len(seq) and \
                tuple(b - a for a, b in zip(seq[j], seq[j + 1])) == delta:
            j += 1
        runs.append((seq[i], j - i + 1))
        i = j + 1
    # the shrinking coordinates are the ones the turn decreases
    shrink = [t for t in range(n) if delta[t] < 0]
    ok = sum(1 for c, k in runs
             if shrink and k == min(c[t] // (-delta[t]) for t in shrink))
    return {"skel": skel, "delta": delta, "shrink": shrink,
            "runs": len(runs), "branch_ok": ok,
            "cost": obs[1][1] - obs[0][1], "first": runs[:4]}


if __name__ == "__main__":
    blk = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    for line, code in MACHINES:
        r = analyse(line, code, blk)
        if r is None:
            print("line %-5d no usable shape at b=%d" % (line, blk))
            continue
        print("line %-5d shape %s" % (line, r["skel"]))
        print("    turn: counters += %s   cost of first turn %d"
              % (str(r["delta"]), r["cost"]))
        print("    branch k = min over shrinking coords %s : %d/%d runs"
              % (r["shrink"], r["branch_ok"], r["runs"]))
        print("    first run starts: %s" % (str(r["first"])[:100],))
