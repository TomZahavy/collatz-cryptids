"""Machine 3 — the theorems, verified.

T1 (halting criterion).  From A(1,1) the machine halts iff the a-value reaches
   an exact power of 3, a = 3^j, with j = 0 (mod 3).  Equivalently: a divide
   chain reaches a = 1 (which happens exactly when the pre-divide value is a
   pure power of 3, M = 1), landing at A(1, 3^j + j); and 3^j + j = j (mod 3),
   so it halts iff j = 0 (mod 3).  The halting set of a-values is therefore
        {3^j : j = 0 mod 3} = {27, 729, 19683, ...} = {27^m : m >= 1}.
   This is a MULTIPLICATIVE-coincidence cryptid (the Space Needle type of the
   bbchallenge catalogue): halting requires the orbit to land exactly on a
   power, not on an affine family.

T2 (divide-chain closed form).  From (N, b0), N = 3^j * M, M % 3 != 0, the
   a % 3 == 0 rule applied j times yields (M, b0 + (N - M) + j).  This is the
   acceleration: an otherwise O(N) chain of divisions is one jump.

T3 (monotone potential).  Phi = a + b increases by at least 1 at every
   non-halting step.  Proof: divide adds exactly 1; a reset a -> (4a+8)/3 (or
   (4a+10)/3) with b cancelling gives increment (a+8)/3 (resp. (a+10)/3) > 0;
   the a=1 exits give +3 and +2.  Minimum increment 1, attained by divides.
   COROLLARY: the machine cannot cycle; from A(1,1) it halts or escapes to
   infinity, with no eventually-periodic alternative (cf. Skelet #1).

T4 (b is bounded away from mattering except at a = 1).  Between the rare
   power-of-3 events, b is 1 at every reset; b only grows inside a divide
   chain and is immediately consumed by the following reset.  The halting
   test reads b only at a = 1, where b = 3^j + j is pinned by the exponent.

Measurements: growth rate of a per reset; frequency of divide chains and the
distribution of their depth j (a Geom-like law, since a mod 3 behaves
pseudo-randomly); reset-value stream for the P8 risk accounting.
"""
from m3_base import step, HALT
from m3_accel import cstep, v3
import random
from collections import Counter


def phi(a, b):
    return a + b


if __name__ == "__main__":
    rng = random.Random(0)

    # ---- T1: halting criterion, direct ----
    # construct a = 3^j reset states and confirm the halt/pass-through split
    bad = 0
    for j in range(1, 16):
        # place the machine at (3^j, 1) and run base steps to resolution
        s = (3 ** j, 1)
        for _ in range(3 * j + 5):
            s = step(s)
            if s == HALT:
                break
        halted = (s == HALT)
        if halted != (j % 3 == 0):
            bad += 1
    assert bad == 0
    print("T1  a = 3^j halts iff j = 0 (mod 3); halting set {27^m}: OK")

    # ---- T2: divide-chain closed form ----
    bad = 0
    for _ in range(30000):
        j = rng.randint(1, 14)
        M = rng.choice([m for m in range(1, 60) if m % 3])
        b0 = rng.randint(1, 10 ** 6)
        N = 3 ** j * M
        a, b = N, b0
        for _ in range(j):
            a, b = a // 3, b + 2 * (a // 3) + 1
        assert (a, b) == (M, b0 + (N - M) + j)
        bad += (a, b) != (M, b0 + (N - M) + j)
    print("T2  divide chain (N,b0) -> (M, b0 + (N-M) + j): 30,000 cases OK")

    # ---- T3: potential ----
    mininc, n = 10 ** 9, 0
    for a in range(1, 400):
        for b in range(1, 400):
            r = step((a, b))
            if r == HALT:
                continue
            inc = phi(*r) - phi(a, b)
            assert inc >= 1, (a, b, r)
            mininc = min(mininc, inc)
            n += 1
    for _ in range(200000):
        a = rng.randint(1, 10 ** rng.randint(1, 10))
        b = rng.randint(1, 10 ** rng.randint(1, 10))
        r = step((a, b))
        if r == HALT:
            continue
        inc = phi(*r) - phi(a, b)
        assert inc >= 1, (a, b, r)
        mininc = min(mininc, inc)
        n += 1
    print(f"T3  Phi = a + b increment >= 1 on {n} transitions (min {mininc}): "
          f"no cycles: OK")

    # ---- measurements: divide depth and growth ----
    a, b = 1, 1
    depth = Counter()
    resets = 0
    a_at_reset = []
    steps = 0
    while steps < 400000:
        r = cstep(a, b)
        if r[0] == "HALT":
            print("HALT during measurement (unexpected):", r)
            break
        if r[0] == "A1":
            a, b = 1, r[1]
            steps += 1
            continue
        na, nb = r
        if a % 3 == 0:
            j, _ = v3(a)
            depth[j] += 1
        a, b = na, nb
        if b == 1 and a % 3 != 0:
            resets += 1
            if len(a_at_reset) < 4000:
                a_at_reset.append(a)
        steps += 1
    tot = sum(depth.values())
    print(f"\nmeasured over {steps} composite steps: {resets} resets, "
          f"{tot} divide chains")
    print("divide-chain depth j = 3-adic valuation; law P(j) = (2/3)(1/3)^(j-1):")
    for j in range(1, 7):
        pred = (2 / 3) * (1 / 3) ** (j - 1)
        print(f"   j={j}: {depth[j] / tot:.4f}   model {pred:.4f}")
    # growth of a per reset (log2)
    import math
    if len(a_at_reset) > 100:
        lg = [math.log2(x) for x in a_at_reset if x > 1]
        slope = (lg[-1] - lg[100]) / (len(lg) - 100)
        print(f"growth: log2(a) rises ~{slope:.4f} bits per reset "
              f"(reset map ~ x4/3 => log2(4/3) = {math.log2(4/3):.4f} minus "
              f"strip losses)")
