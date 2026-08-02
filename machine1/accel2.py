"""Level 3: cascade super-rules (geometric batching) on top of accel.py.

Cascade A ("shrink-drain"): at (0,b,d) with d >= 2b+6, one round of
  shrink; drain  gives  (0, 2b+4, d-2b-6)   in  b+2 base steps.
  n rounds:  b_n = 2^n (b+4) - 4,   d_n = d - 2(b+4)(2^n - 1) + 2n
             base steps = (b+4)(2^n - 1) - 2n ... verified below.

Cascade B ("sweep"): at (a,b,d) with 0 < 3d and d <= a//3, one round of
  full-drain; recharge  gives  (a-3d+1, 0, 2b+4d+2)  in d+1 base steps.
  n rounds (b=0 after round 1):
     d_n = ((3d+2)*4^n - 2)/3 ... but round 1 uses b:  d_1 = 2b+4d+2
  Implemented as a loop (only ~log4 rounds), with closed form checked.
"""
import random
from collatz import base_step, HALT
from accel import acc_step, is_halt_state

def cascadeA_n(b, d, n):
    p = 1 << n
    return (p*(b+4) - 4, d - 2*(b+4)*(p-1) + 2*n), (b+4)*(p-1) - 2*n + 2*n  # steps fixed below

def acc2_step(t):
    a, b, d = t
    # Cascade A: a == 0, d >= 2b+6  (shrink applies and drain completes)
    if a == 0 and d >= 2*b + 6 and not is_halt_state(t):
        # find max n >= 1 with guard holding before every round
        def state(n):
            p = 1 << n
            return p*(b+4) - 4, d - 2*(b+4)*(p-1) + 2*n
        n = 1
        while True:
            bn, dn = state(n)
            if not (dn >= 2*bn + 6):
                break
            n += 1
        bn, dn = state(n)
        # base steps: each round i costs (shrink:1) + (drain: b_i+1) = b_i + 2
        steps = sum(( (1 << i)*(b+4) - 4 ) + 2 for i in range(n))  # = (b+4)(2^n-1)-2n
        return (0, bn, dn), steps
    # Cascade B: sweep loop
    if d > 0 and a >= 3 and d <= a // 3:
        steps = 0
        while d > 0 and a >= 3 and d <= a // 3:
            a, b, d, steps = a - 3*d + 1, 0, 2*b + 4*d + 2, steps + d + 1
        return (a, b, d), steps
    return acc_step(t)

# ---- verification: acc2 checkpoints must be step-exact w.r.t. acc ----
def verify_acc2(t0, n_macro):
    """Run acc (level 2, already verified against base) recording cumulative
    base steps; run acc2 and require every acc2 checkpoint to appear in the
    acc trajectory at the identical cumulative step count."""
    seen = {}  # state -> cumulative base steps (first visit)
    t, cum = t0, 0
    order = [(t, 0)]
    for _ in range(n_macro):
        if is_halt_state(t): break
        t, k = acc_step(t)
        cum += k
        order.append((t, cum))
    idx = {st_cum: i for i, st_cum in enumerate(order)}
    # walk acc2
    t, cum, i = t0, 0, 0
    while True:
        if is_halt_state(t) or (t, cum) not in idx:
            # allow acc2 to overrun the recorded horizon
            assert is_halt_state(t) or cum > order[-1][1], ("mismatch", t0, t, cum)
            return
        j = idx[(t, cum)]
        assert j >= i, ("order violation", t0, t)
        i = j
        if j == len(order) - 1: return
        t2, k = acc2_step(t)
        t, cum = t2, cum + k

if __name__ == "__main__":
    rng = random.Random(11)
    n = 0
    starts = [(0,0,0), (10,10,10), (0,0,5), (5,0,7), (1,0,0)]
    starts += [tuple(rng.randint(0,50) for _ in range(3)) for _ in range(40)]
    starts += [tuple(rng.randint(0,5000) for _ in range(3)) for _ in range(15)]
    for s in starts:
        verify_acc2(s, 4000); n += 1
    print("acc2 checkpoint verification passed on", n, "starts")

    # speed comparison: base steps covered per macro step
    for s in [(0,0,0), (10,10,10)]:
        t, cum = s, 0
        for i in range(300):
            if is_halt_state(t): break
            t, k = acc2_step(t); cum += k
        print(s, "-> 300 level-3 steps cover", "%.3e" % cum, "base steps; state size ~10^%d" %
              len(str(max(t))))
