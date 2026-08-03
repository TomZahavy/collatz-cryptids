/-
THE SYMBOLIC LAYER: expressions in the phase index, with a decidable
"stays above a threshold forever" test.

This is what lets a certificate speak about ALL phase indices at once,
and it is the prerequisite for a verified checker (after which each
machine reduces to evaluating a decidable predicate on certificate data,
instead of carrying its own 350-line development).

DESIGN NOTE -- why there are no rational numbers here.

The Python certificates carry coefficients in Q: machine 431's block
count is (2*2^n - 2)/3, and denominators 2 and 3 both occur across the
nine.  Building Q without mathlib, and then deciding when a rational
expression takes INTEGER values (which a step count must), needs the
eventual periodicity of n |-> 2^n mod d -- a real piece of work.

All of it disappears with a change of generator.  A parity branch has
n = 2m + r, so 2^n = 2^r * 4^m; re-indexing that branch by m and adding

    geo q m  =  1 + q + ... + q^(m-1)

-- an integer BY CONSTRUCTION, defined below by its recurrence -- makes
every coefficient integral:

    (2*2^n - 2)/3   at n = 2m   =   (2*4^m - 2)/3   =   2 * geo 4 m,

and we checked that this covers every denominator occurring in the nine
certificates.  So the class is

    eval e q m  =  a + b*m + c*(q^m) + g*(geo q m),     a,b,c,g in Z,

integer coefficients only, closed under m |-> m+1, addition and integer
scaling.

DESIGN NOTE -- why the positivity test is deliberately weak.

Deciding whether a general linear recurrence stays nonnegative is the
Positivity problem, open in general.  Our class has characteristic roots
1, 1, q, so it is easy; nonetheless the criterion below is a SUFFICIENT
condition, not a characterisation.  The checker may therefore reject a
certificate it cannot certify.  That costs completeness and never
soundness, which is the right trade for a proof-producing tool.

Everything here is mathlib-free: `ring`, `push_cast` and the `Monoid.npow`
lemmas are unavailable, so powers are defined by an explicit recursion
and the algebra is done with core `Int` lemmas and `omega`.
-/
import LeanBbf.Fractran

namespace Fractran

/-! ## Powers and the geometric generator, by explicit recursion -/

/-- `pw q m = q^m`, defined so that `pw q (m+1) = q * pw q m` holds by
    `rfl` (no `Monoid.npow` machinery). -/
def pw (q : Nat) : Nat → Int
  | 0 => 1
  | m + 1 => (q : Int) * pw q m

/-- `geo q m = 1 + q + ... + q^(m-1)`. -/
def geo (q : Nat) : Nat → Int
  | 0 => 0
  | m + 1 => (q : Int) * geo q m + 1

theorem pw_pos (q : Nat) (hq : 1 ≤ q) : ∀ m, 0 < pw q m
  | 0 => Int.zero_lt_one
  | m + 1 => by
    have ih := pw_pos q hq m
    have hq' : (1 : Int) ≤ (q : Int) := by exact_mod_cast hq
    show 0 < (q : Int) * pw q m
    have : (0 : Int) < (q : Int) := by omega
    exact Int.mul_pos this ih

theorem geo_nonneg (q : Nat) : ∀ m, 0 ≤ geo q m
  | 0 => Int.le_refl 0
  | m + 1 => by
    have ih := geo_nonneg q m
    show 0 ≤ (q : Int) * geo q m + 1
    have h : (0 : Int) ≤ (q : Int) * geo q m :=
      Int.mul_nonneg (Int.natCast_nonneg q) ih
    omega

/-! ## Expressions -/

/-- `a + b*m + c*(q^m) + g*(geo q m)`, integer coefficients. -/
structure Exp where
  a : Int
  b : Int
  c : Int
  g : Int
deriving DecidableEq, Repr

namespace Exp

def eval (e : Exp) (q : Nat) (m : Nat) : Int :=
  e.a + e.b * m + e.c * pw q m + e.g * geo q m

/-! ## The monotonicity criterion

The whole difficulty is that `c * pw q (m+1)` and `c * pw q m` are
unrelated atoms as far as `omega` is concerned.  We supply the two
comparisons it is missing and then everything is linear. -/

/-- `x ≤ q*x` for `x ≥ 0`, `q ≥ 1`: the step `omega` cannot take. -/
theorem le_mul_self {x : Int} (hx : 0 ≤ x) {q : Nat} (hq : 1 ≤ q) :
    x ≤ (q : Int) * x := by
  have hq' : (1 : Int) ≤ (q : Int) := by exact_mod_cast hq
  have h := Int.mul_le_mul_of_nonneg_right hq' hx
  rwa [Int.one_mul] at h

/-- Scaled form: `k*x ≤ k*(q*x)` for `k, x ≥ 0`. -/
theorem mul_le_mul_pw {k x : Int} (hk : 0 ≤ k) (hx : 0 ≤ x)
    {q : Nat} (hq : 1 ≤ q) : k * x ≤ k * ((q : Int) * x) :=
  Int.mul_le_mul_of_nonneg_left (le_mul_self hx hq) hk

/-- MONOTONICITY.  Nonnegative exponential and geometric coefficients,
    with the linear part not overwhelming the geometric one, make the
    expression nondecreasing. -/
theorem eval_mono (e : Exp) {q : Nat} (hq : 1 ≤ q)
    (hc : 0 ≤ e.c) (hg : 0 ≤ e.g) (hb : 0 ≤ e.b + e.g) (m : Nat) :
    e.eval q m ≤ e.eval q (m + 1) := by
  have hP : (0 : Int) ≤ pw q m := Int.le_of_lt (pw_pos q hq m)
  have hG : (0 : Int) ≤ geo q m := geo_nonneg q m
  -- the two comparisons `omega` cannot make on its own
  have h1 : e.c * pw q m ≤ e.c * ((q : Int) * pw q m) :=
    mul_le_mul_pw hc hP hq
  have h2 : e.g * geo q m ≤ e.g * ((q : Int) * geo q m) :=
    mul_le_mul_pw hg hG hq
  -- and the distributivity `omega` also cannot do
  have e1 : e.eval q (m + 1)
      = e.a + (e.b * (m : Int) + e.b) + e.c * ((q : Int) * pw q m)
        + (e.g * ((q : Int) * geo q m) + e.g) := by
    show e.a + e.b * (((m + 1 : Nat)) : Int) + e.c * pw q (m + 1)
          + e.g * geo q (m + 1) = _
    have hpw : pw q (m + 1) = (q : Int) * pw q m := rfl
    have hgeo : geo q (m + 1) = (q : Int) * geo q m + 1 := rfl
    have hcast : (((m + 1 : Nat)) : Int) = (m : Int) + 1 := by omega
    rw [hpw, hgeo, hcast, Int.mul_add, Int.mul_one, Int.mul_add, Int.mul_one]
  rw [e1]
  show e.a + e.b * (m : Int) + e.c * pw q m + e.g * geo q m ≤ _
  omega

/-- Monotone from `m0` upward gives the bound at every `m ≥ m0`. -/
theorem le_eval_of_mono (e : Exp) {q : Nat} (hq : 1 ≤ q)
    (hc : 0 ≤ e.c) (hg : 0 ≤ e.g) (hb : 0 ≤ e.b + e.g)
    {t : Int} {m0 : Nat} (h0 : t ≤ e.eval q m0) :
    ∀ m, m0 ≤ m → t ≤ e.eval q m := by
  intro m
  induction m with
  | zero =>
    intro h
    have : m0 = 0 := Nat.le_zero.mp h
    exact this ▸ h0
  | succ k ih =>
    intro h
    rcases Nat.lt_or_ge m0 (k + 1) with hlt | hge
    · have hk : m0 ≤ k := by omega
      exact Int.le_trans (ih hk) (eval_mono e hq hc hg hb k)
    · have : m0 = k + 1 := by omega
      exact this ▸ h0

/-! ## The executable test -/

/-- The Boolean the checker calls: "is `eval e q m ≥ t` for every
    `m ≥ m0`?"  Sufficient, not complete. -/
def alwaysGE (e : Exp) (q : Nat) (t : Int) (m0 : Nat) : Bool :=
  decide (1 ≤ q) && decide (0 ≤ e.c) && decide (0 ≤ e.g) &&
  decide (0 ≤ e.b + e.g) && decide (t ≤ e.eval q m0)

/-- SOUNDNESS.  One Boolean evaluation yields an infinite family of
    inequalities -- this is the property that lets a finite certificate
    cover all phase indices. -/
theorem alwaysGE_sound {e : Exp} {q : Nat} {t : Int} {m0 : Nat}
    (h : alwaysGE e q t m0 = true) :
    ∀ m, m0 ≤ m → t ≤ e.eval q m := by
  unfold alwaysGE at h
  simp only [Bool.and_eq_true, decide_eq_true_eq] at h
  obtain ⟨⟨⟨⟨hq, hc⟩, hg⟩, hb⟩, h0⟩ := h
  exact le_eval_of_mono e hq hc hg hb h0

end Exp

/-! ## Worked instances

Expressions that really occur in the certificates, and the test running
on them at compile time. -/

-- machine 431's v2 boundary coordinate, re-indexed to base 4: 2*4^m - 1
example : (⟨-1, 0, 2, 0⟩ : Exp).eval 4 3 = 127 := by decide
-- its v11 coordinate: m
example : (⟨0, 1, 0, 0⟩ : Exp).eval 4 5 = 5 := by decide
-- the block count (2*2^n-2)/3 at n = 2m, i.e. 2*geo 4 m -- integral,
-- which was the entire point of the generator
example : (⟨0, 0, 0, 2⟩ : Exp).eval 4 3 = 42 := by decide

-- the checker's guard tests, decided at compile time
example : Exp.alwaysGE ⟨-1, 0, 2, 0⟩ 4 1 0 = true := by decide
example : Exp.alwaysGE ⟨0, 0, 0, 2⟩ 4 0 0 = true := by decide
-- and one it must reject: 5 - m is not eventually ≥ 1
example : Exp.alwaysGE ⟨5, -1, 0, 0⟩ 4 1 0 = false := by decide

/-- Soundness in use: infinitely many facts from one `decide`. -/
example : ∀ m, 0 ≤ m → (1 : Int) ≤ (⟨-1, 0, 2, 0⟩ : Exp).eval 4 m :=
  Exp.alwaysGE_sound (by decide)

end Fractran
