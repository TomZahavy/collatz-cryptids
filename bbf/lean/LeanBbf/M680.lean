/-
Machine 680 = FRACTRAN program [9/70, 44/15, 25/2, 7/55, 3/5], BBf(23)
holdout #680, in exponent-vector form over the primes (2, 3, 5, 7, 11).

    f0 = 9/70  : (v2--, v3+=2, v5--, v7--)   guard v2,v5,v7 >= 1
    f1 = 44/15 : (v2+=2, v3--, v5--, v11++)  guard v3,v5 >= 1
    f2 = 25/2  : (v2--, v5+=2)               guard v2 >= 1
    f3 = 7/55  : (v5--, v7++, v11--)         guard v5,v11 >= 1
    f4 = 3/5   : (v3++, v5--)                guard v5 >= 1

THEOREM (m680_never_halts): started from n = 2 = (1,0,0,0,0), the
program never halts.

  * boundary family  Bst m = (2^m, 0, 0, 0, 2^m - 1);
  * entry (Lemma 1): ZERO steps -- the START STATE IS Bst 0 = (1,0,0,0,0);
  * one phase (Lemma 2): f2^X, f3^(X-1), f4, f1, (f0^2 f1)^P, [f0],
    Q-blocks, T-blocks, with X = 2^m, split on X mod 3 (the parity of m);
    the Q-block word ROTATES with the parity -- (f2 f0 f1) when m is even
    (v2 pinned at 2), (f2 f1 f0) when m is odd (v2 pinned at 1);
    arriving at Bst (m+1) in exactly 6*2^m - 3 steps;
  * induction: the orbit visits every Bst m, hence never halts.

ENTRY REMARK.  m_siblings_proofs.py enters at Bst 4 after 78 steps.  The
phase lemmas below hold for all parameter values and the start state is
already the m = 0 boundary, so the formalization inducts from step 0 --
this is the last and cleanest of the nine entries (78 = `T 4`).
-/
import LeanBbf.M431

set_option linter.unusedSimpArgs false

namespace Fractran.M680

open Fractran
open Fractran.M431 (two_pow_pos two_pow_mod3)

/-! ## The rules -/

def f0 : Rule := ⟨fun s => decide (1 ≤ s.a ∧ 1 ≤ s.c ∧ 1 ≤ s.d),
                  fun s => ⟨s.a - 1, s.b + 2, s.c - 1, s.d - 1, s.e⟩⟩
def f1 : Rule := ⟨fun s => decide (1 ≤ s.b ∧ 1 ≤ s.c),
                  fun s => ⟨s.a + 2, s.b - 1, s.c - 1, s.d, s.e + 1⟩⟩
def f2 : Rule := ⟨fun s => decide (1 ≤ s.a),
                  fun s => ⟨s.a - 1, s.b, s.c + 2, s.d, s.e⟩⟩
def f3 : Rule := ⟨fun s => decide (1 ≤ s.c ∧ 1 ≤ s.e),
                  fun s => ⟨s.a, s.b, s.c - 1, s.d + 1, s.e - 1⟩⟩
def f4 : Rule := ⟨fun s => decide (1 ≤ s.c),
                  fun s => ⟨s.a, s.b + 1, s.c - 1, s.d, s.e⟩⟩

def M680 : Machine := [f0, f1, f2, f3, f4]

theorem step_M680 (a b c d e : Nat) :
    step M680 ⟨a, b, c, d, e⟩ =
      if 1 ≤ a ∧ 1 ≤ c ∧ 1 ≤ d then some ⟨a - 1, b + 2, c - 1, d - 1, e⟩
      else if 1 ≤ b ∧ 1 ≤ c then some ⟨a + 2, b - 1, c - 1, d, e + 1⟩
      else if 1 ≤ a then some ⟨a - 1, b, c + 2, d, e⟩
      else if 1 ≤ c ∧ 1 ≤ e then some ⟨a, b, c - 1, d + 1, e - 1⟩
      else if 1 ≤ c then some ⟨a, b + 1, c - 1, d, e⟩
      else none := by
  simp only [M680, step, f0, f1, f2, f3, f4, decide_eq_true_eq]

/-! ## Lemma 0: the halt criterion -/

/-- LEMMA 0.  No rule fires iff `v2 = 0` and `v5 = 0`. -/
theorem halt_iff (a b c d e : Nat) :
    step M680 ⟨a, b, c, d, e⟩ = none ↔ a = 0 ∧ c = 0 := by
  rw [step_M680]
  by_cases h0 : 1 ≤ a ∧ 1 ≤ c ∧ 1 ≤ d
  · rw [if_pos h0]; simp; omega
  · rw [if_neg h0]
    by_cases h1 : 1 ≤ b ∧ 1 ≤ c
    · rw [if_pos h1]; simp; omega
    · rw [if_neg h1]
      by_cases h2 : 1 ≤ a
      · rw [if_pos h2]; simp; omega
      · rw [if_neg h2]
        by_cases h3 : 1 ≤ c ∧ 1 ≤ e
        · rw [if_pos h3]; simp; omega
        · rw [if_neg h3]
          by_cases h4 : 1 ≤ c
          · rw [if_pos h4]; simp; omega
          · rw [if_neg h4]; simp; omega

example : step M680 ⟨0, 0, 0, 0, 0⟩ = none := by decide

/-! ## Single-firing lemmas -/

theorem fire0 (a b c d e : Nat) :
    step M680 ⟨a + 1, b, c + 1, d + 1, e⟩ = some ⟨a, b + 2, c, d, e⟩ := by
  rw [step_M680]
  rw [if_pos (by omega : 1 ≤ a + 1 ∧ 1 ≤ c + 1 ∧ 1 ≤ d + 1)]
  simp

/-- f1 with `v2 = 0` (which disables f0). -/
theorem fire1a (b c d e : Nat) :
    step M680 ⟨0, b + 1, c + 1, d, e⟩ = some ⟨2, b, c, d, e + 1⟩ := by
  rw [step_M680]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c + 1 ∧ 1 ≤ d))]
  rw [if_pos (by omega : 1 ≤ b + 1 ∧ 1 ≤ c + 1)]
  simp

/-- f1 with `v7 = 0` (which disables f0 even as v2 grows). -/
theorem fire1b (a b c e : Nat) :
    step M680 ⟨a, b + 1, c + 1, 0, e⟩ = some ⟨a + 2, b, c, 0, e + 1⟩ := by
  rw [step_M680]
  rw [if_neg (by omega : ¬(1 ≤ a ∧ 1 ≤ c + 1 ∧ 1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ b + 1 ∧ 1 ≤ c + 1)]
  simp

/-- f2 with `v5 = 0` (which disables both f0 and f1). -/
theorem fire2 (a b d e : Nat) :
    step M680 ⟨a + 1, b, 0, d, e⟩ = some ⟨a, b, 2, d, e⟩ := by
  rw [step_M680]
  rw [if_neg (by omega : ¬(1 ≤ a + 1 ∧ 1 ≤ (0:Nat) ∧ 1 ≤ d))]
  rw [if_neg (by omega : ¬(1 ≤ b ∧ 1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ a + 1)]
  simp

/-- f2 with `v3 = 0` (f1 off) and `v7 = 0` (f0 off) -- the shape used by
    the opening `f2^X` run, where v5 GROWS and so cannot be the
    disabler. -/
theorem fire2b (a c e : Nat) :
    step M680 ⟨a + 1, 0, c, 0, e⟩ = some ⟨a, 0, c + 2, 0, e⟩ := by
  rw [step_M680]
  rw [if_neg (by omega : ¬(1 ≤ a + 1 ∧ 1 ≤ c ∧ 1 ≤ (0:Nat)))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c))]
  rw [if_pos (by omega : 1 ≤ a + 1)]
  simp

/-- f3 with `v2 = 0` (f0, f2 off) and `v3 = 0` (f1 off). -/
theorem fire3 (c d e : Nat) :
    step M680 ⟨0, 0, c + 1, d, e + 1⟩ = some ⟨0, 0, c, d + 1, e⟩ := by
  rw [step_M680]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c + 1 ∧ 1 ≤ d))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c + 1))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ c + 1 ∧ 1 ≤ e + 1)]
  simp

/-- f4 at `v11 = 0` exactly: that is what stops the f3-run. -/
theorem fire4 (c d : Nat) :
    step M680 ⟨0, 0, c + 1, d, 0⟩ = some ⟨0, 1, c, d, 0⟩ := by
  rw [step_M680]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c + 1 ∧ 1 ≤ d))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c + 1))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
  rw [if_neg (by omega : ¬(1 ≤ c + 1 ∧ 1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ c + 1)]
  simp

/-! ## Single-rule runs -/

theorem run_f2 (n a c e : Nat) :
    Steps M680 n ⟨a + n, 0, c, 0, e⟩ ⟨a, 0, c + 2 * n, 0, e⟩ := by
  induction n generalizing c with
  | zero => exact steps_zero M680 _
  | succ n ih =>
    exact ((steps_one M680 (fire2b (a + n) c e)).comp (ih (c + 2)) rfl).cast
      (by omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

theorem run_f3 (n c d e : Nat) :
    Steps M680 n ⟨0, 0, c + n, d, e + n⟩ ⟨0, 0, c, d + n, e⟩ := by
  induction n generalizing d with
  | zero => exact steps_zero M680 _
  | succ n ih =>
    exact ((steps_one M680 (fire3 (c + n) d (e + n))).comp (ih (d + 1))
      rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

theorem run_f0 (n a b c d e : Nat) :
    Steps M680 n ⟨a + n, b, c + n, d + n, e⟩ ⟨a, b + 2 * n, c, d, e⟩ := by
  induction n generalizing b with
  | zero => exact steps_zero M680 _
  | succ n ih =>
    exact ((steps_one M680 (fire0 (a + n) b (c + n) (d + n) e)).comp
      (ih (b + 2)) rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-! ## The three block modes -/

/-- ROUND block `(f0^2 f1)^n`: spends 3 of v5 and 2 of v7 per round,
    builds v3, restores v2 = 2. -/
theorem rounds (n : Nat) : ∀ b c d e : Nat,
    Steps M680 (n * 3) ⟨2, b, c + 3 * n, d + 2 * n, e⟩
      ⟨2, b + 3 * n, c, d, e + n⟩ := by
  induction n with
  | zero => intro b c d e; exact steps_zero M680 _
  | succ n ih =>
    intro b c d e
    exact ((run_f0 2 0 b (c + 3 * n + 1) (d + 2 * n) e).comp
      ((steps_one M680 (fire1a (b + 3) (c + 3 * n) (d + 2 * n) e)).comp
        (ih (b + 3) c d (e + 1)) rfl) rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- Q block, EVEN parity: `(f2 f0 f1)^n` with v2 pinned at 2. -/
theorem qblockE (n : Nat) : ∀ b d e : Nat,
    Steps M680 (n * 3) ⟨2, b, 0, d + n, e⟩ ⟨2, b + n, 0, d, e + n⟩ := by
  induction n with
  | zero => intro b d e; exact steps_zero M680 _
  | succ n ih =>
    intro b d e
    exact ((steps_one M680 (fire2 1 b (d + n + 1) e)).comp
      ((steps_one M680 (fire0 0 b 1 (d + n) e)).comp
        ((steps_one M680 (fire1a (b + 1) 0 (d + n) e)).comp
          (ih (b + 1) d (e + 1)) rfl) rfl) rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- Q block, ODD parity: `(f2 f1 f0)^n` with v2 pinned at 1 — the
    ROTATED word.  It is the rotation, not a relabelling, that makes 680
    a template of its own (cf. the decider's non-isomorphism verdict). -/
theorem qblockO (n : Nat) : ∀ b d e : Nat,
    Steps M680 (n * 3) ⟨1, b + 1, 0, d + n, e⟩
      ⟨1, b + 1 + n, 0, d, e + n⟩ := by
  induction n with
  | zero => intro b d e; exact steps_zero M680 _
  | succ n ih =>
    intro b d e
    exact ((steps_one M680 (fire2 0 (b + 1) (d + n + 1) e)).comp
      ((steps_one M680 (fire1a b 1 (d + n + 1) e)).comp
        ((steps_one M680 (fire0 1 b 0 (d + n) (e + 1))).comp
          (ih (b + 1) d (e + 1)) rfl) rfl) rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- T block `(f2 f1^2)^n`: v7 = 0 keeps f0 dead, so each block converts
    two of v3 into three of v2 and two of v11. -/
theorem tblock (n : Nat) : ∀ a b e : Nat,
    Steps M680 (n * 3) ⟨a + 1, b + 2 * n, 0, 0, e⟩
      ⟨a + 1 + 3 * n, b, 0, 0, e + 2 * n⟩ := by
  induction n with
  | zero => intro a b e; exact steps_zero M680 _
  | succ n ih =>
    intro a b e
    exact ((steps_one M680 (fire2 a (b + 2 * n + 2) 0 e)).comp
      ((steps_one M680 (fire1b a (b + 2 * n + 1) 1 e)).comp
        ((steps_one M680 (fire1b (a + 2) (b + 2 * n) 0 (e + 1))).comp
          (ih (a + 3) b (e + 2)) rfl) rfl) rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-! ## Lemma 2: one full phase -/

/-- Even case: `X = 3P + 1`. -/
theorem phase_even (P : Nat) :
    Steps M680 (18 * P + 3) ⟨3 * P + 1, 0, 0, 0, 3 * P⟩
      ⟨6 * P + 2, 0, 0, 0, 6 * P + 1⟩ := by
  have s1 : Steps M680 (3 * P + 1) ⟨3 * P + 1, 0, 0, 0, 3 * P⟩
      ⟨0, 0, 6 * P + 2, 0, 3 * P⟩ :=
    (run_f2 (3 * P + 1) 0 0 (3 * P)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s2 : Steps M680 (3 * P) ⟨0, 0, 6 * P + 2, 0, 3 * P⟩
      ⟨0, 0, 3 * P + 2, 3 * P, 0⟩ :=
    (run_f3 (3 * P) (3 * P + 2) 0 0).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s3 : Steps M680 1 ⟨0, 0, 3 * P + 2, 3 * P, 0⟩
      ⟨0, 1, 3 * P + 1, 3 * P, 0⟩ :=
    (steps_one M680 (fire4 (3 * P + 1) (3 * P))).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) rfl
  have s4 : Steps M680 1 ⟨0, 1, 3 * P + 1, 3 * P, 0⟩
      ⟨2, 0, 3 * P, 3 * P, 1⟩ :=
    (steps_one M680 (fire1a 0 (3 * P) (3 * P) 0)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) rfl
  have s5 : Steps M680 (P * 3) ⟨2, 0, 3 * P, 3 * P, 1⟩
      ⟨2, 3 * P, 0, P, P + 1⟩ :=
    (rounds P 0 0 P 1).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s6 : Steps M680 (P * 3) ⟨2, 3 * P, 0, P, P + 1⟩
      ⟨2, 4 * P, 0, 0, 2 * P + 1⟩ :=
    (qblockE P (3 * P) 0 (P + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s7 : Steps M680 (2 * P * 3) ⟨2, 4 * P, 0, 0, 2 * P + 1⟩
      ⟨6 * P + 2, 0, 0, 0, 6 * P + 1⟩ :=
    (tblock (2 * P) 1 0 (2 * P + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  exact s1.comp (s2.comp (s3.comp (s4.comp (s5.comp (s6.comp s7 rfl) rfl)
    rfl) rfl) rfl) (by omega)

/-- Odd case: `X = 3P + 2`; one extra `f0` and the ROTATED Q-block. -/
theorem phase_odd (P : Nat) :
    Steps M680 (18 * P + 9) ⟨3 * P + 2, 0, 0, 0, 3 * P + 1⟩
      ⟨6 * P + 4, 0, 0, 0, 6 * P + 3⟩ := by
  have s1 : Steps M680 (3 * P + 2) ⟨3 * P + 2, 0, 0, 0, 3 * P + 1⟩
      ⟨0, 0, 6 * P + 4, 0, 3 * P + 1⟩ :=
    (run_f2 (3 * P + 2) 0 0 (3 * P + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s2 : Steps M680 (3 * P + 1) ⟨0, 0, 6 * P + 4, 0, 3 * P + 1⟩
      ⟨0, 0, 3 * P + 3, 3 * P + 1, 0⟩ :=
    (run_f3 (3 * P + 1) (3 * P + 3) 0 0).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s3 : Steps M680 1 ⟨0, 0, 3 * P + 3, 3 * P + 1, 0⟩
      ⟨0, 1, 3 * P + 2, 3 * P + 1, 0⟩ :=
    (steps_one M680 (fire4 (3 * P + 2) (3 * P + 1))).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) rfl
  have s4 : Steps M680 1 ⟨0, 1, 3 * P + 2, 3 * P + 1, 0⟩
      ⟨2, 0, 3 * P + 1, 3 * P + 1, 1⟩ :=
    (steps_one M680 (fire1a 0 (3 * P + 1) (3 * P + 1) 0)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega) rfl
  have s5 : Steps M680 (P * 3) ⟨2, 0, 3 * P + 1, 3 * P + 1, 1⟩
      ⟨2, 3 * P, 1, P + 1, P + 1⟩ :=
    (rounds P 0 1 (P + 1) 1).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s6 : Steps M680 1 ⟨2, 3 * P, 1, P + 1, P + 1⟩
      ⟨1, 3 * P + 2, 0, P, P + 1⟩ :=
    (run_f0 1 1 (3 * P) 0 P (P + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s7 : Steps M680 (P * 3) ⟨1, 3 * P + 2, 0, P, P + 1⟩
      ⟨1, 4 * P + 2, 0, 0, 2 * P + 1⟩ :=
    (qblockO P (3 * P + 1) 0 (P + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  have s8 : Steps M680 ((2 * P + 1) * 3) ⟨1, 4 * P + 2, 0, 0, 2 * P + 1⟩
      ⟨6 * P + 4, 0, 0, 0, 6 * P + 3⟩ :=
    (tblock (2 * P + 1) 0 0 (2 * P + 1)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  exact s1.comp (s2.comp (s3.comp (s4.comp (s5.comp (s6.comp (s7.comp s8 rfl)
    rfl) rfl) rfl) rfl) rfl) (by omega)

/-! ## The boundary family and the induction -/

/-- `Bst m = (2^m, 0, 0, 0, 2^m - 1)`; `Bst 0 = (1,0,0,0,0)` IS the
    start state, so the entry costs zero steps. -/
def Bst (m : Nat) : St := ⟨2 ^ m, 0, 0, 0, 2 ^ m - 1⟩

/-- LEMMA 1 (entry): the start state is already the m = 0 boundary. -/
theorem entry : Steps M680 0 ⟨1, 0, 0, 0, 0⟩ (Bst 0) := by decide

/-- LEMMA 2 at the boundary family: `Bst m -> Bst (m+1)` in
    `6·2^m - 3` steps. -/
theorem phase_step (m : Nat) :
    Steps M680 (6 * 2 ^ m - 3) (Bst m) (Bst (m + 1)) := by
  have h1 : 2 ^ (m + 1) = 2 ^ m * 2 := Nat.pow_succ 2 m
  have hp := two_pow_pos m
  rcases Nat.mod_two_eq_zero_or_one m with hpar | hpar
  · obtain ⟨t, ht⟩ : ∃ t, m = 2 * t := ⟨m / 2, by omega⟩
    obtain ⟨c, hc⟩ := two_pow_mod3 t
    have hX : 2 ^ m = 3 * c + 1 := by rw [ht, hc]
    exact (phase_even c).cast (by omega)
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)
  · obtain ⟨t, ht⟩ : ∃ t, m = 2 * t + 1 := ⟨m / 2, by omega⟩
    obtain ⟨c, hc⟩ := two_pow_mod3 t
    have hps : 2 ^ (2 * t + 1) = 2 ^ (2 * t) * 2 := Nat.pow_succ 2 (2 * t)
    have hX : 2 ^ m = 3 * (2 * c) + 2 := by rw [ht, hps, hc]; omega
    exact (phase_odd (2 * c)).cast (by omega)
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)

/-- `T m = 6·2^m - 3m - 6` steps to `Bst m`; `T 0 = 0`. -/
def T : Nat → Nat
  | 0 => 0
  | m + 1 => T m + (6 * 2 ^ m - 3)

theorem reach : ∀ m, Steps M680 (T m) ⟨1, 0, 0, 0, 0⟩ (Bst m)
  | 0 => entry
  | m + 1 => (reach m).comp (phase_step m) rfl

theorem T_ge (m : Nat) : m ≤ T m := by
  induction m with
  | zero => exact Nat.le_refl 0
  | succ m ih =>
    have hp := two_pow_pos m
    show m + 1 ≤ T m + (6 * 2 ^ m - 3)
    omega

/-! ## The theorem -/

/-- THEOREM M680.  The FRACTRAN program [9/70, 44/15, 25/2, 7/55, 3/5],
    started at n = 2, never halts. -/
theorem m680_never_halts : NeverHalts M680 ⟨1, 0, 0, 0, 0⟩ :=
  neverHalts_of_unbounded fun n => ⟨T n, Bst n, T_ge n, reach n⟩

theorem orbit_never_stuck (n : Nat) (s' : St)
    (h : iter M680 n ⟨1, 0, 0, 0, 0⟩ = some s') : step M680 s' ≠ none := by
  intro hstep
  apply m680_never_halts (n + 1)
  rw [iter_add M680 n 1, h]
  show (step M680 s').bind (iter M680 0) = none
  rw [hstep]
  rfl

/-- LEMMA 3: no state on the orbit satisfies the halt criterion. -/
theorem no_halt_state_on_orbit (n : Nat) (s' : St)
    (h : iter M680 n ⟨1, 0, 0, 0, 0⟩ = some s') : ¬(s'.a = 0 ∧ s'.c = 0) := by
  intro hcrit
  apply orbit_never_stuck n s' h
  obtain ⟨a, b, c, d, e⟩ := s'
  exact (halt_iff a b c d e).mpr hcrit

/-! ## Ground-truth cross-check: `T 4 = 78`, the entry step count
recorded in m_siblings_proofs.py, lands on its boundary (16,0,0,0,15). -/

example : T 4 = 78 := by decide
set_option maxRecDepth 8192 in
example : iter M680 78 ⟨1, 0, 0, 0, 0⟩ = some ⟨16, 0, 0, 0, 15⟩ := by decide
example : Bst 4 = ⟨16, 0, 0, 0, 15⟩ := by decide

end Fractran.M680
