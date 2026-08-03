/-
THE MIDDLE LAYER: turning certificate data into `Steps`.

`Decider.lean` proves the two ends of the argument:
  * `neverHalts_of_phases` -- IF every boundary steps to the next, the
    machine never halts;
  * `Exp.alwaysGE_sound` (in `Exp.lean`) -- ONE Boolean evaluation
    settles infinitely many guard inequalities.
What was missing is the middle: given a stage of a certificate, actually
PRODUCE the `Steps`.  That is this file.

The reusable content is `run_affine`: a rule fired `k` times along an
affine segment.  Every machine file currently proves three or four
instances of it by hand (`run_f0`, `run_f2`, ...), each an induction with
its own state shape.  Here it is proved once, for an arbitrary machine
and an arbitrary integer delta, from ENDPOINT hypotheses only -- which is
exactly the interface `Exp.alwaysGE_sound` provides.

DESIGN.  States are `St` (five `Nat` coordinates), but deltas are
integers, so the arithmetic is done in `Int` and pushed back through
`Int.toNat`.  The guard hypotheses are what keep every coordinate
nonnegative along the run, so the conversion is lossless exactly where it
is used -- and stating that carefully is most of the work below.
-/
import LeanBbf.Runner
import LeanBbf.Exp

namespace Fractran

/-! ## Integer deltas on states -/

/-- A delta vector: the effect of one rule firing, as five integers. -/
structure IVec where
  d0 : Int
  d1 : Int
  d2 : Int
  d3 : Int
  d4 : Int
deriving DecidableEq, Repr

/-- `s` shifted by `t` copies of `v`, computed in `Int` and clipped back
    to `Nat`.  The clipping is inert on the range we use it: the guard
    conditions below force every coordinate to stay nonnegative. -/
def shiftN (s : St) (v : IVec) (t : Nat) : St :=
  ⟨((s.a : Int) + t * v.d0).toNat, ((s.b : Int) + t * v.d1).toNat,
   ((s.c : Int) + t * v.d2).toNat, ((s.d : Int) + t * v.d3).toNat,
   ((s.e : Int) + t * v.d4).toNat⟩

@[simp] theorem shiftN_zero (s : St) (v : IVec) : shiftN s v 0 = s := by
  cases s
  simp [shiftN]

/-- The coordinates of a shifted state, as integers, whenever they are
    nonnegative -- the bridge between `Int` reasoning and `Nat` states. -/
theorem shiftN_coord_a {s : St} {v : IVec} {t : Nat}
    (h : 0 ≤ (s.a : Int) + t * v.d0) :
    ((shiftN s v t).a : Int) = (s.a : Int) + t * v.d0 := by
  show ((((s.a : Int) + t * v.d0).toNat : Nat) : Int) = _
  exact Int.toNat_of_nonneg h

theorem shiftN_coord_b {s : St} {v : IVec} {t : Nat}
    (h : 0 ≤ (s.b : Int) + t * v.d1) :
    ((shiftN s v t).b : Int) = (s.b : Int) + t * v.d1 :=
  Int.toNat_of_nonneg h

theorem shiftN_coord_c {s : St} {v : IVec} {t : Nat}
    (h : 0 ≤ (s.c : Int) + t * v.d2) :
    ((shiftN s v t).c : Int) = (s.c : Int) + t * v.d2 :=
  Int.toNat_of_nonneg h

theorem shiftN_coord_d {s : St} {v : IVec} {t : Nat}
    (h : 0 ≤ (s.d : Int) + t * v.d3) :
    ((shiftN s v t).d : Int) = (s.d : Int) + t * v.d3 :=
  Int.toNat_of_nonneg h

theorem shiftN_coord_e {s : St} {v : IVec} {t : Nat}
    (h : 0 ≤ (s.e : Int) + t * v.d4) :
    ((shiftN s v t).e : Int) = (s.e : Int) + t * v.d4 :=
  Int.toNat_of_nonneg h

/-! ## The generic affine run

This is the lemma the per-machine `run_fX` inductions were all doing by
hand.  Stated with the successor step as a hypothesis, so that a caller
supplies only "the rule fires at each point of the segment" -- which is
what `step_of_first` plus the endpoint principle deliver. -/

/-- GENERIC AFFINE RUN.  If from every point of the affine segment the
    machine takes one step to the next point, it performs the whole
    segment. -/
theorem run_affine {M : Machine} (s : St) (v : IVec) (k : Nat)
    (h : ∀ t, t < k → step M (shiftN s v t) = some (shiftN s v (t + 1))) :
    Steps M k s (shiftN s v k) := by
  have := run_of_firing (fun t => shiftN s v t) k h
  simpa using this

/-- The form a certificate uses: the segment is described by a rule of
    the machine, and the successor property is derived from the rule's
    action rather than assumed. -/
theorem run_affine_of_rule {M : Machine} (pre : Machine) (r : Rule)
    (post : Machine) (hM : M = pre ++ r :: post)
    (s : St) (v : IVec) (k : Nat)
    (hdis : ∀ t, t < k → ∀ q ∈ pre, q.guard (shiftN s v t) = false)
    (hen : ∀ t, t < k → r.guard (shiftN s v t) = true)
    (hact : ∀ t, t < k → r.act (shiftN s v t) = shiftN s v (t + 1)) :
    Steps M k s (shiftN s v k) := by
  refine run_affine s v k (fun t ht => ?_)
  subst hM
  rw [step_of_first pre r post (hdis t ht) (hen t ht), hact t ht]

/-! ## Endpoint hypotheses suffice

The point of the affine shape: a guard is a lower bound on a coordinate,
which along the segment is a linear function of `t`, so it holds
throughout as soon as it holds at the two ends.  `affine_nonneg_of_endpoints`
in `Fractran.lean` is the principle; this packages it in the form the
checker produces. -/

/-- A coordinate bound propagated from the two ends of a run. -/
theorem coord_ge_of_endpoints (base del thr : Int) (k : Nat)
    (h0 : thr ≤ base) (h1 : thr ≤ base + del * (((k - 1 : Nat)) : Int)) :
    ∀ t : Nat, t < k → thr ≤ base + del * (t : Int) := by
  intro t ht
  have hk : t ≤ k - 1 := by omega
  have h := affine_nonneg_of_endpoints (base - thr) del (k - 1)
    (by omega) (by omega) t hk
  omega

/-- Dually, a coordinate staying BELOW a threshold across the run -- the
    form used to keep a higher-priority rule disabled.  Note it is a
    single coordinate, never a disjunction: that is the content of
    `Decider.disjunctive_endpoint_check_unsound`. -/
theorem coord_lt_of_endpoints (base del thr : Int) (k : Nat)
    (h0 : base ≤ thr) (h1 : base + del * (((k - 1 : Nat)) : Int) ≤ thr) :
    ∀ t : Nat, t < k → base + del * (t : Int) ≤ thr := by
  intro t ht
  have hk : t ≤ k - 1 := by omega
  exact affine_le_of_endpoints base del thr (k - 1) h0 h1 t hk

/-! ## Worked instance: the endpoint interface in action

A run of a rule that decrements one coordinate and increments another,
with the guard checked only at the two ends.  This is the shape of every
`run_fX` lemma in the nine machine files. -/

example (base del : Int) (k : Nat)
    (h0 : (1 : Int) ≤ base)
    (h1 : (1 : Int) ≤ base + del * (((k - 1 : Nat)) : Int)) :
    ∀ t : Nat, t < k → (1 : Int) ≤ base + del * (t : Int) :=
  coord_ge_of_endpoints base del 1 k h0 h1

end Fractran
