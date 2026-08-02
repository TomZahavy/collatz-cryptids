/-
Machine 431 = FRACTRAN program [5/6, 9/35, 8/55, 7/2, 605/7], BBf(23)
holdout #431, in exponent-vector form over the primes (2, 3, 5, 7, 11).

    f0 = 5/6    : (v2--, v3--, v5++)      guard v2>=1 & v3>=1
    f1 = 9/35   : (v3+=2, v5--, v7--)     guard v5>=1 & v7>=1
    f2 = 8/55   : (v2+=3, v5--, v11--)    guard v5>=1 & v11>=1
    f3 = 7/2    : (v2--, v7++)            guard v2>=1
    f4 = 605/7  : (v5++, v7--, v11+=2)    guard v7>=1

THEOREM (m431_never_halts): started from n = 2 = (1,0,0,0,0), the
program never halts.

Proof skeleton (mirrors m431_proof.py):
  * boundary family  B_i = (2^(i+1)-1, 0, 0, 0, i),  B_0 = the start;
  * one phase (Lemma 2): from B_i the machine performs
      f3^W, (f4 f1)^m, f4, f2, then (f0^3 f2)^q and a trailing f2-run
      (i even, 2m = 3q) or (f0^3 f2)^q, f0^2, f2-run (i odd, 2m = 3q+2),
    where W = 2m+1, m = 2^i - 1, arriving at B_{i+1} in 8m+3 steps;
  * induction: the orbit visits every B_i, so it survives >= i steps for
    every i, i.e. it never halts.  (The i = 0 phase IS the entry
    n = 2 -> B_1 of Lemma 1: f3 f4 f2.)
-/
import LeanBbf.Fractran

/- The state-cast tactic `simp only [St.mk.injEq, ...] <;> omega` is used
   mechanically; on some goals simp already closes everything by rfl and
   the listed lemmas go unused, which is fine. -/
set_option linter.unusedSimpArgs false

namespace Fractran.M431

open Fractran

/-! ## The rules (DELTA/GUARD tables of m431_proof.py, priority order) -/

def f0 : Rule := ⟨fun s => decide (1 ≤ s.a ∧ 1 ≤ s.b),
                  fun s => ⟨s.a - 1, s.b - 1, s.c + 1, s.d, s.e⟩⟩
def f1 : Rule := ⟨fun s => decide (1 ≤ s.c ∧ 1 ≤ s.d),
                  fun s => ⟨s.a, s.b + 2, s.c - 1, s.d - 1, s.e⟩⟩
def f2 : Rule := ⟨fun s => decide (1 ≤ s.c ∧ 1 ≤ s.e),
                  fun s => ⟨s.a + 3, s.b, s.c - 1, s.d, s.e - 1⟩⟩
def f3 : Rule := ⟨fun s => decide (1 ≤ s.a),
                  fun s => ⟨s.a - 1, s.b, s.c, s.d + 1, s.e⟩⟩
def f4 : Rule := ⟨fun s => decide (1 ≤ s.d),
                  fun s => ⟨s.a, s.b, s.c + 1, s.d - 1, s.e + 2⟩⟩

def M431 : Machine := [f0, f1, f2, f3, f4]

/-- The priority step function of machine 431 in closed form. -/
theorem step_M431 (a b c d e : Nat) :
    step M431 ⟨a, b, c, d, e⟩ =
      if 1 ≤ a ∧ 1 ≤ b then some ⟨a - 1, b - 1, c + 1, d, e⟩
      else if 1 ≤ c ∧ 1 ≤ d then some ⟨a, b + 2, c - 1, d - 1, e⟩
      else if 1 ≤ c ∧ 1 ≤ e then some ⟨a + 3, b, c - 1, d, e - 1⟩
      else if 1 ≤ a then some ⟨a - 1, b, c, d + 1, e⟩
      else if 1 ≤ d then some ⟨a, b, c + 1, d - 1, e + 2⟩
      else none := by
  simp only [M431, step, f0, f1, f2, f3, f4, decide_eq_true_eq]

/-! ## Lemma 0: the halt criterion -/

/-- LEMMA 0.  No rule fires iff `v2 = 0`, `v7 = 0` and (`v5 = 0` or
    `v11 = 0`). -/
theorem halt_iff (a b c d e : Nat) :
    step M431 ⟨a, b, c, d, e⟩ = none ↔
      a = 0 ∧ d = 0 ∧ (c = 0 ∨ e = 0) := by
  rw [step_M431]
  by_cases h0 : 1 ≤ a ∧ 1 ≤ b
  · rw [if_pos h0]; simp; omega
  · rw [if_neg h0]
    by_cases h1 : 1 ≤ c ∧ 1 ≤ d
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

/-- The machine is not degenerate: it CAN halt (from the zero vector). -/
example : step M431 ⟨0, 0, 0, 0, 0⟩ = none := by decide

/-! ## Single-firing lemmas

One lemma per rule, in "successor pattern" form: the hypotheses of the
guard and the FAILURE of every higher-priority guard are baked into the
shape of the state, so each lemma is hypothesis-free and `omega`-ready.
`fire2` needs two shapes (v2 = 0, or v3 = 0 with v2 arbitrary), matching
the two priority situations in which rule 2 actually fires. -/

theorem fire0 (a b c d e : Nat) :
    step M431 ⟨a + 1, b + 1, c, d, e⟩ = some ⟨a, b, c + 1, d, e⟩ := by
  rw [step_M431]
  rw [if_pos (by omega : 1 ≤ a + 1 ∧ 1 ≤ b + 1)]
  simp

theorem fire1 (b c d e : Nat) :
    step M431 ⟨0, b, c + 1, d + 1, e⟩ = some ⟨0, b + 2, c, d, e⟩ := by
  rw [step_M431]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ b))]
  rw [if_pos (by omega : 1 ≤ c + 1 ∧ 1 ≤ d + 1)]
  simp

theorem fire2a (b c e : Nat) :
    step M431 ⟨0, b, c + 1, 0, e + 1⟩ = some ⟨3, b, c, 0, e⟩ := by
  rw [step_M431]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ b))]
  rw [if_neg (by omega : ¬(1 ≤ c + 1 ∧ 1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ c + 1 ∧ 1 ≤ e + 1)]
  simp

theorem fire2b (a c e : Nat) :
    step M431 ⟨a, 0, c + 1, 0, e + 1⟩ = some ⟨a + 3, 0, c, 0, e⟩ := by
  rw [step_M431]
  rw [if_neg (by omega : ¬(1 ≤ a ∧ 1 ≤ (0:Nat)))]
  rw [if_neg (by omega : ¬(1 ≤ c + 1 ∧ 1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ c + 1 ∧ 1 ≤ e + 1)]
  simp

theorem fire3 (a d e : Nat) :
    step M431 ⟨a + 1, 0, 0, d, e⟩ = some ⟨a, 0, 0, d + 1, e⟩ := by
  rw [step_M431]
  rw [if_neg (by omega : ¬(1 ≤ a + 1 ∧ 1 ≤ (0:Nat)))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ d))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ e))]
  rw [if_pos (by omega : 1 ≤ a + 1)]
  simp

theorem fire4 (b d e : Nat) :
    step M431 ⟨0, b, 0, d + 1, e⟩ = some ⟨0, b, 1, d, e + 2⟩ := by
  rw [step_M431]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ b))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ d + 1))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ e))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ d + 1)]
  simp

/-! ## Lemma 1: the entry

From n = 2 the run begins f3, f4, f2 and reaches B_1 = (3,0,0,0,1) at
step 3.  (This is also the i = 0 instance of the phase lemma below.) -/

theorem entry : Steps M431 3 ⟨1, 0, 0, 0, 0⟩ ⟨3, 0, 0, 0, 1⟩ := by decide

/-! ## Single-rule runs (affine in the run counter)

Each of these is the affine run lemma instantiated at one rule: the
state after `t` firings is affine in `t`, and the guard/priority side
conditions are linear in `t`, discharged by `omega` for ALL `t` at once
(the endpoint principle `Fractran.affine_nonneg_of_endpoints` /
`affine_le_of_endpoints` in general form).  Proved by induction on the
run length, peeling one firing in front. -/

/-- `f3^k`: drains v2 into v7 (needs v3 = v5 = 0, which disables
    f0, f1, f2 throughout). -/
theorem run_f3 (k x d e : Nat) :
    Steps M431 k ⟨x + k, 0, 0, d, e⟩ ⟨x, 0, 0, d + k, e⟩ := by
  induction k generalizing d with
  | zero => exact steps_zero M431 _
  | succ k ih =>
    exact ((steps_one M431 (fire3 (x + k) d e)).comp (ih (d + 1))
      rfl).cast (by omega) rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- `f0^k`: top priority, drains v2 and v3 together into v5. -/
theorem run_f0 (k x y c d e : Nat) :
    Steps M431 k ⟨x + k, y + k, c, d, e⟩ ⟨x, y, c + k, d, e⟩ := by
  induction k generalizing c with
  | zero => exact steps_zero M431 _
  | succ k ih =>
    exact ((steps_one M431 (fire0 (x + k) (y + k) c d e)).comp (ih (c + 1))
      rfl).cast (by omega) rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- `f2^k`: drains v5 (and v11), pays out 3 to v2 per firing; needs
    v3 = 0 (disables f0) and v7 = 0 (disables f1). -/
theorem run_f2 (k a x y : Nat) :
    Steps M431 k ⟨a, 0, x + k, 0, y + k⟩ ⟨a + 3 * k, 0, x, 0, y⟩ := by
  induction k generalizing a with
  | zero => exact steps_zero M431 _
  | succ k ih =>
    exact ((steps_one M431 (fire2b a (x + k) (y + k))).comp (ih (a + 3))
      rfl).cast (by omega) rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-! ## The two repeated blocks (start state affine in the block index) -/

/-- Stage 2 block: `(f4 f1)^n`.  From (0, b, 0, d + 2n, e) each pair
    f4, f1 converts two units of v7 into two of v3 and two of v11. -/
theorem stage2 (n : Nat) : ∀ b e : Nat, ∀ d : Nat,
    Steps M431 (n * 2) ⟨0, b, 0, d + 2 * n, e⟩ ⟨0, b + 2 * n, 0, d, e + 2 * n⟩ := by
  induction n with
  | zero => intro b e d; exact steps_zero M431 _
  | succ n ih =>
    intro b e d
    exact ((steps_one M431 (fire4 b (d + 2 * n + 1) e)).comp
      ((steps_one M431 (fire1 b 0 (d + 2 * n) (e + 2))).comp
        (ih (b + 2) (e + 2) d) rfl)
      rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- Stage 4 block: `(f0^3 f2)^n`.  From (3, y + 3n, c, 0, e + n) each
    round trades three units of v3 and one of v11 for two of v5,
    restoring v2 = 3. -/
theorem stage4 (n : Nat) : ∀ y e : Nat, ∀ c : Nat,
    Steps M431 (n * 4) ⟨3, y + 3 * n, c, 0, e + n⟩ ⟨3, y, c + 2 * n, 0, e⟩ := by
  induction n with
  | zero => intro y e c; exact steps_zero M431 _
  | succ n ih =>
    intro y e c
    exact ((run_f0 3 0 (y + 3 * n) c 0 (e + (n + 1))).comp
      ((steps_one M431 (fire2a (y + 3 * n) (c + 2) (e + n))).comp
        (ih y e (c + 2)) rfl)
      rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-! ## Lemma 2: one full phase

From B_i = (2m+1, 0, 0, 0, i) with m = 2^i - 1 the machine reaches
B_{i+1} = (4m+3, 0, 0, 0, i+1) in exactly 8m+3 = 2^(i+3) - 5 steps.
Stated over an ABSTRACT m with the two possible residues of 2m mod 3 as
a hypothesis (2m = 3q for i even, 2m = 3q + 2 for i odd), which makes
every side condition linear, i.e. `omega`-decidable. -/

/-- One phase, even case (2m ≡ 0 mod 3, i.e. i even).  The word is
    f3^(2m+1), (f4 f1)^m, f4, f2, (f0^3 f2)^q, f2^(2q). -/
theorem phase_even (i m q : Nat) (hq : 2 * m = 3 * q) :
    Steps M431 (8 * m + 3) ⟨2 * m + 1, 0, 0, 0, i⟩ ⟨4 * m + 3, 0, 0, 0, i + 1⟩ := by
  -- Stage 1: f3^(2m+1) : (2m+1,0,0,0,i) -> (0,0,0,2m+1,i)
  have s1 : Steps M431 (2 * m + 1) ⟨2 * m + 1, 0, 0, 0, i⟩ ⟨0, 0, 0, 2 * m + 1, i⟩ :=
    (run_f3 (2 * m + 1) 0 0 i).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- Stage 2: (f4 f1)^m : -> (0, 2m, 0, 1, i+2m)
  have s2 : Steps M431 (m * 2) ⟨0, 0, 0, 2 * m + 1, i⟩ ⟨0, 2 * m, 0, 1, i + 2 * m⟩ :=
    (stage2 m 0 i 1).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- trailing f4 : -> (0, 2m, 1, 0, i+2m+2)
  have s3 : Steps M431 1 ⟨0, 2 * m, 0, 1, i + 2 * m⟩ ⟨0, 2 * m, 1, 0, i + 2 * m + 2⟩ :=
    (steps_one M431 (fire4 (2 * m) 0 (i + 2 * m))).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- Stage 3: f2 : -> (3, 2m, 0, 0, i+2m+1)
  have s4 : Steps M431 1 ⟨0, 2 * m, 1, 0, i + 2 * m + 2⟩ ⟨3, 2 * m, 0, 0, i + 2 * m + 1⟩ :=
    (steps_one M431 (fire2a (2 * m) 0 (i + 2 * m + 1))).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- Stage 4 rounds: (f0^3 f2)^q : -> (3, 0, 2q, 0, i+2q+1)
  have s5 : Steps M431 (q * 4) ⟨3, 2 * m, 0, 0, i + 2 * m + 1⟩ ⟨3, 0, 2 * q, 0, i + 2 * q + 1⟩ :=
    (stage4 q 0 (i + 2 * q + 1) 0).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- Stage 4 drain: f2^(2q) : -> (3+6q, 0, 0, 0, i+1) = (4m+3, 0, 0, 0, i+1)
  have s6 : Steps M431 (2 * q) ⟨3, 0, 2 * q, 0, i + 2 * q + 1⟩ ⟨3 + 6 * q, 0, 0, 0, i + 1⟩ :=
    (run_f2 (2 * q) 3 0 (i + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  exact (s1.comp (s2.comp (s3.comp (s4.comp (s5.comp s6 rfl) rfl) rfl) rfl)
    (by omega)).cast rfl rfl (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- One phase, odd case (2m ≡ 2 mod 3, i.e. i odd).  The word is
    f3^(2m+1), (f4 f1)^m, f4, f2, (f0^3 f2)^q, f0^2, f2^(2q+2). -/
theorem phase_odd (i m q : Nat) (hq : 2 * m = 3 * q + 2) :
    Steps M431 (8 * m + 3) ⟨2 * m + 1, 0, 0, 0, i⟩ ⟨4 * m + 3, 0, 0, 0, i + 1⟩ := by
  have s1 : Steps M431 (2 * m + 1) ⟨2 * m + 1, 0, 0, 0, i⟩ ⟨0, 0, 0, 2 * m + 1, i⟩ :=
    (run_f3 (2 * m + 1) 0 0 i).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s2 : Steps M431 (m * 2) ⟨0, 0, 0, 2 * m + 1, i⟩ ⟨0, 2 * m, 0, 1, i + 2 * m⟩ :=
    (stage2 m 0 i 1).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s3 : Steps M431 1 ⟨0, 2 * m, 0, 1, i + 2 * m⟩ ⟨0, 2 * m, 1, 0, i + 2 * m + 2⟩ :=
    (steps_one M431 (fire4 (2 * m) 0 (i + 2 * m))).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s4 : Steps M431 1 ⟨0, 2 * m, 1, 0, i + 2 * m + 2⟩ ⟨3, 2 * m, 0, 0, i + 2 * m + 1⟩ :=
    (steps_one M431 (fire2a (2 * m) 0 (i + 2 * m + 1))).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- rounds leave v3 = 2 this time: -> (3, 2, 2q, 0, i+2q+3)
  have s5 : Steps M431 (q * 4) ⟨3, 2 * m, 0, 0, i + 2 * m + 1⟩ ⟨3, 2, 2 * q, 0, i + 2 * q + 3⟩ :=
    (stage4 q 2 (i + 2 * q + 3) 0).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- f0^2 : -> (1, 0, 2q+2, 0, i+2q+3)
  have s6 : Steps M431 2 ⟨3, 2, 2 * q, 0, i + 2 * q + 3⟩ ⟨1, 0, 2 * q + 2, 0, i + 2 * q + 3⟩ :=
    (run_f0 2 1 0 (2 * q) 0 (i + 2 * q + 3)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- f2^(2q+2) : -> (6q+7, 0, 0, 0, i+1) = (4m+3, 0, 0, 0, i+1)
  have s7 : Steps M431 (2 * q + 2) ⟨1, 0, 2 * q + 2, 0, i + 2 * q + 3⟩
      ⟨1 + 3 * (2 * q + 2), 0, 0, 0, i + 1⟩ :=
    (run_f2 (2 * q + 2) 1 0 (i + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  exact (s1.comp (s2.comp (s3.comp (s4.comp (s5.comp (s6.comp s7 rfl) rfl) rfl) rfl) rfl)
    (by omega)).cast rfl rfl (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-! ## Powers of two: the three arithmetic facts the induction needs -/

theorem two_pow_pos (i : Nat) : 1 ≤ 2 ^ i := by
  induction i with
  | zero => decide
  | succ i ih => rw [Nat.pow_succ]; omega

/-- 4^t ≡ 1 (mod 3), in existential form. -/
theorem two_pow_mod3 (t : Nat) : ∃ c, 2 ^ (2 * t) = 3 * c + 1 := by
  induction t with
  | zero => exact ⟨0, by decide⟩
  | succ t ih =>
    obtain ⟨c, hc⟩ := ih
    have he : 2 * (t + 1) = 2 * t + 1 + 1 := by omega
    exact ⟨4 * c + 1, by rw [he, Nat.pow_succ, Nat.pow_succ, hc]; omega⟩

/-! ## The boundary family and the induction -/

/-- The phase-i boundary state B_i = (2^(i+1)-1, 0, 0, 0, i).
    B_0 = (1,0,0,0,0) is the start state n = 2. -/
def Bst (i : Nat) : St := ⟨2 ^ (i + 1) - 1, 0, 0, 0, i⟩

/-- LEMMA 2 at the boundary family: B_i -> B_{i+1} in 2^(i+3)-5 steps. -/
theorem phase_step (i : Nat) :
    Steps M431 (8 * 2 ^ i - 5) (Bst i) (Bst (i + 1)) := by
  have hp := two_pow_pos i
  have h1 : 2 ^ (i + 1) = 2 ^ i * 2 := Nat.pow_succ 2 i
  have h2 : 2 ^ (i + 2) = 2 ^ i * 2 * 2 := by
    rw [Nat.pow_succ, Nat.pow_succ]
  rcases Nat.mod_two_eq_zero_or_one i with hpar | hpar
  · -- i even: 2m = 3q with q = 2c, where 2^i = 3c+1
    obtain ⟨t, ht⟩ : ∃ t, i = 2 * t := ⟨i / 2, by omega⟩
    obtain ⟨c, hc⟩ := two_pow_mod3 t
    have hm : 2 * (2 ^ i - 1) = 3 * (2 * c) := by rw [ht, hc]; omega
    exact (phase_even i (2 ^ i - 1) (2 * c) hm).cast (by omega)
      (by simp only [Bst, St.mk.injEq, and_true] <;> omega)
      (by simp only [Bst, St.mk.injEq, and_true] <;> omega)
  · -- i odd: 2m = 3q + 2 with q = 4c, where 2^(i-1) = 3c+1
    obtain ⟨t, ht⟩ : ∃ t, i = 2 * t + 1 := ⟨i / 2, by omega⟩
    obtain ⟨c, hc⟩ := two_pow_mod3 t
    have hps : 2 ^ (2 * t + 1) = 2 ^ (2 * t) * 2 := Nat.pow_succ 2 (2 * t)
    have hm : 2 * (2 ^ i - 1) = 3 * (4 * c) + 2 := by
      rw [ht, hps, hc]; omega
    exact (phase_odd i (2 ^ i - 1) (4 * c) hm).cast (by omega)
      (by simp only [Bst, St.mk.injEq, and_true] <;> omega)
      (by simp only [Bst, St.mk.injEq, and_true] <;> omega)

/-- Total step count to reach B_i (S 1 = 3 is the entry;
    S (i+1) - S i = 2^(i+3) - 5 is the phase length). -/
def S : Nat → Nat
  | 0 => 0
  | i + 1 => S i + (8 * 2 ^ i - 5)

/-- THE ORBIT VISITS EVERY BOUNDARY: from n = 2, after exactly S i
    steps the machine is at B_i — for every i. -/
theorem reaches_Bst : ∀ i, Steps M431 (S i) ⟨1, 0, 0, 0, 0⟩ (Bst i)
  | 0 => steps_zero M431 _
  | i + 1 => (reaches_Bst i).comp (phase_step i) rfl

theorem S_ge (i : Nat) : i ≤ S i := by
  induction i with
  | zero => exact Nat.le_refl 0
  | succ i ih =>
    have hp := two_pow_pos i
    show i + 1 ≤ S i + (8 * 2 ^ i - 5)
    omega

/-! ## The theorem -/

/-- THEOREM M431.  The FRACTRAN program [5/6, 9/35, 8/55, 7/2, 605/7],
    started at n = 2 (exponent vector (1,0,0,0,0)), never halts. -/
theorem m431_never_halts : NeverHalts M431 ⟨1, 0, 0, 0, 0⟩ :=
  neverHalts_of_unbounded fun n => ⟨S n, Bst n, S_ge n, reaches_Bst n⟩

/-! ## Lemma 3, explicit form -/

/-- Every state visited on the orbit has a successor. -/
theorem orbit_never_stuck (n : Nat) (s' : St)
    (h : iter M431 n ⟨1, 0, 0, 0, 0⟩ = some s') : step M431 s' ≠ none := by
  intro hstep
  apply m431_never_halts (n + 1)
  rw [iter_add M431 n 1, h]
  show (step M431 s').bind (iter M431 0) = none
  rw [hstep]
  rfl

/-- LEMMA 3: no state on the orbit satisfies the halt criterion of
    Lemma 0. -/
theorem no_halt_state_on_orbit (n : Nat) (s' : St)
    (h : iter M431 n ⟨1, 0, 0, 0, 0⟩ = some s') :
    ¬(s'.a = 0 ∧ s'.d = 0 ∧ (s'.c = 0 ∨ s'.e = 0)) := by
  intro hcrit
  apply orbit_never_stuck n s' h
  obtain ⟨a, b, c, d, e⟩ := s'
  exact (halt_iff a b c d e).mpr hcrit

/-! ## Ground-truth cross-checks (independent of the lemmas above) -/

-- five phases simulated concretely: 223 = S 5 steps land exactly on
-- B_5 = (2^6 - 1, 0, 0, 0, 5)
example : S 5 = 223 := by decide
example : iter M431 223 ⟨1, 0, 0, 0, 0⟩ = some ⟨63, 0, 0, 0, 5⟩ := by decide
example : Bst 5 = ⟨63, 0, 0, 0, 5⟩ := by decide

end Fractran.M431
