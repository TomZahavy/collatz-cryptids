"""Machine 4 -- EXACT accelerated section-to-section map (cascade batched).

The section is S = {(a,1) : a odd}.  Interior dynamics is the T5 clean table
(m4_mod16.py); the cascade rule b >= a+5 : (a,b) -> (2a+5, b-a-4) is batched
via T3's closed form
      a_j = 2^j (a+5) - 5,   b_j = b - (2^j - 1)(a+5) + j
so   d_j = b_j - a_j = b + j + 5 - (2^{j+1} - 1)(a+5),
which is strictly decreasing in j (d_{j+1} - d_j = 1 - 2^{j+1}(a+5) < 0).
The batch runs while d_j >= 5; the exit j* is the least j with d_{j*} < 5.
No halt can occur strictly inside a batch (interior cascade states have
b >= a+5 by definition of the guard; the halt line is b = a+3 < a+5), so
batching is exact.

Excursion-ending configurations (x odd interior value, y the b-coordinate):
    y = x-1 (y even, m-rule)  -> (2x+1, 1)   return
    y = x+1 (y even)          -> (2x-1, 1)   return
    y = x+2 (y odd)           -> (2x+5, 1)   return
    y = x+3 (y even)          -> HALT
    y = x+4 (y odd)           -> (2x+3, 1)   return
    y = x+5 (y even, cascade) -> (2x+5, 1)   return
Every excursion ends at its FIRST such configuration (or never ends).

excursion(a, cap) returns a dict:
    out      : 'HALT' | 'RETURN' | 'CAP'
    val      : return value a' (RETURN only)
    base     : exact number of base-machine steps for the excursion
               (from (a,1) up to and including the step that lands on
               (a',1) or HALT)
    rounds   : accelerated steps used (m-rules + cascade batches + exit)
    exit_d   : y - x at the ending configuration (in {-1,1,2,3,4,5})
    exit_m8  : x mod 8 at the ending configuration
    closest  : min |y - (x+3)| over all cascade-exit / near-line states seen
               (an 'almost halted' diagnostic; 0 iff HALT)
"""

HALT = "HALT"


def _cascade_exit(x, y):
    """Least j >= 1 with d_j < 5, for a state with y >= x+5.
    Returns (j, x_j, y_j)."""
    # d_j < 5  <=>  (2^{j+1} - 1)(x+5) > y + j.
    s = x + 5
    # initial guess from bit lengths: 2^{j+1} ~ (y + s)/s
    j = max(((y // s + 1).bit_length()) - 1, 1)
    # ensure guess is an exit (d_j < 5), then walk back to the least such j
    while y + j + 5 - (((1 << (j + 1)) - 1) * s) >= 5:      # still interior
        j += 1
    while j > 1 and y + (j - 1) + 5 - (((1 << j) - 1) * s) < 5:
        j -= 1
    p = 1 << j
    return j, p * s - 5, y - (p - 1) * s + j


def excursion(a, cap=None):
    """One exact excursion from section state (a,1), a odd.  cap = optional
    bound on accelerated rounds (None = unbounded)."""
    assert a % 2 == 1 and a >= 1
    x, y = a, 1
    base = 0
    rounds = 0
    closest = None
    while True:
        if cap is not None and rounds >= cap:
            return {"out": "CAP", "val": None, "base": base,
                    "rounds": rounds, "exit_d": None, "exit_m8": None,
                    "closest": closest, "state": (x, y)}
        rounds += 1
        if y <= x:
            # the two m-rules (this also covers the very first step (a,1))
            if y & 1:
                nx, ny = 2 * y + 1, x - y + 3          # ny >= 3: no return
                x, y = nx, ny
                base += 1
            else:
                nx, ny = 2 * y + 3, x - y
                base += 1
                if ny == 1:                             # y = x-1: return
                    d = -1
                    m8 = x & 7
                    miss = 4                            # |y-(x+3)| = 4
                    closest = miss if closest is None else min(closest, miss)
                    return {"out": "RETURN", "val": nx, "base": base,
                            "rounds": rounds, "exit_d": d, "exit_m8": m8,
                            "closest": closest}
                x, y = nx, ny
            continue
        d = y - x
        if d >= 5:
            if d == 5:                                  # single step, returns
                miss = 2
                closest = miss if closest is None else min(closest, miss)
                return {"out": "RETURN", "val": 2 * x + 5, "base": base + 1,
                        "rounds": rounds, "exit_d": 5, "exit_m8": x & 7,
                        "closest": closest}
            j, x2, y2 = _cascade_exit(x, y)
            base += j
            if y2 == 1:
                # the batch's LAST step had b = a+5 exactly: (a,a+5)->(2a+5,1),
                # a return to the section with value x2 (same d=5 channel)
                miss = 2
                closest = miss if closest is None else min(closest, miss)
                return {"out": "RETURN", "val": x2, "base": base,
                        "rounds": rounds, "exit_d": 5,
                        "exit_m8": ((x2 - 5) >> 1) & 7,   # source a of the step
                        "closest": closest}
            x, y = x2, y2
            continue
        # d in {1,2,3,4}: near-line dispatch
        miss = abs(d - 3)
        closest = miss if closest is None else min(closest, miss)
        base += 1
        m8 = x & 7
        if d == 3:
            return {"out": HALT, "val": None, "base": base,
                    "rounds": rounds, "exit_d": 3, "exit_m8": m8,
                    "closest": 0}
        val = 2 * x - 1 if d == 1 else (2 * x + 5 if d == 2 else 2 * x + 3)
        return {"out": "RETURN", "val": val, "base": base,
                "rounds": rounds, "exit_d": d, "exit_m8": m8,
                "closest": closest}


# ---------------------------------------------------------------------------
# verification against the raw base machine
# ---------------------------------------------------------------------------
def base_excursion(a, cap=10**7):
    """Reference: raw m4_base.step from (a,1) to first return/HALT.
    Returns (out, val, base_steps) with out in {'HALT','RETURN','CAP'}."""
    from m4_base import step, HALT as BH
    s = step((a, 1))
    n = 1
    while n <= cap:
        if s == BH:
            return ("HALT", None, n)
        if s[1] == 1:
            return ("RETURN", s[0], n)
        s = step(s)
        n += 1
    return ("CAP", None, n)


if __name__ == "__main__":
    import random
    import time
    t0 = time.time()
    # 1) exhaustive: all odd a <= 2000, values AND base-step counts
    bad = 0
    for a in range(1, 2001, 2):
        ref = base_excursion(a, cap=10**7)
        acc = excursion(a)
        got = (acc["out"], acc["val"], acc["base"])
        if ref != got:
            bad += 1
            print("MISMATCH", a, ref, got)
    print(f"exhaustive odd a <= 2000: {bad} mismatches "
          f"[{time.time()-t0:.1f}s]")
    # 2) random larger starts (base cap 10^7; skip CAP-CAP agreement checks)
    rng = random.Random(20260801)
    bad = tested = capped = 0
    while tested < 400:
        a = rng.randrange(1 << 12, 1 << 22) | 1
        ref = base_excursion(a, cap=10**7)
        if ref[0] == "CAP":
            capped += 1
            continue
        acc = excursion(a)
        got = (acc["out"], acc["val"], acc["base"])
        if ref != got:
            bad += 1
            print("MISMATCH", a, ref, got)
        tested += 1
    print(f"random 400 starts in [2^12,2^22): {bad} mismatches "
          f"({capped} base-capped skipped) [{time.time()-t0:.1f}s]")
    assert bad == 0
    print("acceleration is STEP-EXACT (values and base-step counts)")
