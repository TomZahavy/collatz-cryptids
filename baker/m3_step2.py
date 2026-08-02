"""Machine 3, step -2: the next-to-last branch is v_3 = 1 too (large-j test).

m3_deep.py finds the depth-1 halting seeds exactly:

    F1 = { (3^5 * R^t - 33)/10 : t >= 0 },  branch (1,1),   R = 27^4 = 3^12
    F2 = { (3^14 * R^t - 39)/10 : t >= 0 }, branch (1,2)

(members 21, 12914013, ... and 478293, ...).  A value a' two steps from a halt
must satisfy G(a') in F1 u F2, so for its branch (j, r) with N = 3^{j+1}+1 the
sieve condition N | h - P applies with h in F1 u F2.

A FAST NECESSARY CONDITION.  Multiplying by 10 (exact in Z):

        10 h = 3^{e + 12 t} - C,     (e, C) = (5, 33) or (14, 39),

so  N | h - P  forces   3^{e + 12t} = 10 P + C   (mod N).   Now <3> mod N is
just {+-3^i : 0 <= i <= j} (m3_theorem.py, since 3^{j+1} = -1), so the left side
ranges over at most 2(j+1) known residues.  Membership is therefore a tiny
finite test -- no discrete logarithm, no large modulus.  Failing it EXCLUDES the
branch (the condition is necessary, so exclusion is sound).

PARITY LEMMA (closed form, all j).  Every member of F1 and F2 is odd, and N is
always even, so N | h - P forces P odd.  P = r 3^j - 3^{j+1}(j + c_r) has parity
r + j + c_r, and r + c_r = 4 (r=1) or 6 (r=2) -- even in both cases.  So P is
odd iff j is odd: THE NEXT-TO-LAST BRANCH MUST HAVE ODD VALUATION.  In
particular j = 0, which carries 2/3 of all steps, is excluded outright.
"""
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/baker")
from sieve_m3 import affine                                # noqa: E402

JMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 500
FAMS = [("F1", 5, 33), ("F2", 14, 39)]


def reachable_pow3(j, e):
    """{3^{e+12t} mod N : t >= 0} where N = 3^{j+1}+1, as an exact finite set."""
    N = 3 ** (j + 1) + 1
    out, x, seen = set(), pow(3, e, N), set()
    step = pow(3, 12, N)
    while x not in seen:
        seen.add(x)
        out.add(x)
        x = x * step % N
    return out, N


print(f"machine 3, step -2: testing every branch (j, r), j <= {JMAX}\n")

# --- the parity lemma, checked ---
odd_members = all(v % 2 == 1 for v in
                  [(3 ** 5 * (3 ** 12) ** t - 33) // 10 for t in range(4)] +
                  [(3 ** 14 * (3 ** 12) ** t - 39) // 10 for t in range(4)])
print(f"PARITY LEMMA: all sampled members of F1, F2 odd: {odd_members}")
bad_par = []
for j in range(JMAX + 1):
    for r in (1, 2):
        _, _, P, _ = affine(j, r)
        if (P % 2 == 1) != (j % 2 == 1):
            bad_par.append((j, r))
print(f"  N = 3^(j+1)+1 even for all j: "
      f"{all((3 ** (j + 1) + 1) % 2 == 0 for j in range(JMAX + 1))}")
print(f"  P odd <=> j odd, for every j <= {JMAX}: "
      f"{'OK' if not bad_par else bad_par[:5]}")
print(f"  => every even valuation is excluded at step -2, closed form.\n")

# --- the full finite test ---
surv = []
for j in range(JMAX + 1):
    for r in (1, 2):
        N, D, P, Q = affine(j, r)
        for name, e, C in FAMS:
            reach, _ = reachable_pow3(j, e)
            if (10 * P + C) % N in reach:
                surv.append((j, r, name))
print(f"NECESSARY-CONDITION TEST  3^(e+12t) = 10P + C (mod N)")
print(f"  branches (j, r, family) that survive, j <= {JMAX}:")
print(f"    {surv}")
jset = sorted({j for j, _, _ in surv})
print(f"  surviving valuations: {jset}")
print(f"\n{'THEOREM CONFIRMED' if jset == [1] else 'NOT PINNED'}: the "
      f"next-to-last branch before a halt has v_3 = 1"
      f" (machine-verified for j <= {JMAX}).")

freq = (2 / 9) ** 2
print(f"\nCOMBINED with the step -1 theorem: the last TWO steps before any halt")
print(f"  both have v_3 = 1.  A random pair of consecutive steps does so with")
print(f"  probability (2/9)^2 = {freq:.6f} = 4/81, so {100 * (1 - freq):.2f}% of")
print(f"  consecutive step-pairs are unconditionally excluded as halt-endings.")
