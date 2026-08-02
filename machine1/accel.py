"""Accelerated system on triples (a, b, d)  [c eliminated],
with exact base-step counts per macro rule, plus per-rule verification."""
import random
from collatz import base_step, HALT

# ---------------------------------------------------------------
# Level 1+2: c eliminated; unary loops batched into closed forms.
# Correspondence: base (a,b,c,d) with c=0  <->  triple (a,b,d).
# A base state with c>0 drains to (a, b+c, 0, d) in c steps first.
# Each macro rule returns (new_triple_or_HALT, exact_base_steps).
# ---------------------------------------------------------------
def acc_step(t):
    a, b, d = t
    if d == 0:
        return (a+1, 0, 2*b+2), 1                       # M-recharge
    if a >= 3:
        k = min(a // 3, d)                              # M-drain (batched)
        return (a-3*k, b+2*k, d-k), k
    if a == 2:
        return (0, b+1, d-1), b+2                       # M-two (incl. c-drain)
    if a == 1 and b > 0:
        # d pump rounds (each costs b_i+2 with b_i = b+2i), then recharge
        return (2, 0, 2*b + 4*d + 2), d*b + d*d + d + 1 # M-pump (batched)
    if a == 1:
        return (0, 0, d+2), 1                           # M-jump
    # a == 0
    if d == 1:
        return (0, 2, (2*b+1) if b > 0 else 5), 3       # M-seed
    # a == 0, d >= 2
    if b >= d-1:
        return (3*d-4, 3, 2*b-2*d+3), 3                 # M-expand
    if d == b+2:
        return HALT, 0
    if d == b+3:
        return (3*b+2, 0, 6), 1                         # M-reset3
    if d == b+4:
        return (3*b+4, 0, 4), 1                         # M-reset4
    return (3*b+3, 2, d-b-5), 1                         # M-shrink (d>=b+5)

def is_halt_state(t):
    a, b, d = t
    return a == 0 and d >= 2 and d == b + 2

# ---------------------------------------------------------------
# Verification 1: per-rule exactness.
# For a triple t=(a,b,d), embed as base state (a,b,0,d), apply the macro
# rule -> (t', k). Then k applications of base_step must land exactly on
# (a',b',0,d')  (or on HALT).
# ---------------------------------------------------------------
def verify_rule(t):
    a, b, d = t
    if is_halt_state(t):
        assert base_step((a, b, 0, d)) == HALT, t
        return "halt"
    t2, k = acc_step(t)
    s = (a, b, 0, d)
    for _ in range(k):
        s = base_step(s)
        assert s != HALT, ("premature halt", t)
    a2, b2, d2 = t2
    assert s == (a2, b2, 0, d2), ("mismatch", t, t2, s, k)
    return "ok"

def random_triples(n, lo, hi, seed):
    rng = random.Random(seed)
    for _ in range(n):
        yield (rng.randint(lo, hi), rng.randint(lo, hi), rng.randint(lo, hi))

if __name__ == "__main__":
    count = 0
    # exhaustive small box
    for a in range(0, 25):
        for b in range(0, 25):
            for d in range(0, 25):
                verify_rule((a, b, d)); count += 1
    # random medium and large
    for t in random_triples(20000, 0, 10**3, 1): verify_rule(t); count += 1
    for t in random_triples(2000, 0, 10**4, 2): verify_rule(t); count += 1
    # targeted: hit every guard with big values (keep k modest where cost ~ b*d)
    rng = random.Random(3)
    for _ in range(2000):
        b = rng.randint(0, 500); d = rng.randint(1, 500)
        verify_rule((1, b, d)); verify_rule((2, b, d))          # pump / two
        verify_rule((10**6 + rng.randint(0,9), b, d))           # drain, huge a
        verify_rule((0, b, d)); verify_rule((rng.randint(0,4), b, 0))
        verify_rule((0, d-2 if d >= 2 else 0, d))               # halt guard
        count += 6
    print("per-rule verification passed on", count, "states")
