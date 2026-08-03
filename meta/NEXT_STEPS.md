# Next steps

_Last revised Aug 3, 2026, after the BBf(23) campaign._

## Where the program actually stands

The program has **decided machines** — its first, and they are wild ones on
a live competition list, not members of a manufactured census. That changes
what "next" should mean.

| | status |
|---|---|
| BBf(23) decisions | 25/694 refined (16 new); official-list sweep running, ~11% hit rate, ~1,100 decided so far |
| the method | rigid phase certificates: miner + checker, end-to-end, soundness proved |
| Lean | 9 machines + decider soundness, sorry-free, mathlib-free; generic layers partly built |
| the sheep | arithmetic closed (H in closed form, no separating modulus, sieve saturates at 29.6%); orbit open |
| the Needle / census | no modulus separates, proved; frontier is a rank-2 S-unit condition |
| machine 4 | halt hunt inconclusive; per-visit p ≈ 0.111 flat, but cost is Θ(a) so it is a T^−0.118 gamble |
| symmetry | negative: holdout list already canonical under the sound relabelling |

**The dividing line the campaign found**, and the thing worth carrying
everywhere: *rigid* (phases repeat a fixed word with formula counts) vs
*digit-consuming*. Rigidity is the decidable margin. It is visible in a
bounded simulation, it explains which machines have historically fallen,
and it is empty-by-construction for the rest — 675 of 694.

## Ranked next steps

### 1. Port the method to Turing machines (BB(6)) — the high-impact bet
BB(6) is where the community's attention is: 1,064 holdouts, and **nobody
has swept them for rigidity**. Our certificate method is orthogonal to
every decider they run (theirs work on tape languages; ours on the
arithmetic of a reduction). The one previously decided machine of this
genre was done by hand, in April 2026.

The blocker is the reduction TM → guarded counter machine, which the
community currently does by hand. That is the research content: a
macro-machine / rule-extraction pass that produces guarded affine rules
automatically, after which the existing miner and checker apply unchanged.
Risk is real (the reduction may not automate cleanly), payoff is the
largest available: it would turn a FRACTRAN result into a general
technique, and it would put the method where the flagship problem is.

### 2. Ship what exists (blocked only on a decision)
The BBf decisions are worth nothing until they reach the people
maintaining the list. Needs: attribution call, then an upstream PR to
int-y1/BBFractran plus a wiki note; the sheep page likewise. Low risk,
high value, currently idle.

### 3. Finish the verified checker
The stage-composition fold, then blocks, then `Cert` + `checkCert`. Until
it lands, ~1,100 machines are checker-verified and only nine are
Lean-verified. This is also the paper's strongest possible claim.

### 4. Sheep: the weighted-automaton lane
The one certificate class not proved empty for it. Two-sided: a positive
decides a named cryptid; a negative is a publishable strengthening.

### Deprioritised, with reasons
* **Machine 4 halt hunt** — measured as a T^−0.118 gamble; the k=34–38
  sweeps are the only decision-relevant part and they are slow. Stop
  unless the sweeps land.
* **More census harvesting** — completeness proved; the box is exhausted.
* **Hydra / Antihydra / Fenrir** — no technique exists for cumulative-count
  halting, by our own q-adic memory theorem.
* **Needle certificate work** — every bounded lane is proved empty.


> **This header is the program's single current-state statement.** Everything
> below it — the July 25 plan, the July 28 status board and evening plan,
> Addenda 1–3, and the July 30 header this replaces — is the historical record
> of how it was reached, kept because the revisions are themselves findings,
> but **no ranking below this header is current.**

## Where the program stands

**The theorem chain of July 28–30 is complete.** Universal sieve lemma
(`B_v ∈ ⟨2⟩ mod A_v`, all odd-β) → ten non-halting machine theorems (labels
T1–T11; T3 is the m = 3 criterion) with a **completeness proof** → C4/C6/C8
congruence criteria → δ-saturation T12 → even-modulus T14 with the β-parity
mechanism → descent lemma → reach lemma → **T15: for β odd, A_v > 0,
gcd(δ,M′)=1, the closure of every residue is all of Z_M at every modulus.**

> **Corollary: no modulus separates the Space Needle. No hypotheses left.**

**Base-q transfer (July 30): machine 3 joins.** M3-N1 (no modulus separates
machine 3), M3-N2 (last-two-steps v₃=1 pinning, 77/81 exact), and the
Needle/machine-3 asymmetry explained by **the rank of the sieve group**
(listable {±3^i} rank 1, theorem side — vs thin {±3^a2^i} rank 2, the open
S-unit frontier).

**July 31 — the program leaves the Needle.** Four machines other than the
Needle were taken up, and every one of them yielded.

* **The sheep machine** (`1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE`, BB(6),
  found by *sheep* 7 April 2026, a listed bbchallenge Cryptid) is the
  **second cryptid inside our interface** and the Needle's sibling with
  β = 3 → 1: census member **(1,1,1,1,0)** plus one exceptional branch at
  oddPart = 3. Results (`sheep/RESULTS.md`, all reproduced in 2 s):
  - **S3** the last-step sieve reduces to `2^(t+1) ≡ 2v−1 (mod 2^(v+1)+1)`
    and **closes completely**: only `v ∈ {0,1}` can precede a halt, every
    `v ≥ 2` forbidden — *proved*. The wiki's `even_case_no_pow2` assumes the
    threshold `a ≥ 2`; here it is the conclusion, and the two survivors are
    located at the same time.
  - **S5** the halting set in closed form, `H = {2^i} ∪ H₀ ∪ H₁` with
    `H₀ = (2^(2j+1)+1)/3` and `H₁ = 2(2^(4j)−1)/5` — *proved*, matched exactly
    against brute force below 300,000. **The Needle has no such closed form.**
  - **S6** no modulus separates it (T15 applies verbatim; verified M ≤ 200).
  - **S2** the census member (1,1,1,1,0) *halts* (3 → 4); the exceptional
    branch intercepts exactly that value. One extra branch on one odd part
    turns a halting census member into an open problem.
  **This is the first empirical confirmation of the rank-of-sieve-group
  dichotomy on a machine we did not construct, and the prediction was on the
  record before we looked.**

* **Machine 1's congruence question is closed** (`machine1/RESULTS.md`).
  **T16** — a machine-independent saturation lemma (`gcd(δ,M) = gcd(ρ,M) = 1`
  ⟹ the closure of any residue under `c ↦ Ac + δn + ε + κρⁿ` is `Z_M`; no
  hypothesis on A or κ), the descent stripped of the VAL(2) schema.
  **M1-D** — the dominant branch's closed form *and its exact domain*, both
  derived. **M1-N1** — no odd modulus separates machine 1, *proved*. With the
  2-adic side, the complete congruence content of machine 1 is exactly
  "D ≡ 9 (mod 16)", which does not separate. Machine 1 is the first case-file
  machine on the **β-even** side of the parity dichotomy.
  **Erratum:** `mod16.py`'s universal claim is false — `F(5) = 17`; four
  producers of a `b = 1` anchor exist, not two, and the closed forms settle
  only two of them. The orbit corollary survives.

* **Machine 4 gets a 2-adic theorem and a genre correction**
  (`machine4/RESULTS.md`). **T8** the image of the return map avoids 13 and 15
  (mod 16) — *proved* via an interior 4-adic confinement (T6) and a parity
  lock (T7). **T9** exactly a quarter of the primary halting family
  (`j ≡ 5,7 mod 16`) is therefore unreachable from any start. And **T11/T12**:
  machine 4's halting set is **not thin** (per-excursion halt probability
  bounded away from 0 over nine octaves) while the orbit visits the section
  only logarithmically often — so its own pseudorandom heuristic **predicts a
  halt**. Machine 4 is the collection's only *probviously-halting* machine,
  and the taxonomy row calling it "sparse coincidence / linear growth" is
  wrong twice over.


## Goals scorecard (July 31)

* **G1 (new observations):** excellent, and now on wild machines: the sheep
  sieve, T16, M1-N1, T8/T9, and the machine-4 genre correction are all new.
* **G2 (decide halting):** 329 manufactured machines decided; **still zero
  wild cryptids decided** — but for the first time the program has produced a
  *proved theorem about a wild cryptid* (sheep S3–S5), sharpening a
  community lemma rather than restating it.
* **G3 (why the hard ones are hard):** the conditional-hardness capstone
  remains the one missing theorem. The sheep gives it a second data point:
  last-step analysis can close completely and leave the orbit question
  untouched.
* **G4 (transferable toolkit):** confirmed hard. The toolkit transferred to a
  machine found by someone else (sheep), and T16 shows the saturation
  machinery does not need the VAL(2) schema at all.

## The current plan

| # | item | status |
|---|---|---|
| 1 | **Publish the sheep results** to the bbchallenge wiki page | ready; needs the user's go-ahead (outward-facing) |
| 2 | **BBf(23) sieve campaign** — run the machine-independent sieve + congruence closure over the 694 refined FRACTRAN holdouts (`github.com/int-y1/BBFractran`) | open; **the one G2 shot that counts** — none of the nine community deciders on that list is a valuation sieve |
| 3 | **Machine 4: hunt the halt** — accelerate the section map (T3 cascade + closed-form returns) and search | open; a *positive* answer would be the program's first decided case-file machine, and the heuristic now says one exists |
| 4 | **Space Needle Variant 1** — extend the interface to "branch-affine + one accumulator" | open; G4's next frontier, with a named machine waiting |
| 5 | **C — conditional hardness** | open; the G3 capstone |
| 6 | **Lean: universal lemma + descent + reach + T16** | open; the verification-monoculture fix |
| 7 | **Lucy's Moonlight** (mod-3 ×8/3, probviously halting) — the same genre machine 4 just joined | open |
| 8 | **F — WFAR search / Erdős machine calibration** | open; the only untried positive-certificate route |

**Stopped, with reasons on record:** census harvesting (completeness proved);
more SAT states / backward depth / congruence rungs; counting-style
universality barriers (refuted as a genre); Skolem-witness machinery (shape
mismatch, proved);
Hydra/Fenrir (outside the interface, and their own q-adic memory theorem
already gives the no-congruence conclusion).

---

# Historical record below this line

## The superseded header of July 30, 2026

> Kept verbatim; superseded by the July 31 header above.

**The theorem chain of July 28-30 is complete.** Universal sieve lemma
(`B_v in <2> mod A_v`, all odd-beta) -> ten non-halting machine theorems
(labels T1-T11; T3 is the m = 3 criterion) with a **completeness proof** (no
twelfth exists; every other machine carries an explicit surviving-branch
certificate) -> C4/C6/C8 congruence criteria -> delta-saturation T12 ->
even-modulus T14 with the beta-parity mechanism -> descent lemma -> reach
lemma -> **T15: for beta odd, A_v > 0, gcd(delta,M') = 1, the closure of every
residue is all of Z_M at every modulus.**

> **Corollary: no modulus separates the Space Needle. No hypotheses left.**

Alongside: Theorem R + T13 (12.31% of the family is provably computation-free),
the refutation of every counting-style universality barrier ("universality is a
property of a single point, not of a family"), and the placement of the
Needle's halting one syntactic step beyond the 2026 linear-exponential
decidability frontier.

**Base-q transfer (July 30): machine 3 joins.** The chain transfers verbatim
with 2->3 (machine 3 = the base-3 (1,1)-class member, delta=1, beta=1):
**M3-N1 -- no modulus separates machine 3**, unconditional; **M3-N2** -- the
last-two-steps v_3=1 pinning is now a theorem for all j (77/81 = 95.06%
exact); and the Needle/machine-3 asymmetry is explained: **the rank of the
sieve group** (listable {+-3^i}, rank 1, theorem side -- vs thin {+-3^a 2^i},
rank 2, the open S-unit frontier). Fenrir/Hydra are structurally outside the
interface (constant branch modulus, path-counter halting); their
no-congruence conclusion already follows from their own q-adic memory
theorem. Verification of record: `machine3/m3_nocert.py`.

**Goals scorecard (from the July 30 strategic review).** G1: excellent --
observations upgraded from measurements to mechanisms. G2: two tracks -- 329
manufactured machines decided (with completeness), **zero of the seven wild
cryptids ever**, now backed by theorems saying why; G2-for-cryptids is
Collatz-hard and should not drive allocation. G3: one theorem from complete --
the conditional-hardness capstone remains. G4: settled and now running both
ways (census produces machines; the new lemmas transfer back to base q).

The July 30 plan ranked: (1) 2-adic reach [done], (2) consolidate + draft the
paper [done], (3) base-q transfer [done], (4) C -- conditional hardness,
(5) positive-theorem portfolio, (6) Lean, (7) F -- WFAR search.

---

# Next steps: the ranked research plan (July 25, 2026)

> Everything from here down is the record of how the plan was made and revised,
> not instructions.


Produced from three commissioned literature surveys (`surveys/`) plus local analysis
of the program's state (meta report §2 goals, §12 open problems, explorations
Findings 1–6). Program goals served, in the meta report's order: **G1** new
observations, **G2** decide halting where possible, **G3** explain what makes the
hard ones hard, **G4** a toolkit that transfers.

**The headline convergence:** all three surveys — commissioned independently on
different literatures — converge on the same top idea from three directions:
*automatic-set (base-q regular) invariants are the one certificate class that our
no-congruence theorems do not exclude, that decides bbchallenge holdouts in
practice (FAR), and that nobody has ever pointed at an arithmetic Collatz-like
map.* And on the same second idea: *the halting-basin density theorem is the most
provable-right-now new theorem available* (the expanding-machine mirror of
Krasikov–Lagarias, with the sign flipped in our favor).

---

## WS1. Automatic-invariant certificates ("FAR for arithmetic maps") — TOP PRIORITY

**The idea.** For a return map F with q-recognizable halting set (Needle: powers
of 2; machine 3: powers of 27 in base 3), search for a q-automatic set I with:
start ∈ I, F(I) ⊆ I, I ∩ Halt = ∅. Any such I is a complete, finite,
machine-checkable non-halting proof. Search by SAT over small DFAs (LSB-first),
exactly as bbchallenge's FAR `mitm_dfa` does over tape languages; verify
candidates by automata products (each closure condition is a decidable statement
of Büchi arithmetic; Walnut-checkable).

**Why this is the best bet.**
- *Untried by anyone*: not in bbchallenge (their FAR runs on unary-coded tapes,
  which collapses to congruences — the very thing our no-congruence theorems
  cover), not in regular model checking, not in the automatic-sequences world
  (survey confirmation, all three reports).
- *Not obstructed*: Dhiman–Pandey (Feb 2026) proved the reachability *relation*
  of 3x+1-type maps is not Büchi-definable — but an *invariant* needs no
  reachability; no known obstruction exists. Congruences are the degenerate
  1-state case of automatic sets; the q-adic branch-memory structure we found in
  Hydra is exactly a digit-pattern conservation law — the non-degenerate kind.
- *Two-sided bet*: success = the first-ever non-halting certificate for a
  cryptid-grade arithmetic map (G2, sensational). Failure at bounded size is a
  theorem: "no q-automatic invariant with ≤ N states" is decidable per machine —
  a strict base-q strengthening of our no-congruence theorems and the first
  structural explanation of why cryptids are "irregular" (G3). Both outcomes
  publish.
- All existing verification-tool certificate classes (Presburger, semialgebraic,
  geometric) are *provably* inexpressive for our machines (survey B5) — automatic
  sets are the unique remaining mechanizable class.

**Concrete first steps.** (1) Needle in base 2: implement the one-step relation
as a base-2 transducer (odd branch (5b−3)/2 is affine — easy; even branch needs
the v-shift — build and verify against `needle.py`). (2) DFA search: SAT encoding
of closure for DFAs of 2..~40 states; UNSAT certificates archived per size.
(3) Same for machine 3 in base 3. (4) Weighted variant (WFAR analog: Z-weights on
transitions, interval acceptance) when the plain search exhausts. (5) Calibration
target: the Erdős 2^n base-3 machine (the community's only certified cryptid with
a regular-digit halting set) — same certificate shape, known open.

**Risks.** The even-branch transducer may not be synchronized-rational (the
+v(b) term adds a logarithm-sized quantity) — then closure must be checked by
bounded-window arguments instead of pure automata products; still SAT-able.
Cobham/Furstenberg ×2-×3 rigidity heuristics suggest the Hydra map has no such
invariant — start with the valuation-driven maps (Needle, machine 3) where the
map "speaks base q" natively.

## WS2. The halting-density theorem ("almost no start halts", quantitatively)

**The idea.** Prove: #{starts ≤ x whose orbit halts} = O(x^c) with explicit
c < 1 (target: polylog for the Needle). This is the expanding-machine mirror of
Krasikov–Lagarias — their backward tree of 1 is thick (lower bounds, x^0.84);
our backward tree of H is thin, and the same stratified counting gives *upper*
bounds, which is the useful direction here.

**Why now.** Local verification (this session): ~~the Needle map is strictly
increasing~~ — **corrected July 26: F is _not_ monotone (F(9)=21 > F(10)=17,
990 inversions below 2000); the property the counting needs is _expansion_,
F(x) ≥ x+3, which does hold** — so H is exactly backward-enumerable, and
backward branching is subcritical — expected preimages per node = Σ_{v≥0} 1/(2^{v+1}+3) = 0.5453 < 1
(**corrected July 27: an earlier draft wrote "1/5 + Σ_v", double-counting the v=0 term**);
empirically ~1 halting seed per octave (Finding 5). The counting tools are in
hand: branch-word enumeration, LTE control of within-ascent structure,
Shallit–Wilson/Stérin bounded-budget regularity giving transfer matrices to pin
c. Kontorovich–Lagarias's η5 ≈ 0.65049 (the 5x+1 backward-tree exponent) is the
established template.

**Deliverable.** A per-machine theorem sequence (Needle first, then machine 3,
then the coincidence machines): rigorous, quantitative "almost all starts never
halt" — G1's strongest available entry, and it formalizes exactly why the fixed
start is a needle in a haystack. Also the k-cutoff lemma that turns Finding 5's
enumeration-with-ceiling into an unconditional count.

## WS3. Baker escalation: block-graded unconditional halting exclusions

**The idea.** Extend Finding 6 up the m-cycle ladder. Grade halting branch words
by block count B (number of ascent/valuation alternations); exclude halting for
all words with ≤ B blocks via two/three-log Baker bounds (Rhin,
Laurent–Mignotte–Nesterenko, Matveev) + continued-fraction reduction + the
verified orbit prefix — precisely the Steiner (B=1, 1977) → Simons–de Weger
(m ≤ 68) → Hercher (m ≤ 91, 2023) architecture, aimed at *halting* instead of
cycles. First transfer of the m-cycle program to an avoidance question.

**Why now.** April 2026: a BB(6) machine was proved non-halting via
Baker–Wüstholz (LLM-assisted formalization) — the first number-theoretic decider
event in bbchallenge; the method demonstrably closes cryptid-adjacent cases. Our
LTE bound is already the B=1 case. Per-family halting equations are dominant-root
/ 2-3-term S-unit — the *decidable* regime (existential Presburger-with-powers,
arXiv:2407.05191). The only known technology producing unconditional statements
about *the actual orbit* (all three surveys agree).

**Deliverable.** "No halt within any branch word of ≤ B blocks" for growing B on
Needle/machine 3; combined with WS2's tree count, potentially full unconditional
non-halting for the most structured family members (G2). Hard ceiling: unbounded
alternation — the Collatz obstruction itself — which is exactly where the program
says the difficulty must live.

## WS4. The formal hardness frontier (upgrade formal/ from class to boundary)

> **EXECUTED July 27, 2026 — `formal/ws4/`.** All three parts delivered, with
> corrections; see the execution note near the end of this file. Read that note
> before reusing anything below: 4.1's framing ("strictly below") was withdrawn,
> 4.2's claim was upgraded from assertion to proof, and 4.3 grew a threshold
> argument that the plan did not anticipate.

Three theorem-shaped write-ups, all assembled from known results + our theorems:
1. **Size frontier**: construct the smallest *universal* machine in our exact
   guarded-counter syntax (Ben-Amram's fixed-modulus Theorem 9 + a small
   universal register machine); state "universal at (counters, rules) = (c,r);
   our cryptids sit strictly below" — the BB(15)-genre hardness result for our
   own format.
2. **The MSB/LSB fault line**: 1D *interval*-branched piecewise-affine
   reachability is open (decidable when injective, LICS 2023); 1D
   *valuation*-branched is Sigma-0-1-complete as a class even at fixed modulus.
   Our machines sit on the undecidable side by branching type, not dimension.
3. **Certificate-impossibility meta-theorems**: (a) the no-sieve theorem (our
   no-congruence results = the affine sieve's fuel provably absent); (b) every
   linear-arithmetic/semialgebraic/geometric non-termination certificate is
   inexpressive for our machines (formalizing survey B5's argument); (c) the
   observation that bbchallenge regular deciders on unary-coded counters reduce
   to congruence+threshold — so our no-congruence theorems are the first
   structural explanation of cryptid decider-resistance.
Feeds G3 directly and gives the meta report a sharp "where and why decision
technology dies" section. Also: engage Carelli (ICALP 2026) — check whether our
families instantiate his weak Collatz mappings and whether his d=2 method
transfers.

## WS5. Join the ecosystem: Fenrir, holdouts, the guarded-affine census, Lean

- **Fenrir case file** (immediate): the first FRACTRAN cryptid (Mar 2026) *is* a
  2-counter guarded affine machine — S(x,2y) → S(x−1,5y+2); S(x,2y+1) → S(x+2,5y);
  halt at S(0,even). Run the full pipeline (accelerate, no-cycle, halting set,
  taxonomy type, P8) as machine 7. Direct comparability with the community.
- **Census**: no census of guarded-affine counter machines exists (MBB covers
  only inc/dec Minsky machines and expects cryptids at size 8–10, unreached;
  BBf covers FRACTRAN, with 21,295 public BBf(23) holdouts). Automate our
  pipeline (Playbooks A+B) and enumerate small guarded-affine machines — the
  discovery engine that turns per-machine handcraft into a program, and the
  natural home for "new model + census + cryptids" (an established, welcomed
  genre). Our existing machines become the founding case files.
- **Lean formalization** of one flagship result (the universal sieve lemma, or the Hydra
  conjugacy — template: rwst/Antihydra-Basics); LLM-assisted formalization is
  now normal practice there. This is the community's price of admission for
  "certified cryptid" status and the durability layer for future agents.
- **Contribute the hardness ranking**: the community has only
  probviously-halting/non-halting tags and explicitly lacks a formal ranking;
  ours (certified vs candidate, Pi-0-1 vs Pi-0-2) fills a stated gap (wiki page
  / discuss post / TMBR mention).

## WS6. The rigorous stochastic backbone

Make the risk accounting a theorem about a proved model, in three steps:
1. **Haar ergodicity** of the q-adic extension of each return map
   (Matthews–Watts hypotheses are checkable for our rules): "for Haar-a.e. seed,
   the branch sequence is normal and the orbit a.s. avoids H" — the correct
   formalization of P5's pseudorandomness, with the measure-zero caveat stated.
2. **Certified spectral gap** for the mantissa circle map (machine 1, Finding 2):
   upgrade the power-iteration numerics to a rigorous Lasota–Yorke + interval
   arithmetic certificate (template: arXiv:2602.19435, 2026) — turning the
   spectral gap 0.77 and the log2(5/4) breakpoint density into theorems.
3. **Stretch — FLP carry combinatorics**: Flatto–Lagarias–Pollington prove no
   real ×3/2 orbit stays in a window shorter than 1/3, by bare-hands carry
   analysis — one of the only unconditional single-orbit theorems for expanding
   ×(p/q) maps, and the one candidate for a non-Baker unconditional constraint
   on our actual orbits (Hydra family / mantissa windows around powers of q).

---

## Suggested sequencing

- **Phase 1 (start immediately, independent of each other):**
  WS1 on the Needle (transducer + SAT search), WS2 on the Needle (density
  theorem), WS5a (Fenrir case file). Three crisp deliverables, each a first.
- **Phase 2:** extend WS1/WS2 to machine 3 and the coincidence machines; WS3
  (Baker ladder); WS4 write-ups.
- **Phase 3:** WS5 census + Lean + community contribution; WS6 backbone.

## What we deliberately will NOT pursue (recorded to save future effort)

- Tao/GGM almost-all transport: provably blocked by expansion (needs
  q < p^{p/(p−1)}, i.e. negative drift; ours is positive) — and unnecessary,
  since WS2 reaches the a.e. statement by the cheap direction.
- Berg–Meinardus functional-equation reformulations: exact but
  difficulty-preserving; 30 years of precedent (including Opfer's failed proof).
- Affine sieve: its only fuel (congruence-quotient expansion) provably absent
  here — write the short no-sieve note (WS4.3a) and stop.
- Skolem-hardness reductions into our families: our halting equations are
  dominant-root — the *decidable* Skolem case; hardness lives in iteration, not
  arithmetic. Pursue Positivity-style conditional hardness (WS4) instead.
- Off-the-shelf non-termination provers: certificate classes provably
  inexpressive (WS4.3b records why).

## Key 2025–2026 external facts the plan leans on

| Fact | Source | Used by |
|---|---|---|
| Fenrir: first FRACTRAN cryptid = 2-counter guarded affine machine (Mar 2026) | wiki/Fenrir | WS5 |
| BB(6) machine proved non-halting via Baker–Wüstholz (Apr 2026) | TMBR Apr 2026 | WS3 |
| Reachability of 3x+1-type maps not Büchi-definable; invariants unobstructed (Feb 2026) | arXiv:2602.06066 | WS1 |
| Carelli: 1-var loop termination ⟺ weak-Collatz reachability conjecture (ICALP 2026) | arXiv:2605.15094 | WS4 |
| Certified transfer-operator spectra with validated numerics (2026) | arXiv:2602.19435 | WS6 |
| MBB census (Dec 2025) expects counter cryptids at size 8–10, unreached; no guarded-affine census exists | wiki/Register_machine | WS5 |
| BBf(23): 21,295 public holdouts (June 2026) | int-y1/BBFractran | WS5 |
| Hercher: no Collatz m-cycles, m ≤ 91 (2023) — the escalation template | J. Integer Seq. 26 | WS3 |
| Kontorovich–Lagarias η5 ≈ 0.65049 backward-tree exponent — the counting template | arXiv:0910.1944 | WS2 |

---

## Revision (July 27, 2026)

### What Phases 1–2 settled

| WS | delivered | bounding resource | reach | cost per extra unit |
|---|---|---|---|---|
| WS1 | no automatic non-halting certificate | DFA states | Needle 11 (LSB minimal-word) / 13 (LSB 0-inv) / 13 (MSB); machine 3, 7 | ×2.7–11.2 solver time per state, **rising monotonically** under single-load measurement |
| WS4 | certificate families converted to one currency; semilinear class refuted | modulus / DFA states | **every m ≤ 20,000, any threshold**, both machines | ~30 s total — this bound is cheap and the SAT bounds are not |
| WS2 | depth-graded polylog density theorem + completeness cutoff lemma | backward depth L | exact complete counts for every fixed L, to x = 10^192 | ×(log x) per unit of depth |
| WS3 | forbidden-valuation theorem + machine-independent sieve | composed steps (rungs) | 1 rung Needle (28.7% of steps); 2 rungs machine 3 (95.06% of pairs) | q_b^(n−1) per rung — saturates at once |
| WS5a | Fenrir as machine 7, exact halting criterion T3 | — | done | — |

Against the goals: **G1** is where the yield is; **G2 did not move** (no cryptid
decided, and none of the three methods composes into a decision); **G3** is the
surprise — the negatives became an account, not a list; **G4** is settled — the
branch-affine interface `F(x) = A_p·m + B_p` on `x = q^|p|·m + val(p)` carries
the sieve, the base-q SAT search and the density counting unmodified.

### Revised ranking for what remains

1. ~~**WS4, rewritten.**~~ **DONE July 27 (evening)** — see the execution note
   below and `formal/ws4/`. The framing survived; two of its premises did not.
   The three bounds are *not* comparable as written, and converting them put the
   LSB headline last by three orders of magnitude; and WS4.1's "our cryptids sit
   strictly below" presumed an answer nobody has, so it is now a stated open
   question instead.
2. **MSB-first automatic invariants** (promoted; the original plan had this only
   as a risk footnote). Every WS1 bound is on **LSB-first** state count, and an
   MSB automaton for the same set can be exponentially smaller — so "no
   certificate at ≤ 11 LSB states" says almost nothing about small MSB ones.
   This is the one place a *positive* WS1 result could still be hiding, which
   makes it the only remaining two-sided bet. Work required: a new encoding (the
   branch relation is not MSB-synchronous); everything else is reused.
3. ~~**WS5 census** (promoted above WS6).~~ **DONE July 27 (evening)** — see
   the execution note below and `census/`. Newly unblocked: the pipeline is
   branch-table-generic, as the WS3 sweep and `sat_generalq.py` demonstrated, so
   it can be run automatically over an enumeration of small guarded-affine
   machines. It is the only item that changes the **supply** of results rather
   than pushing one machine further — the right move when three methods have
   just hit their ceilings on the same two machines.
4. **WS6**, now with a specific target it lacked. ~~Matthews–Watts Haar
   ergodicity is the natural home for the branching-ceiling coincidence
   (measured average backward branching sits *on* its rigorous ceiling on both
   machines — Needle 0.5452 vs 0.5453, machine 3 0.8080 vs 0.8081).~~
   **Corrected July 27: that coincidence is forced and is evidence of nothing.**
   `v_2(b) = v` is automatic given the backward congruence (3-line proof, meta
   report §2.4; verified on both machines), so the interval density *is* the
   ceiling by construction, and `density/density.py` was measuring over an
   interval. ~~The real target is the **tree** deficit: pooled backward branching
   along the complete backward tree of H is 0.433 (Needle) and 0.563 (machine
   3) against ceilings of 0.5453 and 0.8081 — 21% and 30% below, settling
   rather than drifting, unexplained, and in the direction that would
   strengthen WS2.~~ **Corrected July 27 (evening): the tree deficit is forced
   too, and WS6 has no target again.** The exact criterion is
   `y ≡ 2^v + v (mod 2^(v+1)+3)`, one class per branch — but the tree's *roots*
   are H, and a power of 2 meets the cyclic subgroup `<2>` mod A_v, not the
   residue classes. Branch density off a power of 2 is `1/ord_{A_v}(2)` or **0**;
   nine of the first twenty valuations are impossible outright. Predicted root
   branching 0.4336, measured 0.4339. Machine 3 is sharper: only `j=1` survives,
   predicted and measured **0.5000** exactly, i.e. *every preimage of a power of
   27 has `v_3 = 1`*. **Control settles it:** generic roots of the same size sit
   on the ceiling at every depth (0.5205–0.5482 vs 0.5453), the halting tree sits
   20% below at every depth. Code `density/tree_deficit.py`, meta report §2.7.
   Proving `c < 1` *uniformly along the tree* remains open, but there is no
   anomaly to explain.

### Executed July 27 (afternoon) — three items, one of them not on the list

**MSB-first automatic invariants (was ranked 2, "needs a new encoding since the
branch relation is not MSB-synchronous").** *That premise was false.* For **any**
branch-affine machine, eliminating `m` from `x = q^|p| m + val(p)`,
`F(x) = A_p m + B_p` gives `q^|p| F(x) − A_p x = q^|p| B_p − A_p val(p) =: C_p`,
a constant — a single linear relation, hence letter-to-letter synchronous with
running remainder bounded by `|C_p| + q^|p| + A_p`. Verified on both machines
(299,987 and 299,980 values, 0 violations). The product is **O(n²)** against
LSB's O(n³), which makes it 42× cheaper at n=10 (24.6 s vs 1041 s) — and the
ratio *compounds*: 4.00, 9.33, 14.15, 22.60, 42.32 for n=6..10. Result: **no MSB
certificate for the Needle at ≤ 13 states** (n=13 completed UNSAT in 9,174 s),
cross-validated four ways. ~~On a matched cumulative budget MSB reaches 12 where
LSB reaches 10 — a gain of exactly 2 states.~~ **Corrected: the reach gap is
budget-dependent** — 2 states at 1,874 s, 1 at 17,703 s. Both correct; a reach
gap is a function of the budget you fix, and only the *order* of the answer (one
or two states) survives. ~~The wall re-formed with the same gradient.~~
**Retracted twice over:** LSB's newest step is 15.89× against MSB's 10.18×, so
the gradients were never equal — and under WS4's single-load re-measurement the
MSB series is monotone rising, so the apparent fall-back to 5.47× at n=13 was
load, not mathematics (`formal/ws4/clean_growth.py`). Files:
`automatic/msb_search.py`, `msb_validate.py`, `msb_calibrate.py`.

**Encoding adequacy (not on the list; it should have been).** All the
impossibility results are completed UNSATs, which no solver slowness can
undermine. The real risk was an over-constrained encoding making them vacuous,
and the only calibration on record was a machine with a **2-state** certificate.
Now settled by construction rather than by search (`automatic/adequacy.py`):
both encodings provably admit certificates at k = 3, 5, 7, 11, 13, 17, 19, 23,
covering all three claimed bounds. Search-based calibration agrees, finding
planted certificates at exactly n = k. **WS4 can lean on the bounds.**

**Feeding the halting basin into the SAT search — predicted "several states",
delivered one-eighth of a state.** Sound (the clauses are implied, so the
theorem is unchanged) and the effect is real and reproducible (~25–30% faster,
three interleaved runs), but against a per-state factor of 5.5–18.5× it is
nothing. Extra halt values carrying no new information are actively *worse*
(1.28×). The lesson: **the wall is not made of missing information, it is made
of search space.**

A bias to carry forward: refuting at n costs minutes while *finding* a
certificate that exists at n costs hours (k=11: 36 s to refute n=10, 213–2803 s
to find at n=11). This machinery will keep producing negative answers cheaply
and may never produce a positive one — a property of the evidence we generate,
not of the machines.

### Executed July 27 (evening) — WS4, the formal hardness frontier

Code, logs and `RESULTS.md` in `formal/ws4/`; PDF `ws4_report.pdf` reads every
number out of the logs.

- **The three bounds were never comparable, and converting them reorders the
  program.** A congruence certificate is a union of residue classes mod m,
  recognised by **m** states MSB-first and **m·ord_m(2)** LSB-first. So an
  n-state impossibility kills every modulus whose tracker fits in n states:
  MSB ≤ 13 kills m ≤ 13; **LSB ≤ 11 kills exactly {2, 3, 4}**; and a 30-second
  direct sweep kills **every m ≤ 20,000, with any threshold**. The LSB bound —
  the headline for two days — is the weakest of the three on this axis by three
  orders of magnitude. Its durable content was never the state count; it is the
  halting-basin shape, which survives the conversion.
- **One-variable semilinear = congruence + threshold**, so that single sweep
  refutes linear-arithmetic certificates, the affine sieve, *and* every
  bbchallenge regular decider (unary counters ⟹ ultimately periodic) at once.
  The m = 1 case is *proved*, not swept: the orbit is unbounded (T2), a finite
  union of intervals containing it holds a ray, every ray holds a power of 2.
- **New proved lemma (machine 3): `G(a) ≡ v_3(a) (mod 2)`.** Found by diagnosing
  the one modulus (2·3⁸) that survived the sweep — a survivor would have been a
  *proof* of non-halting, so it was worth an hour. It was luck (p = 0.10 once
  the lemma corrects the parity model from ½ to ¼), and the orbit killed it at
  index 105,033.
- **WS4.2 settled by computation, not assertion.** Both hypotheses of the
  decidable 1D-PAM island fail independently: the slope set is *infinite*
  (1 + 3·2^−(v+1), all distinct, → 1) so no refinement repairs the piece count;
  and the maps are not injective (`F(10) = F(12) = 17`, on the published orbit).
- **WS4.1 delivered a verified compiler** (register machine → FRACTRAN-style
  one-counter GAM, ≤ 2I rules, step-exact) and a citation-free anchor (PRIMEGAME
  = 14 rules, checked to emit the primes) — but **withdrew the plan's claim**
  that our cryptids sit strictly below. VAL(q) unfolds one schema into
  infinitely many affine pieces; smaller on the page is not smaller in power.

**The new open question, and the only two-sided bet left:** *is the one-schema
VAL(q) class Turing-complete?* Universal ⟹ the size frontier is vacuous for our
machines and the resistance is structural. Decidable ⟹ **it decides our
cryptids**.

### Executed July 27 (evening) — WS5, the census

Code, logs, `RESULTS.md` in `census/`; PDF `census_report.pdf`.

Family: five integers (α,β,γ,δ,ε), `F(x) = A_v k + B_v` on
`x = 2^(v+1)k + 2^v`, `A_v = α2^(v+1)+β`, `B_v = γ2^v+δv+ε`, halt iff x is a
power of 2. **The Space Needle is (1,3,1,1,0)** — verified against its own step
function. 1,080 enumerated, 3 ill-defined, **1,077 analysed in 220 s**.

- **G2 MOVES, for the first time in four stock-takes. 318 of 1,077 (29.5%)
  decided outright** by an exact congruence test — complete for its class,
  unlike WS4's necessary condition, because A_v, B_v mod m depend on v only
  through `(2^v mod m, v mod m)`, so iterating until that state repeats
  enumerates every branch. **All 318 certificates re-audited by brute force
  without reusing that machinery: 0 failures.** Honest size of the move: these
  are *new and easier* machines, not the cryptids — a machine with a separating
  congruence is by definition not one. 220 s decided 318 machines; two days of
  SAT search bought two states.
- **T1, T2 (proved): two machines never halt after their first step.** (1,1,2,0,1) has
  B_v = A_v so `F(x) = A_v(k+1)` always carries an odd factor > 1. (2,−1,2,1,1)
  has every branch sieved out: mod `A_v = 2^(v+2)−1` the condition collapses to
  "2v+3 is a power of 2", and 2v+3 is odd, > 1 and < A_v.
- **T3 (proved, exact on all 1,077): decided at m=3 ⟺ δ≡0, γ≡α, β+ε≡0 (mod 3).**
  41 predicted, 41 decided, 0 discrepancies. **Corollary — the sharpest thing we
  have on why the flagship resists: the v-linear term blocks the cheapest
  certificate there is, and the Needle has δ=1.**
- **The Needle is not special in anything measured globally.** Drift and the
  branching ceiling are functions of (α,β) ALONE (24 classes, none carrying two
  values), so **45 machines share its drift 0.9411 and ceiling 0.54528 exactly**.
  Both statistics the program spent weeks on are blind to 44 siblings. The sieve
  does separate them (0.0000–0.7988 across the twins; Needle 0.2852, an
  independent reproduction of WS3's 28.7%).
- **β parity is what makes a member hard**: even β decided 68%, odd β 5%; 108 of
  the 120 cryptid candidates have odd β. Odd A_v = the classic Collatz
  situation, no 2-adic structure to exploit.
- **Five machines have every branch forbidden to v=200 and are NOT claimed** —
  that is not "for all v". Best open leads: (2,−1,2,2,1), (2,−1,3,0,0),
  (2,−1,3,1,0), (2,1,1,2,−1), (3,3,2,0,1).

Not touched: whether one-schema VAL(2) is Turing-complete. A census maps a
family; it does not bound its power.

### Added to the "will NOT pursue" list

- **More SAT states, more backward depth, more congruence rungs.** These buy
  constants, not structure: the next Needle state is ~3 hours then ~a day, the
  next depth multiplies the bound by a logarithm, and the next rung does not
  exist (the sieve constrains the last block alone). Recorded so the effort is
  not spent twice.

---

## Status board (July 28, 2026)

**This section supersedes every ranking above it.** Consolidated as meta report
§2.10; this is the working copy.

### Every workstream

| WS | status | delivered | reach attained | goals |
|---|---|---|---|---|
| WS1 automatic invariants | **executed**, closed at its bound | no q-automatic certificate at the sizes searched; encodings proved adequate by construction, so the UNSATs are not vacuous | Needle 13 MSB / 11 LSB minimal-word / 13 LSB 0-invariant; machine 3, 7 in base 3 | G3 |
| WS2 halting density | **executed** | depth-graded polylog density theorem + completeness cutoff lemma | exact complete counts at every fixed depth, to x = 10^192 | G1 |
| WS3 forbidden valuations | **executed**, saturated | unconditional exclusions on the *actual* orbit; sieve proved machine-independent | Needle 28.7% of steps; m3 95.06% of pairs; ladder has one rung | G1, G3 |
| WS4 hardness frontier | **executed** | three bounds in one currency; semilinear refuted wholesale; slope theorem; verified compiler | every m ≤ 20,000, any threshold, both machines, ~30 s | G3 |
| WS5a Fenrir | **executed** | machine 7 + exact halting criterion | complete | G1 |
| WS5b census | **executed** | 318 decided and audited; T1, T2, T3 | whole (α,β,γ,δ,ε) box, 1,077 machines, moduli ≤ 64, 220 s | G2, G1, G3 |
| WS5c Lean + community | **not started** | — | — | G4 |
| WS6 stochastic backbone | **not started; target vacated twice** | — | both anomalies proved forced (§2.4, §2.7) | G1 |

### Progress against the goals

- **G1 (new observations) — the program's main yield, consistently.** Density
  theorem + cutoff lemma, forbidden-valuation theorem, m3 pinned to one
  valuation for the last two steps before any halt, Fenrir's criterion, the
  thin-H law, the slope theorem, T1/T2/T3, and drift+ceiling depending on
  (α,β) alone.
- **G2 (decide halting) — moved once, and only on easier machines.** 318 of
  1,077 census members decided plus two any-start theorems, against **zero of
  the seven case-file cryptids in either direction**. A machine with a
  separating congruence is by definition not a cryptid: the move is real, and
  it is not the move the goal was written for.
- **G3 (explain the hardness) — the surprise; a list became an account.** Four
  measured mechanisms: a certificate must avoid the whole halting *basin*, not
  the halting set; the sieve's strength is governed by how thin H is as a set
  of values; every method is exact inside a bounded resource and silent beyond
  it with the growth constant measured (P9); and δ·v blocks the cheapest
  certificate there is.
- **G4 (transferable toolkit) — settled, and now generative.** The
  branch-affine interface carries the sieve, the SAT search and the density
  counting unmodified; the census made the toolkit *produce* machines, the only
  thing here that scales with compute rather than attention.

**The uncomfortable summary:** every positive result the program has is about
machines that are not hard, and every result about the hard ones is negative.
That is a coherent position — it is what G3 is for — but it should be stated,
not inferred.

### New (July 28): three of the five census leads are now theorems

`census/leads.py`, `census/leads.log`. Checking the unclaimed
all-branches-forbidden leads against *each other* rather than one at a time:

- **Four have `A_v = 2^(v+2) − 1` identically** — the whole α=2, β=−1 corner —
  which is T2's modulus, where `ord(2) = v+2` makes the powers of two the
  listable set {1, 2, …, 2^(v+1)}.
- **Lemma (proved).** Writing branch v's halting condition as
  `2^e ≡ S_v (mod A_v)`, the fixed point gives `P₀ = (2B_v − A_v)2^v`,
  `Q₀ = 1 − 2^(v+1)`; and `2^(v+2) ≡ 1` forces `2^(v+1) ≡ 2⁻¹`, so `Q₀ ≡ 2⁻¹`
  and everything collapses to **`S_v ≡ 2·B_v (mod A_v)`**. Verified: 45
  machines, 18,045 branches, v = 0..400, 0 mismatches.
- A power of two mod A_v is 1 or even, so **S_v odd and > 1 already forbids the
  branch**, as does S_v = 0. Derived targets: 2v+3 (this is T2), 4v+3,
  2^(v+1)+1, 2^(v+1)+2v+1.
- **T4, T5, T6 (proved): (2,−1,2,2,1), (2,−1,3,0,0), (2,−1,3,1,0) never halt
  after their first step.** Derivations, not range checks — the earlier v ≤ 300 sweep
  now confirms the derivation instead of substituting for it. **Statement note:**
  "from any start" was loose in T1/T2 as well — a start that *is* a power of
  two halts at step 0. Brute force found it: all non-power-of-two starts below
  20,000, 400 steps, 0 halts on all five machines.
- **Still open:** (2,1,1,2,−1) has `A_v = 2^(v+2)+1` with `ord(2) = 2(v+2)` —
  still listable, twice as long, so the question is whether S_v avoids a set of
  size 2v+4 rather than v+2. (3,3,2,0,1) has `A_v = 3(2^(v+1)+1)` and a
  v-dependent order (4, 18, 8, 30, 12, 42) — no listable set at all.

**The method lesson, now a trap in meta report §11.** These four sat in a list
for a day, each looking like its own research problem. Nothing new was computed;
the collapse came from putting them in a row and noticing a shared modulus.
*Consolidating the open items is not clerical work — it was the cheapest search
this program has run.* Consolidate **before** deciding what to work on.

### The ranking

1. **Promote one census candidate to a full case file.** T3 says where to look:
   odd β, δ ≠ 0. The 120 candidates are candidates on the strength of an
   undecided orbit alone, which is not the standard the seven case files were
   held to — halting-set characterization, taxonomy placement, equidistribution
   model.
2. **The two leads that did not transfer.** (2,1,1,2,−1) is the more promising:
   its order is still listable, just twice as long, so it is the same argument
   with a weaker margin rather than a new idea. (3,3,2,0,1) needs something else
   entirely.
3. **VAL(q) universality** (meta report §12) — still the only two-sided bet.
   Universal ⟹ the resistance is structural and the size frontier is vacuous for
   our machines. Decidable ⟹ **it decides our cryptids.**
4. **Lean formalization + the community hardness ranking** (WS5c). Durability
   rather than discovery, and the only item here that does not depend on a
   research outcome going our way.
5. ~~**WS6.**~~ **Demoted, and the reason is on the record twice.** Pointed at
   the ceiling coincidence (§2.4 proved it forced), then at the tree deficit
   (§2.7 proved it forced too). Take it up again when a *third*, genuinely
   unexplained measurement appears — not on the strength of its position in a
   plan written before either correction.

~~**Derive S_v symbolically.**~~ **DONE July 28**, above — it was one line, and
it produced T4, T5, T6.

---

## The plan (July 28, 2026, evening)

**This section supersedes the status board above it**, which it outlived by
about six hours. Written after a zoom-out: a literature sweep (2020–26), an
inventory of the corpus's own unexecuted ideas, a census-wide exploitation
sweep, and an analysis of the universality question. Code of record for the new
mathematics: `census/universal.py`, `census/universal.log`.

### What changed underneath the board

**1. The lemma was universal all along, and saying so finished the method.**
`S_v ≡ 2B_v (mod A_v)` was written "for α = 2, β = −1" because that is the
corner it was found in. The derivation uses neither value — reducing the sieve's
fixed point mod `A_v` deletes the `A_v` terms and leaves `P₀Q₀⁻¹ ≡ B_v`. So for
**every** odd-β machine, branch v can precede a halt **iff `B_v ∈ ⟨2⟩ mod A_v`**
(*verified: 672 machines, 51,030 branches, v ≤ 80, 0 mismatches*). And since
`α·2^(v+1) ≡ −β`, multiplying by α gives **`α·S_v ≡ 2αδv + 2αε − βγ`** — affine
in v for every machine. *The exponential is not in the target; it is only in the
modulus.*

**2. Both "open" leads fall, three unseen machines appear, and then it stops.**
T7 = (2,1,1,2,−1), T8 = (3,3,2,0,1), plus **T9 = (2,−1,2,0,1), T10 =
(2,−1,1,2,−1), T11 = (3,3,3,0,0)** — ten machines now proved never to halt
after their first step. The three strays were hidden by a **pool filter** (the
leads came from undecided *growers*; two were congruence-decided, one is a
cycler with F(3)=3) — and for the two congruence-decided ones this is a strict
upgrade from "never halts from x₀=3" to "from any start". **Then the sweep
returns an explicit surviving branch for every other machine in the box.** That
is **completeness, not exhaustion** — the first method this program has closed
with a proof instead of a budget.

**3. The Needle's problem now has a one-line statement, and a negative.**
`A_v = 2^(v+1)+3` forces `2^(v+1) ≡ −3`, so ⟨2⟩ = {±3^a·2^i} and the condition is

> **`2v − 3 ∈ {±3^a·2^i}  (mod 2^(v+1)+3)`**

a 2,3-S-unit membership question. **It does not close**: 18 of the first 41
branches survive, not thinning (v = 34, 37, 38 still survive). The last-step
sieve saturates near 28.7% weighted forever. *No asymptotic exclusion is
available by this route — recorded so nobody searches for one.*

**4. Two placements from the literature, both new to the program.**
- Our theorems are explicit instances of **Skolem's conjecture** (an unsolvable
  exponential Diophantine equation is unsolvable modulo some witness). There is
  an active school — Bertók–Hajdu (arXiv:1407.6499, with a Carmichael-λ
  *algorithm* for constructing the witnessing modulus), Hajdu–Tijdeman (Acta
  Arith. 192), Le–Miyazaki (arXiv:2508.17601, 2025) — and nobody has pointed it
  at a Collatz-like sieve.
- The Needle's lifted halting equation is a **linear-exponential Diophantine
  system** of the shape Dong–Shafrir (STOC 2026, arXiv:2505.19141) and
  Chistikov–Mansutti–Starchak (ICALP 2024, arXiv:2407.07083) prove decidable —
  *except* for one product of a free variable with an exponential, and a modulus
  that is not a power of two. **One syntactic step beyond the 2026 decidability
  frontier.** That is the most precise answer G3 has ever had.

**5. Three lanes confirmed to have no competitor** (as of July 2026): the
1,077-machine census (no census of Collatz-like *arithmetic* machines exists
anywhere), the automatic-invariant negatives (nobody has run an invariant search
on any cryptid map; Dhiman–Pandey constrain only *relations* and are uncited),
and the depth-graded density theorem (no preimage-tree-of-sparse-sets
literature). Fenrir has been untouched by the community since March 2026; the
Space Needle has never had an invariant search by anyone but us; the April 2026
Baker–Wüstholz decider had zero follow-up.

**6. Universality, sharpened.** The (v,k) normal form is a **one-register**
machine — no control state, and (v,k) is a recoding of one integer, not two
counters. Low branches are programmable ((A₀,A₁) surjective up to the parity tie
A₁ ≡ A₀ mod 2; (B₀,B₁) surjective onto ℤ²), but **everything at v ≥ 2 is forced
extrapolation from five integers**. Proved: classic Collatz is **not** embeddable
single-step (no integer (α,β) puts slopes 1/2 and 3/2 on two branches).
Refuted: the idea that α ≥ 2's growth gives an effective halting bound — growth
does not bound the number of chances, since a fresh power of two is passed every
step forever.

### The ranking

| # | move | what it is | risk / payoff |
|---|---|---|---|
| **A** | ~~**Harvest**~~ | **DONE this evening** — T7–T11 verified in-project on two independent code paths, universal lemma + completeness theorem + tier map written into `census/RESULTS.md`, `census_report.pdf` (6 pp, clean) and meta report §2.11 (45 pp, clean) | zero-risk, certain |
| **B** | ~~**The Skolem bridge**~~ | **DONE July 29 — the import failed, the question it raised did not.** BH's class admits only exponents as unknowns; our k and δ·v are linear, and our local-to-global step is a *theorem with a forced modulus*, not a conjecture with a searched one. Their greedy returns a power of two on all 16 forbidden branches tested, never A_v. **But asking "why does no witness modulus exist?" produced T12, the δ-saturation theorem: no odd prime can ever separate the Needle, unconditionally.** Plus C4/C6/C8 and the m=7 correction. `census/saturation.py` | delivered more than assigned |
| **C** | **The hardness address** | formalize per-branch halting as a linear-exponential system; mechanize per-family finiteness via the ICALP-24 NP procedure; attempt a Dong–Shafrir-style conditional-hardness theorem ("deciding our schema decides variable-coefficient base-{2,3} systems") | deep; the G3 endgame. **Now the top open item** |
| **D** | ~~**The expressiveness barrier**~~ | **DONE July 29 — the barrier holds only on a slice, and the genre is refuted.** Theorem R (rigidity) + T13: 12.31% of machines are provably computation-free. But measured branch bandwidth is ≥ M for every modulus, so the counting argument fails — and *universality is a property of a single point, not of a family*, which retires every rank/dimension/density variant. What survives is a slope-resolution **compression** bound. `formal/ws4/rigidity.py` | negative, and the negative is the value |
| **E** | **The Needle family** | promote the exact sieve-twin **(1,3,2,2,0)** — identical forbidden set at every v — and the top siblings to a *family* case file; the twin is a controlled experiment. Also WS2's real open step: uniform c < 1 along the backward tree, where `density/tree_deficit.log` already tabulates the depth-≥3 rebound nobody analyzed | the only lane touching the actual cryptids' orbits |
| **F** | **Last positive-certificate bet** | the **weighted-automaton (WFAR-analogue) search** — Z-weights, interval acceptance. Its trigger condition ("when the plain search exhausts") was met and it was never built. Also point the existing SAT machinery at Antihydra's ⌊3n/2⌋ map for direct community comparability | two-sided; the only remaining route to a *positive* certificate |
| **G** | **Stake the empty lanes** | census + T1–T11 + tier map is paper-shaped; Fenrir wiki contribution (we are ahead of the community and unpublished); the certified-vs-candidate hardness ranking (`formal/ranking.py`, built, never contributed); Lean one flagship result | durability; independent of any research outcome |

**Recommended order: B and D in parallel** (highest information per unit
effort), **E** as the standing research line, **G** ongoing in the background.

### Recorded negatives (so the effort is not spent twice)

- **No asymptotic all-branches-forbidden theorem for the Needle.** The surviving
  branch set does not thin out; the sieve saturates near 28.7%.
- **The sieve-to-theorem pipeline is finished at ten machines**, with a
  completeness proof. More sweeping cannot produce a twelfth.
- **α ≥ 2 does not give an effective halting bound** by growth alone.
- **Classic Collatz is not single-step embeddable** in the schema.
- Still standing from the previous round: more SAT states, more backward depth,
  and more congruence rungs all buy constants, not structure.

### The method lesson, second instance in two days

Yesterday: *consolidating the open items is itself a search.* Today, its sharper
form: **the leads were closed not by new computation but by deleting a
hypothesis nobody had tested.** "For α = 2, β = −1" was in the lemma because
that is where it was found, not because the proof needed it — and that phrase
alone kept two theorems classified as hard open leads and three more machines
out of sight. Both are now traps in meta report §11, along with a third: **a
filter chosen for one purpose silently bounds every later use of the list it
produced.**

---

## Addendum (July 29, 2026): what B and D returned, and the revised ranking

Both commissioned imports **failed at their assigned task and produced something
better**. Code: `census/saturation.py`, `formal/ws4/rigidity.py`; meta report
§2.12. All results below were re-verified independently before being recorded.

### New theorems

- **T12, δ-saturation (proved).** For M odd with `gcd(δ,M)=1` and
  `gcd(ord_M(2),M)=1`, the one-step image `{φ_v(c)}` is *all* of Z_M.
  **Corollary: no odd prime modulus can ever separate the Space Needle** —
  unconditionally, not up to a bound. Falsifier run: of the 318 separating
  certificates, 274 have even modulus, 44 fail a gcd condition, **0 would
  refute**. Honest boundary: **even M is not covered**, and that is where 274 of
  the 318 certificates live.
- **C4, C6, C8 (proved)** — the T3-analogues at m = 4, 6, 8, each verified
  *completely* on (Z_m)⁵ and against all 1,077 census machines, 0 discrepancies.
- **Theorem R + T13 (proved).** Branch v is rigid iff `v₂(B_v) < v₂(A_v)`; if
  every branch is rigid the orbit has a closed form and the machine cannot carry
  a computation. **12.31% of the box (2,351 of 19,092).**
- **Slope-resolution bound (proved).** At most `⌊log₂(|β|/ρ)⌋` branches are
  ρ-separated in slope — an exponential *compression* bound, not an impossibility.

### The genre-level refutation (the most important item here)

The counting barrier is **false**: branch bandwidth is ≥ M for every modulus
tested (100 at M=23, 412 at M=101, 1,036 at M=257), so VAL(2) supplies at least
as many branch behaviours as a Conway reduction consumes. The reason generalises:

> **Universality is a property of a single point, not of a family.**

Every "too few degrees of freedom / rank ≤ 5 / density / bandwidth" argument is
therefore answering a question nobody asked — including the composite-step
version. **Do not attempt any of them.** A real barrier needs a property shared
by every point; only two are known (Theorem R, β-even only; and the slope
spectrum, which gives compression rather than impossibility).

### Corrections found by verification

- The deciding-modulus list in `census/RESULTS.md` **omitted m = 7** and its
  three machines — why its counts never reconciled. Fixed.
- The rigidity criterion "`gcd(δ,2^a) ∤ ε` with `a = v₂(β) ≥ 1`" is exact on
  β even and **nonzero**, but **silently omits β = 0**, which supplies 758 of
  the 2,351 rigid machines. β = 0 makes `v₂(A_v) = v+1` unbounded, so rigidity
  there is generic rather than exceptional. Recorded in `formal/ws4/RESULTS.md`.
- **Naming collision caught:** B's report called its congruence criteria
  "T7/T8/T9", but T7–T11 are the non-halting machine theorems from §2.11. The
  congruence family is now **C4, C6, C8** (companions to T3), δ-saturation is
  **T12**, and the rigidity barrier is **T13**.

### Revised ranking

1. **C — the hardness address.** Now the top open item: formalize per-branch
   halting as a linear-exponential system and attempt the conditional-hardness
   theorem. G3's endgame, and the literature is moving (Dong–Shafrir announced
   follow-ups).
2. **The even-modulus question**, newly sharp and newly cheap. T12 covers odd M
   only; 274 of 318 certificates live at even moduli. Either extend T12 to even
   M (2 is not invertible — a genuinely different argument) or prove that even
   moduli are where any surviving certificate must be.
3. **E — the Needle family**, unchanged: the exact sieve-twin (1,3,2,2,0) as a
   controlled experiment, and WS2's uniform-c step with the depth-≥3 tree data
   already tabulated.
4. **Multi-step / return-map simulation on the β-odd slice** — the only live
   direction on universality. Every negative to date is *one-step and
   branch-index-preserving*; that is precisely the gap left.
5. **F — the weighted-automaton search**, still the only untried route to a
   *positive* certificate.
6. **G — stake the empty lanes**, ongoing.

### Added to the "will NOT pursue" list

- **Every counting/dimension/rank/density barrier against universality.**
  Refuted as a genre, with the reason. See above.
- **Bertók–Hajdu / Skolem witness construction as a tool.** Shape mismatch is
  structural: our unknowns are linear where theirs are exponential. Keep the
  connection as an orienting remark only.

### The method lesson, third instance in three days

Three results in three days, and **none of them came from new computation**:
consolidating the board (§2.10), deleting an untested hypothesis (§2.11), and
now extracting the question from two failed imports (§2.12). Each time the
material was already on disk. The operative question each time was *what does
this actually depend on?* — asked about a status list, about a lemma's stated
hypotheses, and about why an import would not fit.

---

## Addendum 2 (July 29, 2026, later): the even half is closed, and #1 is done

`census/even_saturation.py`, `even_saturation.log`; meta report §2.13.
Ranked item #1 from the addendum above is **executed**.

### T14 — even-modulus saturation (proved)

**The mechanism, which is the whole content:** write M = 2^s·M'. A source residue
with `v₂(c) = v < s` **pins the branch index exactly** — the low bits of the value
*are* the valuation, and that is precisely the information T12 proves an odd
modulus can never have. On a source ≡ 0 (mod 2^s), k is free mod 2^s and the
target is `βk + δv + ε (mod 2^s)`: **β odd sweeps everything and kills the 2-adic
information in one step; β even leaves ⟨gcd(β,2^s)⟩ — the escape hatch.**

So the census's oldest empirical fact — β parity is what makes a member hard — is
not a tendency but this mechanism.

**T14.** For M = 2^s·M' with (i) β odd, (ii) `gcd(δ,M')=1`,
(iii) `gcd(ord_{M'}(2),M')=1`, (iv) the closure reaching a residue ≡ 0 mod 2^s:
the closure is all of Z_M — no separation, no branch excluded.

**Falsifier: 267 of the 274 even-modulus certificates have β even, 7 have δ = 0,
0 would refute.** The census confirmed the mechanism without being asked.

**T14′ — the sharp form, an *iff*.** Mod M', `a_v = B_v − A_v/2 =
(γ−α)2^v + δv + (ε − β/2)` and `μ_v = α + β/2^(v+1)` — no hidden v-dependence.
Writing `v = v₀ + j·ord`, `φ_v(c) = φ_(v₀)(c) + δ·ord·j`, which sweeps ⟨g⟩ with
`g = gcd(ord,M')`. So the closure is everything **iff the ord base points cover
all g cosets** — decidable in O(ord), with (iii) its trivial case g = 1.

### Scorecard, stated precisely

- **Proved, no upper bound on M:** no modulus whose odd part satisfies
  `gcd(ord_{M'}(2),M')=1` separates the Needle. **12,916 of 19,999 moduli ≤
  20,000 — 64.58%** — by a one-line gcd test, where WS4 had only a computation.
- **Reduced, not proved:** the remaining third. T14′ covers it in every case
  tested, but it is a per-modulus test, not a closed form in (α,…,ε). A descent
  exists (`g₁ = gcd(ord_g(2),g) < g` for g > 1) but needs the base points
  controlled at every level. **Named as a gap.**

### Revised ranking

1. **Close the descent.** Turn T14′ into a closed form: show the base points
   cover the cosets at every level of the `g → gcd(ord_g(2),g)` recursion. If it
   works, "**no modulus whatever separates the Space Needle**" becomes a theorem
   — the first unbounded statement about the flagship in either direction. The
   reduction is done; only the descent remains. **Cheapest high-value item.**
2. **C — the hardness address** (linear-exponential conditional hardness). The
   G3 endgame; unchanged.
3. **E — the Needle family**: the exact sieve-twin (1,3,2,2,0) as a controlled
   experiment, and WS2's uniform-c step.
4. **Multi-step / return-map simulation on the β-odd slice** — the only live
   direction on universality.
5. **F — the weighted-automaton search**, still the only untried route to a
   *positive* certificate.
6. **G — stake the empty lanes**, ongoing.

### What the last two days changed about the program's position

The uncomfortable summary was: *every positive result is about machines that are
not hard; every result about the hard ones is negative.* Still true. But the
**kind** of negative has changed — from a spent budget ("nothing below 20,000")
to an unconditional theorem over infinitely many moduli. That is the first thing
the program has said with no upper bound about the flagship itself, and it is
what G3 was written to want.

---

## Addendum 3 (July 30, 2026): the descent closed, and so did the question

`census/descent.py`, `descent.log`; meta report §2.14. Ranked item #1 from
Addendum 2 is **executed**, and it went further than expected.

### The descent lemma (proved) — hypothesis (iii) was never needed

**What exposed it is a methodological point.** T14's proof used a *single* step
from c₀ — but the object being bounded is a **closure**, so composition is free.
The cheap first experiment was "redo the M′-part with two steps". It returned
something better: the **one-step** image was already all of Z_{M'} in every one
of 6,336 uncovered cases. The coset analysis had simply been too pessimistic.

> **Descent lemma.** M odd with `gcd(δ,M) = 1` ⟹ the one-step image is all of
> Z_M, with **no condition on `ord_M(2)`**.

Proof: with `g_(j+1) = gcd(ord_{g_j}(2), g_j)`, the chain descends strictly
(`ord_g(2) ≤ λ(g) < g`) and terminates at 1; and at each level
`I_j = Z_{g_j} ⟺ I_(j+1) = Z_{g_(j+1)}`, because reducing the image mod
`g_(j+1)` annihilates the shifts and leaves exactly the base points. The chain of
equivalences bottoms out at the trivial modulus, so every level is full.

**The point the first attempt missed:** the shifts sweep a *full* subgroup
because v ranges over **infinitely many** integers. Restricting v to one period —
what a finite search does, and what the conservative hypothesis silently assumed
— loses exactly that.

*Verified: 2,500 instances with `gcd(δ,M)=1`, of which 708 have
`gcd(ord_M(2),M) > 1` — precisely the excluded cases — 0 failures. Chain descends
for every odd g < 6,000, longest chain 7.*

### The corollary

> **No modulus separates the Space Needle** — odd or even, no upper bound, no
> arithmetic side condition.

*Verified: every modulus 2..400, 0 separate. Falsifier: of the 318 certificates,
267 fail "β odd", 51 fail the gcd condition, 0 fail 2-adic reach, and **0 are
explained by the dropped hypothesis alone**.*

**Still a hypothesis: 2-adic reach**, verified on 8,512 cases with 0 failures but
not proved. It is a condition on the closure, not on the parameters — decidable
per (machine, modulus), which is not the same as true for all M.
**The arithmetic side is closed; one reachability hypothesis remains.**

### Revised ranking

1. ~~**Prove 2-adic reach for β odd.**~~ **DONE July 30 (afternoon)** — the
   reach lemma, `census/reach.py`, meta report §2.15. Proved by the T-lift /
   exponent-ledger argument (each step spends v+1 bits of the lift's free
   coefficient; either a divisibility event lands the orbit on 0 mod 2^s or the
   ledger empties and β odd makes the free multiplier a unit that sweeps
   everything). Constructively verified: 4,000 witness orbits built and run, 0
   failures; falsifier confirms β-even certificate machines are exactly where
   reach fails. **T15 (final form): β odd, A_v > 0, gcd(δ,M') = 1 ⟹ closure =
   Z_M at every modulus. Corollary: no modulus separates the Space Needle — no
   hypotheses left.** The strategic-review plan's item 1 is complete.
2. **C — the hardness address.** Now unambiguously the main open line: per-branch
   halting as a linear-exponential system, aiming at the Dong–Shafrir-style
   conditional-hardness theorem. G3's endgame.
3. **E — the Needle family.** The exact sieve-twin (1,3,2,2,0) as a controlled
   experiment; WS2's uniform-c step.
4. **Multi-step / return-map simulation on the β-odd slice** — the only live
   direction on universality.
5. **F — the weighted-automaton search**, the only untried route to a *positive*
   certificate.
6. **G — stake the empty lanes**, ongoing. Note this now includes a genuinely
   publishable unit: *the congruence-certificate question for a cryptid-grade
   machine, answered.*

### The method lesson, fourth in four days

Every result this week came from re-reading what was already there, not from new
computation. This one is the sharpest instance: **the conservative hypothesis
came from analysing one step of an object defined by closure.** The fix was to
ask what the *definition* allowed rather than what the first proof used. Related
trap, now in §11: a hypothesis introduced to make a proof go through is a
statement about the proof, not about the theorem — test it before you publish it.
