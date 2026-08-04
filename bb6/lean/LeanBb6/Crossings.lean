/-
The chain-step table, proved.

`TM.lean` proves that a block crossing repeats; this file supplies the
crossings themselves.  Each is two base steps across a two-cell block,
and every one is discharged by `rfl` -- the configurations are concrete
apart from the surrounding tape, which is exactly what `CrossR` and
`CrossL` quantify over.

GENERATED from the same `macro.inner` the Python simulators use, so the
table cannot drift from the one the measurements were taken with.  Each
crossing additionally carries a `#guard` that runs the machine and
checks it executably, which catches an orientation error
(nearest-head-first vs left-to-right) that a well-typed but wrong
statement would otherwise hide.
-/
import LeanBb6.Machines

namespace Bb6

/-! ### line 336 -/

theorem m336_A_R : CrossR m336 0 [false, true] [true, false] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m336_A_L : CrossL m336 0 [true, false] [false, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m336_B_R : CrossR m336 1 [true, false] [false, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m336_B_L : CrossL m336 1 [false, true] [true, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m336_C_L : CrossL m336 2 [true, false] [true, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m336_D_L : CrossL m336 3 [false, true] [true, false] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m336_E_R : CrossR m336 4 [false, true] [true, false] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m336_F_R : CrossR m336 5 [true, false] [false, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

/-! ### line 555 -/

theorem m555_A_R : CrossR m555 0 [false, true] [true, false] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m555_B_R : CrossR m555 1 [true, false] [false, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m555_B_L : CrossL m555 1 [false, true] [true, false] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m555_C_R : CrossR m555 2 [false, true] [true, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m555_C_L : CrossL m555 2 [true, false] [false, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m555_D_R : CrossR m555 3 [true, false] [true, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m555_E_L : CrossL m555 4 [false, true] [true, false] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m555_F_L : CrossL m555 5 [true, false] [false, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

/-! ### line 1002 -/

theorem m1002_A_L : CrossL m1002 0 [true, false] [true, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m1002_B_R : CrossR m1002 1 [false, true] [true, false] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m1002_B_L : CrossL m1002 1 [true, false] [false, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m1002_C_R : CrossR m1002 2 [true, false] [false, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m1002_C_L : CrossL m1002 2 [false, true] [true, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m1002_D_L : CrossL m1002 3 [false, true] [true, false] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m1002_E_R : CrossR m1002 4 [false, true] [true, false] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

theorem m1002_F_R : CrossR m1002 5 [true, false] [false, true] 2 := by
  intro X Rest
  exact steps_of_runFor 2 _ _ rfl

/-! ## Executable confirmation of every crossing above -/

#guard runFor m336 2 (Cfg.mk [] ([false, true] ++ [true]) 0 true) = some (Cfg.mk (List.reverse [true, false]) [true] 0 true)
#guard runFor m336 2 (Cfg.mk ([true, false] ++ [true]) [] 0 false) = some (Cfg.mk [true] (List.reverse [false, true]) 0 false)
#guard runFor m336 2 (Cfg.mk [] ([true, false] ++ [true]) 1 true) = some (Cfg.mk (List.reverse [false, true]) [true] 1 true)
#guard runFor m336 2 (Cfg.mk ([false, true] ++ [true]) [] 1 false) = some (Cfg.mk [true] (List.reverse [true, true]) 1 false)
#guard runFor m336 2 (Cfg.mk ([true, false] ++ [true]) [] 2 false) = some (Cfg.mk [true] (List.reverse [true, true]) 2 false)
#guard runFor m336 2 (Cfg.mk ([false, true] ++ [true]) [] 3 false) = some (Cfg.mk [true] (List.reverse [true, false]) 3 false)
#guard runFor m336 2 (Cfg.mk [] ([false, true] ++ [true]) 4 true) = some (Cfg.mk (List.reverse [true, false]) [true] 4 true)
#guard runFor m336 2 (Cfg.mk [] ([true, false] ++ [true]) 5 true) = some (Cfg.mk (List.reverse [false, true]) [true] 5 true)
#guard runFor m555 2 (Cfg.mk [] ([false, true] ++ [true]) 0 true) = some (Cfg.mk (List.reverse [true, false]) [true] 0 true)
#guard runFor m555 2 (Cfg.mk [] ([true, false] ++ [true]) 1 true) = some (Cfg.mk (List.reverse [false, true]) [true] 1 true)
#guard runFor m555 2 (Cfg.mk ([false, true] ++ [true]) [] 1 false) = some (Cfg.mk [true] (List.reverse [true, false]) 1 false)
#guard runFor m555 2 (Cfg.mk [] ([false, true] ++ [true]) 2 true) = some (Cfg.mk (List.reverse [true, true]) [true] 2 true)
#guard runFor m555 2 (Cfg.mk ([true, false] ++ [true]) [] 2 false) = some (Cfg.mk [true] (List.reverse [false, true]) 2 false)
#guard runFor m555 2 (Cfg.mk [] ([true, false] ++ [true]) 3 true) = some (Cfg.mk (List.reverse [true, true]) [true] 3 true)
#guard runFor m555 2 (Cfg.mk ([false, true] ++ [true]) [] 4 false) = some (Cfg.mk [true] (List.reverse [true, false]) 4 false)
#guard runFor m555 2 (Cfg.mk ([true, false] ++ [true]) [] 5 false) = some (Cfg.mk [true] (List.reverse [false, true]) 5 false)
#guard runFor m1002 2 (Cfg.mk ([true, false] ++ [true]) [] 0 false) = some (Cfg.mk [true] (List.reverse [true, true]) 0 false)
#guard runFor m1002 2 (Cfg.mk [] ([false, true] ++ [true]) 1 true) = some (Cfg.mk (List.reverse [true, false]) [true] 1 true)
#guard runFor m1002 2 (Cfg.mk ([true, false] ++ [true]) [] 1 false) = some (Cfg.mk [true] (List.reverse [false, true]) 1 false)
#guard runFor m1002 2 (Cfg.mk [] ([true, false] ++ [true]) 2 true) = some (Cfg.mk (List.reverse [false, true]) [true] 2 true)
#guard runFor m1002 2 (Cfg.mk ([false, true] ++ [true]) [] 2 false) = some (Cfg.mk [true] (List.reverse [true, true]) 2 false)
#guard runFor m1002 2 (Cfg.mk ([false, true] ++ [true]) [] 3 false) = some (Cfg.mk [true] (List.reverse [true, false]) 3 false)
#guard runFor m1002 2 (Cfg.mk [] ([false, true] ++ [true]) 4 true) = some (Cfg.mk (List.reverse [true, false]) [true] 4 true)
#guard runFor m1002 2 (Cfg.mk [] ([true, false] ++ [true]) 5 true) = some (Cfg.mk (List.reverse [false, true]) [true] 5 true)

/-! ## The chain lemma firing on real machines

Each line below turns a two-step check into a statement about arbitrarily
long stretches of tape: `n` copies of the block are crossed in `2n` steps,
for every `n`, with the surrounding tape arbitrary.  That is the whole
point of the exercise -- the macro simulator's chain step, as a theorem.

These are the crossings the inner unit is built from: the machine
converts `01` to `10` (or its mirror), which is the transport that moves
one unit of a counter from one block to another. -/

theorem m336_sweep (n : Nat) (L Rest : List Bool) :
    Steps m336 (n * 2) (Cfg.mk L (rep [false, true] n ++ Rest) 0 true)
      (Cfg.mk ((rep [true, false] n).reverse ++ L) Rest 0 true) :=
  crossR_rep m336_A_R n L Rest

theorem m555_sweep (n : Nat) (L Rest : List Bool) :
    Steps m555 (n * 2) (Cfg.mk L (rep [false, true] n ++ Rest) 0 true)
      (Cfg.mk ((rep [true, false] n).reverse ++ L) Rest 0 true) :=
  crossR_rep m555_A_R n L Rest

theorem m1002_sweep (n : Nat) (R Rest : List Bool) :
    Steps m1002 (n * 2) (Cfg.mk (rep [true, false] n ++ Rest) R 0 false)
      (Cfg.mk Rest ((rep [true, true] n).reverse ++ R) 0 false) :=
  crossL_rep m1002_A_L n R Rest

/-! Ten copies crossed in twenty steps, computed -- the chain lemma and
the machine agreeing on a case big enough to be a real check. -/

#guard runFor m336 20 (Cfg.mk [] (rep [false, true] 10 ++ [true]) 0 true)
    = some (Cfg.mk ((rep [true, false] 10).reverse) [true] 0 true)

end Bb6
