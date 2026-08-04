"""Is the extracted outer map a CRYPTID?

A cryptid, in the bbchallenge sense, is a small explicit machine whose
halting is equivalent to an open Collatz-type orbit-avoidance problem.
What makes such a problem open is not size but shape, and the shape has
three parts:

  1. PIECEWISE-AFFINE  -- finitely many affine branches selected by
     conditions, so the map is completely explicit and yet has no closed
     form for its iterates;
  2. EXPANSION         -- the map grows its argument on average, so the
     orbit never settles into a region that could be searched;
  3. DIGIT CONSUMPTION -- which branch fires depends on ever-deeper
     digits of the argument, so the branch sequence is pseudorandom and
     no bounded-state invariant tracks it.

`twolevel.py` produces exactly the object these criteria apply to: the
outer map of a two-level Turing machine, carrying one reservoir value to
the next. This file measures the three criteria on that map.

WHAT A VERDICT MEANS.  "Cryptid-shaped" is a statement about structure,
not a theorem about halting, and it is worth reporting on its own: it
says the machine's halting question has been REDUCED to a Collatz-type
orbit problem, which is where the difficulty actually lives.  That is the
same status Antihydra had before anyone proved anything about it.

Each criterion is measured against exact observations -- every step count
and counter comes from a step-exact simulator -- and each is reported
with the evidence, never as a bare verdict.
"""
import sys
from fractions import Fraction as Fr

from returnmap import outer_data
from twolevel import report as twolevel_report


def solve_exact(rows, nunk):
    """Solve an exactly-determined linear system over Q and verify it on
    every remaining row.  `rows` are (coeff_0..coeff_{nunk-1}, rhs).
    Returns the coefficient tuple, or None."""
    if len(rows) < nunk + 1:
        return None                     # no row left to falsify the fit
    work = [[Fr(x) for x in r] for r in rows]
    piv_rows = []
    used = []
    for col in range(nunk):
        piv = None
        for i, r in enumerate(work):
            if i in used:
                continue
            if r[col] != 0:
                piv = i
                break
        if piv is None:
            return None
        used.append(piv)
        pr = work[piv]
        pv = pr[col]
        pr = [x / pv for x in pr]
        work[piv] = pr
        for i, r in enumerate(work):
            if i != piv and r[col] != 0:
                f = r[col]
                work[i] = [x - f * y for x, y in zip(r, pr)]
        piv_rows.append(piv)
    co = []
    for col in range(nunk):
        co.append(work[piv_rows[col]][nunk])
    for i, r in enumerate(rows):
        if sum(c * Fr(x) for c, x in zip(co, r[:nunk])) != Fr(r[nunk]):
            return None
    return tuple(co)


def classify_map(rows, q):
    """Measure the three cryptid criteria on an outer orbit.

    `rows` are (R_n, k_n, step_n, x0_n) as produced by `returnmap`."""
    # DROP THE LAST OUTER STEP.  The simulation stops at a fixed macro
    # budget, which almost always lands in the MIDDLE of the final inner
    # loop, so that loop's length k is an undercount -- an artefact of
    # where we stopped, not a fact about the machine.  Observed directly:
    # raising the budget from 8M to 40M changed line 106's last k from 9
    # to 10, which flipped its verdict.  A criterion that depends on the
    # final delta is therefore reading the budget, not the orbit.
    rows = rows[:-1]
    if len(rows) < 5:
        return None
    Rs = [r[0] for r in rows]
    ks = [r[1] for r in rows]
    out = {"n": len(rows), "R": Rs, "k": ks}

    # (1) piecewise-affine: R_{n+1} = a*R_n + b*q^{k_n} + c, exactly
    sys_rows = [(Rs[i], q ** ks[i], 1, Rs[i + 1]) for i in range(len(Rs) - 1)]
    out["affine"] = solve_exact(sys_rows, 3)
    # a weaker reading, in case the reservoir alone drives it
    out["affine2"] = solve_exact(
        [(Rs[i], 1, Rs[i + 1]) for i in range(len(Rs) - 1)], 2)

    # (2) expansion: the orbit must grow ON AVERAGE, not at every step.
    #     Requiring every ratio to exceed 1 is wrong, and demonstrably so:
    #     it rejects Collatz, whose map halves on every even argument.
    #     Line 168 was mis-classified by exactly this -- 98.9% of its
    #     steps decrease, yet its orbit runs 28 -> 43,665 over 3,049
    #     steps.  The right test is the geometric mean.
    import math as _math
    ratios = [Fr(Rs[i + 1], Rs[i]) for i in range(len(Rs) - 1) if Rs[i]]
    out["ratios"] = [float(r) for r in ratios]
    out["min_ratio"] = float(min(ratios)) if ratios else 0.0
    if len(Rs) >= 2 and Rs[0] > 0 and Rs[-1] > 0:
        out["growth"] = _math.exp(
            (_math.log(Rs[-1]) - _math.log(Rs[0])) / (len(Rs) - 1))
    else:
        out["growth"] = 0.0
    out["expanding"] = out["growth"] > 1.0

    # (3) digit consumption: the branch index must keep changing, and
    #     must not be an eventually-affine function of the phase index --
    #     if it were, the branch sequence would be predictable and a
    #     bounded-state invariant would track it
    dk = [ks[i + 1] - ks[i] for i in range(len(ks) - 1)]
    out["k_deltas"] = dk
    out["k_constant"] = len(set(ks)) == 1
    out["k_affine"] = len(set(dk)) <= 1
    # A PERIODIC delta pattern is just as predictable as a constant one:
    # 1,2,3,1,2,3 is generated by a three-state automaton, so a bounded
    # invariant does track the branch sequence and the orbit is not
    # digit-consuming.  Testing only for constancy lets these through,
    # which is how line 990 first read as cryptid-shaped.
    out["k_period"] = None
    for p in range(1, len(dk) // 2 + 1):
        if all(dk[i] == dk[i % p] for i in range(len(dk))):
            out["k_period"] = p
            break
    out["digit_consuming"] = (not out["k_constant"] and not out["k_affine"]
                              and out["k_period"] is None)
    return out


def verdict(m):
    """Turn measurements into a label, conservatively.

    NOTE ON THE DIRECTION OF CRITERION (1).  Piecewise-affineness is not
    something to look for: the outer map of a two-level machine is affine
    on each branch by construction, since it is built from macro rules
    that are themselves affine.  What has to be TESTED is the opposite --
    whether a SINGLE affine branch explains the whole orbit.  If one
    does, the orbit has a closed form and the machine is tractable, which
    is exactly what a cryptid is not.  So a failed global affine fit is
    evidence of several branches, i.e. evidence FOR the cryptid shape.

    A verdict here is a statement about structure, never about halting,
    and it does not mean the machine is undecided: the Baker-Wustholz
    machine is cryptid-shaped and was nevertheless decided, with heavy
    machinery.  The label says where the difficulty lives."""
    if m is None:
        return "INSUFFICIENT"
    if m["affine"] is not None or m["affine2"] is not None:
        return "CLOSED-FORM"
    if not m["expanding"]:
        return "NOT-EXPANDING"
    if not m["digit_consuming"]:
        return "PREDICTABLE-BRANCHES"
    return "CRYPTID-SHAPED"


def analyse(code, blocks=(1, 2, 3, 4, 5, 6), macro_budget=1000000):
    """Find two-level sections and measure each one."""
    results = []
    for f in twolevel_report(code, blocks, macro_budget):
        q = f["recur"][0]
        if q <= 1:
            continue
        for od in outer_data(code, f["blk"], macro_budget,
                             coord=f["coord"], want=f["recur"],
                             skel=f["skel"]):
            m = classify_map(od["rows"], q)
            results.append({"code": code, "blk": f["blk"], "recur": f["recur"],
                            "skel": od["skel"], "meas": m,
                            "verdict": verdict(m), "rows": od["rows"]})
        # one section per recurrence is enough to characterise the machine
        if results:
            break
    return results


def show(code, blocks=(1, 2, 3, 4, 5, 6), macro_budget=1000000):
    rs = analyse(code, blocks, macro_budget)
    print(code)
    if not rs:
        print("  no two-level structure -> not a cryptid candidate by this route")
        return rs
    for r in rs:
        m = r["meas"]
        a, b = r["recur"]
        print("  b=%d  inner x -> %s*x + %s   VERDICT: %s"
              % (r["blk"], a, b, r["verdict"]))
        if m is None:
            print("     too few outer steps to measure")
            continue
        print("     outer steps observed: %d" % m["n"])
        print("     outer orbit R_n : %s" % (m["R"][:10],))
        print("     branch index k_n: %s   deltas %s"
              % (m["k"][:10], m["k_deltas"][:9]))
        print("     (1) single affine branch explains orbit: %s"
              " (a YES here would mean tractable, not cryptid)"
              % ("YES " + str(m["affine"]) if m["affine"] else "no"))
        print("     (2) expanding: %s   min ratio %.3f"
              % (m["expanding"], m["min_ratio"]))
        print("     (3) digit-consuming (k neither constant nor affine): %s"
              % m["digit_consuming"])
    return rs


if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else \
        "1RB1LA_1RC1RE_1LD0RB_1LA0LC_0RF0RD_0RB---"
    bud = int(sys.argv[2]) if len(sys.argv) > 2 else 1000000
    show(code, macro_budget=bud)
