/-
Turing machines, mathlib-free, with the block-crossing lemma.

WHY THE HEAD SITS BETWEEN CELLS.  The first version of this file put the
head ON a cell and proved a sweep lemma for a state that re-enters itself
in the same direction.  That lemma is correct and useless here: NONE of
the three machines has such a transition at cell level.  Checked, on the
transition tables -- every state moves to a different state.  That is
precisely why the Python side had to go to macro machines: a self-loop
that does not exist at cell level appears once cells are grouped into
blocks.

So the object to prove things about is a BLOCK CROSSING: a fixed word `u`
of length p which, entered in state q from the left, is left in state q
from the right, rewritten as `v`, in p steps.  Iterating that across
`u^n` is the chain step, and it is what the unit lemma is built from.

With the head between cells, facing a direction, a block crossing is
literally list concatenation -- `right = u ++ Rest` becomes
`right = Rest` -- so the induction goes through with no index
arithmetic.  With the head on a cell it does not, because the scanned
cell has to be peeled off the front of every statement.  The
representation is the proof strategy.

THE MODEL.  `left` and `right` list the tape outward from the head,
NEAREST CELL FIRST.  Facing right, the machine reads the head of
`right`; facing left, the head of `left`.  Unwritten tape reads `false`,
which `hd []` supplies, so the bi-infinite blank tape needs no special
case.  One step pops from the side being read and pushes the written
cell onto the side the head is leaving.
-/

namespace Bb6

/-- One transition: symbol written, whether the head moves right, next
    state. -/
structure Tr where
  wr : Bool
  rt : Bool
  nx : Nat
deriving DecidableEq, Repr

/-- A machine: a transition for each state and scanned symbol, or
    nothing, which means it halts. -/
def Machine := Nat → Bool → Option Tr

/-- A configuration.  The head is between `left` and `right`, facing
    `d` (true = right), and reads the nearest cell on that side. -/
structure Cfg where
  left : List Bool
  right : List Bool
  q : Nat
  d : Bool
deriving DecidableEq, Repr

def hd : List Bool → Bool
  | [] => false
  | b :: _ => b

def tl : List Bool → List Bool
  | [] => []
  | _ :: t => t

@[simp] theorem hd_cons (b : Bool) (l : List Bool) : hd (b :: l) = b := rfl
@[simp] theorem tl_cons (b : Bool) (l : List Bool) : tl (b :: l) = l := rfl

/-- The cell the head is about to read. -/
def scan (c : Cfg) : Bool :=
  if c.d then hd c.right else hd c.left

/-- One step.  The cell read is popped from the side being faced; the
    cell written is pushed onto the side the head leaves, which is the
    side OPPOSITE the direction of motion. -/
def step (M : Machine) (c : Cfg) : Option Cfg :=
  match M c.q (scan c) with
  | none => none
  | some t =>
      let l := if c.d then c.left else tl c.left
      let r := if c.d then tl c.right else c.right
      if t.rt then
        some ⟨t.wr :: l, r, t.nx, true⟩
      else
        some ⟨l, t.wr :: r, t.nx, false⟩

/-- `Steps M n a b`: exactly `n` steps from `a` to `b`, halting nowhere
    in between. -/
inductive Steps (M : Machine) : Nat → Cfg → Cfg → Prop
  | zero (c : Cfg) : Steps M 0 c c
  | succ {n : Nat} {a b c : Cfg} :
      step M a = some b → Steps M n b c → Steps M (n + 1) a c

theorem Steps.one {M : Machine} {a b : Cfg} (h : step M a = some b) :
    Steps M 1 a b :=
  Steps.succ h (Steps.zero b)

/-- Runs compose and step counts add. -/
theorem Steps.trans {M : Machine} :
    ∀ {m n : Nat} {a b c : Cfg}, Steps M m a b → Steps M n b c →
      Steps M (m + n) a c := by
  intro m n a b c hab hbc
  induction hab with
  | zero x => simpa using hbc
  | succ h _ ih =>
      rw [Nat.succ_add]
      exact Steps.succ h (ih hbc)

/-- Never halting, as the property the theorems will actually supply:
    runs of every length exist. -/
def NeverHalts (M : Machine) (c : Cfg) : Prop :=
  ∀ n : Nat, ∃ d : Cfg, Steps M n c d

/-! ## Crossing a repeated block

`CrossR M q u v k` says: entered in state `q` facing right with `u` at
the front of the tape, the machine emerges `k` steps later in state `q`
still facing right, having replaced `u` by `v` and consumed nothing
else.  The quantification over `L` and `Rest` is what makes it a
statement about the block alone, independent of its surroundings -- and
that independence is exactly what licenses repeating it. -/

def CrossR (M : Machine) (q : Nat) (u v : List Bool) (k : Nat) : Prop :=
  ∀ L Rest : List Bool,
    Steps M k ⟨L, u ++ Rest, q, true⟩ ⟨v.reverse ++ L, Rest, q, true⟩

def CrossL (M : Machine) (q : Nat) (u v : List Bool) (k : Nat) : Prop :=
  ∀ R Rest : List Bool,
    Steps M k ⟨u ++ Rest, R, q, false⟩ ⟨Rest, v.reverse ++ R, q, false⟩

/-- `u` repeated `n` times. -/
def rep (u : List Bool) : Nat → List Bool
  | 0 => []
  | n + 1 => u ++ rep u n

@[simp] theorem rep_zero (u : List Bool) : rep u 0 = [] := rfl
theorem rep_succ (u : List Bool) (n : Nat) : rep u (n + 1) = u ++ rep u n := rfl

theorem rep_append (u : List Bool) (n : Nat) (Rest : List Bool) :
    rep u (n + 1) ++ Rest = u ++ (rep u n ++ Rest) := by
  show (u ++ rep u n) ++ Rest = _
  exact List.append_assoc u (rep u n) Rest

theorem reverse_rep_append (v : List Bool) (n : Nat) (L : List Bool) :
    (rep v n).reverse ++ (v.reverse ++ L) = (rep v (n + 1)).reverse ++ L := by
  show _ = (v ++ rep v n).reverse ++ L
  rw [List.reverse_append, List.append_assoc]

/-- THE CHAIN LEMMA.  A block crossing repeats: `n` copies of `u` are
    crossed in `n * k` steps and come out as `n` copies of `v`.  This is
    the macro simulator's chain step, proved once, for an arbitrary
    machine and an arbitrary block. -/
theorem crossR_rep {M : Machine} {q : Nat} {u v : List Bool} {k : Nat}
    (h : CrossR M q u v k) :
    ∀ n L Rest, Steps M (n * k) ⟨L, rep u n ++ Rest, q, true⟩
      ⟨(rep v n).reverse ++ L, Rest, q, true⟩ := by
  intro n
  induction n with
  | zero =>
      intro L Rest
      simp only [Nat.zero_mul, rep_zero, List.nil_append, List.reverse_nil]
      exact Steps.zero _
  | succ j ih =>
      intro L Rest
      rw [rep_append u j Rest]
      have h1 := h L (rep u j ++ Rest)
      have h2 := ih (v.reverse ++ L) Rest
      have := Steps.trans h1 h2
      rw [reverse_rep_append v j L] at this
      have harith : k + j * k = (j + 1) * k := by
        rw [Nat.succ_mul]
        exact Nat.add_comm k (j * k)
      rw [harith] at this
      exact this

/-- The mirror image. -/
theorem crossL_rep {M : Machine} {q : Nat} {u v : List Bool} {k : Nat}
    (h : CrossL M q u v k) :
    ∀ n R Rest, Steps M (n * k) ⟨rep u n ++ Rest, R, q, false⟩
      ⟨Rest, (rep v n).reverse ++ R, q, false⟩ := by
  intro n
  induction n with
  | zero =>
      intro R Rest
      simp only [Nat.zero_mul, rep_zero, List.nil_append, List.reverse_nil]
      exact Steps.zero _
  | succ j ih =>
      intro R Rest
      rw [rep_append u j Rest]
      have h1 := h R (rep u j ++ Rest)
      have h2 := ih (v.reverse ++ R) Rest
      have := Steps.trans h1 h2
      rw [reverse_rep_append v j R] at this
      have harith : k + j * k = (j + 1) * k := by
        rw [Nat.succ_mul]
        exact Nat.add_comm k (j * k)
      rw [harith] at this
      exact this

end Bb6
