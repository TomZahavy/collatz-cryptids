"""Lucy's Moonlight (bbchallenge BB(6) cryptid, Racheline 2025) -- exact
implementation of Ligocki's Collatz-like reduction, for the exhibit-a-halt
comparison with machine 4.

Rules (C(a,b), from sligocki.com/2025/04/21/lucys-moonlight.html and the
bbchallenge wiki -- both sources agree):
    main phase   a>=1, b=3k   : C(a, b) -> C(a-1, 8k+6)
                 a>=2, b=3k+1 : C(a, b) -> C(a-2, 8k+16)
                 a>=2, b=3k+2 : C(a, b) -> C(a-2, 8k+22)
    reset        a=0,  b=3k   : C(0, b) -> C(2k, 8)
                 a=1,  b=3k+2 : C(1, b) -> C(2k+4, 8)
    zero phase   a=0,  b=3k+1 : C(0, b) -> C(0, 8k+5)
                 a=0,  b=3k+2 : C(0, b) -> C(0, 8k+5)
    halt         a=1,  b=3k+1 : HALT
Start: C(0, 0).  Published checkpoints (configs C(c,8)): c1=14, c2=11292,
c3 ~ 10^2901.92.  VALIDATION: this file must reproduce them exactly/log-wise.
"""
import math
import random
import sys


def step(a, b):
    k, r = divmod(b, 3)
    if a == 0:
        if r == 0:
            return (2 * k, 8, "reset")
        return (0, 8 * k + 5, "zero")
    if a == 1:
        if r == 1:
            return None                       # HALT
        if r == 2:
            return (2 * k + 4, 8, "reset")
        return (0, 8 * k + 6, "main")         # a=1, b=3k -> C(0, 8k+6)
    if r == 0:
        return (a - 1, 8 * k + 6, "main")
    if r == 1:
        return (a - 2, 8 * k + 16, "main")
    return (a - 2, 8 * k + 22, "main")


def run_to_checkpoint(a, b, max_steps=10**7):
    """Run until the next reset lands on C(c, 8) (returns ('reset', c, steps))
    or HALT (returns ('halt', None, steps))."""
    for n in range(1, max_steps + 1):
        nxt = step(a, b)
        if nxt is None:
            return ("halt", None, n)
        a, b, kind = nxt
        if kind == "reset":
            return ("reset", a, n)
    return ("cap", None, max_steps)


if __name__ == "__main__":
    # ---- validate against the published trajectory ----
    a, b = 0, 0
    cps = [(0, 0)]
    steps_total = 0
    while len(cps) < 5:
        out, c, n = run_to_checkpoint(a, b)
        steps_total += n
        assert out == "reset", out
        cps.append((c, steps_total))
        a, b = c, 8
    print("checkpoints (c, cumulative reduction steps):")
    for i, (c, s) in enumerate(cps):
        d = math.log10(c) if c > 10**6 else None
        print(f"  c{i} = {c if d is None else f'10^{d:.2f}'}"
              f"   (step {s})")
    # cps[0] is the start config, cps[1] the immediate trivial reset C(0,8)
    assert cps[2][0] == 14 and cps[3][0] == 11292
    l3 = math.log10(cps[4][0])
    print(f"  c3 log10 = {l3:.2f}  (published: 2901.92)")
    assert abs(l3 - 2901.92) < 0.02
    print("  -> matches the published c1, c2, c3: reduction is faithful\n")

    # the NEXT excursion needs ~c3 ~ 10^2901 reduction steps: unreachable.
    print(f"next halt opportunity: end of the countdown from C(c3, 8), "
          f"~0.6*c3 ~ 10^{l3 - 0.2:.0f} reduction steps away -- unreachable\n")

    # ---- per-checkpoint halt probability, random checkpoints C(a, 8) ----
    print("per-checkpoint P(halt before next reset), random a of n bits:")
    rng = random.Random(4)
    for nbits, samples in ((10, 400), (12, 300), (14, 200)):
        h = t = 0
        for _ in range(samples):
            a0 = rng.randrange(1 << nbits, 1 << (nbits + 1))
            out, c, n = run_to_checkpoint(a0, 8)
            if out == "halt":
                h += 1
            t += 1
        print(f"  n={nbits}: {h}/{t} = {h/t:.3f}")
    print("\n(sligocki's heuristic: 1/5 per checkpoint)")
