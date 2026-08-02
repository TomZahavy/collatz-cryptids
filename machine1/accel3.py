"""Level 3 in fully closed form: the complete 13-rule system.

State (a, b, d); an original config embeds as (a, b, c, d) -> (a, b+c, d).
Every rule is a closed-form expression; the two cascade rules use a round
count n defined by a single monotone inequality (binary-searchable, and
n = floor(log2(.)) or floor(log4(.)) up to +-1).

Each rule returns (state', exact number of original base steps replaced).
Verified below against accel2 (which is verified against accel, which is
verified per-rule and per-trajectory against the original base system).
"""
import random
from accel import acc_step, is_halt_state
from accel2 import acc2_step

def n_A(b, d):
    """max { m >= 1 : (b+4)*2^(m+1) <= d + 2(b+4) + 2m }  (guard: d >= 2b+6)"""
    m = 1
    while (b + 4) << (m + 2) <= d + 2*(b + 4) + 2*(m + 1):
        m += 1
    return m

def n_B(a, b, d):
    """max { m >= 1 : w*4^(m-1) <= 3(a-3d) + w + 9(m-1) },  w = 6b+12d+8
    (guard: 3d <= a)"""
    w = 6*b + 12*d + 8
    m = 1
    while w * 4**m <= 3*(a - 3*d) + w + 9*m:
        m += 1
    return m

def acc3_step(t):
    a, b, d = t
    # 1. HALT
    if a == 0 and d >= 2 and d == b + 2:
        return "HALT", 0
    # 2. recharge
    if d == 0:
        return (a + 1, 0, 2*b + 2), 1
    if a >= 3:
        # 3. Cascade B (sweep):  3d <= a
        if 3*d <= a:
            n = n_B(a, b, d)
            w = 6*b + 12*d + 8
            T = (4**(n - 1) - 1) // 3
            return (a - 3*d + 3*n - 2 - w*T, 0, (w * 4**(n - 1) - 2) // 3), \
                   d + 1 + (w*T + n - 1) // 3
        # 4. partial drain (3d > a  =>  k = floor(a/3))
        q = a // 3
        return (a % 3, b + 2*q, d - q), q
    # 5-7. small a
    if a == 2:
        return (0, b + 1, d - 1), b + 2
    if a == 1 and b > 0:
        return (2, 0, 2*b + 4*d + 2), b*d + d*d + d + 1
    if a == 1:
        return (0, 0, d + 2), 1
    # a == 0
    # 8. seed
    if d == 1:
        return (0, 2, (2*b + 1) if b > 0 else 5), 3
    # 9. expand
    if b >= d - 1:
        return (3*d - 4, 3, 2*b - 2*d + 3), 3
    # 10. Cascade A (shrink-drain):  d >= 2b+6
    if d >= 2*b + 6:
        n = n_A(b, d)
        p = 1 << n
        return (0, p*(b + 4) - 4, d - 2*(b + 4)*(p - 1) + 2*n), \
               (b + 4)*(p - 1) - 2*n
    # 11. single shrink (b+5 <= d <= 2b+5)
    if d >= b + 5:
        return (3*b + 3, 2, d - b - 5), 1
    # 12-13. resets
    if d == b + 3:
        return (3*b + 2, 0, 6), 1
    return (3*b + 4, 0, 4), 1           # d == b + 4

# ------------------------- verification --------------------------------
def acc2_multi(t, target_cum):
    """Advance acc2 until cumulative steps reach target_cum; return state."""
    cum = 0
    while cum < target_cum:
        t, k = acc2_step(t)
        cum += k
    assert cum == target_cum, "checkpoint not aligned"
    return t

if __name__ == "__main__":
    rng = random.Random(17)
    checked = 0
    # per-step: acc3's result must equal acc2 advanced by the same step count
    for _ in range(20000):
        t = (rng.randint(0, 10**rng.randint(1, 9)),
             rng.randint(0, 10**rng.randint(1, 4)),
             rng.randint(0, 10**rng.randint(1, 9)))
        if is_halt_state(t):
            assert acc3_step(t) == ("HALT", 0); checked += 1; continue
        t3, k3 = acc3_step(t)
        if k3 > 10**7:  # skip pathological pump costs in the *walk*; state check only
            pass
        assert t3 == acc2_multi(t, k3), (t, t3, k3)
        checked += 1
    # trajectory: acc3 and acc2 visit identical (state, cum) checkpoint pairs
    for s in [(0,0,0), (10,10,10), (0,0,5), (5,0,7)]:
        t2, t3, c2, c3 = s, s, 0, 0
        for _ in range(400):
            if is_halt_state(t3):
                assert is_halt_state(t2) and c2 == c3; break
            t3, k = acc3_step(t3); c3 += k
            while c2 < c3:
                t2, k2 = acc2_step(t2); c2 += k2
            assert (t2, c2) == (t3, c3), (s, t3, c3)
        checked += 1
    print("closed-form level-3 verified on", checked, "checks")
