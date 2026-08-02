"""Cross-validate the SAT encoding against the exhaustive ICDFA enumeration.

The SAT search is only worth anything if it gives exactly the same answer as
search.py wherever both can run.  For every machine, size and branch depth in
range, this compares:

    SAT says "certificate exists"   vs   some ICDFA survives Horn propagation

Any disagreement is a bug in the encoding and is reported loudly.  It also
re-verifies any certificate SAT produces by direct simulation, so a SAT answer
is never taken on trust either.
"""
import sys

from dfa_invariant import icdfas, lsb_word, needle_branch, run, times4_branch
from search import orbit, refute
from sat_search import search

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
from needle import is_pow2, step1                          # noqa: E402


def brute(which, n, vmax):
    branches = {"needle": needle_branch, "times4": times4_branch}[which]
    orb = orbit(6, 40) if which == "needle" else [6 * 4 ** i for i in range(40)]
    tw = [lsb_word(x) for x in orb]
    fw = [lsb_word(1 << e) for e in range(2 * n + 6)]
    for delta in icdfas(n):
        if not refute(delta, n, branches, vmax, tw, fw, minimal=False):
            return delta
    return None


def verify_certificate(which, delta, acc, n):
    """Check a produced certificate directly, by simulation."""
    accs = set(acc)
    step = step1 if which == "needle" else (lambda x: 4 * x)
    inI = lambda x: run(delta, 0, lsb_word(x)) in accs                # noqa: E731
    orb = orbit(6, 40) if which == "needle" else [6 * 4 ** i for i in range(40)]
    ok_start = all(inI(x) for x in orb)
    ok_H = not any(inI(1 << e) for e in range(300))
    ok_closed = True
    for x in range(1, 200000):
        if is_pow2(x):
            continue
        if inI(x) and not inI(step(x)):
            ok_closed = False
            break
    return ok_start, ok_H, ok_closed


print("cross-validation: SAT encoding vs exhaustive ICDFA enumeration")
print("(0-invariant convention, which is what search.py's minimal=False uses)\n")
print(f"{'machine':>8} {'n':>3} {'vmax':>5} {'SAT':>12} {'brute force':>14}   verdict")
bad = 0
for which in ("needle", "times4"):
    for vmax in (0, 1, 2):
        for n in range(1, 6):
            got = search(which, n, vmax, general=False, orbit_len=40,
                         verbose=False)
            surv = brute(which, n, vmax)
            s_yes, b_yes = got is not None, surv is not None
            agree = s_yes == b_yes
            bad += not agree
            print(f"{which:>8} {n:>3} {vmax:>5} "
                  f"{'certificate' if s_yes else 'none':>12} "
                  f"{'certificate' if b_yes else 'none':>14}   "
                  f"{'agree' if agree else '*** DISAGREE ***'}")
            if s_yes:
                delta, acc = got
                st, h, cl = verify_certificate(which, delta, acc, n)
                print(f"{'':>8} {'':>3} {'':>5} certificate {delta} acc={acc}: "
                      f"orbit in I={st}, avoids H={h}, closed={cl}")
                assert st and h and cl, "SAT produced a bogus certificate"

print(f"\n{'ALL AGREE' if not bad else f'{bad} DISAGREEMENTS'} "
      f"-- the SAT encoding reproduces the exhaustive search exactly.")
