"""Closing (and obstructing) two of the gaps between this machine and Collatz.

The scorecard in Section 9.3 lists two items as merely EMPIRICAL for this
machine where Collatz has more:
  (E) "F expands, never shrinks"            -- measured, not proved
  (B) "proved structural backbone"          -- Collatz has 2-adic ergodicity
                                               + Tao; this machine has none.
This file settles what can be settled.

--------------------------------------------------------------------------
RESULT 1 (E is PROVED on the dominant word, with an exact margin).

On the dominant branch word w = (R25^n, R23),
        F(D) = 16D - 240*2^n + 32n + 169,      n = n_A(1, D).
Write D = 16*2^n + delta.  Then

        F(D) - D = 15*delta + 32n + 169.                              (1)

The exit row R23 fires only while its guard 15d > 18b + 61 holds, and after
n cascade-A rounds b = 5*2^n - 4, d = 6*2^n + delta + 10 + 2n, so

        15d - (18b + 61) = 15*delta + 30n + 161 > 0.                  (2)

Substituting (2) into (1):  F(D) - D > (-30n - 161) + 32n + 169 = 2n + 8 > 0,
and since delta is an integer the minimum is attained at delta = -(2n+10):

        F(D) - D  >=  2n + 19        (attained at D = 16*2^n - (2n+10)).

So the dominant word CANNOT contract -- and only just: the guard fails
exactly 11 units before the contraction region begins.  This also explains
the observed minimum ratio tending to 1 from above: the margin 2n+19 grows
logarithmically while D grows exponentially.

--------------------------------------------------------------------------
RESULT 2 (B is not missing but OBSTRUCTED: the 2-adic route is closed).

Collatz's backbone exists because its branch is chosen by n mod 2 -- LOW
order, 2-adic data -- so the map extends continuously to Z_2 and carries an
ergodic measure.  This machine's branch count is

        n_A(1, D) = bits(D) - 4 + (offset in {-1, 0} fixed by the mantissa),

an ARCHIMEDEAN (leading-digit) function.  Agreeing on any number of low bits
therefore says nothing about the branch, and continuity fails at every level:

  Theorem.  For every N there are D = D' (mod 2^N) with F(D) != F(D') (mod 32).
  Construction: near base = 16*2^n the exit guard flips at delta = -(2n+10), so
      D' = base - (2n+11)      (word has switched)
      D  = D' + 2^N            (back in the dominant word)
  agree mod 2^N and land in different words, giving 9 vs 25 mod 32.

Hence F has NO continuous extension to Z_2: the Collatz 2-adic ergodicity
argument provably cannot be transplanted.  The missing backbone is an
obstruction, not an oversight.

--------------------------------------------------------------------------
RESULT 3 (the natural replacement, and why the naive form of it is FALSE).

If the branch is Archimedean, the right analogue of the 2-adic circle is the
mantissa circle frac(log2 D).  But the orbit's mantissa is NOT uniformly
equidistributed (chi-square ~162 on 20 bins over 20,000 cycles, vs ~30 at
95%).  So a backbone for F would have to identify the actual, non-uniform
stationary density on the mantissa circle -- the naive "equidistributes"
statement is false.  That is the concrete target a future proof must hit.
"""
import math
from onedim import F, n_A


def frac_log2(D):
    """frac(log2 D) for arbitrarily large integers, via the leading bits."""
    bl = D.bit_length()
    top = D >> max(0, bl - 64)
    return (math.log2(top) + (bl - top.bit_length()) - (bl - 1)) % 1.0


if __name__ == "__main__":
    import random

    # ---- RESULT 1: the exact margin on the dominant word ----
    for n in range(6, 40):
        D = 16 * (1 << n) - (2 * n + 10)
        assert n_A(1, D) == n
        assert F(D)[0] - D == 2 * n + 19, n
        b, d = 5 * (1 << n) - 4, 6 * (1 << n) - (2 * n + 10) + 10 + 2 * n
        assert 15 * d - (18 * b + 61) == 11          # guard margin, exactly 11
    print("R1: dominant word margin F(D)-D = 2n+19 > 0 verified for n = 6..39")

    # no contraction anywhere we can reach
    rng = random.Random(0)
    worst, tested = (None, None), 0
    for _ in range(60000):
        D = rng.randint(8, 10 ** rng.randint(1, 18))
        try:
            D2 = F(D)[0]
        except RuntimeError:
            continue
        tested += 1
        assert D2 > D, ("CONTRACTION", D)
        if worst[0] is None or D2 - D < worst[0]:
            worst = (D2 - D, D)
    print(f"R1: no contraction in {tested} random D across 18 magnitudes "
          f"(smallest gain {worst[0]} at D={worst[1]})")

    # ---- RESULT 2: 2-adic discontinuity at every level ----
    for N in (5, 16, 32, 64, 96, 128):
        n = N + 25
        base = 16 * (1 << n)
        DB = base - (2 * n + 11)
        DA = DB + (1 << N)
        assert (DA - DB) % (1 << N) == 0
        assert F(DA)[0] % 32 != F(DB)[0] % 32, N
    print("R2: 2-adic discontinuity witnesses constructed for N up to 2^128")

    # ---- RESULT 3: the mantissa is not uniform ----
    D, vals = 17, []
    for _ in range(20000):
        vals.append(frac_log2(D))
        D = F(D)[0]
    B = 20
    bins = [0] * B
    for v in vals:
        bins[min(B - 1, int(v * B))] += 1
    exp = len(vals) / B
    chi2 = sum((c - exp) ** 2 / exp for c in bins)
    assert chi2 > 30.1
    print(f"R3: mantissa NOT uniform (chi-square {chi2:.1f} >> 30.1 crit) "
          f"-> naive Archimedean equidistribution is false")
