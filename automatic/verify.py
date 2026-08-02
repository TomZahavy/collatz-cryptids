"""Independent verification of the WS1 search: certificates and diagnostics.

Three checks, none of which trusts the search:
  (1) CERTIFICATE CHECK -- take a structure, take the minimal (Horn) accepting
      labelling, and test the three certificate conditions by brute force over
      the integers, using needle.step1 itself (not the branch algebra).
  (2) CALIBRATION -- the search must FIND the known certificate for x -> 4x
      (I = "even number of 1 bits"), and that certificate must pass check (1).
  (3) DIAGNOSTICS -- how much of the Needle refutation comes from which
      branches, so the impossibility theorem can be stated at its true strength.
"""
import sys

from dfa_invariant import (branch_pairs, icdfas, lsb_word, needle_branch,
                           run, state_of, times4_branch)
from search import orbit, refute

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
from needle import step1, is_pow2                        # noqa: E402


def minimal_model(delta, n, branches, vmax, true_words, false_words):
    """Least accepting set satisfying the units + implications, or None."""
    false_states = {run(delta, 0, w) for w in false_words}
    imp = [set() for _ in range(n)]
    for p in range(n):
        z = delta[p][0]
        imp[p].add(z)
        imp[z].add(p)
    for v in range(vmax + 1):
        a, b = branches(v)
        for p, q in branch_pairs(delta, v, a, b):
            imp[p].add(q)
    forced = set()
    stack = [run(delta, 0, w) for w in true_words]
    while stack:
        p = stack.pop()
        if p in forced:
            continue
        forced.add(p)
        stack.extend(imp[p])
    return None if forced & false_states else forced


def check_certificate(delta, accept, step, x0, limit=200000, label=""):
    """Brute-force the three certificate conditions over x < limit."""
    def inI(x):
        return state_of(delta, x) in accept

    assert inI(x0), f"{label}: start {x0} not in I"
    for x in range(1, limit):
        if is_pow2(x):
            assert not inI(x), f"{label}: halting value {x} is in I"
        elif inI(x):
            y = step(x)
            assert inI(y), f"{label}: closure fails at x={x} -> {y}"
    return True


def main():
    # ---------------- (2) calibration: x -> 4x, certificate must exist -------
    orb4 = [6 * 4 ** i for i in range(60)]
    tw4 = [lsb_word(x) for x in orb4]
    fw = [lsb_word(1 << v) for v in range(20)]
    found = None
    for n in (2, 3):
        for delta in icdfas(n):
            if not refute(delta, n, times4_branch, 6, tw4, fw):
                acc = minimal_model(delta, n, times4_branch, 6, tw4, fw)
                if acc:
                    check_certificate(delta, acc, lambda x: 4 * x, 6,
                                      label=f"times4 n={n}")
                    found = found or (n, delta, acc)
        print(f"  calibration x->4x, n={n}: survivors give certificates that "
              f"pass brute-force verification over x < 200000: OK")
    n, delta, acc = found
    print(f"  smallest calibration certificate: {n} states, delta={delta}, "
          f"accepting={sorted(acc)}")
    print(f"    (it is I = {{x : x has an even number of 1 bits}} -- "
          f"6,24,96,... all have 2, powers of 2 have 1)")

    # ---------------- (1)+(3) the Needle: where does refutation come from ----
    orbN = orbit(6, 60)
    twN = [lsb_word(x) for x in orbN]
    print(f"\n  Needle orbit valuations (first 40): "
          f"{[(x & -x).bit_length() - 1 for x in orbN[:40]]}")

    print("\n  refutation strength by branch budget (n = number of states):")
    print("     vmax | " + " | ".join(f"n={n}" for n in range(1, 6)))
    for vmax in (0, 1, 2, 4, 6, 10):
        row = []
        for n in range(1, 6):
            fwn = [lsb_word(1 << v) for v in range(2 * n + 3)]
            alive = sum(1 for d in icdfas(n)
                        if not refute(d, n, needle_branch, vmax, twN, fwn))
            row.append(f"{alive:>5}")
        print(f"     {vmax:>4} | " + " | ".join(row))
    print("     (entries = structures still admitting a labelling; "
          "0 = impossibility proved)")

    # units-only control: how much work the orbit units do on their own
    for n in (4, 5):
        fwn = [lsb_word(1 << v) for v in range(2 * n + 3)]
        alive_units = sum(1 for d in icdfas(n)
                          if not refute(d, n, needle_branch, -1, twN, fwn))
        print(f"  control: with NO branch conditions (units + trailing-zero "
              f"invariance only), n={n}: {alive_units} structures survive")


if __name__ == "__main__":
    main()
