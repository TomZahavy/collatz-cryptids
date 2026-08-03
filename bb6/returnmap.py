"""From a two-level Turing machine to an integer map.

WHY THIS IS THE POINT OF THE WHOLE PORT.  Our Collatz-side toolkit --
halting criteria, forbidden-valuation sieves, density estimates, the
cryptid framing -- all operate on ONE object: an integer map D |-> F(D)
whose orbit from a fixed start we are asked to control.  `twolevel.py`
showed that the interesting BB(6) machines have an inner rigid loop
wrapped in an outer map; this file extracts that outer map as data, so
the machine stops being a tape and becomes an arithmetic problem.

THE SECTION.  Take the skeleton that carries the inner recurrence and
keep only the visits at which the driving counter is at its RESET value
-- the first term of an inner run.  Those are the outer phase
boundaries.  Between two of them the machine runs the inner loop k times,
where k is however many times the recurrence fits inside the reservoir.
Recording (reservoir before, k, reservoir after) for many outer steps is
what turns "some structure" into a candidate closed form.

WHAT IS PROVED HERE: nothing.  This is measurement, and the numbers it
prints are exact observations of the machine (every step count is
step-exact, see `macro.py`).  Whether the observed relation is the map
FOR ALL n is the proof obligation, and it is separate.
"""
import sys
from fractions import Fraction as Fr

from rigid import scan
from twolevel import split_runs, MINRUN


def outer_data(code, blk, macro_budget, coord=None, want=(Fr(3), Fr(4)),
               skel=None):
    """Collect (reservoir_before, k, reservoir_after) for the outer map.

    Returns a list of findings, one per (skeleton, driving coordinate)
    that exhibits the target recurrence in at least three inner runs."""
    status, events, steps = scan(code, blk, macro_budget)
    buckets = {}
    for st, sk, ct in events:
        buckets.setdefault(sk, []).append((st, ct))
    out = []
    for sk, occ in buckets.items():
        if len(occ) < 3 * MINRUN:
            continue
        if skel is not None and sk != skel:
            continue
        ncoord = len(occ[0][1])
        # a coordinate index is only meaningful for the skeleton it came
        # from; other skeletons have other widths
        for j in (range(ncoord) if coord is None
                  else ([coord] if coord < ncoord else [])):
            vals = [c[j] for _, c in occ]
            runs = [r for r in split_runs(vals)
                    if r[2] == want and r[1] >= MINRUN]
            if len(runs) < 3:
                continue
            # the reservoir is the coordinate that DECREASES across an
            # inner run -- the one being spent to drive the recurrence
            res = None
            i0, ln0, _ = runs[0]
            for c2 in range(ncoord):
                if c2 == j:
                    continue
                a = occ[i0][1][c2]
                b = occ[i0 + ln0 - 1][1][c2]
                if b < a:
                    res = c2
                    break
            if res is None:
                continue
            rows = []
            for (i, ln, _) in runs:
                rows.append((occ[i][1][res], ln, occ[i][0],
                             occ[i][1][j]))
            out.append({"skel": sk, "blk": blk, "coord": j, "res": res,
                        "rows": rows, "nruns": len(runs),
                        "status": status, "steps": steps})
    out.sort(key=lambda f: -f["nruns"])
    return out


def show(code, blk, macro_budget):
    fs = outer_data(code, blk, macro_budget)
    if not fs:
        print("no two-level section found at b=%d" % blk)
        return
    for f in fs[:2]:
        print("skeleton %s   driving coord %d, reservoir coord %d, %d runs"
              % (f["skel"], f["coord"], f["res"], f["nruns"]))
        print("   %14s %5s %8s %16s" % ("reservoir R_n", "k_n", "x_start",
                                        "step"))
        prev = None
        for R, k, st, x0 in f["rows"]:
            ratio = ("%.4f" % (float(R) / float(prev))) if prev else "-"
            print("   %14d %5d %8d %16d   R/Rprev=%s" % (R, k, x0, st, ratio))
            prev = R
        print()


if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else \
        "1RB1LA_1RC1RE_1LD0RB_1LA0LC_0RF0RD_0RB---"
    blk = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    bud = int(sys.argv[3]) if len(sys.argv) > 3 else 2000000
    print("=== %s  b=%d  macro budget %d ===" % (code, blk, bud))
    show(code, blk, bud)
