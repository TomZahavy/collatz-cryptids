"""The Hydra family through the toolkit — theorems and measurements.

T1 (no cycles, whole family).  The value strictly increases from step 2 on:
    H(n) = floor(3n/2) > n for n >= 2, and Fenrir's y-map exceeds y for
    y >= 2 (small cases 0 -> 2 -> 7 escape explicitly).  So none of Hydra,
    Antihydra, Fenrir can cycle: each halts or escapes to infinity.  (For
    these machines the trichotomy collapse is immediate — unlike machine 1,
    where it required the potential theorems.)

T2 (q-adic branch memory).  For the pure Hydra map,
    n_t mod 3^k  is an explicit function of the last k parities
    (p_{t-k}, ..., p_{t-1}), independent of everything earlier.
  Proof: n_t = 3*floor(n_{t-1}/2) + p_{t-1} and halving is invertible mod
  3^k, so mod 3^k the recursion reads r -> 3*(r - p)/2 + p; the factor 3
  pushes the unknown start residue up one 3-adic digit per step, so after k
  steps it is annihilated mod 3^k.  Same statement mod 5^k for Fenrir.
  COROLLARY (why bounded invariants are blind here): any congruence
  invariant of the value alone carries only a bounded window of branch
  history — while halting depends on the *cumulative count* of branches.
  A congruence on n can therefore never decide the walk's absorption:
  the 3-adic side of n stores the past, the 2-adic side decides the
  future, and the halting condition lives in neither.

T3 (exact acceleration).  H^s(2^s t) = 3^s t, so a maximal even run
  collapses to one jump with certificate s; an orbit is a sequence of
  blocks (one odd step, then v even steps) with per-block walk increment
  +2 - v (Hydra's b) or 2v - 1 (Antihydra's a).

T4 (the walk model, rigorous about itself).  If the walk takes +2 or -1
  with probability 1/2 each, the probability of ever reaching -1 from
  height 0 is the root in (0,1) of  q = (1 + q^3)/2, i.e.
      q = (sqrt(5) - 1)/2  (golden-ratio conjugate, ~0.6180),
  and from height h it is q^(h+1).  This is the constant behind the wiki's
  "probviously non-halting" verdicts for the family, and it is exact for
  the model — the open question is only whether the parity stream justifies
  the model (the single-orbit gap).
"""
from hydra import Hstep, hydra_step, antihydra_step, fenrir_step, HALT
import random


def mem3(parities, k):
    M = 3 ** k
    inv2 = pow(2, -1, M)
    r = 0
    for p in parities:
        r = (3 * ((r - p) * inv2) + p) % M
    return r


def blocks(n, nblocks):
    """T3 batch runner: yields (v, odd_part_step) per block from odd n."""
    out = []
    for _ in range(nblocks):
        assert n & 1
        m = Hstep(n)                       # the odd step
        v = (m & -m).bit_length() - 1      # 2-adic valuation
        n = 3 ** v * (m >> v)              # v even steps at once (T3)
        out.append(v)
    return n, out


if __name__ == "__main__":
    rng = random.Random(0)

    # ---- T1: value increase, incl. Fenrir small cases ----
    assert all(Hstep(n) > n for n in range(2, 100000))
    fy = lambda y: 5 * (y // 2) + (2 if y % 2 == 0 else 0)
    assert all(fy(y) > y for y in range(2, 100000))
    assert fy(0) == 2 and fy(1) == 0 and fy(fy(1)) == 2      # 1 -> 0 -> 2 escape
    print("T1  value strictly increases (n >= 2); family cannot cycle: OK")

    # ---- T2: q-adic memory ----
    bad = 0
    for _ in range(30000):
        n = rng.randint(2, 10 ** 12)
        k = rng.randint(1, 8)
        ps = []
        for _ in range(k):
            ps.append(n & 1)
            n = Hstep(n)
        if n % 3 ** k != mem3(ps, k):
            bad += 1
    assert bad == 0
    print("T2  n mod 3^k = function of last k parities: 30,000 checks OK")

    # ---- T3: acceleration + block equivalence ----
    for _ in range(2000):
        s = rng.randint(1, 40)
        t = rng.randint(1, 10 ** 9)
        n = (1 << s) * t
        for _ in range(s):
            n = Hstep(n)
        assert n == 3 ** s * t
    n0 = 9
    nb, vs = blocks(n0, 200)
    n = n0
    for _ in range(200 + sum(vs)):
        n = Hstep(n)
    assert n == nb
    print("T3  H^s(2^s t) = 3^s t and block runner vs single steps: OK")

    # ---- T4: the ruin constant, by exact truncated recursion ----
    # P_h = prob of reaching -1 from height h with steps -1/+2 (p = 1/2):
    # solve on 0..N with absorbing tail approximations from both sides.
    # The ruin probability is the MINIMAL non-negative solution of
    # P_h = (P_{h-1} + P_{h+2})/2 with P_{-1} = 1 (standard hitting-
    # probability theory); iterating from all-zeros converges to it.
    q = (5 ** 0.5 - 1) / 2
    N = 4000
    lo = [0.0] * (N + 3)
    for _ in range(20000):
        for h in range(N, -1, -1):
            lo[h] = 0.5 * (1.0 if h == 0 else lo[h - 1]) + 0.5 * lo[h + 2]
    assert abs(lo[0] - q) < 1e-6, lo[0]
    assert abs(q ** 3 - 2 * q + 1) < 1e-12
    assert all(abs(lo[h] - q ** (h + 1)) < 1e-5 for h in range(0, 40))
    print(f"T4  ruin prob from height h = q^(h+1), q = (sqrt5-1)/2 = {q:.6f} "
          f"(minimal-solution iteration: {lo[0]:.7f}): OK")

    # ---- measurements: valuation distribution (P4) and drift ----
    n = 9
    from collections import Counter
    cnt = Counter()
    T = 200000
    for _ in range(T):
        m = Hstep(n)
        v = (m & -m).bit_length() - 1 if m else 0
        n = 3 ** v * (m >> v)
        cnt[v] += 1
    tot = sum(cnt.values())
    print("P4  block valuation distribution vs Geom(1/2):")
    for v in range(7):
        print(f"      v={v}: {cnt[v]/tot:.4f}   2^-(v+1) = {2**-(v+1):.4f}")
    Ev = sum(v * c for v, c in cnt.items()) / tot
    print(f"      E[v] = {Ev:.4f} (model: 1); Antihydra drift/block = "
          f"{2*Ev-1:.3f} (model: +1)")
