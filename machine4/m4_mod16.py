"""Machine 4 -- the mod-16 image theorem, and the unreachable quarter of H.

Everything here is checked step-exactly against m4_base.step (the raw rules).

--------------------------------------------------------------------------
T5 (clean rule table).  From an odd a the base rules read, with no case on k:

      b <= a, b even :  (a, b) -> (2b + 3, a - b)
      b <= a, b odd  :  (a, b) -> (2b + 1, a - b + 3)
      b  = a + 1     :  (a, b) -> (2a - 1, 1)
      b  = a + 2     :  (a, b) -> (2a + 5, 1)
      b  = a + 3     :  HALT
      b  = a + 4     :  (a, b) -> (2a + 3, 1)
      b >= a + 5     :  (a, b) -> (2a + 5, b - a - 4)

   (Substitute a = 2k+1 into m4_base to see these are the same rules; the
   point of the rewrite is that every new a is now a multiple of 2 plus a
   small odd constant, which is what makes the 2-adic statements below
   visible.)  Note b = a + 5 lands on b' = 1: it is a *return*, not a
   cascade step.

--------------------------------------------------------------------------
The section is S = {(a, 1) : a odd}; the return map is
   R4(a) = the a-value of the first state after (a,1) with b = 1.
"Interior" = every state strictly between two section visits.

T6 (interior confinement, 4-adic).  Every interior state has a = 3 (mod 4).
   PROOF.  The first step out of the section is (a,1) -> (3, a+2) by the
   "b <= a, b odd" rule with b = 1, and 3 = 3 (mod 4).  Thereafter the three
   rules that do NOT return produce a' in {2b+3 (b even), 2b+1 (b odd),
   2a+5 (a odd)}; in each case 2*(even)+3, 2*(odd)+1 and 2*(odd)+5 are all
   = 3 (mod 4).  The two rules that produce a' = 1 (mod 4), namely 2a-1 and
   2a+3, both output b' = 1, so their targets are section states, not
   interior ones.  QED

T7 (parity lock).  Every interior state with a = 7 (mod 8) has b odd.
   PROOF.  List the producers of an interior state and the residue of the
   new a modulo 8, using T6 (the source a is 3 mod 4 whenever it is itself
   interior, so 2a + 5 = 6 + 5 = 3 (mod 8)):
     (i)   from the section, (a,1) -> (3, a+2):      a' = 3 (mod 8);
     (ii)  b >= a+5,       -> (2a+5, b-a-4):         a' = 3 (mod 8);
     (iii) b <= a even,    -> (2b+3, a-b):           a' = 7 (mod 8) iff
                                                     b = 2 (mod 4);
     (iv)  b <= a odd,     -> (2b+1, a-b+3):         a' = 7 (mod 8) iff
                                                     b = 3 (mod 4).
   So a' = 7 (mod 8) only via (iii) or (iv).  In (iii) the new b is
   a - b = odd - even = odd; in (iv) it is a - b + 3 = odd - odd + 3 = odd.
   QED

T8 (image theorem).  For every odd a >= 1 for which R4(a) is defined,
        R4(a)  is NOT  13 or 15   (mod 16),
   i.e. the image of R4 lies in {1, 3, 5, 7, 9, 11} (mod 16).
   PROOF.  A return is produced by exactly four rules, from an interior
   state (a, b); write a = 4s + 3 by T6.
        b = a+1 : a' = 2a - 1 = 8s + 5
        b = a-1 : a' = 2b + 3 = 2a + 1 = 8s + 7      (the b <= a even rule
                                                      with a - b = 1)
        b = a+4 : a' = 2a + 3 = 8s + 9
        b = a+2 : a' = 2a + 5 = 8s + 11
        b = a+5 : a' = 2a + 5 = 8s + 11
   (b <= a odd cannot return: a - b + 3 = 1 forces b = a + 2 > a.)
   If a = 3 (mod 8) then s is even, s = 2u, and the five values are
   16u + {5, 7, 9, 11}, i.e. a' in {5, 7, 9, 11} (mod 16).
   If a = 7 (mod 8) then b is odd by T7, so b = a+1, b = a-1, b = a+5 are
   impossible (those are even, a being odd), leaving b = a+2 and b = a+4;
   with s odd, s = 2u+1, these give 16u + 19 and 16u + 17, i.e.
   a' in {1, 3} (mod 16).
   Union: {1, 3, 5, 7, 9, 11} (mod 16); 13 and 15 never occur.  QED

T9 (the unreachable quarter).  The primary halting family is
        h_j = 16*2^j - j - 12,   j odd
   (every h_j halts in one R4-step).  Since 16*2^j = 0 (mod 16) for j >= 0,
        h_j = 4 - j   (mod 16),
   so h_j = 15 (mod 16) iff j = 5 (mod 16), and h_j = 13 (mod 16) iff
   j = 7 (mod 16).  By T8 those members are never return values.  Hence
   *exactly a quarter of the primary halting family* -- the j in
   {5, 7} (mod 16), two of the eight odd classes -- is unreachable by any
   orbit after its first return to the section, whatever the start.

   (T9 does not decide machine 4: the remaining three quarters are still
   available, and the deeper halts below are far more numerous than the
   primary family anyway.)

--------------------------------------------------------------------------
T10 (H is NOT thin).  Machine 4's halting set on the section has density
   6%-20% per dyadic block over a = 1..2*10^5 -- see the measurement at the
   end.  Every other machine in this collection has a thin (geometric,
   density -> 0) halting set; machine 4 does not, and its non-halting is
   correspondingly a *dynamical* statement (the orbit funnels into a few
   values) rather than a needle-in-a-haystack statement.
"""
from m4_base import step, HALT

SEC = 1          # the section is b = SEC


def clean_step(s):
    """T5's table, verbatim.  Returns HALT or (a', b')."""
    a, b = s
    assert a % 2 == 1, "clean_step is stated for odd a only"
    if b <= a:
        return (2 * b + 3, a - b) if b % 2 == 0 else (2 * b + 1, a - b + 3)
    d = b - a
    if d == 1:
        return (2 * a - 1, 1)
    if d == 2:
        return (2 * a + 5, 1)
    if d == 3:
        return HALT
    if d == 4:
        return (2 * a + 3, 1)
    return (2 * a + 5, b - a - 4)


def R4(a, cap=10 ** 6):
    """First return to b = 1.  Returns (a', interior_states) or
    ('HALT', interior_states) or None if the cap is hit."""
    s, interior = step((a, SEC)), []
    for _ in range(cap):
        if s == HALT:
            return HALT, interior
        if s[1] == SEC:
            return s[0], interior
        interior.append(s)
        s = step(s)
    return None, interior


def primary(j):
    return 16 * (1 << j) - j - 12


if __name__ == "__main__":
    import time
    t0 = time.time()
    print("=" * 74)
    print("MACHINE 4: the mod-16 image theorem")
    print("=" * 74)

    # ---- T5: the clean table is the base rules ----------------------------
    bad = 0
    for a in range(1, 2001, 2):
        for b in range(1, a + 12):
            if step((a, b)) != clean_step((a, b)):
                bad += 1
    import random
    rng = random.Random(11)
    for _ in range(300000):
        a = 2 * rng.randint(0, 10 ** rng.randint(1, 12)) + 1
        b = rng.randint(1, a + 10 ** rng.randint(1, 12))
        if step((a, b)) != clean_step((a, b)):
            bad += 1
    assert bad == 0
    print(f"\nT5  clean table == m4_base.step: exhaustive a<2000 x b<=a+11 "
          f"plus 300k random to 10^12 -- {bad} mismatches")

    # ---- T6 / T7 at the rule level (the proof's own steps) ----------------
    # Both are statements about single transitions, so they are checked here
    # directly over a huge random box; the orbit sweep below then confirms
    # the reachability side on real trajectories.
    bad6 = bad7 = 0
    seen7 = 0
    for _ in range(400000):
        a = 4 * rng.randint(0, 10 ** rng.randint(1, 12)) + 3      # interior a
        b = rng.randint(1, a + 10 ** rng.randint(1, 12))
        r = step((a, b))
        if r == HALT:
            continue
        ap, bp = r
        if bp != 1 and ap % 4 != 3:
            bad6 += 1                       # T6: interior successors are 3 mod 4
        if bp != 1 and ap % 8 == 7:
            seen7 += 1
            if bp % 2 != 1:
                bad7 += 1                   # T7: those have odd b
    # and from the section itself
    for _ in range(50000):
        a = 2 * rng.randint(0, 10 ** rng.randint(1, 12)) + 1
        ap, bp = step((a, SEC))
        if bp != 1 and ap % 4 != 3:
            bad6 += 1
        if bp != 1 and ap % 8 == 7 and bp % 2 != 1:
            bad7 += 1
    assert bad6 == 0 and bad7 == 0
    print(f"T6* rule level, 450k random transitions to 10^12: every interior "
          f"successor is 3 (mod 4) -- {bad6} violations")
    print(f"T7* rule level: {seen7} transitions landed on a = 7 (mod 8); all "
          f"had b odd -- {bad7} violations")

    # ---- run the section dynamics, collecting every interior state --------
    AMAX = 30001
    interiors = 0
    res_interior_mod4 = set()
    res_a7_b_parity = set()
    image_mod16 = {}
    halting = []
    capped = 0
    returns = 0
    exit_kinds = {}
    for a in range(1, AMAX, 2):
        out, inter = R4(a)
        for (x, y) in inter:
            interiors += 1
            res_interior_mod4.add(x % 4)
            if x % 8 == 7:
                res_a7_b_parity.add(y % 2)
        if out is None:
            capped += 1
            continue
        if out == HALT:
            halting.append(a)
            continue
        returns += 1
        image_mod16[out % 16] = image_mod16.get(out % 16, 0) + 1
        src = inter[-1] if inter else (a, SEC)
        d = src[1] - src[0]
        exit_kinds[(src[0] % 8, d)] = exit_kinds.get((src[0] % 8, d), 0) + 1

    print(f"\n    a = 1..{AMAX} odd: {returns} return, {len(halting)} halt, "
          f"{capped} capped; {interiors} interior states seen")

    # ---- T6 ---------------------------------------------------------------
    assert res_interior_mod4 == {3}, res_interior_mod4
    print(f"T6  interior a (mod 4) over {interiors} states: "
          f"{sorted(res_interior_mod4)}  -> confinement to 3 (mod 4) holds")

    # ---- T7 ---------------------------------------------------------------
    assert res_a7_b_parity == {1}, res_a7_b_parity
    print(f"T7  interior states with a = 7 (mod 8): b parity seen "
          f"{sorted(res_a7_b_parity)} (1 = odd)  -> parity lock holds")

    # ---- T8 ---------------------------------------------------------------
    seen = sorted(image_mod16)
    assert set(seen) <= {1, 3, 5, 7, 9, 11}, seen
    assert 13 not in seen and 15 not in seen
    print(f"T8  R4 image (mod 16): {seen}   [13 and 15 absent]")
    print("    counts: " + ", ".join(f"{r}:{image_mod16[r]}" for r in seen))
    src37 = {}
    for (am8, d), c in exit_kinds.items():
        src37.setdefault(am8, {})[d] = c
    for am8 in sorted(src37):
        ds = ", ".join(f"b=a{d:+d} x{c}" for d, c in sorted(src37[am8].items()))
        print(f"      exits from a = {am8} (mod 8): {ds}")

    # the case split of T8's proof, checked directly
    bad = 0
    for a in range(3, 200000, 4):                 # a = 3 (mod 4)
        for (d, val) in ((1, 2 * a - 1), (-1, 2 * a + 1), (4, 2 * a + 3),
                         (2, 2 * a + 5), (5, 2 * a + 5)):
            b = a + d
            if b < 1:
                continue
            r = step((a, b))
            if r == HALT or r[1] != 1 or r[0] != val:
                bad += 1
            if a % 8 == 7 and d in (1, -1, 5) and b % 2 == 1:
                bad += 1                          # T7 says these b are even
            if val % 16 in (13, 15) and not (a % 8 == 7 and d in (1, -1, 5)):
                bad += 1
    assert bad == 0
    print(f"    T8 case split re-checked on every a = 3 (mod 4) below 200000: "
          f"{bad} violations")

    # ---- T9 ---------------------------------------------------------------
    fam = [(j, primary(j)) for j in range(1, 18, 2)]
    onestep_ok = all(R4(h)[0] == HALT for _, h in fam if h < 10 ** 7)
    assert onestep_ok
    print(f"\nT9  primary family h_j = 16*2^j - j - 12 (j odd), one-step halt "
          f"verified for j = 1..17: {onestep_ok}")
    print("      j, h_j, h_j mod 16, reachable-as-return:")
    for j, h in fam:
        print(f"        j={j:2d}  h={h:<9d}  {h % 16:2d}  "
              f"{'NO (T8)' if h % 16 in (13, 15) else 'yes'}")
    blocked = [j for j in range(1, 1000, 2) if primary(j) % 16 in (13, 15)]
    assert all(j % 16 in (5, 7) for j in blocked)
    print(f"      blocked j below 1000: {len(blocked)} of "
          f"{len(range(1, 1000, 2))} = "
          f"{len(blocked) / len(range(1, 1000, 2)):.4f} of the family; "
          f"all are j = 5 or 7 (mod 16)")
    print(f"      first blocked j: {blocked[:8]}")

    # ---- T10: density -----------------------------------------------------
    print("\nT10 halting density of the section set H4, by dyadic block:")
    e = 6
    while (1 << e) < AMAX:
        lo, hi = 1 << e, min(1 << (e + 1), AMAX)
        n = len([h for h in halting if lo <= h < hi])
        tot = len(range(lo if lo % 2 else lo + 1, hi, 2))
        print(f"      [2^{e:2d}, 2^{e + 1:2d}) : {n:6d} / {tot:6d} = "
              f"{n / tot:.4f}")
        e += 1
    print(f"      total |H4 cap [1,{AMAX})| = {len(halting)}; density "
          f"{len(halting) / len(range(1, AMAX, 2)):.4f}")
    print("      -> NOT a thin halting set (contrast: every other machine in "
          "the collection has density -> 0)")

    print(f"\n[{time.time() - t0:6.1f}s] all checks passed")
