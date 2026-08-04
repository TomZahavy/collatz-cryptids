/-
The machines, and the check that this file's semantics are the real ones.

A formalisation is worth nothing if its `step` is not the step the rest
of the world means.  The Python side pinned its simulators against the
four busy-beaver champions -- known step counts and known numbers of
ones -- and this file does the same, at compile time, with `#guard`.
If the Lean model drifted from the standard convention (which cell is
written, when the halting transition counts as a step, what unwritten
tape reads) at least one of these numbers would move.

BB(5) is not checked here: 47,176,870 steps is beyond what the kernel
should be asked to evaluate.  BB(2), BB(3) and BB(4) pin the convention;
the Python cross-check covers the rest.
-/
import LeanBb6.TM

namespace Bb6

/-- Build a machine from a table, one entry per state, each a pair
    (transition on 0, transition on 1). -/
def ofTable (t : List (Option Tr × Option Tr)) : Machine :=
  fun q s =>
    match t[q]? with
    | none => none
    | some (a, b) => if s then b else a

/-- `1RB` and friends: write, right?, next state. -/
def tr (w : Bool) (r : Bool) (n : Nat) : Option Tr := some ⟨w, r, n⟩
def hlt : Option Tr := none

/-- The initial configuration: blank tape, state A, facing right. -/
def start : Cfg := ⟨[], [], 0, true⟩

/-- Executable run, for validation only. -/
def runFor (M : Machine) : Nat → Cfg → Option Cfg
  | 0, c => some c
  | n + 1, c =>
      match step M c with
      | none => none
      | some c' => runFor M n c'

/-- The bridge from computation to proof: if the executable runner gets
    from `a` to `b` in `n` steps, then `Steps` holds.

    This is what makes a concrete crossing a one-liner.  Proving one
    directly with `Steps.succ` requires naming the intermediate
    configuration, because it appears as a metavariable the tactic
    cannot solve before elaborating the rest; going through `runFor`
    lets the kernel compute it instead. -/
theorem steps_of_runFor {M : Machine} :
    ∀ (n : Nat) (a b : Cfg), runFor M n a = some b → Steps M n a b := by
  intro n
  induction n with
  | zero =>
      intro a b h
      injection h with h
      exact h ▸ Steps.zero a
  | succ k ih =>
      intro a b h
      unfold runFor at h
      cases hs : step M a with
      | none => rw [hs] at h; exact absurd h (by simp)
      | some c => rw [hs] at h; exact Steps.succ hs (ih c b h)

/-- The number of steps before halting, if it halts within `fuel`. -/
def haltAt (M : Machine) : Nat → Nat → Cfg → Option Nat
  | 0, _, _ => none
  | fuel + 1, n, c =>
      match step M c with
      | none => some n
      | some c' => haltAt M fuel (n + 1) c'

def ones (c : Cfg) : Nat :=
  (c.left.filter id).length + (c.right.filter id).length

def onesAt (M : Machine) : Nat → Cfg → Nat
  | 0, c => ones c
  | fuel + 1, c =>
      match step M c with
      | none => ones c
      | some c' => onesAt M fuel c'

/-! ## The champions, as a check on the semantics -/

-- BB(2) = 1RB1LB_1LA1RZ, halting after 6 steps with 4 ones.
-- State Z is the halt state; here it is a state with no transitions.
def bb2 : Machine := ofTable
  [ (tr true true 1, tr true false 1)
  , (tr true false 0, tr true true 2)
  , (hlt, hlt) ]

-- BB(3) = 1RB1RZ_1LB0RC_1LC1LA, 21 steps, 5 ones.
def bb3 : Machine := ofTable
  [ (tr true true 1, tr true true 3)
  , (tr true false 1, tr false true 2)
  , (tr true false 2, tr true false 0)
  , (hlt, hlt) ]

-- BB(4) = 1RB1LB_1LA0LC_1RZ1LD_1RD0RA, 107 steps, 13 ones.
def bb4 : Machine := ofTable
  [ (tr true true 1, tr true false 1)
  , (tr true false 0, tr false false 2)
  , (tr true true 4, tr true false 3)
  , (tr true true 3, tr false true 0)
  , (hlt, hlt) ]

#guard haltAt bb2 100 0 start = some 6
#guard onesAt bb2 100 start = 4
#guard haltAt bb3 200 0 start = some 21
#guard onesAt bb3 200 start = 5
#guard haltAt bb4 500 0 start = some 107
#guard onesAt bb4 500 start = 13

/-! ## The three cryptid candidates

Lines 336, 555 and 1002 of the BB(6) holdout list.  States are numbered
A = 0 .. F = 5; the halt is F on 0, undefined in all three. -/

-- 1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE
def m336 : Machine := ofTable
  [ (tr true true 1,  tr false false 3)
  , (tr true false 2, tr false true 0)
  , (tr true true 0,  tr true false 1)
  , (tr true false 0, tr true false 4)
  , (tr true true 5,  tr false false 2)
  , (hlt,             tr false true 4) ]

-- 1RB1RE_1LC0RA_1RD0LB_1LB1RC_1LF0RD_---0LE
def m555 : Machine := ofTable
  [ (tr true true 1,  tr true true 4)
  , (tr true false 2, tr false true 0)
  , (tr true true 3,  tr false false 1)
  , (tr true false 1, tr true true 2)
  , (tr true false 5, tr false true 3)
  , (hlt,             tr false false 4) ]

-- 1RB1LC_1RC0LD_1LA0RB_1LB1LE_1RF0LA_---0RE
def m1002 : Machine := ofTable
  [ (tr true true 1,  tr true false 2)
  , (tr true true 2,  tr false false 3)
  , (tr true false 0, tr false true 1)
  , (tr true false 1, tr true false 4)
  , (tr true true 5,  tr false false 0)
  , (hlt,             tr false true 4) ]

-- None of them halts early: a machine that did would not be a holdout,
-- and a transcription slip in the tables above would most likely show up
-- as a spurious halt.
#guard haltAt m336 20000 0 start = none
#guard haltAt m555 20000 0 start = none
#guard haltAt m1002 20000 0 start = none

/-- Halting is decided entirely by the transition table. -/
theorem step_none_iff (M : Machine) (c : Cfg) :
    step M c = none ↔ M c.q (scan c) = none := by
  unfold step
  cases h : M c.q (scan c) with
  | none => simp
  | some t => cases h' : t.rt <;> simp [h']

/-- The halt condition, shared by all three machines: state F (= 5) on
    symbol 0.

    The range hypothesis is not decoration.  `ofTable` also returns
    `none` for a state index past the end of the table, so without
    `q < 6` the statement is false -- every out-of-range state would
    count as a halt.  Reachable states are always in range, but that is
    a fact to be carried, not assumed silently. -/
theorem m336_none_iff {q : Nat} (hq : q < 6) (s : Bool) :
    m336 q s = none ↔ (q = 5 ∧ s = false) := by
  match q, s with
  | 0, false | 0, true | 1, false | 1, true | 2, false | 2, true
  | 3, false | 3, true | 4, false | 4, true | 5, true =>
      simp [m336, ofTable, tr]
  | 5, false => simp [m336, ofTable, hlt]
  | (n + 6), _ => exact absurd hq (by omega)

theorem m555_none_iff {q : Nat} (hq : q < 6) (s : Bool) :
    m555 q s = none ↔ (q = 5 ∧ s = false) := by
  match q, s with
  | 0, false | 0, true | 1, false | 1, true | 2, false | 2, true
  | 3, false | 3, true | 4, false | 4, true | 5, true =>
      simp [m555, ofTable, tr]
  | 5, false => simp [m555, ofTable, hlt]
  | (n + 6), _ => exact absurd hq (by omega)

theorem m1002_none_iff {q : Nat} (hq : q < 6) (s : Bool) :
    m1002 q s = none ↔ (q = 5 ∧ s = false) := by
  match q, s with
  | 0, false | 0, true | 1, false | 1, true | 2, false | 2, true
  | 3, false | 3, true | 4, false | 4, true | 5, true =>
      simp [m1002, ofTable, tr]
  | 5, false => simp [m1002, ofTable, hlt]
  | (n + 6), _ => exact absurd hq (by omega)

/-- Restated on configurations: these machines halt exactly when the
    head is in state F reading a 0 -- the E/F gadget's `00`. -/
theorem m336_halt_iff {c : Cfg} (hq : c.q < 6) :
    step m336 c = none ↔ (c.q = 5 ∧ scan c = false) := by
  rw [step_none_iff, m336_none_iff hq]

theorem m555_halt_iff {c : Cfg} (hq : c.q < 6) :
    step m555 c = none ↔ (c.q = 5 ∧ scan c = false) := by
  rw [step_none_iff, m555_none_iff hq]

theorem m1002_halt_iff {c : Cfg} (hq : c.q < 6) :
    step m1002 c = none ↔ (c.q = 5 ∧ scan c = false) := by
  rw [step_none_iff, m1002_none_iff hq]

end Bb6
