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
