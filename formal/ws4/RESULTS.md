# WS4 — The formal hardness frontier

Executed July 27, 2026. Code and logs of record in this directory; the PDF
(`ws4_report.pdf`, built by `make_ws4_report.py`) reads every number out of the
logs, so it cannot drift from the computation.

WS4 was planned as an assembly job — known results plus our theorems, write down
the boundary. The July 27 revision changed the brief to *our own* three
impossibility results and their measured growth rates. Executing that produced
four things the plan did not anticipate, one of which is a correction to a claim
this program had been making for two days.

---

## The headline: the units were never comparable

Three certificate families had been refuted, each measured in its own unit — DFA
states, congruence modulus, backward depth. Converting the two that *can* be
converted:

| certificate family | unit | reach, expressed in moduli | what it covers |
|---|---|---|---|
| congruence + threshold | modulus | **every m ≤ 20,000**, any threshold | unions of residue classes only |
| MSB automatic, ≤ 13 states | DFA states | moduli 2..13 (12 of them) | any 2-automatic set |
| LSB automatic, ≤ 11 states | DFA states | moduli **{2, 3, 4}** | any 2-automatic set |
| backward-depth counting (WS2) | depth L | exact counts at every fixed L | density, not separation |

The conversion is exact and takes twenty lines (`certificate_classes.py`). A
congruence certificate is a union of residue classes mod m; the canonical
trackers are **m** states MSB-first (`c → 2c+d`) and **m·ord_m(2)** states
LSB-first, so an *n*-state impossibility kills every modulus whose tracker fits
in *n* states.

**The LSB bound — the program's headline for two days, and the thing three
multi-day jobs were spent on — covers three moduli.** A 30-second sweep covers
20,000, i.e. **1,538× more** than even the MSB bound. Neither family contains
the other: a union of residue classes is a vanishing fraction of the automatic
sets of any size, so on everything outside congruences the SAT bounds are the
only statement there is.

This is not an argument that WS1 was wasted. Its value was never the state
count — it was the *shape* of the obstruction (a certificate must avoid the
whole halting basin, not just H), and that survives the conversion intact.

---

## WS4.1 — one syntax for cryptids and for universality (`gam.py`)

**Definition.** A one-counter *guarded affine machine* (GAM): state x > 0,
selector σ(x), rules x → (a_i x + b_i)/c_i guarded by exact division.

- **RES(d)** — σ decided by x mod d. Finitely many affine pieces. *FRACTRAN is
  exactly this*, so Conway's universality theorem is a statement about our
  syntax with no translation layer, and Fenrir (machine 7) is written in the
  very class Conway proved universal — which says nothing about Fenrir itself,
  only that no translation is needed to compare it with universal programs.
- **VAL(q)** — σ(x) = v_q(x). Infinitely many affine pieces from one schema.

**Construction (machine-verified).** Register machine → RES-GAM, encoding
`n = ∏ p_j^{r_j} · s_L` with one label prime to the first power:

```
INC(j,k) at L   →   p_j·s_k / s_L
DEC(j,k,z) at L →   s_k / (p_j·s_L)   then   s_z / s_L
```

Exactly one label prime divides n at any time, so instructions cannot compete;
within an instruction the guard order performs the zero test. **≤ 2I rules for
I instructions, one step per step.** Verified in lockstep against a direct
interpreter: `r0 += r1·r2` compiles 6 instructions to 9 rules, 0 mismatches over
1,072 steps across 64 starts, every start also checked to produce the *right
answer* so a silently-looping program cannot pass by vacuity.

With Minsky's theorem, **RES-GAMs are Turing-complete**, and the smallest
universal instruction count I bounds the frontier at 2I rules.

**Anchor needing no citation.** Conway's PRIMEGAME is a **14-rule** RES-GAM with
modulus 6,469,693,230; run here from x=2, its pure powers of two have exponents
2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47 — the primes,
consecutively, checked rather than quoted.

### The correction: the frontier does not separate our machines

The Needle is one counter, VAL(2), **one** rule schema. Machine 3 likewise.
Written down they are smaller than 14 rules.

**The plan's phrasing — "our cryptids sit strictly below" — does not follow and
should not be repeated.** VAL(q) unfolds one schema into infinitely many affine
pieces (WS4.2 proves the Needle really has infinitely many distinct slopes), so
smaller on the page is not smaller in power. Nothing here, and nothing we know
of in the literature, lower-bounds the power of a one-schema VAL machine.

### The open question this leaves — worth more than the section that produced it

> **Is the one-schema VAL(q) class Turing-complete?**

A genuine **two-sided bet**, and the only one still open now that MSB-first is
spent:

- *Universal* → the size frontier is vacuous for our machines, and the
  resistance has a structural explanation.
- *Decidable* → **it decides our cryptids.**

---

## WS4.2 — the fault line, made checkable (`branch_type.py`)

1D piecewise-affine reachability has a decidable island: **injective** maps with
**finitely many** interval-cut pieces (LICS 2023). The plan *asserted* we sit
outside it. Both hypotheses now checked against the machines' own verified steps.

**(H1) fails — the slope set is infinite.** On v_2(x) = v the Needle map is
exactly

```
F(x) = (1 + 3·2^-(v+1)) x + (v − 3/2)
```

and machine 3 is `G(a) = (1 + 3^-(j+1)) a + (j + c_r − r/3)` on v_3(a) = j.
Verified in exact rational arithmetic: **0 mismatches** over 2 ≤ x < 200,000
(branches v = 0..16) and 0 over 2 ≤ a < 200,000 (branches j = 0..10). Slopes
5/2, 7/4, 11/8, 19/16, 35/32, 67/64, … → 1, pairwise distinct (all 400 of the
first 400). A finitely-piecewise-affine map has finitely many slopes, so **no
refinement of the partition can repair this** — the obstruction is in the slope
set, not in the description.

Second reading, worth keeping: the slopes tend to **1**. The map is expanding on
average while nearly all individual pieces are almost neutral — which is why
bounded-state reasoning over any fixed finite set of branches says nothing.

**(H2) fails — neither map is injective.** `F(10) = F(12) = 17`, and 17 is the
third element of the *published* orbit 6, 10, 17, 41, 101, … — the failure is
visible on the trajectory the whole problem is about. Machine 3:
`G(16) = G(18) = 24`.

The two hypotheses fail for unrelated reasons, which is stronger than "not
covered": a reformulation would have to fix both.

---

## WS4.3 — the certificate-impossibility account (`congruence.py`)

**In one variable, semilinear = ultimately periodic = congruence + threshold.**
Three literature strands collapse into this single class here:

- linear-arithmetic non-termination certificates (in one variable there is
  nothing else to write);
- **bbchallenge regular deciders** (FAR, WFAR, RepWL, CPS) — they read counters
  in unary/block form, and a regular language over one letter is ultimately
  periodic;
- the **affine sieve**, whose only fuel (congruence-quotient expansion) is
  provably absent here.

Refuting the one class refutes all three, for a reason the wiki states only
empirically.

### The argument, and the bug in my first version of it

Suppose `I = {x < T} ∪ {x ≥ T : x mod m ∈ S}` contains the orbit and avoids H.
Take an orbit element x_i ≥ T and h ∈ H with h ≥ T and h ≡ x_i (mod m); then
x_i ∈ I forces its class into S, so h ∈ I — and h ∈ H.

**The bug.** My first implementation collected *every* residue 2^e takes mod m.
That is unsound for the threshold claim: 2^e mod m is only *eventually*
periodic, and a pre-period residue is taken by finitely many powers, so a
collision there is defeated by a large enough T. Mod 12 the powers run
1, 2, 4, 8, 4, 8, … — a collision at 1 or 2 proves nothing about T > 2.

**The fix strengthened the theorem.** Restricting to the eventual cycle makes
every witness an *infinite* family of halting values, so the refutation holds
for **every** threshold rather than for thresholds below a cutoff. The search
got harder; the conclusion got better.

**Result (machine-verified over the stated domain).** For both machines every
modulus 2 ≤ m ≤ 20,000 collides at orbit index ≥ 500 against complete cycle
residues. **No congruence certificate at any modulus ≤ 20,000, with any
threshold whatsoever.** Hardest cases: Needle m = 14,336 (index 11,265);
machine 3 m = 13,122 (index 105,033).

**The m = 1 case is proved, not swept.** The Needle's b is strictly increasing
(T2), so the orbit is unbounded; a finite union of intervals containing an
unbounded set contains a ray [T, ∞); every ray contains a power of two. **No
finite-union-of-intervals certificate exists, unconditionally.**

### A lemma found by chasing the last survivor

One modulus held out: **13,122 = 2·3⁸** for machine 3, cycle residue {6561},
which demands v_3(a) ≥ 8 *and* an odd 3-free part. All eight orbit values with
v_3 ≥ 8 in the first 60,500 had an even 3-free part — 8/8 looks structural at
p = 1/256, *if the parity were balanced*. A separating congruence would **prove**
machine 3 never halts, so this was diagnosed rather than dismissed.

> **Lemma (proved; machine-verified).** `G(a) ≡ v_3(a) (mod 2)`.
>
> *Proof.* `G(a) = (3^{j+1}+1)m + (r·3^j + j + c_r)`, j = v_3(a), r ∈ {1,2},
> c_1 = 3, c_2 = 4. The first coefficient is even and 3^j is odd, so
> `G(a) ≡ r + j + c_r (mod 2)`; r + c_r is odd for both r, leaving `G(a) ≡ j`. ∎
>
> Verified: 0 mismatches over 399,987 values a < 400,000.

So the 3-free part is odd only ≈ ¼ of the time, 8 evens in a row has probability
**0.10**, and the survivor was luck. Extending the orbit killed it at index
105,033. **The lemma is the durable output — a new proved fact about machine 3,
obtained only because a null result was checked instead of accepted.**

---

## Measurement hygiene (`clean_growth.py`)

Every growth constant in the report is a ratio of solver times, and the earlier
ones were not fit for that use: those runs were concurrent on one 10-core box at
varying load (±30% recorded). The trigger was concrete — the MSB step 12→13
measured **10.18×** under heavy load and **5.47×** after two competing multi-day
jobs were killed, and the two cannot be separated after the fact.

`clean_growth.py` re-measures under one condition: one process, strictly
sequential, nothing else of ours running, load average sampled at every
instance and printed into the log. The effect is not subtle — MSB n=10 took
**7.9 s** clean against **24.6 s** loaded, a factor of 3.1.

| n | MSB sec | MSB step | LSB sec | LSB step | LSB/MSB |
|---|---|---|---|---|---|
| 6 | — | — | 0.7 | — | — |
| 7 | — | — | 3.1 | 4.30× | — |
| 8 | 0.7 | — | 13.4 | 4.35× | 18.98 |
| 9 | 1.9 | 2.73× | 74.5 | 5.55× | 38.62 |
| 10 | 7.9 | 4.10× | 705.0 | 9.46× | 89.23 |
| 11 | 54.6 | 6.91× | — | — | — |
| 12 | 613.3 | 11.23× | — | — | — |
| 13 | 8,046.7 | 13.12× | — | — | — |

**Both series come out strictly monotone.** The loaded MSB measurement had
wandered — 4.33 down to 3.46, up to 5.47, 6.70, 10.18, then back down to 5.47 —
and every reversal was load. Two claims settle here:

- **Withdrawn:** "the per-state factor fell back to 5.47 at n=13". It arrived
  exactly as two competing multi-day jobs were killed; clean, that step is the
  **largest** in the series at 13.12×.
- **Upheld, on better evidence:** "the last step is the largest in every
  series" — it rested on four noisy series, and now rests on two clean ones.

The cross-encoding ratio compounds under clean measurement too (18.98, 38.62,
89.23 at n = 8, 9, 10), so MSB genuinely carries a smaller per-state factor
rather than a constant discount — and both arguments of the old exchange-rate
formula `log_g(C)` drift, which is why no particular number from it survived.

---

## What WS4 changes about the program's own claims

| claim | status after WS4 |
|---|---|
| "Our cryptids sit strictly below the universal machines" | **Withdrawn.** Upper bound only; one-schema VAL(q) is not known to be weaker. Now a stated open question. |
| "No MSB automatic certificate at ≤ 12 states" | **Now ≤ 13.** n=13 completed UNSAT (9,174 s, loaded run). |
| "The per-state factor fell back to 5.47 at n=13" | **Withdrawn** — an artefact of killing two competing jobs mid-window. |
| "Our no-congruence theorems explain regular-decider resistance" | **Upheld and quantified**: semilinear = congruence + threshold, refuted to m ≤ 20,000 for any threshold. |
| "The LSB bound is the headline impossibility result" | **Demoted.** Three moduli. Its durable content is the halting-basin shape. |

---

## Traps added

- **Convert bounds into a common currency before ranking them.** Three numbers
  in three units invite ranking by size. Two of ours differed by three orders of
  magnitude in the direction opposite to how they'd been presented.
- **When a sweep leaves survivors, diagnose them; don't just widen the window.**
  A genuine survivor would have been a proof. Diagnosing produced a lemma.
- **"Arbitrarily large" needs the residues taken *infinitely often*, not the
  residues taken.** The pre-period is where threshold arguments leak, and the
  leak is invisible in the output — the sweep reported success either way.
- **Don't measure growth constants under variable load.** Bounds survive
  contaminated timing; the constants that price them do not.

---

## Follow-up (July 29, 2026): a barrier over a slice, and the refutation of the genre

`rigidity.py`, `rigidity.log`. WS4 ended by asking whether one-schema VAL(2) is
Turing-complete. This does not settle it. It proves a barrier over an explicit
slice, and — more usefully — **refutes the whole family of arguments the program
had planned to attack the question with**.

### Theorem R — branch rigidity (proved)

> Branch v sends every non-halting input to the **same** valuation ⟺
> `v₂(B_v) < v₂(A_v)`; and then `v₂(F(x)) = v₂(B_v)` for every x on the branch.

*Proof.* With `A_v = 2^a A′`, `B_v = 2^b B′` (A′,B′ odd): if b < a then
`F(x) = 2^b(2^(a−b)A′k + B′)` and the bracket is odd for every k. If b ≥ a then
`F(x) = 2^a(A′k + 2^(b−a)B′)`, and A′ is a unit, so the bracket realises every
residue as k varies and its valuation is unbounded. ∎
*Machine-verified: 6,462 (machine, branch) pairs, k ≤ 899, 0 disagreements.*

### T13 — the barrier theorem (proved)

> If `v₂(B_v) < v₂(A_v)` for every v, the branch sequence is a fixed sequence
> **independent of the state** (`v_(n+1) = v₂(B_(v_n))` depends on `v_n` alone),
> hence eventually periodic; the orbit is a periodic composition of affine maps
> with closed form `x_n = cλⁿ + d`.

Such a machine does **no state-dependent branching** and cannot carry a
computation; halting degenerates to an S-unit equation. *Machine-verified:
**2,351 of 19,092 machines — 12.31%** — are globally rigid, all with β even.*

**A correction the verification forced.** The closed form "with `a = v₂(β) ≥ 1`,
`gcd(δ,2^a) ∤ ε`" is **exact on β even and nonzero** (8,716 machines, 1,593
rigid, agreement confirmed) but **silently omits β = 0**, which supplies **758 of
the 2,351** — almost a third. That case is genuinely different, not degenerate:
β = 0 makes `v₂(A_v) = v+1` grow without bound, so rigidity there is *generic*
rather than exceptional.

### The counting barrier is refuted, and the reason retires the genre

The plan was: `(A_v, B_v) mod M` depends on v only through `(2^v mod M, v mod M)`,
so the branch table is eventually periodic in v with period dividing
`lcm(ord_M(2), M)` — while a Conway/Kurtz–Simon reduction mod M needs M
independent affine pieces. **The periodicity is true. The conclusion is false.**
Measured branch bandwidth (distinct `(A_v,B_v) mod M` actually achieved) is
**≥ M for every modulus tested** — 100 at M=23, 412 at M=101, 1,036 at M=257.
VAL(2) supplies at least as many branch behaviours as such a reduction consumes.

And the reason generalises past this one attempt:

> **Universality is a property of a single point, not of a family.**

A 5-parameter family of dimension 5 inside a 2V-dimensional space of branch
tables can still contain a universal machine, because a universal machine is a
**0-parameter object**. So every argument of the form *too few degrees of
freedom*, *rank ≤ 5*, *density M^(5−2V)*, *bandwidth too small* answers a
question nobody asked. This retires the entire counting genre — including the
composite-step version, where the dimension bound survives at 5 for every step
count and is equally useless.

A real barrier needs a property shared by **every point**. Two candidates exist.
Theorem R is one, but holds only on the β-even slice. The other is the slope
spectrum `s_v = α + β·2^−(v+1)`, geometrically convergent for every machine:

> **Slope-resolution bound (proved).** At most `⌊log₂(|β|/ρ)⌋` branches are
> pairwise ρ-separated in slope, so k separated branches cost `|β| ≥ ρ·2^(k−1)`.

*Machine-verified: 9,000 (machine, ρ) pairs, 0 mismatches.* That is an
**exponential compression bound, not an impossibility** — and saying so is the
honest end of this line.

### Status of the universality question

**Q1** (some single member has an undecidable halting set) — **untouched**. The
12.31% slice is decided *because* it is trivial.
**Q2** (the parametrized problem) — **narrowed three ways, not settled**: the
rigid slice is computation-free; branch-index-preserving one-step simulation of
FRACTRAN/RES is impossible (forced α,β come out non-integral for PRIMEGAME and
for both WS4-compiled machines); and confinement to v ∈ {0,1}, wherever it can
be certified, collapses the machine *below* the 3x+1 shape onto a closed-form
recurrence rather than onto it. Untouched: **the β-odd half**, where both
flagship machines live and where the control graph on valuations is complete.

**Next experiment:** multi-step / return-map simulation on the β-odd slice. Every
negative above is explicitly *one-step and branch-index-preserving* — that is the
gap they leave, and the only direction where a positive answer is still live.
