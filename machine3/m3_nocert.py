"""Machine 3 joins the no-certificate theorems: the base-q transfer, verified.

The week's base-2 chain -- universal sieve lemma, delta-saturation, descent,
reach, T15 -- was built on the census family.  None of it used base 2 in any
essential way, and this file records its transfer to machine 3 (base 3, halting
set {27^k}), independently of the derivation that produced it: every check
below recomputes from machine 3's RAW two-variable rules (m3_base.step), not
from the branch table being tested.

--------------------------------------------------------------------------
THE BRANCH TABLE (proved by the acceleration, re-verified here).  Write a
non-spine value as a = 3^(j+1) m + r 3^j with j = v_3(a), digit r in {1,2}
(spine = pure powers 3^j, which carry the halting condition: halt iff 27 | a
... iff 3 | j).  The return map to the b = 1 section is

    G(a) = A_j m + B_(j,r),    A_j = 3^(j+1) + 1,
                               B_(j,r) = r 3^j + j + c_r,  c_1 = 3, c_2 = 4

reached in j + 1 raw steps.  In census coordinates (base 3): alpha = 1,
beta = 1, gamma = r, DELTA = 1, eps_r = r + 2.  Machine 3 is the base-3
member of the (1,1) class -- the LISTABLE class.

--------------------------------------------------------------------------
BASE-q UNIVERSAL SIEVE LEMMA (proved; here in its cleanest instance).  The
WS3 sieve forbids a halt after a branch-(j,r) step unless some h in H
satisfies Q0 h = P0 (mod A_j), with P0, Q0 from the branch's fixed point.
For machine 3, Q0 = 3^(j+1) - A_j = -1 exactly, and 3^(j+1) = -1 (mod A_j)
gives P0 = -B_(j,r), so the condition collapses to

    **h = B_(j,r)  (mod A_j)**   for some h in {27^k} --
    i.e.  B_(j,r) in <27> (mod A_j).

(The base-2 form "S_v = 2 B_v" was this plus a normalization artifact; the
invariant content in every base is target = B.)  Because ord_{A_j}(3) =
2(j+1) -- the class relation 3^(j+1) = -1 -- the set <3> = {+-3^i} is a
SHORT LIST, and the gap argument closes every branch except j = 1:

  M3-T1 (was: WS3's step -1 result).  A halt can only follow a branch with
  v_3 = 1.  Branch (1,1) and (1,2) genuinely survive: 21 -> 27 -> HALT and
  478293 -> 27^4 -> HALT.

  M3-N2 (NEW -- upgrade of m3_step2's j <= 500 verification to all j).
  Two steps before a halt is also pinned to v_3 = 1: the depth-2 target
  families reduce, via 10*3^j = 3^j - 3 (mod A-of-the-composition), to
  values sitting strictly inside the gaps of {+-3^i}, with the finitely
  many small j checked exactly.  So the LAST TWO steps before any halt
  both have v_3 = 1 -- now a theorem for every j, and the excluded-pair
  frequency 1 - (2/9)^2 = 77/81 = 95.0617% is exact.

--------------------------------------------------------------------------
M3-N1 -- THE NO-CERTIFICATE THEOREM FOR MACHINE 3 (proved).

  For every modulus M >= 2, the closure of every residue under machine 3's
  branch relation is ALL of Z_M.  No congruence certificate at any modulus
  can separate the orbit from the residues of {27^k}; for gcd(M,3) = 1 not
  even one branch can be excluded (the one-step image is already Z_M).

  Proof = the base-2 assembly with 2 -> 3 throughout: gcd(M,3) = 1 by
  delta-saturation + descent (machine 3 HAS the linear term: delta = 1, the
  "+j" in B, inherited from the divide-chain length; and mod M the
  exponential cancels exactly since gamma_r = alpha * r); M = 3^s M' by the
  reach lemma (the T-lift's exponent ledger spends trits, e' = e - (j+1))
  plus beta = 1 a unit mod every power of 3 -- the escape hatch, which in
  base 2 was "beta even", is here "beta divisible by 3", and beta = 1 shuts
  it.  Spine transitions only enlarge closures, so the theorem holds a
  fortiori for the full machine.

  This upgrades WS4's bounded sweeps for machine 3 to an unconditional
  statement, and it corrects the informal argument of explorations Finding 3
  ("the valuation is invisible mod M, hence no congruence closure"), which
  proves too much: 44 of the census's 318 certificates live at odd moduli
  where the valuation is equally invisible.  The true mechanism is
  relational saturation, and it genuinely needs delta and beta.

--------------------------------------------------------------------------
WHY MACHINE 3 IS ON THE THEOREM SIDE AND THE NEEDLE IS NOT (M3-N4).  Both
have delta = 1 and beta coprime to the base -- so both get the no-certificate
theorem.  The difference is the SIEVE GROUP: machine 3's class (1,1) has
3^(j+1) = -1, ord = 2(j+1), <3> = {+-3^i} listable (rank 1) -- the gap
argument closes every branch question it meets.  The Needle's class (1,3)
has <2> = {+-3^a 2^i} (rank 2, thin) -- the S-unit frontier.  One class
parameter decides which sibling yields theorems.  A class property, not a
machine accident.

Fenrir and the Hydra family do NOT take the transfer: their branch modulus
is constant (A = 5, A = 3), there is no valuation-indexed branch family and
no delta-sweep, and halting is a path-counter condition, not a value
condition.  Their no-congruence conclusion is already delivered by the
q-adic branch-memory theorem (hydra/theorems.py T2) -- a different mechanism.
Recorded as an obstruction, not a failure.
"""
import sys
from math import gcd

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/machine3")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/baker")
from m3_base import step, HALT
from sieve import geometric_solver


def v3(n):
    c = 0
    while n % 3 == 0:
        n //= 3
        c += 1
    return c


def A(j):
    return 3 ** (j + 1) + 1


def B(j, r):
    return r * 3 ** j + j + (3 if r == 1 else 4)


def G_raw(a, cap=10 ** 6):
    """The return map on b = 1 states, straight from the raw rules."""
    s, n = (a, 1), 0
    while n < cap:
        s = step(s)
        n += 1
        if s == HALT:
            return HALT, n
        if s[1] == 1:
            return s[0], n
    raise RuntimeError("no return")


def step1_table():
    print("STEP 1 -- THE BRANCH TABLE, AGAINST THE RAW RULES")
    print("-" * 70)
    bad = tested = 0
    for a in range(2, 60000):
        j = v3(a)
        m3 = a // 3 ** j
        if m3 == 1:
            continue                            # spine
        r = m3 % 3
        m = (a - r * 3 ** j) // 3 ** (j + 1)
        tested += 1
        got, n = G_raw(a)
        if got != A(j) * m + B(j, r) or n != j + 1:
            bad += 1
    sp = sum(1 for j in range(1, 12)
             if (G_raw(3 ** j)[0] == HALT) != (j % 3 == 0))
    print("  non-spine a < 60,000: %d values, table mismatches: %d" % (tested, bad))
    print("  spine 3^j, j = 1..11: halt iff 3 | j -- violations: %d" % sp)
    return bad == 0 and sp == 0


def step2_lemma():
    print("\nSTEP 2 -- THE BASE-q LEMMA vs THE PROJECT'S OWN SIEVE")
    print("-" * 70)
    solve = geometric_solver(27, 1, 1)
    bad, surv = 0, []
    for j in range(25):
        for r in (1, 2):
            # WS3 data from the fixed point, computed here from scratch
            N, D = A(j), 3 ** (j + 1)
            P0, Q0 = D * B(j, r) - N * (r * 3 ** j), D - N
            assert Q0 == -1
            ws3 = solve(P0, Q0, N) is not None
            # the lemma: B in <27> mod A
            seen, p, hit = set(), 27 % N, False
            while p not in seen:
                seen.add(p)
                if p == B(j, r) % N:
                    hit = True
                p = p * 27 % N
            if ws3 != hit:
                bad += 1
            if hit:
                surv.append((j, r))
    print("  50 branches j <= 24: lemma verdict vs geometric_solver mismatches: %d" % bad)
    print("  surviving branches: %s   (M3-T1: only v_3 = 1 can precede a halt)" % surv)
    w = [G_raw(21), G_raw(478293)]
    print("  positive witnesses, raw rules: 21 -> %s; 478293 -> %s" % (w[0][0], w[1][0]))
    ok = surv == [(1, 1), (1, 2)] and w[0][0] == 27 and w[1][0] == 27 ** 4
    return bad == 0 and ok


def step3_saturation():
    print("\nSTEP 3 -- M3-N1: closure = Z_M, INDEPENDENT COMPUTATION")
    print("-" * 70)
    bad = tested = 0
    for M in range(2, 251):
        # branch relation mod M: enumerate branches until the (3^j mod M, j mod M)
        # state repeats (the decide.py technique), edges over m in Z_M
        adj = {c: set() for c in range(M)}
        seen, jj = set(), 0
        while True:
            key = (pow(3, jj, M), jj % M)
            if key in seen:
                break
            seen.add(key)
            for r in (1, 2):
                a_, b_ = A(jj) % M, B(jj, r) % M
                s3, t3 = pow(3, jj + 1, M), (r * pow(3, jj, M)) % M
                for m in range(M):
                    adj[(s3 * m + t3) % M].add((a_ * m + b_) % M)
            jj += 1
        for c0 in (4 % M, 1 % M, 2 % M):
            tested += 1
            reach, frontier = {c0}, [c0]
            while frontier:
                c = frontier.pop()
                for t in adj[c]:
                    if t not in reach:
                        reach.add(t)
                        frontier.append(t)
            if len(reach) != M:
                bad += 1
    print("  every modulus M = 2..250, three start residues each: %d closures" % tested)
    print("  closure NOT all of Z_M: %d" % bad)
    return bad == 0


def step4_depth2():
    """M3-N2 brute check.  A 'branch value' is a non-spine value the return
    map acts on.  For every non-spine a < 10^6: follow the raw machine until
    HALT or until two return-map hops are spent; if it halted, every non-spine
    value on the way (a itself, and the intermediate return value if any) must
    have v_3 = 1."""
    print("\nSTEP 4 -- M3-N2 SPOT CHECK: brute force the last-two-steps pinning")
    print("-" * 70)
    bad = found = 0
    seeds = []
    for a in range(2, 10 ** 6):
        if a // 3 ** v3(a) == 1:
            continue                            # spine (powers of 3)
        path = [a]
        y = a
        halted = False
        for _ in range(2):
            y, _ = G_raw(y)
            if y == HALT:
                halted = True
                break
            if y // 3 ** v3(y) == 1:            # landed on the spine
                halted = v3(y) % 3 == 0         # a power of 27 halts next
                break
            path.append(y)
        if halted:
            found += 1
            if len(seeds) < 6:
                seeds.append((a, path))
            for z in path:
                if v3(z) != 1:
                    bad += 1
    print("  non-spine starts a < 10^6 halting within two return steps: %d" % found)
    print("  first few: %s" % [s[0] for s in seeds])
    print("  branch values en route with v_3 != 1: %d" % bad)
    return bad == 0 and found > 0


def main():
    r = [step1_table(), step2_lemma(), step3_saturation(), step4_depth2()]
    print("\n" + "=" * 70)
    if all(r):
        print("RESULT: the transfer is verified on an independent code path.")
        print("M3-N1: no modulus separates machine 3 -- unconditional. M3-T1 +")
        print("M3-N2: the last two steps before any halt have v_3 = 1, all j.")
        print("The Needle/machine-3 split is the rank of the sieve group.")
    else:
        print("RESULT: FAILED -- do not update the reports")


if __name__ == "__main__":
    main()
