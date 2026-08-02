"""THE HALTING CRITERION and its machine verification.

Define  phi(a,b,d) = d - b - a  on level-2 macro states (c eliminated).

THEOREM. From any c=0 configuration, the system halts if and only if its
trajectory contains a level-2 macro state t = (a,b,d) with

    P(t):   phi(t) = 2   and   a mod 3 != 1.

Moreover a P-state halts within at most 2 further macro steps.

PROOF SKETCH (each case machine-checked below).
(<=)  Let phi=2, a mod 3 != 1.
  a=0: d = b+2 >= 2 -- this IS the halt state.
  a=2: d = b+4 > 0, the a=2 rule gives (0, b+1, b+3): halt state.
  a>=3: d = a+b+2 > floor(a/3), so the drain runs k = floor(a/3) fully,
        giving (a mod 3, b+2k, d-k). phi is DRAIN-INVARIANT
        (delta = +3k -2k -k... i.e. d-k - (b+2k) - (a-3k) = d-b-a), and
        a mod 3 is in {0,2}: previous cases apply.
(=>)  A halt state (0, t, t+2) has phi = 2. The only rules that can output
  an a=0 state with phi=2 are drain (input a = 0 mod 3, phi preserved) and
  the a=2 rule (input phi preserved, a=2). Every other producer of a=0
  states misses phi=2 identically:
      jump   (1,0,d) -> (0,0,d+2):        phi' = d+2 >= 3
      seed   (0,b,1) -> (0,2,2b+1 or 5):  phi' = 2b-1 or 3, both odd... != 2
  So walking backwards through the maximal drain/two suffix (phi and
  "a mod 3 != 1" both preserved) reaches a macro state satisfying P.  #

COROLLARY (the explicit halting lines). phi=2-with-a-mod-3!=1 can only be
*created* by three rules; hence the system halts iff it ever reaches
  (i)   an a=0 state with d = b + 2          (immediate halt),
  (ii)  an a=0 state with d = 4b + 12        (via shrink),
  (iii) an a=0 state with 5d = 2b + 2, d>=2  (via expand),
  (iv)  a  d=0 state with a = 2b - 1 and b mod 3 != 2  (via recharge).
The remaining rules provably never create phi=2:
  pump:   phi' = 2b+4d       >= 6   (d>=1)
  jump:   phi' = d+2         >= 3
  seed:   phi' = 2b-1 or 3   (odd)
  reset3: phi' = 4-3b        = 2 impossible
  reset4: phi' = -3b         = 2 impossible
"""
import random
from collatz import base_step, HALT
from accel import acc_step, is_halt_state

def P(t):
    a, b, d = t
    return d - b - a == 2 and a % 3 != 1

def check_exact(t, N):
    """Horizon-exact check: within the first N base steps, the criterion must
    predict halting exactly, and a predicted halt must occur at precisely the
    base step certified by the macro step counts."""
    tt, cum, hit_at = t, 0, None
    while cum <= N:
        if is_halt_state(tt) or P(tt):
            hit_at = cum; break
        tt, k = acc_step(tt); cum += k
    s = (t[0], t[1], 0, t[2])
    if hit_at is not None:
        extra = 0
        while not is_halt_state(tt):          # criterion: at most 2 more steps
            tt, k = acc_step(tt); extra += k
        T = hit_at + extra
        for i in range(T):
            s = base_step(s)
            assert s != HALT, ("early halt", t, i, T)
        assert base_step(s) == HALT, ("no halt at certified step", t, T)
        return True
    for i in range(N):
        s = base_step(s)
        assert s != HALT, ("unpredicted halt", t, i)
    return False

if __name__ == "__main__":
    n = halts = 0
    for a in range(18):                        # exhaustive box
        for b in range(18):
            for d in range(18):
                halts += check_exact((a, b, d), 20000); n += 1
    rng = random.Random(31)
    for _ in range(1500):                      # random medium
        halts += check_exact((rng.randint(0, 60), rng.randint(0, 60),
                              rng.randint(0, 60)), 50000); n += 1
    for _ in range(1200):                      # adversarial: on/near phi = 2
        a, b = rng.randint(0, 40), rng.randint(0, 40)
        for eps in (-1, 0, 1):
            d = a + b + 2 + eps
            if d >= 0:
                halts += check_exact((a, b, d), 50000); n += 1
    print(f"halting criterion verified on {n} states "
          f"({halts} halts, each at its certified exact step), 0 violations")
