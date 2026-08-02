"""THE SYSTEM AFTER STEP 25.

From (0,0,0,0), after exactly 25 base steps the machine is at (0,1,0,17).
From there it never leaves the anchor section {a = 0, c = 0}, up to bounded
closed-form jumps, so the entire machine is equivalent to this 2-variable
system with initial state

    (b, d) = (1, 17)        [entered at base step 25]

Rules (first match fires; each returns the next anchor and the EXACT number
of original base steps it replaces):

 0  HALT                                        if d = b + 2
 1  cascade: n = n_A(b, d) rounds at once       if d >= 2b + 6
      -> (2^n (b+4) - 4, d - 2(b+4)(2^n - 1) + 2n)
      interior halt iff  3(b+4)*2^i = d + 2b + 10 + 2i  for some 0 <= i <= n
      (then the round-i anchor has d = b + 2: transition there and halt)
 2  exit -> (1, 16(d - b) - 55)                 if b+5 <= d <= 2b+5, 15d > 18b+61
 3  SWEEP(6b - 3d + 19, 4d - 4b - 14)           if b+5 <= d <= 2b+5
 4  SWEEP(3b + 2, 6)                            if d = b + 3
 5  SWEEP(3b + 4, 4)                            if d = b + 4
 6  -> (2d, 2b - 3d + 4)                        if 2 <= d, 3d < 2b + 5
 7  -> (6d - 4b - 8, 10b - 11d + 24)            if d <= b+1, 11d <= 10b + 24
      (on the boundary 3d = 2b+5 this specializes to (2, 4d-1), cost d+3,
       matching the distinct recharge path exactly - so no separate rule)
 8  SWEEP(9d - 6b - 12, 8b - 8d + 20)           if d <= b+1
 9  -> (0, 2b + 4)                              if d = 0
10  -> (2, 2b + 1), or (2, 5) if b = 0          if d = 1

SWEEP(A, Delta): the closed-form sub-map of formal.py (cascade B + 3-way
exit); here extended with exact costs.

Orbit usage (verified census below): the orbit of (1, 17) exercises rules
{1, 2, 3, 4, 6, 8, 9}; rules 5, 7, 10, 11 have never fired in 20,000 cycles
but are kept - they are near-diagonal cases of the same kind as HALT itself,
and equivalence requires them.
"""
from accel import acc_step, is_halt_state
from onedim import n_A, n_B

def _pump_cost(b, d):
    return b*d + d*d + d + 1

def _geom_halt_i(b, d, n):
    """smallest-solution search: integer 0 <= i <= n with
    3(b+4)*2^i == d + 2b + 10 + 2i  (LHS-RHS strictly increasing)."""
    C, K = 3*(b + 4), d + 2*b + 10
    lo, hi = 0, n
    while lo <= hi:
        m = (lo + hi) // 2
        v = C * (1 << m) - K - 2*m
        if v == 0: return m
        if v < 0: lo = m + 1
        else: hi = m - 1
    return None

def sweep_cost(A, Dl):
    """(next anchor, exact base steps) for the state (A, 0, Dl), Dl >= 1."""
    cost = 0
    if 3*Dl <= A and A >= 3:
        n = n_B(A, 0, Dl)
        w = 12*Dl + 8
        T = (4**(n - 1) - 1) // 3
        As = A - 3*Dl + 3*n - 2 - w*T
        Ds = (w * 4**(n - 1) - 2) // 3
        cost += Dl + 1 + (w*T + n - 1) // 3          # cascade-B certificate
        if As == 1:                                   # interior anchor: the
            return ((Ds - 2) // 2, 0), cost - 1       # final recharge not taken
    else:
        As, Ds = A, Dl
        if As == 0: return (0, Ds), 0
        if As == 1: return (0, Ds + 2), 1             # jump
    if As == 2: return (1, Ds - 1), cost + 2          # two (b = 0: cost 2)
    q, r = divmod(As, 3)
    if r == 0: return (2*q, Ds - q), cost + q         # drain
    if r == 2: return (2*q + 1, Ds - q - 1), cost + q + (2*q + 2)  # drain, two
    #  r == 1: drain, pump, two
    return (1, 4*Ds + 1), cost + q + _pump_cost(2*q, Ds - q) + 2

def step25(b, d):
    """One rule of the after-step-25 system: (next, exact base steps),
    or ('HALT', k) when the halt state is reached after k steps."""
    if d == b + 2 and d >= 2:  return "HALT", 0
    if d >= 2*b + 6:                                          # rule 1
        n = n_A(b, d)
        i = _geom_halt_i(b, d, n)
        if i is not None:                                     # interior halt
            p = 1 << i
            return "HALT", (b + 4)*(p - 1) - 2*i
        p = 1 << n
        return (p*(b + 4) - 4, d - 2*(b + 4)*(p - 1) + 2*n), \
               (b + 4)*(p - 1) - 2*n
    if b + 5 <= d <= 2*b + 5:
        if 15*d > 18*b + 61:                                  # rule 2 (exit)
            bp, dp = 4*b - 2*d + 12, 5*d - 6*b - 20
            return (1, 16*(d - b) - 55), b + 3 + _pump_cost(bp, dp) + 2
        nxt, c = sweep_cost(6*b - 3*d + 19, 4*d - 4*b - 14)   # rule 3
        return nxt, (d - b - 3) + c
    if d == b + 3:
        nxt, c = sweep_cost(3*b + 2, 6)                       # rule 4
        return nxt, 1 + c
    if d == b + 4:
        nxt, c = sweep_cost(3*b + 4, 4)                       # rule 5
        return nxt, 1 + c
    if d >= 2:
        if 3*d < 2*b + 5:                                     # rule 6
            return (2*d, 2*b - 3*d + 4), 3*d + 2
        # the boundary 3d = 2b+5 is subsumed by rule 7: its guard always
        # holds there (11d <= 15d-1) and the formula specializes to
        # (2, 4d-1) with the same cost d+3
        if 11*d <= 10*b + 24:                                 # rule 7
            return (6*d - 4*b - 8, 10*b - 11*d + 24), d + 3
        nxt, c = sweep_cost(9*d - 6*b - 12, 8*b - 8*d + 20)   # rule 9
        return nxt, (2*b - 2*d + 7) + c
    if d == 0:  return (0, 2*b + 4), 2                        # rule 10
    return ((2, 2*b + 1) if b > 0 else (2, 5)), 3             # rule 11

# --------------------------- verification ------------------------------
def next_anchor_exec(b, d):
    """Ground truth: level-2 composition with exact costs. Returns the next
    anchor plainly (a halt-state anchor is returned as a state; halting is
    detected on the following call, matching step25's semantics)."""
    t, cum = (0, b, d), 0
    if is_halt_state(t): return "HALT", 0
    while True:
        t, k = acc_step(t)
        cum += k
        if t[0] == 0: return (t[1], t[2]), cum

if __name__ == "__main__":
    import random
    from collections import Counter
    from onedim import F as F_onedim
    rng = random.Random(13)

    def exec_rule(b, d):
        """Ground truth matching rule granularity: the cascade rule spans
        every consecutive anchor with d >= 2b + 6 (halting if an interior
        anchor is the halt state); all other rules span one anchor step."""
        if d == b + 2 and d >= 2: return "HALT", 0
        if d < 2*b + 6: return next_anchor_exec(b, d)
        cum = 0
        while d >= 2*b + 6:
            r, k = next_anchor_exec(b, d)
            cum += k
            if r == "HALT": return "HALT", cum
            b, d = r
            if d == b + 2 and d >= 2: return "HALT", cum
        return (b, d), cum

    n = 0                                     # rule-level: states AND costs
    for _ in range(40000):
        b = rng.randint(0, 10**rng.randint(1, 8))
        d = rng.randint(0, 10**rng.randint(1, 8))
        assert step25(b, d) == exec_rule(b, d), (b, d)
        n += 1
    print(f"after-step-25 system verified (states and exact costs) on {n} anchors")

    # whole-orbit: D-sequence and cumulative base steps vs onedim
    (b, d), cum = (1, 17), 25
    D, total = 17, 25
    for _ in range(1000):
        D, c, _ = F_onedim(D); total += c
        while True:
            r, k = step25(b, d)
            assert r != "HALT"
            cum += k; b, d = r
            if b == 1: break
        assert (d, cum) == (D, total), (D, d)
    print("orbit reproduced for 1000 cycles: same D and same exact base-step totals")

    # usage census over 20,000 cycles
    (b, d), used = (1, 17), Counter()
    cycles = 0
    while cycles < 20000:
        if d == b + 2 and d >= 2: used["halt"] += 1; break
        if d >= 2*b + 6: tag = "1-cascade"
        elif b + 5 <= d <= 2*b + 5: tag = "2-exit" if 15*d > 18*b + 61 else "3-sweep"
        elif d == b + 3: tag = "4-reset3"
        elif d == b + 4: tag = "5-reset4"
        elif d >= 2:
            tag = ("6-expand" if 3*d < 2*b + 5 else
                   "7-boundary" if 3*d == 2*b + 5 else
                   "8-expand-deep" if 11*d <= 10*b + 24 else "9-sweep-expand")
        elif d == 0: tag = "10-d0"
        else: tag = "11-seed"
        used[tag] += 1
        (b, d), _ = step25(b, d)
        if b == 1: cycles += 1
    print("rule usage over 20,000 cycles:", dict(used.most_common()))
