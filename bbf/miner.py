"""The certificate MINER: raw FRACTRAN program in, certificate out.

`decider.py` CHECKS a rigid phase certificate.  This file FINDS one, so
that the pair is an end-to-end decision procedure:

    fractions  --miner-->  certificate  --checker-->  NEVER HALTS

Soundness is unaffected by anything here.  The miner is a search: it may
fail, and it may propose a wrong certificate.  Every certificate it
proposes is handed to `decider.check`, which is the sole authority; a
mined certificate counts only once the checker accepts it, and the
checker's verdict is symbolic in the phase index (all n at once), not a
range check.  So the miner needs no correctness proof -- only the
checker does, and that proof is in the paper and in Lean.

--------------------------------------------------------------------------
THE ALGORITHM

1. SIMULATE the machine from n = 2, recording the firing word and the
   state before every step.

2. FIND BOUNDARY CANDIDATES.  For each rule r, take the positions that
   begin a maximal run of r.  A boundary family is a subsequence of such
   positions whose states fit the expression class
   EXP = {a + b*n + c*2^n} coordinatewise.  (Every machine we know of is
   marked by its "reset" rule, but we simply try all five.)

3. FIT the boundary.  Three unknowns per coordinate, solved exactly over
   the rationals from three consecutive phases, then required to
   reproduce every other observed phase exactly.  Transient prefixes are
   handled by trying successive start offsets.

4. SEGMENT each phase word into STAGES: a maximal repetition of a fixed
   sub-word of period 2..4 becomes a block; anything else is a run.

5. CHECK STRUCTURAL AGREEMENT within a parity class (and, if the classes
   agree, merge them into a single branch).  The stage signature -- the
   sequence of rules and the within-block counts -- must be identical
   across phases; only the repetition counts may vary.

6. FIT THE COUNTS.  Each run count and each block repetition count is
   fitted to EXP over the phase index, the same way as the boundary.

7. COMPOSE.  Block start states are NOT fitted: they are obtained by
   symbolically composing the earlier stages, which is exactly what the
   checker will re-derive.  Only the k-slope is needed, and it is the
   block word's delta.

8. EMIT and hand to `decider.check`.

WHAT THE MINER CANNOT DO, by construction: find a certificate for a
machine that has none.  Non-rigid machines -- the overwhelming majority
of the holdout lists -- consume digits, so no fixed stage signature
recurs and step 5 fails.  That failure is the honest answer, not a
budget problem.
"""
from fractions import Fraction as Fr

from decider import (E, M, Reject, check, report_equivalence, FRACS,
                     all_certs)

MAXP = 4          # largest block period (in runs) we look for
MINREP = 2        # a block must repeat at least this many times
MINPH = 6         # phases needed before we trust a fit


# ======================= exact EXP fitting ==============================
def fit_exp(pts):
    """pts: list of (n, y).  Return E with a + b*n + c*2^n = y on every
    point, or None.  Solves exactly on the first three points and then
    demands the rest agree."""
    if len(pts) < 3:
        return None
    (n0, y0), (n1, y1), (n2, y2) = pts[0], pts[1], pts[2]
    rows = [[Fr(1), Fr(n0), Fr(1 << n0), Fr(y0)],
            [Fr(1), Fr(n1), Fr(1 << n1), Fr(y1)],
            [Fr(1), Fr(n2), Fr(1 << n2), Fr(y2)]]
    # Gaussian elimination with exact rationals
    for col in range(3):
        piv = next((r for r in range(col, 3) if rows[r][col] != 0), None)
        if piv is None:
            return None
        rows[col], rows[piv] = rows[piv], rows[col]
        pv = rows[col][col]
        rows[col] = [x / pv for x in rows[col]]
        for r in range(3):
            if r != col and rows[r][col] != 0:
                f = rows[r][col]
                rows[r] = [x - f * y for x, y in zip(rows[r], rows[col])]
    g = E(rows[0][3], rows[1][3], rows[2][3])
    for n, y in pts:
        try:
            if g.ev(n) != y:
                return None
        except AssertionError:            # non-integral at some index
            return None
    return g


# ======================= simulation & segmentation ======================
def trace(mach, nsteps):
    """Return (states, word): state[i] is the state before word[i]."""
    v, states, word = (1, 0, 0, 0, 0), [], []
    for _ in range(nsteps):
        for j in range(5):
            if all(v[c] >= t for c, t in mach.GUARD[j]):
                states.append(v)
                word.append(j)
                v = tuple(a + d for a, d in zip(v, mach.DELTA[j]))
                break
        else:
            break
    return states, word


def rle(seq):
    out = []
    for x in seq:
        if out and out[-1][0] == x:
            out[-1][1] += 1
        else:
            out.append([x, 1])
    return [(r, c) for r, c in out]


def segment(runs):
    """Runs -> stages: ('run', rule, count) | ('block', reps, word)."""
    out, i = [], 0
    while i < len(runs):
        best = None
        for p in range(2, MAXP + 1):
            if i + MINREP * p > len(runs):
                continue
            pat = runs[i:i + p]
            k = 1
            while i + (k + 1) * p <= len(runs) and \
                    runs[i + k * p:i + (k + 1) * p] == pat:
                k += 1
            if k >= MINREP and (best is None or k * p > best[0] * best[1]):
                best = (k, p, pat)
        if best:
            k, p, pat = best
            out.append(("block", k, tuple(pat)))
            i += k * p
        else:
            out.append(("run",) + tuple(runs[i]))
            i += 1
    return out


def signature(stages):
    """Structure with repetition counts abstracted away."""
    sig = []
    for s in stages:
        sig.append(("R", s[1]) if s[0] == "run" else ("B", s[2]))
    return tuple(sig)


# ============================ the miner =================================
def mine(fracs, nsteps=60000, verbose=False):
    """Return a certificate accepted by decider.check, or None."""
    mach = M(fracs)
    states, word = trace(mach, nsteps)
    if len(word) < 100:
        return None

    for marker in range(5):                       # candidate marker rule
        # positions that begin a maximal run of `marker`
        pos = [i for i, r in enumerate(word)
               if r == marker and (i == 0 or word[i - 1] != marker)]
        if len(pos) < MINPH + 2:
            continue
        for skip in range(0, 4):                  # drop transient phases
            occ = pos[skip:]
            if len(occ) < MINPH + 1:
                break
            cert = _try(mach, states, word, occ, skip, verbose)
            if cert is not None:
                return cert
    return None


def _try(mach, states, word, occ, idx0, verbose):
    nph = len(occ) - 1                            # complete phases seen
    if nph < MINPH:
        return None

    # ---- 3. fit the boundary family --------------------------------
    B = []
    for c in range(5):
        g = fit_exp([(idx0 + j, states[occ[j]][c]) for j in range(nph + 1)])
        if g is None:
            return None
        B.append(g)

    # ---- 4/5. segment every phase and group by parity ---------------
    stages = [segment(rle(word[occ[j]:occ[j + 1]])) for j in range(nph)]
    sigs = [signature(s) for s in stages]
    classes = {}                                  # parity -> list of j
    for j in range(nph):
        classes.setdefault((idx0 + j) % 2, []).append(j)
    if len(set(sigs)) == 1:                       # one branch suffices
        groups = [(None, list(range(nph)))]
    else:
        groups = [(p, js) for p, js in sorted(classes.items())]
        for _, js in groups:
            if len({sigs[j] for j in js}) != 1:
                return None                       # not rigid: word varies
            if len(js) < 3:
                return None                       # too few to fit

    # ---- 6/7. fit counts; compose block starts symbolically ---------
    branches = []
    for parity, js in groups:
        sig = sigs[js[0]]
        st = list(B)                              # symbolic running state
        out = []
        for si in range(len(sig)):
            kind = sig[si][0]
            # ("run", rule, count) vs ("block", reps, word): the varying
            # quantity sits at a different index in the two shapes.
            ci = 2 if kind == "R" else 1
            pts = [(idx0 + j, stages[j][si][ci]) for j in js]
            cnt = fit_exp(pts) if len(pts) >= 3 else None
            if cnt is None:
                return None
            if kind == "R":
                rule = sig[si][1]
                out.append(("run", rule, cnt))
                st = [s + cnt * d for s, d in zip(st, mach.DELTA[rule])]
            else:
                wd = sig[si][1]
                delta = [sum(c * mach.DELTA[r][i] for r, c in wd)
                         for i in range(5)]
                start = [(st[i], delta[i]) for i in range(5)]
                out.append(("block", cnt, list(wd), start))
                st = [A + B_ * cnt for (A, B_) in start]
        branches.append((parity, out))

    cert = {"B": B, "entry": (occ[0], idx0), "br": branches}
    try:
        check(mach, cert)
    except (Reject, AssertionError, ValueError, ZeroDivisionError) as e:
        if verbose:
            print(f"      rejected: {e}")
        return None
    return cert


# ================================ main ==================================
if __name__ == "__main__":
    import time
    t0 = time.time()
    P = lambda *a: print(*a, flush=True)
    P("=" * 74)
    P("THE CERTIFICATE MINER: raw fractions -> certificate -> decision")
    P("=" * 74)

    # ---- 1. rediscover all nine from scratch ------------------------
    P("\n1.  The nine rigid BBf(23) holdouts, mined from the fraction "
      "lists alone")
    good = []
    for mid in sorted(FRACS):
        c = mine(FRACS[mid])
        ok = c is not None
        good.append(ok)
        if ok:
            nb = len(c["br"])
            ns = sum(len(s) for _, s in c["br"])
            P(f"      {mid}: MINED and CHECKER-ACCEPTED  "
              f"(entry {c['entry'][0]} steps at idx {c['entry'][1]}, "
              f"{nb} branch{'es' if nb > 1 else ''}, {ns} stages)")
        else:
            P(f"      {mid}: no certificate found")
    P(f"    -> {sum(good)}/9 decided end-to-end, with no human input "
      f"beyond the fraction list")

    # ---- 2. agreement with the hand-written certificates ------------
    P("\n2.  Do the mined certificates agree with the hand-written ones?")
    hand = all_certs()
    for mid in sorted(FRACS):
        c = mine(FRACS[mid])
        if c is None:
            continue
        h = hand[mid]
        sameB = all(c["B"][i] == h["B"][i] for i in range(5))
        P(f"      {mid}: boundary family identical: {sameB}"
          f"   (mined idx0 {c['entry'][1]} vs hand {h['entry'][1]})")

    # ---- 3. the miner must FAIL on non-rigid machines ---------------
    P("\n3.  Control: the miner on NON-rigid holdouts (must find nothing)")
    import random
    rows = [l.strip() for l in open("bbf_sz23_694_unofficial.txt")]
    geo = set(FRACS[m] and str(FRACS[m]) for m in FRACS)
    rng = random.Random(7)
    sample = rng.sample(range(len(rows)), 40)
    found = 0
    tested = 0
    for i in sample:
        try:
            fr = [tuple(int(x) for x in t.strip().split("/"))
                  for t in rows[i].strip("[]").split(",")]
            mm = M(fr)
        except Exception:
            continue
        tested += 1
        if mine(fr, nsteps=20000) is not None:
            found += 1
            P(f"      line {i+1}: certificate FOUND -- {rows[i]}")
    P(f"      {tested} random refined-list machines tested, "
      f"{found} certificates found")
    P("      (the nine rigid ones are ~1.3% of that list, so a small "
      "number of hits here is expected, not a bug)")

    P(f"\n[{time.time()-t0:.1f}s] miner run complete")
