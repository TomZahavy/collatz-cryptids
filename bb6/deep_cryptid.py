"""Deeper runs on the five cryptid candidates, and an attempt to pin the
outer map down in closed form.

The sweep verdicts rested on five to eight outer steps, which is enough
to notice a shape and not enough to name one.  This runs each candidate
far longer and then tries to write the outer map explicitly:

    inner loop:   x -> a*x + b, run k times, so
                  x_k = a^k * x0 + b*(a^k - 1)/(a - 1)
    outer step:   R' = alpha*R + beta*x_k + gamma

with k chosen by how far the reservoir stretches.  If a single
(alpha, beta, gamma) reproduces every observed outer step, the machine
has a closed-form return map and is TRACTABLE.  If several branches are
needed, and which branch fires depends on deep digits of R, that is the
Collatz-type orbit problem the halting question has been reduced to --
i.e. the machine is a genuine cryptid candidate and the write-up can
state the problem precisely.

Nothing here is a proof.  Every number is an exact observation of a
step-exact simulation; the question of whether the fitted relation holds
FOR ALL n is separate and open.
"""
import sys
import time
from fractions import Fraction as Fr

from cryptid import analyse, classify_map, solve_exact

FIVE = [
    (106, "1RB0LF_1LC0LD_1RD1LB_---1RE_0RA1RE_1LA0LE"),
    (336, "1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE"),
    (555, "1RB1RE_1LC0RA_1RD0LB_1LB1RC_1LF0RD_---0LE"),
    (990, "1RB0LF_1LC1RA_0RE0RD_---1LE_1LF1RC_1LC1LA"),
    (1002, "1RB1LC_1RC0LD_1LA0RB_1LB1LE_1RF0LA_---0RE"),
]


def inner_value(a, b, x0, k):
    """x after k applications of x -> a*x + b."""
    ak = Fr(a) ** k
    return ak * Fr(x0) + Fr(b) * (ak - 1) / (Fr(a) - 1)


def fit_outer(rows, a, b):
    """Try R' = alpha*R + beta*x_k + gamma over all observed outer steps."""
    if len(rows) < 5:
        return None
    sysr = []
    for i in range(len(rows) - 1):
        R, k, _, x0 = rows[i]
        xk = inner_value(a, b, x0, k)
        sysr.append((Fr(R), xk, Fr(1), Fr(rows[i + 1][0])))
    return solve_exact(sysr, 3)


def growth(Rs):
    """Geometric mean growth factor of the outer orbit."""
    if len(Rs) < 2 or Rs[0] <= 0:
        return None
    import math
    return math.exp((math.log(Rs[-1]) - math.log(Rs[0])) / (len(Rs) - 1))


def run(line, code, budget):
    t0 = time.time()
    rs = analyse(code, blocks=(1, 2, 3, 4), macro_budget=budget)
    if not rs:
        print("line %-5d %s  -> two-level structure LOST at budget %d"
              % (line, code, budget), flush=True)
        return
    r = rs[0]
    m = r["meas"]
    a, b = r["recur"]
    if m is None:
        print("line %-5d  too few outer steps at budget %d" % (line, budget),
              flush=True)
        return
    Rs = m["R"]
    co = fit_outer(r["rows"], a, b)
    g = growth(Rs)
    print("line %-5d  b=%d  inner x -> %s*x + %s   [%.0fs, budget %d]"
          % (line, r["blk"], a, b, time.time() - t0, budget), flush=True)
    print("    outer steps: %d   verdict %s" % (m["n"], r["verdict"]),
          flush=True)
    print("    R_n: %s" % (Rs[:14],), flush=True)
    print("    k_n: %s  deltas %s  period %s"
          % (m["k"][:14], m["k_deltas"][:13], m["k_period"]), flush=True)
    print("    growth per outer step: %s"
          % ("%.4f" % g if g else "n/a"), flush=True)
    print("    closed form R' = aR + b*x_k + c : %s"
          % ("YES " + str(co) if co else "no (multiple branches)"),
          flush=True)


if __name__ == "__main__":
    bud = int(sys.argv[1]) if len(sys.argv) > 1 else 4000000
    print("=== deeper runs, macro budget %d ===" % bud)
    for line, code in FIVE:
        try:
            run(line, code, bud)
        except Exception as exc:                       # noqa: BLE001
            print("line %-5d ERROR %s" % (line, exc), flush=True)
