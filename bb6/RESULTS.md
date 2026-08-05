# BB(6) port — results, Aug 3 2026

Porting the rigid-certificate method from FRACTRAN holdouts to the
BB(6) Turing-machine holdout list (`bbf/bb6_holdouts_1064.txt`, mxdys,
July 28 2026, 1,064 machines up to equivalence).

## The simulator stack (all step-exact, cross-checked)

| file | what | verification |
|---|---|---|
| `tm.py` | cell-at-a-time simulator | all four BB champions exact; BB(5) = 47,176,870 steps / 4,098 ones |
| `blocktape.py` | chain-step acceleration | step-exact vs `tm.py`, 3,000 random machines + 60 holdouts, tape-identical |
| `macro.py` | Marxen–Buntrock macro machines, b = 1..6 | 3,454 machine/block-size pairs cross-checked |
| `rigid.py` | single-level rigidity detector | BB(5) control; exact EXP/POLY fitting |
| `twolevel.py` | inner recurrence + outer map | BW positive control recovers `x -> 3x + 4` |
| `cryptid.py` | measures the three cryptid criteria | BW reads CRYPTID-SHAPED |

**Measured negative:** chain steps alone give ~1.2x on this list — these
machines have almost no base-level self-loops. Macro machines give
~1,900x on BB(5). Recorded so it is not re-derived.

## Census 1 — single-level rigidity (all 1,064, 3,191 s)

| class | count | share |
|---|---|---|
| NONRIGID | 626 | 58.8% |
| FEWPHASE | 431 | 40.5% |
| GEO | 4 | 0.4% |
| UNCONFIRMED | 3 | 0.3% |

Two filters make this number mean anything, and without them the
detector reported 15% POLY — impossible for machines that survived
Cyclers, Translated Cyclers, CTL, n-gram CPS, WFAR and RepWL:

1. **eventual positivity** — a fitted counter with a negative trend
   describes a transient, not a phase family. A real example: `381 - 4n`,
   exact over all 96 phases it was fitted on, then the family ends
   because the counter reaches zero. The longer the transient, the more
   convincing the fit looks.
2. **confirmation** — every fit is re-tested on phases it never saw.

## The four GEO candidates, and why they are NOT decidable by us

Lines 360, 833, 852, 1005. Their boundaries are genuinely rigid:
re-run at a 20M macro budget (100x the fitting budget), each reproduced
7–8 unseen phases with **zero mismatches**. Boundary shape, e.g. line 360:

    B(n) = 1^(6+2n) 0 1^23 0 1^12,  head at far left facing left, state D
    steps between boundaries = 72140 - 6n + 96 * 2^n

So: linear tape, exponential clock, all counters affine except one.

**But a certificate needs the word BETWEEN boundaries to be a fixed stage
list, and it is not.** Measured across b = 1..6:

| b | phase-word lengths | stages | max run |
|---|---|---|---|
| 1 | 15, 30, 60, 120, 240 | same as length | 1 |
| 2 | 11, 19, 39, 78, 156 | same as length | 1 |
| 4 | 29, 141, 568, 2180, 8708 | same as length | 1 |

Every run-length count is 1 at every block size: the word never
compresses. At b = 1 and 2 it doubles exactly; at b = 4 it grows faster.

Further structure, uniform across all four machines and every level:

    |W(n+1)| = 2 |W(n)|   exactly
    common prefix = |W(n)| - 6   exactly (same constant 6 for all four,
                                 including the machine whose base word
                                 is 17 rather than 15)

The obvious recursion this suggests, `W(n+1) = W(n)[:-6] + X + W(n)`
with `X` the constant 6-symbol divergence block, is **FALSE** at every
level — tested. The divergence from "W(n) repeated twice" grows
proportionally (13, 22, 44, 88 symbols), so it is not a bounded-edit
substitution either. Intermediate tapes pass through periodic `(011)^k`
forms, which is why b = 3 was worth trying; it yields no phase family.

### The conceptual finding

**Rigid boundaries do not imply a rigid phase word.** For the nine
FRACTRAN holdouts the two came together, and fitting the boundary was
the hard part. On Turing machines they come apart: the boundary family
can be exactly affine while the word between boundaries is exponentially
complex and incompressible. The boundary fit is therefore necessary and
nowhere near sufficient, and a rigidity census over-counts what the
certificate method can actually decide — here by a factor of infinity,
since 4 candidates yield 0 decisions.

Deciding these four needs a decider for the reachable *set* — a
closed-tape-language / regular-language argument — not a certificate for
a single orbit. That is a different tool from ours, and one the
community already has better versions of.

## Census 2 — cryptid-shaped outer maps (all 1,064, 523 s)

| class | count | share |
|---|---|---|
| no two-level structure | 1,033 | 97.1% |
| INSUFFICIENT | 22 | 2.1% |
| **CRYPTID-SHAPED** | **5** | **0.5%** |
| NOT-EXPANDING | 3 | 0.3% |
| PREDICTABLE-BRANCHES | 1 | 0.1% |

The five, all with inner recurrence in base 2 (the BW machine is base 3):

| line | machine | inner | outer orbit R_n | k_n |
|---|---|---|---|---|
| 106 | `1RB0LF_1LC0LD_1RD1LB_---1RE_0RA1RE_1LA0LE` | `2x+3` | 28, 57, 125, 255, 505 | 3,4,5,6,5 |
| 336 | `1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE` | `2x+4` | 49, 160, 300, 1243, 4954 | 3,5,5,7,9 |
| 555 | `1RB1RE_1LC0RA_1RD0LB_1LB1RC_1LF0RD_---0LE` | `2x+5` | 31, 75, 163, 327, 535, 1770, 3309, 9489 | 3,4,5,6,6,8,9,10 |
| 990 | `1RB0LF_1LC1RA_0RE0RD_---1LE_1LF1RC_1LC1LA` | `2x+2` | 12, 52, 219, 1182, 3268 | 3,4,6,9,10 |
| 1002 | `1RB1LC_1RC0LD_1LA0RB_1LB1LE_1RF0LA_---0RE` | `2x+4` | 58, 241, 712, 1452, 3004, 6744 | 3,5,7,8,9,10 |

### After deeper runs (40M macro budget) — three survive

Two corrections to the criteria, both found by running deeper, both
eliminating candidates:

1. **The last outer step is systematically truncated.** The simulation
   stops at a fixed macro budget, which lands in the middle of the final
   inner loop, so its `k` is an undercount. Raising the budget from 8M to
   40M changed line 106's last `k` from 9 to 10 and flipped its verdict.
   A criterion that depends on the final delta is reading the budget, not
   the machine. The last step is now dropped.
2. **A periodic branch pattern is as predictable as a constant one.**
   `1,2,3,1,2,3` is generated by a three-state automaton, so a bounded
   invariant does track it. Testing only for constant deltas let line 990
   through as cryptid-shaped.

Final standing, all corrections applied:

| line | inner | outer steps | k deltas | growth/step | verdict |
|---|---|---|---|---|---|
| 336 | `2x+4` | 10 | 2,0,2,2,2,2,2,1,1 | 2.94 | **CRYPTID-SHAPED** |
| 555 | `2x+5` | 12 | 1,1,1,0,2,1,1,2,2,1,2 | 2.56 | **CRYPTID-SHAPED** |
| 1002 | `2x+4` | 10 | 2,2,1,1,1,1,2,2,2 | 2.93 | **CRYPTID-SHAPED** |
| 106 | `2x+3` | 6 | 1,1,1,1,1 (period 1) | 2.06 | PREDICTABLE-BRANCHES |
| 990 | `2x+2` | 7 | 1,2,3,1,2,3 (period 3) | 4.48 | PREDICTABLE-BRANCHES |

Outer orbits of the three survivors:

    336:  49, 160, 300, 1243, 4954, 19177, 70408, 224311, 380662, 804790
    555:  31, 75, 163, 327, 535, 1770, 3309, 9489, 34404, 105063, 290455, 975958
    1002: 58, 241, 712, 1452, 3004, 6744, 19936, 77239, 285790, 933973

None admits a single-branch closed form `R' = aR + b*x_k + c`.

**The cost wall.** Growth is ~2.5–2.9 per outer step and the work per
step scales with R, so each additional outer step costs roughly 3x the
last. Going from 12 outer steps to 20 costs ~3^8 ≈ 6,600x. Ten to twelve
steps is close to the practical limit at this budget — the same
power-law wall the machine-4 hunt ran into, and the reason these stay
candidates rather than named cryptids.

### Is the TM-to-map equivalence provable? The precondition holds.

Decomposing the macro word of one outer phase into maximal periodic
runs, at block size 2, for all three machines:

    336:  periods [40, 5,0, 5,0, 5,0, 5,0, 5,0, ...]   stages 23, 25, 33, 41
    555:  periods [42, 5,0, 5,0, 5,0, 4,0, 15, ...]    stages 21, 25, 29, 31
    1002: periods [40, 5,0, 5,0, 5,0, 5,0, 5,0, ...]   stages 25, 31, 35, 39

The stage COUNT grows with the phase, so the phase is not a fixed stage
list -- which is what sank the four GEO candidates. But here the growth
is structured: a fixed prologue, then a repeated unit consisting of a
period-5 block plus a separator, then an epilogue. The number of units is
exactly the inner-loop count k, and the j-th block's length doubles with
j because the inner counter doubles. (An earlier reading found "period
20" because four consecutive units of period 5 look like one of period
20; the exact decomposition is the period-5 one.)

So each phase has the shape

    prologue . PRODUCT over j = 1..k of [ (P5)^(c * 2^j) . sep ] . epilogue

which is a NESTED block certificate: an outer repetition of k, with an
inner repetition count of `c * 2^j`, i.e. in EXP = {a + b*n + c*2^n}.
That is inside the certificate class -- unlike the four GEO machines,
whose words never compressed at any block size.

Proof obligations for `TM halts iff the F-orbit meets H`:

1. **entry** -- from blank tape the machine reaches C(R_0): finite
   simulation;
2. **inner step lemma** -- from counter x, one unit takes the machine to
   counter 2x + c in T(x) steps: one induction over the block count;
3. **inner iteration** -- the unit runs k times, k fixed by a guard
   comparison against the reservoir;
4. **outer step** -- compose prologue, k units, epilogue to get F;
5. **halting** -- characterise when the `---` transition can fire.

### Towards Lean: the symbolic simulator, and the inner lemma

`symbolic.py` runs the macro simulator with block counts as expressions
`a + b*x`, cross-checked against the concrete simulator (36 runs, three
machines, six values of x, identical configurations and step counts).

Its important property is what it REFUSES to do. A chain step may cross a
symbolic block, because it consumes the block entirely whatever its
length. But consuming a symbolic block ONE CELL AT A TIME branches: for
some x the block survives and is read again, for others it vanishes and
the next block is read. The simulator stops there rather than picking a
branch. That refusal is what makes its output sound — and it means plain
symbolic simulation reaches only **5 to 7 macro steps** on these
machines, far short of an inner unit.

The classical fix (Marxen–Buntrock; sligocki's proof system) is an
INDUCTION RULE: a fixed finite word that returns the machine to the same
state, direction and skeleton with a bounded change to the counters, so
that running it n times is one symbolic move. Measured, at block size 2,
in the periodic region of an inner phase:

| line | unit | counter delta | cost of the j-th unit | verified exactly for |
|---|---|---|---|---|
| 336 | 5 macro steps | `(0, -1, +2, -1)` | `16 + 8j` base steps | 151 consecutive units |
| 555 | 5 macro steps | `(+2, -1, 0, -1)` | `8 + 8j` base steps | 16 consecutive units |
| 1002 | 5 macro steps | `(0, -1, +2, -1)` | `16 + 8j` base steps | 156 consecutive units |

"Verified exactly" means the predicted skeleton, every counter AND the
cumulative step count all matched at every one of those units. Lines 336
and 1002 have the *same* rule, which is evidence they are relatives.

So after n units, from counters `c`:

    counters = c + n * delta       cost = c0*n + 8*n*(n-1)/2

The cost is quadratic in n because the head sweeps a block that is itself
growing — which is why an earlier check, written assuming constant cost,
reported the rule failing at the second iteration. The rule was right;
the check was wrong.

**This is the inner lemma in the form Lean needs**: a finite base case
(five macro transitions) and a step whose effect is a fixed vector, so
the guards `c1 >= 1`, `c3 >= 1` propagate downward and the induction goes
through. It is the same shape as `steps_blocks` in `bbf/lean/Fractran.lean`,
with a quadratic rather than linear cost.

### Rule-based acceleration — obligation 4, and the cost wall broken

`accel.py` applies the induction rule at run time. At each macro step it
looks ahead for a return to the same skeleton, state and direction; if
the counters move by the same fixed vector on two consecutive
repetitions and the per-repetition cost is constant or grows by a
constant, it computes how many repetitions fit before a guard would fail
and jumps the whole way. `n` is chosen one short of any guard failing, so
a jump never crosses a branch.

The jump *is* the composition of prologue, n units and epilogue that
obligation 4 asks for — the closed form, applied.

**Verified against the unaccelerated simulator** at 5.0e7, 6.3e7 and
5.1e7 base steps for the three machines: identical skeleton, identical
counters, identical base-step count, with 63/90/79 jumps skipping
12,409 / 15,215 / 14,956 units. Beyond that range the detector still
self-checks — it observes two full repetitions with matching deltas
before every jump — but that is a safeguard, not a proof.

**Effect.** Reach goes from ~1e7 base steps to **~1e165 in 45 seconds**,
about 158 orders of magnitude, and outer orbits go from 10-12 steps to
**289-294**:

| line | outer steps | growth/step | k range | delta period | halted |
|---|---|---|---|---|---|
| 336 | 289 | 2.4648 | 3 .. 378 | none | no |
| 555 | 294 | 2.4166 | 3 .. 374 | none | no |
| 1002 | 290 | 2.4936 | 3 .. 384 | none | no |

At ~290 outer steps the aperiodicity of the branch sequence is on much
firmer ground than it was at 10, and the growth rate is stable rather
than a small-sample artefact. **No halt anywhere in ~1e165 steps.**

This is the acceleration the Collatz playbook promises — the machine
becomes simulable to astronomical horizons with polylog work — and it is
what makes the halting question sharply askable rather than merely
plausible.

### Obligation 5 — the halting criterion

All three machines have exactly one undefined transition, **state F on
symbol 0**, and in all three F is entered from exactly one place: state
E reading 0. Read straight off the transition tables:

| line | E | F | scan direction |
|---|---|---|---|
| 336 | `0 -> 1RF`, `1 -> 0LC` | `0 -> ---`, `1 -> 0RE` | right |
| 555 | `0 -> 1LF`, `1 -> 0RD` | `0 -> ---`, `1 -> 0LE` | left |
| 1002 | `0 -> 1RF`, `1 -> 0LA` | `0 -> ---`, `1 -> 0RE` | right |

So E and F form a scanning pair. From E on a 0 the machine writes 1,
steps one cell in the scan direction, and lands in F. F on a 1 writes 0,
steps again, and returns to E. F on a 0 halts. E on a 1 leaves the scan
entirely.

    HALT  <=>  at some moment the machine is in state E reading 0 with
               the next cell in the scan direction also 0

Equivalently, the E/F pair consumes the word `01` (mirrored to `10` for
line 555) over and over, and

  * meeting `1` at an E position ends the scan normally,
  * meeting `00` halts.

**Verified:** over 6e6 base steps per machine there are 3,005 / 4,130 /
4,904 E-on-0 scans and **zero** carrying a `00` -- every one of them
reads `01` and continues. Combined with the accelerated runs, no halt
occurs anywhere in ~1e165 steps.

This is the reduction the whole exercise was for: halting is now a
condition on the TAPE WORD at a specific, identifiable moment, rather
than a statement about the machine's whole future. What remains is to
express "the scanned word contains `00`" in terms of the section
counters, which turns it into an arithmetic condition on the outer orbit
-- the halting set H of the orbit-avoidance problem.

### The unit lemma, DERIVED

`symbolic.py` stalls after five to seven macro steps, and I had recorded
that as a wall. It is not: the stall happens when a single cell is taken
from a symbolic block, but the lemma we want ASSUMES that block is
non-empty. Carrying the guard forward instead of stopping lets the run
continue -- provided the block being lifted is the one the unit actually
sweeps. (Lifting the wrong block, a constant-1 one, fragments the tape
into a configuration the machine never reaches; the first attempt did
exactly that and produced nonsense. The symbolic variable has to be the
growing counter.)

With the right block lifted, one unit crosses symbolically, skeleton
preserved:

| line | lifted | one unit | cost |
|---|---|---|---|
| 336 | c2 | `(1, c1, x, c3) -> (1, c1-1, x+2, c3-1)` | `4x + 12` |
| 555 | c0 | `(x, c1, 1, c3) -> (x+2, c1-1, 1, c3-1)` | `4x + 4` |
| 1002 | c2 | `(1, c1, x, c3) -> (1, c1-1, x+2, c3-1)` | `4x + 12` |

**The derivation reproduces the measured cost law exactly.** At unit j
the swept block has `x = x0 + 2j`, so `4x + 12 = 8j + (4x0 + 12)`, which
at `x0 = 1` is `8j + 16` -- the `16 + 8j` measured empirically over 151
and 156 consecutive units, from an entirely independent route.
Independently checked at x = 1, 2, 3, 7, 11, 20, 53, 100, 301, 1000:
**10/10 exact** for all three machines.

So the unit lemma is no longer an observation. It is:

> For all x >= 1, from the configuration with skeleton S and counters
> `(1, c1, x, c3)`, the machine reaches `(1, c1-1, x+2, c3-1)` in exactly
> `4x + 12` base steps, provided `c1 >= 1` and `c3 >= 1`.

with the guards recorded rather than assumed. That is precisely the
statement a Lean proof needs, and its proof is a five-macro-step case
analysis -- finite, and of the same shape as the firing lemmas already
in `bbf/lean/LeanBbf/Runner.lean`.

**Honest status:** three two-level BB(6) holdouts whose outer maps are
expanding, multi-branch, and have no periodic branch pattern over the
observed range. That is the cryptid signature, measured on 10–12 outer
steps. It is not a proof that the branch sequence is aperiodic forever,
and a longer period than the observed range could still be hiding.

### On the direction of the piecewise-affine criterion

Piecewise-affineness is not something to look for: the outer map of a
two-level machine is affine on each branch by construction. What must be
tested is whether a **single** affine branch explains the whole orbit —
if one does, the orbit has a closed form and the machine is tractable.
A failed global affine fit is evidence of several branches, i.e.
evidence FOR the cryptid shape. Getting this backwards initially made
the BW machine read NO-CLOSED-FORM instead of CRYPTID-SHAPED.

Cryptid-shaped does not mean undecided: the BW machine is cryptid-shaped
and was decided in April 2026, with Baker–Wüstholz. The label says where
the difficulty lives.

### The unit lemma as a Lean target: statement and decomposition

The statement, verified at cell level on 54 independent instances
(x in {1,2,3,5,9,14}, a in {2,4,7}, b in {2,5,8}, arbitrary trailing
context), 54/54 exact, for line 336:

    for all x, a, b and arbitrary Lr, Rr:

      [11] ++ (10)^(a+1) ++ Lr  |  (10)^x ++ (11)^(b+1) ++ Rr   state A, facing left
        -- 4x + 12 steps -->
      [11] ++ (10)^a ++ Lr      |  (10)^(x+2) ++ (11)^b ++ Rr   state A, facing left

(left is written nearest-head-first, so blocks appear right-to-left.)

Traced at x = 3 and x = 5, the run decomposes as

| piece | steps | x=3 | x=5 |
|---|---|---|---|
| prologue, fixed | 4 | 4 | 4 |
| chain right: `x+2` crossings of `01 -> 10` | 2x+4 | 10 | 14 |
| turnaround, fixed | 2 | 2 | 2 |
| chain left: `x+1` crossings of `10 -> 01` | 2x+2 | 8 | 12 |
| total | **4x+12** | 24 | 32 |

Both chains are instances of crossings already proved in
`lean/LeanBb6/Crossings.lean` (`m336_A_R` and `m336_A_L`), so the Lean
proof is: four `steps_of_runFor` fragments and two `crossR_rep` /
`crossL_rep` applications, composed with `Steps.trans`. Nothing in it is
open; it is assembly, and it is not yet done.

### PROVED (Lean): the unit lemma and its iteration

`lean/LeanBb6/Unit.lean`. 833 lines across the development, 0 sorries,
38 `#guard` checks, no added axioms.

    m336_unit (x a b : Nat) (Lr Rr : List Bool) :
      Steps m336 (4 * x + 12)
        [11] (10)^(a+1) Lr | (10)^x (11)^(b+1) Rr   state A, facing left
        [11] (10)^a Lr     | (10)^(x+2) (11)^b Rr   state A, facing left

Proved for ALL x, a, b and arbitrary surrounding tape -- the statement
the Python side had verified on 54 instances. The proof is the four-piece
decomposition above: two fragments computed by the kernel via
`steps_of_runFor`, two applications of `crossR_rep`/`crossL_rep`, and the
list algebra needed to expose each chain's pattern.

That algebra is the whole difficulty and it reduces to one fact,
`shift_10` / `shift_01`: a 0 in front of a run of 10s is a 0 behind a run
of 01s. Everything else is `rep_snoc` and `rev_rep`.

Also proved:

* `m336_units` -- n turns: each side shrinks by n, the middle grows by 2n.
* `unitCost_closed` -- the cost of n turns is `4nx + 4n^2 + 8n`. The
  quadratic term is the price of the middle block growing under the head.

Two mathlib reflexes to avoid, both hit here: `set` is not available, and
`0 * x` is not definitionally `0` (Nat.mul recurses on its second
argument), so the zero case of a cost induction needs `simp`, not `rfl`.

**Remaining for the full equivalence:** the outer half -- composing
prologue, n turns and epilogue into the return map, and expressing the
E/F halting condition in terms of the section counters. Both are assembly
on results already stated and verified, and both are done for only one of
the three machines so far.

### The branch condition, DERIVED (line 336)

The unit lemma says one turn is `(p, q+1, x, r+1) -> (p, q, x+2, r)`, so
the inner loop must run until one of the two shrinking counters is
exhausted. That predicts the branch index, and the prediction holds:

    k = min(q, r)                                  68 / 68 runs

Between flips the machine follows an explicit two-counter rule:

    q <= r :   (q, r)  ->  (2q + 3,  r - (q + 2))  61 / 61 transitions

so `q` runs through 2, 7, 17, 37, 77, 157, 317, 637, ... doubling until
it overtakes the reservoir. The cascade lengths between flips are 6, 8,
10, 12, 14, 16 -- each cascade one longer than the last, which is the
reservoir roughly doubling and buying one more doubling of `q`.

    q > r  :   flip -- q resets to 2, a new reservoir is installed

**The flip is the outer step, and it is NOT in closed form.** Its output
reservoirs are 302, 1245, 4956, 19179, 70410, 224313, 380664, which are
exactly the outer orbit values plus 2 -- so the flip branch is precisely
the map whose orbit the halting question is about. Several fits were
tried against the state at the flip (`4x + 25`, `4x + 4q + 1`, `2q - r`);
each matches one or two instances and fails on the rest. The epilogue
between the last turn and the next cascade has not been analysed, and
without it there is no honest formula. Recorded so the failed fits are
not retried.

So the closed rule set covers the inner cascade and the branch condition;
the outer step remains observed rather than derived.

#### A fit that survived six cascades and then died

Worth recording in full, because it is the third time the same trap has
been walked into in this project. Taking the state at the end of a
cascade, the quantity `r' - 4*x_end + q_end` came out as

    31, 37, 43, 49, 55, 61

-- arithmetic, difference 6, tracking the cascade length L exactly as
`3L + 13`. That gives

    r' = 4*x_end - q_end + 3L + 13

and it is EXACT on six consecutive cascades, L = 6, 8, 10, 12, 14, 16.
It then fails on the next two, and badly (predicted 149,435 against an
actual 804,792).

The reason is visible in the cascade lengths themselves. They run
6, 8, 10, 12, 14, 16 -- an arithmetic progression -- and then 17, 18. The
formula was not a law; it was a description of the regular regime, and
the `3L + 13` term was the warning sign all along. A constant that
depends on the cascade length means an untracked state variable, and it
holds only while that variable moves regularly.

**This is the same failure mode as `381 - 4n` (section on census 1) and
as `W(n+1) = W(n)[:-6] + X + W(n)` (section on the four GEO machines):
a formula exact over every instance available, describing a transient.
The defence is the same each time -- extend the range and re-test, never
fit and ship.**

The break is also a positive datum. Cascade lengths ceasing to be an
arithmetic progression is precisely the digit-consuming behaviour the
cryptid criteria are about, seen from a new angle and at the inner level
rather than the outer one. It is evidence FOR the classification, and it
is why no closed form for the flip has been found: if one existed in this
simple a class, the machine would not be a cryptid candidate.

### What happened to the other 1,061 machines: nothing was decided

Worth stating plainly, because the censuses are easy to misread as
verdicts. Across both sweeps of all 1,064 machines there were **zero**
HALTED and **zero** INFINITE classifications. Not one machine on the list
was proved to halt, and not one was proved not to halt. The classes are
statements about STRUCTURE, and about whether this method has any handle
on a machine -- not about halting.

| group | count | status |
|---|---|---|
| no two-level structure | 1,033 | method finds no handle; nothing learned about halting |
| INSUFFICIENT | 22 | too few outer steps at the budget used |
| cryptid-shaped | 3 | reduced to orbit avoidance; halting open |
| PREDICTABLE-BRANCHES | 2 (lines 106, 990) | **possibly tractable, never attempted** |
| NOT-EXPANDING | 3 | **possibly tractable, never attempted** |
| GEO (rigid boundaries) | 4 | shown NOT decidable by this method |
| UNCONFIRMED | 3 | fits failed confirmation |

The five in bold are the interesting leftover: by our own criteria a
predictable branch sequence or a non-expanding map is the case where a
bounded invariant might track the orbit, which is what a decision would
need. Nobody has tried. That is the most actionable unexplored item this
work produced, and it is cheap compared with anything else here.

## CORRECTION: five candidates, not three

The two machines eliminated as PREDICTABLE-BRANCHES were eliminated on
six and seven outer steps. The accelerator reaches 200+, and at that
depth their branch sequences are **not** periodic:

    line 990  deltas 1,2,3,1,2,3,5,3,3,0,1,2,2,0,0,0,0,0,3,0,0,2,1,0,...
              -- the period-3 pattern holds for exactly six terms
    line 106  deltas 1,1,1,1,1,3,3
              -- the period-1 pattern holds for exactly five

Re-classified at accelerator depth, all five meet the criteria:

| line | outer steps | growth | k range | period | verdict |
|---|---|---|---|---|---|
| 106 | 7 | 2.5979 | 3..11 | none | CRYPTID-SHAPED (weak: only 7 steps) |
| 336 | 247 | 2.4775 | 3..325 | none | CRYPTID-SHAPED |
| 555 | 249 | 2.4036 | 3..316 | none | CRYPTID-SHAPED |
| 990 | 202 | 3.3192 | 3..350 | none | CRYPTID-SHAPED |
| 1002 | 248 | 2.4687 | 3..325 | none | CRYPTID-SHAPED |

**The periodicity test was right; the depth was not.** Adding the test
was a correct fix -- a period-3 delta sequence really is generated by a
three-state automaton and really would be predictable. Applying it to
seven data points was not. Short orbits manufacture regularity, and the
test cannot tell a real period from a coincidence at that length; only
more data can.

This is the same lesson as `381 - 4n`, as `W(n+1) = W(n)[:-6] + X + W(n)`
and as `r' = 4x - q + 3L + 13`, arriving from the opposite direction:
those were false regularities that survived every check available, and
these were false regularities that CAUSED a wrong elimination. Both come
from testing at a depth the phenomenon does not live at.

Honest standing: **four machines with strong evidence** (336, 555, 990,
1002, all at 200+ outer steps) and **one weak** (106, at 7 -- the
accelerator makes little progress on it, so its classification rests on
about as much data as the erroneous elimination did, and should be
treated accordingly).

Not re-tested at depth: the three NOT-EXPANDING machines (lines 168, 259,
396, with inner maps `2x+2`, `2x-6` and `8x/3 - 41/3`). They were
classified at the shallow sweep budget, exactly like 106 and 990 were,
so the same doubt applies to them and they are the obvious next check.

## SECOND CORRECTION: the expansion test rejected Collatz

The three NOT-EXPANDING machines were re-checked at accelerator depth.
Unlike lines 106 and 990, the classification held -- but for line 168 it
held for the wrong reason, and checking why exposed a flaw in the
criterion itself.

`expanding` was implemented as "every step-to-step ratio exceeds 1".
That is not what expansion means for a Collatz-type map, and the test
**rejects Collatz**: the orbit of 27 begins 27, 82, 41, 124, 62, ...,
halving on every even argument. Run on the 3x+1 map, the criterion
returns False.

Line 168 is the same shape. Over **3,049 outer steps** -- by a wide
margin the most data of any candidate -- 98.9% of its steps DECREASE, and
the orbit nevertheless runs 28 -> 43,665, a factor of 1,560, at a
geometric-mean growth of 1.00242 per step. It grows the way Collatz
grows: rarely and in jumps, against a background of decrease.

The test is now the geometric mean. Under it:

| line | outer steps | growth | k range | period | verdict |
|---|---|---|---|---|---|
| 168 | 3,049 | 1.00242 | 3..14, 12 distinct | none | **CRYPTID-SHAPED** |
| 259 | 8 | 1.0000 | 3 only | 1 | predictable |
| 396 | 28 | 1.0780 | 3 only | 1 | predictable |

So line 168 joins the list: **six candidates** -- 106, 168, 336, 555,
990, 1002 -- and 168 has more supporting data than any of the others.
Lines 259 and 396 stay out, now on the branch criterion rather than the
expansion one.

**Three criterion errors are now on record**, all of the same species: a
test that was too strict, too weak, or applied too shallow, each giving a
confident wrong answer. The periodicity test was too weak, then applied
at seven data points. This one was too strict, in a way that a
thirty-second check against the canonical example would have caught at
any point. Testing a criterion against the problem it is modelled on
should be routine and was not.

## Rule sets for all six candidates

`rules.py`, with a corrected shape-finder. The first version picked the
shape that recurs MOST OFTEN, which is usually one the machine passes
through on every macro step and whose runs are all of length one; lines
106 and 990 both failed that way. Scoring candidate shapes by mean run
length finds the loop rather than the traffic.

| line | loop shape | turn rule | first-turn cost | branch k = min |
|---|---|---|---|---|
| 106 | `((2,3),1,1,(1,))` | `+= (1, 0, -1)` | 4 | **34/34** |
| 168 | `((3,1),1,1,(3,))` | `+= (2, -1, -1)` | 10 | **566/566** |
| 336 | `((3,2),0,0,(1,3))` | `+= (0, -1, 2, -1)` | 16 | 66/67 |
| 555 | `((2,3),1,1,(3,1))` | `+= (2, -1, 0, -1)` | 16 | **87/87** |
| 990 | `((0,2),3,1,(3,))` | `+= (0, -1, 1)` | 4 | **5/5** |
| 1002 | `((3,2),1,0,(1,3))` | `+= (0, -1, 2, -1)` | 16 | 79/80 |

Every one of the six obeys `k = min over the shrinking coordinates`, the
branch condition the turn rule predicts. Line 168 is the strongest case
in the whole study at 566 consecutive runs.

**A caveat about section choice.** A two-level machine has a HIERARCHY of
sections, and different ones give different, all-valid rule sets. Scoring
by mean run length picks a coarser section for 336, 555 and 1002 than the
one the Lean proof uses (for 336 it returns shape `((2,),0,0,(1,3,1))`
with turn `+= (2,0,-1,0)` and first-turn cost 582, branch 6/6). The table
above reports the FINE shapes for those three, so that the rule set and
the Lean theorem describe the same object. This is worth stating because
"the rule set of a machine" is not well-defined without naming the
section.

### State of the Lean development against the rule sets

| | 336 | 555 | 1002 | 106 | 168 | 990 |
|---|---|---|---|---|---|---|
| R1 turn | **Lean** | measured | **Lean** | measured | measured | measured |
| R2 branch | 66/67 | 87/87 | 79/80 | 34/34 | 566/566 | 5/5 |
| R3 cascade | 60/60 | 78/78 | 72/72 | - | - | - |
| R4 flip | open | open | open | - | - | - |
| H halt | **Lean** | **Lean** | **Lean** | - | - | - |

So: one machine has a machine-checked turn rule, three have halting
lemmas, all six have measured turn rules and branch conditions, and no
machine has a machine-checked R2, R3 or R4. That is the gap between what
is claimed and what is proved, stated as a table so it cannot be blurred.

### Lean: a second machine

`m1002_unit` and `m1002_units` are proved. Lines 336 and 1002 have
IDENTICAL block structure at the loop shape -- same block words, same
arrangement, same turn delta `(0,-1,+2,-1)`, same cost `4x+12` -- and
differ only in which state the loop runs in, A for 336 and B for 1002. So
the proof is the same proof with the state index changed and the two
crossings taken from 1002's table. That the two share a proof is not a
convenience of the write-up; it is what made them siblings.

Statement verified independently at cell level first, 54/54 exact, the
same test 336's statement passed.

Line 555 does NOT adapt. Its loop shape has five counters and three left
blocks where 336 and 1002 have four and two, so it needs its own
decomposition trace. The remaining three candidates (106, 168, 990) have
measured rules and no formalisation.

Lean now: 923 lines, 0 sorries, 39 `#guard` checks, no added axioms.

**Unproved anywhere: R2, R3, R4.** R2 and R3 are checked exhaustively
over every run observed and look reachable with what is built -- R2 is an
induction on the smaller counter, R3 is R1 composed with itself. R4 is
not, and the failed fit above suggests that is the obstruction rather
than unfinished work.

### R2 proved (positive half), and a correction about R3

`m336_loop` and `m1002_loop`: from counters (q, r) the machine performs
`min q r` turns, at cost `unitCost x (min q r)`, leaving
`(q - min q r, x + 2*min q r, r - min q r)`. Proved for both machines,
directly from the iteration lemma by choosing `n = min q r`. Also
`loop_exhausts`: at least one of the two counters ends empty, which is
what makes `min` the right count rather than merely an upper bound.

The other half of R2 -- that the loop runs no FURTHER -- is deliberately
not claimed. It would say the next turn fails, and what the machine does
instead of that turn is the flip, R4, which has no closed form. The two
halves of R2 are not equally within reach.

**Correction to an earlier claim.** This file previously said R3 "is R1
composed with itself" and would follow from the machinery already built.
That is wrong. R3 relates consecutive LOOP starts, and between one loop
and the next the machine runs an epilogue -- the segment that converts
the accumulated middle block into the next loop's counter. R3 therefore
needs the epilogue, exactly as R4 does, and is not a corollary of R1.

The epilogue does look tractable: measured on line 336 it costs
`2X + 22` steps for a middle block of X, constant in the reservoir. But
the resulting counter did not match what the run data implies on the
first attempt -- the detection broke mid-epilogue -- and it is not
recorded as a rule until that is resolved. Two rules in this project have
already been shipped from measurements that stopped one step too early.

Standing: R1 and R2 (positive half) proved in Lean for lines 336 and
1002; R3 and R4 need the epilogue; H proved for three machines. No
machine yet has ALL its rules proved.

## The epilogue, pinned (line 336)

The segment between one loop and the next, which R3 and R4 both need.
Measured against the real machine by subtracting the loop cost from the
gap between consecutive loop starts:

| loop start | turns | loop cost | gap | epilogue | X after loop |
|---|---|---|---|---|---|
| (1,2,1,302) | 2 | 40 | 62 | **22** | 5 |
| (1,7,1,298) | 7 | 280 | 322 | **42** | 15 |
| (1,17,1,289) | 17 | 1,360 | 1,442 | **82** | 35 |
| (1,37,1,270) | 37 | 5,920 | 6,082 | **162** | 75 |
| (1,77,1,91) | 77 | 24,640 | 24,962 | **322** | 155 |

Cost is exactly `2X + 12` on all five, X the middle block after the loop.

Stated at cell level and verified on 54 independent instances, 54/54:

    [11] blank | (10)^X (11)^R Rr        state A, facing left
      -- 2X + 12 steps -->
    [11] (10)^(X+1) [1] | (10) (11)^(R-2) Rr

Two things had to be got right, and both bit first:

* **the left context must be blank, not arbitrary.** The epilogue reads
  leftward past the [11] block, so with an arbitrary tail it does not
  close. In the machine the left stack has exactly two blocks, so the
  tail really is blank -- but that is a fact about the reachable
  configurations, not a free choice.
* **the result ends `(10)^(X+1) [1]`, not `(10)^(X+2)`.** The trailing 1
  plus the blank tape beyond it forms the last block at block level, so
  the block count is X+2 while the explicit cell list is one 0 shorter.
  A pattern-matching detector reported X+1 and then X+2 depending on
  where it stopped; only checking against the real machine settled it.

### R3 now follows

From (q, r) with x = 1 and q <= r: the loop runs q turns to
(0, 1+2q, r-q), then the epilogue gives (1+2q+2, 1, r-q-2), i.e.

    (q, r)  ->  (2q + 3,  r - (q + 2))

which is R3 exactly. The reservoir arithmetic checks on every observed
loop: 302-2-2 = 298, 298-7-2 = 289, 289-17-2 = 270, 270-37-2 = 231.

### And R4 is the other branch

The second row of the table above is the flip: q = 157 > r = 12, so the
RESERVOIR exhausts rather than the counter, and the epilogue cost is
142,454 rather than 2X+12. R4 is therefore not a separate mystery -- it
is the same segment entered with the other counter empty. That is a much
better-defined target than "the flip has no closed form", which is how it
was described an hour ago.

### The epilogue proved in Lean, and why R3 does not yet compose

`m336_epilogue` is proved: three steps of prologue, `X+1` crossings of
`10 -> 01` in state F, seven steps of tail, totalling `2X + 12`. Lean is
now 1,035 lines, 0 sorries, 40 `#guard` checks, no added axioms.

The pieces of R3 are therefore both proved -- `m336_loop` gives the loop
and `m336_epilogue` gives the segment after it -- and yet R3 does not
follow by composing them, for a reason worth recording.

**The two lemmas disagree about the left tail.** `m336_loop` holds for an
arbitrary tail `Lr`; `m336_epilogue` requires the tail to be exactly
blank, because its prologue reads leftward past the `[11]` block. That is
fine for one composition. But the epilogue's OUTPUT ends
`(10)^(X+1) [1]` -- a trailing `1` against blank tape -- so the next
loop runs with `Lr = [true]`, and when THAT loop exhausts the left tape
is `[1,1,1]`, not `[1,1]`. The epilogue as stated does not apply again.

At block level there is no discrepancy: a trailing `1` followed by blank
tape IS a `10` block, which is exactly why the block count is `X+2` while
the cell list shows `X+1` complete blocks. The two configurations behave
identically because `hd [] = false`. But they are not equal as lists, so
Lean will not rewrite one into the other, and making them interchangeable
needs a small lemma -- that appending blanks to the left tail changes
nothing -- which does not exist yet.

So R3 is one structural lemma away rather than one composition away. The
missing piece is stated precisely and is about the representation, not
about the machine.

Standing: R1, R2 (positive half) and the epilogue proved for line 336;
R1 and R2 for line 1002; H for three machines. R3 blocked on the
blank-tail lemma. R4 is the epilogue entered with the reservoir empty
instead, and is not yet attempted.

## R3 PROVED IN LEAN (line 336)

The blank-tail obstruction had a better fix than a padding lemma, and
finding it finished the chain.

**The phantom turn.** The loop's LAST turn is not an ordinary turn. By
then the left tape has run down to `[1,1,1]`, and the final `10` block is
the trailing `1` together with the blank tape beyond it. Such a turn
reads `1,1,1,blank` where an ordinary turn reads `1,1,1,0` -- and
`hd [] = false`, so those are the same four symbols and the same
four-fragment proof applies. Verified first at cell level, 54/54, then
proved as `m336_phantom`.

That is what makes the loop and the epilogue compose: `n` ordinary turns,
then the phantom turn consuming the trailing `1`, leaving the left tape
exactly `[1,1]` -- which is what the epilogue requires.

The chain, all proved, no sorries, no added axioms:

    m336_unit        one turn, all counters, arbitrary tape, 4x + 12
    m336_units       n turns
    m336_loop        n = min q r turns (R2, positive half)
    m336_phantom     the last turn, against blank tape
    m336_loop_full   n ordinary turns + the phantom turn
    m336_epilogue    the segment between loops, 2X + 12
    m336_cascade     loop_full + epilogue -- and its end configuration
                     has the SAME SHAPE as its start, so it composes
                     with itself
    m336_cascade_counters
                     the same rule stated on the block counts:

        (q, r)  ->  (2q + 3,  r - (q + 2))       for 1 <= q, q + 2 <= r

That last line is the accelerated Collatz-like rule the whole exercise
was aimed at, and it is now machine-checked rather than measured. The
block count `q` counts the trailing `1`-against-blank as a block, which
is why `q = n + 1` in the cell-level statement.

Lean: 1,165 lines, 0 sorries, 41 `#guard` checks, axioms `propext` and
`Quot.sound` only.

### Line 336: what is proved

| rule | status |
|---|---|
| R1 turn | **Lean** |
| R2 loop, positive half | **Lean** |
| R3 cascade | **Lean** |
| R4 flip | open |
| H halt (F on 0) | **Lean** |

R4 remains. It is the same segment entered with the RESERVOIR empty
rather than the counter, and unlike the epilogue it is not a short fixed
word: one measured instance cost 142,454 steps. It is the one rule still
outside the formalisation, and it is what a full halting argument would
need.

## R4: what it actually is, and why it is not the epilogue's sibling

Earlier this file called R4 "the same segment entered with the reservoir
empty instead", and said that was a better-defined target than "no closed
form". The first half is right and the second was too optimistic.
Measured, the flip cost against the block it consumes:

| x after the loop | flip cost | cost / x^2 |
|---|---|---|
| 25 | 142,454 | 228 |
| 305 | 2,460,830 | 26.5 |
| 1,235 | 39,012,534 | 25.6 |
| 4,821 | 586,494,838 | 25.2 |
| 17,911 | 7,986,062,046 | 24.9 |
| 58,937 | 83,694,136,686 | 24.1 |
| 120,987 | 301,776,560,038 | 20.6 |

The epilogue costs `2X + 12` -- a fixed word plus one chain. The flip
costs roughly `25 x^2`, and the ratio drifts rather than settling, so it
is not even exactly quadratic. **R4 is not a segment at all; it is a
second nested loop**, over the block the cascade accumulated, with its
own inner structure to be found. Formalising it is comparable work to
everything done for the cascade, not an increment on it.

### Where that leaves the claim

For line 336 the CASCADE is machine-checked, end to end, as an
accelerated self-composing Collatz-like rule, together with the halting
criterion. What is not machine-checked is the flip -- and the flip is
what generates the outer orbit. The R_n sequence whose statistics the
cryptid criteria measure is precisely the sequence of reservoirs the
flips install.

So the honest bottom line is slightly uncomfortable and worth stating
plainly: **the part now proved is the regular recursive part, and the
part carrying the Collatz-like difficulty is exactly the part that
resists.** That is not an accident of effort. The cascade is regular
because it is a fixed rule iterated; the flip is where the machine reads
deep digits of its own accumulated block and decides how much reservoir
to build, which is the digit consumption the classification is about.

A complete cryptid claim for this machine needs R4. What exists today is
a proved reduction of the cascade phase, a proved halting criterion, and
a measured -- not proved -- outer map.

## The flip is structural, not incidental: a plan decision is needed

Before grinding R4 for line 336, the other candidates were measured to
see whether any closes cleanly. Line 106 has the cleanest structure found
anywhere in this study:

    ordinary cascade:  k -> 2k + 4,  cost 6k^2 + 26k + 36     30/30 exact
    flips at k = 124, 252, 508, 1020, each resetting k to 4

The cost formula is exact on every ordinary transition and fails only at
the four flips. Line 168 and line 990 were measured too. **Every machine
has a flip, and in every case it is the step that resists.**

That is structural rather than incidental, and the reason is the one
already given for 336: a cascade is regular because it is a fixed rule
iterated, while a flip is where the machine reads deep digits of its
accumulated block and decides how much reservoir to rebuild. Digit
consumption is the third cryptid criterion. **A machine whose flip had a
closed form would not be a cryptid candidate** -- the classification and
the obstruction are the same fact seen twice.

So "pick a machine where everything closes" has no solution among the
six. The options are honest ones:

**(A) Finish R4 for one machine.** It is a second nested loop, so it
needs its own unit lemma, iteration, epilogue and composition -- the
whole R1-R3 arc again, on a structure not yet explored. Line 106 is the
best target: its cascade rule is exact 30/30 and its flips are frequent,
so instances are cheap to observe. Multi-session.

**(B) Ship what is complete, and say what it is.** For line 336: a
machine-checked reduction of the cascade phase plus a machine-checked
halting criterion. That is a real theorem and a complete one -- it is
simply not the cryptid claim. The cryptid claims for all six remain
measured conjectures, which is what this file has said throughout.

What is NOT available is a complete cryptid claim for any machine today,
and no amount of further measurement will produce one. Only (A) will.

## R4 opened: the machine is self-similar, and that reframes the job

Starting option (A) on line 336's flip. The flip window is 1,500 macro
steps (142,558 base steps), and it is NOT opaque -- four shapes recur
about 180 times each inside it, so it is a nested loop, exactly as its
quadratic cost suggested.

Its unit shape `((1,), 2, 0, (2,3,1))` occurs 187 times with a constant
counter delta `(-1, +2, -1, 0)` holding on **181 of 186** consecutive
pairs. The five exceptions are not noise: they fall at indices 1, 8, 25,
with gaps 7 and 17.

**7 and 17 are the outer cascade's own doubling sequence** -- 2, 7, 17,
37, 77, 157 -- the sequence generated by `q -> 2q + 3`, which is R3.

So the flip is not a new kind of object. It is a cascade of the same
shape as R3, running inside R4, punctuated by its own sub-flips. The
machine is self-similar.

### What this changes

Treating R4 as "another R1-R3 arc on unexplored structure" was the wrong
model, and it was the model behind the multi-session estimate. If the
flip's cascade really is R3's cascade at a smaller scale, then R4 should
be expressible RECURSIVELY in terms of the rules already proved, rather
than rebuilt from scratch. That is a different and much better shaped
problem -- and it is also the first evidence in this study for why the
outer orbit is hard: a self-similar flip means the branch structure at
every level is the branch structure at every other level.

It is also a conjecture on one flip's worth of data. Indices 1, 8, 25 is
three exceptions and two gaps; 7 and 17 matching the doubling sequence
could be coincidence at that length, and this file records three separate
occasions where exactly that kind of match was coincidence. The next step
is to measure sub-flip positions across several flips and check whether
the gaps continue 37, 77, 157 -- cheap, decisive, and not yet done.

**Status: R4 is open, its structure is identified but not confirmed, and
no complete cryptid claim exists for any machine.**

## CONFIRMED: the machine is exactly self-similar

The decisive measurement, run across four independent flip windows of
line 336. Inside each flip, the unit shape `((1,),2,0,(2,3,1))` recurs
with constant delta `(-1,+2,-1,0)`, broken at these indices:

| flip | unit observations | break indices | gaps |
|---|---|---|---|
| 0 | 187 | 1, 8, 25, 62, 139 | 7, 17, 37, 77 |
| 1 | 605 | 1, 8, 25, 62, 139, 296 | 7, 17, 37, 77, 157 |
| 2 | 2,476 | 1, 8, 25, 62, 139, 296, 613, 1250 | 7, 17, 37, 77, 157, 317, 637 |
| 3 | 9,771 | ... 2527, 5084 | ... 1277, 2557 |

The gaps are `7, 17, 37, 77, 157, 317, 637, 1277, 2557` -- exactly
`a -> 2a + 3`, which is **the outer cascade's own sequence**, the one R3
generates. The break indices are identical across all four windows and
the sequence simply extends further in each larger flip.

This is no longer the two-point coincidence flagged when it was first
noticed. It is four windows, sequences of length 4, 5, 7 and 9, all
agreeing exactly.

**The machine is self-similar.** The outer level runs a cascade
`q -> 2q + 3` punctuated by flips; inside each flip runs the same cascade
with the same rule, punctuated by its own sub-flips; and so on down.

### What this means for R4

R4 is not a new structure needing its own R1-R3 arc. It is R3 one level
down. The right formalisation is therefore recursive: a single theorem,
parameterised by depth, whose inductive step is the cascade rule already
proved, rather than a fresh development per level. That is a
qualitatively different and much smaller job than the multi-session
estimate this file recorded an hour ago, and the estimate should be
treated as withdrawn rather than merely revised.

It also explains, structurally, why the outer orbit resisted a closed
form all day. A self-similar flip means the branch structure at every
level is the branch structure at every other level, so there is no
outermost level at which the branching becomes simple. That is what
digit consumption looks like from the inside, and it is the first
mechanical account this study has produced of WHY these machines are
hard rather than merely that they are.

### Sharpening the self-similarity claim (and correcting it)

"R4 is R3 one level down" was too loose. Measured, inside flip 2, the
counters at each sub-run start are

    (2, 1, 2492, 1)  (7, 1, 2488, 1)  (17, 1, 2479, 1)  (37, 1, 2460, 1)
    (77, 1, 2421, 1) (157, 1, 2342, 1) (317, 1, 2183, 1) (637, 1, 1864, 1)

so the first coordinate runs `2, 7, 17, 37, 77, 157, 317, 637` and the
third decreases by `4, 9, 19, 39, 79, 159, 319`, i.e. by `q + 2`. The
flip's cascade therefore obeys

    (q, r)  ->  (2q + 3,  r - (q + 2))

**exactly R3's rule** -- and the sub-run lengths `2, 7, 17, 37, ...` are
`k = q`, exactly R2.

But it obeys it at a DIFFERENT SHAPE. The outer cascade lives at
`((3,2),0,0,(1,3))` with turn delta `(0,-1,+2,-1)` on coordinates 1 and
3; the flip's cascade lives at `((1,),2,0,(2,3,1))` with turn delta
`(-1,+2,-1,0)` on coordinates 0 and 2. Same rule, different embedding.

So the self-similarity is real and exact, but it is not literal reuse.
In Lean, R4 needs **its own unit lemma** -- a new four-fragment proof at
the new shape, with its own crossings from the table -- after which the
cascade scaffolding already built (units, loop, phantom, epilogue,
compose) transfers, because that scaffolding never mentions the
particular shape except through the unit lemma.

That is the precise specification of the remaining work, and it is a
single well-understood lemma plus a re-instantiation, not a fresh arc.
The earlier withdrawal of the multi-session estimate stands; so does the
correction to "one level down", which overstated what was measured.
