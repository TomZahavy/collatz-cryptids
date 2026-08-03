"""Rigidity detector for Turing machines -- the BB(6) analogue of
`bbf/phase_detect.py`.

THE IDEA, TRANSPLANTED.  For FRACTRAN the state is a vector of prime
exponents, and a machine is *rigid* when some sub-sequence of its states
-- the phase boundaries -- has coordinates given by formulas in
EXP = {a + b*n + c*q^n}, with the same word of rules between consecutive
boundaries.  A Turing machine has no exponent vector, but it has one as
soon as the tape is run-length encoded:

    ... 0^i 1^j 0^k <head> 1^l ...   ->   skeleton (0,1,0,|,1),
                                          counters (i, j, k, l).

The SKELETON -- the block symbols, the state, the scanned symbol, the
number of blocks on each side -- is a finite object.  The block LENGTHS
are the counters.  A configuration is then exactly a counter-machine
state, and "rigid" means literally the same thing it means for FRACTRAN:
some skeleton recurs forever with its counters in EXP.

WHERE TO LOOK.  Encoding the tape at every step is quadratic and
pointless: almost every step happens strictly inside a block.  We sample
at RECORD events -- the steps on which the head reaches a cell it has
never visited.  Those are the moments the machine commits to new
territory, they are cheap to detect, and for an expanding machine they
are exactly the boundaries a human would draw.

WHAT A HIT MEANS, AND WHAT IT DOES NOT.  A fitted skeleton is a
CONJECTURE about all later phases, produced from finitely many of them.
It is the input to a proof, not a proof.  The same division of labour as
in `bbf/`: the miner guesses, the checker decides.  Nothing here is
sound and nothing here needs to be.

CALIBRATION.  Machines whose counters are affine (c = 0) with a fixed
skeleton are translated cyclers and their relatives -- precisely what the
community's deciders already dispose of.  So a *holdout* list should come
back overwhelmingly NONRIGID, with few or no POLY hits.  A flood of POLY
would mean a bug in this file, not a discovery; see `selftest`.
"""
from fractions import Fraction as Fr

from tm import TM, HALT
from macro import MacroSim, L, R

BLOCKS = (1, 2, 3, 4, 5, 6)   # block sizes tried; b is a representation

MINPH = 6          # occurrences of a skeleton needed before we fit
MAXOFF = 4         # transient prefixes we are willing to drop
MAXBLOCKS = 40     # skeletons wider than this are not phase boundaries
BASES = (2, 3, 4)  # exponential bases tried in EXP = {a + b*n + c*q^n}
MODS = (1, 2, 3)   # residue splittings of the phase index


# ---------------------------------------------------------------- fitting

def fit(pts, basis):
    """Solve exactly for coefficients making `basis` reproduce every point.

    `pts` is [(n, y)]; `basis` is a list of three functions of n.  Returns
    the coefficient triple, or None if the first three points give no
    solution or a later point disagrees."""
    if len(pts) < 3:
        return None
    rows = [[Fr(f(n)) for f in basis] + [Fr(y)] for n, y in pts[:3]]
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
    co = (rows[0][3], rows[1][3], rows[2][3])
    for n, y in pts[3:]:
        if sum(c * Fr(f(n)) for c, f in zip(co, basis)) != y:
            return None
    return co


def fit_exp(pts, q):
    """EXP_q = {a + b*n + c*q^n}."""
    return fit(pts, [lambda n: 1, lambda n: n, lambda n, q=q: q ** n])


def fit_poly(pts):
    """POLY = {a + b*n + c*n^2}."""
    return fit(pts, [lambda n: 1, lambda n: n, lambda n: n * n])


def fit_series(vals):
    """Fit one observed series (a counter, or the step count) over the
    phase index.  Returns (kind, coefficients) with kind in
    {'geo','poly'}, preferring the polynomial reading when both hold
    (they coincide only when the series is affine)."""
    pts = list(enumerate(vals))
    co = fit_poly(pts)
    if co is not None:
        return ("poly", co)
    for q in BASES:
        co = fit_exp(pts, q)
        if co is not None and co[2] != 0:
            return ("geo", (q,) + co)
    return None


def eventually_nonneg(f):
    """Can this fitted series stay nonnegative forever?

    THE CRITERION THAT MAKES THE DETECTOR MEAN ANYTHING.  A block length
    is a count of tape cells, so a phase family in which some counter has
    a negative trend is not a description of the machine's eventual
    behaviour -- it is a description of a TRANSIENT that runs out.  Fits
    like `381 - 4n` are perfectly exact over the 96 phases they were
    fitted on and then the family simply ends, because the counter has
    reached zero.  Without this test the detector reports such transients
    as structure, and the longer the transient the more convincing the
    fit looks.

    This is the same eventual-positivity question the FRACTRAN checker
    answers with `alwaysGE`, and it is easy here for the same reason:
    the characteristic roots are 1, 1, q, so the sign of the leading
    coefficient decides it."""
    kind, co = f
    if kind == "poly":
        a, b, c = co
    else:
        _, a, b, c = co
        if c != 0:
            return c > 0
        c = 0
    if c != 0:
        return c > 0
    if b != 0:
        return b > 0
    return a >= 0


# ---------------------------------------------------------------- scanning

_SCAN_MEMO = {}


def scan(code, blk=1, macro_budget=200000, max_blocks=4000):
    """Memoised wrapper: the two-level analysis asks for the same scan
    several times per machine, and a scan is the expensive thing here.
    Only the most recent handful are kept, which is all a per-machine
    sweep ever needs."""
    key = (code, blk, macro_budget, max_blocks)
    hit = _SCAN_MEMO.get(key)
    if hit is None:
        if len(_SCAN_MEMO) > 12:
            _SCAN_MEMO.clear()
        hit = _SCAN_MEMO[key] = _scan(code, blk, macro_budget, max_blocks)
    return hit


def _scan(code, blk, macro_budget, max_blocks):
    """Run the accelerated simulator at block size `blk`, sampling at
    every record event.

    A record event is the macro step on which the head first faces
    unwritten tape -- the moment it commits to new territory.  It costs
    O(1) to detect (one stack is empty), and with macro acceleration the
    machine actually reaches enough of them to fit.

    Returns (status, events, steps) with events (step, skeleton,
    counters).  `status` is 'halt'; 'infinite' -- the machine provably
    never halts, either because it is trapped inside one block or
    because it marches into blank tape in a fixed state; 'blocks' -- the
    tape fragmented past `max_blocks`, which is what digit consumption
    looks like; or 'budget'."""
    s = MacroSim(TM(code), blk)
    events = []
    prev_edge = True
    while s.macro < macro_budget:
        edge = not s.st[s.d]
        if edge:
            # a macro rule that re-enters its own state moving the same
            # way on blank tape never terminates
            r = s.trans(s.q, s.d, 0)
            if r[0] == 0 and r[3] == s.q and r[2] == s.d:
                return ("infinite", events, s.steps)
            if not prev_edge and s.nblocks() <= MAXBLOCKS:
                events.append((s.steps, s.skeleton(), s.counters()))
        prev_edge = edge
        if not s.step():
            return ("infinite" if s.infinite else "halt", events, s.steps)
        if s.nblocks() > max_blocks:
            return ("blocks", events, s.steps)
    return ("budget", events, s.steps)


TAILS = (48, 32, 24, 16, 12, 8, 6)


def windows(sub):
    """Candidate phase windows within one skeleton's occurrence list:
    a few leading transients dropped, plus tails of several lengths."""
    out = []
    seen = set()
    for w in ([sub[off:] for off in range(MAXOFF + 1)] +
              [sub[-t:] for t in TAILS if len(sub) >= t]):
        key = (len(w), w[0][0] if w else -1)
        if key not in seen:
            seen.add(key)
            out.append(w)
    return out


# ------------------------------------------------------------ classifying

def analyse_at(code, blk, macro_budget=200000, max_blocks=4000):
    """Classify one machine AT ONE BLOCK SIZE.  Returns a dict; `cls` is

      HALTED    -- halted inside the budget
      INFINITE  -- provably never halts (trapped, or marching into blank
                   tape in a fixed state)
      GEO       -- a skeleton recurs with an exponentially growing counter
      POLY      -- a skeleton recurs with polynomial counters
      NONRIGID  -- no skeleton recurs with counters in EXP
      FEWPHASE  -- no skeleton recurred often enough to judge
    """
    status, events, steps = scan(code, blk, macro_budget, max_blocks)
    out = {"code": code, "blk": blk, "status": status, "steps": steps,
           "nevents": len(events)}
    if status == "halt":
        out["cls"] = "HALTED"
        return out
    if status == "infinite":
        out["cls"] = "INFINITE"
        return out
    buckets = {}
    for st, sk, ct in events:
        buckets.setdefault(sk, []).append((st, ct))
    best = None
    for sk, occ in buckets.items():
        if len(occ) < MINPH:
            continue
        for mod in MODS:
            for r in range(mod):
                sub = occ[r::mod] if mod > 1 else occ
                # Rigidity is an EVENTUAL property, so the windows that
                # matter are anchored at the END of the observed run, not
                # the start.  Dropping a few leading phases only clears a
                # short transient; a machine that settles late needs a
                # tail window, and the BW machine is one of those.
                for tail in windows(sub):
                    if len(tail) < MINPH:
                        continue
                    fits = [fit_series([c[j] for _, c in tail])
                            for j in range(len(tail[0][1]))]
                    if any(f is None for f in fits):
                        continue
                    if not all(eventually_nonneg(f) for f in fits):
                        continue          # a transient, not a phase family
                    sf = fit_series([s for s, _ in tail])
                    if sf is None:
                        continue
                    kind = ("geo" if any(f[0] == "geo" for f in fits + [sf])
                            else "poly")
                    # the window is identified by the step at which it
                    # starts, not by an offset: offsets shift when a
                    # longer run turns up more occurrences, step numbers
                    # do not, so `confirm` can find the same window again
                    cand = {"skel": sk, "mod": mod, "res": r,
                            "nph": len(tail), "counters": fits,
                            "steps_fit": sf, "kind": kind,
                            "first_step": tail[0][0]}
                    if best is None or (kind == "geo" and best["kind"] != "geo") \
                       or (kind == best["kind"] and len(tail) > best["nph"]):
                        best = cand
    if best is None:
        out["cls"] = "FEWPHASE" if not buckets or \
            max(len(v) for v in buckets.values()) < MINPH else "NONRIGID"
        out["nskel"] = len(buckets)
        out["maxocc"] = max((len(v) for v in buckets.values()), default=0)
        return out
    out["cls"] = "GEO" if best["kind"] == "geo" else "POLY"
    out["hit"] = best
    out["nskel"] = len(buckets)
    return out


RANK = {"HALTED": 0, "INFINITE": 1, "GEO": 2, "POLY": 3,
        "NONRIGID": 4, "FEWPHASE": 5}


def analyse(code, blocks=BLOCKS, macro_budget=200000, max_blocks=4000):
    """Classify a machine, searching over block sizes.

    A block size is a way of LOOKING at the tape, not a property of the
    machine: structure invisible at b = 1 can be plain at b = 3, because
    the bouncing that hides it gets absorbed into one macro transition.
    So we read the machine at several block sizes and keep the most
    informative reading.  Nothing downstream depends on the choice --
    every block size yields exact base-step counts -- so this is a search
    over presentations, not a guess."""
    best = None
    for blk in blocks:
        r = analyse_at(code, blk, macro_budget, max_blocks)
        if best is None or RANK[r["cls"]] < RANK[best["cls"]]:
            best = r
        if r["cls"] in ("HALTED", "INFINITE"):
            break
    return best


def ev(fit_result, n):
    """Evaluate a fitted series at phase index `n`."""
    kind, co = fit_result
    if kind == "poly":
        a, b, c = co
        return a + b * n + c * n * n
    q, a, b, c = co
    return a + b * n + c * Fr(q) ** n


def confirm(res, extra=4, macro_budget=3 * 10 ** 6):
    """Re-run further and check the fitted formulas against phases the
    fit never saw.

    `fit` already determines each closed form from three phases and
    demands every other OBSERVED phase agree, so a hit is never a
    curve-fit through all its data.  This goes one better: it extends the
    simulation and confronts the formula with genuinely new phases.
    Returns (n_new_checked, n_mismatches)."""
    hit = res["hit"]
    sk, mod, r0 = hit["skel"], hit["mod"], hit["res"]
    _, events, _ = scan(res["code"], res["blk"], macro_budget)
    occ = [(s, c) for s, k, c in events if k == sk]
    sub = occ[r0::mod] if mod > 1 else occ
    # relocate the fitted window by the step it started at
    start = next((i for i, (s, _) in enumerate(sub)
                  if s == hit["first_step"]), None)
    if start is None:
        return (0, 0)
    tail = sub[start:]
    seen = hit["nph"]
    new = tail[seen:seen + extra]
    bad = 0
    for j, (st, ct) in enumerate(new):
        n = seen + j
        if ev(hit["steps_fit"], n) != st:
            bad += 1
            continue
        for i, f in enumerate(hit["counters"]):
            if ev(f, n) != ct[i]:
                bad += 1
                break
    return len(new), bad


# ------------------------------------------------------------------ test

def selftest():
    # 1. the BB(5) champion halts, and the detector says so at the right step
    r = analyse("1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA", blocks=(1,),
                max_blocks=10 ** 6)
    assert r["cls"] == "HALTED", r["cls"]
    assert r["steps"] == 47176870, r["steps"]
    print("  ok  BB(5) champion -> HALTED at %d steps" % r["steps"])

    # 2. exact fitting is exact
    assert fit_exp([(0, 2), (1, 3), (2, 5), (3, 9), (4, 17)], 2) == \
        (Fr(1), Fr(0), Fr(1))
    assert fit_exp([(0, 2), (1, 3), (2, 5), (3, 9), (4, 18)], 2) is None
    assert fit_poly([(0, 1), (1, 4), (2, 9), (3, 16)]) == (Fr(1), Fr(2), Fr(1))
    print("  ok  exact EXP / POLY fitting")


if __name__ == "__main__":
    print("rigid.py selftest")
    selftest()
    print("all pass")
