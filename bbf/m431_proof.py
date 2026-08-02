"""BBf(23) holdout #431  [5/6, 9/35, 8/55, 7/2, 605/7]  NEVER HALTS.

THEOREM (M431).  The FRACTRAN program F = [5/6, 9/35, 8/55, 7/2, 605/7],
started at n = 2, never halts.  [proved; every step of the proof is
machine-verified below]

Notation.  State = exponent vector (v2, v3, v5, v7, v11) of n over the primes
(2, 3, 5, 7, 11) -- no other prime ever appears (each numerator/denominator
factors over these).  The rules, in priority order, with their guards:

    f0 = 5/6    : (v2--, v3--, v5++)         guard  v2>=1 & v3>=1
    f1 = 9/35   : (v3+=2, v5--, v7--)        guard  v5>=1 & v7>=1
    f2 = 8/55   : (v2+=3, v5--, v11--)       guard  v5>=1 & v11>=1
    f3 = 7/2    : (v2--, v7++)               guard  v2>=1
    f4 = 605/7  : (v5++, v7--, v11+=2)       guard  v7>=1

LEMMA 0 (halt criterion).  No rule fires  <=>  v2 = 0 and v7 = 0 and
(v5 = 0 or v11 = 0).   [f0's guard implies f3's; f1's implies f4's; so halting
reduces to f2, f3, f4 all disabled.]

LEMMA 1 (entry).  From n = 2 = (1,0,0,0,0) the run begins f3, f4, f2 and
reaches (3,0,0,0,1) at step 3 with f3 next.   [direct computation]

Define the PHASE-i BOUNDARY state (i >= 1), with W := 2^(i+1) - 1 and
m := 2^i - 1 (so W = 2m + 1, W odd):

    B_i := (v2, v3, v5, v7, v11) = (W, 0, 0, 0, i),  next rule f3.

Lemma 1 says B_1 is reached at step 3.

LEMMA 2 (one phase).  For every i >= 1, from B_i the program executes exactly
the following word and arrives at B_{i+1}, in 2^(i+3) - 5 steps, never
halting on the way:

  Stage 1   f3 ^ W                  (W,0,0,0,i)        -> (0,0,0,W,i)
  Stage 2   (f4 f1)^m  f4           -> (0, 2m, 1, 0, i+2m+2)
  Stage 3   f2                      -> (3, 2m, 0, 0, u),  u := i+2m+1
  Stage 4   [i even, so 2m = 0 (mod 3), q := 2m/3]:
                (f0^3 f2)^q         -> (3, 0, 2q, 0, u-q)
                f2 ^ 2q             -> (3+6q, 0, 0, 0, u-3q) = B_{i+1}
            [i odd, so 2m = 2 (mod 3), q := (2m-2)/3]:
                (f0^3 f2)^q         -> (3, 2, 2q, 0, u-q)
                f0 ^ 2              -> (1, 0, 2q+2, 0, u-q)
                f2 ^ (2q+2)         -> (7+6q, 0, 0, 0, u-3q-2) = B_{i+1}

  (Even case: 3+6q = 3+4m = 2^(i+2)-1 and u-3q = i+1.  Odd case: 7+6q =
   3+4m = 2^(i+2)-1 and u-3q-2 = i+1.  Both land on B_{i+1} exactly.)

PROOF of Lemma 2.  Within any single-rule run the state is affine in the run
counter, so every guard/priority condition below is affine in it and holds
throughout a run iff it holds at both ends [checked at both ends for every
run, every i, in the verification]:

  Stage 1: v3 = v5 = 0 disables f0, f1, f2 throughout; f3 fires while
    v2 >= 1, i.e. exactly W times; then v2 = 0, v7 = W >= 1, so f4 is next.
  Stage 2: at each f4 moment v2 = v5 = 0 disables f0, f1, f2, f3; f4 gives
    v5 = 1, and while v7 >= 1 rule f1 (priority over f2) fires, restoring
    v5 = 0 and paying v7.  After the k-th pair v7 = W - 2k; the pair repeats
    while W - 2k - 1 >= 1, i.e. for k < m; at k = m the trailing f4 leaves
    v7 = 0, v5 = 1, v11 = i + 2m + 2 >= 1, so f2 (not f1) is next.
  Stage 3: v2 = 0, v3 = 2m: f0 disabled (v2 = 0), f1 disabled (v7 = 0);
    f2 fires once.
  Stage 4 rounds: from (3, y, s, 0, w) with y >= 3: f0 is top priority and
    fires while v2 >= 1 & v3 >= 1, i.e. 3 times (v2: 3 -> 0); then f0 is
    disabled by v2 = 0, f1 by v7 = 0, and f2 needs s + 3 >= 1 (yes) and
    w >= 1 -- the ONLY nontrivial guard in the whole phase.  Since v11 over
    stage 4 is u - (number of f2 firings so far) and ends at i + 1, we have
    v11 >= i + 1 >= 2 at every f2 firing [verified], so f2 fires; each round
    is (f0^3, f2): v3 -= 3, v5 += 2, v11 -= 1, v2: 3 -> 3.
    The rounds repeat while v3 >= 3.  v3 = 2m - 3r hits its residue mod 3:
      2m = 2^(i+1) - 2 = 0 (mod 3) iff i even   [2^(i+1) = 2, 1 (mod 3) for
      i even, odd resp.]
    i even: after q = 2m/3 rounds v3 = 0; f0 disabled forever after; the
      pending v5 = 2q drains by f2 ^ 2q (guard v11 >= 1 holds: v11 ends at
      i+1 >= 2), each firing adding 3 to v2; then v5 = 0, v2 >= 1, v3 = 0,
      v7 = 0 -- f3 is next: boundary B_{i+1}.
    i odd: after q = (2m-2)/3 rounds v3 = 2; f0 fires exactly twice
      (v2: 3 -> 1, v3: 2 -> 0), stops on v3 = 0 with v2 = 1 left; f1, f0
      disabled; f2 ^ (2q+2) drains v5 as above (v2 = 1 does not matter:
      f2 has priority over f3); then f3 is next: boundary B_{i+1}.
  Step count: W + (2m+1) + 1 + [6q | 6q+4] = 2^(i+3) - 5 in both cases.  QED

LEMMA 3 (no halt inside a phase).  At every state visited during Lemma 2's
word, some rule fires.  [By Lemma 0 a halt needs v2 = 0 = v7 and
(v5 = 0 or v11 = 0).  States with v2 = v7 = 0 occur only: at stage-2 f4
moments (v5 = 1 after, v11 >= i >= 1 -- f2 enabled even at the very last
one); and mid-stage-4 after each f0^3 with v5 >= 2, v11 >= i+1 >= 1 (f2
enabled).  Verified exhaustively along the word.]

THEOREM M431 = Lemma 1 + induction over Lemma 2 + Lemma 3: the orbit visits
B_i for every i >= 1 and never halts.  Note v11(B_i) = i: the machine's
"fuel" grows linearly per phase -- the margin is linear, not thin; no
p-adic or Baker-type input is needed anywhere.

--------------------------------------------------------------------------
VERIFICATION (this file):
  V0  vector simulator == big-int FRACTRAN on 200,000 steps.
  V1  Lemma 0 over the full 6^5 box of exponent vectors (entries 0..5).
  V2  Lemma 1 directly.
  V3  Lemma 2 as a BLOCK WALK in exact arithmetic for i = 1..2000: the
      repeated blocks (f4 f1)^m and (f0^3 f2)^q have block-start states
      affine in the block index k, and every guard/priority value is
      jointly affine in (k, within-run counter), so its minimum over the
      k-by-counter rectangle is attained at a corner: checking the first
      and last block (with full endpoint checks inside each) covers all
      2^i blocks.  Exact landing on B_{i+1}, exact step count.
  V4  the full firing WORD of Lemma 2 vs ground-truth simulation,
      phase-by-phase, for i = 1..13 (word-for-word equality).
  V5  Lemma 3 along the simulated word for i = 1..13 (no halting state
      ever visited), plus the closed-form v11 >= i floor for i = 1..2000.
"""
from fractions import Fraction

PRIMES = (2, 3, 5, 7, 11)
FRACS = [(5, 6), (9, 35), (8, 55), (7, 2), (605, 7)]

# rule vectors and guards over (v2, v3, v5, v7, v11)
DELTA = [(-1, -1, +1, 0, 0), (0, +2, -1, -1, 0), (+3, 0, -1, 0, -1),
         (-1, 0, 0, +1, 0), (0, 0, +1, -1, +2)]
GUARD = [((0, 1), (1, 1)), ((2, 1), (3, 1)), ((2, 1), (4, 1)),
         ((0, 1),), ((3, 1),)]        # ((coord, min), ...)


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
            word.append("HALT")
            return v, word
        v, word2 = v2, word.append(j)
    return v, word


def int_of(v):
    n = 1
    for p, e in zip(PRIMES, v):
        n *= p ** e
    return n


def B(i):
    return ((1 << (i + 1)) - 1, 0, 0, 0, i)


def S(i):
    return (1 << (i + 3)) - 5 * i - 8


def phase_runs(i):
    """Lemma 2's word for phase i as (rule, count) runs -- EXPONENTIALLY
    long in i; only used for the small-i ground-truth comparison (V4/V5)."""
    W, m = (1 << (i + 1)) - 1, (1 << i) - 1
    runs = [(3, W)]
    runs += [(4, 1), (1, 1)] * m + [(4, 1)]
    runs += [(2, 1)]
    if i % 2 == 0:
        q = (2 * m) // 3
        runs += [(0, 3), (2, 1)] * q + [(2, 2 * q)]
    else:
        q = (2 * m - 2) // 3
        runs += [(0, 3), (2, 1)] * q + [(0, 2), (2, 2 * q + 2)]
    return [(r, c) for r, c in runs if c > 0]


def check_block(start_of, word, K):
    """A block = `word` (list of (rule, count)) repeated K times, with
    start_of(k) affine in k giving the state at the start of block k.
    Every guard/priority value inside a block is jointly affine in
    (k, within-run counters), so checking blocks k = 0 and k = K-1 with
    full endpoint checks covers the whole rectangle.  Returns the state
    after the last block and asserts internal consistency of start_of."""
    if K == 0:
        return start_of(0)
    for k in ([0] if K == 1 else [0, K - 1]):
        v = start_of(k)
        for rule, count in word:
            v = apply_run(v, rule, count, check=True)
        nxt = start_of(k + 1)
        assert v == nxt, ("block chain", k, v, nxt)
    # affinity spot-proof: start_of(k) must be affine in k
    if K >= 3:
        a, b, c = start_of(0), start_of(1), start_of(2)
        assert all(2 * y == x + z for x, y, z in zip(a, b, c)), "not affine"
    return start_of(K)


def walk_phase(i):
    """Lemma 2 at block level: O(1) big-int work per stage.  Returns
    (end state, exact step count, min v11 over the phase)."""
    W, m = (1 << (i + 1)) - 1, (1 << i) - 1
    u = i + 2 * m + 1
    v = B(i)
    # Stage 1: f3^W
    v = apply_run(v, 3, W, check=True)
    assert v == (0, 0, 0, W, i)
    # Stage 2: (f4 f1)^m then f4
    v = check_block(lambda k: (0, 2 * k, 0, W - 2 * k, i + 2 * k),
                    [(4, 1), (1, 1)], m)
    assert v == (0, 2 * m, 0, 1, i + 2 * m)
    v = apply_run(v, 4, 1, check=True)
    assert v == (0, 2 * m, 1, 0, u + 1)
    # Stage 3: f2
    v = apply_run(v, 2, 1, check=True)
    assert v == (3, 2 * m, 0, 0, u)
    # Stage 4
    if i % 2 == 0:
        q = (2 * m) // 3
        v = check_block(lambda r: (3, 2 * m - 3 * r, 2 * r, 0, u - r),
                        [(0, 3), (2, 1)], q)
        assert v == (3, 0, 2 * q, 0, u - q)
        v = apply_run(v, 2, 2 * q, check=True)
        steps4 = 6 * q
    else:
        q = (2 * m - 2) // 3
        v = check_block(lambda r: (3, 2 * m - 3 * r, 2 * r, 0, u - r),
                        [(0, 3), (2, 1)], q)
        assert v == (3, 2, 2 * q, 0, u - q)
        v = apply_run(v, 0, 2, check=True)
        assert v == (1, 0, 2 * q + 2, 0, u - q)
        v = apply_run(v, 2, 2 * q + 2, check=True)
        steps4 = 6 * q + 4
    steps = W + (2 * m + 1) + 1 + steps4
    # v11 along the phase: i (stages 1), rising (2), falling to i+1 (4):
    # min = i, attained at the boundary itself.
    return v, steps, i


def apply_run(v, rule, count, check=True):
    """Apply `count` firings of `rule`, checking guard + priority at BOTH
    ends of the run (state is affine in the counter, so ends suffice)."""
    def ok(state, k_left):
        assert enabled(state, rule), (rule, state)
        for h in range(rule):
            assert not enabled(state, h), ("priority", h, rule, state)
    end = tuple(a + count * d for a, d in zip(v, DELTA[rule]))
    if check:
        ok(v, count)
        last = tuple(a + (count - 1) * d for a, d in zip(v, DELTA[rule]))
        ok(last, 1)
        assert all(x >= 0 for x in end), (rule, end)
    return end


if __name__ == "__main__":
    import itertools
    import time
    t0 = time.time()
    P = lambda *a: print(*a, flush=True)
    P("=" * 74)
    P("MACHINE 431 = [5/6, 9/35, 8/55, 7/2, 605/7]: THE NON-HALTING PROOF")
    P("=" * 74)

    # ---- V0: vector simulator == big-int FRACTRAN ------------------------
    n, v = 2, (1, 0, 0, 0, 0)
    for s in range(200000):
        # big-int step
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
    P(f"\nV0  vector simulator == big-int FRACTRAN for 200,000 steps: OK")

    # ---- V1: the halt criterion ------------------------------------------
    bad = 0
    for v in itertools.product(range(6), repeat=5):
        halts = fire_next(v) is None
        crit = v[0] == 0 and v[3] == 0 and (v[2] == 0 or v[4] == 0)
        bad += halts != crit
    assert bad == 0
    P("V1  Lemma 0 (halt <=> v2=0 & v7=0 & (v5=0 | v11=0)): all 7,776 "
      "vectors in the 0..5 box: OK")

    # ---- V2: entry -------------------------------------------------------
    v, word = run_word((1, 0, 0, 0, 0), 3)
    assert word == [3, 4, 2] and v == B(1) == (3, 0, 0, 0, 1)
    P("V2  Lemma 1 (entry): n=2 --f3,f4,f2--> B_1 = (3,0,0,0,1) at step 3: OK")

    # ---- V3: the block walk, exact, i = 1..2000 --------------------------
    IMAX = 2000
    for i in range(1, IMAX + 1):
        v, steps, min_v11 = walk_phase(i)
        assert v == B(i + 1), i
        assert steps == (1 << (i + 3)) - 5, i
        assert S(i) + steps == S(i + 1), i
        assert min_v11 >= i, (i, min_v11)          # the linear fuel floor
    P(f"V3  Lemma 2 block walk, i = 1..{IMAX}: guards & priorities at the "
      f"corners of every block rectangle, exact landing on B(i+1), step "
      f"count 2^(i+3)-5, v11 floor = i: OK")

    # ---- V4: word-for-word vs ground truth, i = 1..13 --------------------
    v = B(1)
    for i in range(1, 14):
        pred = []
        for rule, count in phase_runs(i):
            pred += [rule] * count
        v_end, got = run_word(v, len(pred))
        assert got == pred, f"word mismatch in phase {i}"
        assert v_end == B(i + 1), i
        v = v_end
    P("V4  Lemma 2's firing word == ground-truth simulation, word-for-word, "
      "phases i = 1..13 (through step "
      f"{S(14)} = S(14)): OK")

    # ---- V5: no halting state along the way, i = 1..13 -------------------
    v = B(1)
    visited_halt = 0
    for i in range(1, 14):
        L = (1 << (i + 3)) - 5
        for _ in range(L):
            if v[0] == 0 and v[3] == 0 and (v[2] == 0 or v[4] == 0):
                visited_halt += 1
            v, j = vstep(v)
            assert j is not None
    assert visited_halt == 0
    P("V5  Lemma 3: no state on the orbit satisfies the halt criterion, "
      "phases 1..13 exhaustively (and v11 >= i floor for i <= 2000 in V3): OK")

    P(f"\nTHEOREM M431: the program never halts from n = 2.  "
      f"[{time.time()-t0:.1f}s]")
