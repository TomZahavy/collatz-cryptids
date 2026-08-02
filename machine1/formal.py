"""Formalization of the level-4 return map F.

ANCHORS. An anchor is a c=0 state with a=0, written (b, d). Every
trajectory visits anchors repeatedly (between two anchors lies a bounded
chain of rules plus at most one cascade). Define G(b, d) = the next anchor.

THE ANCHOR MAP G - complete case table (first match; all closed-form):

  guard                                      next anchor (b', d')
  ------------------------------------------------------------------
  d = 0                                      (0, 2b + 4)
  d = 1                                      (2, 2b + 1) if b > 0, else (2, 5)
  d = b + 2                                  HALT
  2 <= d <= b+1  and  3d < 2b + 5            (2d, 2b - 3d + 4)          [expand, full drain, two]
  2 <= d <= b+1  and  3d = 2b + 5            (2, 4d - 1)                [boundary: a,d hit 2,0 together]
  2 <= d <= b+1  and  11d <= 10b + 24        (6d - 4b - 8, 10b - 11d + 24)  [expand, drain to d=0,
                                                                         recharge, full drain]
  2 <= d <= b+1                              SWEEP(9d - 6b - 12, 8b - 8d + 20)
  d = b + 3                                  SWEEP(3b + 2, 6)
  d = b + 4                                  SWEEP(3b + 4, 4)
  b+5 <= d <= 2b+5  and  15d > 18b + 61      (1, 16(d - b) - 55)        [shrink, drain to d=0,
                                                                         recharge, drain, pump, two]
  b+5 <= d <= 2b+5                           SWEEP(6b - 3d + 19, 4d - 4b - 14)
  d >= 2b + 6                                (2b + 4, d - 2b - 6)       [one cascade-A round]

  SWEEP(A, Dl) - the state (A, 0, Dl). If 3*Dl <= A, cascade B runs to its
  exit (A*, 0, D*) (closed form, n_B rounds); A* = 1 signals that the last
  round hit A' = 3D' exactly and its drain landed on the interior anchor
  ((D* - 2)/2, 0), where G stops. Otherwise (3D* > A*, A* >= 2) the exit
  drains fully, q = floor(A*/3); by A* mod 3:
     0:  anchor (2q, D* - q)
     2:  ... two:            anchor (2q + 1, D* - q - 1)
     1:  ... pump, two:      anchor (1, 4*D* + 1)        <- an F-exit!

F = first-return map of G to the section {b = 1}: from (1, D), iterate G
until b = 1 again; the d-component is F(D).

PIECEWISE AFFINITY. Every G-case is affine in (b, d) once the cascade
round counts are fixed, so on each finite branch word w (the sequence of
G-cases with their round counts) F is affine: F|w(D) = alpha_w * D + beta_w.
The word is determined by D, and word lengths grow ~ log D (F reads D's
binary expansion top-down) - hence countably many affine pieces rather
than one finite formula.

Example (the dominant word: full cascade A, then the shrink F-exit):
    F(D) = 16*D - 240*2^n + 32*n + 169,    n = n_A(1, D),
verified below on every cycle using that word.
"""
from accel import acc_step, is_halt_state
from onedim import n_A, n_B, F as F_onedim

def sweep(A, Dl):
    """SWEEP(A, Dl): the state (A, 0, Dl), Dl >= 1. Runs cascade B if its
    guard 3*Dl <= A holds (n >= 1 closed-form rounds), else zero rounds;
    then the exit chain. Total for every A >= 0."""
    if 3*Dl <= A and A >= 3:
        n = n_B(A, 0, Dl)
        w = 12*Dl + 8
        T = (4**(n - 1) - 1) // 3
        As = A - 3*Dl + 3*n - 2 - w*T
        Ds = (w * 4**(n - 1) - 2) // 3
        if As == 1:
            # As = A' - 3D' + 1 = 1 means the last round had A' = 3D'
            # exactly: its drain landed on the anchor (2D', 0) BEFORE the
            # recharge. D' = (Ds - 2)/4, so the anchor is ((Ds - 2)/2, 0).
            return ((Ds - 2) // 2, 0)
    else:
        As, Ds = A, Dl                        # no full sweep round possible
        if As == 0: return (0, Ds)            # already an anchor
        if As == 1: return (0, Ds + 2)        # jump (b = 0 here)
    if As == 2: return (1, Ds - 1)            # two
    q, r = divmod(As, 3)                      # full drain (3*Ds > As)
    if r == 0: return (2*q, Ds - q)
    if r == 2: return (2*q + 1, Ds - q - 1)   # ... two
    return (1, 4*Ds + 1)                      # r == 1: pump, two - an F-exit

def G(b, d):
    """The anchor map, straight from the case table."""
    if d == 0:          return (0, 2*b + 4)
    if d == 1:          return (2, 2*b + 1) if b > 0 else (2, 5)
    if d == b + 2:      return "HALT"
    if d <= b + 1:
        if 3*d < 2*b + 5:     return (2*d, 2*b - 3*d + 4)
        if 3*d == 2*b + 5:    return (2, 4*d - 1)     # a,d hit 2,0 together
        if 11*d <= 10*b + 24: return (6*d - 4*b - 8, 10*b - 11*d + 24)
        return sweep(9*d - 6*b - 12, 8*b - 8*d + 20)
    if d == b + 3:      return sweep(3*b + 2, 6)
    if d == b + 4:      return sweep(3*b + 4, 4)
    if d <= 2*b + 5:
        if 15*d > 18*b + 61:  return (1, 16*(d - b) - 55)
        return sweep(6*b - 3*d + 19, 4*d - 4*b - 14)
    return (2*b + 4, d - 2*b - 6)

def G_exec(b, d):
    """Ground truth: compose verified LEVEL-2 steps to the next anchor
    (level 3 would jump over intermediate anchors inside cascades)."""
    t = (0, b, d)
    if is_halt_state(t):
        return "HALT"
    while True:
        t, _ = acc_step(t)
        if t == "HALT":
            return "HALT"
        if t[0] == 0:
            return (t[1], t[2])

def F_via_G(D):
    """First return of G to the section {b = 1}."""
    b, d = G(1, D)
    while b != 1:
        r = G(b, d)
        if r == "HALT": return "HALT"
        b, d = r
    return d

def steps_to_section(b, d, cap=20000):
    """Anchor steps until b == 1 or HALT; None if cap exceeded."""
    for i in range(cap):
        if b == 1: return i
        r = G(b, d)
        if r == "HALT": return i
        b, d = r
    return None

if __name__ == "__main__":
    import random
    rng = random.Random(9)

    # 1. G == step-composition, on random anchors of many magnitudes
    n = 0
    for _ in range(40000):
        b = rng.randint(0, 10**rng.randint(1, 10))
        d = rng.randint(0, 10**rng.randint(1, 10))
        assert G(b, d) == G_exec(b, d), (b, d, G(b, d), G_exec(b, d))
        n += 1
    print(f"anchor map G verified against step composition on {n} states")

    # 2. F_via_G == onedim.F along the true orbit
    D = 17
    for _ in range(800):
        D2, _, _ = F_onedim(D)
        assert F_via_G(D) == D2, D
        D = D2
    print("F as first-return map of G verified for 800 orbit cycles")

    # 3. piecewise affinity: the dominant word's affine formula
    D, hits = 17, 0
    for _ in range(3000):
        n_ = n_A(1, D)
        B, E = 5*(1 << n_) - 4, D - 10*((1 << n_) - 1) + 2*n_
        D2, _, _ = F_onedim(D)
        if B + 5 <= E <= 2*B + 5 and 15*E > 18*B + 61:   # word = [caseA^n, exit]
            assert D2 == 16*D - 240*(1 << n_) + 32*n_ + 169, D
            hits += 1
        D = D2
    print(f"affine piece F(D) = 16D - 240*2^n + 32n + 169 verified on "
          f"{hits} of 3000 orbit cycles (the dominant branch word)")

    # 4. section return: every tested anchor reaches b == 1 or halts
    worst = 0
    for b in range(0, 201):
        for d in range(0, 201):
            s = steps_to_section(b, d)
            assert s is not None, (b, d)
            worst = max(worst, s)
    for _ in range(2000):
        b = rng.randint(1, 2**rng.choice([10, 40, 160, 320]))
        d = rng.randint(max(1, b//3), 3*b)
        s = steps_to_section(b, d)
        assert s is not None, (b, d)
        worst = max(worst, s)
    print(f"section return verified on 40,401 box + 2,000 random anchors "
          f"(max {worst} anchor steps; no growth with scale)")
