"""WS3 ladder: what the congruence (*) excludes, and how far it reaches.

Two unconditional consequences of  q_v^n | 3*2^{m-v} - 3 + 2v  (runs.py):

  FORBIDDEN VALUATIONS.  If the congruence is unsolvable mod q_v it is
  unsolvable mod q_v^n for every n, so a halt can never follow a step of that
  valuation -- at any scale, at any time.

  A POSITION BOUND.  For an allowed v, the halting exponent must lie in one
  residue class mod ord(2, q_v^n), so m >= t_min(v,n) + v.  Since the map
  expands by at most 3 per step, x_N <= 6*3^N and m <= 1.585 N + 2.585, hence a
  halt at the end of a v-run of length n cannot occur before step

      N_min(v, n) = (t_min(v,n) + v - 2.585) / 1.585.
"""
import math
import sys

from runs import dlog, min_exponent, qv, target

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
from needle import step1, v2, is_pow2                      # noqa: E402

VMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 34


def allowed(v):
    return min_exponent(v, 1) is not None


print("1. FORBIDDEN VALUATIONS (halting can never follow such a step)")
forb = [v for v in range(VMAX + 1) if not allowed(v)]
allow = [v for v in range(VMAX + 1) if allowed(v)]
print(f"   forbidden, v <= {VMAX}: {forb}")
print(f"   allowed,   v <= {VMAX}: {allow}")
print(f"   => {len(forb)} of {VMAX + 1} valuations are excluded outright "
      f"({100 * len(forb) / (VMAX + 1):.0f}%)")

print("\n2. POSITION BOUND for the allowed valuations, by run length n")
print("   n |" + "".join(f"  v={v:<2d}    " for v in allow[:6]))
for n in (1, 2, 3):
    row = []
    for v in allow[:6]:
        t = min_exponent(v, n)
        if t is None:
            row.append("  none   ")
        else:
            N = (t + v - 2.585) / 1.585
            row.append(f" N>={max(N, 0):8.3g}" if N > 1 else "        -")
    print(f"   {n} |" + "".join(row))
print("   ('-' = no constraint: the bound is below step 1; 'none' = the "
      "congruence is unsolvable, so that (v,n) is excluded outright)")

print("\n3. HOW MUCH OF THE ACTUAL ORBIT THIS EXCLUDES")
print("   At step N the orbit can halt only if x_N is a power of 2; the run of")
print("   valuation v and length n ending at N-1 then forces (*), so the halt is")
print("   excluded when (*) is unsolvable or when t_min(v,n) + v > 1.585 N + 2.6.")
CACHE = {}


def tmin(v, n):
    """t_min for the branch (v, n), capped at n = 3 to keep moduli small.

    Using a smaller n imposes FEWER constraints, so the resulting bound is a
    conservative under-estimate -- sound for exclusion.
    """
    n = min(n, 3)
    if (v, n) not in CACHE:
        CACHE[(v, n)] = (min_exponent(v, n) if qv(v) ** n < 10 ** 13 else
                         min_exponent(v, 1))
    return CACHE[(v, n)]


x, N = 6, 200000
runlen, prevv = 0, None
excl_forb, excl_pos, notexcl, counts = 0, 0, 0, {}
for i in range(N):
    v = v2(x)[0]
    runlen = runlen + 1 if v == prevv else 1
    prevv = v
    counts[v] = counts.get(v, 0) + 1
    t = tmin(v, runlen)
    if t is None:
        excl_forb += 1                       # a halt here is impossible, ever
    elif t + v > 1.585 * (i + 1) + 2.6:
        excl_pos += 1                        # impossible this early
    else:
        notexcl += 1
    x = step1(x)
    if is_pow2(x):
        raise SystemExit("HALTED")
print(f"   over the first {N:,} steps:")
print(f"     halt excluded because the valuation is forbidden : "
      f"{excl_forb:>7,}  ({100 * excl_forb / N:.2f}%)")
print(f"     halt excluded by the position bound              : "
      f"{excl_pos:>7,}  ({100 * excl_pos / N:.2f}%)")
print(f"     not excluded by this method                      : "
      f"{notexcl:>7,}  ({100 * notexcl / N:.2f}%)")
theory = sum(2.0 ** -(v + 1) for v in forb)
print(f"   asymptotic share of forbidden-valuation steps "
      f"(sum 2^-(v+1) over forbidden v) = {theory:.4f}")
print(f"   longest run seen per valuation: "
      f"{ {v: c for v, c in sorted(counts.items())[:8]} } (step counts)")
