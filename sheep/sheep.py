"""The sheep machine -- a second cryptid inside the one-schema VAL(2) family.

THE OBJECT.  Turing machine  1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE,
a 6-state 2-symbol machine found by "sheep" on 7 April 2026 and listed as a
Cryptid on the bbchallenge wiki.  The wiki gives a halting-equivalent
one-variable reduction, quoted verbatim from
https://wiki.bbchallenge.org/wiki/1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE
(fetched 31 July 2026):

    f(n) = { HALT,                            for n = 2^i  <=> oddPart(n) = 1
           { n + v_2(n) + 3,                  for oddPart(n) = 3
           { n + v_2(n) + (oddPart(n)-1)/2,   for oddPart(n) > 3

    "Start at A(5)";  the open conjecture is  NOT exists k, f^k(5) = HALT.

The same page states two lemmas:

    even_case_no_pow2 : for even n with v_2(n) = a >= 2 and oddPart m >= 5,
                        m*2^a + a + (m-1)/2 is never a power of 2;
    oddPart3_no_pow2  : for any a, 3*2^a + a + 3 is never a power of 2.

WHY IT MATTERS TO THIS PROGRAM.  Until now the only cryptid inside our
interface was the Space Needle, and the whole theory had been developed
against that single point.  The sheep machine is the second, and it is the
Needle's sibling with beta changed from 3 to 1 -- which is exactly the
parameter the program's "rank of the sieve group" dichotomy says should
decide whether the last-step sieve closes.  It closes.  That prediction was
made before we looked, and the wiki's own lemma is the special case.

--------------------------------------------------------------------------
S1  (identification; proved).  Write n = 2^v * m, m odd, m = 2k+1.  For the
    GENERIC branch (m > 3, i.e. k >= 2),

        f(n) = n + v + (m-1)/2 = 2^v(2k+1) + v + k = A_v k + B_v
        with  A_v = 2^(v+1) + 1,   B_v = 2^v + v,

    which is census member (alpha, beta, gamma, delta, epsilon) =
    (1, 1, 1, 1, 0).  The Space Needle's reduction is (1, 3, 1, 1, 0): the
    two machines differ in beta alone.  The m = 1 branch (HALT on powers of
    two) is the family's own halting rule, so the sheep machine is the
    census member PLUS one exceptional branch at m = 3.

S2  (the exception is the cryptid; proved).  Census member (1,1,1,1,0) is
    recorded in the census as HALTING: from x = 3 it steps 3 -> 4 = 2^2.
    The sheep machine does not, because m = 3 is exactly the value the
    exceptional branch intercepts: f(3) = 3 + 0 + 3 = 6.  One extra branch
    on one residue converts a halting census member into an open problem.

S3  (last-step sieve; proved -- the wiki lemma with its threshold derived).
    A step from the generic branch v lands on a power of two iff
        2^t = A_v k + B_v  for some k >= 2,
    i.e. iff 2^t = B_v (mod A_v) is solvable, i.e. iff B_v lies in the
    subgroup <2> of (Z/A_v)^*.  Now A_v = 2^(v+1) + 1, so
        2^(v+1) = -1  (mod A_v)    and    2^{-1} = 2^v + 1  (mod A_v),
    whence B_v = 2^v + v = 2^{-1} - 1 + v and the condition becomes

        SIEVE:   2^(t+1) = 2v - 1   (mod 2^(v+1) + 1).

    Because 2^(v+1) = -1, the group <2> is contained in the LIST
        {2^i : 0 <= i <= v}  u  {A_v - 2^i : 0 <= i <= v},
    so the sieve is decidable by inspection:
      * 2v - 1 = 2^i forces i = 0 (2v-1 is odd), hence v = 1;
      * 2v - 1 = A_v - 2^i forces 2^i = 2^(v+1) - 2v + 2, which for v >= 3
        lies strictly between 2^v and 2^(v+1) (since 2^v > 2v - 2 and
        2v > 2) and so is not a power of two; v = 2 gives 6, not a power
        of two;
      * v = 0: A_0 = 3 and 2v - 1 = -1 = 2 = 2^1, which IS in <2>.
    THEREFORE only v = 0 and v = 1 can immediately precede a halt, and
    every v >= 2 is forbidden.  The wiki's even_case_no_pow2 is the v >= 2
    half; the threshold "a >= 2" there is a hypothesis, here it is the
    conclusion, and the two surviving branches are located at the same time.

S4  (the exceptional branch never halts either; proved).  3*2^a + a + 3 is
    never a power of two.  For a >= 3, a + 3 <= 2^a with equality never
    attained (2^a > a + 3 for a >= 3), so 3*2^a < 3*2^a + a + 3 < 2^(a+2);
    a = 0,1,2 give 6, 10, 17.  (This is the wiki's oddPart3_no_pow2.)

S5  (the halting set, in closed form; proved).  n halts in one step iff n is
    a power of two.  n reaches a power of two in exactly one step iff n lies
    in one of two geometric families:
        H_0 = { (2^(2j+1) + 1)/3 : j >= 2 }  =  11, 43, 171, 683, ...
              (v = 0: f(m) = (3m-1)/2 = 2^t, t = 2j even, t >= 4)
        H_1 = { 2*(2^(4j) - 1)/5 : j >= 2 }  =  102, 1638, 26214, ...
              (v = 1: f(2m) = (5m+1)/2 = 2^t, t = 4j-1, t >= 7)
    The excluded first members of each family (t = 2, giving m = 3; t = 3,
    giving m = 3) are precisely the ones the exceptional branch removes --
    S2 again.  So

        H = {2^i : i >= 0}  u  H_0  u  H_1,

    a complete and explicit description.  This is more than the Needle has:
    there the surviving branch set is infinite and only sieved to density
    ~0.71, and no closed form for H is available.

S6  (no congruence certificate; proved via T15, verified here).  beta = 1 is
    odd and delta = 1, so gcd(delta, M') = 1 at every modulus; T15 applies
    verbatim and no modulus separates the sheep machine's orbit from H.
    Verified below by direct closure computation for every M <= 200.

WHAT IS AND IS NOT SETTLED.  S3-S5 settle the *arithmetic* of the sheep
machine completely: we know exactly which values can halt.  What remains is
the same single-orbit avoidance question as for Collatz and for the Needle --
does the orbit of 5 ever land in H -- and S6 says the congruence method
cannot answer it.  The sheep machine is therefore a cryptid for which the
last-step analysis is CLOSED and the orbit question is open; the Needle is
one for which both are open.  That is the sharpest instance so far of the
program's rank-of-sieve-group dichotomy, on a machine we did not construct.
"""
import sys
from math import gcd

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/census")
from family import Machine, HALT                                  # noqa: E402

TM = "1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE"
START = 5
CENSUS_MEMBER = (1, 1, 1, 1, 0)


def v2(n):
    return (n & -n).bit_length() - 1


def f(n):
    """The wiki's reduction, transcribed literally."""
    v = v2(n)
    m = n >> v
    if m == 1:
        return HALT
    if m == 3:
        return n + v + 3
    return n + v + (m - 1) // 2


def is_pow2(n):
    return n > 0 and n & (n - 1) == 0


def sieve_target(v):
    """The residue 2v - 1 that must lie in <2> mod A_v (S3)."""
    return (2 * v - 1) % (2 ** (v + 1) + 1)


def group_of_2(A):
    """<2> as a subgroup of (Z/A)^*, or None if 2 is not invertible."""
    if gcd(2, A) != 1:
        return None
    g, x = {1 % A}, 2 % A
    while x not in g:
        g.add(x)
        x = (x * 2) % A
    return g


def survives(v):
    """Can branch v immediately precede a halt?  (S3's criterion.)"""
    A = 2 ** (v + 1) + 1
    return sieve_target(v) in group_of_2(A)


def halt_predecessors(bound):
    """Every n <= bound with f(n) a power of two (brute force ground truth)."""
    out = []
    for n in range(2, bound):
        y = f(n)
        if y is not HALT and is_pow2(y):
            out.append(n)
    return out


def H0(j):
    return (2 ** (2 * j + 1) + 1) // 3


def H1(j):
    return 2 * (2 ** (4 * j) - 1) // 5


# --------------------------------------------------------------------------
# S6: the congruence closure
# --------------------------------------------------------------------------

def closure_mod(M, x0, vmax=None):
    """Residues mod M reachable from x0 under the one-step over-approximation
    of f: for every v and every k mod M there is a genuine integer x with
    v_2(x) = v and (oddPart(x)-1)/2 = k (mod M), so the relation
        2^v (2k+1)  ->  A_v k + B_v      (generic, k >= 2)
        2^v * 3     ->  3*2^v + v + 3    (exceptional)
    is exactly the set of realizable residue edges."""
    if vmax is None:
        vmax = M.bit_length() + 2 * M
    edges = {}
    for v in range(vmax):
        p = pow(2, v, M)
        A = (pow(2, v + 1, M) + 1) % M
        B = (p + v) % M
        for k in range(M):
            src = (p * (2 * k + 1)) % M
            edges.setdefault(src, set()).add((A * k + B) % M)
        src3 = (3 * p) % M
        edges.setdefault(src3, set()).add((3 * p + v + 3) % M)
    seen = {x0 % M}
    frontier = [x0 % M]
    while frontier:
        nxt = []
        for c in frontier:
            for y in edges.get(c, ()):
                if y not in seen:
                    seen.add(y)
                    nxt.append(y)
        frontier = nxt
    return seen


def pow2_residues(M):
    s, x = set(), 1 % M
    while x not in s:
        s.add(x)
        x = (2 * x) % M
    return s


# --------------------------------------------------------------------------
if __name__ == "__main__":
    import time
    t0 = time.time()
    P = lambda *a: print(*a, flush=True)
    P("=" * 74)
    P(f"THE SHEEP MACHINE   {TM}")
    P(f"  discovered by sheep, 7 April 2026; start A({START})")
    P("=" * 74)

    mach = Machine(*CENSUS_MEMBER)

    # ---- S1 --------------------------------------------------------------
    bad = 0
    for v in range(0, 40):
        for k in range(2, 400):
            n = (1 << v) * (2 * k + 1)
            if f(n) != mach.A(v) * k + mach.B(v):
                bad += 1
    import random
    rng = random.Random(7)
    for _ in range(200000):
        v = rng.randrange(0, 200)
        k = rng.randrange(2, 10 ** rng.randint(1, 30))
        n = (1 << v) * (2 * k + 1)
        if f(n) != mach.A(v) * k + mach.B(v):
            bad += 1
    assert bad == 0
    P(f"\nS1  generic branch == census member {CENSUS_MEMBER}: "
      f"15,920 systematic + 200,000 random (v < 200, k < 10^30) -- "
      f"{bad} mismatches")
    P(f"      A_v = 2^(v+1) + 1, B_v = 2^v + v; the Space Needle is "
      f"(1,3,1,1,0) -- beta 3 vs 1 is the only difference")

    # every n: f agrees with the member except at oddPart 3
    diff = [n for n in range(2, 60000)
            if (f(n) is HALT) != (mach.step(n) is HALT)
            or (f(n) is not HALT and f(n) != mach.step(n))]
    assert all((n >> v2(n)) == 3 for n in diff), diff[:5]
    P(f"      f differs from the census member on exactly the "
      f"{len(diff)} values n < 60000 with oddPart(n) = 3, and nowhere else")

    # ---- S2 --------------------------------------------------------------
    P(f"\nS2  census member from x = 3: {mach.step(3)} = 2^2 -> "
      f"{mach.step(mach.step(3))}   (the census records it HALT)")
    P(f"      sheep machine from n = 3: {f(3)}  -- the exceptional branch "
      f"intercepts exactly this value")
    assert mach.step(3) == 4 and mach.step(4) is HALT and f(3) == 6

    # ---- S3 --------------------------------------------------------------
    surv = [v for v in range(0, 260) if survives(v)]
    P(f"\nS3  last-step sieve  2^(t+1) = 2v - 1 (mod 2^(v+1)+1):")
    P(f"      surviving branches with v < 260: {surv}")
    assert surv == [0, 1]
    # the proof's own case analysis, checked
    bad = 0
    for v in range(2, 4000):
        r = 2 ** (v + 1) - 2 * v + 2
        if is_pow2(r):
            bad += 1                       # "A_v - 2^i" case must never fire
        if is_pow2(2 * v - 1):
            bad += 1                       # "2^i" case: only v = 1
    assert bad == 0
    P(f"      proof steps re-checked for 2 <= v < 4000: 2^(v+1) - 2v + 2 is "
      f"never a power of two, and 2v - 1 never is -- {bad} violations")
    # ground truth: brute force the wiki lemma
    viol = [(v, m) for v in range(2, 14) for m in range(5, 20000, 2)
            if is_pow2(m * 2 ** v + v + (m - 1) // 2)]
    P(f"      brute force (wiki even_case_no_pow2), v = 2..13, m = 5..19999: "
      f"{len(viol)} counterexamples {viol}")
    assert viol == []

    # ---- S4 --------------------------------------------------------------
    viol = [a for a in range(0, 6000) if is_pow2(3 * 2 ** a + a + 3)]
    P(f"\nS4  oddPart-3 branch: 3*2^a + a + 3 a power of two for a < 6000? "
      f"{viol}")
    assert viol == []

    # ---- S5 --------------------------------------------------------------
    BOUND = 300000
    brute = halt_predecessors(BOUND)
    fam = ([H0(j) for j in range(2, 40) if H0(j) < BOUND]
           + [H1(j) for j in range(2, 40) if H1(j) < BOUND])
    pw = [1 << i for i in range(0, 40) if (1 << i) < BOUND]
    P(f"\nS5  halting set below {BOUND}")
    P(f"      brute force, f(n) a power of two: {brute}")
    P(f"      H_0 = {[H0(j) for j in range(2, 7)]} ...")
    P(f"      H_1 = {[H1(j) for j in range(2, 6)]} ...")
    assert sorted(brute) == sorted(fam), (sorted(brute), sorted(fam))
    P(f"      closed form matches brute force exactly ({len(fam)} members)")
    hb = [n for n in range(2, 20000) if f(n) is HALT]
    assert hb == [x for x in pw if 2 <= x < 20000]
    P(f"      immediate halts below 20000 = the powers of two: {hb}")

    # ---- S6 --------------------------------------------------------------
    P(f"\nS6  congruence certificates")
    sep = []
    for M in range(2, 201):
        cl = closure_mod(M, START)
        if cl.isdisjoint(pow2_residues(M)):
            sep.append(M)
        if M <= 24:
            P(f"      M = {M:3d}: |closure of 5| = {len(cl):3d} of {M:3d}"
              f"{'   (= Z_M)' if len(cl) == M else ''}")
    P(f"      separating moduli 2 <= M <= 200: {sep}")
    assert sep == []
    P(f"      consistent with T15 (beta = 1 odd, delta = 1): no modulus "
      f"separates the sheep machine")

    # ---- the orbit -------------------------------------------------------
    P(f"\nORBIT from {START}")
    n, seq, maxv, hit3, steps = START, [], 0, 0, 0
    NSTEP = 30000
    for i in range(NSTEP):
        v = v2(n)
        m = n >> v
        maxv = max(maxv, v)
        if m == 3:
            hit3 += 1
        if i < 12:
            seq.append(n)
        y = f(n)
        if y is HALT:
            break
        n = y
        steps = i + 1
    P(f"      first iterates: {seq}")
    P(f"      {steps} steps, no halt; n has {n.bit_length()} bits, "
      f"max v_2 seen = {maxv}, oddPart = 3 hit {hit3} times")
    P(f"      drift = {mach.drift():.6f} bits/step (member {CENSUS_MEMBER}); "
      f"observed {(n.bit_length() - START.bit_length()) / steps:.6f}")
    opp = 0
    n2 = START
    for _ in range(steps):
        if v2(n2) in (0, 1):
            opp += 1
        n2 = f(n2)
    P(f"      steps taken from a SURVIVING branch (v in {{0,1}}): {opp} of "
      f"{steps} = {opp / steps:.4f}  (predicted 3/4)")

    # ---- the heuristic, with the number actually computed -----------------
    # H has three geometric families, so |H cap [x, 2x]| is bounded; count it.
    b = n.bit_length()
    per_octave = (1.0                                   # one power of two
                  + 0.5                                 # H_0: ratio 4 per member
                  + 0.25)                               # H_1: ratio 16 per member
    d = mach.drift()
    # expected hits from here on: sum_j per_octave / x_j, x_j = 2^(b + d*j)
    from math import log10
    tail = per_octave / (1.0 - 2.0 ** (-d))
    log10_exp = log10(tail) - b * log10(2.0)
    P(f"\nHEURISTIC (not a proof)")
    P(f"      |H cap [x,2x]| ~ {per_octave} (1 power of two + 1/2 from H_0 "
      f"+ 1/4 from H_1)")
    P(f"      expected future hits from the current value (2^{b}) "
      f"= {tail:.4f} * sum_j 2^-(b + {d:.4f} j)")
    P(f"      = 10^({log10_exp:.1f})")
    P(f"      geometrically convergent, as for Collatz; and as for Collatz "
      f"the gap is single-orbit vs almost-everywhere")

    P(f"\n[{time.time() - t0:6.1f}s] all checks passed")
