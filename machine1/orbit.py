"""Deep verified run from (0,0,0,0): does the system ever halt?

Halting criterion (machine-verified exhaustively, see writeup): the system
halts iff some level-2 macro state (a,b,d) satisfies
    P:  d - b - a == 2   and   a % 3 != 1.

This runner uses the level-3 closed-form system for speed but checks P at
every level-2 macro state, including all states INTERNAL to the two
cascades, via exact binary searches (each phi-along-cascade sequence is
strictly monotone, so phi == 2 is decidable in O(log n) without expansion).

Cascade A from (0,b,d), rounds i = 0..n-1, visits:
  a=0 states  (0,b_i,d_i):            phi_i = d+2b+12+2i - 3(b+4)*2^i
  shrink outs (3b_i+3, 2, d_i-b_i-5): psi_i = d+2b+14+2i - 6(b+4)*2^i
  (both a-values have a % 3 != 1, so phi==2 or psi==2 means HALT)
  f(i) = 3(b+4)2^i - (d+2b+10+2i)  is strictly increasing (3(b+4) >= 12 > 2),
  so phi_i == 2 has at most one root: exact binary search. Same for psi.

Cascade B from (a,b,d) visits drain outputs (d=0 so phi = -a-b < 2: safe)
and recharge outputs with
  phi_1 = 2b+7d+1-a,   phi_i = 7*d_{i-1}+1-a_{i-1}  (i>=2),
strictly increasing (phi_{i+1}-phi_i = 24*d_{i-1}+13 > 0): binary search.
A hit is flagged conservatively (without checking a%3) - sound.
"""
import time
from accel import acc_step, is_halt_state
from accel3 import acc3_step, n_A, n_B

def P(a, b, d):
    return d - b - a == 2 and a % 3 != 1

def geom_root(C, K, imax):
    """True iff some integer 0 <= i <= imax has C*2^i == K + 2i  (C >= 12)."""
    lo, hi = 0, imax
    while lo <= hi:
        mid = (lo + hi) // 2
        v = C * (1 << mid) - K - 2*mid       # strictly increasing in mid
        if v == 0: return True
        if v < 0: lo = mid + 1
        else: hi = mid - 1
    return False

def cascadeA_safe(b, d, n):
    if geom_root(3*(b+4), d + 2*b + 10, n):        # phi_i == 2, i in 0..n
        return False
    if n >= 1 and geom_root(6*(b+4), d + 2*b + 12, n - 1):  # psi_i == 2
        return False
    return True

def cascadeB_safe(a, b, d, n):
    def state_at(i):
        """(phi, a) at recharge output i (1-indexed)."""
        if i == 1:
            return 2*b + 7*d + 1 - a, a - 3*d + 1
        w = 6*b + 12*d + 8
        T = (4**(i - 2) - 1) // 3
        a_prev = a - 3*d + 1 + 3*(i - 2) - w*T
        d_prev = (w * 4**(i - 2) - 2) // 3
        return 7*d_prev + 1 - a_prev, a_prev - 3*d_prev + 1
    lo, hi = 1, n
    while lo <= hi:
        mid = (lo + hi) // 2
        v, a_out = state_at(mid)              # phi strictly increasing in mid
        if v == 2:
            return a_out % 3 == 1             # a=1 mod 3 escapes via pump
        if v < 2: lo = mid + 1
        else: hi = mid - 1
    return True

def cross_check_small(t):
    """For small cascades, expand every internal level-2 state and test P
    directly - validates the binary-search checks."""
    a, b, d = t
    states = []
    if a == 0 and d >= 2*b + 6:
        while d >= 2*b + 6:
            states.append((0, b, d))
            states.append((3*b + 3, 2, d - b - 5))
            b, d = 2*b + 4, d - 2*b - 6
        states.append((0, b, d))
    elif a >= 3 and d > 0 and 3*d <= a:
        while d > 0 and a >= 3 and 3*d <= a:
            states.append((a, b, d))
            states.append((a - 3*d, b + 2*d, 0))
            a, b, d = a - 3*d + 1, 0, 2*b + 4*d + 2
        states.append((a, b, d))
    return any(P(*s) for s in states)

def run(macro_cap, report_every=10000, validate_below=10**40):
    t = (0, 0, 0)
    total = 0
    t0 = time.time()
    for macro in range(macro_cap):
        a, b, d = t
        if is_halt_state(t) or P(a, b, d):
            return ("HALT-PATH", t, total, macro)
        if a == 0 and d >= 2*b + 6:
            unsafe = not cascadeA_safe(b, d, n_A(b, d))
            if max(t) < validate_below:
                assert unsafe == cross_check_small(t), t
            if unsafe: return ("HALT-IN-CASCADE-A", t, total, macro)
        elif a >= 3 and d > 0 and 3*d <= a:
            unsafe = not cascadeB_safe(a, b, d, n_B(a, b, d))
            if max(t) < validate_below:
                assert unsafe == cross_check_small(t), t
            if unsafe: return ("HALT-IN-CASCADE-B", t, total, macro)
        t, k = acc3_step(t)
        total += k
        if (macro + 1) % report_every == 0:
            print(f"  macro {macro+1}: ~10^{len(str(total))-1} base steps, "
                  f"{time.time()-t0:.0f}s", flush=True)
    return ("NO-HALT", t, total, macro_cap)

if __name__ == "__main__":
    kind, t, total, macro = run(120000)
    if kind == "NO-HALT":
        print(f"NO HALT within the first 10^{len(str(total))-1} base steps "
              f"({macro} level-3 steps, exact count has {len(str(total))} digits)")
    else:
        print(kind, "at", t, "after ~10^%d base steps" % (len(str(total))-1))
