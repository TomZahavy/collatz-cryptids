/-
Machine 678 = FRACTRAN program [9/70, 25/2, 44/15, 7/55, 3/5], BBf(23)
holdout #678, in exponent-vector form over the primes (2, 3, 5, 7, 11).

    f0 = 9/70  : (v2--, v3+=2, v5--, v7--)   guard v2>=1 & v5>=1 & v7>=1
    f1 = 25/2  : (v2--, v5+=2)               guard v2>=1
    f2 = 44/15 : (v2+=2, v3--, v5--, v11++)  guard v3>=1 & v5>=1
    f3 = 7/55  : (v5--, v7++, v11--)         guard v5>=1 & v11>=1
    f4 = 3/5   : (v3++, v5--)                guard v5>=1

THEOREM (m678_never_halts): started from n = 2 = (1,0,0,0,0), the
program never halts.

Proof skeleton (mirrors m678_proof.py):
  * boundary family  B_i = (0, 0, 2(w+1), 0, w),  w := 2^(i+1) - 1,
    carrying the invariant v5 = 2(v11 + 1);
  * entry: 16 steps reach B_1 = (0,0,8,0,3)  [the Python enters at B_2;
    the uniform template below is proved for ALL parameter values, so the
    Lean induction can start one boundary earlier];
  * one phase: from B_i the machine performs f3^w, f4, then three block
    modes: C-blocks (f2 f0^2)^P, Q-blocks (f2 f0 f1 with v5 pinned at 2
    for w = 3P+1, i.e. i even / f2 f1 f0 with v5 pinned at 1 for w = 3F,
    i.e. i odd), and T-blocks (f2 f1^2)^T, T = 3P+1+Q; landing exactly on
    B_{i+1} in 7w + 4 steps;
  * induction: the orbit visits every B_i, hence never halts.
-/
import LeanBbf.M431

/- The state-cast tactic `simp only [St.mk.injEq, ...] <;> omega` is used
   mechanically; on some goals simp already closes everything and the
   listed lemmas go unused, which is fine. -/
set_option linter.unusedSimpArgs false

namespace Fractran.M678

open Fractran
open Fractran.M431 (two_pow_pos two_pow_mod3)

/-! ## The rules (DELTA/GUARD tables of m678_proof.py, priority order) -/

def f0 : Rule := ⟨fun s => decide (1 ≤ s.a ∧ 1 ≤ s.c ∧ 1 ≤ s.d),
                  fun s => ⟨s.a - 1, s.b + 2, s.c - 1, s.d - 1, s.e⟩⟩
def f1 : Rule := ⟨fun s => decide (1 ≤ s.a),
                  fun s => ⟨s.a - 1, s.b, s.c + 2, s.d, s.e⟩⟩
def f2 : Rule := ⟨fun s => decide (1 ≤ s.b ∧ 1 ≤ s.c),
                  fun s => ⟨s.a + 2, s.b - 1, s.c - 1, s.d, s.e + 1⟩⟩
def f3 : Rule := ⟨fun s => decide (1 ≤ s.c ∧ 1 ≤ s.e),
                  fun s => ⟨s.a, s.b, s.c - 1, s.d + 1, s.e - 1⟩⟩
def f4 : Rule := ⟨fun s => decide (1 ≤ s.c),
                  fun s => ⟨s.a, s.b + 1, s.c - 1, s.d, s.e⟩⟩

def M678 : Machine := [f0, f1, f2, f3, f4]

/-- The priority step function of machine 678 in closed form. -/
theorem step_M678 (a b c d e : Nat) :
    step M678 ⟨a, b, c, d, e⟩ =
      if 1 ≤ a ∧ 1 ≤ c ∧ 1 ≤ d then some ⟨a - 1, b + 2, c - 1, d - 1, e⟩
      else if 1 ≤ a then some ⟨a - 1, b, c + 2, d, e⟩
      else if 1 ≤ b ∧ 1 ≤ c then some ⟨a + 2, b - 1, c - 1, d, e + 1⟩
      else if 1 ≤ c ∧ 1 ≤ e then some ⟨a, b, c - 1, d + 1, e - 1⟩
      else if 1 ≤ c then some ⟨a, b + 1, c - 1, d, e⟩
      else none := by
  simp only [M678, step, f0, f1, f2, f3, f4, decide_eq_true_eq]

/-! ## Lemma 0: the halt criterion -/

/-- LEMMA 0.  No rule fires iff `v2 = 0` and `v5 = 0`. -/
theorem halt_iff (a b c d e : Nat) :
    step M678 ⟨a, b, c, d, e⟩ = none ↔ a = 0 ∧ c = 0 := by
  rw [step_M678]
  by_cases h0 : 1 ≤ a ∧ 1 ≤ c ∧ 1 ≤ d
  · rw [if_pos h0]; simp; omega
  · rw [if_neg h0]
    by_cases h1 : 1 ≤ a
    · rw [if_pos h1]; simp; omega
    · rw [if_neg h1]
      by_cases h2 : 1 ≤ b ∧ 1 ≤ c
      · rw [if_pos h2]; simp; omega
      · rw [if_neg h2]
        by_cases h3 : 1 ≤ c ∧ 1 ≤ e
        · rw [if_pos h3]; simp; omega
        · rw [if_neg h3]
          by_cases h4 : 1 ≤ c
          · rw [if_pos h4]; simp; omega
          · rw [if_neg h4]; simp; omega

/-- The machine is not degenerate: it CAN halt (from the zero vector). -/
example : step M678 ⟨0, 0, 0, 0, 0⟩ = none := by decide

/-! ## Single-firing lemmas (successor-pattern, hypothesis-free)

`fire1` needs two shapes: v5 = 0 (inside Q-blocks) and v7 = 0 (inside
T-blocks) — each disables the higher-priority f0 on its own. -/

theorem fire0 (a b c d e : Nat) :
    step M678 ⟨a + 1, b, c + 1, d + 1, e⟩ = some ⟨a, b + 2, c, d, e⟩ := by
  rw [step_M678]
  rw [if_pos (by omega : 1 ≤ a + 1 ∧ 1 ≤ c + 1 ∧ 1 ≤ d + 1)]
  simp

theorem fire1c (a b d e : Nat) :
    step M678 ⟨a + 1, b, 0, d, e⟩ = some ⟨a, b, 2, d, e⟩ := by
  rw [step_M678]
  rw [if_neg (by omega : ¬(1 ≤ a + 1 ∧ 1 ≤ (0:Nat) ∧ 1 ≤ d))]
  rw [if_pos (by omega : 1 ≤ a + 1)]
  simp

theorem fire1d (a b c e : Nat) :
    step M678 ⟨a + 1, b, c, 0, e⟩ = some ⟨a, b, c + 2, 0, e⟩ := by
  rw [step_M678]
  rw [if_neg (by omega : ¬(1 ≤ a + 1 ∧ 1 ≤ c ∧ 1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ a + 1)]
  simp

theorem fire2 (b c d e : Nat) :
    step M678 ⟨0, b + 1, c + 1, d, e⟩ = some ⟨2, b, c, d, e + 1⟩ := by
  rw [step_M678]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c + 1 ∧ 1 ≤ d))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ b + 1 ∧ 1 ≤ c + 1)]
  simp

theorem fire3 (c d e : Nat) :
    step M678 ⟨0, 0, c + 1, d, e + 1⟩ = some ⟨0, 0, c, d + 1, e⟩ := by
  rw [step_M678]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c + 1 ∧ 1 ≤ d))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c + 1))]
  rw [if_pos (by omega : 1 ≤ c + 1 ∧ 1 ≤ e + 1)]
  simp

theorem fire4 (c d : Nat) :
    step M678 ⟨0, 0, c + 1, d, 0⟩ = some ⟨0, 1, c, d, 0⟩ := by
  rw [step_M678]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c + 1 ∧ 1 ≤ d))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c + 1))]
  rw [if_neg (by omega : ¬(1 ≤ c + 1 ∧ 1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ c + 1)]
  simp

/-! ## Single-rule runs -/

/-- Stage-A runs `f3^k`: drains v11 into v7 (v2 = 0 kills f0, f1;
    v3 = 0 kills f2). -/
theorem run_f3 (k c d e : Nat) :
    Steps M678 k ⟨0, 0, c + k, d, e + k⟩ ⟨0, 0, c, d + k, e⟩ := by
  induction k generalizing d with
  | zero => exact steps_zero M678 _
  | succ k ih =>
    exact ((steps_one M678 (fire3 (c + k) d (e + k))).comp (ih (d + 1))
      rfl).cast (by omega) rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- `f0^k` (top priority): pays v2, v5, v7 down together, builds v3. -/
theorem run_f0 (k x b c d e : Nat) :
    Steps M678 k ⟨x + k, b, c + k, d + k, e⟩ ⟨x, b + 2 * k, c, d, e⟩ := by
  induction k generalizing b with
  | zero => exact steps_zero M678 _
  | succ k ih =>
    exact ((steps_one M678 (fire0 (x + k) b (c + k) (d + k) e)).comp
      (ih (b + 2)) rfl).cast (by omega) rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- `f1^k` at v7 = 0 (f0 disabled): converts v2 into pairs of v5. -/
theorem run_f1d (k x b c e : Nat) :
    Steps M678 k ⟨x + k, b, c, 0, e⟩ ⟨x, b, c + 2 * k, 0, e⟩ := by
  induction k generalizing c with
  | zero => exact steps_zero M678 _
  | succ k ih =>
    exact ((steps_one M678 (fire1d (x + k) b c e)).comp (ih (c + 2))
      rfl).cast (by omega) rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-! ## The three block modes (start states affine in the block index) -/

/-- C-blocks `(f2 f0^2)^n`: net per block v3 += 3, v5 -= 3, v7 -= 2,
    v11 += 1 (f0 fires exactly twice, limited by v2 = 2). -/
theorem blockC (n : Nat) : ∀ y e c d : Nat,
    Steps M678 (n * 3) ⟨0, y + 1, c + 3 * n, d + 2 * n, e⟩
      ⟨0, y + 3 * n + 1, c, d, e + n⟩ := by
  induction n with
  | zero => intro y e c d; exact steps_zero M678 _
  | succ n ih =>
    intro y e c d
    exact ((steps_one M678 (fire2 y (c + 3 * n + 2) (d + 2 * (n + 1)) e)).comp
      ((run_f0 2 0 y (c + 3 * n) (d + 2 * n) (e + 1)).comp
        (ih (y + 3) (e + 1) c d) rfl)
      rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- Q-blocks, even case `(f2 f0 f1)^n`: v5 pinned at 2 (after f2 it is
    1, so f0 outranks f1); net v3 += 1, v7 -= 1, v11 += 1. -/
theorem blockQE (n : Nat) : ∀ y e d : Nat,
    Steps M678 (n * 3) ⟨0, y + 1, 2, d + n, e⟩
      ⟨0, y + n + 1, 2, d, e + n⟩ := by
  induction n with
  | zero => intro y e d; exact steps_zero M678 _
  | succ n ih =>
    intro y e d
    exact ((steps_one M678 (fire2 y 1 (d + (n + 1)) e)).comp
      ((steps_one M678 (fire0 1 y 0 (d + n) (e + 1))).comp
        ((steps_one M678 (fire1c 0 (y + 2) (d + n) (e + 1))).comp
          (ih (y + 1) (e + 1) d) rfl) rfl)
      rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- Q-blocks, odd case `(f2 f1 f0)^n`: v5 pinned at 1 (f2 zeroes v5, so
    f1 must fire before f0 can); same net effect. -/
theorem blockQO (n : Nat) : ∀ y e d : Nat,
    Steps M678 (n * 3) ⟨0, y + 1, 1, d + n, e⟩
      ⟨0, y + n + 1, 1, d, e + n⟩ := by
  induction n with
  | zero => intro y e d; exact steps_zero M678 _
  | succ n ih =>
    intro y e d
    exact ((steps_one M678 (fire2 y 0 (d + (n + 1)) e)).comp
      ((steps_one M678 (fire1c 1 y (d + (n + 1)) (e + 1))).comp
        ((steps_one M678 (fire0 0 y 1 (d + n) (e + 1))).comp
          (ih (y + 1) (e + 1) d) rfl) rfl)
      rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- T-blocks `(f2 f1^2)^n` at v7 = 0 (f0 dead): each remaining 3 becomes
    three 5s and an 11; net v3 -= 1, v5 += 3, v11 += 1. -/
theorem blockT (n : Nat) : ∀ b c e : Nat,
    Steps M678 (n * 3) ⟨0, b + n, c + 1, 0, e⟩
      ⟨0, b, c + 1 + 3 * n, 0, e + n⟩ := by
  induction n with
  | zero => intro b c e; exact steps_zero M678 _
  | succ n ih =>
    intro b c e
    exact ((steps_one M678 (fire2 (b + n) c 0 e)).comp
      ((run_f1d 2 0 (b + n) c (e + 1)).comp
        (ih b (c + 3) (e + 1)) rfl)
      rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-! ## One full phase

From B = (0, 0, 2w+2, 0, w) the machine reaches (0, 0, 4w+4, 0, 2w+1) in
exactly 7w + 4 steps.  Stated over an abstract w with its residue mod 3
as hypothesis (w = 3P+1 for i even, w = 3F for i odd). -/

/-- One phase, even case (w = 3P+1): word f3^w, f4, (f2 f0^2)^P,
    (f2 f0 f1)^(P+1), (f2 f1^2)^(4P+2). -/
theorem phase_even (w P : Nat) (hw : w = 3 * P + 1) :
    Steps M678 (7 * w + 4) ⟨0, 0, 2 * w + 2, 0, w⟩
      ⟨0, 0, 4 * w + 4, 0, 2 * w + 1⟩ := by
  -- Stage A: f3^w : -> (0, 0, w+2, w, 0)
  have s1 : Steps M678 w ⟨0, 0, 2 * w + 2, 0, w⟩ ⟨0, 0, w + 2, w, 0⟩ :=
    (run_f3 w (w + 2) 0 0).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- Stage B: f4 : -> (0, 1, w+1, w, 0)
  have s2 : Steps M678 1 ⟨0, 0, w + 2, w, 0⟩ ⟨0, 1, w + 1, w, 0⟩ :=
    (steps_one M678 (fire4 (w + 1) w)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- C-blocks: -> (0, 3P+1, 2, P+1, P)
  have s3 : Steps M678 (P * 3) ⟨0, 1, w + 1, w, 0⟩
      ⟨0, 3 * P + 1, 2, P + 1, P⟩ :=
    (blockC P 0 0 2 (P + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- Q-blocks (Q = P+1): -> (0, 4P+2, 2, 0, 2P+1)
  have s4 : Steps M678 ((P + 1) * 3) ⟨0, 3 * P + 1, 2, P + 1, P⟩
      ⟨0, 4 * P + 2, 2, 0, 2 * P + 1⟩ :=
    (blockQE (P + 1) (3 * P) P 0).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- T-blocks (T = 4P+2): -> (0, 0, 4w+4, 0, 2w+1)
  have s5 : Steps M678 ((4 * P + 2) * 3) ⟨0, 4 * P + 2, 2, 0, 2 * P + 1⟩
      ⟨0, 0, 4 * w + 4, 0, 2 * w + 1⟩ :=
    (blockT (4 * P + 2) 0 1 (2 * P + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  exact s1.comp (s2.comp (s3.comp (s4.comp s5 rfl) rfl) rfl) (by omega)

/-- One phase, odd case (w = 3F): word f3^w, f4, (f2 f0^2)^F,
    (f2 f1 f0)^F, (f2 f1^2)^(4F+1). -/
theorem phase_odd (w F : Nat) (hw : w = 3 * F) :
    Steps M678 (7 * w + 4) ⟨0, 0, 2 * w + 2, 0, w⟩
      ⟨0, 0, 4 * w + 4, 0, 2 * w + 1⟩ := by
  have s1 : Steps M678 w ⟨0, 0, 2 * w + 2, 0, w⟩ ⟨0, 0, w + 2, w, 0⟩ :=
    (run_f3 w (w + 2) 0 0).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s2 : Steps M678 1 ⟨0, 0, w + 2, w, 0⟩ ⟨0, 1, w + 1, w, 0⟩ :=
    (steps_one M678 (fire4 (w + 1) w)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- C-blocks: -> (0, 3F+1, 1, F, F)
  have s3 : Steps M678 (F * 3) ⟨0, 1, w + 1, w, 0⟩
      ⟨0, 3 * F + 1, 1, F, F⟩ :=
    (blockC F 0 0 1 F).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- Q-blocks (Q = F): -> (0, 4F+1, 1, 0, 2F)
  have s4 : Steps M678 (F * 3) ⟨0, 3 * F + 1, 1, F, F⟩
      ⟨0, 4 * F + 1, 1, 0, 2 * F⟩ :=
    (blockQO F (3 * F) F 0).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- T-blocks (T = 4F+1): -> (0, 0, 4w+4, 0, 2w+1)
  have s5 : Steps M678 ((4 * F + 1) * 3) ⟨0, 4 * F + 1, 1, 0, 2 * F⟩
      ⟨0, 0, 4 * w + 4, 0, 2 * w + 1⟩ :=
    (blockT (4 * F + 1) 0 0 (2 * F)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  exact s1.comp (s2.comp (s3.comp (s4.comp s5 rfl) rfl) rfl) (by omega)

/-! ## The boundary family and the induction -/

/-- The boundary state B_i = (0, 0, 2^(i+2), 0, 2^(i+1) - 1), carrying
    the invariant v5 = 2(v11 + 1).  B_1 = (0, 0, 8, 0, 3). -/
def Bst (i : Nat) : St := ⟨0, 0, 2 ^ (i + 2), 0, 2 ^ (i + 1) - 1⟩

/-- Entry: from n = 2 the machine reaches B_1 in 16 steps. -/
theorem entry : Steps M678 16 ⟨1, 0, 0, 0, 0⟩ (Bst 1) := by decide

/-- The phase at the boundary family: B_i -> B_{i+1} in 7w+4 steps,
    w = 2^(i+1) - 1. -/
theorem phase_step (i : Nat) :
    Steps M678 (7 * (2 ^ (i + 1) - 1) + 4) (Bst i) (Bst (i + 1)) := by
  have hp1 := two_pow_pos (i + 1)
  have h2 : 2 ^ (i + 2) = 2 ^ (i + 1) * 2 := Nat.pow_succ 2 (i + 1)
  -- the same facts in the exact atom shapes `Bst (i+1)` unfolds to
  have hA : (2:Nat) ^ (i + 1 + 1) = 2 ^ (i + 1) * 2 := Nat.pow_succ 2 (i + 1)
  have hB : (2:Nat) ^ (i + 1 + 2) = 2 ^ (i + 1 + 1) * 2 :=
    Nat.pow_succ 2 (i + 1 + 1)
  rcases Nat.mod_two_eq_zero_or_one i with hpar | hpar
  · -- i even: w = 2^(i+1) - 1 ≡ 1 (mod 3)
    obtain ⟨t, ht⟩ : ∃ t, i = 2 * t := ⟨i / 2, by omega⟩
    obtain ⟨c, hc⟩ := two_pow_mod3 t
    have hps : 2 ^ (2 * t + 1) = 2 ^ (2 * t) * 2 := Nat.pow_succ 2 (2 * t)
    have hw : 2 ^ (i + 1) - 1 = 3 * (2 * c) + 1 := by
      rw [ht, hps, hc]; omega
    exact (phase_even (2 ^ (i + 1) - 1) (2 * c) hw).cast rfl
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)
  · -- i odd: w = 2^(i+1) - 1 ≡ 0 (mod 3)
    obtain ⟨t, ht⟩ : ∃ t, i = 2 * t + 1 := ⟨i / 2, by omega⟩
    obtain ⟨c, hc⟩ := two_pow_mod3 (t + 1)
    have he : i + 1 = 2 * (t + 1) := by omega
    have hw : 2 ^ (i + 1) - 1 = 3 * c := by rw [he, hc]; omega
    exact (phase_odd (2 ^ (i + 1) - 1) c hw).cast rfl
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)

/-- Total step count to reach B_{k+1}: T 0 = 16 (the entry), then one
    phase per boundary.  T k = 7·2^(k+2) - 3(k+1) - 9. -/
def T : Nat → Nat
  | 0 => 16
  | k + 1 => T k + (7 * (2 ^ (k + 2) - 1) + 4)

/-- The orbit visits every boundary: after exactly T k steps the machine
    is at B_{k+1} — for every k. -/
theorem reach : ∀ k, Steps M678 (T k) ⟨1, 0, 0, 0, 0⟩ (Bst (k + 1))
  | 0 => entry
  | k + 1 => (reach k).comp (phase_step (k + 1)) rfl

theorem T_ge (k : Nat) : k ≤ T k := by
  induction k with
  | zero => exact Nat.zero_le 16
  | succ k ih =>
    have hp := two_pow_pos (k + 2)
    show k + 1 ≤ T k + (7 * (2 ^ (k + 2) - 1) + 4)
    omega

/-! ## The theorem -/

/-- THEOREM M678.  The FRACTRAN program [9/70, 25/2, 44/15, 7/55, 3/5],
    started at n = 2 (exponent vector (1,0,0,0,0)), never halts. -/
theorem m678_never_halts : NeverHalts M678 ⟨1, 0, 0, 0, 0⟩ :=
  neverHalts_of_unbounded fun n => ⟨T n, Bst (n + 1), T_ge n, reach n⟩

/-! ## Lemma 3, explicit form -/

/-- Every state visited on the orbit has a successor. -/
theorem orbit_never_stuck (n : Nat) (s' : St)
    (h : iter M678 n ⟨1, 0, 0, 0, 0⟩ = some s') : step M678 s' ≠ none := by
  intro hstep
  apply m678_never_halts (n + 1)
  rw [iter_add M678 n 1, h]
  show (step M678 s').bind (iter M678 0) = none
  rw [hstep]
  rfl

/-- LEMMA 3: no state on the orbit satisfies the halt criterion of
    Lemma 0 (v2 = 0 and v5 = 0). -/
theorem no_halt_state_on_orbit (n : Nat) (s' : St)
    (h : iter M678 n ⟨1, 0, 0, 0, 0⟩ = some s') :
    ¬(s'.a = 0 ∧ s'.c = 0) := by
  intro hcrit
  apply orbit_never_stuck n s' h
  obtain ⟨a, b, c, d, e⟩ := s'
  exact (halt_iff a b c d e).mpr hcrit

/-! ## Ground-truth cross-checks (independent of the lemmas above)

Four phases beyond the entry: T 4 = 424 = 7·2^6 - 15 - 9 steps from
n = 2 land exactly on B_5 = (0, 0, 128, 0, 63). -/

example : T 4 = 424 := by decide
set_option maxRecDepth 20000 in
example : iter M678 424 ⟨1, 0, 0, 0, 0⟩ = some ⟨0, 0, 128, 0, 63⟩ := by
  decide
example : Bst 5 = ⟨0, 0, 128, 0, 63⟩ := by decide

end Fractran.M678
