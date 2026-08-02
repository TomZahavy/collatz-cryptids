# WS1 — automatic non-halting certificates for the Space Needle

**Question.** Is there a 2-automatic set `I` (recognised by a DFA reading binary
digits, LSB-first, on minimal words) with

    6 in I,    F(I) subset of I,    I cap H = empty,        H = {1,2,4,8,...}

for the Space Needle map `F`? Such an `I` is a finite, machine-checkable proof
that the orbit of 6 never halts. It is the one certificate class our
no-congruence theorems do not exclude.

## The enabling identity (proved + machine-verified)

    F(x) = x + 3*(x >> (v+1)) + v = (2^(v+1) + 3)*k + (2^v + v),
    where v = v_2(x) and k = x >> (v+1),  i.e. x = 2^(v+1) k + 2^v.

Each valuation branch is **affine in k**, so branch closure for a fixed DFA is
computed exactly by a finite product (DFA-state on x) x (carry) x (DFA-state on
y). Verified against `needle.step1` for all non-powers-of-2 below 300,000.

**Local-action lemma** (proved; disjoint bit ranges): if `3k + v < 2^v` then the
LSB word of `F(x)` is `(v+3k) in v bits . 1 . w(k)` — the tail `k` is untouched,
only the zero block is rewritten, and `v_2(F(x)) = v_2(3k+v)`.

## Results (exhaustive, machine-verified)

| states | structures | certificate for orbit of 6 | any nonempty F-invariant avoiding H |
|---|---|---|---|
| 1–5 | 160,675 | none | none |
| 6 | 5,931,540 | none | none |
| 7 | 256,182,290 | none | (not run) |

Both are complete searches: every isomorphism class of transition structure is
visited once, and for each, whether *any* acceptance labelling works is decided
exactly by Horn propagation. Only branches `v <= V` are imposed, which is sound
for impossibility (a subset of the closure requirement); `v <= 1` already
suffices at every size tested.

## The obstruction is dynamical, not a failure to see

| states | structures | separate the orbit from H | survive closure |
|---|---|---|---|
| 3 | 216 | 4 | 0 |
| 4 | 5,248 | 100 | 0 |
| 5 | 160,675 | 2,887 | 0 |

Every separating structure dies at the **first** closure step (all 504 audited
chains have length 1). Mechanism, always the same shape: some `x` shares a state
with an orbit element, so `x` must be in `I`, and `F(x)` is (or shares a state
with) a power of 2. Example, `delta = [[0,1],[1,2],[1,3],[1,2]]`: orbit element
101 and 7 share state 3; `F(7) = 16 = 2^4`.

So the real requirement is avoiding the whole **halting basin**
`H* = union_j F^-j(H)`, not just `H`. The theorem reads: at these sizes no
finite-state partition of the integers separates the orbit of 6 from the
halting basin — the automatic generalisation of our no-congruence theorems
(a congruence class is the degenerate automatic set).

## Calibration

The same code finds a genuine certificate for the control machine `C(x) = 4x`
(same halting set, same branch format) at **2 states**: `I = {x : even number of
1 bits}`, re-verified by brute force against the actual map for `x < 200,000`.
So the machinery succeeds when a certificate exists.

## Past the enumeration wall: the SAT encoding (July 27, 2026)

The transition structure itself becomes SAT variables (`T[s][c][t]`, `A[s]`),
plus a reachability variable per product state — the arithmetic analogue of
bbchallenge's FAR `mitm_dfa`. Two design points make it work:

- **Only the FORWARD closure of the product reachability is encoded.** That
  forces `R` to *contain* the reachable set but permits `R = reach`, which does
  satisfy forward closure — so a real certificate always yields a satisfying
  assignment, and `UNSAT` is a sound impossibility proof. An over-approximating
  `R` would impose the pair implication on unreachable states and could report
  UNSAT spuriously.
- **BFS-canonical symmetry breaking** (the ICDFA canonical form, as clauses)
  removes the `n!` relabellings. This took n=7 from 47.8s to 0.1s.

| machine | convention | exhaustive reach | SAT reach | last size, time |
|---|---|---|---|---|
| Space Needle (base 2) | minimal words (general) | 7 states | **11 states** | n=11, 16,538 s |
| Space Needle (base 2) | all representations (0-invariant) | — | **13 states** | n=13, 12,284 s |
| Machine 3 (base 3) | minimal words (general) | 4 states | **7 states** | n=7, 12,018 s |

All UNSAT. Machine 3's n=5 took 18 s by SAT against an ~1 hour estimate by
enumeration. The per-state cost factor is what sets each wall's position, and
**it rises within every series** — 5.5–15.9x on the needle's general convention
(2.8, 18.4, 102, 1041, 16,538 s for n=7..11), 18.5x on the last 0-invariant step
(662 s at n=12, 12,284 s at n=13), and 53.2x on machine 3's last step (226 s at
n=6, 12,018 s at n=7). Each further state is a day, then a week. The full
four-series table and what follows from it are below, under the MSB search.

### Handing the solver the halting basin does not move the wall (July 27, 2026)

WS1's own finding is that a certificate must avoid the whole basin
`union_j F^-j(H)`, and WS2 enumerates that basin exactly (`basin.py`; F expands,
so the backward tree below a cap is finite and complete — 80 elements below
2^40, of which 39 are not powers of 2). Since `x in basin => x not in I` is
*implied* by the existing constraints, adding it as unit clauses cannot change
the satisfying assignments: the theorem proved at each size is identical and
only the solver's work changes. Measured at n=9, interleaved to spread load:

| clauses added | run 1 | run 2 | run 3 | ratio to baseline |
|---|---|---|---|---|
| baseline (`2n+6` powers of 2) | 116.1 s | 160.4 s | 198.6 s | — |
| more powers of 2 only (< 2^40) | 157.2 s | 197.3 s | 192.4 s | 1.35, 1.23, 0.97 |
| full basin (< 2^40) | 92.1 s | 116.0 s | 104.1 s | **0.79, 0.72, 0.52** |

The machine was running five other jobs throughout, so absolute times are noisy
— which is why the runs are interleaved and reported individually rather than
averaged. The direction is consistent in all three: the basin helps by roughly a
quarter to a third, and extra halt values carrying no new information do not
help at all. But against a per-state factor of 5.5–18.5x, a 30% saving buys
about **one-eighth of a state**. The prediction that this would move the wall by
several states was wrong by an order of magnitude. Recorded as a negative
result, and as a corrective: the wall is not made of missing information, it is
made of search space.

**Cross-validated, not trusted.** `sat_validate.py` compares SAT against the
exhaustive enumeration for every machine, size and branch depth where both can
run — 30/30 agreements in base 2 (both conventions) and 12/12 in base 3 — and
every certificate SAT produces is re-verified by direct simulation against the
actual map. Two encoding bugs were caught this way and fixed: on a nonzero
digit the product must branch into *both* "the tail ends here" and "the tail
continues" (taking only the first restricted the tail to a single nonzero
digit), and the first symmetry-breaking attempt wrongly forced `delta(0,0)=0`.

## Reading from the other end: the MSB-first search (July 27, 2026)

Every bound above is on **LSB-first** state count. An MSB automaton for the same
set can be exponentially smaller, so those bounds say little about small MSB
certificates — and the structure this program independently found to govern
these machines (the mantissa backbone, the `log2(5/4)` circle map) is a
*leading-digit* phenomenon, exactly the kind an LSB automaton cannot express
compactly. `NEXT_STEPS.md` listed this as blocked, on the grounds that the
branch relation is not MSB-synchronous. **It is synchronous, for every machine
in the family.**

**Proposition** (proved; verified on both machines, 299,987 and 299,980 values,
0 violations). For any branch-affine machine — `x = q^|p| m + val(p)`,
`F(x) = A_p m + B_p` — eliminating `m` gives a single linear equation with a
constant right-hand side:

    q^|p| * F(x)  -  A_p * x  =  q^|p| B_p - A_p val(p)  =:  C_p.

Read `x` and `F(x)` in parallel MSB-first, left-padded, and track
`R_i = q^|p| y_i - A_p x_i`. Then `R_i = q R_{i-1} + q^|p| e_i - A_p d_i` and
`R_final = C_p`. The unread suffix contributes at most `(q^|p| + A_p)(q^{N-i}-1)`,
so `|R_i| <= |C_p| + q^|p| + A_p` along any pair that can still reach `C_p`, and
anything outside that box doubles away and never returns. So the branch relation
is a letter-to-letter transduction with finitely many states: no lookahead, no
delay. The only end-anchored condition, `v_q(x) = |p|-1`, is settled by a shift
register of the last `|p|` digits.

Consequences: the product state is `(state on x, state on y, R, shift)`, which
is **O(n²)**, against the LSB product's `O(n³)` — the LSB encoding must also
carry the "state after the last emitted nonzero digit" to support the
minimal-word convention. Measured, same machine, same branches, same n:

| n | LSB-first (general) | MSB-first | clauses LSB / MSB |
|---|---|---|---|
| 9 | 116.1 s | **4.5 s** | 2,522,209 / 710,584 |
| 10 | 1041.1 s | **24.6 s** | 4,178,899 / 1,060,220 |
| 11 | **16,538.3 s** | **164.9 s** | 6,617,663 / 1,527,455 |
| 12 | — | **1678.6 s** | — / 2,136,505 |
| 13 | — | **9174.1 s** | — / 2,913,890 |

All UNSAT: **no MSB-first leading-zero-invariant automatic certificate for the
Space Needle at ≤ 13 states**. MSB moves the wall by a state or two rather than
removing it — but it is a different, previously unbounded size measure, and it
is the one in which a positive result was most likely to hide.

> **How much that bound is actually worth** was settled later the same day, in
> WS4 (`formal/ws4/`). Converted into moduli — a congruence certificate mod m is
> a union of residue classes, recognised by **m** states MSB-first and
> **m·ord_m(2)** LSB-first — the ≤ 13 MSB bound rules out congruence
> certificates for m ≤ 13, and the ≤ 11 LSB bound rules out exactly
> **{2, 3, 4}**. A 30-second direct sweep rules out **every m ≤ 20,000, with any
> threshold**. The state count was never what made WS1 valuable; the
> halting-basin shape was.

**Two searches were deliberately abandoned, July 27, 2026** (not crashed, not
inconclusive-by-accident): the 0-invariant run at n=14 and the machine 3 run at
n=8, killed after the rising-factor measurement priced them at roughly 63 h and
178 h respectively. Neither result would have changed any claim here — each
would have moved one bound by one state in a series whose growth is already
recorded — so the cost bought nothing. The decision follows from the exchange
rate, and is the exchange rate's first practical use. Their completed rows
(n &le; 13 and n &le; 7) stand; the abandoned n are simply not claimed.

**The reach gain, measured on cumulative cost — and why it is not one number.**
MSB reached n=12 in 1,874 s of total search. At that same budget LSB stood at
n=10 (1,164 s cumulative), so the encodings deliver 10 and 12: **a gain of 2**,
and this was the datapoint the exchange rate (below) predicted before it
arrived. LSB then *completed* n=11, in 16,538.3 s. At that larger budget of
17,703 s LSB reaches 11 while MSB is still at 12 (its n=13 needs roughly
19,000 s cumulative), so the same comparison **reads 1**.

Both readings are correct; the gap is a function of the budget one fixes, which
was written down here *before* the n=11 run finished and is now confirmed. What
survives is the order of the answer — the best encoding change available is
worth one or two states, not an order of magnitude — which was the claim that
mattered. No particular number survives.

**But the per-state factor is not constant — it rises.** This was assumed flat
when the exchange rate was first written, and the assumption is wrong:

| series | per-state factors, in n order | last step |
|---|---|---|
| MSB (needle) | 3.00, 4.33, 3.46, 5.47, 6.70, 10.18, 5.47 | n=12→13 |
| LSB general (needle) | 7.00, 6.57, 5.53, 10.24, **15.89** | n=10→11 |
| LSB 0-invariant (needle) | 9.64, **18.55** | n=12→13 |
| Machine 3 (base 3) | 3.38, 12.62, **53.20** | n=6→7 |
| — *single load, one process* — | | |
| MSB (needle), re-measured | 2.73, 4.10, 6.91, 11.23, **13.12** | n=12→13 |
| LSB general (needle), re-measured | 4.30, 4.35, 5.55, **9.46** | n=9→10 |

The largest factor is the last one in **all four** series as measured at the
time (the MSB series has since gained an n=13 step reading 5.47x, on which see
the single-load note below) — and
machine 3's last step, 53.20x (226 s at n=6 to 12,018 s at n=7), is the
steepest measured anywhere in the program. Note it is a different machine with
a far larger encoding (73.2M clauses at n=7), so its absolute g is not
comparable to the Needle's; what transfers is the *direction*. Two
consequences. First, MSB's advantage was never a fixed constant: the ratio
LSB/MSB at matched n runs 4.00, 9.33, 14.15, 22.60, 42.32, **100.29** for
n = 6..11, so it compounds — MSB's per-state factor really is smaller, and the
compounding has not stopped. **This also breaks the formula's other input:**
log_g(C) takes C to be a constant improvement, but C is measured at a given n
and is itself growing, so both arguments drift. Two encodings with different
growth rates do not differ by a constant factor at all.

Second — and this **retracts** what stood here earlier — the claim that "the
wall re-formed with the same gradient" (MSB 10.18x against LSB's 10.24x) does
not survive the n=11 run. LSB's newest step costs **15.89x**, against MSB's
10.18x, so the two gradients are not equal and MSB remains the cheaper
encoding per state. The earlier reading compared MSB's latest step against an
LSB step that was no longer LSB's latest.

*Caveat on the timings:* these runs were made concurrently on a shared 10-core
machine at varying load, so cross-run absolute times carry perhaps ±30%. The
42x constant is far outside that; a single per-step factor of 6.70 vs 10.18 is
not. The claim that survives the noise is the qualitative one — the rise is
consistent across all four independent series.

**The caveat was not enough, and the fix changed a reading.** The n=13 MSB run
completed at **5.47x**, which looked like the rise reversing — except that two
competing multi-day jobs were killed partway through its window, so it ran on a
quieter box than n=12 did. That confound cannot be removed after the fact, so
WS4 re-measured under a single condition (`formal/ws4/clean_growth.py`: one
process, strictly sequential, load sampled at every instance). **The
contamination is about threefold** — MSB n=10 takes 7.9 s clean against 24.6 s
loaded — and under clean measurement **both** series come out strictly
monotone (MSB 2.73, 4.10, 6.91, 11.23, 13.12; LSB 4.30, 4.35, 5.55, 9.46), with
the ratio still compounding (18.98, 38.62, 89.23 at n = 8, 9, 10). The apparent
fall-back at n=13 is therefore **withdrawn**: it was load, not mathematics — and
clean, that step is the *largest* in the series. General rule now on the record: a completed UNSAT
survives a noisy box, but the constant that prices it does not.

Consequence for the exchange rate: computing `log_g(C)` from a *mean* g
overstates what a constant factor buys, and increasingly so with n. The inverse
figures quoted below (364x for 3 states, 18,590x for 5) are therefore
**optimistic** — the true cost is higher. This strengthens the conclusion that
no further states are worth buying; it does not weaken it.

**Convention.** Left padding forces leading-zero invariance, imposed as
`delta(q0, 0) = q0`. WLOG as a class: for any MSB-recognisable set of integers,
the minimal DFA of `0*L` has that property, since the residual of `0*L` by `0`
is `0*L` itself. As with the two LSB conventions this is a different *size
measure*, not a different class of sets.

**Cross-validated** (`msb_validate.py`), because the LSB encoding had two bugs
that only this caught:

1. the elimination identity against `needle.step1` — 198,430 values, `v <= 6`;
2. the product's emitted pairs against the true `(state(x), state(F(x)))` for
   random explicit DFAs: **0 missing pairs** (a missing pair weakens the
   constraint and would give spurious SAT). Ten of 120 DFAs emit *extra* pairs;
   all are accounted for — the `k = 0` pair, i.e. `x = 2^v`, which halts, so its
   `A` is forced false and the implication is vacuous — plus truncation of the
   enumeration. **0 unexplained.**
3. SAT verdict against brute-force enumeration of all `n`-state DFAs, n = 2,3,4:
   agree.
4. Calibration `C(x) = 4x` recovers a 2-state certificate,
   `delta=[[0,1],[1,0]] acc=[0]` (even number of 1 bits), then audited
   independently against the actual map for `x < 300,000`: start, closure and
   halt-disjointness violations all **0**.

## Are the impossibility results vacuous? (July 27, 2026)

Every result above is a completed `UNSAT`, which is a *complete* refutation — no
amount of solver slowness can undermine one, and "would it have found a
certificate in time?" is not the question. The failure mode that would hollow
them out is different: an encoding that is accidentally **over-constrained**
reports UNSAT for machines that *do* have certificates, and then every theorem
built on it is vacuous. Before WS4 leans on these bounds, that had to be ruled
out. The only calibration on record was `C(x) = 4x`, whose certificate has **2**
states — enough to show the search is not blind, not that it admits a 10-state
one.

**The instrument** (`calibrate.py`). Machines `G_m` keeping the Needle's own
multipliers `a_v = 2^(v+1)+3` and moving only the additive constant to
`b_v = a_v * inv2 mod m`. Then `m | x = 2^v(2k+1)` with `m` odd forces
`k ≡ -inv2 (mod m)`, so `G_m(x) = a_v k + b_v ≡ a_v(-inv2) + a_v inv2 = 0`: the
multiples of `m` are invariant, they miss the powers of 2, and a certificate
provably exists at exactly `m` states. **`m` must be prime** — for composite `m`
every odd divisor `d | m` gives a coarser invariant `I_d`, and indeed `m = 9`
was solved at `n = 3` by the multiples-of-3 certificate rather than at 9.

**Answered by construction, not by search** (`adequacy.py`). The SAT side of a
space this size is far slower than the UNSAT side — planted `k = 11` took 2803 s
(LSB) and 213 s (MSB) to *find*, against 36 s to *refute* `n = 10` — so a
search-based probe gets expensive exactly where the answer matters. Instead:
take the planted certificate, build the assignment it induces, and check the
formula family by family (transitions hold by construction; symmetry breaking
iff the DFA is BFS-canonical; units iff the orbit is accepted and no power of 2
is; closure iff every emitted pair preserves acceptance). No solver involved.

| planted size k | 3 | 5 | 7 | 11 | 13 | 17 | 19 | 23 |
|---|---|---|---|---|---|---|---|---|
| LSB-first, minimal words | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| MSB-first, leading-zero-inv. | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Both encodings admit a certificate at every one of those sizes — covering and
exceeding all three claimed bounds (11, 13, 12). **The impossibility results are
not artefacts of an over-constrained encoding.**

The search-based calibration agrees, and independently pins the minima:

| planted k | LSB, first found at | MSB, first found at |
|---|---|---|
| 3 | n=3, 0.0 s | n=3, 0.1 s |
| 5 | n=5, 0.5 s | n=5, 0.6 s |
| 7 | n=7, 7.1 s | n=7, 3.8 s |
| 11 | **n=11, 2802.8 s** | **n=11, 213.4 s** |

Found at exactly `n = k` every time, with UNSAT at every `n < k` — so `k` is the
true minimum, with no appeal to the construction. The MSB certificate recovered
at k=11 is literally the residue automaton `r -> 2r + d mod 11`. (An early run
of `calibrate.py`, before the prime-only fix, shows `k = 9` solved at `n = 3`:
that is the composite-`m` flaw above, caught live.)

A caveat worth recording for the next phase: the SAT/UNSAT asymmetry means this
machinery will keep producing *negative* answers efficiently and may never
produce a positive one. At `n ≥ 11` a refutation costs minutes and finding a
certificate that exists costs hours or more. So "no certificate at ≤ N states"
will go on getting cheaper to extend than "here is one" — which is a bias in the
evidence this program generates, not a fact about the machines.

## Honest limits

- Nothing here bounds certificates of unbounded size. The general conjecture
  ("every nonempty 2-automatic F-invariant meets H") is open.
- ~~The bound is on LSB-first state count... a direct MSB search is a real gap
  until done.~~ **Closed** — the MSB search has been run, to 13 states, on the
  size measure the LSB bounds do not constrain (see above). What is left of this
  caveat is only that 12 is a bound, not an impossibility.
- The three conventions are different *size measures*, not different classes of
  set: every 2-automatic set admits a trailing-zero-invariant DFA, possibly with
  more states. So the 13-state 0-invariant, 11-state minimal-word and 12-state
  MSB bounds are each genuine, and none subsumes another.
- SAT cost per state is **not** a fixed factor: it rises with n, reaching
  10.2x (MSB), 10.2x (LSB general) and 18.6x (0-invariant) at the last measured
  step of each. So each further state is dearer than the one before, and the
  wall is pushed out by a couple of states rather than removed.

## Files

- `dfa_invariant.py` — machinery + tests (branch algebra, exact pair sets, ICDFA
  enumeration). Run standalone to check.
- `search.py` — certificate search for the orbit of 6. `python3 search.py needle 6 6`
- `anystart.py` — start-free search. `python3 anystart.py 5 4`
- `witness.py` — extracts and independently audits refutation witnesses.
- `strength.py` — separation-vs-closure decomposition.
- `verify.py` — calibration and diagnostics.
- `sat_search.py` — the base-2 SAT search. `python3 sat_search.py needle 1 11 1`
- `sat_generalq.py` — the base-q SAT search (machine 3 via `run_m3_sat.py`).
- `sat_validate.py` — cross-validation of SAT against the exhaustive search.
- `make_ws1_report.py` / `ws1_report.pdf` — the write-up.
