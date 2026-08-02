"""Power calibration for the WS1 SAT search: if a k-state certificate EXISTS,
does the search find it -- and at what cost?

WHY THIS IS NEEDED.  The only calibration so far was C(x) = 4x, which has a
2-STATE certificate (even number of 1 bits).  Finding that shows the search is
not blind; it says nothing about whether a 9-state certificate would be found.
Until that is measured, "no certificate at <= 10 states" for the Needle has
unknown statistical power, and WS4's account of decider-resistance rests on it.

THE INSTRUMENT.  We need machines that (a) provably HAVE a certificate whose
size we control, and (b) produce SAT instances of the same shape and size as the
Needle's, so the timings are comparable.  Both are achieved by keeping the
Needle's own branch multipliers and moving only the additive constants:

    Needle    branch v:   x = 2^{v+1} k + 2^v   |->   a_v k + b_v,
                          a_v = 2^{v+1} + 3,     b_v = 2^v + v.

    Instrument G_m, same a_v, but   b_v := a_v * inv2  (mod m),  m odd,
                          where inv2 = (m+1)/2 is the inverse of 2 mod m.

CLAIM (proved, verified below).  I_m = {x : m | x} is G_m-invariant.
    m | x = 2^v (2k+1) and m is odd, so m | 2k+1, i.e. k = -inv2 (mod m).
    Then G_m(x) = a_v k + b_v = a_v(-inv2) + a_v inv2 = 0 (mod m).
The halt set is unchanged (powers of 2), and no power of 2 is a multiple of an
odd m > 1, so I_m misses it; the orbit of any multiple of m stays in I_m, so a
certificate exists.  Its size is controlled by m: k(m) = the number of states of
the minimal DFA for "value = 0 mod m", read LSB-first.  Since b_v < m and the
Needle's own b_v are also small, the carry sets -- which is what the product
size is driven by -- stay the same magnitude.  This is as close to a like-for-
like instrument as the encoding permits.

WHAT IT MEASURES -- and what it does not.  A COMPLETED "UNSAT" is a complete
refutation: the solver has proved no satisfying assignment exists, so no amount
of solver slowness can undermine it, and "would it have found one in time?" is
not the question.  The live risk is the other one: an encoding that is
accidentally OVER-CONSTRAINED reports UNSAT for machines that do have
certificates, and every impossibility theorem built on it is then vacuous.  That
is what this calibrates.  For each planted size k we check the encoding admits a
certificate at n = k -- any certificate, not only the planted one.  Reaching
k = 13 covers every size at which this program claims an impossibility result.

THE INSTRUMENT IS SELF-CERTIFYING.  k(m) is only an UPPER bound on the smallest
certificate a priori: the minimal-word convention leaves the DFA's behaviour on
non-minimal words as don't-cares, and don't-cares can only help.  But the run
sweeps n upwards, so the UNSAT verdicts at every n < k prove no smaller
certificate exists at all -- combined with the planted one at k, that pins the
true minimum to exactly k, with no appeal to the construction.

Usage:  python3 calibrate.py [kmin] [kmax]
"""
import sys
import time

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/automatic")

from general import lsb_word                                # noqa: E402
from sat_generalq import search_sat                         # noqa: E402


# ------------------------------------------------------- the planted set ----
def min_dfa_size(m):
    """States of the minimal DFA for {w : value_LSB(w) = 0 mod m}.

    State (r, p): r = value read so far mod m, p = 2^len mod m.  Reachable set
    first, then Moore partition refinement.
    """
    start = (0, 1 % m)
    states, stack = {start: 0}, [start]
    while stack:
        r, p = stack.pop()
        for d in (0, 1):
            nxt = ((r + d * p) % m, (2 * p) % m)
            if nxt not in states:
                states[nxt] = len(states)
                stack.append(nxt)
    trans = [[0, 0] for _ in states]
    for (r, p), i in states.items():
        for d in (0, 1):
            trans[i][d] = states[((r + d * p) % m, (2 * p) % m)]
    order = sorted(states.items(), key=lambda kv: kv[1])
    part = [0 if r == 0 else 1 for (r, _p), _i in order]
    while True:                                        # Moore refinement
        sig, new = {}, []
        for i in range(len(part)):
            key = (part[i], part[trans[i][0]], part[trans[i][1]])
            new.append(sig.setdefault(key, len(sig)))
        if len(set(new)) == len(set(part)):
            return len(set(new))
        part = new


def machine(m, vmax):
    """Branch table for G_m in sat_generalq's format, plus a sanity check."""
    inv2 = (m + 1) // 2
    brs = []
    for v in range(vmax + 1):
        a = (1 << (v + 1)) + 3
        b = (a * inv2) % m
        brs.append(([0] * v + [1], a, b, False))
    return brs


def step(m, x):
    """G_m applied to x.  Defined on every branch, not only the encoded ones:
    capping v is about which CLOSURE constraints are encoded, not about the
    machine, and the orbit must be the machine's true orbit."""
    v = 0
    while not (x >> v) & 1:
        v += 1
    a = (1 << (v + 1)) + 3
    return a * (x >> (v + 1)) + (a * ((m + 1) // 2)) % m


# ------------------------------------------------------------ verification --
def verify(m):
    """Machine-verify the invariance claim (every multiple of m below 400k, so
    every branch v <= 18 is exercised) before anything is built on it."""
    for x in range(m, 400000, m):
        assert step(m, x) % m == 0, (m, x)
    return min_dfa_size(m)


def main():
    kmin = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    kmax = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    vmax = 1
    print("WS1 power calibration -- planted certificates of known size")
    print("machine G_m: Needle multipliers a_v = 2^{v+1}+3, b_v = a_v*inv2 mod m")
    print("halt set: powers of 2 (as for the Needle).  convention: minimal words")
    print()

    # One m per planted size.  m MUST BE PRIME: for composite m every proper
    # odd divisor d | m gives I_d strictly containing I_m and equally
    # invariant, so the true minimum is k(d), not k(m).  Observed live: m = 9
    # was solved at n = 3 by the multiples-of-3 certificate, not at n = 9.
    bysize = {}
    for m in range(3, 400, 2):
        if any(m % d == 0 for d in range(3, int(m ** 0.5) + 1, 2)):
            continue
        k = min_dfa_size(m)
        if kmin <= k <= kmax and k not in bysize:
            bysize[k] = m
    print(f"planted sizes available: "
          f"{ {k: bysize[k] for k in sorted(bysize)} }")
    print()

    for k in sorted(bysize):
        m = bysize[k]
        assert verify(m) == k
        brs = machine(m, vmax)
        orb, x = [], m
        for _ in range(40):
            orb.append(x)
            x = step(m, x)
        assert all(o % m == 0 for o in orb), m       # the orbit stays in I_m
        halts = [1 << e for e in range(2 * kmax + 8)]
        print(f"--- planted k={k} (m={m}, b_v={[br[2] for br in brs]}, "
              f"orbit {len(orb)} elts) ---")
        t0 = time.time()
        for n in range(2, k + 3):
            got = search_sat(n, 2, brs, orb, halts)
            if got:
                delta, acc = got
                print(f"      FOUND at n={n} after {time.time()-t0:.1f}s total"
                      f"   delta={delta} acc={acc}")
                break
        else:
            print(f"      NOT FOUND up to n={k+2} "
                  f"({time.time()-t0:.1f}s) -- planted size was {k}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
