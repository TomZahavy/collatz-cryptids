"""A certified non-halting DECIDER for rigid FRACTRAN machines.

This file turns the nine hand proofs (m431/m455/m678/m_siblings) into a
general, sound decision procedure with machine-checkable certificates, and
proves the nine machines non-halting FOR ALL phase indices symbolically --
removing the "idx <= 2000" numeric sweeps of the individual proof files.

--------------------------------------------------------------------------
THE CERTIFICATE CLASS

A *rigid phase certificate* for a FRACTRAN program F (rules over exponent
vectors of (2,3,5,7,11), first-match priority) consists of:

  * an entry: (E, idx0) -- from n = 2, F reaches B(idx0) in E steps;
  * a boundary family B(n): five coordinates, each an expression in the
    class  EXP := { a + b*n + c*2^n : a, b, c rational };
  * one or two BRANCHES (covering all n >= idx0, split by parity when the
    phase word depends on n mod 2), each a list of stages:
      - run(rule, count)          count in EXP
      - block(K, word, start)     K in EXP; word a fixed list of
                                  (rule, small-int count); start(k) affine:
                                  coordinate i = A_i + B_i * k, A_i in EXP,
                                  B_i an integer.

CHECKING (all symbolic, exact rational arithmetic):

  C1  chain:  within a block, start(k) + (word deltas) = start(k+1) is an
      integer identity per coordinate (word delta == B_i), and the stage
      sequence composes: each stage's symbolic end state is the next
      stage's start; the final state equals B(n+1) (coefficient equality
      -- sound because {1, n, 2^n} are linearly independent over Q).
  C2  guards:  every run's rule guard holds at the run's両 endpoints; in a
      block, at the four corners (k in {0, K-1} x t in {0, c-1}).  Guard
      values are JOINTLY AFFINE in (k, t) with EXP coefficients, so corner
      nonnegativity implies rectangle nonnegativity.  The corner value is
      again in EXP, and "> = threshold for all admissible n" is DECIDED by
      the eventual-sign procedure below.
  C3  priority:  for every higher-priority rule h, some SINGLE guard
      condition of h fails at all corners -- an affine function failing at
      the corners fails on the whole rectangle (affine functions attain
      extremes at corners), so h is disabled throughout.  (Endpoint failure
      of the *conjunction* alone would NOT be sound; the single-condition
      form is.)
  C4  entry: direct simulation, E steps, exact match with B(idx0).
  C5  coverage: the branches' parity classes cover every n >= idx0.

EVENTUAL-SIGN DECISION for g(n) = a + b*n + c*2^n on a parity class:
  if c > 0: find N with g(N) >= t and 3*c*2^N + 2*b >= 0 (then g is
    increasing on the class beyond N); check n0..N directly.  If c = 0:
    linear case (b > 0 similarly; b = 0: compare a; b < 0: reject).
  If c < 0: reject.  This decides "g >= t for all admissible n" outright.

SOUNDNESS THEOREM.  If check(F, C) accepts, then F never halts from n = 2.
  Proof.  C4 gives reach of B(idx0).  Fix any admissible n and its branch.
  By C1-C3 and the affine run lemma (a rule whose guard holds and whose
  higher-priority rivals are disabled at both endpoints of an affine
  segment fires at every point of it), the machine's actual trajectory
  from B(n) follows the certified word exactly and lands on B(n+1); no
  state on the word is halting because at every state the named rule
  fires.  C5 closes the induction: every phase index >= idx0 is covered,
  so the orbit visits B(n) for all n and never halts.  QED

  Note what makes this a *decider* for the certified class: certificate
  checking is finite, exact, and needs no simulation beyond the entry.
  The class EXP is closed under every operation the checker performs
  (shift n -> n+1, integer combinations, K-1 substitution), and its
  linear independence makes state equality a finite coefficient check.

COMPLETENESS (empirical, not claimed as theorem): all nine rigid (GEO)
machines of the refined BBf(23) holdout list admit certificates in this
class -- they are exactly the certificates below.

--------------------------------------------------------------------------
EQUIVALENCE DECIDER (second half of the file)

Two certified machines are *template-isomorphic* if some prime-axis
permutation and rule bijection maps one's certificate (stages, counts,
start states, boundary) exactly onto the other's, allowing a constant
index shift.  Template isomorphism of certificates is decidable by finite
search (<= 5! * 5! maps), and it implies that the two machines' orbits
correspond exactly from their entry boundaries on.  Running it on the nine
gives the corrected family structure -- see report_equivalence().
"""
from fractions import Fraction as Fr

PRIMES = (2, 3, 5, 7, 11)


def fac(n):
    v = [0] * 5
    for k, p in enumerate(PRIMES):
        while n % p == 0:
            n //= p
            v[k] += 1
    assert n == 1
    return tuple(v)


# ============================ EXP expressions ============================
class E:
    """a + b*n + c*2^n, exact rationals."""
    __slots__ = ("a", "b", "c")

    def __init__(self, a=0, b=0, c=0):
        self.a, self.b, self.c = Fr(a), Fr(b), Fr(c)

    def __add__(s, o):
        o = E(o) if not isinstance(o, E) else o
        return E(s.a + o.a, s.b + o.b, s.c + o.c)

    __radd__ = __add__

    def __sub__(s, o):
        o = E(o) if not isinstance(o, E) else o
        return E(s.a - o.a, s.b - o.b, s.c - o.c)

    def __rsub__(s, o):
        return (E(o) if not isinstance(o, E) else o) - s

    def __mul__(s, k):
        return E(s.a * k, s.b * k, s.c * k)

    __rmul__ = __mul__

    def __eq__(s, o):
        o = E(o) if not isinstance(o, E) else o
        return (s.a, s.b, s.c) == (o.a, o.b, o.c)

    def __hash__(s):
        return hash((s.a, s.b, s.c))

    def shift(s):
        """n -> n+1."""
        return E(s.a + s.b, s.b, 2 * s.c)

    def ev(s, n):
        v = s.a + s.b * n + s.c * (1 << n)
        assert v.denominator == 1, (s.a, s.b, s.c, n)
        return int(v)

    def __repr__(s):
        return f"E({s.a},{s.b},{s.c})"


def tail_start(K, n0, step2, cap=400):
    """First admissible n with K(n) >= 1, verifying K == 0 exactly on all
    earlier admissible n (vacuous-stage soundness).  None if K == 0
    everywhere scanned AND symbolically (the zero expression)."""
    if K == E(0):
        return None
    n = n0
    while n <= cap:
        v = K.ev(n)
        if v >= 1:
            return n
        if v != 0:
            raise Reject(f"stage count negative at n={n}")
        n += step2
    raise Reject("stage count never positive (cap)")


def ge_forall(g, t, n0, step2, cap=400):
    """Decide g(n) >= t for all n >= n0 with n stepping by `step2` (2 for a
    parity class, 1 for all n).  Returns True/False (False = cannot
    certify, treat as reject)."""
    a, b, c = g.a, g.b, g.c
    if c < 0 or (c == 0 and b < 0):
        return False
    if c == 0 and b == 0:
        return a >= t
    n = n0
    while n <= cap:
        grow = (3 if step2 == 2 else 1) * c * (1 << n) + step2 * b
        if g.ev(n) >= t and grow >= 0:
            return all(g.ev(m) >= t for m in range(n0, n + 1, step2))
        n += step2
    return False


# ============================ the machine ================================
class M:
    def __init__(self, fracs):
        self.fracs = fracs
        self.DELTA, self.GUARD = [], []
        for a, b in fracs:
            na, nb = fac(a), fac(b)
            self.DELTA.append(tuple(x - y for x, y in zip(na, nb)))
            self.GUARD.append(tuple((k, e) for k, e in enumerate(nb) if e))

    def sim(self, v, nsteps):
        for _ in range(nsteps):
            for j in range(5):
                if all(v[c] >= t for c, t in self.GUARD[j]):
                    v = tuple(a + d for a, d in zip(v, self.DELTA[j]))
                    break
            else:
                return None
        return v


# =========================== the checker =================================
class Reject(Exception):
    pass


def _corner_states(start, word, K):
    """Symbolic states at which guards must be checked, as lists of EXP
    (k substituted with 0 and K-1), each tagged with the rule to fire."""
    outs = []
    for ke in (E(0), K - 1):                       # corner k values
        st = [A + B * ke for (A, B) in start]
        for rule, cnt in word:
            outs.append((st, rule))                # t = 0 corner
            if cnt > 1:                            # t = cnt-1 corner
                outs.append((
                    [s + (cnt - 1) * d for s, d in
                     zip(st, DELTAS_CUR[rule])], rule))
            st = [s + cnt * d for s, d in zip(st, DELTAS_CUR[rule])]
    return outs


DELTAS_CUR = None     # set per machine during check (E-lifted deltas)


def check(mach, cert, verbose=False):
    """Sound checker; raises Reject or returns the certified idx0."""
    global DELTAS_CUR
    DELTAS_CUR = mach.DELTA          # plain int deltas: EXP is multiplied
                                     # only by integer constants
    Bnd, (Esteps, idx0), branches = cert["B"], cert["entry"], cert["br"]

    # C4 entry
    v = mach.sim((1, 0, 0, 0, 0), Esteps)
    if v is None or list(v) != [x.ev(idx0) for x in Bnd]:
        raise Reject("entry")

    # C5 coverage
    pars = sorted(p for p, _ in branches)
    if pars not in ([0, 1], [None]):
        raise Reject("coverage")

    for parity, stages in branches:
        step2 = 2 if parity is not None else 1
        n0 = idx0 if parity is None else \
            idx0 + ((parity - idx0) % 2)
        st = list(Bnd)

        def need(g, t, what, ne):
            if not ge_forall(g, t, ne, step2):
                raise Reject(f"guard {what} parity={parity}: {g}>={t}")

        def guards_at(state, rule, what, ne):
            for c, t in mach.GUARD[rule]:
                need(state[c], t, f"{what} r{rule} coord{c}", ne)

        def prio_at(states, rule, what, ne):
            """states: list of symbolic states where `rule` fires; every
            higher-priority h must have ONE condition failing at all."""
            for h in range(rule):
                okcond = False
                for c, t in mach.GUARD[h]:
                    if all(ge_forall(E(t - 1) - s[c], 0, ne, step2)
                           for s in states):
                        okcond = True
                        break
                if not okcond:
                    raise Reject(f"prio {what}: rule {h} not excluded")

        for si, stage in enumerate(stages):
            if stage[0] == "run":
                _, rule, cnt = stage
                end = [s + cnt * d for s, d in
                       zip(st, DELTAS_CUR[rule])]
                ne = tail_start(cnt, n0, step2)
                if ne is not None:
                    last = [s + (cnt - 1) * d for s, d in
                            zip(st, DELTAS_CUR[rule])]
                    guards_at(st, rule, f"s{si}@0", ne)
                    guards_at(last, rule, f"s{si}@end", ne)
                    prio_at([st, last], rule, f"s{si}", ne)
                st = end
            else:
                _, K, word, start = stage
                # chain identity: word delta must equal the k-coefficient
                tot = [sum((cnt * DELTAS_CUR[r][i] for r, cnt in word),
                           E(0)) for i in range(5)]
                for i in range(5):
                    if tot[i] != E(start[i][1]):
                        raise Reject(f"s{si} chain coord {i}")
                # block entry: current state must equal start(0)
                for i in range(5):
                    if st[i] != start[i][0]:
                        raise Reject(f"s{si} block entry coord {i}")
                ne = tail_start(K, n0, step2)
                if ne is not None:
                    corners = _corner_states(start, word, K)
                    by_rule = {}
                    for cst, rule in corners:
                        guards_at(cst, rule, f"s{si}blk", ne)
                        by_rule.setdefault(rule, []).append(cst)
                    for rule, csts in by_rule.items():
                        prio_at(csts, rule, f"s{si}blk r{rule}", ne)
                st = [A + B * K for (A, B) in start]
        # landing
        for i in range(5):
            if st[i] != Bnd[i].shift():
                raise Reject(f"landing coord {i} parity={parity}")
    return idx0


# ========================= the nine certificates =========================
def run(rule, cnt):
    return ("run", rule, cnt if isinstance(cnt, E) else E(cnt))


def blk(K, word, start):
    return ("block", K, word,
            [(A if isinstance(A, E) else E(A), B) for (A, B) in start])


def C431():
    W, m, u, I = E(-1, 0, 2), E(-1, 0, 1), E(-1, 1, 2), E(0, 1, 0)
    B = [W, E(0), E(0), E(0), I]
    common = [run(3, W),
              blk(m, [(4, 1), (1, 1)],
                  [(0, 0), (0, 2), (0, 0), (W, -2), (I, 2)]),
              run(4, 1), run(2, 1)]
    def rounds(q):
        return blk(q, [(0, 3), (2, 1)],
                   [(3, 0), (2 * m, -3), (0, 2), (0, 0), (u, -1)])
    qe, qo = E(Fr(-2, 3), 0, Fr(2, 3)), E(Fr(-4, 3), 0, Fr(2, 3))
    return dict(B=B, entry=(3, 1), br=[
        (0, common + [rounds(qe), run(2, 2 * qe)]),
        (1, common + [rounds(qo), run(0, 2), run(2, 2 * qo + 2)])])


def C455():
    X, I = E(0, 0, 1), E(0, 1, 0)
    B = [X + 1, X - 2, E(0), E(0), I - 1]
    head = [run(2, X + 1), run(3, X - 1), run(4, 1), run(1, 1)]
    def rounds(K):
        return blk(K, [(0, 3), (1, 1)],
                   [(3, 0), (0, 6), (X - 1, -3), (0, 2), (X + I - 1, -1)])
    Re, F = (X - 1) * Fr(1, 3), (X - 2) * Fr(1, 3)
    Le, Lo = (2 * X + 1) * Fr(1, 3), (2 * X - 1) * Fr(1, 3)
    return dict(B=B, entry=(11, 2), br=[
        (0, head + [rounds(Re - 1), run(0, 3), run(1, Le)]),
        (1, head + [rounds(F), run(0, 1), run(1, Lo)])])


def C678():
    w, Y = E(-1, 0, 2), E(0, 0, 4)
    B = [E(0), E(0), Y, E(0), w]
    def stages(P, Q, T, qword, s0):
        return [run(3, w), run(4, 1),
                blk(P, [(2, 1), (0, 2)],
                    [(0, 0), (1, 3), (w + 1, -3), (w, -2), (0, 1)]),
                blk(Q, qword,
                    [(0, 0), (3 * P + 1, 1), (E(s0), 0), (w - 2 * P, -1),
                     (P, 1)]),
                blk(T, [(2, 1), (1, 2)],
                    [(0, 0), (T, -1), (E(s0), 3), (0, 0), (P + Q, 1)])]
    Pe, Qe = (w - 1) * Fr(1, 3), (w + 2) * Fr(1, 3)
    Po = Qo = w * Fr(1, 3)
    return dict(B=B, entry=(41, 2), br=[
        (0, stages(Pe, Qe, 3 * Pe + 1 + Qe, [(2, 1), (0, 1), (1, 1)], 2)),
        (1, stages(Po, Qo, 3 * Po + 1 + Qo, [(2, 1), (1, 1), (0, 1)], 1))])


def transport(cert, rulemap, axmap):
    """Certificate for a machine whose rules/axes are a bijective image."""
    def mst(vec):                       # vector of E or (E,int) pairs
        out = [None] * 5
        for t, x in enumerate(vec):
            out[axmap[t]] = x
        return out
    def mstage(s):
        if s[0] == "run":
            return ("run", rulemap[s[1]], s[2])
        _, K, word, start = s
        return ("block", K, [(rulemap[r], c) for r, c in word], mst(start))
    return dict(B=mst(cert["B"]), entry=cert["entry"],
                br=[(p, [mstage(s) for s in sts]) for p, sts in cert["br"]])


def C574():
    s = E(-1, 1, Fr(1, 2))
    w = E(-1, 0, Fr(1, 2))
    B = [E(0), E(0), s, E(-1, 0, 1), E(0)]
    return dict(B=B, entry=(36, 4), br=[(None, [
        run(3, w), run(4, 1),
        blk(w, [(0, 1), (1, 1)],
            [(0, 2), (1, 0), (s, -1), (0, 2), (w, -1)]),
        run(0, 1), run(2, 2 * w + 3)])])


def C570():
    x, y = E(-1, 0, 1), E(0, 2, 2)
    B = [E(0), y, E(0), E(0), x]
    head = [run(3, x), run(4, 1), run(1, 1)]
    def rounds(q):
        return blk(q, [(0, 3), (1, 1)],
                   [(3, 0), (y - 2, -4), (x, -3), (0, 2), (1, 4)])
    qe, qo = x * Fr(1, 3), (x - 1) * Fr(1, 3)
    return dict(B=B, entry=(76, 4), br=[
        (0, head + [rounds(qe), run(1, 2 * qe), run(2, 3 + 6 * qe)]),
        (1, head + [rounds(qo), run(0, 1), run(1, 2 * qo + 1),
                    run(2, 6 * qo + 5)])])


def C680():
    X = E(0, 0, 1)
    B = [X, E(0), E(0), E(0), X - 1]
    head = [run(2, X), run(3, X - 1), run(4, 1), run(1, 1)]
    def rounds(P):
        return blk(P, [(0, 2), (1, 1)],
                   [(2, 0), (0, 3), (X - 1, -3), (X - 1, -2), (1, 1)])
    Pe = (X - 1) * Fr(1, 3)
    Qe = X - 1 - 2 * Pe
    Te = (3 * Pe + Qe) * Fr(1, 2)
    Po = (X - 2) * Fr(1, 3)
    Qo = X - 2 - 2 * Po
    To = (3 * Po + 2 + Qo) * Fr(1, 2)
    return dict(B=B, entry=(78, 4), br=[
        (0, head + [rounds(Pe),
                    blk(Qe, [(2, 1), (0, 1), (1, 1)],
                        [(2, 0), (3 * Pe, 1), (0, 0), (X - 1 - 2 * Pe, -1),
                         (1 + Pe, 1)]),
                    blk(Te, [(2, 1), (1, 2)],
                        [(2, 3), (3 * Pe + Qe, -2), (0, 0), (0, 0),
                         (1 + Pe + Qe, 2)])]),
        (1, head + [rounds(Po), run(0, 1),
                    blk(Qo, [(2, 1), (1, 1), (0, 1)],
                        [(1, 0), (3 * Po + 2, 1), (0, 0),
                         (X - 2 - 2 * Po, -1), (1 + Po, 1)]),
                    blk(To, [(2, 1), (1, 2)],
                        [(1, 3), (3 * Po + 2 + Qo, -2), (0, 0), (0, 0),
                         (1 + Po + Qo, 2)])])])


FRACS = {
    431: [(5, 6), (9, 35), (8, 55), (7, 2), (605, 7)],
    455: [(63, 10), (8, 77), (33, 2), (5, 9), (7, 3)],
    678: [(9, 70), (25, 2), (44, 15), (7, 55), (3, 5)],
    673: [(9, 35), (5, 6), (8, 55), (7, 2), (605, 7)],
    502: [(7, 15), (9, 14), (125, 77), (2, 5), (847, 2)],
    623: [(9, 10), (5, 21), (343, 55), (2, 7), (605, 2)],
    574: [(8, 15), (147, 22), (35, 2), (11, 49), (3, 7)],
    570: [(77, 30), (88, 21), (9, 2), (5, 11), (7, 3)],
    680: [(9, 70), (44, 15), (25, 2), (7, 55), (3, 5)],
}


def all_certs():
    c431 = C431()
    return {
        431: c431, 455: C455(), 678: C678(),
        673: transport(c431, {0: 1, 1: 0, 2: 2, 3: 3, 4: 4},
                       (0, 1, 2, 3, 4)) | {"entry": (3, 1)},
        502: transport(c431, {0: 0, 1: 1, 2: 2, 3: 3, 4: 4},
                       (2, 1, 3, 0, 4)) | {"entry": (2, 1)},
        623: transport(c431, {0: 1, 1: 0, 2: 2, 3: 3, 4: 4},
                       (3, 1, 2, 0, 4)) | {"entry": (2, 1)},
        574: C574(), 570: C570(), 680: C680(),
    }


# ======================= template isomorphism ============================
def canon(cert):
    """Abstract shape used for isomorphism search (axes/rules abstracted
    away are supplied by the candidate maps)."""
    return cert


def iso(certA, certB, machA, machB):
    """Search rule bijection + axis permutation mapping certA onto certB
    exactly (same counts, same start/boundary expressions after mapping).
    Returns (rulemap, axmap) or None."""
    from itertools import permutations
    for rm in permutations(range(5)):
        # rule deltas must correspond under some axis map; try axis perms
        for am in permutations(range(5)):
            ok = True
            for r in range(5):
                dA = machA.DELTA[r]
                dB = machB.DELTA[rm[r]]
                if any(dA[t] != dB[am[t]] for t in range(5)):
                    ok = False
                    break
                gA = sorted((am[c], t) for c, t in machA.GUARD[r])
                gB = sorted(machB.GUARD[rm[r]])
                if gA != gB:
                    ok = False
                    break
            if not ok:
                continue
            t = transport(certA, {i: rm[i] for i in range(5)}, am)
            t["entry"] = certB["entry"]
            if t == certB:
                return rm, am
    return None


def report_equivalence(certs):
    ids = sorted(certs)
    machs = {i: M(FRACS[i]) for i in ids}
    classes = []
    for i in ids:
        for cl in classes:
            if iso(certs[cl[0]], certs[i], machs[cl[0]], machs[i]):
                cl.append(i)
                break
        else:
            classes.append([i])
    return classes


# ================================ main ===================================
if __name__ == "__main__":
    import time
    t0 = time.time()
    P = lambda *a: print(*a, flush=True)
    P("=" * 74)
    P("THE RIGID-PHASE-CERTIFICATE DECIDER, run on the nine BBf(23) GEO "
      "holdouts")
    P("=" * 74)
    certs = all_certs()
    for mid in sorted(certs):
        mach = M(FRACS[mid])
        idx0 = check(mach, certs[mid])
        P(f"  {mid}: CERTIFIED NEVER-HALTING for ALL phases n >= {idx0} "
          f"(symbolic; no numeric sweep)")
    P(f"\nTemplate-isomorphism classes (rule bijection + axis permutation, "
      f"exact certificate match):")
    for cl in report_equivalence(certs):
        P(f"  {cl}")
    # ---- falsifier: corrupted certificates must be rejected -------------
    import copy
    rejected = accepted = 0
    for mid in sorted(certs):
        mach = M(FRACS[mid])
        for mut in range(60):
            c = copy.deepcopy(certs[mid])
            k = mut % 6
            if k == 0:      # perturb a boundary coefficient
                c["B"][mut % 5] = c["B"][mut % 5] + 1
            elif k == 1:    # wrong entry length
                c["entry"] = (c["entry"][0] + 1, c["entry"][1])
            elif k == 2:    # perturb a run count / block K
                p, sts = c["br"][mut % len(c["br"])]
                st = sts[mut % len(sts)]
                if st[0] == "run":
                    sts[mut % len(sts)] = ("run", st[1], st[2] + 1)
                else:
                    sts[mut % len(sts)] = ("block", st[1] + 1, st[2], st[3])
            elif k == 3:    # wrong rule in a stage
                p, sts = c["br"][mut % len(c["br"])]
                st = sts[mut % len(sts)]
                if st[0] == "run":
                    sts[mut % len(sts)] = ("run", (st[1] + 1) % 5, st[2])
                else:
                    w = [((r + 1) % 5, ct) for r, ct in st[2]]
                    sts[mut % len(sts)] = ("block", st[1], w, st[3])
            elif k == 4:    # perturb a block start A-coefficient
                p, sts = c["br"][mut % len(c["br"])]
                blks = [x for x in sts if x[0] == "block"]
                if not blks:
                    continue
                b = blks[mut % len(blks)]
                i = sts.index(b)
                stt = list(b[3])
                stt[mut % 5] = (stt[mut % 5][0] + 1, stt[mut % 5][1])
                sts[i] = ("block", b[1], b[2], stt)
            else:           # perturb a block start k-coefficient
                p, sts = c["br"][mut % len(c["br"])]
                blks = [x for x in sts if x[0] == "block"]
                if not blks:
                    continue
                b = blks[mut % len(blks)]
                i = sts.index(b)
                stt = list(b[3])
                stt[mut % 5] = (stt[mut % 5][0], stt[mut % 5][1] + 1)
                sts[i] = ("block", b[1], b[2], stt)
            try:
                check(mach, c)
                accepted += 1
            except (Reject, AssertionError):
                rejected += 1
    P(f"\nFalsifier: {rejected} corrupted certificates rejected, "
      f"{accepted} wrongly accepted")
    assert accepted == 0, "SOUNDNESS BUG: a corrupted certificate passed"
    P(f"\n[{time.time()-t0:.1f}s] decider run complete")
