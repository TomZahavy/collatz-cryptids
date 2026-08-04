/-
The unit lemma for line 336: one turn of the inner loop, for every value
of the counter, with the surrounding tape arbitrary.

THE DECOMPOSITION.  Traced at several counter values, one unit is

    prologue        4 steps      fixed
    chain right     2(x+2)       x+2 crossings of 01 -> 10
    turnaround      2 steps      fixed
    chain left      2(x+1)       x+1 crossings of 10 -> 01
                    ---------
                    4x + 12

Both chains are crossings already proved in `Crossings.lean`, so the work
here is bookkeeping: rewriting the tape between fragments so the next
fragment's pattern is exposed.  That is what the `shift` lemmas are for.
The two block words in play, `10` and `01`, are each other's shift, and
the whole proof turns on moving one cell across a run.
-/
import LeanBb6.Crossings

namespace Bb6

/-! ## List algebra

Kept separate and general.  Proved inline inside the main argument these
inductions capture the surrounding hypotheses and become unusable. -/

/-- A repeated block commutes with one more copy of itself. -/
theorem rep_snoc (u : List Bool) : ∀ n, rep u n ++ u = u ++ rep u n := by
  intro n
  induction n with
  | zero => show [] ++ u = u ++ []; rw [List.nil_append, List.append_nil]
  | succ k ih =>
      show (u ++ rep u k) ++ u = u ++ (u ++ rep u k)
      rw [List.append_assoc, ih]

/-- Reversing a repeated block reverses the block. -/
theorem rev_rep (u : List Bool) : ∀ n, (rep u n).reverse = rep u.reverse n := by
  intro n
  induction n with
  | zero => rfl
  | succ k ih =>
      show (u ++ rep u k).reverse = _
      rw [List.reverse_append, ih]
      exact rep_snoc u.reverse k

theorem rev_rep_10 (n : Nat) :
    (rep [true, false] n).reverse = rep [false, true] n := rev_rep _ n

theorem rev_rep_01 (n : Nat) :
    (rep [false, true] n).reverse = rep [true, false] n := rev_rep _ n

/-- THE SHIFT.  A `0` in front of a run of `10`s is a `0` behind a run of
    `01`s.  Everything below is this fact applied in one direction or the
    other. -/
theorem shift_10 (n : Nat) (T : List Bool) :
    false :: (rep [true, false] n ++ T)
      = rep [false, true] n ++ (false :: T) := by
  induction n with
  | zero => rfl
  | succ k ih =>
      show false :: true :: false :: (rep [true, false] k ++ T)
        = false :: true :: (rep [false, true] k ++ (false :: T))
      rw [← ih]

theorem shift_01 (n : Nat) (T : List Bool) :
    true :: (rep [false, true] n ++ T)
      = rep [true, false] n ++ (true :: T) := by
  induction n with
  | zero => rfl
  | succ k ih =>
      show true :: false :: true :: (rep [false, true] k ++ T)
        = true :: false :: (rep [true, false] k ++ (true :: T))
      rw [← ih]

/-! ## Normalising the tape between fragments -/

/-- After the prologue the right-hand tape is `010` followed by the old
    contents; this is the same thing written as a run of `01`s, which is
    the pattern the rightward chain consumes. -/
theorem norm_right (x b : Nat) (Rr : List Bool) :
    false :: true :: false ::
        (rep [true, false] x ++ (rep [true, true] (b + 1) ++ Rr))
      = rep [false, true] (x + 2)
          ++ (true :: (rep [true, true] b ++ Rr)) := by
  rw [shift_10 x (rep [true, true] (b + 1) ++ Rr)]
  show [false, true] ++ (rep [false, true] x
        ++ ([false, true] ++ (true :: (rep [true, true] b ++ Rr))))
    = [false, true] ++ ([false, true] ++ rep [false, true] x)
        ++ (true :: (rep [true, true] b ++ Rr))
  rw [← List.append_assoc (rep [false, true] x) [false, true],
      rep_snoc [false, true] x]
  simp [List.append_assoc]

/-- Before the leftward chain the left-hand tape is a `1` in front of a
    run of `01`s; the chain consumes `10`s, so it is shifted. -/
theorem norm_left (x : Nat) (T : List Bool) :
    true :: (rep [false, true] (x + 1) ++ T)
      = rep [true, false] (x + 1) ++ (true :: T) := shift_01 (x + 1) T

/-! ## The unit lemma -/

/-- ONE TURN OF THE INNER LOOP, for every counter value `x`, every pair
    of surrounding block counts `a` and `b`, and arbitrary tape beyond
    them.  The machine takes one block from each side and gives two to
    the middle, in exactly `4x + 12` steps.

    This is the statement the Python side verified on 54 independent
    instances; here it is proved for all of them. -/
theorem m336_unit (x a b : Nat) (Lr Rr : List Bool) :
    Steps m336 (4 * x + 12)
      (Cfg.mk ([true, true] ++ (rep [true, false] (a + 1) ++ Lr))
              (rep [true, false] x ++ (rep [true, true] (b + 1) ++ Rr))
              0 false)
      (Cfg.mk ([true, true] ++ (rep [true, false] a ++ Lr))
              (rep [true, false] (x + 2) ++ (rep [true, true] b ++ Rr))
              0 false) := by
  -- fragment 1: the prologue, four steps, computed by the kernel
  have p1 : Steps m336 4
      (Cfg.mk ([true, true] ++ (rep [true, false] (a + 1) ++ Lr))
              (rep [true, false] x ++ (rep [true, true] (b + 1) ++ Rr))
              0 false)
      (Cfg.mk (true :: (rep [true, false] a ++ Lr))
              (false :: true :: false ::
                (rep [true, false] x ++ (rep [true, true] (b + 1) ++ Rr)))
              0 true) := steps_of_runFor 4 _ _ rfl
  -- expose the run of 01s that the rightward chain consumes
  rw [norm_right x b Rr] at p1
  -- fragment 2: the rightward chain, x+2 crossings
  have p2 := crossR_rep m336_A_R (x + 2) (true :: (rep [true, false] a ++ Lr))
      (true :: (rep [true, true] b ++ Rr))
  rw [rev_rep_10 (x + 2)] at p2
  -- fragment 3: the turnaround, two steps, computed
  have p3 : Steps m336 2
      (Cfg.mk (rep [false, true] (x + 2) ++ (true :: (rep [true, false] a ++ Lr)))
              (true :: (rep [true, true] b ++ Rr)) 0 true)
      (Cfg.mk (true :: (rep [false, true] (x + 1)
                 ++ (true :: (rep [true, false] a ++ Lr))))
              (true :: false :: (rep [true, true] b ++ Rr)) 0 false) :=
    steps_of_runFor 2 _ _ rfl
  -- expose the run of 10s that the leftward chain consumes
  rw [norm_left x (true :: (rep [true, false] a ++ Lr))] at p3
  -- fragment 4: the leftward chain, x+1 crossings
  have p4 := crossL_rep m336_A_L (x + 1)
      (true :: false :: (rep [true, true] b ++ Rr))
      (true :: (true :: (rep [true, false] a ++ Lr)))
  rw [rev_rep_01 (x + 1)] at p4
  -- compose the four fragments
  have key := Steps.trans p1 (Steps.trans p2 (Steps.trans p3 p4))
  have hcount : 4 + ((x + 2) * 2 + (2 + (x + 1) * 2)) = 4 * x + 12 := by omega
  rw [hcount] at key
  -- reconcile the two ways of writing the final right-hand tape
  have hr : rep [true, false] (x + 1)
        ++ (true :: false :: (rep [true, true] b ++ Rr))
      = rep [true, false] (x + 2) ++ (rep [true, true] b ++ Rr) := by
    show _ = ([true, false] ++ rep [true, false] (x + 1))
        ++ (rep [true, true] b ++ Rr)
    rw [← rep_snoc [true, false] (x + 1), List.append_assoc]
    rfl
  rw [hr] at key
  exact key

/-! The same statement, checked executably at two concrete instances.
The proof above establishes it for all of them; these would catch a
statement that is provable but not the one intended. -/

#guard runFor m336 (4 * 3 + 12)
    (Cfg.mk ([true, true] ++ (rep [true, false] 5 ++ [true, true, false, false]))
            (rep [true, false] 3 ++ (rep [true, true] 6 ++ [false, false, true, true]))
            0 false)
  = some (Cfg.mk ([true, true] ++ (rep [true, false] 4 ++ [true, true, false, false]))
            (rep [true, false] 5 ++ (rep [true, true] 5 ++ [false, false, true, true]))
            0 false)

#guard runFor m336 (4 * 7 + 12)
    (Cfg.mk ([true, true] ++ (rep [true, false] 3 ++ [false, true]))
            (rep [true, false] 7 ++ (rep [true, true] 4 ++ [true, false]))
            0 false)
  = some (Cfg.mk ([true, true] ++ (rep [true, false] 2 ++ [false, true]))
            (rep [true, false] 9 ++ (rep [true, true] 3 ++ [true, false]))
            0 false)

/-! ## Iterating the unit

The cost of `n` units is given recursively rather than in closed form,
because each unit is more expensive than the last: the swept block has
grown by two.  The closed form is proved just below. -/

def unitCost (x : Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => (4 * x + 12) + unitCost (x + 2) n

/-- `n` turns of the inner loop.  Each turn moves one block from each
    side into the middle, so after `n` of them the middle has grown by
    `2n` and each side has shrunk by `n`. -/
theorem m336_units : ∀ (n x a b : Nat) (Lr Rr : List Bool),
    Steps m336 (unitCost x n)
      (Cfg.mk ([true, true] ++ (rep [true, false] (a + n) ++ Lr))
              (rep [true, false] x ++ (rep [true, true] (b + n) ++ Rr))
              0 false)
      (Cfg.mk ([true, true] ++ (rep [true, false] a ++ Lr))
              (rep [true, false] (x + 2 * n) ++ (rep [true, true] b ++ Rr))
              0 false) := by
  intro n
  induction n with
  | zero =>
      intro x a b Lr Rr
      show Steps m336 0 _ _
      simp only [Nat.add_zero, Nat.mul_zero]
      exact Steps.zero _
  | succ k ih =>
      intro x a b Lr Rr
      have one := m336_unit x (a + k) (b + k) Lr Rr
      have rest := ih (x + 2) a b Lr Rr
      have hstep := Steps.trans one rest
      have hx : x + 2 + 2 * k = x + 2 * (k + 1) := by omega
      rw [hx] at hstep
      have ha : a + k + 1 = a + (k + 1) := by omega
      have hb : b + k + 1 = b + (k + 1) := by omega
      rw [ha, hb] at hstep
      exact hstep

/-- The closed form: `n` units cost `4nx + 4n^2 + 8n` steps.  The
    quadratic term is the price of the middle block growing under the
    head. -/
theorem unitCost_closed : ∀ (n x : Nat),
    unitCost x n = 4 * n * x + 4 * n * n + 8 * n := by
  intro n
  induction n with
  | zero =>
      intro x
      show (0 : Nat) = _
      simp
  | succ k ih =>
      intro x
      show (4 * x + 12) + unitCost (x + 2) k = _
      rw [ih (x + 2)]
      simp only [Nat.succ_mul, Nat.mul_succ, Nat.mul_add, Nat.add_mul]
      omega

end Bb6
