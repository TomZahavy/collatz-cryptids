"""Two-level structure: the shape BB(6) machines actually have.

WHAT THE POSITIVE CONTROL TAUGHT US.  The April 2026 BB(6) machine
`1RB1LA_1RC1RE_1LD0RB_1LA0LC_0RF0RD_0RB---` was decided by mxdys with a
closed-form orbit plus a Baker-Wustholz argument, so it was the obvious
test for a rigidity detector.  It fails the test -- and the reason is the
interesting part.  Sampling its configurations at one skeleton gives

    (4, 11, 2) (4, 37, 2) (16, 26, 2) (4, 136, 2) (16, 125, 2)
    (52, 90, 2) (4, 969, 2) (16, 958, 2) (52, 923, 2) (160, 816, 2) ...

The first counter runs 4, 16, 52, 160, 484, 1456, 4372 -- exactly
x -> 3x + 4 -- while the second is drained to pay for it.  When the
reservoir runs out the first counter RESETS to 4 and the whole thing
starts again against a bigger reservoir.

So the machine has TWO levels: an inner loop that is perfectly rigid
(a geometric recurrence), and an outer map that decides how long each
inner loop is allowed to run.  Our FRACTRAN certificate class describes
one level, which is why it decided nine FRACTRAN holdouts with linear
margins and says nothing here.  And it explains the Baker-Wustholz: the
outer step depends on how many times 3x + 4 fits inside the reservoir,
i.e. on how close a power of 3 lands to a given number -- a linear form
in logarithms.

WHAT THIS FILE DOES.  Split a skeleton's occurrence list into maximal
INNER RUNS, each following one fixed recurrence x -> a*x + b, and expose
the OUTER MAP that carries one run's starting counters to the next.
That outer map is the object our Collatz-side toolkit already knows how
to attack: a piecewise map on integers, to be tested for a halting
criterion, a sieve, a density.

The inner recurrence is fitted, not assumed, and the fit is exact over
the rationals; a run is only accepted when the recurrence reproduces
every one of its terms.  As everywhere in this pipeline, the output is a
conjecture about the machine, and the proof obligation is separate.
"""
from fractions import Fraction as Fr

from rigid import scan, MINPH

MINRUN = 3         # terms needed before a recurrence counts as a run
MINRUNS = 3        # inner runs needed before we believe an outer map


def fit_recur(vals):
    """Fit x_{n+1} = a*x_n + b exactly.  Returns (a, b) or None."""
    if len(vals) < 3:
        return None
    x0, x1, x2 = Fr(vals[0]), Fr(vals[1]), Fr(vals[2])
    if x1 == x0:
        if x2 != x1:
            return None
        return (Fr(1), Fr(0))
    a = (x2 - x1) / (x1 - x0)
    b = x1 - a * x0
    for i in range(len(vals) - 1):
        if a * Fr(vals[i]) + b != Fr(vals[i + 1]):
            return None
    return (a, b)


def split_runs(vals):
    """Cut a series into maximal stretches obeying one recurrence.

    Greedy and left-to-right: extend the current run while the fitted
    recurrence keeps predicting, then start a new one.  Returns a list of
    (start index, length, (a, b))."""
    runs = []
    i = 0
    n = len(vals)
    while i + MINRUN <= n:
        r = fit_recur(vals[i:i + MINRUN])
        if r is None:
            i += 1
            continue
        # the recurrence is pinned by the first three terms, so extend it
        # one term at a time instead of re-fitting the whole prefix --
        # re-fitting makes this cubic and it does not terminate on the
        # skeletons that matter
        a, b = r
        j = i + MINRUN
        while j < n and a * Fr(vals[j - 1]) + b == Fr(vals[j]):
            j += 1
        runs.append((i, j - i, r))
        i = j
    return runs


def analyse_two_level(code, blk, macro_budget=200000):
    """Look for a skeleton whose counters split into inner geometric runs.

    Returns a list of findings, best first.  A finding records the
    skeleton, which counter drives the inner recurrence, the recurrence
    itself, and the outer sequence -- the counters at the start of each
    inner run, which is the return map's orbit."""
    status, events, steps = scan(code, blk, macro_budget)
    if status in ("halt", "infinite"):
        return []
    buckets = {}
    for st, sk, ct in events:
        buckets.setdefault(sk, []).append((st, ct))
    found = []
    for sk, occ in buckets.items():
        if len(occ) < MINPH:
            continue
        ncoord = len(occ[0][1])
        for j in range(ncoord):
            vals = [c[j] for _, c in occ]
            runs = split_runs(vals)
            geo = [r for r in runs if r[2][0] > 1 and r[1] >= MINRUN]
            if len(geo) < MINRUNS:
                continue
            # the recurrence must be the SAME in every inner run, or it
            # is not one structure repeating but several coincidences
            rec = geo[0][2]
            if any(g[2] != rec for g in geo):
                continue
            outer = [occ[g[0]][1] for g in geo]
            found.append({
                "skel": sk, "blk": blk, "coord": j, "recur": rec,
                "nruns": len(geo), "runlens": [g[1] for g in geo],
                "outer": outer,
                "outer_steps": [occ[g[0]][0] for g in geo],
                "nocc": len(occ),
            })
    found.sort(key=lambda f: (-f["nruns"], -sum(f["runlens"])))
    return found


def report(code, blocks=(1, 2, 3, 4, 5, 6), macro_budget=200000):
    out = []
    for b in blocks:
        out.extend(analyse_two_level(code, b, macro_budget))
    out.sort(key=lambda f: (-f["nruns"], -sum(f["runlens"])))
    return out


def show(code, blocks=(1, 2, 3, 4, 5, 6), macro_budget=200000, top=3):
    fs = report(code, blocks, macro_budget)
    print(code)
    if not fs:
        print("  no two-level structure found")
        return fs
    for f in fs[:top]:
        a, b = f["recur"]
        print("  b=%d coord %d   x -> %s*x + %s   %d inner runs, lengths %s"
              % (f["blk"], f["coord"], a, b, f["nruns"],
                 f["runlens"][:10]))
        print("     skeleton %s" % (f["skel"],))
        print("     outer orbit (counters at each run start):")
        for c in f["outer"][:8]:
            print("        %s" % (str(c)[:78],))
    return fs


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        show(sys.argv[1])
    else:
        print("=== positive control: the Baker-Wustholz machine ===")
        fs = show("1RB1LA_1RC1RE_1LD0RB_1LA0LC_0RF0RD_0RB---")
        assert fs, "two-level detector fails its positive control"
        assert any(f["recur"] == (Fr(3), Fr(4)) for f in fs), \
            "expected the inner recurrence x -> 3x + 4"
        print("\n  ok  inner recurrence x -> 3x + 4 recovered")
