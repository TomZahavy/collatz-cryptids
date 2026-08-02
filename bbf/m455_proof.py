"""BBf(23) holdout #455  [63/10, 8/77, 33/2, 5/9, 7/3]  NEVER HALTS.

THEOREM (M455).  The FRACTRAN program F = [63/10, 8/77, 33/2, 5/9, 7/3],
started at n = 2, never halts.  [proved; every step machine-verified below]

State = exponent vector (v2, v3, v5, v7, v11) over the primes (2,3,5,7,11)
-- no other prime occurs.  Rules in priority order:

    f0 = 63/10 : (v2--, v3+=2, v5--, v7++)   guard  v2>=1 & v5>=1
    f1 = 8/77  : (v2+=3, v7--, v11--)        guard  v7>=1 & v11>=1
    f2 = 33/2  : (v2--, v3++, v11++)         guard  v2>=1
    f3 = 5/9   : (v3-=2, v5++)               guard  v3>=2
    f4 = 7/3   : (v3--, v7++)                guard  v3>=1

LEMMA 0 (halt criterion).  No rule fires  <=>  v2 = 0 and v3 = 0 and
(v7 = 0 or v11 = 0).   [f2 subsumes f0's v2; f4 subsumes f3's v3.]

LEMMA 1 (entry).  From n = 2 = (1,0,0,0,0) the word
f2 f4 f1 f2^3 f3 f4 f1 f0 f1 (11 steps) reaches (5,2,0,0,1) with f2 next.

BOUNDARY (i >= 2), with X := 2^i:   B_i := (X+1, X-2, 0, 0, i-1), f2 next.
Lemma 1 says B_2 is reached at step 11 = S(2), where S(i) := 2^(i+2) - 5.

LEMMA 2 (one phase).  For every i >= 2, from B_i the program executes
exactly the following word, in 4X steps, arriving at B_{i+1}:

  Stage A   f2 ^ (X+1)     (X+1, X-2, 0, 0, i-1) -> (0, 2X-1, 0, 0, X+i)
  Stage B   f3 ^ (X-1)     -> (0, 1, X-1, 0, X+i)
  Stage C   f4             -> (0, 0, X-1, 1, X+i)
  Stage D   f1             -> (3, 0, X-1, 0, X+i-1)
  Stage E   rounds of (f0^3, f1); round r (0-indexed) starts at
                (3, 6r, X-1-3r, 2r, X+i-1-r)                  [affine in r]
    i even  (X = 1 mod 3, R := (X-1)/3):
                (f0^3 f1)^(R-1)  ->  round R-1 start, v5 = 3
                f0^3             ->  (0, 2X-2, 0, 2R+1, X+i-R)
                f1^L, L := 2R+1 = (2X+1)/3   [= v7: drains it to 0 exactly]
                                 ->  (3L, 2X-2, 0, 0, i) = B_{i+1}
    i odd   (X = 2 mod 3, F := (X-2)/3):
                (f0^3 f1)^F      ->  (3, 2X-4, 1, 2F, X+i-1-F)
                f0^1             ->  (2, 2X-2, 0, 2F+1, X+i-1-F)
                                     [single: v5 = 1 runs out, not v2]
                f1^L, L := 2F+1 = (2X-1)/3   [= v7 again]
                                 ->  (2+3L, 2X-2, 0, 0, i) = B_{i+1}
  (Even: 3L = 2X+1.  Odd: 2+3L = 2X+1.  Both = X'+1 with X' = 2X.  QED shape.)

PROOF.  Every guard/priority value is jointly affine in the round index and
within-run counter, so corner checks cover each block (as in m431_proof).
The nontrivial facts, all verified:
  - Stage A: v5 = v7 = 0 disables f0, f1 throughout; f2 runs v2 out.
  - Stage B: v3 = 2X-1 odd, so f3 stops at v3 = 1 exactly; v2 = 0 disables
    f0, f2; v7 = 0 disables f1.
  - Stage E rounds: f0 is top priority and stops each time because v2 = 0
    (v5 = X-1-3r stays >= 3 through round R-2 resp. F-1); at the f1
    moments v2 = 0, v7 = 2r+3 >= 1, v11 >= i+1 >= 1.
  - The endgame split: at the last round v5 hits 3 (i even: one full f0^3)
    or 1 (i odd: f0 fires ONCE, stopped by v5 = 0 with v2 = 2 left).
  - The final f1-run: f0 is disabled by v5 = 0 even as v2 grows by 3 per
    firing; its length is forced to be exactly v7 = 2R+1 resp. 2F+1
    (f1 stops on v7 = 0), and v11 lands on exactly i.
  - Then (v2, v5, v7) = (2X+1, 0, 0): f0, f1 disabled, f2 next: B_{i+1}.
  Step count: (X+1) + (X-1) + 1 + 1 + [4(R-1)+3+L | 4F+1+L] = 4X both.  QED

LEMMA 3 (no halt inside a phase).  Halting needs v2 = 0 = v3 (Lemma 0).
On the word, v2 = v3 = 0 occurs only at the stage C/D hinge, where
v7 = 1 and v11 = X + i >= 1 keep f1 enabled.  [verified exhaustively]

FUEL.  min v11 over phase i is i - 1 (attained at B_i itself): the margin
grows linearly, exactly as in machine 431; no thin condition anywhere.

THEOREM M455 = Lemma 1 + induction over Lemma 2 + Lemma 3.

VERIFICATION: V0 vector==bigint sim; V1 halt box; V2 entry; V3 block walk
i = 2..2000 (corner checks, exact landing, steps = 4X, v11 floor);
V4 word-for-word vs ground truth i = 2..12; V5 no-halt along phases 2..12.
"""

PRIMES = (2, 3, 5, 7, 11)
FRACS = [(63, 10), (8, 77), (33, 2), (5, 9), (7, 3)]
DELTA = [(-1, +2, -1, +1, 0), (+3, 0, 0, -1, -1), (-1, +1, 0, 0, +1),
         (0, -2, +1, 0, 0), (0, -1, 0, +1, 0)]
GUARD = [((0, 1), (2, 1)), ((3, 1), (4, 1)), ((0, 1),), ((1, 2),),
         ((1, 1),)]


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
    X = 1 << i
    return (X + 1, X - 2, 0, 0, i - 1)


def S(i):
    return (1 << (i + 2)) - 5


def apply_run(v, rule, count, check=True):
    """count firings of rule; guard + priority checked at both run ends
    (state affine in the counter)."""
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
    """word repeated K times; start_of(k) affine in k; corners cover all."""
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
    """Lemma 2's word as (rule, count) runs -- exponential in i; V4/V5 only."""
    X = 1 << i
    runs = [(2, X + 1), (3, X - 1), (4, 1), (1, 1)]
    if i % 2 == 0:
        R = (X - 1) // 3
        runs += [(0, 3), (1, 1)] * (R - 1) + [(0, 3), (1, (2 * X + 1) // 3)]
    else:
        F = (X - 2) // 3
        runs += [(0, 3), (1, 1)] * F + [(0, 1), (1, (2 * X - 1) // 3)]
    return [(r, c) for r, c in runs if c > 0]


def walk_phase(i):
    """Lemma 2 at block level; returns (end state, steps, min v11)."""
    X = 1 << i
    v = B(i)
    v = apply_run(v, 2, X + 1)
    assert v == (0, 2 * X - 1, 0, 0, X + i)
    v = apply_run(v, 3, X - 1)
    assert v == (0, 1, X - 1, 0, X + i)
    v = apply_run(v, 4, 1)
    v = apply_run(v, 1, 1)
    assert v == (3, 0, X - 1, 0, X + i - 1)

    def round_start(r):
        return (3, 6 * r, X - 1 - 3 * r, 2 * r, X + i - 1 - r)
    if i % 2 == 0:
        R = (X - 1) // 3
        v = check_block(round_start, [(0, 3), (1, 1)], R - 1)
        v = apply_run(v, 0, 3)
        L = (2 * X + 1) // 3
        assert v == (0, 2 * X - 2, 0, L, X + i - R), v
        v = apply_run(v, 1, L)
        steps = (X + 1) + (X - 1) + 2 + 4 * (R - 1) + 3 + L
    else:
        F = (X - 2) // 3
        v = check_block(round_start, [(0, 3), (1, 1)], F)
        v = apply_run(v, 0, 1)
        L = (2 * X - 1) // 3
        assert v == (2, 2 * X - 2, 0, L, X + i - 1 - F), v
        v = apply_run(v, 1, L)
        steps = (X + 1) + (X - 1) + 2 + 4 * F + 1 + L
    return v, steps, i - 1        # v11 floor = i-1, at the boundary itself


if __name__ == "__main__":
    import itertools
    import time
    t0 = time.time()
    P = lambda *a: print(*a, flush=True)
    P("=" * 74)
    P("MACHINE 455 = [63/10, 8/77, 33/2, 5/9, 7/3]: THE NON-HALTING PROOF")
    P("=" * 74)

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
    P("\nV0  vector simulator == big-int FRACTRAN for 200,000 steps: OK")

    # ---- V1 --------------------------------------------------------------
    bad = 0
    for v in itertools.product(range(6), repeat=5):
        halts = fire_next(v) is None
        crit = v[0] == 0 and v[1] == 0 and (v[3] == 0 or v[4] == 0)
        bad += halts != crit
    assert bad == 0
    P("V1  Lemma 0 (halt <=> v2=0 & v3=0 & (v7=0 | v11=0)): all 7,776 "
      "vectors in the 0..5 box: OK")

    # ---- V2 --------------------------------------------------------------
    v, word = run_word((1, 0, 0, 0, 0), 11)
    assert word == [2, 4, 1, 2, 2, 2, 3, 4, 1, 0, 1] and v == B(2), (v, word)
    P("V2  Lemma 1 (entry): n=2 reaches B_2 = (5,2,0,0,1) at step 11 = S(2): "
      "OK")

    # ---- V3 --------------------------------------------------------------
    IMAX = 2000
    for i in range(2, IMAX + 1):
        v, steps, min_v11 = walk_phase(i)
        assert v == B(i + 1), i
        assert steps == 4 * (1 << i), i
        assert S(i) + steps == S(i + 1), i
        assert min_v11 == i - 1 >= 1, i
    P(f"V3  Lemma 2 block walk, i = 2..{IMAX}: corner guard/priority checks, "
      f"exact landing on B(i+1), step count 4X, v11 floor i-1: OK")

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
    P(f"V4  Lemma 2's firing word == ground-truth simulation, word-for-word, "
      f"phases i = 2..12 (through step {S(13)} = S(13)): OK")

    # ---- V5 --------------------------------------------------------------
    v = B(2)
    visited_halt = 0
    for i in range(2, 13):
        for _ in range(4 * (1 << i)):
            if v[0] == 0 and v[1] == 0 and (v[3] == 0 or v[4] == 0):
                visited_halt += 1
            v, j = vstep(v)
            assert j is not None
    assert visited_halt == 0
    P("V5  Lemma 3: no state on the orbit satisfies the halt criterion, "
      "phases 2..12 exhaustively: OK")

    P(f"\nTHEOREM M455: the program never halts from n = 2.  "
      f"[{time.time()-t0:.1f}s]")
