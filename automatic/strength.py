"""How much of the impossibility is separation, and how much is F-closure?

Two very different reasons a structure can fail:

  SEPARATION.  The DFA cannot even tell the orbit of 6 apart from the powers of
  2 -- some orbit element and some 2^m reach the same state.  Nothing dynamical:
  a statement about the digit complexity of the orbit at small automaton sizes.

  CLOSURE.  The DFA does separate them, but F(I) subset of I then drags a power
  of 2 into I.  This is the dynamical content, and it is what the WS1 claim is
  really about.

This script reports both columns, and profiles the refutation witnesses on the
separating structures only -- the ones where closure is the binding constraint.
"""
import sys

from dfa_invariant import icdfas, lsb_word, state_of
from search import orbit, refute
from witness import audit, find_witness

from dfa_invariant import needle_branch                   # noqa: E402


def main():
    orb = orbit(6, 60)
    tw = [lsb_word(x) for x in orb]
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    vmax = int(sys.argv[2]) if len(sys.argv) > 2 else 6

    print("  n | structures | separate orbit from H | also survive closure | "
          "closure kills")
    for n in range(1, nmax + 1):
        fw = [lsb_word(1 << v) for v in range(2 * n + 3)]
        pows = [1 << v for v in range(2 * n + 3)]
        sep, tot, alive = [], 0, 0
        for delta in icdfas(n):
            tot += 1
            bad = {state_of(delta, p) for p in pows}
            if any(state_of(delta, x) in bad for x in orb):
                continue                       # cannot separate
            sep.append([r[:] for r in delta])
            if not refute(delta, n, needle_branch, vmax, tw, fw):
                alive += 1
        print(f" {n:2d} | {tot:>10,} | {len(sep):>21,} | {alive:>20} | "
              f"{len(sep) - alive:>13,}")

        if sep:                                # profile witnesses on those
            lens = []
            for delta in sep[:400]:
                w = find_witness(delta, n)
                assert w is not None and w["kind"] == "forced-power"
                assert audit(delta, w)
                lens.append(len(w["chain"]))
            hist = {}
            for L in lens:
                hist[L] = hist.get(L, 0) + 1
            print(f"      witness chain lengths on separating structures "
                  f"(n={n}, {len(lens)} audited): {dict(sorted(hist.items()))}")


if __name__ == "__main__":
    main()
