"""Machine 4 — theorems and measurements.

T1 (a is always odd).  Every odd-a rule outputs an odd a (4m+3, 4k+1, 4k+7,
   4k+5 are all odd), and the start a = 1 is odd.  So a stays odd forever and
   the even-a rules A(2k, .) are never used from A(1,1).

T2 (halting criterion).  With a odd, halting occurs exactly at the rule
   A(2k+1, 2k+4) -> HALT, i.e. at b = a + 3.  Since a is odd, b = a + 3 is
   even.  So the machine halts iff it reaches a state with a odd and
        b = a + 3.
   The dispatch on b - a near the line: b=a+1 -> (2a-1,1); b=a+2 -> (2a+5,1);
   b=a+3 -> HALT; b=a+4 -> (2a+3,1); b>=a+5 -> the cascade (T3).

T3 (cascade closed form).  The rule b >= a+5, (a,b) -> (2a+5, b-a-4), iterated
   j times gives
        a_j = 2^j (a+5) - 5,     b_j = b - (2^j - 1)(a+5) + j,
   valid while the guard b_j >= a_j + 5 holds.  a doubles and b drops by ~a
   each round -- so a long run of the dominant rule collapses to one jump.  An interior landing
   on the halt line b_j = a_j + 3 is detected in closed form.

T4 (no cycles, via a potential WITH RECOVERY).  No affine p*a+q*b is monotone
   here (the small-b rules R_e/R_o shrink a sharply, and b=a+1 lowers a+b by 1),
   so the plain P6 recipe fails.  But a+b is a potential with recovery:
     Lemma A: Delta(a+b) <= 0 only for b=a+1 (Delta=-1) and b=a+4 (Delta=0),
              and both land on a state with b=1.
     Lemma B: from any (a,1) with a odd, Delta(a+b) = +4.
   So every non-increasing step is isolated and immediately followed by a +4
   step; over any cycle the total Delta(a+b) is then strictly positive (each
   non-positive step pairs with the following +4 for a net >= +3, and every
   other step is >= +1), contradicting a cycle's zero sum.  Hence the machine
   cannot cycle: it halts or escapes to infinity.  This extends P6 -- the
   affine quantity need not be monotone step-by-step, only over a bounded
   recovery window -- and is the first machine in the collection to require it.
"""
from m4_base import step, HALT
import random


def cascade_state(a, b, j):
    p = 1 << j
    return p * (a + 5) - 5, b - (p - 1) * (a + 5) + j


if __name__ == "__main__":
    rng = random.Random(0)

    # ---- T1: a stays odd ----
    bad = 0
    for _ in range(300000):
        a = 2 * rng.randint(0, 10 ** 8) + 1      # odd a
        b = rng.randint(1, 10 ** 8)
        r = step((a, b))
        if r != HALT and r[0] % 2 == 0:
            bad += 1
    assert bad == 0
    s = (1, 1)
    for _ in range(200000):
        s = step(s)
        if s == HALT:
            break
        assert s[0] % 2 == 1
    print("T1  a stays odd (every odd-a rule outputs odd a); 300k random + "
          "200k orbit: OK")

    # ---- T2: halting criterion b = a+3, a odd ----
    for a in range(1, 4000, 2):
        for b in range(1, a + 8):
            r = step((a, b))
            if (r == HALT) != (b == a + 3):
                raise AssertionError((a, b, r))
    print("T2  halts iff b = a + 3 (a odd), exhaustively for a < 4000: OK")

    # ---- T3: cascade closed form ----
    bad = 0
    for _ in range(20000):
        a = 2 * rng.randint(0, 10 ** 6) + 1
        b = rng.randint(a + 5, a + 5 + 10 ** 7)  # in the b >= a+5 region
        # run the base rule while the guard holds, up to 200 rounds
        x, y = a, b
        j = 0
        while y >= x + 5 and j < 200:
            x, y = 2 * x + 5, y - x - 4
            j += 1
        if (x, y) != cascade_state(a, b, j):
            bad += 1
    assert bad == 0
    print("T3  cascade a_j = 2^j(a+5)-5, b_j = b-(2^j-1)(a+5)+j: 20,000 runs OK")

    # ---- T4: the recovery lemmas ----
    badA = badB = 0
    for _ in range(400000):
        a = 2 * rng.randint(0, 10 ** 8) + 1
        b = rng.randint(1, 10 ** 8)
        r = step((a, b))
        if r == HALT:
            continue
        d = (r[0] + r[1]) - (a + b)
        nonpos = d <= 0
        special = (b == a + 1) or (b == a + 4)
        if nonpos != special:
            badA += 1
        if nonpos and r[1] != 1:
            badA += 1
        if b == 1 and d != 4:
            badB += 1
    for a in range(1, 200000, 2):
        r = step((a, 1))
        if (r[0] + r[1]) - (a + 1) != 4:
            badB += 1
    assert badA == 0 and badB == 0
    print("T4  Lemma A (Delta(a+b)<=0 only at b=a+1,a+4, landing on b=1) and "
          "Lemma B (b=1 gives +4): OK -> no cycles")

    # ---- measurements ----
    from collections import Counter
    s = (1, 1)
    rules = Counter()
    ab = []
    best = 10 ** 18
    for _ in range(500000):
        a, b = s
        ab.append(a + b)
        if a % 2 == 1:
            best = min(best, abs((b - a) - 3))
        r = step(s)
        if r == HALT:
            break
        s = r
    drift = (ab[-1] - ab[0]) / len(ab)
    decs = sum(1 for i in range(len(ab) - 1) if ab[i + 1] < ab[i])
    print(f"\nmeasured over 500,000 steps: a+b drift {drift:.3f}/step, "
          f"{decs} decreases (each -1); closest |b-a-3| = {best}")
    print("growth is linear (a+b ~ 2.34 t); no plain affine potential is "
          "monotone, but a+b with the recovery lemma proves no cycles (T4)")
