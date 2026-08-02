/-
Machine 455 = FRACTRAN program [63/10, 8/77, 33/2, 5/9, 7/3], BBf(23)
holdout #455, in exponent-vector form over the primes (2, 3, 5, 7, 11).

    f0 = 63/10 : (v2--, v3+=2, v5--, v7++)   guard v2>=1 & v5>=1
    f1 = 8/77  : (v2+=3, v7--, v11--)        guard v7>=1 & v11>=1
    f2 = 33/2  : (v2--, v3++, v11++)         guard v2>=1
    f3 = 5/9   : (v3-=2, v5++)               guard v3>=2
    f4 = 7/3   : (v3--, v7++)                guard v3>=1

THEOREM (m455_never_halts): started from n = 2 = (1,0,0,0,0), the
program never halts.

Proof skeleton (mirrors m455_proof.py):
  * boundary family  B_i = (X+1, X-2, 0, 0, i-1),  X := 2^i,  i >= 2;
  * entry (Lemma 1): 11 steps f2 f4 f1 f2^3 f3 f4 f1 f0 f1 reach B_2;
  * one phase (Lemma 2): from B_i the machine performs
      f2^(X+1), f3^(X-1), f4, f1, then rounds of (f0^3 f1) with
      round-start (3, 6r, X-1-3r, 2r, X+i-1-r), and an endgame split on
      X mod 3:  X = 3R+1 (i even): (f0^3 f1)^(R-1), f0^3, f1^(2R+1);
                X = 3F+2 (i odd):  (f0^3 f1)^F,     f0^1, f1^(2F+1);
    arriving at B_{i+1} in exactly 4X steps;
  * induction: the orbit visits every B_i, hence never halts.
-/
import LeanBbf.M431

/- The state-cast tactic `simp only [St.mk.injEq, ...] <;> omega` is used
   mechanically; on some goals simp already closes everything and the
   listed lemmas go unused, which is fine. -/
set_option linter.unusedSimpArgs false

namespace Fractran.M455

open Fractran
open Fractran.M431 (two_pow_pos two_pow_mod3)

/-! ## The rules (DELTA/GUARD tables of m455_proof.py, priority order) -/

def f0 : Rule := ⟨fun s => decide (1 ≤ s.a ∧ 1 ≤ s.c),
                  fun s => ⟨s.a - 1, s.b + 2, s.c - 1, s.d + 1, s.e⟩⟩
def f1 : Rule := ⟨fun s => decide (1 ≤ s.d ∧ 1 ≤ s.e),
                  fun s => ⟨s.a + 3, s.b, s.c, s.d - 1, s.e - 1⟩⟩
def f2 : Rule := ⟨fun s => decide (1 ≤ s.a),
                  fun s => ⟨s.a - 1, s.b + 1, s.c, s.d, s.e + 1⟩⟩
def f3 : Rule := ⟨fun s => decide (2 ≤ s.b),
                  fun s => ⟨s.a, s.b - 2, s.c + 1, s.d, s.e⟩⟩
def f4 : Rule := ⟨fun s => decide (1 ≤ s.b),
                  fun s => ⟨s.a, s.b - 1, s.c, s.d + 1, s.e⟩⟩

def M455 : Machine := [f0, f1, f2, f3, f4]

/-- The priority step function of machine 455 in closed form. -/
theorem step_M455 (a b c d e : Nat) :
    step M455 ⟨a, b, c, d, e⟩ =
      if 1 ≤ a ∧ 1 ≤ c then some ⟨a - 1, b + 2, c - 1, d + 1, e⟩
      else if 1 ≤ d ∧ 1 ≤ e then some ⟨a + 3, b, c, d - 1, e - 1⟩
      else if 1 ≤ a then some ⟨a - 1, b + 1, c, d, e + 1⟩
      else if 2 ≤ b then some ⟨a, b - 2, c + 1, d, e⟩
      else if 1 ≤ b then some ⟨a, b - 1, c, d + 1, e⟩
      else none := by
  simp only [M455, step, f0, f1, f2, f3, f4, decide_eq_true_eq]

/-! ## Lemma 0: the halt criterion -/

/-- LEMMA 0.  No rule fires iff `v2 = 0`, `v3 = 0` and (`v7 = 0` or
    `v11 = 0`). -/
theorem halt_iff (a b c d e : Nat) :
    step M455 ⟨a, b, c, d, e⟩ = none ↔
      a = 0 ∧ b = 0 ∧ (d = 0 ∨ e = 0) := by
  rw [step_M455]
  by_cases h0 : 1 ≤ a ∧ 1 ≤ c
  · rw [if_pos h0]; simp; omega
  · rw [if_neg h0]
    by_cases h1 : 1 ≤ d ∧ 1 ≤ e
    · rw [if_pos h1]; simp; omega
    · rw [if_neg h1]
      by_cases h2 : 1 ≤ a
      · rw [if_pos h2]; simp; omega
      · rw [if_neg h2]
        by_cases h3 : 2 ≤ b
        · rw [if_pos h3]; simp; omega
        · rw [if_neg h3]
          by_cases h4 : 1 ≤ b
          · rw [if_pos h4]; simp; omega
          · rw [if_neg h4]; simp; omega

/-- The machine is not degenerate: it CAN halt (from the zero vector). -/
example : step M455 ⟨0, 0, 0, 0, 0⟩ = none := by decide

/-! ## Single-firing lemmas (successor-pattern, hypothesis-free)

Guard and higher-priority-failure conditions are baked into the state
shape.  `fire1` needs two shapes (v2 = 0, or v5 = 0 with v2 arbitrary),
matching the two situations in which rule 1 fires on the orbit. -/

theorem fire0 (a b c d e : Nat) :
    step M455 ⟨a + 1, b, c + 1, d, e⟩ = some ⟨a, b + 2, c, d + 1, e⟩ := by
  rw [step_M455]
  rw [if_pos (by omega : 1 ≤ a + 1 ∧ 1 ≤ c + 1)]
  simp

theorem fire1a (b c d e : Nat) :
    step M455 ⟨0, b, c, d + 1, e + 1⟩ = some ⟨3, b, c, d, e⟩ := by
  rw [step_M455]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c))]
  rw [if_pos (by omega : 1 ≤ d + 1 ∧ 1 ≤ e + 1)]
  simp

theorem fire1b (a b d e : Nat) :
    step M455 ⟨a, b, 0, d + 1, e + 1⟩ = some ⟨a + 3, b, 0, d, e⟩ := by
  rw [step_M455]
  rw [if_neg (by omega : ¬(1 ≤ a ∧ 1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ d + 1 ∧ 1 ≤ e + 1)]
  simp

theorem fire2 (a b e : Nat) :
    step M455 ⟨a + 1, b, 0, 0, e⟩ = some ⟨a, b + 1, 0, 0, e + 1⟩ := by
  rw [step_M455]
  rw [if_neg (by omega : ¬(1 ≤ a + 1 ∧ 1 ≤ (0:Nat)))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ e))]
  rw [if_pos (by omega : 1 ≤ a + 1)]
  simp

theorem fire3 (b c e : Nat) :
    step M455 ⟨0, b + 2, c, 0, e⟩ = some ⟨0, b, c + 1, 0, e⟩ := by
  rw [step_M455]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ e))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 2 ≤ b + 2)]
  simp

theorem fire4 (c e : Nat) :
    step M455 ⟨0, 1, c, 0, e⟩ = some ⟨0, 0, c, 1, e⟩ := by
  rw [step_M455]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ e))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
  rw [if_neg (by omega : ¬(2 ≤ (1:Nat)))]
  rw [if_pos (by omega : 1 ≤ (1:Nat))]

/-! ## Lemma 1: the entry

From n = 2 the word f2 f4 f1 f2^3 f3 f4 f1 f0 f1 (11 steps) reaches
B_2 = (5, 2, 0, 0, 1). -/

/-! ## Single-rule runs (state affine in the run counter; all guard and
priority conditions linear in it, discharged by `omega` for all t) -/

/-- Stage-A runs `f2^k`: drains v2 into v3 and v11 (v5 = v7 = 0 disables
    f0 and f1 throughout). -/
theorem run_f2 (k x b e : Nat) :
    Steps M455 k ⟨x + k, b, 0, 0, e⟩ ⟨x, b + k, 0, 0, e + k⟩ := by
  induction k generalizing b e with
  | zero => exact steps_zero M455 _
  | succ k ih =>
    exact ((steps_one M455 (fire2 (x + k) b e)).comp (ih (b + 1) (e + 1))
      rfl).cast (by omega) rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- Stage-B runs `f3^k`: converts v3-pairs into v5 (v2 = 0 disables
    f0, f2; v7 = 0 disables f1). -/
theorem run_f3 (k b c e : Nat) :
    Steps M455 k ⟨0, b + 2 * k, c, 0, e⟩ ⟨0, b, c + k, 0, e⟩ := by
  induction k generalizing c with
  | zero => exact steps_zero M455 _
  | succ k ih =>
    exact ((steps_one M455 (fire3 (b + 2 * k) c e)).comp (ih (c + 1))
      rfl).cast (by omega) rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- Endgame runs `f1^k` with v5 = 0: v5 = 0 keeps f0 disabled even as v2
    grows by 3 per firing; drains v7 and v11 together. -/
theorem run_f1b (k a b x y : Nat) :
    Steps M455 k ⟨a, b, 0, x + k, y + k⟩ ⟨a + 3 * k, b, 0, x, y⟩ := by
  induction k generalizing a with
  | zero => exact steps_zero M455 _
  | succ k ih =>
    exact ((steps_one M455 (fire1b a b (x + k) (y + k))).comp (ih (a + 3))
      rfl).cast (by omega) rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- Round runs `f0^k`: top priority, drains v2 and v5 together, pays
    2 to v3 and 1 to v7 per firing. -/
theorem run_f0 (k x b c d e : Nat) :
    Steps M455 k ⟨x + k, b, c + k, d, e⟩ ⟨x, b + 2 * k, c, d + k, e⟩ := by
  induction k generalizing b d with
  | zero => exact steps_zero M455 _
  | succ k ih =>
    exact ((steps_one M455 (fire0 (x + k) b (c + k) d e)).comp
      (ih (b + 2) (d + 1)) rfl).cast (by omega) rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-! ## The Stage-E round block (start state affine in the round index) -/

/-- `(f0^3 f1)^n`: each round burns 3 of v5 and 1 of v11 into 6 of v3
    and 2 of v7, restoring v2 = 3. -/
theorem stageE (n : Nat) : ∀ y d c e : Nat,
    Steps M455 (n * 4) ⟨3, y, c + 3 * n, d, e + n⟩
      ⟨3, y + 6 * n, c, d + 2 * n, e⟩ := by
  induction n with
  | zero => intro y d c e; exact steps_zero M455 _
  | succ n ih =>
    intro y d c e
    exact ((run_f0 3 0 y (c + 3 * n) d (e + (n + 1))).comp
      ((steps_one M455 (fire1a (y + 2 * 3) (c + 3 * n) (d + 2) (e + n))).comp
        (ih (y + 6) (d + 2) c e) rfl)
      rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-! ## Lemma 2: one full phase

From B = (X+1, X-2, 0, 0, j) the machine reaches
(2X+1, 2X-2, 0, 0, j+1) in exactly 4X steps.  Stated over an abstract X
with its residue mod 3 as hypothesis (X = 3R+1 for i even, X = 3F+2 for
i odd), making every side condition `omega`-linear. -/

/-- One phase, even case (X = 3R+1, R ≥ 1).  The word is f2^(X+1),
    f3^(X-1), f4, f1, (f0^3 f1)^(R-1), f0^3, f1^(2R+1). -/
theorem phase_even (j X R : Nat) (hX : X = 3 * R + 1) (hR : 1 ≤ R) :
    Steps M455 (4 * X) ⟨X + 1, X - 2, 0, 0, j⟩
      ⟨2 * X + 1, 2 * X - 2, 0, 0, j + 1⟩ := by
  -- Stage A: f2^(X+1) : -> (0, 2X-1, 0, 0, X+j+1)
  have s1 : Steps M455 (X + 1) ⟨X + 1, X - 2, 0, 0, j⟩
      ⟨0, 2 * X - 1, 0, 0, X + j + 1⟩ :=
    (run_f2 (X + 1) 0 (X - 2) j).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- Stage B: f3^(X-1) : -> (0, 1, X-1, 0, X+j+1)
  have s2 : Steps M455 (X - 1) ⟨0, 2 * X - 1, 0, 0, X + j + 1⟩
      ⟨0, 1, X - 1, 0, X + j + 1⟩ :=
    (run_f3 (X - 1) 1 0 (X + j + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- Stage C: f4 : -> (0, 0, X-1, 1, X+j+1)
  have s3 : Steps M455 1 ⟨0, 1, X - 1, 0, X + j + 1⟩
      ⟨0, 0, X - 1, 1, X + j + 1⟩ :=
    steps_one M455 (fire4 (X - 1) (X + j + 1))
  -- Stage D: f1 : -> (3, 0, X-1, 0, X+j)
  have s4 : Steps M455 1 ⟨0, 0, X - 1, 1, X + j + 1⟩
      ⟨3, 0, X - 1, 0, X + j⟩ :=
    (steps_one M455 (fire1a 0 (X - 1) 0 (X + j))).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- Stage E rounds: (f0^3 f1)^(R-1) : -> (3, 6(R-1), 3, 2(R-1), X+j+1-R)
  have s5 : Steps M455 ((R - 1) * 4) ⟨3, 0, X - 1, 0, X + j⟩
      ⟨3, 6 * (R - 1), 3, 2 * (R - 1), X + j + 1 - R⟩ :=
    (stageE (R - 1) 0 0 3 (X + j + 1 - R)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- last full f0^3 : -> (0, 6R, 0, 2R+1, X+j+1-R)
  have s6 : Steps M455 3 ⟨3, 6 * (R - 1), 3, 2 * (R - 1), X + j + 1 - R⟩
      ⟨0, 6 * R, 0, 2 * R + 1, X + j + 1 - R⟩ :=
    (run_f0 3 0 (6 * (R - 1)) 0 (2 * (R - 1)) (X + j + 1 - R)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- final f1^(2R+1) : -> (6R+3, 6R, 0, 0, j+1) = (2X+1, 2X-2, 0, 0, j+1)
  have s7 : Steps M455 (2 * R + 1) ⟨0, 6 * R, 0, 2 * R + 1, X + j + 1 - R⟩
      ⟨2 * X + 1, 2 * X - 2, 0, 0, j + 1⟩ :=
    (run_f1b (2 * R + 1) 0 (6 * R) 0 (j + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  exact s1.comp (s2.comp (s3.comp (s4.comp (s5.comp (s6.comp s7 rfl) rfl)
    rfl) rfl) rfl) (by omega)

/-- One phase, odd case (X = 3F+2).  The word is f2^(X+1), f3^(X-1),
    f4, f1, (f0^3 f1)^F, f0^1, f1^(2F+1) — the last round's f0 fires
    only once, stopped by v5 = 0 with v2 = 2 left over. -/
theorem phase_odd (j X F : Nat) (hX : X = 3 * F + 2) :
    Steps M455 (4 * X) ⟨X + 1, X - 2, 0, 0, j⟩
      ⟨2 * X + 1, 2 * X - 2, 0, 0, j + 1⟩ := by
  have s1 : Steps M455 (X + 1) ⟨X + 1, X - 2, 0, 0, j⟩
      ⟨0, 2 * X - 1, 0, 0, X + j + 1⟩ :=
    (run_f2 (X + 1) 0 (X - 2) j).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s2 : Steps M455 (X - 1) ⟨0, 2 * X - 1, 0, 0, X + j + 1⟩
      ⟨0, 1, X - 1, 0, X + j + 1⟩ :=
    (run_f3 (X - 1) 1 0 (X + j + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s3 : Steps M455 1 ⟨0, 1, X - 1, 0, X + j + 1⟩
      ⟨0, 0, X - 1, 1, X + j + 1⟩ :=
    steps_one M455 (fire4 (X - 1) (X + j + 1))
  have s4 : Steps M455 1 ⟨0, 0, X - 1, 1, X + j + 1⟩
      ⟨3, 0, X - 1, 0, X + j⟩ :=
    (steps_one M455 (fire1a 0 (X - 1) 0 (X + j))).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- rounds: (f0^3 f1)^F : -> (3, 6F, 1, 2F, X+j-F)
  have s5 : Steps M455 (F * 4) ⟨3, 0, X - 1, 0, X + j⟩
      ⟨3, 6 * F, 1, 2 * F, X + j - F⟩ :=
    (stageE F 0 0 1 (X + j - F)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- single f0 : -> (2, 6F+2, 0, 2F+1, X+j-F)
  have s6 : Steps M455 1 ⟨3, 6 * F, 1, 2 * F, X + j - F⟩
      ⟨2, 6 * F + 2, 0, 2 * F + 1, X + j - F⟩ :=
    (run_f0 1 2 (6 * F) 0 (2 * F) (X + j - F)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- final f1^(2F+1) : -> (6F+5, 6F+2, 0, 0, j+1) = (2X+1, 2X-2, 0, 0, j+1)
  have s7 : Steps M455 (2 * F + 1) ⟨2, 6 * F + 2, 0, 2 * F + 1, X + j - F⟩
      ⟨2 * X + 1, 2 * X - 2, 0, 0, j + 1⟩ :=
    (run_f1b (2 * F + 1) 2 (6 * F + 2) 0 (j + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  exact s1.comp (s2.comp (s3.comp (s4.comp (s5.comp (s6.comp s7 rfl) rfl)
    rfl) rfl) rfl) (by omega)

/-! ## The boundary family and the induction -/

/-- The phase-i boundary state B_i = (2^i + 1, 2^i - 2, 0, 0, i-1),
    meaningful for i ≥ 2; B_2 = (5, 2, 0, 0, 1). -/
def Bst (i : Nat) : St := ⟨2 ^ i + 1, 2 ^ i - 2, 0, 0, i - 1⟩

/-- LEMMA 1 (entry): from n = 2 the word f2 f4 f1 f2^3 f3 f4 f1 f0 f1
    (11 steps) reaches B_2. -/
theorem entry : Steps M455 11 ⟨1, 0, 0, 0, 0⟩ (Bst 2) := by decide

/-- LEMMA 2 at the boundary family: B_i -> B_{i+1} in 4·2^i steps. -/
theorem phase_step (i : Nat) (hi : 2 ≤ i) :
    Steps M455 (4 * 2 ^ i) (Bst i) (Bst (i + 1)) := by
  have h1 : 2 ^ (i + 1) = 2 ^ i * 2 := Nat.pow_succ 2 i
  have h4 : (4:Nat) ≤ 2 ^ i :=
    calc (4:Nat) = 2 ^ 2 := by decide
    _ ≤ 2 ^ i := Nat.pow_le_pow_right (by decide) hi
  rcases Nat.mod_two_eq_zero_or_one i with hpar | hpar
  · -- i even: X = 2^i ≡ 1 (mod 3)
    obtain ⟨t, ht⟩ : ∃ t, i = 2 * t := ⟨i / 2, by omega⟩
    obtain ⟨c, hc⟩ := two_pow_mod3 t
    have hX : 2 ^ i = 3 * c + 1 := by rw [ht, hc]
    have hR : 1 ≤ c := by rw [ht] at h4; omega
    exact (phase_even (i - 1) (2 ^ i) c hX hR).cast rfl
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)
  · -- i odd: X = 2^i ≡ 2 (mod 3)
    obtain ⟨t, ht⟩ : ∃ t, i = 2 * t + 1 := ⟨i / 2, by omega⟩
    obtain ⟨c, hc⟩ := two_pow_mod3 t
    have hps : 2 ^ (2 * t + 1) = 2 ^ (2 * t) * 2 := Nat.pow_succ 2 (2 * t)
    have hX : 2 ^ i = 3 * (2 * c) + 2 := by rw [ht, hps, hc]; omega
    exact (phase_odd (i - 1) (2 ^ i) (2 * c) hX).cast rfl
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)

/-- Total step count to reach B_{k+2}: T 0 = 11 (the entry), then one
    phase of 4·2^i steps per boundary.  T k = 2^(k+4) - 5. -/
def T : Nat → Nat
  | 0 => 11
  | k + 1 => T k + 4 * 2 ^ (k + 2)

/-- The orbit visits every boundary: after exactly T k steps the machine
    is at B_{k+2} — for every k. -/
theorem reach : ∀ k, Steps M455 (T k) ⟨1, 0, 0, 0, 0⟩ (Bst (k + 2))
  | 0 => entry
  | k + 1 => (reach k).comp (phase_step (k + 2) (by omega)) rfl

theorem T_ge (k : Nat) : k ≤ T k := by
  induction k with
  | zero => exact Nat.zero_le 11
  | succ k ih =>
    have hp := two_pow_pos (k + 2)
    show k + 1 ≤ T k + 4 * 2 ^ (k + 2)
    omega

/-! ## The theorem -/

/-- THEOREM M455.  The FRACTRAN program [63/10, 8/77, 33/2, 5/9, 7/3],
    started at n = 2 (exponent vector (1,0,0,0,0)), never halts. -/
theorem m455_never_halts : NeverHalts M455 ⟨1, 0, 0, 0, 0⟩ :=
  neverHalts_of_unbounded fun n => ⟨T n, Bst (n + 2), T_ge n, reach n⟩

/-! ## Lemma 3, explicit form -/

/-- Every state visited on the orbit has a successor. -/
theorem orbit_never_stuck (n : Nat) (s' : St)
    (h : iter M455 n ⟨1, 0, 0, 0, 0⟩ = some s') : step M455 s' ≠ none := by
  intro hstep
  apply m455_never_halts (n + 1)
  rw [iter_add M455 n 1, h]
  show (step M455 s').bind (iter M455 0) = none
  rw [hstep]
  rfl

/-- LEMMA 3: no state on the orbit satisfies the halt criterion of
    Lemma 0. -/
theorem no_halt_state_on_orbit (n : Nat) (s' : St)
    (h : iter M455 n ⟨1, 0, 0, 0, 0⟩ = some s') :
    ¬(s'.a = 0 ∧ s'.b = 0 ∧ (s'.d = 0 ∨ s'.e = 0)) := by
  intro hcrit
  apply orbit_never_stuck n s' h
  obtain ⟨a, b, c, d, e⟩ := s'
  exact (halt_iff a b c d e).mpr hcrit

/-! ## Ground-truth cross-checks (independent of the lemmas above)

Four phases simulated concretely: T 4 = 251 = 2^8 - 5 steps from n = 2
land exactly on B_6 = (65, 62, 0, 0, 5). -/

example : T 4 = 251 := by decide
set_option maxRecDepth 8192 in
example : iter M455 251 ⟨1, 0, 0, 0, 0⟩ = some ⟨65, 62, 0, 0, 5⟩ := by decide
example : Bst 6 = ⟨65, 62, 0, 0, 5⟩ := by decide

end Fractran.M455
