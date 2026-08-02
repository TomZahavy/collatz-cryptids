"""The reach lemma: the last hypothesis falls, and the theorem is unconditional.

T14 (even_saturation.py) carried one verified-but-unproved hypothesis:

    (iv)  the R_M-closure of x0 contains some residue = 0 (mod 2^s)

-- "2-adic reach".  It was verified on 8,512 cases with 0 failures and left
standing as the honest boundary.  This file proves it, from beta odd alone, and
in a stronger form: not just some closure element, but the actual orbit of a
suitably chosen lift.

--------------------------------------------------------------------------
THE REACH LEMMA (proved).  Let a machine have beta odd and A_v > 0 for all v
(every odd-beta census member qualifies: A_0 = 2*alpha + beta >= 1 and A_v
increases).  Let M = 2^s M' with M' odd, and let c be ANY residue mod M.  Then
there is a lift x = c (mod M) whose F-orbit reaches a value = 0 (mod 2^s)
within at most s + 1 steps.  In particular the R_M-closure of every residue
contains a residue divisible by 2^s.

PROOF.  If c = 0 (mod 2^s) there is nothing to do, so let v0 = v_2(c mod 2^s)
< s.  Choose the lift

    x  =  c_int + 2^s M' T,        T a free non-negative integer,

where c_int is any fixed integer representative.  Every such lift has
v_2(x) = v0, and iterating F on x EXACTLY -- integers, not residues -- keeps
the T-dependence affine:

    y_n  =  p_n + q_n T,       q_n = A_{v_{n-1}} ... A_{v_0} * M' * 2^{e_n},

with the EXPONENT LEDGER

    e_1 = s - (v_0 + 1),       e_{n+1} = e_n - (v_n + 1).

Why: the step from y_n reads v_n = v_2(y_n) and forms k = (y_n - 2^{v_n}) /
2^{v_n+1}, which divides the T-coefficient by 2^{v_n+1}; multiplying by
A_{v_n} (odd) and adding B_{v_n} changes nothing 2-adically.  So each step
SPENDS v_n + 1 bits of the ledger -- the same precision accounting that the
confinement analysis met from the other side (rigidity.py: a confinement
certificate exhausts its precision; here the orbit exhausts the pin).

Now run the chain and watch two events, one of which must occur:

  DONE-EVENT at step n:  2^{e_n} | p_n  (in particular p_n = 0).  Then

      y_n = p_n + (odd * M') 2^{e_n} T  = 0 (mod 2^s)

  has a solution: T = -(p_n / 2^{e_n}) * (odd * M')^{-1}  (mod 2^{s - e_n}).
  Choose such a T, as large as desired.  The orbit of that lift hits
  0 (mod 2^s) at step n.

  LEDGER-EVENT: e_{n+1} = 0 with every earlier step not-done.  Then at step
  n + 1 the multiplier k = (y_n - 2^{v_n})/2^{v_n+1} has T-coefficient
  odd * M' * 2^0 -- a UNIT times T -- so as T varies, k mod 2^s takes every
  value; and A_{v_n} is odd (beta odd!), so y_{n+1} = A k + B takes every
  residue mod 2^s.  Choose T with y_{n+1} = 0 (mod 2^s).

  These are exhaustive: while not-done, v_2(p_n) < e_n, so v_n = v_2(y_n) =
  v_2(p_n) is T-INDEPENDENT (the T-term has the strictly larger valuation
  e_n), the branch sequence is well defined independently of T, and
  e_{n+1} = e_n - v_n - 1 >= 0 with strict decrease.  A quantity that starts
  at e_1 <= s - 1 and strictly decreases reaches 0 within s steps.

  Legitimacy of the chain: with T large, every y_n = p_n + q_n T is huge
  (q_n > 0 because A_v > 0), has v_2(y_n) = v_n < s, hence odd part > 1: no
  y_n halts en route, k >= 1 always, and every value is positive.  QED

WHERE beta ODD IS USED, exactly twice: the A's are odd, so (a) they never add
to the exponent ledger (the pin erodes at full speed), and (b) at the
ledger-event the free k is multiplied by a unit.  For beta EVEN both fail --
and must fail, because machines with even-modulus separating certificates are
exactly 2-adically confined.  The falsifier below exhibits this.

--------------------------------------------------------------------------
T15 -- THE NO-CERTIFICATE THEOREM, FINAL AND UNCONDITIONAL FORM (proved).

  Let a machine have beta odd, A_v > 0, and gcd(delta, M') = 1, where M' is
  the odd part of M.  Then the R_M-closure of every residue is ALL of Z_M:
  no modulus M separates, and no branch can be excluded.

  Assembly: M odd -- the descent lemma (descent.py) alone.  M = 2^s M' --
  the reach lemma supplies a closure element c0 = 0 (mod 2^s), and T14's
  argument (even_saturation.py) with the descent lemma on the M'-part gives
  everything from c0.

  COROLLARY (the Space Needle).  beta = 3 odd, delta = 1, A_v = 2^{v+1}+3 > 0:
  every hypothesis holds at every modulus.  **No modulus separates the Space
  Needle.**  No search bound, no arithmetic side condition, no reachability
  hypothesis.  The question "is there a congruence certificate for the
  Needle?", open since WS4 swept m <= 20,000, is closed: there is none, and
  the reason is delta = 1 and beta odd -- exactly the two parameters T3
  flagged from the census's first day.
"""
import random
import sys
from math import gcd

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/census")
from family import Machine
from even_saturation import closure, order2, v2, tup, ROWS

random.seed(30)


def v2i(n):
    c = 0
    while n % 2 == 0:
        n //= 2
        c += 1
    return c


def witness(mach, c_int, s, Mp):
    """Follow the proof's recipe.  Returns (T, n): the orbit of the lift
    x = c_int + 2^s*Mp*T reaches a value = 0 (mod 2^s) at step n <= s + 1.
    Raises AssertionError if the proof's bookkeeping is ever violated
    (it must not be)."""
    S = 1 << s
    p, q = c_int, S * Mp                        # y = p + q*T; y_0 = x
    for n in range(1, s + 3):
        e = v2i(q)                              # the exponent ledger
        v = v2i(p) if p else e                  # v2(0) := infinity, capped
        if v >= e:                              # DONE-EVENT: 2^e | p
            assert e < s, "done-event before any step was taken"
            u = q >> e                          # odd * M', a unit mod 2^(s-e)
            T = (-(p >> e) * pow(u, -1, S >> e)) % (S >> e) + (S >> e) * 7
            return T, n - 1                     # y_(n-1) = 0 (mod 2^s)
        # not-done: v < e, so v is T-independent; take one exact F-step
        A, B = mach.A(v), mach.B(v)
        assert A > 0
        assert (p - (1 << v)) % (1 << (v + 1)) == 0
        p = A * ((p - (1 << v)) >> (v + 1)) + B
        q = A * (q >> (v + 1))
        if v2i(q) == 0:                         # LEDGER-EVENT: q is now a unit
            T = (-p * pow(q, -1, S)) % S + S * 7
            return T, n                         # y_n = 0 (mod 2^s)
    raise AssertionError("recipe did not terminate within s+1 steps")


def orbit_hits(mach, x, s, cap):
    """Steps until the F-orbit of integer x hits = 0 (mod 2^s), or None."""
    S = 1 << s
    for n in range(cap + 1):
        if x % S == 0:
            return n
        y = mach.step(x)
        if y == "HALT" or y < 1:
            return None
        x = y
    return None


def step1_constructive():
    print("STEP 1 -- THE RECIPE, END TO END: build the witness, run the orbit")
    print("-" * 72)
    tested = fails = 0
    worst = 0
    while tested < 4000:
        t = (random.randint(1, 3), random.choice([-1, 1, 3, 5, 7]),
             random.randint(1, 3), random.randint(0, 2), random.randint(-2, 2))
        m = Machine(*t)
        if not m.well_defined(500):
            continue
        s = random.randint(1, 9)
        Mp = random.randrange(1, 40, 2)
        c = random.randrange((1 << s) * Mp)
        if c % (1 << s) == 0:
            continue                            # trivial case
        tested += 1
        try:
            T, n = witness(m, c, s, Mp)
            x = c + (1 << s) * Mp * T
            hit = orbit_hits(m, x, s, s + 1)
            if hit is None or hit > s + 1:
                fails += 1
            else:
                worst = max(worst, hit)
        except AssertionError as ex:
            fails += 1
            if fails < 4:
                print("  BOOKKEEPING VIOLATION:", t, "s=%d M'=%d c=%d" % (s, Mp, c), ex)
    print("  %d (beta-odd machine, M = 2^s M', residue) instances" % tested)
    print("  witness lift's orbit reached 0 (mod 2^s): all but %d" % fails)
    print("  deepest hit used %d steps (bound: s + 1 <= 10)" % worst)
    return fails == 0


def step2_ledger():
    print("\nSTEP 2 -- THE PROOF'S BOOKKEEPING, CHECKED IN ISOLATION")
    print("-" * 72)
    bad_led = bad_tind = n_ = 0
    while n_ < 3000:
        t = (random.randint(1, 3), random.choice([-1, 1, 3, 5, 7]),
             random.randint(1, 3), random.randint(0, 2), random.randint(-2, 2))
        m = Machine(*t)
        if not m.well_defined(500):
            continue
        s = random.randint(2, 9)
        Mp = random.randrange(1, 30, 2)
        c = random.randrange((1 << s) * Mp)
        if c % 2 == 0:
            c += 1                              # start at v0 = 0 for max depth
        n_ += 1
        # (a) e-ledger: e_{n+1} = e_n - (v_n + 1) on the T = 0 chain, vs the
        #     exact q_n valuation; (b) v_n is the same for T = 0 and T = 13.
        p0, q0 = c, (1 << s) * Mp
        pT = c + q0 * 13
        e = v2i(q0)
        for _ in range(s + 1):
            if p0 == 0 or v2i(p0) >= e:
                break
            v = v2i(p0)
            if v2i(pT) != v:
                bad_tind += 1
            A, B = m.A(v), m.B(v)
            p0 = A * ((p0 - (1 << v)) >> (v + 1)) + B
            pT = A * ((pT - (1 << v)) >> (v + 1)) + B
            q0 = A * (q0 >> (v + 1))
            e_next = e - (v + 1)
            if v2i(q0) != e_next:
                bad_led += 1
            e = e_next
            if e == 0:
                break
    print("  %d chains: ledger e_(n+1) = e_n - (v_n+1) violated %d times;"
          % (n_, bad_led))
    print("  branch valuations differed between T = 0 and T = 13: %d times"
          % bad_tind)
    return bad_led == 0 and bad_tind == 0


def step3_t15():
    print("\nSTEP 3 -- T15 END TO END: closure = Z_M for beta odd, gcd(delta,M')=1")
    print("-" * 72)
    tested = bad = 0
    for r in ROWS:
        t = tup(r)
        if t[1] % 2 == 0:
            continue
        for M in (4, 8, 16, 32, 12, 24, 48, 20, 40, 18, 36, 9, 27, 15, 45):
            s = v2(M) if M % 2 == 0 else 0
            Mp = M >> s
            if Mp > 1 and gcd(t[3], Mp) != 1:
                continue
            tested += 1
            if len(closure(Machine(*t), M)) != M:
                bad += 1
    print("  %d (beta-odd machine, modulus) pairs meeting T15's hypotheses" % tested)
    print("  closure was NOT all of Z_M: %d" % bad)
    needle = Machine(1, 3, 1, 1, 0)
    nb = sum(1 for M in range(2, 401) if len(closure(needle, M)) != M)
    print("  the Needle, every modulus 2..400: not-saturated count = %d" % nb)
    return bad == 0 and nb == 0


def step4_falsifier():
    print("\nSTEP 4 -- FALSIFIER: beta EVEN machines must be able to FAIL reach")
    print("-" * 72)
    # machines separated at an even modulus are 2-adically confined there:
    # their closure contains NO residue divisible by 2^s.  If reach held for
    # them too, the lemma's beta-odd hypothesis would be decoration.
    even_cert = [r for r in ROWS
                 if r["cong"] and int(r["cong"]) % 2 == 0
                 and tup(r)[1] % 2 == 0]
    confined = 0
    for r in even_cert[:40]:
        t, M = tup(r), int(r["cong"])
        s = v2(M)
        if not any(c % (1 << s) == 0 for c in closure(Machine(*t), M)):
            confined += 1
    print("  beta-even machines with an even-modulus certificate: %d tested"
          % min(40, len(even_cert)))
    print("  closure avoids 0 (mod 2^s) -- reach FAILS -- in %d of them" % confined)
    print("  (so the lemma's beta-odd hypothesis is load-bearing, not decoration)")
    return confined > 0


def main():
    r = [step1_constructive(), step2_ledger(), step3_t15(), step4_falsifier()]
    print("\n" + "=" * 72)
    if all(r):
        print("RESULT: the reach lemma is proved and its construction verified.")
        print("T15 -- beta odd, A_v > 0, gcd(delta, M') = 1 => NO modulus")
        print("separates, closure = Z_M always.  COROLLARY: no modulus separates")
        print("the Space Needle, with no hypotheses left. The theorem is done.")
    else:
        print("RESULT: FAILED -- do not update the reports")


if __name__ == "__main__":
    main()
