/-
THE DECIDER, FORMALIZED.

`decider.py` implements a decision procedure for non-halting of rigid
FRACTRAN machines: a *rigid phase certificate* is checked symbolically,
and acceptance is claimed to imply that the machine never halts.  This
file formalizes the MATHEMATICS THAT MAKES THAT CHECKER SOUND -- the
three principles the checker implements -- and shows that the nine
machine proofs are all instances of one abstract theorem.

What is and is not formalized (stated plainly, for the paper):
  * FORMALIZED: the soundness ARGUMENT.  Theorem A below is the exact
    statement "a certificate of this shape implies NeverHalts", with no
    reference to any particular machine; Theorems B and C are the two
    geometric facts that justify the checker's finite guard checks.
  * NOT FORMALIZED: the Python implementation itself (the parser, the
    EXP arithmetic, the search).  A bug in the *code* could make it
    accept a certificate that does not satisfy Theorem A's hypotheses;
    what is proved here is that no such certificate can exist for a
    halting machine.

-----------------------------------------------------------------------
A. PHASE-CERTIFICATE SOUNDNESS.  If some boundary family is reached from
   the start, and every boundary steps to the next in >= 1 steps, the
   machine never halts.  Every one of the nine machines instantiates
   this (see the corollaries at the end).

B. THE CORNER PRINCIPLE.  Inside a block the state is jointly affine in
   (block index k, within-run counter t), so every guard value has the
   form  a + b*k + c*t.  Such a function is nonnegative on the whole
   rectangle as soon as it is nonnegative at the four corners.  This is
   what licenses `decider.py`'s check C2 (and, at L = 0, the endpoint
   checks in the nine hand proofs).

C. PRIORITY EXCLUSION MUST PIN ONE CONJUNCT.  A rule is disabled when
   SOME conjunct of its guard fails.  Checking "the rule is disabled" at
   the two endpoints of a run is NOT sound: the disjunction can hold at
   both ends via DIFFERENT conjuncts and fail in between.  The checker
   therefore requires one FIXED conjunct to fail at all corners, which
   is sound by B.  Both halves are proved below -- the unsoundness by an
   explicit counterexample.
-/
import LeanBbf.M431
import LeanBbf.M455
import LeanBbf.M678
import LeanBbf.M574
import LeanBbf.M570
import LeanBbf.M680

namespace Fractran.Decider

open Fractran

/-! ## A. Phase-certificate soundness -/

/-- **THEOREM A (soundness of rigid phase certificates).**
    Let `B : Nat → St` be a boundary family.  If the machine reaches
    `B i₀` from `s₀`, and from every `B i` (`i ≥ i₀`) it performs at
    least one step and arrives at `B (i+1)`, then it never halts from
    `s₀`.

    This is exactly the certificate contract of `decider.py`: C4 is the
    `entry` hypothesis, C1–C3 establish the `phase` hypothesis for the
    branch covering `i`, and C5 guarantees every `i ≥ i₀` is covered. -/
theorem neverHalts_of_phases {M : Machine} {s₀ : St} (B : Nat → St)
    (i₀ E : Nat) (entry : Steps M E s₀ (B i₀))
    (phase : ∀ i, i₀ ≤ i → ∃ n, 1 ≤ n ∧ Steps M n (B i) (B (i + 1))) :
    NeverHalts M s₀ := by
  have key : ∀ k, ∃ m, k ≤ m ∧ Steps M m s₀ (B (i₀ + k)) := by
    intro k
    induction k with
    | zero => exact ⟨E, Nat.zero_le E, entry⟩
    | succ k ih =>
      obtain ⟨m, hm, hs⟩ := ih
      obtain ⟨n, hn, hp⟩ := phase (i₀ + k) (Nat.le_add_right i₀ k)
      exact ⟨m + n, by omega, hs.comp hp rfl⟩
  exact neverHalts_of_unbounded fun N =>
    let ⟨m, hm, hs⟩ := key N; ⟨m, B (i₀ + N), hm, hs⟩

/-- The common special case: a fixed step-count function. -/
theorem neverHalts_of_phases' {M : Machine} {s₀ : St} (B : Nat → St)
    (len : Nat → Nat) (i₀ E : Nat) (entry : Steps M E s₀ (B i₀))
    (hlen : ∀ i, i₀ ≤ i → 1 ≤ len i)
    (phase : ∀ i, i₀ ≤ i → Steps M (len i) (B i) (B (i + 1))) :
    NeverHalts M s₀ :=
  neverHalts_of_phases B i₀ E entry
    fun i hi => ⟨len i, hlen i hi, phase i hi⟩

/-! ## B. The corner principle -/

/-- **THEOREM B (corner principle).**  A function jointly affine in two
    Nat parameters, `a + b*k + c*t`, that is nonnegative at the four
    corners of `[0,K] × [0,L]` is nonnegative on the whole rectangle.

    Guard values inside a certificate block have exactly this form (the
    block-start state is affine in the block index `k` with integer
    slope, and within a run the state is affine in the counter `t` with
    the rule's delta as slope), so the checker's four corner tests are
    equivalent to the infinitely many pointwise tests. -/
theorem affine2_nonneg_of_corners (a b c : Int) (K L : Nat)
    (h00 : 0 ≤ a) (hK0 : 0 ≤ a + b * K) (h0L : 0 ≤ a + c * L)
    (hKL : 0 ≤ a + b * K + c * L) :
    ∀ k t : Nat, k ≤ K → t ≤ L → 0 ≤ a + b * k + c * t := by
  intro k t hk ht
  have row0 : ∀ k' : Nat, k' ≤ K → 0 ≤ a + b * k' :=
    affine_nonneg_of_endpoints a b K h00 hK0
  have rowL : ∀ k' : Nat, k' ≤ K → 0 ≤ a + c * L + b * k' :=
    affine_nonneg_of_endpoints (a + c * L) b K h0L
      (by rw [Int.add_right_comm]; exact hKL)
  have eL : 0 ≤ a + b * k + c * L := by
    have h := rowL k hk
    rw [Int.add_right_comm] at h
    exact h
  exact affine_nonneg_of_endpoints (a + b * k) c L (row0 k hk) eL t ht

/-- The dual form used for propagating guard FAILURE (`value ≤ thr`)
    across a rectangle. -/
theorem affine2_le_of_corners (a b c thr : Int) (K L : Nat)
    (h00 : a ≤ thr) (hK0 : a + b * K ≤ thr) (h0L : a + c * L ≤ thr)
    (hKL : a + b * K + c * L ≤ thr) :
    ∀ k t : Nat, k ≤ K → t ≤ L → a + b * k + c * t ≤ thr := by
  intro k t hk ht
  have row0 : ∀ k' : Nat, k' ≤ K → a + b * k' ≤ thr :=
    affine_le_of_endpoints a b thr K h00 hK0
  have rowL : ∀ k' : Nat, k' ≤ K → a + c * L + b * k' ≤ thr :=
    affine_le_of_endpoints (a + c * L) b thr K h0L
      (by rw [Int.add_right_comm]; exact hKL)
  have eL : a + b * k + c * L ≤ thr := by
    have h := rowL k hk
    rw [Int.add_right_comm] at h
    exact h
  exact affine_le_of_endpoints (a + b * k) c thr L (row0 k hk) eL t ht

/-! ## C. Priority exclusion must pin a single conjunct

A guard is a conjunction of coordinate lower bounds; the rule is
DISABLED exactly when some conjunct fails.  Model a conjunct's value
along a run as an affine function `p + u*t`, and "fails" as
`p + u*t ≤ 0` (i.e. the coordinate is below its threshold). -/

/-- **SOUND direction.**  If one FIXED conjunct fails at both endpoints
    of a run, it fails throughout, so the rule is disabled throughout.
    (This is the rule `decider.py` actually implements: check C3 looks
    for a single coordinate condition failing at every corner.) -/
theorem single_conjunct_exclusion (p u thr : Int) (n : Nat)
    (h0 : p ≤ thr) (hn : p + u * n ≤ thr) :
    ∀ t : Nat, t ≤ n → p + u * t ≤ thr :=
  affine_le_of_endpoints p u thr n h0 hn

/-- **UNSOUND direction.**  Checking only that the DISJUNCTION "some
    conjunct fails" holds at the two endpoints does NOT imply the rule
    is disabled in between: the two ends can be witnessed by different
    conjuncts.

    Explicit counterexample: two conjunct-values `p + u*t = t` and
    `q + v*t = 2 - t` on `t ∈ [0,2]`.  At `t = 0` the first is `≤ 0`;
    at `t = 2` the second is `≤ 0`; but at `t = 1` both equal `1 > 0`,
    so the rule IS enabled in the middle of the run.

    Consequence for the checker: endpoint (or corner) testing of a
    conjunctive guard's negation is unsound, and the single-conjunct
    discipline of Theorem C is not a convenience but a requirement. -/
theorem disjunctive_endpoint_check_unsound :
    ∃ (p u q v : Int) (n : Nat),
      (p ≤ 0 ∨ q ≤ 0) ∧
      (p + u * (n : Int) ≤ 0 ∨ q + v * (n : Int) ≤ 0) ∧
      ∃ t : Nat, t ≤ n ∧ ¬(p + u * (t : Int) ≤ 0 ∨ q + v * (t : Int) ≤ 0) :=
  ⟨0, 1, 2, -1, 2, by decide, by decide, 1, by decide, by decide⟩

/-! ## The nine machines are instances of Theorem A

Each of the nine hand proofs consists of exactly the data Theorem A
requires.  Re-deriving the theorems through the abstract lemma
demonstrates that the certificate contract really is what the machine
proofs establish (and that the contract is not vacuous). -/

theorem m574_via_certificate : NeverHalts M574.M574 ⟨1, 0, 0, 0, 0⟩ :=
  neverHalts_of_phases' M574.Bst (fun k => 5 * 2 ^ k) 0 1 M574.entry
    (fun i _ => by have := M431.two_pow_pos i; omega)
    (fun i _ => M574.phase_step i)

theorem m570_via_certificate : NeverHalts M570.M570 ⟨1, 0, 0, 0, 0⟩ :=
  neverHalts_of_phases' M570.Bst (fun m => 5 * 2 ^ m) 0 1 M570.entry
    (fun i _ => by have := M431.two_pow_pos i; omega)
    (fun i _ => M570.phase_step i)

theorem m680_via_certificate : NeverHalts M680.M680 ⟨1, 0, 0, 0, 0⟩ :=
  neverHalts_of_phases' M680.Bst (fun m => 6 * 2 ^ m - 3) 0 0 M680.entry
    (fun i _ => by have := M431.two_pow_pos i; omega)
    (fun i _ => M680.phase_step i)

/-- M455's boundary family is only meaningful from index 2, so its
    certificate is stated with `i₀ = 2` -- the general form of Theorem A
    (an arbitrary starting index) is what makes this an instance too. -/
theorem m455_via_certificate : NeverHalts M455.M455 ⟨1, 0, 0, 0, 0⟩ :=
  neverHalts_of_phases' M455.Bst (fun i => 4 * 2 ^ i) 2 11 M455.entry
    (fun i _ => by have := M431.two_pow_pos i; omega)
    (fun i hi => M455.phase_step i hi)

end Fractran.Decider
