/-
Machine 574 = FRACTRAN program [8/15, 147/22, 35/2, 11/49, 3/7], BBf(23)
holdout #574, in exponent-vector form over the primes (2, 3, 5, 7, 11).

    f0 = 8/15   : (v2+=3, v3--, v5--)        guard v3>=1 & v5>=1
    f1 = 147/22 : (v2--, v3++, v7+=2, v11--) guard v2>=1 & v11>=1
    f2 = 35/2   : (v2--, v5++, v7++)         guard v2>=1
    f3 = 11/49  : (v7-=2, v11++)             guard v7>=2      (threshold 2!)
    f4 = 3/7    : (v3++, v7--)               guard v7>=1

THEOREM (m574_never_halts): started from n = 2 = (1,0,0,0,0), the
program never halts.

Proof skeleton (the phase word of m_siblings_proofs.py `walk_574`, but
re-indexed -- see the entry remark):
  * boundary family  Bst k = (0, 0, 2^k + k, 2^(k+1) - 1, 0);
  * entry (Lemma 1): ONE step (f2) reaches Bst 0 = (0,0,1,1,0);
  * one phase (Lemma 2): from Bst k the machine performs
      f3^w, f4, (f0 f1)^w, f0, f2^(2w+3)   with w + 1 = 2^k,
    arriving at Bst (k+1) in exactly 5*2^k steps.  There is NO parity
    case split -- 574 is the only one of the nine with a single-branch
    phase;
  * induction: the orbit visits every Bst k, hence never halts.

ENTRY REMARK.  m_siblings_proofs.py and decider.py state 574's boundary
for k >= 4 and enter after 36 steps at (0,0,11,15,0).  The phase lemma
below is proved for ALL parameter values, and the machine's very first
step already lands on the k = 0 boundary (n = 2 -> 35 = 5*7), so the
formalization inducts from step 1.  (Same phenomenon as M678's B_1
improvement.)  36 = the old entry is recovered as Steps to Bst 3.
-/
import LeanBbf.M431

set_option linter.unusedSimpArgs false

namespace Fractran.M574

open Fractran
open Fractran.M431 (two_pow_pos)

/-! ## The rules (DELTA/GUARD tables, priority order) -/

def f0 : Rule := ⟨fun s => decide (1 ≤ s.b ∧ 1 ≤ s.c),
                  fun s => ⟨s.a + 3, s.b - 1, s.c - 1, s.d, s.e⟩⟩
def f1 : Rule := ⟨fun s => decide (1 ≤ s.a ∧ 1 ≤ s.e),
                  fun s => ⟨s.a - 1, s.b + 1, s.c, s.d + 2, s.e - 1⟩⟩
def f2 : Rule := ⟨fun s => decide (1 ≤ s.a),
                  fun s => ⟨s.a - 1, s.b, s.c + 1, s.d + 1, s.e⟩⟩
def f3 : Rule := ⟨fun s => decide (2 ≤ s.d),
                  fun s => ⟨s.a, s.b, s.c, s.d - 2, s.e + 1⟩⟩
def f4 : Rule := ⟨fun s => decide (1 ≤ s.d),
                  fun s => ⟨s.a, s.b + 1, s.c, s.d - 1, s.e⟩⟩

def M574 : Machine := [f0, f1, f2, f3, f4]

/-- The priority step function of machine 574 in closed form. -/
theorem step_M574 (a b c d e : Nat) :
    step M574 ⟨a, b, c, d, e⟩ =
      if 1 ≤ b ∧ 1 ≤ c then some ⟨a + 3, b - 1, c - 1, d, e⟩
      else if 1 ≤ a ∧ 1 ≤ e then some ⟨a - 1, b + 1, c, d + 2, e - 1⟩
      else if 1 ≤ a then some ⟨a - 1, b, c + 1, d + 1, e⟩
      else if 2 ≤ d then some ⟨a, b, c, d - 2, e + 1⟩
      else if 1 ≤ d then some ⟨a, b + 1, c, d - 1, e⟩
      else none := by
  simp only [M574, step, f0, f1, f2, f3, f4, decide_eq_true_eq]

/-! ## Lemma 0: the halt criterion -/

/-- LEMMA 0.  No rule fires iff `v2 = 0`, `v7 = 0` and
    (`v3 = 0` or `v5 = 0`). -/
theorem halt_iff (a b c d e : Nat) :
    step M574 ⟨a, b, c, d, e⟩ = none ↔
      a = 0 ∧ d = 0 ∧ (b = 0 ∨ c = 0) := by
  rw [step_M574]
  by_cases h0 : 1 ≤ b ∧ 1 ≤ c
  · rw [if_pos h0]; simp; omega
  · rw [if_neg h0]
    by_cases h1 : 1 ≤ a ∧ 1 ≤ e
    · rw [if_pos h1]; simp; omega
    · rw [if_neg h1]
      by_cases h2 : 1 ≤ a
      · rw [if_pos h2]; simp; omega
      · rw [if_neg h2]
        by_cases h3 : 2 ≤ d
        · rw [if_pos h3]; simp; omega
        · rw [if_neg h3]
          by_cases h4 : 1 ≤ d
          · rw [if_pos h4]; simp; omega
          · rw [if_neg h4]; simp; omega

/-- The machine is not degenerate: it CAN halt (from the zero vector). -/
example : step M574 ⟨0, 0, 0, 0, 0⟩ = none := by decide

/-! ## Single-firing lemmas (hypothesis-free; guard and
higher-priority-failure conditions baked into the state shape) -/

/-- f0 is top priority: only its own guard `v3 >= 1 & v5 >= 1`. -/
theorem fire0 (a b c d e : Nat) :
    step M574 ⟨a, b + 1, c + 1, d, e⟩ = some ⟨a + 3, b, c, d, e⟩ := by
  rw [step_M574]
  rw [if_pos (by omega : 1 ≤ b + 1 ∧ 1 ≤ c + 1)]
  simp

/-- f1 fires when `v3 = 0` (which disables f0) and `v2, v11 >= 1`. -/
theorem fire1 (a c d e : Nat) :
    step M574 ⟨a + 1, 0, c, d, e + 1⟩ = some ⟨a, 1, c, d + 2, e⟩ := by
  rw [step_M574]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c))]
  rw [if_pos (by omega : 1 ≤ a + 1 ∧ 1 ≤ e + 1)]
  simp

/-- f2 fires when `v3 = 0` (f0 off) and `v11 = 0` (f1 off), `v2 >= 1`. -/
theorem fire2 (a c d : Nat) :
    step M574 ⟨a + 1, 0, c, d, 0⟩ = some ⟨a, 0, c + 1, d + 1, 0⟩ := by
  rw [step_M574]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c))]
  rw [if_neg (by omega : ¬(1 ≤ a + 1 ∧ 1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 1 ≤ a + 1)]
  simp

/-- f3 fires when `v2 = v3 = 0` (f0, f1, f2 off) and `v7 >= 2`. -/
theorem fire3 (c d e : Nat) :
    step M574 ⟨0, 0, c, d + 2, e⟩ = some ⟨0, 0, c, d, e + 1⟩ := by
  rw [step_M574]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ e))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
  rw [if_pos (by omega : 2 ≤ d + 2)]
  simp

/-- f4 fires at `v7 = 1` exactly: f3's threshold 2 is what stops the
    f3-run and hands over to f4. -/
theorem fire4 (c e : Nat) :
    step M574 ⟨0, 0, c, 1, e⟩ = some ⟨0, 1, c, 0, e⟩ := by
  rw [step_M574]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ c))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat) ∧ 1 ≤ e))]
  rw [if_neg (by omega : ¬(1 ≤ (0:Nat)))]
  rw [if_neg (by omega : ¬(2 ≤ (1:Nat)))]
  rw [if_pos (by omega : 1 ≤ (1:Nat))]

/-! ## Single-rule runs -/

/-- Stage-1 run `f3^n`: halves v7 into v11 (v2 = v3 = 0 throughout). -/
theorem run_f3 (n c d e : Nat) :
    Steps M574 n ⟨0, 0, c, d + 2 * n, e⟩ ⟨0, 0, c, d, e + n⟩ := by
  induction n generalizing e with
  | zero => exact steps_zero M574 _
  | succ n ih =>
    exact ((steps_one M574 (fire3 c (d + 2 * n) e)).comp (ih (e + 1))
      rfl).cast (by omega) (by simp only [St.mk.injEq, and_true, true_and]
        <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-- Stage-5 run `f2^n`: drains v2 into v5 and v7 (v3 = v11 = 0). -/
theorem run_f2 (n a c d : Nat) :
    Steps M574 n ⟨a + n, 0, c, d, 0⟩ ⟨a, 0, c + n, d + n, 0⟩ := by
  induction n generalizing c d with
  | zero => exact steps_zero M574 _
  | succ n ih =>
    exact ((steps_one M574 (fire2 (a + n) c d)).comp (ih (c + 1) (d + 1))
      rfl).cast (by omega) (by simp only [St.mk.injEq, and_true, true_and]
        <;> omega) (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-! ## The (f0 f1) pair block

Each round spends one v5 and one v11, gains 2 to v2 and 2 to v7, and
restores v3 = 1 — the "pair mode" that makes 574 unlike the other eight
(no parity split, because nothing is consumed three at a time). -/

/-- `(f0 f1)^n` from `(x, 1, c+n, d, e+n)` to `(x+2n, 1, c, d+2n, e)`. -/
theorem pairs (n : Nat) : ∀ x c d e : Nat,
    Steps M574 (n * 2) ⟨x, 1, c + n, d, e + n⟩
      ⟨x + 2 * n, 1, c, d + 2 * n, e⟩ := by
  induction n with
  | zero => intro x c d e; exact steps_zero M574 _
  | succ n ih =>
    intro x c d e
    exact ((steps_one M574 (fire0 x 0 (c + n) d (e + n + 1))).comp
      ((steps_one M574 (fire1 (x + 2) (c + n) d (e + n))).comp
        (ih (x + 2) c (d + 2) e) rfl) rfl).cast (by omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)

/-! ## Lemma 2: one full phase (single branch — no parity case split) -/

/-- ONE PHASE.  From `(0, 0, w+k+1, 2w+1, 0)` the machine performs
    `f3^w, f4, (f0 f1)^w, f0, f2^(2w+3)` and reaches
    `(0, 0, 2w+k+3, 4w+3, 0)` in exactly `5w + 5` steps. -/
theorem phase (w k : Nat) :
    Steps M574 (5 * w + 5) ⟨0, 0, w + k + 1, 2 * w + 1, 0⟩
      ⟨0, 0, 2 * w + k + 3, 4 * w + 3, 0⟩ := by
  -- Stage 1: f3^w  ->  (0, 0, w+k+1, 1, w)
  have s1 : Steps M574 w ⟨0, 0, w + k + 1, 2 * w + 1, 0⟩
      ⟨0, 0, w + k + 1, 1, w⟩ :=
    (run_f3 w (w + k + 1) 1 0).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- Stage 2: f4  ->  (0, 1, w+k+1, 0, w)
  have s2 : Steps M574 1 ⟨0, 0, w + k + 1, 1, w⟩ ⟨0, 1, w + k + 1, 0, w⟩ :=
    steps_one M574 (fire4 (w + k + 1) w)
  -- Stage 3: (f0 f1)^w  ->  (2w, 1, k+1, 2w, 0)
  have s3 : Steps M574 (w * 2) ⟨0, 1, w + k + 1, 0, w⟩
      ⟨2 * w, 1, k + 1, 2 * w, 0⟩ :=
    (pairs w 0 (k + 1) 0 0).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- Stage 4: f0  ->  (2w+3, 0, k, 2w, 0)   (v11 = 0 now disables f1)
  have s4 : Steps M574 1 ⟨2 * w, 1, k + 1, 2 * w, 0⟩
      ⟨2 * w + 3, 0, k, 2 * w, 0⟩ :=
    (steps_one M574 (fire0 (2 * w) 0 k (2 * w) 0)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  -- Stage 5: f2^(2w+3)  ->  (0, 0, 2w+k+3, 4w+3, 0)
  have s5 : Steps M574 (2 * w + 3) ⟨2 * w + 3, 0, k, 2 * w, 0⟩
      ⟨0, 0, 2 * w + k + 3, 4 * w + 3, 0⟩ :=
    (run_f2 (2 * w + 3) 0 k (2 * w)).cast rfl
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
      (by simp only [St.mk.injEq, and_true, true_and] <;> omega)
  exact s1.comp (s2.comp (s3.comp (s4.comp s5 rfl) rfl) rfl) (by omega)

/-! ## The boundary family and the induction -/

/-- The boundary `Bst k = (0, 0, 2^k + k, 2^(k+1) - 1, 0)`.
    `Bst 0 = (0,0,1,1,0)` is reached from n = 2 in one step. -/
def Bst (k : Nat) : St := ⟨0, 0, 2 ^ k + k, 2 ^ (k + 1) - 1, 0⟩

/-- LEMMA 1 (entry): n = 2 -> 35 = 5·7, i.e. one f2 step to `Bst 0`. -/
theorem entry : Steps M574 1 ⟨1, 0, 0, 0, 0⟩ (Bst 0) := by decide

/-- LEMMA 2 at the boundary family: `Bst k -> Bst (k+1)` in `5·2^k`
    steps. -/
theorem phase_step (k : Nat) : Steps M574 (5 * 2 ^ k) (Bst k) (Bst (k + 1)) := by
  obtain ⟨w, hw⟩ : ∃ w, 2 ^ k = w + 1 :=
    ⟨2 ^ k - 1, by have := two_pow_pos k; omega⟩
  have h1 : 2 ^ (k + 1) = 2 ^ k * 2 := Nat.pow_succ 2 k
  have h2 : 2 ^ (k + 1 + 1) = 2 ^ (k + 1) * 2 := Nat.pow_succ 2 (k + 1)
  exact (phase w k).cast (by omega)
    (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)
    (by simp only [Bst, St.mk.injEq, and_true, true_and] <;> omega)

/-- Total steps to `Bst k`: `T 0 = 1`, then `5·2^i` per phase;
    `T k = 5·2^k - 4`. -/
def T : Nat → Nat
  | 0 => 1
  | k + 1 => T k + 5 * 2 ^ k

/-- The orbit visits every boundary. -/
theorem reach : ∀ k, Steps M574 (T k) ⟨1, 0, 0, 0, 0⟩ (Bst k)
  | 0 => entry
  | k + 1 => (reach k).comp (phase_step k) rfl

theorem T_ge (k : Nat) : k ≤ T k := by
  induction k with
  | zero => exact Nat.zero_le 1
  | succ k ih =>
    have hp := two_pow_pos k
    show k + 1 ≤ T k + 5 * 2 ^ k
    omega

/-! ## The theorem -/

/-- THEOREM M574.  The FRACTRAN program [8/15, 147/22, 35/2, 11/49, 3/7],
    started at n = 2 (exponent vector (1,0,0,0,0)), never halts. -/
theorem m574_never_halts : NeverHalts M574 ⟨1, 0, 0, 0, 0⟩ :=
  neverHalts_of_unbounded fun n => ⟨T n, Bst n, T_ge n, reach n⟩

/-! ## Lemma 3, explicit form -/

theorem orbit_never_stuck (n : Nat) (s' : St)
    (h : iter M574 n ⟨1, 0, 0, 0, 0⟩ = some s') : step M574 s' ≠ none := by
  intro hstep
  apply m574_never_halts (n + 1)
  rw [iter_add M574 n 1, h]
  show (step M574 s').bind (iter M574 0) = none
  rw [hstep]
  rfl

/-- LEMMA 3: no state on the orbit satisfies the halt criterion. -/
theorem no_halt_state_on_orbit (n : Nat) (s' : St)
    (h : iter M574 n ⟨1, 0, 0, 0, 0⟩ = some s') :
    ¬(s'.a = 0 ∧ s'.d = 0 ∧ (s'.b = 0 ∨ s'.c = 0)) := by
  intro hcrit
  apply orbit_never_stuck n s' h
  obtain ⟨a, b, c, d, e⟩ := s'
  exact (halt_iff a b c d e).mpr hcrit

/-! ## Ground-truth cross-checks (independent of the lemmas above)

`T 3 = 36` is exactly the entry step count recorded in
m_siblings_proofs.py, and 36 concrete steps land on its boundary
(0,0,11,15,0) = `Bst 3`. -/

example : T 3 = 36 := by decide
set_option maxRecDepth 4096 in
example : iter M574 36 ⟨1, 0, 0, 0, 0⟩ = some ⟨0, 0, 11, 15, 0⟩ := by decide
example : Bst 3 = ⟨0, 0, 11, 15, 0⟩ := by decide

end Fractran.M574
