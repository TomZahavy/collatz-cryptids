"""Machine 1 — the monotone potential: Phi = 2b + d strictly increases.

THEOREM (potential).  At every non-halting anchor step of the after-step-25
system, Phi = 2b + d increases by at least 2.  Consequently the system admits
no cycles, and the trajectory from (0,0,0,0) never repeats a state after
step 25: anchors have strictly increasing Phi, and the segments between
anchors are finite (anchor recurrence).  This closes unconditionally the one
scenario that pure simulation can never exclude — an eventually-periodic
orbit with an astronomically long transient (cf. bbchallenge's Skelet #1,
periodic only after 5.4e51 steps).

PROOF SKETCH (per rule of afterstep25.step25; Delta = Phi' - Phi):

  rule 1 (cascade, d >= 2b+6):  (b,d) -> (2^n(b+4)-4, d-2(b+4)(2^n-1)+2n)
     Delta = 2n >= 2 exactly (the (b+4)(2^n-1) terms cancel 2:1).
  rule 2 (exit):  (b,d) -> (1, 16(d-b)-55)
     Delta = 15d - 18b - 53 >= 9, since the guard is 15d >= 18b + 62.
     (The exit guard IS the potential's positivity condition plus margin 9.)
  rules 6, 7:  Delta = +4 and +8 exactly (direct affine computation).
  rules 10, 11:  Delta = +4 (or +8 at the b = 0 seed).
  sweep rules 3, 4, 5, 9 rest on a conservation lemma for cascade-B:

     LEMMA.  If SWEEP(A, Dl) runs its cascade for n >= 1 rounds, the
     pre-drain outputs satisfy   As + Ds = A + Dl + 3n.
     (From As = A - 3Dl + 3n - 2 - wT, Ds = (w 4^(n-1) - 2)/3, w = 12Dl + 8,
      T = (4^(n-1)-1)/3: substitute wT = Ds - (w-2)/3.)

     The drain post-processing then gives Phi' in
     {Ds + As, Ds + As - 1, Ds + 2 (As=2 path), Ds - 2 (interior anchor),
      4Ds + 3 (pump)}; the first four are >= A + Dl + 3n - 3, and the pump
     case satisfies 4Ds + 3 - (As + Ds) = 3Ds - As + 3 >= 2 because
     As <= 3Ds + 1 at cascade termination.  Hence always
        Phi'_sweep >= A + Dl + 3n - 3 >= A + Dl        (n >= 1).
  rule 3:  A + Dl = Phi + 5, and its guard 15d <= 18b + 61 is EQUIVALENT to
     the cascade condition 3Dl <= A (12d-12b-42 <= 6b-3d+19), so the cascade
     always runs:  Delta >= 3n + 2 >= 5.
  rule 9:  A + Dl = Phi + 8, and its guard 11d > 10b + 24 is equivalent to
     3Dl <= A, so again the cascade always runs:  Delta >= 3n + 5 >= 8.
  rules 4, 5:  A + Dl = Phi + 5 and Phi + 4; when the cascade does not run
     (small b) the drain/pump cases are checked directly (Delta >= 4).

  Minimum over all rules: 2, attained by rule 1 with n = 1 — matching the
  measured minimum exactly.
"""
from afterstep25 import step25
from onedim import n_B


def phi(b, d):
    return 2 * b + d


if __name__ == "__main__":
    import random
    rng = random.Random(0)

    # --- the conservation lemma ---
    bad = n = 0
    for _ in range(60000):
        A = rng.randint(3, 10 ** rng.randint(1, 9))
        Dl = rng.randint(1, max(1, A // 3))
        if 3 * Dl > A:
            continue
        rounds = n_B(A, 0, Dl)
        w = 12 * Dl + 8
        T = (4 ** (rounds - 1) - 1) // 3
        As = A - 3 * Dl + 3 * rounds - 2 - w * T
        Ds = (w * 4 ** (rounds - 1) - 2) // 3
        if As + Ds != A + Dl + 3 * rounds:
            bad += 1
        n += 1
    assert bad == 0
    print(f"lemma As + Ds = A + Dl + 3n: {n} cases, 0 violations")

    # --- guard <=> cascade equivalences used by rules 3 and 9 ---
    for b in range(0, 2000):
        for d in range(0, 2000):
            if b + 5 <= d <= 2 * b + 5 and 15 * d <= 18 * b + 61:
                A, Dl = 6 * b - 3 * d + 19, 4 * d - 4 * b - 14
                assert 3 * Dl <= A and A >= 3, (b, d)
            if d >= 2 and d <= b + 1 and 11 * d > 10 * b + 24:
                A, Dl = 9 * d - 6 * b - 12, 8 * b - 8 * d + 20
                assert 3 * Dl <= A and A >= 3, (b, d)
    print("rules 3 and 9 always run their cascade (guard equivalence): OK")

    # --- the theorem, exhaustively small + randomly large ---
    mininc, n = 10 ** 9, 0
    for b in range(0, 300):
        for d in range(0, 300):
            r, _ = step25(b, d)
            if r == "HALT":
                continue
            inc = phi(*r) - phi(b, d)
            assert inc >= 2, (b, d, r, inc)
            mininc = min(mininc, inc)
            n += 1
    for _ in range(60000):
        b = rng.randint(0, 10 ** rng.randint(1, 10))
        d = rng.randint(0, 10 ** rng.randint(1, 10))
        r, _ = step25(b, d)
        if r == "HALT":
            continue
        inc = phi(*r) - phi(b, d)
        assert inc >= 2, (b, d, r, inc)
        mininc = min(mininc, inc)
        n += 1
    print(f"Phi increment >= 2 on {n} transitions (minimum found: {mininc})")

    # --- along the true orbit ---
    b, d = 1, 17
    prev, steps = phi(b, d), 0
    for _ in range(300000):
        r, _ = step25(b, d)
        if r == "HALT":
            break
        b, d = r
        assert phi(b, d) >= prev + 2
        prev = phi(b, d)
        steps += 1
    print(f"orbit: Phi strictly increased by >= 2 at all {steps} anchor steps")
    print("=> no cycles; the trajectory never repeats a state after step 25")
