/-
General semantics for priority-guarded vector machines (FRACTRAN over a
fixed prime basis, in exponent-vector form), pure Lean 4 core (no mathlib).

A state is the exponent vector (v2, v3, v5, v7, v11) of the FRACTRAN
integer over the primes (2, 3, 5, 7, 11).  A rule has a decidable (Bool)
guard and an action; one machine step applies the FIRST rule (in list
order) whose guard holds, and the machine halts when no guard holds.
-/

namespace Fractran

/-- Exponent vector over primes (2, 3, 5, 7, 11):
    `a` = v2, `b` = v3, `c` = v5, `d` = v7, `e` = v11. -/
structure St where
  a : Nat
  b : Nat
  c : Nat
  d : Nat
  e : Nat
deriving DecidableEq, Repr

/-- A guarded rule: `guard` is the (decidable) enabling condition,
    `act` the effect on the state.  For a FRACTRAN fraction the guard is a
    conjunction of coordinate lower bounds and `act` adds the delta vector;
    the guard always dominates the negative part of the delta, so the
    action is total on `Nat` states. -/
structure Rule where
  guard : St → Bool
  act : St → St

/-- A machine is a priority-ordered list of rules. -/
abbrev Machine := List Rule

/-- One step: the first enabled rule fires; `none` = halt. -/
def step : Machine → St → Option St
  | [], _ => none
  | r :: rs, s => if r.guard s then some (r.act s) else step rs s

/-- `iter M n s` = the state after `n` steps, or `none` if the machine
    halted strictly before completing them. -/
def iter (M : Machine) : Nat → St → Option St
  | 0, s => some s
  | n + 1, s => (step M s).bind (iter M n)

/-- `Steps M n s t`: from `s` the machine runs `n` full steps and is then
    in state `t` (in particular it does not halt on the way). -/
abbrev Steps (M : Machine) (n : Nat) (s t : St) : Prop := iter M n s = some t

/-- `t` is reachable from `s`. -/
def Reaches (M : Machine) (s t : St) : Prop := ∃ n, Steps M n s t

/-- The machine never halts from `s`: every step count is completed. -/
def NeverHalts (M : Machine) (s : St) : Prop := ∀ n, iter M n s ≠ none

theorem steps_zero (M : Machine) (s : St) : Steps M 0 s s := rfl

theorem steps_one (M : Machine) {s t : St} (h : step M s = some t) :
    Steps M 1 s t := by
  show (step M s).bind (iter M 0) = some t
  rw [h]; rfl

/-- Splitting a run: `m + n` steps = `m` steps then `n` steps. -/
theorem iter_add (M : Machine) (m n : Nat) :
    ∀ s, iter M (m + n) s = (iter M m s).bind (iter M n) := by
  induction m with
  | zero => intro s; rw [Nat.zero_add]; rfl
  | succ m ih =>
    intro s
    rw [Nat.succ_add]
    show (step M s).bind (iter M (m + n)) =
      ((step M s).bind (iter M m)).bind (iter M n)
    cases h : step M s with
    | none => rfl
    | some t => exact ih t

/-- Transitivity with explicit step-count bookkeeping. -/
theorem Steps.comp {M : Machine} {m n p : Nat} {s t u : St}
    (h1 : Steps M m s t) (h2 : Steps M n t u) (hp : m + n = p) :
    Steps M p s u := by
  subst hp
  show iter M (m + n) s = some u
  rw [iter_add M m n s, h1]
  exact h2

/-- Rewriting the step count and the endpoints of a run. -/
theorem Steps.cast {M : Machine} {n n' : Nat} {s t s' t' : St}
    (h : Steps M n s t) (hn : n = n') (hs : s = s') (ht : t = t') :
    Steps M n' s' t' :=
  hn ▸ hs ▸ ht ▸ h

/-- ITERATION LEMMA (general block/run form).  If `g k` is the state at
    the start of block `k` and every block is an `L`-step run from `g k`
    to `g (k+1)`, then `K` blocks take `K * L` steps from `g 0` to `g K`.
    With `L = 1` this is the single-rule run lemma: a rule fired `c`
    times consecutively moves `s` to `s + c·δ` in `c` steps. -/
theorem steps_blocks {M : Machine} (g : Nat → St) (L : Nat) :
    ∀ K, (∀ k, k < K → Steps M L (g k) (g (k + 1))) →
      Steps M (K * L) (g 0) (g K) := by
  intro K
  induction K with
  | zero => intro _; rw [Nat.zero_mul]; exact steps_zero M (g 0)
  | succ K ih =>
    intro h
    exact Steps.comp (ih fun k hk => h k (by omega)) (h K (by omega))
      (Nat.succ_mul K L).symm

/-- Trajectory form of the run lemma (`L = 1`). -/
theorem steps_of_traj {M : Machine} (f : Nat → St) (c : Nat)
    (h : ∀ t, t < c → step M (f t) = some (f (t + 1))) :
    Steps M c (f 0) (f c) := by
  have := steps_blocks f 1 c (fun t ht => steps_one M (h t ht))
  rwa [Nat.mul_one] at this

/-- If the machine survives arbitrarily many steps, it never halts. -/
theorem neverHalts_of_unbounded {M : Machine} {s : St}
    (h : ∀ n, ∃ m t, n ≤ m ∧ Steps M m s t) : NeverHalts M s := by
  intro n hn
  obtain ⟨m, t, hnm, hst⟩ := h n
  have hm : m = n + (m - n) := by omega
  rw [hm] at hst
  unfold Steps at hst
  rw [iter_add, hn] at hst
  simp at hst

/-! ## The affine endpoint principle

Within a single-rule run the state is affine in the run counter `t`
(coordinate value `a + b·t`, `b` = the rule's delta).  Every guard /
priority condition is a linear inequality in such a value, so it holds
for all `0 ≤ t ≤ n` iff it holds at the two ends `t = 0` and `t = n`:
a linear integer function attains its minimum (and maximum) over an
interval at an endpoint.  These two lemmas package that principle; the
concrete run lemmas for machine 431 discharge their instances by `omega`
(the deltas there are literal constants, so the conditions are linear). -/

/-- A linear function nonnegative at both ends of `[0, n]` is
    nonnegative at every integer point in between (min at an end). -/
theorem affine_nonneg_of_endpoints (a b : Int) (n : Nat)
    (h0 : 0 ≤ a) (hn : 0 ≤ a + b * n) :
    ∀ t : Nat, t ≤ n → 0 ≤ a + b * t := by
  intro t ht
  rcases Int.le_total 0 b with hb | hb
  · -- b ≥ 0: minimum at t = 0
    exact Int.add_nonneg h0 (Int.mul_nonneg hb (Int.natCast_nonneg t))
  · -- b ≤ 0: minimum at t = n
    have htn : (t : Int) ≤ (n : Int) := by omega
    have h2 : (-b) * (t : Int) ≤ (-b) * (n : Int) :=
      Int.mul_le_mul_of_nonneg_left htn (by omega)
    rw [Int.neg_mul, Int.neg_mul] at h2
    have h3 := Int.neg_le_neg h2
    rw [Int.neg_neg, Int.neg_neg] at h3
    exact Int.le_trans hn (Int.add_le_add_left h3 a)

/-- A linear function bounded by `c` at both ends of `[0, n]` is bounded
    by `c` at every integer point in between (max at an end).  This is
    the form used to propagate FAILURE of a higher-priority guard
    (`value ≤ threshold - 1`) across a whole run from its two ends. -/
theorem affine_le_of_endpoints (a b c : Int) (n : Nat)
    (h0 : a ≤ c) (hn : a + b * n ≤ c) :
    ∀ t : Nat, t ≤ n → a + b * t ≤ c := by
  intro t ht
  rcases Int.le_total 0 b with hb | hb
  · -- b ≥ 0: maximum at t = n
    have htn : (t : Int) ≤ (n : Int) := by omega
    have h2 : b * (t : Int) ≤ b * (n : Int) :=
      Int.mul_le_mul_of_nonneg_left htn hb
    exact Int.le_trans (Int.add_le_add_left h2 a) hn
  · -- b ≤ 0: maximum at t = 0
    have h2 : 0 ≤ (-b) * (t : Int) :=
      Int.mul_nonneg (by omega) (Int.natCast_nonneg t)
    rw [Int.neg_mul] at h2
    have h3 : b * (t : Int) ≤ 0 := by omega
    calc a + b * (t : Int) ≤ a + 0 := Int.add_le_add_left h3 a
      _ = a := Int.add_zero a
      _ ≤ c := h0

end Fractran
