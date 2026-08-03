/-
GENERIC MACHINERY, step one of the verified checker.

The nine per-machine files each re-prove the same three things by hand:

  (a) FIRING: "at this state shape, rule r fires" -- i.e. r's guard holds
      and every higher-priority rule has a failing guard.  Six or so such
      lemmas per machine, each a hand-written `rw [if_neg ...]` chain
      through the closed-form step function.
  (b) RUNS: a rule fired k times consecutively moves the state by k
      deltas.
  (c) BLOCKS: a fixed word repeated K times.

None of that is machine-specific.  This file proves each once, over an
arbitrary machine, so a per-machine file only has to supply the guard
arithmetic.  (b) and (c) already existed in `Fractran.lean` as
`steps_of_traj` and `steps_blocks`; the missing and most valuable piece
is (a), which is where the priority reasoning lives -- and where the
subtlety of Proposition "single conjunct" bites.

This is the reusable core of a verified checker.  The remaining gap to a
fully verified decider is the SYMBOLIC layer: representing a certificate
as data with coefficients in {a + b*n + c*2^n} and deciding the guard
conditions for ALL n at once.  That layer is what would collapse each
machine to `by decide` on certificate data; it is not in this file.
-/
import LeanBbf.Fractran

namespace Fractran

/-! ## The generic firing lemma

`step` scans the rule list and fires the first enabled rule.  So to know
that rule `r` fires it suffices to exhibit the list as `pre ++ r :: post`
with every rule in `pre` disabled.  Nothing about `post` matters -- the
scan never reaches it. -/

/-- GENERIC FIRING.  If the machine is `pre ++ r :: post`, every rule of
    `pre` is disabled at `s`, and `r` is enabled at `s`, then `r` fires.

    This replaces the per-machine `fireN` lemmas: their `rw [if_neg ...]`
    chains are exactly the unfolding of this induction. -/
theorem step_of_first {s : St} :
    ∀ (pre : Machine) (r : Rule) (post : Machine),
      (∀ q ∈ pre, q.guard s = false) → r.guard s = true →
      step (pre ++ r :: post) s = some (r.act s) := by
  intro pre
  induction pre with
  | nil =>
    intro r post _ hr
    show (if r.guard s then some (r.act s) else step post s) = _
    rw [hr]
    rfl
  | cons q qs ih =>
    intro r post hpre hr
    have hq : q.guard s = false := hpre q (List.mem_cons.mpr (Or.inl rfl))
    show (if q.guard s then some (q.act s) else step (qs ++ r :: post) s) = _
    rw [hq]
    exact ih r post (fun x hx => hpre x (List.mem_cons.mpr (Or.inr hx))) hr

/-- The halting counterpart: if every rule is disabled, the machine
    halts.  (Used to state halt criteria generically.) -/
theorem step_none_of_all_disabled {s : St} :
    ∀ M : Machine, (∀ q ∈ M, q.guard s = false) → step M s = none := by
  intro M
  induction M with
  | nil => intro _; rfl
  | cons q qs ih =>
    intro h
    have hq : q.guard s = false := h q (List.mem_cons.mpr (Or.inl rfl))
    show (if q.guard s then some (q.act s) else step qs s) = none
    rw [hq]
    exact ih (fun x hx => h x (List.mem_cons.mpr (Or.inr hx)))

/-- Conversely, a machine with an enabled rule does not halt. -/
theorem step_isSome_of_enabled {s : St} {M : Machine} {r : Rule}
    (hr : r ∈ M) (h : r.guard s = true) : step M s ≠ none := by
  induction M with
  | nil => cases hr
  | cons q qs ih =>
    show (if q.guard s then some (q.act s) else step qs s) ≠ none
    cases hq : q.guard s with
    | true => simp
    | false =>
      simp only [Bool.false_eq_true, if_false]
      rcases List.mem_cons.mp hr with rfl | hmem
      · exact absurd h (by rw [hq]; simp)
      · exact ih hmem

/-! ## Generic runs

A run is a trajectory whose每 step is a firing.  `steps_of_traj` in
`Fractran.lean` already turns a pointwise firing hypothesis into a
`Steps`; this specializes it to the common shape "the state is `f t` at
time `t`". -/

/-- GENERIC RUN.  If at every `t < k` the machine fires from `f t` to
    `f (t+1)`, then it performs `k` steps from `f 0` to `f k`. -/
theorem run_of_firing {M : Machine} (f : Nat → St) (k : Nat)
    (h : ∀ t, t < k → step M (f t) = some (f (t + 1))) :
    Steps M k (f 0) (f k) :=
  steps_of_traj f k h

/-- GENERIC RUN, packaged with the firing lemma: a single rule `r` fired
    `k` times along an explicit state sequence. -/
theorem run_rule {M : Machine} (pre : Machine) (r : Rule) (post : Machine)
    (hM : M = pre ++ r :: post) (f : Nat → St) (k : Nat)
    (hdis : ∀ t, t < k → ∀ q ∈ pre, q.guard (f t) = false)
    (hen : ∀ t, t < k → r.guard (f t) = true)
    (hact : ∀ t, t < k → r.act (f t) = f (t + 1)) :
    Steps M k (f 0) (f k) := by
  subst hM
  refine run_of_firing f k (fun t ht => ?_)
  rw [step_of_first pre r post (hdis t ht) (hen t ht), hact t ht]

/-! ## Generic blocks

`steps_blocks` handles the outer repetition; this states the common case
where each block is itself a fixed number of steps. -/

/-- GENERIC BLOCK.  `K` repetitions of an `L`-step block whose start
    states are `g 0, g 1, ...` take `K * L` steps. -/
theorem block_of_steps {M : Machine} (g : Nat → St) (L K : Nat)
    (h : ∀ k, k < K → Steps M L (g k) (g (k + 1))) :
    Steps M (K * L) (g 0) (g K) :=
  steps_blocks g L K h

end Fractran
