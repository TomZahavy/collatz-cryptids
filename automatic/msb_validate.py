"""Cross-validation for msb_search.py.  Run this before trusting any result.

Two bugs in the LSB encoding were caught only this way and both produced fake
results (one spurious SAT, one spurious UNSAT), so the MSB encoding gets the
same treatment:

  1. the elimination identity (*) itself, against needle.step1;
  2. the product's emitted pairs against the TRUE pairs (state(x), state(F(x)))
     for explicit DFAs -- the check that would catch either a missing successor
     (too weak a constraint, spurious SAT) or an invented one (too strong,
     spurious UNSAT);
  3. the SAT verdict against brute-force enumeration of all small DFAs;
  4. calibration: a machine with a known certificate must yield one.
"""
import itertools
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
from needle import step1, is_pow2, v2                       # noqa: E402

from dfa_invariant import needle_branch                     # noqa: E402
from msb_search import msb_word, const_and_bound, MsbEncoder, search  # noqa: E402


def run(delta, x):
    s = 0
    for d in msb_word(x):
        s = delta[s][d]
    return s


# ---------------------------------------------------------- 1. identity ----
def check_identity(vmax=6, hi=200000):
    n = 0
    for x in range(3, hi):
        if is_pow2(x):
            continue
        v = v2(x)[0]
        if v > vmax:
            continue
        a, b = needle_branch(v)
        C, _ = const_and_bound(v, a, b)
        assert (1 << (v + 1)) * step1(x) - a * x == C, (x, v)
        n += 1
    print(f"1. identity 2^(v+1) F(x) - a_v x = C_v : OK on {n:,} values "
          f"(v <= {vmax}, x < {hi:,})")


# ------------------------------------------------- 2. product vs truth -----
def product_pairs(delta, v, a, b):
    """Pairs the abstract product emits, for an EXPLICIT delta."""
    C, M = const_and_bound(v, a, b)
    mask = (1 << (v + 1)) - 1
    start = (0, 0, 0, 0)
    seen, stack, out = {start}, [start], set()
    while stack:
        px, py, r, sh = stack.pop()
        if r == C and sh == (1 << v):
            out.add((px, py))
        for d in (0, 1):
            for e in (0, 1):
                r2 = 2 * r + (1 << (v + 1)) * e - a * d
                if abs(r2) > M:
                    continue
                nxt = (delta[px][d], delta[py][e], r2, ((sh << 1) | d) & mask)
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    return out


def true_pairs(delta, v, hi):
    out = set()
    for x in range(3, hi):
        if is_pow2(x) or v2(x)[0] != v:
            continue
        out.add((run(delta, x), run(delta, step1(x))))
    return out


def check_product(n_dfas=400, hi=300000, vmax=2):
    """The product must CONTAIN every true pair (else spurious SAT) and should
    contain nothing else (else spurious UNSAT)."""
    import random
    random.seed(7)
    missing = spurious = 0
    for _ in range(n_dfas):
        n = random.randint(2, 5)
        delta = [[random.randrange(n) for _ in (0, 1)] for _ in range(n)]
        delta[0][0] = 0                                  # our convention
        for v in range(vmax + 1):
            a, b = needle_branch(v)
            got = product_pairs(delta, v, a, b)
            want = true_pairs(delta, v, hi)
            if not want <= got:
                missing += 1
                print(f"   MISSING pairs, v={v} delta={delta}: {want - got}")
            if got - want:
                spurious += 1
    print(f"2. product vs truth on {n_dfas} random DFAs, x < {hi:,}, "
          f"v <= {vmax}: {missing} with missing pairs (unsound if > 0), "
          f"{spurious} with extra pairs (over-strong if > 0)")
    return missing, spurious


# ------------------------------------------- 3. SAT vs brute enumeration ---
def brute(n, vmax, orbit_len=40, hi=300000):
    """Every n-state DFA with our convention, checked directly."""
    from msb_search import orbit
    orb = orbit(6, orbit_len)
    halts = [1 << e for e in range(2 * n + 6)]
    slots = [(s, d) for s in range(n) for d in (0, 1)]
    for combo in itertools.product(range(n), repeat=len(slots)):
        delta = [[0, 0] for _ in range(n)]
        for (s, d), t in zip(slots, combo):
            delta[s][d] = t
        if delta[0][0] != 0:
            continue
        # Horn propagation: orbit states TRUE, closure forward, halts must stay
        acc = {run(delta, x) for x in orb}
        pairs = set()
        for v in range(vmax + 1):
            a, b = needle_branch(v)
            pairs |= product_pairs(delta, v, a, b)
        changed = True
        while changed:
            changed = False
            for (p, q) in pairs:
                if p in acc and q not in acc:
                    acc.add(q)
                    changed = True
        if any(run(delta, h) in acc for h in halts):
            continue
        return delta, sorted(acc)
    return None


def check_sat_vs_brute(nmax=4, vmax=1):
    for n in range(2, nmax + 1):
        b = brute(n, vmax)
        s = search(n, vmax, verbose=False)
        agree = (b is None) == (s is None)
        print(f"3. n={n}: brute {'certificate' if b else 'none':<11} "
              f"SAT {'certificate' if s else 'none':<11} "
              f"{'AGREE' if agree else '*** DISAGREE ***'}")
        assert agree, n


# ---------------------------------------------------- 4. calibration -------
def audit_certificate(delta, acc, x0, F, hi=300000, vmax=None):
    """Re-verify a produced certificate against the ACTUAL map, independently
    of the encoding: start in I, I closed under F, I disjoint from H.

    A "certificate found" is the one result in this program that would be a
    positive claim, so it never rests on the solver's word.
    """
    acc = set(acc)
    fails = {"start": [], "closure": [], "halt": []}
    if run(delta, x0) not in acc:
        fails["start"].append(x0)
    for x in range(1, hi):
        s = run(delta, x)
        if is_pow2(x):
            if s in acc:
                fails["halt"].append(x)
            continue
        if vmax is not None and v2(x)[0] > vmax:
            continue          # branch not imposed by the search; not a failure
        if s in acc:
            y = F(x)
            if y == "HALT" or run(delta, y) not in acc:
                fails["closure"].append(x)
    return fails


def check_calibration():
    got = search(2, 3, which="times4", verbose=False)
    print(f"4. calibration C(x) = 4x at n=2: "
          f"{'certificate found -- search is not blind' if got else '*** NOT FOUND ***'}")
    if got:
        delta, acc = got
        fails = audit_certificate(delta, acc, 6, lambda x: 4 * x, vmax=3)
        n = {k: len(v) for k, v in fails.items()}
        print(f"     delta={delta} acc={acc}")
        print(f"     independent audit against C(x)=4x for x < 300,000: "
              f"start/closure/halt violations = {n}")
        assert not any(fails.values()), {k: v[:5] for k, v in fails.items()}
    return got


if __name__ == "__main__":
    check_identity()
    check_product()
    check_sat_vs_brute()
    check_calibration()
