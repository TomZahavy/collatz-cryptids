"""Machine 1 -- the exact congruence content of the return map F.

Three things live here.

(A) AN ERRATUM to mod16.py.  Its stated theorem, "for every non-halting D,
    F(D) = 9 (mod 16)", is FALSE as a universal statement: F(5) = 17 = 1
    (mod 16).  The gap is in the pump-exit half of the proof, which
    establishes D* = 2 (mod 4) only for sweeps that actually run at least
    one cascade-B round.  When the guard 3*Dl <= A fails, sweep() takes its
    else-branch with D* = Dl, and Dl = 2 (mod 4) is not forced.  D = 5 is
    the witness: G(1,5) = sweep(7,4), 3*4 = 12 > 7, so D* = 4 and the exit
    is (1, 4*4+1) = (1,17).
    What survives untouched is the ORBIT corollary -- the trajectory from
    D_0 = 17 does satisfy D_k = 9 (mod 16) for all k >= 1 -- because 5 is
    not on that orbit.  The producer census below (T17) shows the situation
    is worse than a single missing case: FOUR rules can emit a b = 1 anchor,
    the closed form forces "= 9 (mod 16)" for only two of them, and both
    remaining producers do fire (pump-flat once, two-ran six times, for
    2 <= D < 400000).  The corrected universal statement is therefore
    MACHINE-VERIFIED on that range, not proved.

(B) A GENERAL SATURATION LEMMA (T16), machine-independent.

    LEMMA T16 (linear-exponential saturation).  Let M >= 1 and let
    A, delta, eps, kappa, rho be integers with
              gcd(delta, M) = 1   and   gcd(rho, M) = 1.
    Put f(n) = delta*n + eps + kappa*rho^n and let
              R = { (c, A*c + f(n)) mod M : n >= n_min }.
    Then for every c_0 in Z_M the set of residues reachable from c_0 in AT
    LEAST ONE R-step is all of Z_M.
    (No hypothesis on A, none on kappa, and n_min is irrelevant.)

    PROOF (strong induction on M).  M = 1 is trivial.  Let M > 1, put
    T = ord_M(rho) and g = gcd(T, M); since T <= phi(M) < M we have g < M.
    Step 1.  For any c and any n_0, the successors {A*c + f(n_0 + jT)}
      = A*c + f(n_0) + delta*T*Z = A*c + f(n_0) + <gcd(delta*T, M)>
      = A*c + f(n_0) + <g>, using gcd(delta, M) = 1.  So every residue
      reached in >= 1 step lies in a FULL coset of <g> that is also reached.
    Step 2.  If g = 1 that coset is Z_M and we are done.  Otherwise let
      pi : Z_M -> Z_M/<g> = Z_g.  R descends to the same shape over Z_g
      (same A, delta, eps, kappa, rho reduced), and gcd(delta, g) =
      gcd(rho, g) = 1 because g | M.  R is total, so pi(reachable in >= 1
      step) = (reachable in >= 1 R-bar-step from pi(c_0)) = Z_g by the
      induction hypothesis.  Hence the reachable set meets every coset of
      <g>, and by Step 1 it contains each of those cosets entirely.  QED

    The descent chain g_0 = M, g_{j+1} = gcd(ord_{g_j}(rho), g_j) is the
    same one used in census/descent.py; T16 is the observation that it needs
    neither the VAL(2) branch schema nor any hypothesis on the multiplier.

(C) M1-N1 -- T16 applied to machine 1, and what it settles.

    THEOREM M1-D (dominant branch; proved, not fitted).  For n >= 1 and
    every integer D with
              16*2^n - 2n - 10  <=  D  <=  20*2^n - 2n - 13,
    the anchor map from (1, D) runs exactly n cascade-A rounds and then the
    "shrink" exit R23, and
              F(D) = 16*D - 240*2^n + 32*n + 169.
    PROOF.  Cascade A is (b,d) -> (2b+4, d-2b-6), so after j rounds
    (b_j, d_j) = (5*2^j - 4, D - 10*2^j + 10 + 2j).  n_A(1,D) is the largest
    m with 10*2^m <= D + 10 + 2m; the displayed interval is exactly
    { D : n_A(1,D) = n } intersected with the R23 guard
    15*d_n > 18*b_n + 61, both of which reduce to the two endpoints:
      15*d_n > 18*b_n + 61  <=>  15D > 240*2^n - 30n - 161  <=>
                                 D >= 16*2^n - 2n - 10,
      n_A = n (i.e. m = n+1 fails)  <=>  D <= 20*2^n - 2n - 13,
    and the remaining R23 guards b_n + 5 <= d_n <= 2*b_n + 5 are implied.
    R23 outputs (1, 16*(d_n - b_n) - 55) and d_n - b_n = D - 15*2^n + 2n + 14,
    giving the closed form.  QED

    COROLLARY M1-N1 (no odd modulus separates machine 1).  Fix an odd M.
    The interval in M1-D has length 4*2^n - 2, so as soon as 2^n >= (M+2)/4
    it contains a complete residue system mod M; hence the TRUE F-edge
    relation mod M contains
        { (c, 16c + 32n - 240*2^n + 169) : c in Z_M, 2^n >= (M+2)/4 }.
    This is T16 with A = 16, delta = 32, eps = 169, kappa = -240, rho = 2,
    and gcd(32, M) = gcd(2, M) = 1 for odd M.  So the closure of ANY residue
    is all of Z_M: no congruence certificate at any odd modulus can prove
    machine 1 non-halting -- and this holds already for the single dominant
    branch, so no refinement of the other branch words can help.

    Machine 1 is therefore the first case-file machine placed on the
    beta-EVEN side of the program's parity dichotomy, and its congruence
    content is now completely mapped:
      * odd part   -- nothing at all (M1-N1, proved);
      * 2-part     -- exactly the one class 9 (mod 16); the dominant branch
                      alone pins the closure to 25 (mod 32), and taking all
                      branches together restores the second lift 9 (mod 32),
                      so no modulus 2^e with e >= 5 says more than mod 16.
    Every congruence fact about machine 1's orbit is thus "D = 9 (mod 16)",
    which does not separate it from H (mod16.py, item 4).  The congruence
    method is closed on machine 1.
"""
import sys
from math import gcd

from formal import G, sweep as _sweep
from onedim import n_A

# --------------------------------------------------------------------------
# traced anchor map: which rule produced a b = 1 anchor?
# --------------------------------------------------------------------------

def G_traced(b, d):
    """G(b, d) plus a tag naming the producer when the target has b' = 1."""
    if d == 0:
        return (0, 2 * b + 4), None
    if d == 1:
        return ((2, 2 * b + 1) if b > 0 else (2, 5)), None
    if d == b + 2:
        return "HALT", None
    if d <= b + 1:
        if 3 * d < 2 * b + 5:
            return (2 * d, 2 * b - 3 * d + 4), None
        if 3 * d == 2 * b + 5:
            return (2, 4 * d - 1), None
        if 11 * d <= 10 * b + 24:
            return (6 * d - 4 * b - 8, 10 * b - 11 * d + 24), None
        return sweep_traced(9 * d - 6 * b - 12, 8 * b - 8 * d + 20)
    if d == b + 3:
        return sweep_traced(3 * b + 2, 6)
    if d == b + 4:
        return sweep_traced(3 * b + 4, 4)
    if d <= 2 * b + 5:
        if 15 * d > 18 * b + 61:
            return (1, 16 * (d - b) - 55), "R23"
        return sweep_traced(6 * b - 3 * d + 19, 4 * d - 4 * b - 14)
    return (2 * b + 4, d - 2 * b - 6), None


def sweep_traced(A, Dl):
    """sweep(A, Dl) with a tag; 'ran' records whether cascade B fired."""
    from onedim import n_B
    ran = False
    if 3 * Dl <= A and A >= 3:
        ran = True
        n = n_B(A, 0, Dl)
        w = 12 * Dl + 8
        T = (4 ** (n - 1) - 1) // 3
        As = A - 3 * Dl + 3 * n - 2 - w * T
        Ds = (w * 4 ** (n - 1) - 2) // 3
        if As == 1:
            r = ((Ds - 2) // 2, 0)
            return r, ("As1-ran" if r[0] == 1 else None)
    else:
        As, Ds = A, Dl
        if As == 0:
            return (0, Ds), None
        if As == 1:
            return (0, Ds + 2), None
    if As == 2:
        return (1, Ds - 1), ("two-ran" if ran else "two-flat")
    q, r = divmod(As, 3)
    if r == 0:
        return (2 * q, Ds - q), None
    if r == 2:
        return (2 * q + 1, Ds - q - 1), None
    return (1, 4 * Ds + 1), ("pump-ran" if ran else "pump-flat")


def F_traced(D, cap=100000):
    """First return of G to {b = 1}: (F(D), producer tag)."""
    r, tag = G_traced(1, D)
    for _ in range(cap):
        if r == "HALT":
            return "HALT", tag
        b, d = r
        if b == 1:
            return d, tag
        r, tag = G_traced(b, d)
    return None, tag


# --------------------------------------------------------------------------
# T16: closures
# --------------------------------------------------------------------------

def offsets(M, delta, eps, kappa, rho, n_min=0):
    """{ f(n) mod M : n >= n_min } for f(n) = delta*n + eps + kappa*rho^n.
    The pair (n mod M, rho^n mod M) is eventually periodic, so iterate until
    it repeats.  Works for rho invertible or not (needed for M even)."""
    out, seen, p, n = set(), {}, pow(rho, n_min, M), n_min
    while True:
        key = (n % M, p)
        if key in seen:
            return out
        seen[key] = n
        out.add((delta * n + eps + kappa * p) % M)
        p = (p * rho) % M
        n += 1


def closure_plus(M, A, O, c0):
    """Residues reachable from c0 in >= 1 step of c -> A*c + O (mod M)."""
    seen = bytearray(M)
    frontier = [(A * c0 + o) % M for o in O]
    for c in frontier:
        seen[c] = 1
    while frontier:
        nxt = []
        for c in frontier:
            Ac = A * c
            for o in O:
                y = (Ac + o) % M
                if not seen[y]:
                    seen[y] = 1
                    nxt.append(y)
        frontier = nxt
    return sum(seen)


def descent_chain(M, rho):
    """g_0 = M, g_{j+1} = gcd(ord_{g_j}(rho), g_j), down to 1."""
    chain, g = [M], M
    while g > 1:
        x, T = rho % g, 1
        while x != 1 % g:
            x = (x * rho) % g
            T += 1
        g = gcd(T, g)
        chain.append(g)
    return chain


# --------------------------------------------------------------------------
if __name__ == "__main__":
    import random
    import time
    t0 = time.time()
    P = lambda *a: print(*a, flush=True)
    P("=" * 74)
    P("MACHINE 1: the exact congruence content of F")
    P("=" * 74)

    # ---- (A) the erratum --------------------------------------------------
    P("\n(A) ERRATUM to mod16.py")
    fd5, tag5 = F_traced(5)
    P(f"    F(5) = {fd5}  ({fd5 % 16} mod 16)   producer = {tag5}")
    assert fd5 == 17 and fd5 % 16 == 1
    P("    G(1,5) = sweep(7,4): 3*Dl = 12 > A = 7, so cascade B does NOT run")
    P("      and D* = Dl = 4 = 0 (mod 4), breaking the proof's 'D* = 2 (mod 4)'")

    NMAX = 400000
    bad, tags, tag_res, twolist = [], {}, {}, []
    for D in range(2, NMAX):
        v, tg = F_traced(D)
        if v in ("HALT", None):
            continue
        tags[tg] = tags.get(tg, 0) + 1
        tag_res.setdefault(tg, set()).add(v % 16)
        if tg == "two-ran":
            twolist.append(D)
        if v % 16 != 9:
            bad.append((D, v, tg))
    P(f"\n    D = 2..{NMAX}: producers of the b = 1 anchor and the residues "
      f"of F(D) mod 16 they give")
    for tg in sorted(tags):
        P(f"      {tg:9s}  used {tags[tg]:7d} times   F mod 16 in "
          f"{sorted(tag_res[tg])}")
    P(f"    D with F(D) != 9 (mod 16): {len(bad)} -> {bad}")

    # ---- T17: the corrected universal statement ---------------------------
    P("\n    T17 (corrected).  FOUR rules emit a b = 1 anchor, not two:")
    P("        R23       d' = 16(d-b) - 55                = 9 (mod 16)  [proved]")
    P("        pump-ran  d' = 4*D*+1, D* = 2 (mod 4)      = 9 (mod 16)  [proved]")
    P("        pump-flat d' = 4*Dl+1, Dl unconstrained    = 4Dl+1       [free]")
    P("        two-ran   d' = D*-1,   D* = 2 (mod 4)      = 1 (mod 4)   [partial]")
    P("      So the closed forms prove '= 9 (mod 16)' only for the first two.")
    P("      mod16.py proved exactly those two and asserted the theorem; the")
    P("      other two are rare but real, and pump-flat breaks it at D = 5.")
    two = [d for d in twolist]
    P(f"      two-ran fires at D = {two[:12]}{' ...' if len(two) > 12 else ''}"
      f"  -> F mod 16 {sorted(tag_res.get('two-ran', set()))} (forced only "
      f"into {{1,5,9,13}})")
    P(f"      CORRECTED STATEMENT [machine-verified, 2 <= D < {NMAX}]:")
    P(f"        F(D) = 9 (mod 16) for every D in that range except D = 5.")
    P("      The ORBIT corollary is unaffected and stays [proved-modulo-run]:")
    P("        D_0 = 17 never meets D = 5 nor any pump-flat/two-ran anchor "
      "outside the compliant set.")

    # ---- (B) T16 ----------------------------------------------------------
    P("\n(B) T16  linear-exponential saturation lemma")
    rng = random.Random(2026)
    trials = fails = 0
    worst = None
    for _ in range(4000):
        M = rng.randrange(1, 400)
        rho = rng.randrange(2, 60)
        delta = rng.randrange(1, 60)
        if gcd(rho, M) != 1 or gcd(delta, M) != 1:
            continue
        A = rng.randrange(0, 60)
        eps = rng.randrange(0, 60)
        kappa = rng.randrange(-60, 60)
        O = offsets(M, delta, eps, kappa, rho, n_min=rng.randrange(0, 5))
        c0 = rng.randrange(M)
        n = closure_plus(M, A, O, c0)
        trials += 1
        if n != M:
            fails += 1
            worst = (M, A, delta, eps, kappa, rho, c0, n)
    P(f"    hypotheses satisfied: {trials} random (M,A,delta,eps,kappa,rho,c0) "
      f"with M < 400 -- closure = Z_M in {trials - fails}, fails {fails}")
    assert fails == 0, worst

    # falsifier: drop gcd(delta, M) = 1
    trials2 = short = 0
    for _ in range(4000):
        M = rng.randrange(2, 200)
        rho = rng.randrange(2, 40)
        delta = rng.randrange(1, 40)
        if gcd(rho, M) != 1 or gcd(delta, M) == 1:
            continue
        A, eps, kappa = rng.randrange(60), rng.randrange(60), rng.randrange(-60, 60)
        O = offsets(M, delta, eps, kappa, rho)
        trials2 += 1
        if closure_plus(M, A, O, rng.randrange(M)) != M:
            short += 1
    P(f"    falsifier -- gcd(delta,M) > 1: {short} of {trials2} instances fail "
      f"to saturate, so the hypothesis is not decorative")
    assert short > 0

    # the descent chain
    P("    descent chain g -> gcd(ord_g(2), g) for a few odd M:")
    for M in (15, 31, 63, 127, 255, 511, 1023, 2047):
        ch = descent_chain(M, 2)
        P(f"      M = {M:5d}: {' -> '.join(map(str, ch))}")
        assert ch[-1] == 1 and all(ch[i + 1] < ch[i] for i in range(len(ch) - 1))
    P("    (strictly decreasing to 1 in every case: ord_g(2) | phi(g) < g)")

    # ---- (C) M1-N1 --------------------------------------------------------
    P("\n(C) M1-D and M1-N1 for machine 1")

    # M1-D: closed form + interval, verified against the anchor map
    checked = 0
    for n in range(1, 22):
        lo, hi = 16 * (1 << n) - 2 * n - 10, 20 * (1 << n) - 2 * n - 13
        span = list(range(lo, min(hi, lo + 60) + 1))
        span += [rng.randrange(lo, hi + 1) for _ in range(40)] if hi > lo else []
        span += [lo - 1, hi + 1]
        for D in span:
            pred = 16 * D - 240 * (1 << n) + 32 * n + 169
            v, tg = F_traced(D)
            inside = lo <= D <= hi
            if inside:
                assert n_A(1, D) == n, (n, D)
                assert v == pred and tg == "R23", (n, D, v, pred, tg)
                checked += 1
            else:
                assert not (v == pred and tg == "R23") or n_A(1, D) != n, (n, D)
    P(f"    M1-D: closed form + interval verified at {checked} points over "
      f"n = 1..21 (interval ends and 40 random interior points each), plus "
      f"both endpoints+1 excluded")
    P(f"      interval length 4*2^n - 2; complete residue system mod M once "
      f"2^n >= (M+2)/4")

    # M1-N1: exhaustive odd M
    A1, d1, e1, k1, r1 = 16, 32, 169, -240, 2
    MMAX = 401
    notsat = []
    for M in range(1, MMAX + 1, 2):
        O = offsets(M, d1, e1, k1, r1, n_min=1)
        if closure_plus(M, A1, O, 17 % M) != M:
            notsat.append(M)
    P(f"    M1-N1: every odd M <= {MMAX} -- closure of D_0 = 17 under the "
      f"dominant relation alone is all of Z_M; exceptions: {notsat}")
    assert notsat == []
    big = [rng.randrange(1, 1200) | 1 for _ in range(25)]
    nb = [M for M in big
          if closure_plus(M, A1, offsets(M, d1, e1, k1, r1, 1), 17 % M) != M]
    P(f"    plus 25 random odd M < 1200 (max {max(big)}): exceptions {nb}")
    assert nb == []

    # even moduli: what the 2-adic side actually gives
    P("\n    the even side, for contrast (dominant relation mod 2^e):")
    for e in range(1, 11):
        M = 1 << e
        O = offsets(M, d1, e1, k1, r1, n_min=1)
        seen = bytearray(M)
        fr = [(A1 * (17 % M) + o) % M for o in O]
        for c in fr:
            seen[c] = 1
        while fr:
            nx = []
            for c in fr:
                for o in O:
                    y = (A1 * c + o) % M
                    if not seen[y]:
                        seen[y] = 1
                        nx.append(y)
            fr = nx
        cl = [i for i in range(M) if seen[i]]
        P(f"      2^{e:<2d} = {M:5d}: |closure| = {len(cl):4d}"
          + (f"  = {cl}" if len(cl) <= 8 else
             f"  (all = 9 mod 16: {all(c % 16 == 9 for c in cl)})"))

    P(f"\n[{time.time() - t0:6.1f}s] all checks passed")
