/-
Machine 570 = FRACTRAN program [77/30, 88/21, 9/2, 5/11, 7/3], BBf(23)
holdout #570, in exponent-vector form over the primes (2, 3, 5, 7, 11).

    f0 = 77/30 : (v2--, v3--, v5--, v7++, v11++)  guard v2,v3,v5 >= 1
    f1 = 88/21 : (v2+=3, v3--, v7--, v11++)       guard v3,v7 >= 1
    f2 = 9/2   : (v2--, v3+=2)                    guard v2 >= 1
    f3 = 5/11  : (v5++, v11--)                    guard v11 >= 1
    f4 = 7/3   : (v3--, v7++)                     guard v3 >= 1

THEOREM (m570_never_halts): started from n = 2 = (1,0,0,0,0), the
program never halts.

  * boundary family  Bst m = (0, 2^(m+1) + 2m, 0, 0, 2^m - 1);
  * entry (Lemma 1): ONE step (f2) reaches Bst 0 = (0,2,0,0,0);
  * one phase (Lemma 2): f3^x, f4, f1, (f0^3 f1)^q, [f0], f1^L, f2^C
    with x = 2^m - 1, split on x mod 3 (i.e. on the parity of m),
    arriving at Bst (m+1) in exactly 5*2^m steps;
  * induction: the orbit visits every Bst m, hence never halts.

ENTRY REMARK.  m_siblings_proofs.py enters at Bst 4 after 76 steps; the
phase lemmas below hold for all parameter values, so the formalization
inducts from step 1 (76 is recovered as `T 4`).
-/
import LeanBbf.M431

set_option linter.unusedSimpArgs false

namespace Fractran.M570

open Fractran
open Fractran.M431 (two_pow_pos two_pow_mod3)

/-! ## The rules -/

def f0 : Rule := ⟨fun s => decide (1 ≤ s.a ∧ 1 ≤ s.b ∧ 1 ≤ s.c),
                  fun s => ⟨s.a - 1, s.b - 1, s.c - 1, s.d + 1, s.e + 1⟩⟩
def f1 : Rule := ⟨fun s => decide (1 ≤ s.b ∧ 1 ≤ s.d),
                  fun s => ⟨s.a + 3, s.b - 1, s.c, s.d - 1, s.e + 1⟩⟩
def f2 : Rule := ⟨fun s => decide (1 ≤ s.a),
                  fun s => ⟨s.a - 1, s.b + 2, s.c, s.d, s.e⟩⟩
def f3 : Rule := ⟨fun s => decide (1 ≤ s.e),
                  fun s => ⟨s.a, s.b, s.c + 1, s.d, s.e - 1⟩⟩
def f4 : Rule := ⟨fun s => decide (1 ≤ s.b),
                  fun s => ⟨s.a, s.b - 1, s.c, s.d + 1, s.e⟩⟩

def M570 : Machine := [f0, f1, f2, f3, f4]

theorem step_M570 (a b c d e : Nat) :
    step M570 ⟨a, b, c, d, e⟩ =
      if 1 ≤ a ∧ 1 ≤ b ∧ 1 ≤ c then some ⟨a - 1, b - 1, c - 1, d + 1, e + 1⟩
      else if 1 ≤ b ∧ 1 ≤ d then some ⟨a + 3, b - 1, c, d - 1, e + 1⟩
      else if 1 ≤ a then some ⟨a - 1, b + 2, c, d, e⟩
      else if 1 ≤ e then some ⟨a, b, c + 1, d, e - 1⟩
      else if 1 ≤ b then some ⟨a, b - 1, c, d + 1, e⟩
      else none := by
  simp only [M570, step, f0, f1, f2, f3, f4, decide_eq_true_eq]

/-! ## Lemma 0: the halt criterion -/

/-- LEMMA 0.  No rule fires iff `v2 = 0`, `v3 = 0` and `v11 = 0`. -/
theorem halt_iff (a b c d e : Nat) :
    step M570 ⟨a, b, c, d, e⟩ = none ↔ a = 0 ∧ b = 0 ∧ e = 0 := by
  rw [step_M570]
  by_cases h0 : 1 ≤ a ∧ 1 ≤ b ∧ 1 ≤ c
  · rw [if_pos h0]; simp; omega
  · rw [if_neg h0]
    by_cases h1 : 1 ≤ b ∧ 1 ≤ d
    · rw [if_pos h1]; simp; omega
    · rw [if_neg h1]
      by_cases h2 : 1 ≤ a
      · rw [if_pos h2]; simp; omega
      · rw [if_neg h2]
        by_cases h3 : 1 ≤ e
        · rw [if_pos h3]; simp; omega
        · rw [if_neg h3]
          by_cases h4 : 1 ≤ b
          · rw [if_pos h4]; simp; omega
          · rw [if_neg h4]; simp; omega

example : step M570 ⟨0, 0, 0, 0, 0⟩ = none := by decide

/-! ## Single-firing lemmas -/

theorem fire0 (a b c d e : Nat) :
    step M570 ⟨a + 1, b + 1, c + 1, d, e⟩ = some ⟨a, b, c, d + 1, e + 1⟩ := by
  rw [step_M570]
  rw [if_pos (by omega : 1 ≤ a + 1 ∧ 1 ≤ b + 1 ∧ 1 ≤ c + 1)]
  simp

/-- f1 with `v2 = 0` (which disables f0). -/
theorem fire1a (b c d e : Nat) :
    step M570 ⟨0, b + 1, c, d + 1, e⟩ = some ⟨3, b, c, d, e + 1⟩ := by
  rw [step_M570]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ b + 1 ∧ 1 ≤ c))]
  rw [if_pos (by omega : 1 ≤ b + 1 ∧ 1 ≤ d + 1)]
  simp

/-- f1 with `v5 = 0` (which disables f0 even as v2 grows). -/
theorem fire1b (a b d e : Nat) :
    step M570 ⟨a, b + 1, 0, d + 1, e⟩ = some ⟨a + 3, b, 0, d, e + 1⟩ := by
  rw [step_M570]
  rw [if_neg (by omega : ¬(1 ≤ a ∧ 1 ≤ b + 1 ∧ 1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ b + 1 ∧ 1 ≤ d + 1)]
  simp

/-- f2 with `v5 = 0` (f0 off) and `v7 = 0` (f1 off). -/
theorem fire2 (a b e : Nat) :
    step M570 ⟨a + 1, b, 0, 0, e⟩ = some ⟨a, b + 2, 0, 0, e⟩ := by
  rw [step_M570]
  rw [if_neg (by omega : ¬(1 ≤ a + 1 ∧ 1 ≤ b ∧ 1 ≤ (0:Nat)))]
  rw [if_neg (by omega : ¬(1 ≤ b ∧ 1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ a + 1)]
  simp

/-- f3 with `v2 = 0` (f0, f2 off) and `v7 = 0` (f1 off). -/
theorem fire3 (b c e : Nat) :
    step M570 ⟨0, b, c, 0, e + 1⟩ = some ⟨0, b, c + 1, 0, e⟩ := by
  rw [step_M570]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ b ∧ 1 ≤ c))]
  rw [if_neg (by omega : ¬(1 ≤ b ∧ 1 ≤ (0:Nat)))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ e + 1)]
  simp

/-- f4 at `v11 = 0` exactly: that is what stops the f3-run. -/
theorem fire4 (b c : Nat) :
    step M570 ⟨0, b + 1, c, 0, 0⟩ = some ⟨0, b, c, 1, 0⟩ := by
  rw [step_M570]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ b + 1 ∧ 1 ≤ c))]
  rw [if_neg (by omega : ¬(1 ≤ b + 1 ∧ 1 ≤ (0:Nat)))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ b + 1)]
  simp

/-! ## Single-rule runs -/

theorem run_f3 (n b c e : Nat) :
    Steps M570 n ⟨0, b, c, 0, e + n⟩ ⟨0, b, c + n, 0, e⟩ := by
  induction n generalizing c with
  | zero => exact steps_zero M570 _
  | succ n ih =>
    exact ((steps_one M570 (fire3 b c (e + n))).comp (ih (c + 1))
      rfl).cast (by omega) (by simp only [St.mk.injEq, and_true, true_and]
        <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

theorem run_f2 (n a b e : Nat) :
    Steps M570 n ⟨a + n, b, 0, 0, e⟩ ⟨a, b + 2 * n, 0, 0, e⟩ := by
  induction n generalizing b with
  | zero => exact steps_zero M570 _
  | succ n ih =>
    exact ((steps_one M570 (fire2 (a + n) b e)).comp (ih (b + 2))
      rfl).cast (by omega) (by simp only [St.mk.injEq, and_true, true_and]
        <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

theorem run_f0 (n a b c d e : Nat) :
    Steps M570 n ⟨a + n, b + n, c + n, d, e⟩ ⟨a, b, c, d + n, e + n⟩ := by
  induction n generalizing d e with
  | zero => exact steps_zero M570 _
  | succ n ih =>
    exact ((steps_one M570 (fire0 (a + n) (b + n) (c + n) d e)).comp
      (ih (d + 1) (e + 1)) rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

theorem run_f1b (n a b d e : Nat) :
    Steps M570 n ⟨a, b + n, 0, d + n, e⟩ ⟨a + 3 * n, b, 0, d, e + n⟩ := by
  induction n generalizing a e with
  | zero => exact steps_zero M570 _
  | succ n ih =>
    exact ((steps_one M570 (fire1b a (b + n) (d + n) e)).comp
      (ih (a + 3) (e + 1)) rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-! ## The `(f0^3 f1)` round block -/

/-- `(f0^3 f1)^n`: each round spends 4 of v3 and 3 of v5, gains 2 to v7
    and 4 to v11, and restores v2 = 3. -/
theorem rounds (n : Nat) : ∀ b c d e : Nat,
    Steps M570 (n * 4) ⟨3, b + 4 * n, c + 3 * n, d, e⟩
      ⟨3, b, c, d + 2 * n, e + 4 * n⟩ := by
  induction n with
  | zero => intro b c d e; exact steps_zero M570 _
  | succ n ih =>
    intro b c d e
    exact ((run_f0 3 0 (b + 4 * n + 1) (c + 3 * n) d e).comp
      ((steps_one M570 (fire1a (b + 4 * n) (c + 3 * n) (d + 2) (e + 3))).comp
        (ih b c (d + 2) (e + 4)) rfl) rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-! ## Lemma 2: one full phase, split on `x mod 3` -/

/-- Even case: `x = 3q` (m even).  Word: f3^(3q), f4, f1, (f0^3 f1)^q,
    f1^(2q), f2^(6q+3). -/
theorem phase_even (q u : Nat) :
    Steps M570 (15 * q + 5) ⟨0, 6 * q + u + 2, 0, 0, 3 * q⟩
      ⟨0, 12 * q + u + 6, 0, 0, 6 * q + 1⟩ := by
  have s1 : Steps M570 (3 * q) ⟨0, 6 * q + u + 2, 0, 0, 3 * q⟩
      ⟨0, 6 * q + u + 2, 3 * q, 0, 0⟩ :=
    (run_f3 (3 * q) (6 * q + u + 2) 0 0).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s2 : Steps M570 1 ⟨0, 6 * q + u + 2, 3 * q, 0, 0⟩
      ⟨0, 6 * q + u + 1, 3 * q, 1, 0⟩ :=
    (steps_one M570 (fire4 (6 * q + u + 1) (3 * q))).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) rfl
  have s3 : Steps M570 1 ⟨0, 6 * q + u + 1, 3 * q, 1, 0⟩
      ⟨3, 6 * q + u, 3 * q, 0, 1⟩ :=
    (steps_one M570 (fire1a (6 * q + u) (3 * q) 0 0)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s4 : Steps M570 (q * 4) ⟨3, 6 * q + u, 3 * q, 0, 1⟩
      ⟨3, 2 * q + u, 0, 2 * q, 4 * q + 1⟩ :=
    (rounds q (2 * q + u) 0 0 1).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s5 : Steps M570 (2 * q) ⟨3, 2 * q + u, 0, 2 * q, 4 * q + 1⟩
      ⟨6 * q + 3, u, 0, 0, 6 * q + 1⟩ :=
    (run_f1b (2 * q) 3 u 0 (4 * q + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s6 : Steps M570 (6 * q + 3) ⟨6 * q + 3, u, 0, 0, 6 * q + 1⟩
      ⟨0, 12 * q + u + 6, 0, 0, 6 * q + 1⟩ :=
    (run_f2 (6 * q + 3) 0 u (6 * q + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  exact s1.comp (s2.comp (s3.comp (s4.comp (s5.comp s6 rfl) rfl) rfl) rfl)
    (by omega)

/-- Odd case: `x = 3q+1` (m odd).  The extra single `f0` is stopped by
    `v5 = 0` with `v2 = 2` left over. -/
theorem phase_odd (q u : Nat) :
    Steps M570 (15 * q + 10) ⟨0, 6 * q + u + 4, 0, 0, 3 * q + 1⟩
      ⟨0, 12 * q + u + 10, 0, 0, 6 * q + 3⟩ := by
  have s1 : Steps M570 (3 * q + 1) ⟨0, 6 * q + u + 4, 0, 0, 3 * q + 1⟩
      ⟨0, 6 * q + u + 4, 3 * q + 1, 0, 0⟩ :=
    (run_f3 (3 * q + 1) (6 * q + u + 4) 0 0).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s2 : Steps M570 1 ⟨0, 6 * q + u + 4, 3 * q + 1, 0, 0⟩
      ⟨0, 6 * q + u + 3, 3 * q + 1, 1, 0⟩ :=
    (steps_one M570 (fire4 (6 * q + u + 3) (3 * q + 1))).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) rfl
  have s3 : Steps M570 1 ⟨0, 6 * q + u + 3, 3 * q + 1, 1, 0⟩
      ⟨3, 6 * q + u + 2, 3 * q + 1, 0, 1⟩ :=
    (steps_one M570 (fire1a (6 * q + u + 2) (3 * q + 1) 0 0)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s4 : Steps M570 (q * 4) ⟨3, 6 * q + u + 2, 3 * q + 1, 0, 1⟩
      ⟨3, 2 * q + u + 2, 1, 2 * q, 4 * q + 1⟩ :=
    (rounds q (2 * q + u + 2) 1 0 1).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s5 : Steps M570 1 ⟨3, 2 * q + u + 2, 1, 2 * q, 4 * q + 1⟩
      ⟨2, 2 * q + u + 1, 0, 2 * q + 1, 4 * q + 2⟩ :=
    (run_f0 1 2 (2 * q + u + 1) 0 (2 * q) (4 * q + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s6 : Steps M570 (2 * q + 1) ⟨2, 2 * q + u + 1, 0, 2 * q + 1, 4 * q + 2⟩
      ⟨6 * q + 5, u, 0, 0, 6 * q + 3⟩ :=
    (run_f1b (2 * q + 1) 2 u 0 (4 * q + 2)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s7 : Steps M570 (6 * q + 5) ⟨6 * q + 5, u, 0, 0, 6 * q + 3⟩
      ⟨0, 12 * q + u + 10, 0, 0, 6 * q + 3⟩ :=
    (run_f2 (6 * q + 5) 0 u (6 * q + 3)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  exact s1.comp (s2.comp (s3.comp (s4.comp (s5.comp (s6.comp s7 rfl) rfl)
    rfl) rfl) rfl) (by omega)

/-! ## The boundary family and the induction -/

/-- `Bst m = (0, 2^(m+1) + 2m, 0, 0, 2^m - 1)`; `Bst 0 = (0,2,0,0,0)`. -/
def Bst (m : Nat) : St := ⟨0, 2 ^ (m + 1) + 2 * m, 0, 0, 2 ^ m - 1⟩

/-- LEMMA 1 (entry): n = 2 -> 9 = 3², i.e. one f2 step to `Bst 0`. -/
theorem entry : Steps M570 1 ⟨1, 0, 0, 0, 0⟩ (Bst 0) := by decide

/-- LEMMA 2 at the boundary family: `Bst m -> Bst (m+1)` in `5·2^m`. -/
theorem phase_step (m : Nat) : Steps M570 (5 * 2 ^ m) (Bst m) (Bst (m + 1)) := by
  have h1 : 2 ^ (m + 1) = 2 ^ m * 2 := Nat.pow_succ 2 m
  have h2 : 2 ^ (m + 1 + 1) = 2 ^ (m + 1) * 2 := Nat.pow_succ 2 (m + 1)
  have hp := two_pow_pos m
  rcases Nat.mod_two_eq_zero_or_one m with hpar | hpar
  · -- m even: 2^m = 3c+1, so x = 2^m - 1 = 3c
    obtain ⟨t, ht⟩ : ∃ t, m = 2 * t := ⟨m / 2, by omega⟩
    obtain ⟨c, hc⟩ := two_pow_mod3 t
    have hX : 2 ^ m = 3 * c + 1 := by rw [ht, hc]
    exact (phase_even c (2 * m)).cast (by omega)
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)
  · -- m odd: 2^m = 6c+2 = 3(2c)+2, so x = 2^m - 1 = 3(2c)+1
    obtain ⟨t, ht⟩ : ∃ t, m = 2 * t + 1 := ⟨m / 2, by omega⟩
    obtain ⟨c, hc⟩ := two_pow_mod3 t
    have hps : 2 ^ (2 * t + 1) = 2 ^ (2 * t) * 2 := Nat.pow_succ 2 (2 * t)
    have hX : 2 ^ m = 3 * (2 * c) + 2 := by rw [ht, hps, hc]; omega
    exact (phase_odd (2 * c) (2 * m)).cast (by omega)
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)

/-- `T m = 5·2^m - 4` steps to `Bst m`. -/
def T : Nat → Nat
  | 0 => 1
  | m + 1 => T m + 5 * 2 ^ m

theorem reach : ∀ m, Steps M570 (T m) ⟨1, 0, 0, 0, 0⟩ (Bst m)
  | 0 => entry
  | m + 1 => (reach m).comp (phase_step m) rfl

theorem T_ge (m : Nat) : m ≤ T m := by
  induction m with
  | zero => exact Nat.zero_le 1
  | succ m ih =>
    have hp := two_pow_pos m
    show m + 1 ≤ T m + 5 * 2 ^ m
    omega

/-! ## The theorem -/

/-- THEOREM M570.  The FRACTRAN program [77/30, 88/21, 9/2, 5/11, 7/3],
    started at n = 2, never halts. -/
theorem m570_never_halts : NeverHalts M570 ⟨1, 0, 0, 0, 0⟩ :=
  neverHalts_of_unbounded fun n => ⟨T n, Bst n, T_ge n, reach n⟩

theorem orbit_never_stuck (n : Nat) (s' : St)
    (h : iter M570 n ⟨1, 0, 0, 0, 0⟩ = some s') : step M570 s' ≠ none := by
  intro hstep
  apply m570_never_halts (n + 1)
  rw [iter_add M570 n 1, h]
  show (step M570 s').bind (iter M570 0) = none
  rw [hstep]
  rfl

/-- LEMMA 3: no state on the orbit satisfies the halt criterion. -/
theorem no_halt_state_on_orbit (n : Nat) (s' : St)
    (h : iter M570 n ⟨1, 0, 0, 0, 0⟩ = some s') :
    ¬(s'.a = 0 ∧ s'.b = 0 ∧ s'.e = 0) := by
  intro hcrit
  apply orbit_never_stuck n s' h
  obtain ⟨a, b, c, d, e⟩ := s'
  exact (halt_iff a b c d e).mpr hcrit

/-! ## Ground-truth cross-check: `T 4 = 76`, the entry recorded in
m_siblings_proofs.py, lands on its boundary (0, 40, 0, 0, 15). -/

example : T 4 = 76 := by decide
set_option maxRecDepth 8192 in
example : iter M570 76 ⟨1, 0, 0, 0, 0⟩ = some ⟨0, 40, 0, 0, 15⟩ := by decide
example : Bst 4 = ⟨0, 40, 0, 0, 15⟩ := by decide

end Fractran.M570
