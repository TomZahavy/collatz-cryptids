"""Level 4: the machine from (0,0,0,0) as a one-dimensional system.

From the fixed start, the trajectory reaches (0,1,0,17) at base step 25 and
thereafter returns to (0,1,D) every super-cycle: the entire 4-variable
machine reduces to iterating a return map D -> F(D) from D = 17 (the halt
question: does the orbit ever hit one of the four halting lines mid-cycle).

F has no finite closed-form catalog (super-cycle branch signatures grow
without bound - the map processes D's binary expansion, which is its
Collatz-like essence), so a cycle is executed as a short composition of
level-3 steps. The speed win over accel3 is algorithmic: the cascade round
counts n_A, n_B are located by binary search over the strictly monotone
guard inequality in O(log n) bigint operations instead of the O(n) linear
scan - on this orbit n_A ~ bits(D), so this removes the dominant cost.

All halting-line checks from orbit.py run every cycle; base-step totals are
exact.
"""
import time
from accel3 import acc3_step, n_A as n_A_slow, n_B as n_B_slow
from orbit import P, cascadeA_safe, cascadeB_safe

def n_A(b, d):
    """max { m >= 1 : (b+4)*2^(m+1) <= d + 2(b+4) + 2m }, by binary search
    (LHS-RHS is strictly increasing in m since 2(b+4) > 2)."""
    lo, hi, best = 1, d.bit_length() + 2, 1
    while lo <= hi:
        m = (lo + hi) // 2
        if (b + 4) << (m + 1) <= d + 2*(b + 4) + 2*m:
            best = m; lo = m + 1
        else:
            hi = m - 1
    return best

def n_B(a, b, d):
    """max { m >= 1 : w*4^(m-1) <= 3(a-3d) + w + 9(m-1) }, w = 6b+12d+8."""
    w = 6*b + 12*d + 8
    lo, hi, best = 1, (a.bit_length() // 2) + 3, 1
    while lo <= hi:
        m = (lo + hi) // 2
        if w * 4**(m - 1) <= 3*(a - 3*d) + w + 9*(m - 1):
            best = m; lo = m + 1
        else:
            hi = m - 1
    return best

def step(t):
    """One level-3 step with fast cascade sizing and all halting-line checks.
    Returns (t', base_steps) or raises RuntimeError on a halting line."""
    a, b, d = t
    if a == 0 and d >= 2 and d == b + 2:
        raise RuntimeError(("HALT", t))
    if P(a, b, d):
        raise RuntimeError(("P-HIT", t))
    if a == 0 and d >= 2*b + 6:
        n = n_A(b, d)
        if not cascadeA_safe(b, d, n):
            raise RuntimeError(("HALT-IN-CASCADE-A", t))
        p = 1 << n
        return (0, p*(b + 4) - 4, d - 2*(b + 4)*(p - 1) + 2*n), \
               (b + 4)*(p - 1) - 2*n
    if a >= 3 and d > 0 and 3*d <= a:
        n = n_B(a, b, d)
        if not cascadeB_safe(a, b, d, n):
            raise RuntimeError(("HALT-IN-CASCADE-B", t))
        w = 6*b + 12*d + 8
        T = (4**(n - 1) - 1) // 3
        return (a - 3*d + 3*n - 2 - w*T, 0, (w * 4**(n - 1) - 2) // 3), \
               d + 1 + (w*T + n - 1) // 3
    return acc3_step(t)

def F(D):
    """One super-cycle: (0,1,D) -> (0,1,D'). Returns (D', exact base steps,
    level-3 steps used)."""
    t, cum, k = (0, 1, D), 0, 0
    while True:
        t, c = step(t)
        cum += c; k += 1
        if t[0] == 0 and t[1] == 1:
            return t[2], cum, k

def run(cycles, report_every=20000, D=17, total=25):
    """Iterate F from the true start; 'total' starts at 25 = exact base steps
    from (0,0,0,0) to (0,1,0,17)."""
    t0 = time.time()
    for i in range(cycles):
        D, c, _ = F(D)
        total += c
        if (i + 1) % report_every == 0:
            print(f"  cycle {i+1}: ~10^{len(str(total))-1} base steps, "
                  f"D has {len(str(D))} digits, {time.time()-t0:.0f}s", flush=True)
    return D, total

if __name__ == "__main__":
    import random
    rng = random.Random(3)
    for _ in range(3000):                     # fast sizing == slow sizing
        b = rng.randint(0, 200); d = 2*b + 6 + rng.randint(0, 10**rng.randint(1, 12))
        assert n_A(b, d) == n_A_slow(b, d), (b, d)
        dd = rng.randint(1, 10**4); bb = rng.randint(0, 300)
        a = 3*dd + rng.randint(0, 3*dd * 10**rng.randint(0, 6))
        if 3*dd <= a:
            assert n_B(a, bb, dd) == n_B_slow(a, bb, dd), (a, bb, dd)
    print("fast n_A / n_B verified against linear-scan versions")

    D, total = 17, 25
    for _ in range(1000):                     # F == composed level-3 steps
        D2, c, _ = F(D)
        t, cum = (0, 1, D), 0
        while True:
            t, k = acc3_step(t); cum += k
            if t[0] == 0 and t[1] == 1: break
        assert (t[2], cum) == (D2, c), D
        D, total = D2, total + c
    print("F verified against accel3 for 1000 orbit cycles "
          f"(now at ~10^{len(str(total))-1} base steps)")
