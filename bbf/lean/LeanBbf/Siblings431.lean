/-
The three 431-transport siblings of BBf(23): machines 673, 502, 623.

    673 = [9/35, 5/6, 8/55, 7/2, 605/7]    (431 with f0,f1 swapped)
    502 = [7/15, 9/14, 125/77, 2/5, 847/2] (431 under primes 2->5->7->2)
    623 = [9/10, 5/21, 343/55, 2/7, 605/2] (431 under 2<->7, f0,f1 swapped)

THEOREMS: m673_never_halts, m502_never_halts, m623_never_halts — each
program, started at n = 2 = (1,0,0,0,0), never halts.

METHOD (transport, the Lean counterpart of m_siblings_proofs.py).
Abstract states live on 431's axes; an embedding φ : St → St maps them to
each sibling's axes.  `FireSpec M φ` bundles the SIX φ-transported firing
facts that machine 431's phase analysis consumes — one per single-rule
run/firing shape, with the guard and every higher-priority guard of the
sibling's OWN rule list discharged at that shape.  The whole phase
development (runs, blocks, phase lemma with its parity split, boundary
induction, never-halting) is then proved ONCE, generically in (M, φ),
and instantiated three times.

The crucial shape restriction: `fire0` is only demanded at states with
v7 = 0 (machine 431 only ever fires f0 when v7 = 0).  This is exactly
why the f0/f1 priority swap in 673 and 623 does not change the firing
word: at every f0-moment of the word, f1 (their higher-priority rule) is
disabled by v7 = 0.  Machines with genuinely reordered words (574, 680)
do NOT satisfy this spec — their proofs need their own phase analysis.
-/
import LeanBbf.M431

/- The state-cast tactic `simp only [St.mk.injEq, ...] <;> omega` is used
   mechanically; on some goals simp already closes everything and the
   listed lemmas go unused, which is fine. -/
set_option linter.unusedSimpArgs false

namespace Fractran.Siblings431

open Fractran Fractran.M431

/-! ## The firing specification (the per-machine proof obligations) -/

/-- The six firing facts of the 431 template, transported along the axis
    embedding `φ`.  States are written in 431's role coordinates
    (a, b, c, d, e) = (v2, v3, v5, v7, v11)-roles; `φ` places them on the
    sibling's axes.  Each field asserts: at every state of that shape the
    sibling machine fires the corresponding rule — i.e. that rule's guard
    holds and every HIGHER-priority guard of the sibling fails there. -/
structure FireSpec (M : Machine) (φ : St → St) : Prop where
  fire0 : ∀ a b c e : Nat,
    step M (φ ⟨a + 1, b + 1, c, 0, e⟩) = some (φ ⟨a, b, c + 1, 0, e⟩)
  fire1 : ∀ b c d e : Nat,
    step M (φ ⟨0, b, c + 1, d + 1, e⟩) = some (φ ⟨0, b + 2, c, d, e⟩)
  fire2a : ∀ b c e : Nat,
    step M (φ ⟨0, b, c + 1, 0, e + 1⟩) = some (φ ⟨3, b, c, 0, e⟩)
  fire2b : ∀ a c e : Nat,
    step M (φ ⟨a, 0, c + 1, 0, e + 1⟩) = some (φ ⟨a + 3, 0, c, 0, e⟩)
  fire3 : ∀ a d e : Nat,
    step M (φ ⟨a + 1, 0, 0, d, e⟩) = some (φ ⟨a, 0, 0, d + 1, e⟩)
  fire4 : ∀ b d e : Nat,
    step M (φ ⟨0, b, 0, d + 1, e⟩) = some (φ ⟨0, b, 1, d, e + 2⟩)

namespace FireSpec

variable {M : Machine} {φ : St → St}

/-! ## The generic phase development (431's proof, once and for all) -/

theorem run_f3 (hs : FireSpec M φ) (k x d e : Nat) :
    Steps M k (φ ⟨x + k, 0, 0, d, e⟩) (φ ⟨x, 0, 0, d + k, e⟩) := by
  induction k generalizing d with
  | zero => exact steps_zero M _
  | succ k ih =>
    exact ((steps_one M (hs.fire3 (x + k) d e)).comp (ih (d + 1))
      rfl).cast (by omega) rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))

/-- f0-runs, only at v7 = 0 (all the template ever needs). -/
theorem run_f0 (hs : FireSpec M φ) (k x y c e : Nat) :
    Steps M k (φ ⟨x + k, y + k, c, 0, e⟩) (φ ⟨x, y, c + k, 0, e⟩) := by
  induction k generalizing c with
  | zero => exact steps_zero M _
  | succ k ih =>
    exact ((steps_one M (hs.fire0 (x + k) (y + k) c e)).comp (ih (c + 1))
      rfl).cast (by omega) rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))

theorem run_f2 (hs : FireSpec M φ) (k a x y : Nat) :
    Steps M k (φ ⟨a, 0, x + k, 0, y + k⟩) (φ ⟨a + 3 * k, 0, x, 0, y⟩) := by
  induction k generalizing a with
  | zero => exact steps_zero M _
  | succ k ih =>
    exact ((steps_one M (hs.fire2b a (x + k) (y + k))).comp (ih (a + 3))
      rfl).cast (by omega) rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))

theorem stage2 (hs : FireSpec M φ) (n : Nat) : ∀ b e : Nat, ∀ d : Nat,
    Steps M (n * 2) (φ ⟨0, b, 0, d + 2 * n, e⟩)
      (φ ⟨0, b + 2 * n, 0, d, e + 2 * n⟩) := by
  induction n with
  | zero => intro b e d; exact steps_zero M _
  | succ n ih =>
    intro b e d
    exact ((steps_one M (hs.fire4 b (d + 2 * n + 1) e)).comp
      ((steps_one M (hs.fire1 b 0 (d + 2 * n) (e + 2))).comp
        (ih (b + 2) (e + 2) d) rfl)
      rfl).cast (by omega)
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))

theorem stage4 (hs : FireSpec M φ) (n : Nat) : ∀ y e : Nat, ∀ c : Nat,
    Steps M (n * 4) (φ ⟨3, y + 3 * n, c, 0, e + n⟩)
      (φ ⟨3, y, c + 2 * n, 0, e⟩) := by
  induction n with
  | zero => intro y e c; exact steps_zero M _
  | succ n ih =>
    intro y e c
    exact ((hs.run_f0 3 0 (y + 3 * n) c (e + (n + 1))).comp
      ((steps_one M (hs.fire2a (y + 3 * n) (c + 2) (e + n))).comp
        (ih y e (c + 2)) rfl)
      rfl).cast (by omega)
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))

theorem phase_even (hs : FireSpec M φ) (i m q : Nat) (hq : 2 * m = 3 * q) :
    Steps M (8 * m + 3) (φ ⟨2 * m + 1, 0, 0, 0, i⟩)
      (φ ⟨4 * m + 3, 0, 0, 0, i + 1⟩) := by
  have s1 : Steps M (2 * m + 1) (φ ⟨2 * m + 1, 0, 0, 0, i⟩)
      (φ ⟨0, 0, 0, 2 * m + 1, i⟩) :=
    (hs.run_f3 (2 * m + 1) 0 0 i).cast rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
  have s2 : Steps M (m * 2) (φ ⟨0, 0, 0, 2 * m + 1, i⟩)
      (φ ⟨0, 2 * m, 0, 1, i + 2 * m⟩) :=
    (hs.stage2 m 0 i 1).cast rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
  have s3 : Steps M 1 (φ ⟨0, 2 * m, 0, 1, i + 2 * m⟩)
      (φ ⟨0, 2 * m, 1, 0, i + 2 * m + 2⟩) :=
    (steps_one M (hs.fire4 (2 * m) 0 (i + 2 * m))).cast rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
  have s4 : Steps M 1 (φ ⟨0, 2 * m, 1, 0, i + 2 * m + 2⟩)
      (φ ⟨3, 2 * m, 0, 0, i + 2 * m + 1⟩) :=
    (steps_one M (hs.fire2a (2 * m) 0 (i + 2 * m + 1))).cast rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
  have s5 : Steps M (q * 4) (φ ⟨3, 2 * m, 0, 0, i + 2 * m + 1⟩)
      (φ ⟨3, 0, 2 * q, 0, i + 2 * q + 1⟩) :=
    (hs.stage4 q 0 (i + 2 * q + 1) 0).cast rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
  have s6 : Steps M (2 * q) (φ ⟨3, 0, 2 * q, 0, i + 2 * q + 1⟩)
      (φ ⟨3 + 6 * q, 0, 0, 0, i + 1⟩) :=
    (hs.run_f2 (2 * q) 3 0 (i + 1)).cast rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
  exact (s1.comp (s2.comp (s3.comp (s4.comp (s5.comp s6 rfl) rfl) rfl) rfl)
    (by omega)).cast rfl rfl
    (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))

theorem phase_odd (hs : FireSpec M φ) (i m q : Nat) (hq : 2 * m = 3 * q + 2) :
    Steps M (8 * m + 3) (φ ⟨2 * m + 1, 0, 0, 0, i⟩)
      (φ ⟨4 * m + 3, 0, 0, 0, i + 1⟩) := by
  have s1 : Steps M (2 * m + 1) (φ ⟨2 * m + 1, 0, 0, 0, i⟩)
      (φ ⟨0, 0, 0, 2 * m + 1, i⟩) :=
    (hs.run_f3 (2 * m + 1) 0 0 i).cast rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
  have s2 : Steps M (m * 2) (φ ⟨0, 0, 0, 2 * m + 1, i⟩)
      (φ ⟨0, 2 * m, 0, 1, i + 2 * m⟩) :=
    (hs.stage2 m 0 i 1).cast rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
  have s3 : Steps M 1 (φ ⟨0, 2 * m, 0, 1, i + 2 * m⟩)
      (φ ⟨0, 2 * m, 1, 0, i + 2 * m + 2⟩) :=
    (steps_one M (hs.fire4 (2 * m) 0 (i + 2 * m))).cast rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
  have s4 : Steps M 1 (φ ⟨0, 2 * m, 1, 0, i + 2 * m + 2⟩)
      (φ ⟨3, 2 * m, 0, 0, i + 2 * m + 1⟩) :=
    (steps_one M (hs.fire2a (2 * m) 0 (i + 2 * m + 1))).cast rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
  have s5 : Steps M (q * 4) (φ ⟨3, 2 * m, 0, 0, i + 2 * m + 1⟩)
      (φ ⟨3, 2, 2 * q, 0, i + 2 * q + 3⟩) :=
    (hs.stage4 q 2 (i + 2 * q + 3) 0).cast rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
  have s6 : Steps M 2 (φ ⟨3, 2, 2 * q, 0, i + 2 * q + 3⟩)
      (φ ⟨1, 0, 2 * q + 2, 0, i + 2 * q + 3⟩) :=
    (hs.run_f0 2 1 0 (2 * q) (i + 2 * q + 3)).cast rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
  have s7 : Steps M (2 * q + 2) (φ ⟨1, 0, 2 * q + 2, 0, i + 2 * q + 3⟩)
      (φ ⟨1 + 3 * (2 * q + 2), 0, 0, 0, i + 1⟩) :=
    (hs.run_f2 (2 * q + 2) 1 0 (i + 1)).cast rfl
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))
  exact (s1.comp (s2.comp (s3.comp (s4.comp (s5.comp (s6.comp s7 rfl) rfl)
    rfl) rfl) rfl) (by omega)).cast rfl rfl
    (congrArg φ (by simp only [St.mk.injEq, and_true, true_and] <;> omega))

/-- The transported phase lemma at the (φ-image of the) boundary family. -/
theorem phase_step (hs : FireSpec M φ) (i : Nat) :
    Steps M (8 * 2 ^ i - 5) (φ (Bst i)) (φ (Bst (i + 1))) := by
  have hp := two_pow_pos i
  have h1 : 2 ^ (i + 1) = 2 ^ i * 2 := Nat.pow_succ 2 i
  have h2 : 2 ^ (i + 2) = 2 ^ i * 2 * 2 := by
    rw [Nat.pow_succ, Nat.pow_succ]
  rcases Nat.mod_two_eq_zero_or_one i with hpar | hpar
  · obtain ⟨t, ht⟩ : ∃ t, i = 2 * t := ⟨i / 2, by omega⟩
    obtain ⟨c, hc⟩ := two_pow_mod3 t
    have hm : 2 * (2 ^ i - 1) = 3 * (2 * c) := by rw [ht, hc]; omega
    exact (hs.phase_even i (2 ^ i - 1) (2 * c) hm).cast (by omega)
      (congrArg φ (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega))
  · obtain ⟨t, ht⟩ : ∃ t, i = 2 * t + 1 := ⟨i / 2, by omega⟩
    obtain ⟨c, hc⟩ := two_pow_mod3 t
    have hps : 2 ^ (2 * t + 1) = 2 ^ (2 * t) * 2 := Nat.pow_succ 2 (2 * t)
    have hm : 2 * (2 ^ i - 1) = 3 * (4 * c) + 2 := by rw [ht, hps, hc]; omega
    exact (hs.phase_odd i (2 ^ i - 1) (4 * c) hm).cast (by omega)
      (congrArg φ (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega))
      (congrArg φ (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega))

/-! ## Entry + induction ⇒ never halts, generically -/

/-- Steps from the start: `E` entry steps to (the φ-image of) B_1, then
    the phases.  `T E i` = total steps to B_{i+1}. -/
def T (E : Nat) : Nat → Nat
  | 0 => E
  | i + 1 => T E i + (8 * 2 ^ (i + 1) - 5)

theorem reach (hs : FireSpec M φ) {s0 : St} {E : Nat}
    (hE : Steps M E s0 (φ (Bst 1))) :
    ∀ i, Steps M (T E i) s0 (φ (Bst (i + 1)))
  | 0 => hE
  | i + 1 => (reach hs hE i).comp (hs.phase_step (i + 1)) rfl

theorem T_ge (E : Nat) : ∀ i, i ≤ T E i := by
  intro i
  induction i with
  | zero => exact Nat.zero_le E
  | succ i ih =>
    have hp := two_pow_pos (i + 1)
    show i + 1 ≤ T E i + (8 * 2 ^ (i + 1) - 5)
    omega

/-- A machine satisfying the 431 firing spec never halts from any state
    that reaches the (φ-image of the) first boundary. -/
theorem neverHalts (hs : FireSpec M φ) {s0 : St} {E : Nat}
    (hE : Steps M E s0 (φ (Bst 1))) : NeverHalts M s0 :=
  neverHalts_of_unbounded fun n =>
    ⟨T E n, φ (Bst (n + 1)), T_ge E n, hs.reach hE n⟩

end FireSpec

/-! ## Machine 673 = [9/35, 5/6, 8/55, 7/2, 605/7]

431 with the priority of its first two rules swapped; identical axes
(φ = id).  Entry: 3 steps to B_1. -/

def g673_0 : Rule := ⟨fun s => decide (1 ≤ s.c ∧ 1 ≤ s.d),
                      fun s => ⟨s.a, s.b + 2, s.c - 1, s.d - 1, s.e⟩⟩
def g673_1 : Rule := ⟨fun s => decide (1 ≤ s.a ∧ 1 ≤ s.b),
                      fun s => ⟨s.a - 1, s.b - 1, s.c + 1, s.d, s.e⟩⟩

def M673 : Machine := [g673_0, g673_1, f2, f3, f4]

theorem step_M673 (a b c d e : Nat) :
    step M673 ⟨a, b, c, d, e⟩ =
      if 1 ≤ c ∧ 1 ≤ d then some ⟨a, b + 2, c - 1, d - 1, e⟩
      else if 1 ≤ a ∧ 1 ≤ b then some ⟨a - 1, b - 1, c + 1, d, e⟩
      else if 1 ≤ c ∧ 1 ≤ e then some ⟨a + 3, b, c - 1, d, e - 1⟩
      else if 1 ≤ a then some ⟨a - 1, b, c, d + 1, e⟩
      else if 1 ≤ d then some ⟨a, b, c + 1, d - 1, e + 2⟩
      else none := by
  simp only [M673, step, g673_0, g673_1, f2, f3, f4, decide_eq_true_eq]

/-- LEMMA 0 for 673: same halt criterion as 431. -/
theorem halt_iff_673 (a b c d e : Nat) :
    step M673 ⟨a, b, c, d, e⟩ = none ↔
      a = 0 ∧ d = 0 ∧ (c = 0 ∨ e = 0) := by
  rw [step_M673]
  by_cases h0 : 1 ≤ c ∧ 1 ≤ d
  · rw [if_pos h0]; simp; omega
  · rw [if_neg h0]
    by_cases h1 : 1 ≤ a ∧ 1 ≤ b
    · rw [if_pos h1]; simp; omega
    · rw [if_neg h1]
      by_cases h2 : 1 ≤ c ∧ 1 ≤ e
      · rw [if_pos h2]; simp; omega
      · rw [if_neg h2]
        by_cases h3 : 1 ≤ a
        · rw [if_pos h3]; simp; omega
        · rw [if_neg h3]
          by_cases h4 : 1 ≤ d
          · rw [if_pos h4]; simp; omega
          · rw [if_neg h4]; simp; omega

theorem spec673 : FireSpec M673 id := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · -- fire0 at v7 = 0: rule 9/35 (priority 0) is disabled by d = 0
    intro a b c e
    show step M673 ⟨a + 1, b + 1, c, 0, e⟩ = some ⟨a, b, c + 1, 0, e⟩
    rw [step_M673]
    rw [if_neg (by omega : ¬(1 ≤ c ∧ 1 ≤ (0:Nat)))]
    rw [if_pos (by omega : 1 ≤ a + 1 ∧ 1 ≤ b + 1)]
    simp
  · -- fire1: rule 9/35 is now top priority, fires outright
    intro b c d e
    show step M673 ⟨0, b, c + 1, d + 1, e⟩ = some ⟨0, b + 2, c, d, e⟩
    rw [step_M673]
    rw [if_pos (by omega : 1 ≤ c + 1 ∧ 1 ≤ d + 1)]
    simp
  · intro b c e
    show step M673 ⟨0, b, c + 1, 0, e + 1⟩ = some ⟨3, b, c, 0, e⟩
    rw [step_M673]
    rw [if_neg (by omega : ¬(1 ≤ c + 1 ∧ 1 ≤ (0:Nat)))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ b))]
    rw [if_pos (by omega : 1 ≤ c + 1 ∧ 1 ≤ e + 1)]
    simp
  · intro a c e
    show step M673 ⟨a, 0, c + 1, 0, e + 1⟩ = some ⟨a + 3, 0, c, 0, e⟩
    rw [step_M673]
    rw [if_neg (by omega : ¬(1 ≤ c + 1 ∧ 1 ≤ (0:Nat)))]
    rw [if_neg (by omega : ¬(1 ≤ a ∧ 1 ≤ (0:Nat)))]
    rw [if_pos (by omega : 1 ≤ c + 1 ∧ 1 ≤ e + 1)]
    simp
  · intro a d e
    show step M673 ⟨a + 1, 0, 0, d, e⟩ = some ⟨a, 0, 0, d + 1, e⟩
    rw [step_M673]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ d))]
    rw [if_neg (by omega : ¬(1 ≤ a + 1 ∧ 1 ≤ (0:Nat)))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ e))]
    rw [if_pos (by omega : 1 ≤ a + 1)]
    simp
  · intro b d e
    show step M673 ⟨0, b, 0, d + 1, e⟩ = some ⟨0, b, 1, d, e + 2⟩
    rw [step_M673]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ d + 1))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ b))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ e))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
    rw [if_pos (by omega : 1 ≤ d + 1)]
    simp

/-- Entry for 673: f3, f4, f2 — 3 steps from n = 2 to B_1 (word as in
    431; the swap is invisible here too). -/
theorem entry673 : Steps M673 3 ⟨1, 0, 0, 0, 0⟩ (id (Bst 1)) := by decide

/-- THEOREM M673: [9/35, 5/6, 8/55, 7/2, 605/7] never halts from n = 2. -/
theorem m673_never_halts : NeverHalts M673 ⟨1, 0, 0, 0, 0⟩ :=
  spec673.neverHalts entry673

/-! ## Machine 502 = [7/15, 9/14, 125/77, 2/5, 847/2]

431 under the prime permutation 2→5, 5→7, 7→2 (rule order preserved).
Axis embedding: role (a, b, c, d, e) ↦ machine state (d, b, a, c, e).
Entry: 2 steps to the image of B_1. -/

def r502_0 : Rule := ⟨fun s => decide (1 ≤ s.b ∧ 1 ≤ s.c),
                      fun s => ⟨s.a, s.b - 1, s.c - 1, s.d + 1, s.e⟩⟩
def r502_1 : Rule := ⟨fun s => decide (1 ≤ s.a ∧ 1 ≤ s.d),
                      fun s => ⟨s.a - 1, s.b + 2, s.c, s.d - 1, s.e⟩⟩
def r502_2 : Rule := ⟨fun s => decide (1 ≤ s.d ∧ 1 ≤ s.e),
                      fun s => ⟨s.a, s.b, s.c + 3, s.d - 1, s.e - 1⟩⟩
def r502_3 : Rule := ⟨fun s => decide (1 ≤ s.c),
                      fun s => ⟨s.a + 1, s.b, s.c - 1, s.d, s.e⟩⟩
def r502_4 : Rule := ⟨fun s => decide (1 ≤ s.a),
                      fun s => ⟨s.a - 1, s.b, s.c, s.d + 1, s.e + 2⟩⟩

def M502 : Machine := [r502_0, r502_1, r502_2, r502_3, r502_4]

/-- The axis embedding of 502 (axmap (2,1,3,0,4) of the Python). -/
def phi502 : St → St := fun s => ⟨s.d, s.b, s.a, s.c, s.e⟩

theorem step_M502 (a b c d e : Nat) :
    step M502 ⟨a, b, c, d, e⟩ =
      if 1 ≤ b ∧ 1 ≤ c then some ⟨a, b - 1, c - 1, d + 1, e⟩
      else if 1 ≤ a ∧ 1 ≤ d then some ⟨a - 1, b + 2, c, d - 1, e⟩
      else if 1 ≤ d ∧ 1 ≤ e then some ⟨a, b, c + 3, d - 1, e - 1⟩
      else if 1 ≤ c then some ⟨a + 1, b, c - 1, d, e⟩
      else if 1 ≤ a then some ⟨a - 1, b, c, d + 1, e + 2⟩
      else none := by
  simp only [M502, step, r502_0, r502_1, r502_2, r502_3, r502_4,
    decide_eq_true_eq]

/-- LEMMA 0 for 502: halt ⟺ v2 = 0 ∧ v5 = 0 ∧ (v7 = 0 ∨ v11 = 0). -/
theorem halt_iff_502 (a b c d e : Nat) :
    step M502 ⟨a, b, c, d, e⟩ = none ↔
      a = 0 ∧ c = 0 ∧ (d = 0 ∨ e = 0) := by
  rw [step_M502]
  by_cases h0 : 1 ≤ b ∧ 1 ≤ c
  · rw [if_pos h0]; simp; omega
  · rw [if_neg h0]
    by_cases h1 : 1 ≤ a ∧ 1 ≤ d
    · rw [if_pos h1]; simp; omega
    · rw [if_neg h1]
      by_cases h2 : 1 ≤ d ∧ 1 ≤ e
      · rw [if_pos h2]; simp; omega
      · rw [if_neg h2]
        by_cases h3 : 1 ≤ c
        · rw [if_pos h3]; simp; omega
        · rw [if_neg h3]
          by_cases h4 : 1 ≤ a
          · rw [if_pos h4]; simp; omega
          · rw [if_neg h4]; simp; omega

theorem spec502 : FireSpec M502 phi502 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · -- fire0 role ⟨a+1,b+1,c,0,e⟩ ↦ (0, b+1, a+1, c, e): rule 7/15 fires
    intro a b c e
    show step M502 ⟨0, b + 1, a + 1, c, e⟩ = some ⟨0, b, a, c + 1, e⟩
    rw [step_M502]
    rw [if_pos (by omega : 1 ≤ b + 1 ∧ 1 ≤ a + 1)]
    simp
  · -- fire1 role ⟨0,b,c+1,d+1,e⟩ ↦ (d+1, b, 0, c+1, e): rule 9/14 fires
    intro b c d e
    show step M502 ⟨d + 1, b, 0, c + 1, e⟩ = some ⟨d, b + 2, 0, c, e⟩
    rw [step_M502]
    rw [if_neg (by omega : ¬(1 ≤ b ∧ 1 ≤ (0:Nat)))]
    rw [if_pos (by omega : 1 ≤ d + 1 ∧ 1 ≤ c + 1)]
    simp
  · -- fire2a role ⟨0,b,c+1,0,e+1⟩ ↦ (0, b, 0, c+1, e+1): rule 125/77
    intro b c e
    show step M502 ⟨0, b, 0, c + 1, e + 1⟩ = some ⟨0, b, 3, c, e⟩
    rw [step_M502]
    rw [if_neg (by omega : ¬(1 ≤ b ∧ 1 ≤ (0:Nat)))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c + 1))]
    rw [if_pos (by omega : 1 ≤ c + 1 ∧ 1 ≤ e + 1)]
    simp
  · -- fire2b role ⟨a,0,c+1,0,e+1⟩ ↦ (0, 0, a, c+1, e+1): rule 125/77
    intro a c e
    show step M502 ⟨0, 0, a, c + 1, e + 1⟩ = some ⟨0, 0, a + 3, c, e⟩
    rw [step_M502]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ a))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c + 1))]
    rw [if_pos (by omega : 1 ≤ c + 1 ∧ 1 ≤ e + 1)]
    simp
  · -- fire3 role ⟨a+1,0,0,d,e⟩ ↦ (d, 0, a+1, 0, e): rule 2/5 fires
    intro a d e
    show step M502 ⟨d, 0, a + 1, 0, e⟩ = some ⟨d + 1, 0, a, 0, e⟩
    rw [step_M502]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ a + 1))]
    rw [if_neg (by omega : ¬(1 ≤ d ∧ 1 ≤ (0:Nat)))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ e))]
    rw [if_pos (by omega : 1 ≤ a + 1)]
    simp
  · -- fire4 role ⟨0,b,0,d+1,e⟩ ↦ (d+1, b, 0, 0, e): rule 847/2 fires
    intro b d e
    show step M502 ⟨d + 1, b, 0, 0, e⟩ = some ⟨d, b, 0, 1, e + 2⟩
    rw [step_M502]
    rw [if_neg (by omega : ¬(1 ≤ b ∧ 1 ≤ (0:Nat)))]
    rw [if_neg (by omega : ¬(1 ≤ d + 1 ∧ 1 ≤ (0:Nat)))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ e))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
    rw [if_pos (by omega : 1 ≤ d + 1)]
    simp

/-- Entry for 502: rules 847/2 then 125/77 — 2 steps from n = 2 to
    φ(B_1) = (0, 0, 3, 0, 1), i.e. 5³·11. -/
theorem entry502 : Steps M502 2 ⟨1, 0, 0, 0, 0⟩ (phi502 (Bst 1)) := by decide

/-- THEOREM M502: [7/15, 9/14, 125/77, 2/5, 847/2] never halts from n = 2. -/
theorem m502_never_halts : NeverHalts M502 ⟨1, 0, 0, 0, 0⟩ :=
  spec502.neverHalts entry502

/-! ## Machine 623 = [9/10, 5/21, 343/55, 2/7, 605/2]

431 under the prime swap 2 ↔ 7, with the first two rules also swapped in
priority.  Axis embedding: role (a, b, c, d, e) ↦ (d, b, c, a, e).
Entry: 2 steps to the image of B_1. -/

def r623_0 : Rule := ⟨fun s => decide (1 ≤ s.a ∧ 1 ≤ s.c),
                      fun s => ⟨s.a - 1, s.b + 2, s.c - 1, s.d, s.e⟩⟩
def r623_1 : Rule := ⟨fun s => decide (1 ≤ s.b ∧ 1 ≤ s.d),
                      fun s => ⟨s.a, s.b - 1, s.c + 1, s.d - 1, s.e⟩⟩
def r623_2 : Rule := ⟨fun s => decide (1 ≤ s.c ∧ 1 ≤ s.e),
                      fun s => ⟨s.a, s.b, s.c - 1, s.d + 3, s.e - 1⟩⟩
def r623_3 : Rule := ⟨fun s => decide (1 ≤ s.d),
                      fun s => ⟨s.a + 1, s.b, s.c, s.d - 1, s.e⟩⟩
def r623_4 : Rule := ⟨fun s => decide (1 ≤ s.a),
                      fun s => ⟨s.a - 1, s.b, s.c + 1, s.d, s.e + 2⟩⟩

def M623 : Machine := [r623_0, r623_1, r623_2, r623_3, r623_4]

/-- The axis embedding of 623 (axmap (3,1,2,0,4) of the Python). -/
def phi623 : St → St := fun s => ⟨s.d, s.b, s.c, s.a, s.e⟩

theorem step_M623 (a b c d e : Nat) :
    step M623 ⟨a, b, c, d, e⟩ =
      if 1 ≤ a ∧ 1 ≤ c then some ⟨a - 1, b + 2, c - 1, d, e⟩
      else if 1 ≤ b ∧ 1 ≤ d then some ⟨a, b - 1, c + 1, d - 1, e⟩
      else if 1 ≤ c ∧ 1 ≤ e then some ⟨a, b, c - 1, d + 3, e - 1⟩
      else if 1 ≤ d then some ⟨a + 1, b, c, d - 1, e⟩
      else if 1 ≤ a then some ⟨a - 1, b, c + 1, d, e + 2⟩
      else none := by
  simp only [M623, step, r623_0, r623_1, r623_2, r623_3, r623_4,
    decide_eq_true_eq]

/-- LEMMA 0 for 623: halt ⟺ v2 = 0 ∧ v7 = 0 ∧ (v5 = 0 ∨ v11 = 0). -/
theorem halt_iff_623 (a b c d e : Nat) :
    step M623 ⟨a, b, c, d, e⟩ = none ↔
      a = 0 ∧ d = 0 ∧ (c = 0 ∨ e = 0) := by
  rw [step_M623]
  by_cases h0 : 1 ≤ a ∧ 1 ≤ c
  · rw [if_pos h0]; simp; omega
  · rw [if_neg h0]
    by_cases h1 : 1 ≤ b ∧ 1 ≤ d
    · rw [if_pos h1]; simp; omega
    · rw [if_neg h1]
      by_cases h2 : 1 ≤ c ∧ 1 ≤ e
      · rw [if_pos h2]; simp; omega
      · rw [if_neg h2]
        by_cases h3 : 1 ≤ d
        · rw [if_pos h3]; simp; omega
        · rw [if_neg h3]
          by_cases h4 : 1 ≤ a
          · rw [if_pos h4]; simp; omega
          · rw [if_neg h4]; simp; omega

theorem spec623 : FireSpec M623 phi623 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · -- fire0 role ⟨a+1,b+1,c,0,e⟩ ↦ (0, b+1, c, a+1, e): rule 5/21 fires
    -- (its higher-priority rule 9/10 is disabled by v2 = 0)
    intro a b c e
    show step M623 ⟨0, b + 1, c, a + 1, e⟩ = some ⟨0, b, c + 1, a, e⟩
    rw [step_M623]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c))]
    rw [if_pos (by omega : 1 ≤ b + 1 ∧ 1 ≤ a + 1)]
    simp
  · -- fire1 role ⟨0,b,c+1,d+1,e⟩ ↦ (d+1, b, c+1, 0, e): rule 9/10 fires
    intro b c d e
    show step M623 ⟨d + 1, b, c + 1, 0, e⟩ = some ⟨d, b + 2, c, 0, e⟩
    rw [step_M623]
    rw [if_pos (by omega : 1 ≤ d + 1 ∧ 1 ≤ c + 1)]
    simp
  · -- fire2a role ⟨0,b,c+1,0,e+1⟩ ↦ (0, b, c+1, 0, e+1): rule 343/55
    intro b c e
    show step M623 ⟨0, b, c + 1, 0, e + 1⟩ = some ⟨0, b, c, 3, e⟩
    rw [step_M623]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c + 1))]
    rw [if_neg (by omega : ¬(1 ≤ b ∧ 1 ≤ (0:Nat)))]
    rw [if_pos (by omega : 1 ≤ c + 1 ∧ 1 ≤ e + 1)]
    simp
  · -- fire2b role ⟨a,0,c+1,0,e+1⟩ ↦ (0, 0, c+1, a, e+1): rule 343/55
    intro a c e
    show step M623 ⟨0, 0, c + 1, a, e + 1⟩ = some ⟨0, 0, c, a + 3, e⟩
    rw [step_M623]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c + 1))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ a))]
    rw [if_pos (by omega : 1 ≤ c + 1 ∧ 1 ≤ e + 1)]
    simp
  · -- fire3 role ⟨a+1,0,0,d,e⟩ ↦ (d, 0, 0, a+1, e): rule 2/7 fires
    intro a d e
    show step M623 ⟨d, 0, 0, a + 1, e⟩ = some ⟨d + 1, 0, 0, a, e⟩
    rw [step_M623]
    rw [if_neg (by omega : ¬(1 ≤ d ∧ 1 ≤ (0:Nat)))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ a + 1))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ e))]
    rw [if_pos (by omega : 1 ≤ a + 1)]
    simp
  · -- fire4 role ⟨0,b,0,d+1,e⟩ ↦ (d+1, b, 0, 0, e): rule 605/2 fires
    intro b d e
    show step M623 ⟨d + 1, b, 0, 0, e⟩ = some ⟨d, b, 1, 0, e + 2⟩
    rw [step_M623]
    rw [if_neg (by omega : ¬(1 ≤ d + 1 ∧ 1 ≤ (0:Nat)))]
    rw [if_neg (by omega : ¬(1 ≤ b ∧ 1 ≤ (0:Nat)))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ e))]
    rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
    rw [if_pos (by omega : 1 ≤ d + 1)]
    simp

/-- Entry for 623: rules 605/2 then 343/55 — 2 steps from n = 2 to
    φ(B_1) = (0, 0, 0, 3, 1), i.e. 7³·11. -/
theorem entry623 : Steps M623 2 ⟨1, 0, 0, 0, 0⟩ (phi623 (Bst 1)) := by decide

/-- THEOREM M623: [9/10, 5/21, 343/55, 2/7, 605/2] never halts from n = 2. -/
theorem m623_never_halts : NeverHalts M623 ⟨1, 0, 0, 0, 0⟩ :=
  spec623.neverHalts entry623

/-! ## Ground-truth cross-checks (independent of the lemmas above)

Five phases simulated concretely on each machine.  With entry length E,
the step count to the image of B_5 is E + Σ_{j=1..4} (8·2^j − 5):
673: 3 + 220 = 223;  502/623: 2 + 220 = 222. -/

example : step M673 ⟨0, 0, 0, 0, 0⟩ = none := by decide
example : step M502 ⟨0, 0, 0, 0, 0⟩ = none := by decide
example : step M623 ⟨0, 0, 0, 0, 0⟩ = none := by decide

example : iter M673 223 ⟨1, 0, 0, 0, 0⟩ = some ⟨63, 0, 0, 0, 5⟩ := by decide
example : iter M502 222 ⟨1, 0, 0, 0, 0⟩ = some ⟨0, 0, 63, 0, 5⟩ := by decide
example : iter M623 222 ⟨1, 0, 0, 0, 0⟩ = some ⟨0, 0, 0, 63, 5⟩ := by decide

example : phi502 (Bst 5) = ⟨0, 0, 63, 0, 5⟩ := by decide
example : phi623 (Bst 5) = ⟨0, 0, 0, 63, 5⟩ := by decide

end Fractran.Siblings431
