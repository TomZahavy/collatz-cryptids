# Paper outline — "Rigid phase certificates: deciding nine FRACTRAN holdouts"

Working title options:
- *Rigid phase certificates for FRACTRAN non-halting, with nine decided
  BBf(23) holdouts*
- *From hand proofs to a decider: certifying non-halting of rigid FRACTRAN
  machines*

Target: short paper (8–12 pp), venue candidates: arXiv (math.LO/cs.LO) +
bbchallenge community; possibly a workshop (termination / verification).

## Structure

1. **Introduction.** The BBf competition; the March 2026 mass decision and
   its residue; cryptids vs rigid machines; the April 2026 Baker–Wüstholz
   precedent (rigid orbit + thin margin). Contribution list: (i) nine
   holdouts decided; (ii) the certificate class + sound checker (the
   decider); (iii) symbolic ∀-index verification; (iv) template
   isomorphism as an equivalence decider; (v) Lean formalization (status);
   (vi) the toolkit-development narrative (discovery→balance→template→
   corner verification), including the corrected family structure.

2. **Preliminaries.** FRACTRAN with first-match priority as guarded
   vector-addition rules over prime-exponent vectors; halt criterion
   normalization (Lemma-0 style).

3. **The certificate class.** EXP = {a + bn + c·2^n}; boundary families;
   run and block stages; parity branches. THE SOUNDNESS THEOREM (checker
   accepts ⇒ never halts), with the three load-bearing lemmas: affine run
   lemma (endpoint checking), corner lemma (joint affinity on the block
   rectangle), single-condition priority exclusion (why conjunction-level
   endpoint failure would be unsound — a subtlety worth a remark).
   Decidability of eventual-positivity in EXP ⇒ certificate checking is a
   finite, exact procedure (no simulation beyond the entry).

4. **The nine machines.** Table of fractions, boundaries, phase words,
   step counts, margins (linear fuel 431/455-style vs preserved invariant
   678-style). One worked example in full (431). The parity phenomena.
   Discovery methodology: exact acceleration → phase segmentation →
   firing balance (the linear system that pins all run counts) → template
   → corner verification. Family-structure correction: priority
   reorderings change the word (574/570/680 have their own templates) —
   established formally by the template-isomorphism decider: classes
   {431, 502, 623, 673}, {455}, {570}, {574}, {678}, {680}.

5. **The equivalence decider.** Template isomorphism (rule bijection +
   axis permutation, exact certificate match); decidable by finite
   search; implies exact orbit correspondence from the entry boundaries.
   Open refinement: cyclic phase rotation + affine conjugacy (570 vs 455,
   680 vs 678 look rotated but are not permutation-conjugate).

6. **Lean formalization.** Status per machine; the general affine-run
   lemma as the reusable core; relation to busycoq/Lean community
   practice.

7. **Scope and limits.** What rigid certificates cannot do: the 675
   NONRIGID holdouts (digit-consuming, cryptid-shaped); why the class
   boundary is exactly rigidity; relation to our Theorem R; the BW
   machine's thin margin sits outside EXP-certificates (needs the
   Baker tail) — the two decidable genres are disjoint.

8. **Data availability.** Code, certificates, logs; holdout-list
   provenance (int-y1/BBFractran; mxdys BB(6) list).

## Numbers audit obligations (fill before writing)
- 694 refined / 21,233 official counts + dates + URLs.
- 9 = 4 + 1 + 1 + 1 + 1 + 1 class decomposition.
- Verification domains per machine (idx sweeps now superseded by symbolic
  ∀; entry steps; word-for-word ranges).
- Falsifier: 540 corrupted certificates, 0 accepted.

## Style/discipline
- Epistemic labels as in the census paper; [proved] vs [machine-verified].
- The AI-assisted workflow acknowledgment (attribution per Tom's call —
  same decision as the sheep wiki page and upstream submissions).
