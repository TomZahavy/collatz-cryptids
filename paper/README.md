# The census paper — working draft

`main.tex` + `refs.bib`. Drafted July 30, 2026 from the project's verified
results.

## Status

**Draft, compiled — `main.pdf`, 20 pages** (v3, July 31 evening; Tectonic
0.17.0; audit: all expected strings present, zero unresolved references —
`??` count 0 in the rendered text). The source also passed the structural
lint: environment balance, brace balance, `$` parity, zero dangling
`\ref`/`\eqref`, zero missing `\cite` keys.

> Note on the audit script: `scripts/audit_pdf.py --require-crossrefs` reports
> several "dangling" section references on this PDF. That is a false alarm —
> its heading detector is tuned to reportlab output and does not parse LaTeX
> headings; every referenced section exists in the PDF's own table of
> contents. The authoritative check for LaTeX is the `??` count.

Two build notes:
- **Tectonic 0.17's BibTeX hangs on `refs.bib`** (infinite loop after
  fetching `alpha.bst`; killed at 60 CPU-minutes). Workaround: the
  bibliography is **inlined** as a `thebibliography` block in `main.tex`,
  mirroring `refs.bib`. On Overleaf/TeX Live, either keep the inline block
  or restore `\bibliographystyle{alpha}\bibliography{refs}` and check
  whether real BibTeX handles it (it should; suspect a Tectonic bug).
- `xcolor` must be loaded explicitly for the link colors (already fixed in
  the source).

## Numbers audit

Every numerical claim in the draft was checked against the logs of record
(28 checks, all passing — see the session transcript of July 30):

| claim | log |
|---|---|
| 1,077 analysed; 318 decided; audit 0 failures | `census/census.log`, `verify.log` |
| deciding moduli incl. 7 (3) | `census/saturation.log` |
| universal lemma: 672 machines, 51,030 branches | `census/universal.log` |
| completeness 10 + 620 + 42; Needle mass 0.2868; 19/35; 18-of-41 survive | `census/universal.log` |
| descent: 708 excluded-region cases, chain ≤ 7 | `census/descent.log` |
| reach: 4,000 witnesses, deepest 9; T15 7,616 pairs; falsifier 40/40 | `census/reach.log` |
| T14: 7,840 pairs; falsifier 267 + 7 | `census/even_saturation.log` |
| machine M3: table 59,988; 747 closures; seeds 15/21/478293; 77/81 | `machine3/m3_nocert.log` |
| rigidity: 2,351/19,092 = 12.31%; β=0 supplies 758; bandwidth ≥ M | `formal/ws4/rigidity.log` |
| sheep: 15,920+200,000 identity checks; survivors {0,1} to v<260; H matched below 3e5; closure = Z_M for M ≤ 200 | `sheep/sheep.log` |
| T16: 1,705 tuples saturate, 437/671 falsifier; M1-D 1,988 points, n ≤ 21; M1-N1 odd M ≤ 401 + 25 random | `machine1/m1_congruence.log` |

## Before submission (TODO)

1. **Compile** and eyeball; fix any layout issues.
2. **References**: entries marked STANDARD vs CHECKED in `refs.bib`;
   confirm every entry bibliographically (esp. `dhiman-pandey` author
   names; Bertók–Hajdu journal data; Kaščák pages). Add the repository URL
   (two placeholders in the text).
3. **Authorship/acknowledgments**: the `\thanks` note and the
   Acknowledgments section are placeholders for how to credit the
   AI-assisted workflow.
4. **C6/C8 proofs**: the paper points to the repository for the finite case
   analyses; consider an appendix instead.
5. Consider adding the WS1/WS2 material (automatic-invariant UNSAT bounds,
   depth-graded density) as sections rather than one-paragraph summaries —
   currently they are context, not contributions, to keep the paper one
   coherent arc.
6. **Lean formalization** of Lemma 3.1 (universal sieve), the descent and
   reach lemmas would upgrade the verification story; ranked next in the
   program plan.

## What v3 added (July 31, evening)

A new **Section 7, "Two tests outside the design set"** — the corrective for
the paper's own threat-to-validity item that the whole theory was developed
against one machine:

* **7.1 the sheep machine** (`1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE`,
  BB(6), found by *sheep* 7 Apr 2026, a listed bbchallenge Cryptid) — its
  generic branch **is census member (1,1,1,1,0)**, the Needle's (1,3,1,1,0)
  with β = 3 → 1. Prop. 7.1 (identification), Thm 7.2 (**the sieve closes:
  only v ∈ {0,1} survive**, recovering and sharpening the wiki's
  `even_case_no_pow2`), Cor. 7.3 (**the halting set in closed form**, three
  geometric families), Rem. 7.4 (**the rank dichotomy tested** on a machine
  we did not construct, prediction on record first).
* **7.2 Lemma 7.5** — linear-exponential saturation, the descent with the
  VAL(2) schema and the multiplier hypothesis both removed — and **Thm 7.6**,
  no odd modulus certifies machine M1.

Plus: ledger rows for all six new results; a seventh threats-to-validity item
(the design-set concern, now *partly* mitigated — two instances is not
generality); revised G1/G2/G4 rows in the progress table; "G4 demonstrated
three times"; and one clause added to "what did not move" (the sheep's
arithmetic closes and its orbit question does not).

Supporting material: `../sheep/RESULTS.md`, `../machine1/RESULTS.md`,
`../machine4/RESULTS.md`, and the logs `sheep/sheep.log`,
`machine1/m1_congruence.log`, `machine4/m4_mod16.log`,
`machine4/m4_heuristic.log`.

## Structure (v2, July 31)

Restructured so the goals come first and the honesty is structural, not
prose-deep:

1. **§1 Introduction** — §1.1 the three kinds of object (Turing machines vs
   Collatz-like functions vs counter systems) and how they relate; §1.2 the
   four research goals G1–G4; §1.3 progress summary table; **§1.4 what this
   paper does not claim** (6 numbered items); §1.5 epistemic conventions.
2. **§2–§7** the mathematics, each result carrying an explicit label
   `[proved]` / `[proved, computer-assisted]` / `[machine-verified]` /
   `[measured]` / `[interpretation]` plus an **Evidence** note stating the
   exact domain computed over.
3. **§8 Status ledger** — every result in one table with its label, plus
   **§8.2 threats to validity** (6 items, incl. "all verification is by our
   own implementations", the M3 branch-table dependency, and the
   search-evidence asymmetry).
4. **§9 Progress against the goals, revisited** — per goal, ending with
   "what did not move".
5. **§10 Discussion + open problems.**

### Corrections made in v2

- **The Space Needle is a Turing machine**, not a member of our family. What
  is a member (at `(1,3,1,1,0)`) is its published halting-equivalent
  one-variable reduction (Doucette). v1 conflated these; now
  Proposition 2.2 states and proves the identification, and §1.1 keeps the
  distinction throughout.
- **"No Turing machine's halting problem is decided here"** is now stated in
  the abstract, §1.1, §1.4 and §9 — the 328 decided objects are arithmetic
  maps from a manufactured box.
- Results previously presented uniformly as theorems are now separated into
  hand proofs vs exhaustive finite computations (e.g. C6/C8 are
  `[proved, computer-assisted]`, not `[proved]`).
- **M3's branch table is labelled `[machine-verified]`**, not proved — the
  induction is routine but unwritten — and the two theorems depending on it
  say so.
- **Theorem 6.4 (M3 two-step pinning) is flagged as the least independently
  corroborated result in the paper.**

## What the paper is

One arc: family → census with exact decision → sieve lemma → ten machine
theorems + completeness → saturation chain (T12, T14, descent, reach) →
**T15: no modulus separates the Space Needle** → base-3 transfer (M3-N1,
M3-N2) → the rank-of-sieve-group dichotomy → barriers (rigidity,
single-point principle) → the address of the remaining difficulty
(S-unit membership, one step beyond the linear-exponential frontier).
