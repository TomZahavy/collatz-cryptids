# BBf / BB(6) holdout sweep — the BW-sibling hunt (round 11, Aug 1 2026)

Artifacts from the rigid-tail sweep of the community holdout lists, hunting
siblings of the April 2026 Baker–Wüstholz-decided BB(6) machine (rigid
closed-form orbit + power/valuation halting margin).

## Lists (provenance in bbf_README.md notes; all verified line counts)

* `bb6_holdouts_1064.txt` — BB(6) holdouts, mxdys, July 28 2026 (1,064
  machines up to equivalence), from wiki.bbchallenge.org.
* `bbf_sz23_21233.txt` — official BBf(23) FRACTRAN holdouts, July 10 2026
  (21,233), from github.com/int-y1/BBFractran.
* `bbf_sz23_694_unofficial.txt` — refined list, July 25 2026 (694; "unofficial"
  because its decider is not yet independently reproduced).

Convention: start n = 2; the FIRST fraction in list order whose denominator
divides n fires; halt when none does.

## Detector (agent-built, layered, replay-verified)

`fractran_accel.py` (exact O(1) run-jumps), `level2.py` (repeated-block
jumps; the one heuristic layer — census numbers are flags, not proofs),
`phase_detect.py` (phase segmentation + series classification GEO/POLY/
NONRIGID).

## Census results

* refined 694: **9 GEO + 10 POLY + 675 NONRIGID** (`scan694.tsv`); the 9 GEO
  collapse under reordering/prime-relabeling to ~3 machine families.
* official 21,233: 3,253 GEO (15.3%) + 6,797 POLY (32.0%) + 11,183 NONRIGID
  (`scan21233.tsv`, light budget — flags only).

## The three worked candidates — closed forms INDEPENDENTLY VERIFIED

`verify_candidates.py` is the main session's independent check (fresh
simulator, not the agent's code): direct big-int replay vs the claimed
boundary formulas.

| # | fractions | boundary state | at step | verified |
|---|---|---|---|---|
| 431 | 5/6, 9/35, 8/55, 7/2, 605/7 | `2^(2^(i+1)-1)·11^i` | `2^(i+3)-5i-8` | **PROVED NEVER HALTS — see m431_proof.py** |
| 455 | 63/10, 8/77, 33/2, 5/9, 7/3 | `v2,v3,v11 = 2^i+1, 2^i-2, i-1` | `2^(i+2)-5` | 17 boundaries exact, 0 mismatches |
| 678 | 9/70, 25/2, 44/15, 7/55, 3/5 | `5^(2^(i+2))·11^(2^(i+1)-1)`, invariant `v5 = 2(v11+1)` | `7·2^(i+1)-3i-9` | 14 boundaries exact (i ≤ 12), invariant holds at all |

Agent additionally verified each to phase ≈ 140 (≈ 10^44 steps) via the
exact accelerated replay, and the halting-condition analogues to i = 10^4.

**STATUS (Aug 2): ALL NINE RIGID HOLDOUTS ARE DECIDED — every GEO machine
on the refined BBf(23) list is proved non-halting.**

| machine | fractions | proof | template |
|---|---|---|---|
| 431 | 5/6, 9/35, 8/55, 7/2, 605/7 | m431_proof.py | linear fuel v11 = i |
| 455 | 63/10, 8/77, 33/2, 5/9, 7/3 | m455_proof.py | linear fuel v11 = i−1 |
| 678 | 9/70, 25/2, 44/15, 7/55, 3/5 | m678_proof.py | invariant v5 = 2(v11+1) |
| 673 | 9/35, 5/6, … | m_siblings_proofs.py | 431's, rules 0↔1 |
| 502 | 7/15, 9/14, 125/77, 2/5, 847/2 | m_siblings_proofs.py | 431's under π = (2 5 7) |
| 623 | 9/10, 5/21, 343/55, 2/7, 605/2 | m_siblings_proofs.py | 431's under (2 7), 0↔1 |
| 574 | 8/15, 147/22, 35/2, 11/49, 3/7 | m_siblings_proofs.py | own: pair mode |
| 570 | 77/30, 88/21, 9/2, 5/11, 7/3 | m_siblings_proofs.py | own: 455-like, rotated |
| 680 | 9/70, 44/15, 25/2, 7/55, 3/5 | m_siblings_proofs.py | own: 678-like, rotated |

**THE DECIDER (Aug 2, `decider.py`).** The nine hand proofs are now
subsumed by a general certified decision procedure: a *rigid phase
certificate* (boundary family + staged phase word over the expression
class EXP = {a + bn + c·2^n}, rational a,b,c) checked fully symbolically —
chain identities by coefficient equality (sound: {1, n, 2^n} linearly
independent), guards at block-rectangle corners with eventual-positivity
in EXP decided outright, priority exclusion via single-condition failure
(the conjunction-level check would be unsound — see docstring). Checker
acceptance ⇒ never halts, FOR ALL phase indices — strictly stronger than
the per-proof idx ≤ 2000 sweeps. All nine certificates accepted in 0.2 s;
falsifier: 540 corrupted certificates, all rejected, 0 wrongly accepted.
**Equivalence decider** (template isomorphism = rule bijection + axis
permutation, exact certificate match): classes {431, 502, 623, 673},
{455}, {570}, {574}, {678}, {680} — the corrected family structure, now
formal. Next: certificate MINER (raw fractions → certificate) for true
end-to-end decision; Lean (in progress); paper (PAPER_OUTLINE.md).

**LEAN (Aug 2, `lean/`).** Machine 431's non-halting theorem is FULLY
FORMALIZED in Lean 4 (no mathlib): `m431_never_halts : NeverHalts M431
(1,0,0,0,0)` — 0 sorries, axiom audit clean (propext / Classical.choice /
Quot.sound only; the entry lemma is axiom-free), clean `lake build` in
under 2 s, independently re-verified by the main session. General
framework in `LeanBbf/Fractran.lean` (priority semantics, block-iteration
lemma, affine endpoint lemmas). Faithfulness boundary (flagged): the
formalized object is the exponent-vector machine; the bridge to
divisibility FRACTRAN is unformalized (unique-factorization machinery).
A nice find: B_0 = (1,0,0,0,0) is the start, so the entry IS the i = 0
phase.

**Lean transports (Aug 2, later): 673, 502, 623 DONE — 4 of 9 machines
formalized.** `LeanBbf/Siblings431.lean`: the `FireSpec` structure — six
φ-transported firing obligations checked against each sibling's OWN
priority order — with 431's whole phase development and induction proved
ONCE over abstract (M, φ), instantiated three times. This is the Lean
counterpart of decider.py's certificate transport. The key subtlety: the
generic fire0 is demanded only at v7 = 0 states, which is exactly what
makes the f0/f1 priority swaps of 673/623 transparent (and provably
cannot fit 574/680 — matching the decider's non-isomorphism verdict).
All three theorems: 0 sorry, core axioms only, entries axiom-free;
independently re-verified.

**LEAN COMPLETE (Aug 2): ALL NINE MACHINES FORMALIZED, SORRY-FREE.**
`lean/` builds clean from scratch in ~4 s (11 jobs); every file has 0
sorries; no `admit`, no `native_decide`, no `axiom` declarations; the
nine `m*_never_halts` theorems each depend on exactly the three Lean core
axioms (propext, Classical.choice, Quot.sound). Files: Fractran.lean
(general semantics + block-iteration + affine endpoint lemmas), M431,
Siblings431 (673/502/623 via the FireSpec transport), M455, M678, M574,
M570, M680.

Formalization findings worth keeping:
* **Entries collapse.** The Python case files enter at Bst 4 after 36
  (574), 76 (570), 78 (680), 41 (678) steps because the templates were
  only stated for large indices. The Lean phase lemmas hold for ALL
  parameter values, so the real entries are: 574 -> **1 step**, 570 ->
  **1 step**, 678 -> 16 steps (B_1), and 680 -> **0 steps: the start
  state (1,0,0,0,0) IS its m = 0 boundary.** The old entry counts are
  recovered as `T 3` / `T 4` and kept as ground-truth cross-checks.
* **Two firing shapes per rule are the norm**, not the exception: a rule
  is typically disabled by different coordinates in different stages
  (e.g. 680's f2 needs `v5 = 0` inside the Q/T blocks but `v3 = v7 = 0`
  during the opening `f2^X` run). Getting this wrong is the single most
  common error; the decider's single-condition priority rule is the
  same fact in checker form.
* 574 is the only one of the nine with **no parity split** (pair mode).

**DECIDER SOUNDNESS FORMALIZED (`lean/LeanBbf/Decider.lean`).** The
mathematics that makes the checker sound is now itself in Lean:
* **Theorem A** `neverHalts_of_phases` — the certificate contract:
  entry + (every boundary steps to the next in >= 1 steps) => NeverHalts.
  Machine-independent; four of the nine are re-derived through it.
* **Theorem B** `affine2_nonneg_of_corners` / `affine2_le_of_corners` —
  the corner principle: a jointly-affine guard value nonneg at the four
  corners of a block rectangle is nonneg throughout. Licenses check C2.
* **Theorem C** `single_conjunct_exclusion` (sound) together with
  `disjunctive_endpoint_check_unsound` — an explicit machine-checked
  counterexample showing that endpoint-testing a conjunctive guard's
  NEGATION is unsound (the two ends can be witnessed by different
  conjuncts: t and 2-t on [0,2] both fail at an end, both hold at t=1).
  So the checker's single-conjunct discipline is REQUIRED, not a
  convenience. The counterexample is axiom-free.
NOT formalized (stated in the paper): the Python implementation itself.
What is proved is that no certificate satisfying the contract can exist
for a halting machine.

**THE MINER (Aug 3, `miner.py` + `sweep_mine.py`) — the decider is now
END-TO-END, and it decided 16 machines we had not.**

`miner.py` takes a raw fraction list and returns a certificate: simulate;
take each rule's run-start positions as boundary candidates; fit the
boundary family exactly over Q to EXP = {a + bn + c*2^n}; segment each
phase into runs and blocks (maximal repetition of a period-2..4 sub-word);
require the stage signature to be constant within a parity class; fit the
run/block counts; compose block starts symbolically. Every proposal goes
to `decider.check`, which stays the sole authority — the miner needs no
correctness proof.

* **9/9 of the hand-proved machines are rediscovered from the fraction
  lists alone**, several with better entries than we found by hand.
* **Full sweep of the refined 694 list: 25 DECIDED, 669 no certificate,
  0 anomalies** (518 s). Of the 25, **16 are new** — machines nobody had
  decided. Each was re-checked by the checker and independently
  brute-force simulated for 200,000 steps without halting.
* Example new decision: line 97 of the refined list = line 2880 of the
  official 21,233 list, `[1/6, 35/2, 4/55, 3/5, 29282/21]`, certified for
  all phases n >= 1 with a single branch (no parity split); boundary
  B(n) = (0, 0, 4*2^n - 3, 14*2^n - 6n - 13, 0).
* Results in `mined_decided.txt`, log in `sweep_mine_694.log`.

**Status distinction that matters:** the original **nine are
Lean-verified**; the **sixteen new ones are checker-verified only** (the
checker's soundness is itself Lean-verified, but each machine's
certificate has not been transcribed into Lean). Formalizing them is
mechanical but not yet done.

**A bug worth recording.** The miner first found *nothing*. Cause was
mine: for a run stage `("run", rule, count)` the code read index 1 (the
rule) instead of index 2 (the count); blocks were unaffected, so the
failure looked structural rather than clerical. The checker's rejection
message (a v7 coordinate going negative, `E(7,0,-2) >= 1`) localized it.
This is exactly the value of keeping the checker as an independent
authority over the search.

**EQUIVALENCE SWEEP (`equiv_sweep.py`, `equiv_general.py`) — a NEGATIVE
result worth keeping.** Can the holdout list be shrunk by proving
machines equivalent? Two programs are conjugate if a permutation of the
primes carries one onto the other in order. The catch: every program
starts at n = 2, so a permutation pi moves the start to e_pi(2), and the
halting-from-2 question transfers ONLY when pi fixes the prime 2.

Measured over the full official 21,233-machine list (general prime
basis, not just 2/3/5/7/11):
* under permutations FIXING 2 (the sound symmetry): **21,233 classes from
  21,233 machines — ZERO reduction.** The list is already canonical.
* under ALL prime permutations (NOT sound for start n=2): 15,600 classes,
  so 5,633 machines (26.5%) are dynamically conjugate to another entry
  while remaining genuinely distinct questions.

So pure relabelling is exhausted. The residue that IS real: conjugate
machines have template-isomorphic certificates, so the expensive part —
the phase analysis — transfers even though the decision does not.

**SWEEP OF THE OFFICIAL 21,233 LIST — IN PROGRESS.**
`sweep_mine_21233.log` is a PARTIAL run at the time of this commit: 744
machines decided, scan reached roughly line 7,600 of 21,233. Treat the
count as a lower bound in progress, not a final figure. The completed
694-list sweep (25 decided, 16 new, 0 anomalies, all deep-verified to
10^6 steps) is the finished result.

**TOWARD A VERIFIED CHECKER (Aug 3, `lean/LeanBbf/Runner.lean`).** Step
one of collapsing all machine proofs into a single theorem. The generic
priority-firing lemma:

    step_of_first : M = pre ++ r :: post -> (all of pre disabled at s)
                    -> r enabled at s -> step M s = some (r.act s)

plus `step_none_of_all_disabled`, `step_isSome_of_enabled`, `run_rule`,
`block_of_steps`. All machine-independent, 0 sorries.

Measured saving on M431 (`DemoRunner.lean` re-derives its firing lemmas
from the generic one): **42 hand-written lines -> 10**, and each proof is
now `step_of_first [..] f_i [..] (by simp [..]) (by simp [..] <;> omega)`
-- the priority reasoning is discharged by `simp` alone rather than by a
hand-written `rw [if_neg ...]` chain per rule.

**SYMBOLIC LAYER BUILT (`lean/LeanBbf/Exp.lean`).** The design problem
was rational coefficients: the Python certificates use denominators 2 and
3 (e.g. 431's block count (2*2^n-2)/3), and building Q without mathlib
plus deciding integrality needs the periodicity of n -> 2^n mod d.

**That disappears with a change of generator.** A parity branch has
n = 2m+r, so 2^n = 2^r * 4^m; re-index by m and add the generator
geo q m = 1 + q + ... + q^(m-1), an integer BY CONSTRUCTION (defined by
its recurrence). Then (2*2^n-2)/3 at n=2m IS 2*geo 4 m -- integral, no
denominator. Verified that this covers every denominator in the nine.
So the class is  a + b*m + c*q^m + g*geo q m,  integer coefficients only,
closed under m -> m+1, addition and scaling.

Proved (0 sorries, core axioms): `eval_mono` (monotonicity criterion),
`le_eval_of_mono`, and the executable test `alwaysGE` with
**`alwaysGE_sound` -- one Boolean evaluation yielding an INFINITE family
of guard inequalities.** That is the property that lets a finite
certificate cover all phase indices. The criterion is deliberately
SUFFICIENT-not-complete: the checker may reject a certificate it cannot
certify, which costs completeness and never soundness. Compile-time
examples include one the test correctly REJECTS (5 - m is not eventually
>= 1). Mathlib-free throughout: no `ring`, no `push_cast`, no
`Monoid.npow` -- powers are an explicit recursion and the algebra is core
Int lemmas plus omega, with the two comparisons omega cannot make
(`k*x <= k*(q*x)`) supplied as lemmas.

**MIDDLE LAYER, CORE BUILT (`lean/LeanBbf/Check.lean`).** The piece that
turns certificate data into `Steps`:
* `run_affine` / `run_affine_of_rule` — a rule fired k times along an
  affine segment, proved ONCE for an arbitrary machine and an arbitrary
  integer delta. Every machine file currently proves 3-4 instances of
  this by hand (`run_f0`, `run_f2`, ...), each its own induction.
* `coord_ge_of_endpoints` / `coord_lt_of_endpoints` — the endpoint
  interface: a guard bound holding at the two ends of a run holds
  throughout. This is precisely the shape `Exp.alwaysGE_sound` produces,
  so the symbolic layer now plugs into the run layer.
* `shiftN` + the five coordinate lemmas — the Int/Nat bridge, with
  nonnegativity supplied exactly where the guards give it.
0 sorries, core axioms. Note `coord_lt_of_endpoints` is deliberately
about a SINGLE coordinate, never a disjunction — see
`Decider.disjunctive_endpoint_check_unsound` for why that is not a
stylistic choice.

Current line split: **generic layers 865 lines (5 files) vs per-machine
2,884 lines (7 files, 9 machines)**.

**Still remaining for a fully verified decider:**
certificates as DATA with coefficients in {a + b*n + c*2^n}, an
executable `checkCert : Machine -> Cert -> Bool`, and
`checkCert M c = true -> NeverHalts M start`. Then each machine is
`cert_sound M <cert> (by decide)` -- about 20 lines, no mathematics.
Known obstacles, recorded so the next session does not rediscover them:
(i) EXP needs rational coefficients (e.g. (2*2^n-2)/3 occurs in 431), so
without mathlib one must build Q as Int pairs, or carry a denominator and
verify integrality along the progression -- decidable, since both n mod d
and 2^n mod d are eventually periodic, but it is real work;
(ii) **the stage-composition fold** — chaining a LIST of stages while
threading the symbolic state and keeping it equal to the real machine
state. The per-stage machinery is now done; this is the remaining
structural induction, and it is the genuinely hard part because each
stage's state function depends on the previous stages' outputs;
(iii) block stages (structurally similar to runs, via `steps_blocks`);
(iv) the `Cert` datatype and the executable `checkCert : Machine -> Cert
-> Bool` with `checkCert M c = true -> NeverHalts M start`, after which a
machine is ~20 lines of `by decide`.

**PAPER (`paper/main.tex`, 7 pp, compiles clean, 0 unresolved refs).**
"Rigid phase certificates: deciding nine FRACTRAN holdouts, and a
decider that explains why". Every number in it was recomputed from the
lists/logs before writing (audit: all present in the rendered PDF).

Each proof: boundary family + one-phase lemma (exact guarded firing word,
parity case splits) + entry lemma + induction; verified per machine against
its OWN rules and priority order (V0 big-int ground truth 200k steps, V1
halt-criterion box, V2 entry, V3 block walk to idx 2000 with corner
soundness via joint affinity, V4 word-for-word ground truth). No Baker, no
p-adics anywhere. NOTE the family-grouping correction: 574/570/680 are NOT
mere transports — priority swaps change the firing word; each has its own
genuinely different template (574 pair-mode; 570/680 phase-rotated with
their own parity splits). Next (gated on Tom): Lean formalization +
upstream submission to int-y1/BBFractran.

**The original note on 431 (Aug 1), kept for history:** machine 431 was
first — Theorem M431,
`m431_proof.py`: never halts from n = 2.** Complete hand proof (halt
criterion, entry, one-phase template with the i-parity case split,
induction; the fuel v11 = i grows linearly) with every proof step
machine-verified: block walk i = 1..2000 with all guard/priority checks at
block-rectangle corners (sound because every guard value is jointly affine
in the block and run counters), word-for-word ground-truth agreement
through phase 13 (step 130,994), halt-criterion lemma exhaustive on the
0..5 box. Identity: line 432 of the refined 694 list, line 13,649 of the
official sz23_21233 list. The reorder/relabel siblings (673; 502, 623)
inherit the theorem once their equivalences are verified — next.

**455 and 678: candidates, NOT decisions.** Remaining obligation per machine: a
one-phase symbolic template proof (finite case split on affine guard
inequalities) + induction; for 678, invariant-preservation induction
(`(v5,v11) -> (2·v5, 2·v11+1)` preserves `v5 = 2(v11+1)`). Margins are
LINEAR in i (431/455) or exactly-preserved (678) — no LTE range, no Baker
tail needed, unlike the April BW machine.

**Negative finding worth keeping:** among all 9 surviving GEO machines in
the refined list, none has a thin (Baker-type) margin. True BW siblings, if
any, live in the BB(6) TM list and need per-machine tape reductions.

Also from the sweep's BB(6) classification: Lucy's Moonlight and the mxdys
3-tuple probviously-halting holdout are *branch-affine* (base 3 / parity) —
interface-adjacent, potential future case files.
