"""BBf(23) holdout #678  [9/70, 25/2, 44/15, 7/55, 3/5]  NEVER HALTS.

THEOREM (M678).  The FRACTRAN program F = [9/70, 25/2, 44/15, 7/55, 3/5],
started at n = 2, never halts.  [proved; every step machine-verified below]

State = exponent vector (v2, v3, v5, v7, v11) over (2,3,5,7,11).  Rules in
priority order:

    f0 = 9/70  : (v2--, v3+=2, v5--, v7--)   guard  v2>=1 & v5>=1 & v7>=1
    f1 = 25/2  : (v2--, v5+=2)               guard  v2>=1
    f2 = 44/15 : (v2+=2, v3--, v5--, v11++)  guard  v3>=1 & v5>=1
    f3 = 7/55  : (v5--, v7++, v11--)         guard  v5>=1 & v11>=1
    f4 = 3/5   : (v3++, v5--)                guard  v5>=1

LEMMA 0 (halt criterion).  No rule fires  <=>  v2 = 0 and v5 = 0.
[f1 subsumes f0's and f2's... precisely: f1 needs only v2, f4 needs only v5;
f0, f2, f3 each need one of them.]

BOUNDARY (i >= 1), with w := 2^(i+1) - 1 and Y := 2^(i+2) = 2(w+1):
    B_i := (0, 0, Y, 0, w),  next rule f3.
Note the exactly-preserved invariant v5 = 2(v11 + 1) at every boundary.

LEMMA 1 (entry).  From n = 2 = (1,0,0,0,0), direct simulation reaches
B_1 = (0,0,8,0,3) at step 16 = S(1) and B_2 = (0,0,16,0,7) at step 41 =
S(2), where S(i) := 7*2^(i+1) - 3i - 9.  (Phase 1 is transient with its own
word; the uniform template below starts at i = 2.)

LEMMA 2 (one phase).  For every i >= 2, from B_i the program executes
exactly the following word, in 7w + 4 steps, arriving at B_{i+1}:

  Stage A   f3 ^ w        (0,0,Y,0,w) -> (0, 0, w+2, w, 0)
  Stage B   f4            -> (0, 1, w+1, w, 0)
  C-blocks  (f2 f0^2) ^ P      block k starts (0, 3k+1, w+1-3k, w-2k, k)
  Q-blocks  [i even, w = 1 (mod 3): P := (w-1)/3, Q := (w+2)/3, word
             f2 f0 f1, block j starts (0, 3P+1+j, 2, w-2P-j, P+j)]
            [i odd,  w = 0 (mod 3): P := w/3, Q := w/3, word f2 f1 f0,
             block j starts (0, 3P+1+j, 1, w-2P-j, P+j)]
  T-blocks  (f2 f1^2) ^ T, T := 3P+1+Q = (4w+2)/3 resp. (4w+3)/3;
             block t starts (0, T-t, s0+3t, 0, P+Q+t), s0 = 2 resp. 1
  ->  (0, 0, 4w+4, 0, 2w+1) = B_{i+1}.

MECHANISM (the proof's content).  Stage A: f3 is the only enabled rule
(v2 = 0 kills f0/f1, v3 = 0 kills f2) and drains v11 to 0 exactly (w
firings; v5 stays positive: Y - w = w + 2).  Stage B: with v11 = 0, f4
converts one 5 into a 3, waking f2.  C-blocks: f2 pays (v3, v5), yields
v2 = 2 and one 11; f0 (top priority) then fires exactly twice -- limited
by v2, not v5, while v5-at-block-start >= 3 -- paying v5, v7 and building
v3.  Net per block: v3 += 3, v5 -= 3, v7 -= 2, v11 += 1.  C-mode ends when
the block-start v5 = w+1-3k drops to 2 (i even) or 1 (i odd) -- the parity
split, since w+1 = 2^(i+1) is 2 resp. 1 mod 3.  Q-blocks: v5 is now too
small for f0^2; the block locks v5 into a fixed point (2: f2 f0 f1 -- f0
fires before f1 because v5 >= 1 after f2; 1: f2 f1 f0 -- f2 zeroes v5 so
f1 must fire first, then f0).  Net per block: v3 += 1, v7 -= 1, v11 += 1,
v5 fixed.  Q-mode ends when v7 = 0 (after exactly w - 2P = Q blocks --
the f0 fuel runs out).  T-blocks: with v7 = 0, f0 is dead; f2 f1 f1
converts each remaining 3 into three 5s and an 11 (net v3 -= 1, v5 += 3,
v11 += 1).  T-mode ends when v3 = 0; and 3P + 1 + Q, the v3 stock, equals
T by the arithmetic above, leaving exactly (0, 0, 4w+4, 0, 2w+1) = B_{i+1}
with f3 next.  Every guard/priority value is jointly affine in (block
index, within-run counter), so corner checks cover every block [verified].

FIRING BALANCE (cross-check): a3 = w, a4 = 1, a2 = 2w+1, a0 = w,
a1 = 3w+2; total 7w+4.  The balance equations close on all five exponents.

LEMMA 3 (no halt inside a phase).  Halting needs v2 = 0 = v5 (Lemma 0).
Along the word v5 = 0 occurs only inside Q-blocks (odd case, right after
f2; and even case after f2 f0) -- where v2 >= 1 keeps f1 enabled.  At all
other v2 = 0 moments v5 >= 1.  [verified exhaustively]

THEOREM M678 = Lemma 1 + induction over Lemma 2 + Lemma 3.  COROLLARY: the
boundary invariant v5 = 2(v11+1) propagates as (v5, v11) -> (2 v5, 2 v11 + 1);
the machine's survival is invariant-preservation, not margin growth -- the
third distinct non-halting mechanism among the three decided holdouts.

VERIFICATION: V0 vector==bigint sim; V1 halt box; V2 entry to B_2 at step
41; V3 block walk i = 2..2000 (corner checks, exact landing, steps = 7w+4);
V4 word-for-word vs ground truth i = 2..12; V5 no-halt along phases 2..12.
"""

PRIMES = (2, 3, 5, 7, 11)
FRACS = [(9, 70), (25, 2), (44, 15), (7, 55), (3, 5)]
DELTA = [(-1, +2, -1, -1, 0), (-1, 0, +2, 0, 0), (+2, -1, -1, 0, +1),
         (0, 0, -1, +1, -1), (0, +1, -1, 0, 0)]
GUARD = [((0, 1), (2, 1), (3, 1)), ((0, 1),), ((1, 1), (2, 1)),
         ((2, 1), (4, 1)), ((2, 1),)]


def enabled(v, j):
    return all(v[c] >= t for c, t in GUARD[j])


def fire_next(v):
    for j in range(5):
        if enabled(v, j):
            return j
    return None


def vstep(v):
    j = fire_next(v)
    if j is None:
        return None, None
    return tuple(a + d for a, d in zip(v, DELTA[j])), j


def run_word(v, nsteps):
    word = []
    for _ in range(nsteps):
        v2, j = vstep(v)
        if j is None:
            return v, word + ["HALT"]
        v = v2
        word.append(j)
    return v, word


def int_of(v):
    n = 1
    for p, e in zip(PRIMES, v):
        n *= p ** e
    return n


def B(i):
    return (0, 0, 1 << (i + 2), 0, (1 << (i + 1)) - 1)


def S(i):
    return 7 * (1 << (i + 1)) - 3 * i - 9


def pqt(i):
    w = (1 << (i + 1)) - 1
    if i % 2 == 0:                     # w = 1 (mod 3)
        P, Q = (w - 1) // 3, (w + 2) // 3
        qword, s0 = [(2, 1), (0, 1), (1, 1)], 2
    else:                              # w = 0 (mod 3)
        P, Q = w // 3, w // 3
        qword, s0 = [(2, 1), (1, 1), (0, 1)], 1
    T = 3 * P + 1 + Q
    return w, P, Q, T, qword, s0


def apply_run(v, rule, count, check=True):
    def ok(state):
        assert enabled(state, rule), (rule, state)
        for h in range(rule):
            assert not enabled(state, h), ("priority", h, rule, state)
    end = tuple(a + count * d for a, d in zip(v, DELTA[rule]))
    if check and count > 0:
        ok(v)
        ok(tuple(a + (count - 1) * d for a, d in zip(v, DELTA[rule])))
        assert all(x >= 0 for x in end), (rule, end)
    return end


def check_block(start_of, word, K):
    if K == 0:
        return start_of(0)
    for k in ([0] if K == 1 else [0, K - 1]):
        v = start_of(k)
        for rule, count in word:
            v = apply_run(v, rule, count, check=True)
        assert v == start_of(k + 1), ("block chain", k)
    if K >= 3:
        a, b, c = start_of(0), start_of(1), start_of(2)
        assert all(2 * y == x + z for x, y, z in zip(a, b, c)), "not affine"
    return start_of(K)


def phase_runs(i):
    """Lemma 2's word as (rule, count) runs -- exponential in i; V4/V5."""
    w, P, Q, T, qword, s0 = pqt(i)
    runs = [(3, w), (4, 1)]
    runs += [(2, 1), (0, 2)] * P
    runs += qword * Q
    runs += [(2, 1), (1, 2)] * T
    return runs


def walk_phase(i):
    """Lemma 2 at block level; returns (end state, steps)."""
    w, P, Q, T, qword, s0 = pqt(i)
    v = B(i)
    v = apply_run(v, 3, w)
    assert v == (0, 0, w + 2, w, 0)
    v = apply_run(v, 4, 1)
    assert v == (0, 1, w + 1, w, 0)
    v = check_block(lambda k: (0, 3 * k + 1, w + 1 - 3 * k, w - 2 * k, k),
                    [(2, 1), (0, 2)], P)
    assert v == (0, 3 * P + 1, s0, w - 2 * P, P)
    v = check_block(
        lambda j: (0, 3 * P + 1 + j, s0, w - 2 * P - j, P + j), qword, Q)
    assert v == (0, T, s0, 0, P + Q)
    v = check_block(
        lambda t: (0, T - t, s0 + 3 * t, 0, P + Q + t), [(2, 1), (1, 2)], T)
    assert v == (0, 0, s0 + 3 * T, 0, P + Q + T)
    return v, w + 1 + 3 * P + 3 * Q + 3 * T


if __name__ == "__main__":
    import itertools
    import time
    t0 = time.time()
    P_ = lambda *a: print(*a, flush=True)
    P_("=" * 74)
    P_("MACHINE 678 = [9/70, 25/2, 44/15, 7/55, 3/5]: THE NON-HALTING PROOF")
    P_("=" * 74)

    # ---- V0 --------------------------------------------------------------
    n, v = 2, (1, 0, 0, 0, 0)
    for s in range(200000):
        for a, b in FRACS:
            if n % b == 0:
                n = n * a // b
                break
        else:
            n = None
        v, j = vstep(v)
        assert (n is None) == (j is None)
        if n is None:
            break
        assert int_of(v) == n, s
    P_("\nV0  vector simulator == big-int FRACTRAN for 200,000 steps: OK")

    # ---- V1 --------------------------------------------------------------
    bad = 0
    for v in itertools.product(range(6), repeat=5):
        bad += (fire_next(v) is None) != (v[0] == 0 and v[2] == 0)
    assert bad == 0
    P_("V1  Lemma 0 (halt <=> v2=0 & v5=0): all 7,776 vectors in the 0..5 "
       "box: OK")

    # ---- V2 --------------------------------------------------------------
    v, word = run_word((1, 0, 0, 0, 0), S(2))
    assert "HALT" not in word and v == B(2), v
    v1, _ = run_word((1, 0, 0, 0, 0), S(1))
    assert v1 == B(1)
    P_(f"V2  Lemma 1 (entry): n=2 reaches B_1 at step {S(1)} and "
       f"B_2 = (0,0,16,0,7) at step {S(2)}: OK")

    # ---- V3 --------------------------------------------------------------
    IMAX = 2000
    for i in range(2, IMAX + 1):
        w = (1 << (i + 1)) - 1
        v, steps = walk_phase(i)
        assert v == B(i + 1), i
        assert steps == 7 * w + 4, i
        assert S(i) + steps == S(i + 1), i
        # the propagated invariant
        assert v[2] == 2 * (v[4] + 1), i
    P_(f"V3  Lemma 2 block walk, i = 2..{IMAX}: corner guard/priority "
       f"checks in all three block modes, exact landing on B(i+1), step "
       f"count 7w+4, invariant v5 = 2(v11+1): OK")

    # ---- V4 --------------------------------------------------------------
    v = B(2)
    for i in range(2, 13):
        pred = []
        for rule, count in phase_runs(i):
            pred += [rule] * count
        v_end, got = run_word(v, len(pred))
        assert got == pred, f"word mismatch in phase {i}"
        assert v_end == B(i + 1), i
        v = v_end
    P_(f"V4  Lemma 2's firing word == ground-truth simulation, word-for-"
       f"word, phases i = 2..12 (through step {S(13)} = S(13)): OK")

    # ---- V5 --------------------------------------------------------------
    v = B(2)
    visited_halt = 0
    for i in range(2, 13):
        w = (1 << (i + 1)) - 1
        for _ in range(7 * w + 4):
            if v[0] == 0 and v[2] == 0:
                visited_halt += 1
            v, j = vstep(v)
            assert j is not None
    assert visited_halt == 0
    P_("V5  Lemma 3: no state on the orbit satisfies the halt criterion, "
       "phases 2..12 exhaustively: OK")

    P_(f"\nTHEOREM M678: the program never halts from n = 2.  "
       f"[{time.time()-t0:.1f}s]")
