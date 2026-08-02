# Collatz-like machines and cryptids

A research program on small, fully explicit machines whose halting is —
or turns out not to be — an open Collatz-type problem. It contains
decided machines, formal proofs, decision procedures, case files on
undecided ones, and honest records of what did not work.

Every claim carries an epistemic label: **[proved]**, **[proved,
Lean-verified]**, **[machine-verified]** (checked exhaustively over a
stated finite domain), or **[measured]**. Heuristics say so.

---

## Headline results

### Nine FRACTRAN holdouts decided — [`bbf/`](bbf/)

Nine machines on the live `BBf(23)` Busy Beaver holdout list are proved
**never to halt** from their start value `n = 2`. All nine proofs are
formalized in **Lean 4 without mathlib**, are `sorry`-free, and depend
only on Lean's three core axioms.

* [`bbf/paper/main.tex`](bbf/paper/main.tex) — the write-up (7 pp).
* [`bbf/lean/`](bbf/lean/) — the formalization (9 files, ~3,300 lines;
  builds from scratch in a few seconds).
* [`bbf/decider.py`](bbf/decider.py) — a **decision procedure**: *rigid
  phase certificates* over the expression class `{a + bn + c·2^n}`,
  checked symbolically for all phase indices at once; plus a second
  decider for *equivalence* of certified machines.
* [`bbf/lean/LeanBbf/Decider.lean`](bbf/lean/LeanBbf/Decider.lean) — the
  decider's **soundness argument**, formalized: the certificate
  contract, the corner principle, and a machine-checked counterexample
  showing a natural cheaper check is unsound.

Reproduce: `cd bbf && python3 decider.py`; `cd bbf/lean && lake build`.

### The sheep machine — [`sheep/`](sheep/)

A `BB(6)` bbchallenge Cryptid. Its halting set is determined **completely
and in closed form**; no congruence certificate exists at any modulus;
and the last-step sieve provably **saturates** — at any depth it forbids
at most ~29.6% of branch words. The orbit question itself stays open,
which is the honest state of the art for this machine.

### Case files on open machines

[`needle/`](needle/) (the Space Needle's reduction), [`machine1/`](machine1/),
[`machine3/`](machine3/), [`machine4/`](machine4/), [`hydra/`](hydra/),
[`fenrir/`](fenrir/) — exact acceleration, halting criteria, no-cycle
proofs, measured evidence. None is decided; each records precisely what
would decide it.

### Theory

[`census/`](census/) — a 1,077-member family of Collatz-like maps with a
universal last-step sieve lemma, ten machine theorems, and a saturation
chain proving **no modulus separates** the flagship machines.
[`formal/`](formal/), [`automatic/`](automatic/), [`density/`](density/),
[`baker/`](baker/) — certificate-impossibility results, automatic-invariant
searches (negative, with bounds), density theorems, Baker escalation.
[`paper/`](paper/) — a longer paper on the census and saturation theorems.

### Where it stands

[`meta/`](meta/) — a living cross-machine report, and
[`meta/NEXT_STEPS.md`](meta/NEXT_STEPS.md) recording the current plan
*and* the negative program: what was tried, why it failed, what is
provably dead.

---

## What this program does *not* claim

* **No Turing machine's halting problem is decided here.** The nine
  decided objects are FRACTRAN programs; the census machines are
  arithmetic maps from a manufactured family; cryptid reductions are
  halting-equivalent by other people's published analyses, cited where
  used.
* The decided machines are the **rigid** ones — closed-form orbits. Most
  holdouts are not rigid, and these methods are empty for them by
  construction, not by budget.
* Verification is largely by our own implementations. Where an
  independent check exists (Lean; brute-force replay against raw rules;
  agreement with published community lemmas), it is stated.

## Provenance

Holdout lists are those published by the BBFractran project and the
bbchallenge collaboration; sources and dates are in
[`bbf/README.md`](bbf/README.md). Machine reductions taken from the
bbchallenge wiki are quoted verbatim beside the code that uses them.

This work was carried out with substantial AI assistance.

---

# Directory guide

Guarded rewriting systems whose halting questions reduce to open
Collatz-type orbit-avoidance problems ("cryptids"). Each machine directory is
self-contained: run any `.py` file from inside its directory to re-run its
self-verification. Start with `meta/collatz_meta_report.pdf` — the light-weight
layer across the collection: case files, the side-by-side comparison, the
patterns that generalize (P1–P7), and the standard workflow for the next
machine. `meta/make_meta_report.py` regenerates it; extend it when a new
machine is analyzed.

## machine1 — NextConfig(a, b, c, d), start (0, 0, 0, 0)

13 rules over four counters. Reduced through a 4-level exact acceleration to a
one-variable return map D → F(D); halting ⟺ the F-orbit of 17 meets an
infinite halting set H. Proved: halting criterion, mod-16 confinement
(F(D) ≡ 9 mod 16), expansion margin on the dominant word, no 2-adic
continuous extension. Verified: no halt in the first 10^150,514 base steps.
Status: open. Report: `collatz_acceleration_report.pdf`.

- `collatz.py` — the base 13-rule system
- `accel.py`, `accel2.py`, `accel3.py` — acceleration levels 2–3
- `onedim.py` — level 4, the map F
- `formal.py`, `criterion.py`, `orbit.py`, `afterstep25.py` — anchor map,
  halting criterion, deep runs, the after-step-25 system
- `mod16.py`, `gaps.py` — mod-16 confinement; expansion margin, 2-adic
  obstruction, mantissa disproof
- `traj.py` — whole-trajectory equivalence checks; `Archive.zip` — early snapshot

## machine3 — A(a, b), start (1, 1)

6 rules. A **multiplicative-coincidence** cryptid (Space Needle type): halts iff
the a-orbit hits an exact power of 3 with exponent ÷3, {27, 729, 19683, …}.
Divide-chains batched (Thm 2); potential Φ = a+b proves no cycles (Thm 3);
divide depth follows the 3-adic valuation law. No halt in 3M composite steps
(a past 700k bits). Status: open, divergent. Report: `machine3_halting_report.pdf`.
- `m3_base.py`, `m3_accel.py` (batched divides, self-verified), `m3_theorems.py`

## machine4 — A(a, b), start (1, 1)

10 rules. A **sparse-coincidence** cryptid: halts iff b = a+3 (a odd). a stays
odd forever (Thm 1); the dominant rule cascades in closed form (Thm 3); no affine
potential is monotone, but a+b is a **potential with recovery** (dips ≤1,
recovers +4) proving no cycles (Thm 4) — a new technique. Linear growth,
closest approach to halt line = 1, no halt in 3M steps. Status: open, convergent.
Report: `machine4_halting_report.pdf`.
- `m4_base.py`, `m4_theorems.py`

## hydra — the catalogued relatives (program step 1)

Hydra (BB(2,5)), Antihydra (BB(6)), Fenrir (FRACTRAN-22) — all iterate
H(n)=floor(3n/2) (Fenrir in base 5), walk-absorption type. Verified against
every wiki trajectory; q-adic branch-memory theorem (no congruence invariant
of the value can decide halting); exact golden-ratio absorption model; Geom(1/2)
branch statistic. Status: open (as on bbchallenge). Report: `hydra_report.pdf`.
- `hydra.py` (implementations + wiki fidelity), `theorems.py`

## needle — the Space Needle cryptid (analyzed, not integrated into meta yet)

The BB(6) cryptid (mxdys, Jan 2025) that machine 3 was built to mirror.
Doucette one-variable form from b=6, halts iff b hits an exact power of 2 —
the multiplicative archetype. Reproduces the wiki sequence exactly; b is its
own potential (no cycles); 2-adic valuation branch statistic; measured growth
0.6515 vs wiki 0.652355. Divergent, probviously non-halting.
Report: `needle_report.pdf`.
- `needle.py` (one-var + low-level forms, wiki fidelity), `theorems.py`

## formal — Collatz-equivalence and a hardness ordering (theory)

A formal treatment of "are our machines equivalent to / as hard as Collatz?"
Answers: (i) none IS the 3n+1 map; (ii) all are generalized Collatz functions
(Conway / Kurtz-Simon class, Pi-0-2-complete as a class) — the formal meaning of
"Collatz-like"; (iii) each machine's non-halting is a Pi-0-1 SINGLE-ORBIT
statement, one quantifier BELOW the Pi-0-2 Collatz conjecture — so "as hard as
Collatz" is about the shared pseudorandom-orbit obstruction, not logical level.
Ranking (novel — none in the literature): equal at the core; a partial order on
the shell — multiplicative machines {3, Space Needle} are CERTIFIED beyond
congruences (Finding 3), the sparse ones only empirically; Hydra/Antihydra and
machine 1 sit closest to a named open problem (Mahler's 3/2, by analogy).
Report: `collatz_equivalence_report.pdf`.
- `classify.py` (branch-type + class membership + arithmetical level),
  `ranking.py` (the partial order), `make_formal_report.py`
