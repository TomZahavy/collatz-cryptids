"""Independent audit of every census decision.

`decide.congruence_proof` returns a modulus m and a residue set S, and claims
the orbit is trapped in S while S misses every residue of the halting set.  The
claim rests on `branch_maps` enumerating ALL branches v, which is the one place
a bug would silently produce a false proof -- and a false proof of non-halting
is the worst output this program could emit.

So the certificate is re-checked here without reusing any of that machinery:
brute force over a range of actual integers, plus a direct check that S avoids
the powers of two.  A disagreement means the decision procedure is wrong, not
that the machine is interesting.

Run: python3 verify.py            (audits every machine the census decided)
"""
import re
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/census")

import decide                                               # noqa: E402
from family import Machine, HALT                            # noqa: E402

X0 = 3
BRUTE = 200000


def audit(mach, m, S, brute=BRUTE):
    """Returns a list of failure strings; empty means the certificate holds."""
    bad = []
    S = set(S)

    # 1. the class must contain the start
    if X0 % m not in S:
        bad.append(f"start {X0} is not in the class")

    # 2. the class must be closed under F, checked on real integers
    for x in range(2, brute):
        if x % m not in S:
            continue
        y = mach.step(x)
        if y is HALT:
            bad.append(f"x={x} is in the class and HALTS")
            break
        if y % m not in S:
            bad.append(f"x={x} in class, F(x)={y} is not (mod {m})")
            break

    # 3. the class must miss every power of two -- complete, by cycling
    seen, p = set(), 1 % m
    while p not in seen:
        seen.add(p)
        if p in S:
            bad.append(f"class contains residue {p}, taken by a power of 2")
            break
        p = p * 2 % m

    # 4. and the orbit itself must in fact stay put
    x = X0
    for _ in range(2000):
        if x % m not in S:
            bad.append("orbit left the class")
            break
        y = mach.step(x)
        if y is HALT:
            bad.append("orbit HALTED")
            break
        x = y
    return bad


def main():
    # Read the FULL table, not the log's truncated top-25 listing: an audit that
    # covers a tenth of the certificates is not an audit.
    import csv
    path = "/Users/tomzahavy/Documents/Claude/collatz/census/census_rows.tsv"
    rows = [(r["alpha"], r["beta"], r["gamma"], r["delta"], r["eps"], r["cong"])
            for r in csv.DictReader(open(path), delimiter="\t") if r["cong"]]
    if not rows:
        raise SystemExit("verify: no decided machines found in census_rows.tsv")

    print(f"AUDIT of {len(rows)} decided machines "
          f"(brute force to x < {BRUTE:,}, powers of 2 enumerated completely)\n")
    failures = 0
    for *params, m in rows:
        mach = Machine(*(int(p) for p in params))
        got = decide.congruence_proof(mach, X0, int(m))
        if got is None:
            print(f"  {str(mach):>18}  FAIL -- not reproducible")
            failures += 1
            continue
        mm, S = got
        bad = audit(mach, mm, S)
        if bad:
            failures += 1
            print(f"  {str(mach):>18}  m={mm:<3} FAIL: {bad[0]}")
    print(f"\n  machines audited: {len(rows)};  failures: {failures}")
    print("  RESULT:", "clean -- every certificate holds" if failures == 0
          else "*** A CERTIFICATE IS WRONG ***")


if __name__ == "__main__":
    main()
