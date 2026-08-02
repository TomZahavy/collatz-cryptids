"""The five unclaimed leads: four collapse to one lemma, and the lemma is proved.

BACKGROUND.  The census found seven undecided machines whose every branch is
sieved out to v = 200.  Two became T1 and T2; the other five were recorded as
"best open leads" and explicitly NOT claimed, because "forbidden to v = 200" is
not "forbidden for all v".  This file asks the follow-up: is the gap one hard
argument per machine, or one argument for several?

STEP 1 -- THEY ARE NOT FIVE PROBLEMS.  Four of the five have
A_v = 2^(v+2) - 1 identically: they are the whole alpha = 2, beta = -1 corner.
That is exactly T2's modulus, where ord_{A_v}(2) = v+2 makes the powers of two
the listable set {1, 2, 4, ..., 2^(v+1)}.  The other two do not transfer:
(2,1,1,2,-1) has A_v = 2^(v+2)+1 with ord = 2(v+2), twice as many powers to
exclude, and (3,3,2,0,1) has A_v = 3(2^(v+1)+1) with a v-dependent order
(4, 18, 8, 30, 12, 42, ...) -- no listable set at all.

STEP 2 -- THE LEMMA (proved).  On branch v the WS3 sieve forbids a halt unless
Q0 * 2^e = P0 (mod A_v), where P0/Q0 is the branch's affine fixed point.  Since
multiplying by a unit power of two is free, write the condition as
2^e = S_v (mod A_v) with S_v := 2 * P0 * Q0^{-1}.  For alpha = 2, beta = -1:

    the fixed point of x -> (A_v x + (2 B_v - A_v) 2^v) / 2^(v+1) is
        star = (2 B_v - A_v) 2^v / (1 - 2^(v+1)),   so
        P0 = (2 B_v - A_v) 2^v,   Q0 = 1 - 2^(v+1)

    A_v = 2^(v+2) - 1  =>  2^(v+2) = 1  =>  2^(v+1) = 2^{-1}  (mod A_v)
    =>  Q0 = 1 - 2^{-1} = 2^{-1}
    =>  P0 * Q0^{-1} = 2 P0 = (2 B_v - A_v) 2^(v+1) = (2 B_v - A_v) 2^{-1}
    =>  S_v = 2 * that = 2 B_v - A_v = 2 B_v          (mod A_v)

    **S_v = 2 B_v (mod A_v).**   Verified below: 0 mismatches on all 45
    machines of the alpha = 2, beta = -1 slice, every branch v = 0..400.

This is the derivation that the meta report's status board ranked as the next
step and labelled "routine algebra".  It was routine; it is done here.

STEP 3 -- THREE NEW THEOREMS (proved).  With B_v = gamma*2^v + delta*v + eps,

    2 B_v = gamma*2^(v+1) + 2*delta*v + 2*eps

and reducing with 2^(v+2) = 1 kills the leading term whenever gamma is even or
splits it when gamma is odd.  A branch is forbidden iff S_v avoids
{1, 2, ..., 2^(v+1)}; every member of that set except 1 is even, so **S_v odd
and > 1 suffices**, as does S_v = 0.  Machine by machine:

 T4.  (2,-1,2,2,1) never halts after its first step.
      B_v = 2^(v+1) + 2v + 1, so 2B_v = 2^(v+2) + 4v + 2 = 4v + 3 (mod A_v).
      For v >= 2: 4v+3 is odd, > 1, and < 2^(v+2) - 1, hence not a power of
      two.  v = 0: A_0 = 3, S_0 = 6 = 0, not in {1,2}.  v = 1: A_1 = 7,
      S_1 = 14 = 0, not in {1,2,4}.  Every branch forbidden.

 T5.  (2,-1,3,0,0) never halts after its first step.
      B_v = 3*2^v, so 2B_v = 3*2^(v+1) = 2^(v+2) + 2^(v+1) = 2^(v+1) + 1.
      For v >= 1: odd, > 1, and 2^(v+1) + 1 < 2^(v+2) - 1 since 2 < 2^(v+1).
      v = 0: A_0 = 3, S_0 = 6 = 0.  Every branch forbidden.

 T6.  (2,-1,3,1,0) never halts after its first step.
      B_v = 3*2^v + v, so 2B_v = 2^(v+1) + 2v + 1 (mod A_v).
      For v >= 2: odd, > 1, and < A_v since 2v + 2 < 2^(v+1).  v = 0 and v = 1
      both give S_v = 0.  Every branch forbidden.

NOTE ON THE STATEMENT -- this corrects T1 and T2 as originally written, too.
"Never halts from ANY start" is loose, and brute force catches it: a start that
is ITSELF a power of two halts at step 0, because that is the halting condition.
What "every branch is forbidden" actually gives is that no orbit reaches a power
of two after one or more steps.  So the powers of two are exactly the halting
starts of these machines, and they halt immediately.  Step 4 checks the
corrected statement directly (all non-power-of-two starts below 20,000, 400
steps: 0 halts on all five machines).

So three of the five leads are now claimed, on a proof rather than on a range
check.  The remaining two, (2,1,1,2,-1) and (3,3,2,0,1), stay open: their
modulus has no listable power-of-two set and the argument above has nothing to
stand on.

WHAT IS STILL ONLY MACHINE-VERIFIED: nothing in T4-T6.  The closed forms are
now derived from the lemma, and the checks below confirm the derivation rather
than substituting for it.
"""
import sys
from itertools import product

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/census")
from family import Machine

VMAX = 400

LEADS = [(2, -1, 2, 1, 1), (2, -1, 2, 2, 1), (2, -1, 3, 0, 0),
         (2, -1, 3, 1, 0), (2, 1, 1, 2, -1), (3, 3, 2, 0, 1)]

STATUS = {(2, -1, 2, 1, 1): "T2, proved earlier",
          (2, -1, 2, 2, 1): "T4, proved here",
          (2, -1, 3, 0, 0): "T5, proved here",
          (2, -1, 3, 1, 0): "T6, proved here"}

# closed forms DERIVED from the lemma S_v = 2 B_v, not fitted
DERIVED = {
    (2, -1, 2, 1, 1): ("2v + 3",           lambda v: 2 * v + 3),
    (2, -1, 2, 2, 1): ("4v + 3",           lambda v: 4 * v + 3),
    (2, -1, 3, 0, 0): ("2^(v+1) + 1",      lambda v: (1 << (v + 1)) + 1),
    (2, -1, 3, 1, 0): ("2^(v+1) + 2v + 1", lambda v: (1 << (v + 1)) + 2 * v + 1),
}

A_FORMS = {
    "2^(v+2) - 1":    lambda v: (1 << (v + 2)) - 1,
    "2^(v+2) + 1":    lambda v: (1 << (v + 2)) + 1,
    "3(2^(v+1) + 1)": lambda v: 3 * ((1 << (v + 1)) + 1),
}


def order_of_2(A):
    o, p = 1, 2 % A
    while p != 1:
        p, o = (p * 2) % A, o + 1
    return o


def target(mach, v):
    """S_v, or None where the sieve has no expanding fixed point on this branch."""
    data = mach.branch_sieve_data(v)
    if data is None:
        return None
    _, _, P, Q, _ = data
    A = mach.A(v)
    return (2 * (P * pow(Q, -1, A))) % A


def step1_which_leads_share_the_modulus():
    print("STEP 1 -- WHICH LEADS SHARE T2's MODULUS")
    print("-" * 74)
    print("%-16s %-16s %-24s %s"
          % ("machine", "A_v", "ord_{A_v}(2), v = 1..6", "status"))
    shared = []
    for t in LEADS:
        m = Machine(*t)
        name = next((n for n, f in A_FORMS.items()
                     if all(m.A(v) == f(v) for v in range(VMAX + 1))), "?")
        ords = [order_of_2(m.A(v)) for v in range(1, 7)]
        print("%-16s %-16s %-24s %s"
              % (str(t), name, str(ords), STATUS.get(t, "still open")))
        if name == "2^(v+2) - 1":
            shared.append(t)
    print("\nmachines with T2's modulus: %d of %d\n" % (len(shared), len(LEADS)))
    return shared


def step2_lemma():
    """S_v = 2 B_v (mod A_v) on the whole alpha=2, beta=-1 slice."""
    print("STEP 2 -- LEMMA:  S_v = 2 B_v  (mod A_v)  when alpha = 2, beta = -1")
    print("-" * 74)
    bad = tested = machines = 0
    for g, d, e in product((1, 2, 3), (0, 1, 2), (-2, -1, 0, 1, 2)):
        m = Machine(2, -1, g, d, e)
        machines += 1
        for v in range(VMAX + 1):
            S = target(m, v)
            if S is None:
                continue
            tested += 1
            if S != (2 * m.B(v)) % m.A(v):
                bad += 1
    print("  %d machines, %d branches tested (v = 0..%d)" % (machines, tested, VMAX))
    print("  mismatches: %d  ->  %s\n"
          % (bad, "lemma holds" if bad == 0 else "LEMMA FALSE -- stop"))
    return bad == 0


def step3_theorems(shared):
    print("STEP 3 -- THE DERIVED CLOSED FORMS, AND WHETHER EVERY BRANCH IS FORBIDDEN")
    print("-" * 74)
    print("%-16s %-20s %-12s %s"
          % ("machine", "S_v (derived)", "derivation", "branches not forbidden"))
    all_closed = True
    for t in shared:
        m = Machine(*t)
        name, f = DERIVED[t]
        mism, open_v, tested = 0, [], 0
        for v in range(VMAX + 1):
            S = target(m, v)
            if S is None:
                continue
            tested += 1
            A = m.A(v)
            if S != f(v) % A:
                mism += 1
            if S in {(1 << i) % A for i in range(v + 2)}:
                open_v.append(v)
        if open_v or mism:
            all_closed = False
        print("%-16s %-20s %-12s %s"
              % (str(t), name, "OK" if mism == 0 else "%d ERRORS" % mism,
                 open_v if open_v else "none (%d tested)" % tested))
    print()
    return all_closed


def step4_brute_force():
    """A proof that contradicts simulation is wrong.  Check all five any-start
    theorems directly -- and check the STATEMENT, which needs care: a start that
    is ITSELF a power of two halts at step 0 by definition, so the claim can only
    be that no orbit reaches a power of two after one or more steps."""
    print("STEP 4 -- BRUTE FORCE AGAINST THE THEOREMS")
    print("-" * 74)
    print("  claim: no orbit reaches a power of two after >= 1 step")
    print("  (starts that ARE powers of two halt at step 0 and are excluded)")
    named = {(1, 1, 2, 0, 1): "T1", (2, -1, 2, 1, 1): "T2",
             (2, -1, 2, 2, 1): "T4", (2, -1, 3, 0, 0): "T5",
             (2, -1, 3, 1, 0): "T6"}
    total = 0
    for t, nm in named.items():
        m, bad = Machine(*t), 0
        for x0 in range(2, 20000):
            if x0 & (x0 - 1) == 0:
                continue
            x = x0
            for _ in range(400):
                y = m.step(x)
                if y == "HALT":
                    bad += 1
                    break
                if y.bit_length() > 6000:
                    break
                x = y
        total += bad
        print("  %-3s %-16s starts 2..19999, 400 steps: halts = %d"
              % (nm, str(t), bad))
    print("  total counterexamples: %d\n" % total)
    return total == 0


def main():
    shared = step1_which_leads_share_the_modulus()
    lemma_ok = step2_lemma()
    closed = step3_theorems(shared)
    brute_ok = step4_brute_force()
    print("=" * 74)
    if lemma_ok and closed and brute_ok:
        print("RESULT: lemma verified; T4, T5, T6 proved -- three of the five")
        print("leads are now claimed, on a derivation and not on a range check.")
        print("Still open: (2,1,1,2,-1) and (3,3,2,0,1) -- their modulus has no")
        print("listable power-of-two set, so this argument has nothing to stand on.")
    else:
        print("RESULT: FAILED -- do not update the reports")


if __name__ == "__main__":
    main()
