"""Independent check of the three BW-sibling candidates: fresh FRACTRAN
simulator (mine), exact boundary-state formulas vs direct big-int replay.
Convention (int-y1/BBFractran): start n = 2; at each step the FIRST fraction
p/q in list order with q | n fires: n -> n*p/q; halt if none fires."""
from fractions import Fraction

def run(fracs, nmax_steps, watch_num, watch_den):
    """Simulate; record (step, n) at every firing of fraction index `watch`
    that STARTS a run (previous firing was a different fraction)."""
    fr = [Fraction(a, b) for a, b in fracs]
    n = 2
    prev = None
    boundaries = []
    for step in range(nmax_steps):
        for j, f in enumerate(fr):
            if n % f.denominator == 0:
                if (f.numerator, f.denominator) == (watch_num, watch_den) and prev != j:
                    boundaries.append((step, n))
                n = n * f.numerator // f.denominator
                prev = j
                break
        else:
            return boundaries, ("HALT", step)
    return boundaries, ("cap", nmax_steps)

def v(n, p):
    c = 0
    while n % p == 0: n //= p; c += 1
    return c

print("=== candidate 431: [5/6, 9/35, 8/55, 7/2, 605/7] ===")
b, end = run([(5,6),(9,35),(8,55),(7,2),(605,7)], 600000, 7, 2)
print(f"  outcome: {end[0]} at step cap; {len(b)} runs of 7/2 started")
ok = bad = 0
for i, (step, n) in enumerate(b[1:], start=1):        # i >= 1 per the claim
    exp2, exp11 = (1 << (i+1)) - 1, i
    pred_n = (1 << exp2) * 11**i
    pred_s = (1 << (i+3)) - 5*i - 8
    good = (n == pred_n and step == pred_s)
    ok += good; bad += not good
    if not good and bad <= 3:
        print(f"  MISMATCH i={i}: v2={v(n,2)} (pred {exp2}) v11={v(n,11)} "
              f"(pred {exp11}) step={step} (pred {pred_s})")
print(f"  boundary formula n_i = 2^(2^(i+1)-1)*11^i at S(i)=2^(i+3)-5i-8: "
      f"{ok} exact, {bad} mismatches")

print("=== candidate 455: [63/10, 8/77, 33/2, 5/9, 7/3] ===")
b, end = run([(63,10),(8,77),(33,2),(5,9),(7,3)], 600000, 33, 2)
ok = bad = 0
checked = 0
for i0, (step, n) in enumerate(b):
    # claim: v2 = 2^i + 1, v3 = 2^i - 2, v11 = i - 1, S(i) = 2^(i+2) - 5
    # find which i this boundary corresponds to via the step formula
    i = (step + 5).bit_length() - 3
    if (1 << (i+2)) - 5 != step: continue
    pred = (1 << ((1 << i) + 1)) * 3**((1 << i) - 2) * 11**(i-1) if (1<<i) >= 2 and i >= 1 else None
    if pred is None: continue
    checked += 1
    good = (n == pred)
    ok += good; bad += not good
    if not good and bad <= 3:
        print(f"  MISMATCH i={i}: v2={v(n,2)} v3={v(n,3)} v5={v(n,5)} "
              f"v7={v(n,7)} v11={v(n,11)} step={step}")
print(f"  boundary formula (v2,v3,v11)=(2^i+1, 2^i-2, i-1) at S(i)=2^(i+2)-5: "
      f"{ok} exact of {checked} matched boundaries, {bad} mismatches; "
      f"{len(b)} runs of 33/2 seen, outcome {end[0]}")

print("=== candidate 678: [9/70, 25/2, 44/15, 7/55, 3/5] ===")
b, end = run([(9,70),(25,2),(44,15),(7,55),(3,5)], 600000, 25, 2)
ok = bad = 0; checked = 0
for (step, n) in b:
    # claim: n_i = 5^(2^(i+2)) * 11^(2^(i+1)-1) at S(i) = 7*2^(i+1) - 3i - 9
    # invert step formula
    i = 1
    while 7*(1 << (i+1)) - 3*i - 9 < step: i += 1
    if 7*(1 << (i+1)) - 3*i - 9 != step: continue
    pred = 5**(1 << (i+2)) * 11**((1 << (i+1)) - 1)
    checked += 1
    good = (n == pred)
    ok += good; bad += not good
    if not good and bad <= 3:
        print(f"  MISMATCH i={i}: v2={v(n,2)} v3={v(n,3)} v5={v(n,5)} "
              f"v7={v(n,7)} v11={v(n,11)} step={step}")
    # the invariant claimed to protect the machine: v5 = 2*(v11 + 1)
    if v(n,5) != 2*(v(n,11)+1):
        print(f"  INVARIANT FAIL at step {step}: v5={v(n,5)} v11={v(n,11)}")
print(f"  boundary formula 5^(2^(i+2))*11^(2^(i+1)-1) at S(i)=7*2^(i+1)-3i-9: "
      f"{ok} exact of {checked} matched boundaries, {bad} mismatches; "
      f"{len(b)} runs of 25/2 seen, outcome {end[0]}")
