"""WS1 search: is there a small 2-automatic non-halting certificate?

For every canonical initially-connected DFA transition structure with n states
(each isomorphism class once), decide -- exactly, by Horn propagation -- whether
ANY acceptance labelling turns it into a certificate

    x0 in I,   F(I \\ H) subset of I,   I cap H = empty

using the branch conditions v_2(x) = v for v <= vmax.  Because those conditions
are a subset of the full closure requirement, "no structure of size <= n
survives" is a genuine impossibility theorem; survivors are candidates that
still owe the branches v > vmax.

Usage:  python3 search.py [needle|times4] [nmax] [vmax]
"""
import sys
import time

from dfa_invariant import (branch_pairs, branch_pairs_min, icdfas,
                           lsb_word, needle_branch, run, times4_branch)

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
from needle import step1, is_pow2                        # noqa: E402


def orbit(x0, n):
    out, x = [x0], x0
    for _ in range(n - 1):
        x = step1(x)
        assert x != "HALT", "orbit halted"
        out.append(x)
    return out


def refute(delta, n, branches, vmax, true_words, false_words, minimal=True):
    """True iff NO acceptance labelling works (structure refuted).

    minimal=True is the general convention: I is decided on minimal LSB words,
    which is what "2-automatic" means without any normalisation.  minimal=False
    is the restricted convention in which the DFA must also be trailing-zero
    invariant; it is a special case, so refuting the general one is stronger.

    Incremental: branches are added one valuation at a time and propagation is
    interleaved, so most structures die on the v = 0 branch alone.
    """
    false_states = {run(delta, 0, w) for w in false_words}
    forced, stack = set(), []

    def push(s):
        """Force acc(s) = TRUE; returns True if that contradicts H-exclusion."""
        if s in forced:
            return False
        if s in false_states:
            return True
        forced.add(s)
        stack.append(s)
        return False

    for w in true_words:                       # units: the orbit prefix
        if push(run(delta, 0, w)):
            return True

    imp = [set() for _ in range(n)]
    if not minimal:                            # acc(p) <=> acc(delta(p,0))
        for p in range(n):
            z = delta[p][0]
            imp[p].add(z)
            imp[z].add(p)

    pairs_of = branch_pairs_min if minimal else branch_pairs
    for v in range(vmax + 1):
        a, b = branches(v)
        for p, q in pairs_of(delta, v, a, b):
            imp[p].add(q)
            if p in forced and push(q):
                return True
        while stack:                           # propagate with early exit
            p = stack.pop()
            for q in imp[p]:
                if push(q):
                    return True
    return False


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "needle"
    nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    vmax = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    branches = {"needle": needle_branch, "times4": times4_branch}[which]

    if which == "needle":
        orb = orbit(6, 60)
    else:
        orb = [6 * 4 ** i for i in range(60)]
    true_words = [lsb_word(x) for x in orb]
    print(f"machine={which}  start={orb[0]}  orbit prefix: {orb[:6]} ...  "
          f"(60 elements, {orb[-1].bit_length()} bits at the end)")
    print(f"branch conditions imposed: v = 0..{vmax}   "
          f"(a_v, b_v) = {[branches(v) for v in range(min(vmax + 1, 5))]} ...")

    nmin = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    for n in range(nmin, nmax + 1):
        false_words = [lsb_word(1 << v) for v in range(2 * n + 3)]
        t0, tried, alive = time.time(), 0, []
        for delta in icdfas(n):
            tried += 1
            if not refute(delta, n, branches, vmax, true_words, false_words):
                alive.append([r[:] for r in delta])
        dt = time.time() - t0
        tag = "REFUTED (no certificate)" if not alive else \
              f"{len(alive)} SURVIVOR(S)"
        print(f"n={n:2d}  structures={tried:>9,}  {tag:<26} {dt:6.1f}s")
        for d in alive[:5]:
            print(f"        survivor delta={d}")
        if alive and which == "needle":
            print("        -> verify these on branches v > vmax before claiming")


if __name__ == "__main__":
    main()
