import LeanBbf.Runner
import LeanBbf.M431
namespace Demo
open Fractran Fractran.M431

-- All six of M431's firing lemmas, re-derived from the GENERIC lemma.
-- Each is now: exhibit the machine as pre ++ r :: post, discharge the
-- disabled-guards by `simp`+`omega`, discharge r's own guard likewise.

theorem fire0' (a b c d e : Nat) :
    step M431 ⟨a + 1, b + 1, c, d, e⟩ = some ⟨a, b, c + 1, d, e⟩ :=
  step_of_first [] f0 [f1, f2, f3, f4] (by simp) (by simp [f0] <;> omega)

theorem fire1' (a c d e : Nat) :
    step M431 ⟨a, 0, c + 1, d + 1, e⟩ = some ⟨a, 2, c, d, e⟩ :=
  step_of_first [f0] f1 [f2, f3, f4] (by simp [f0]) (by simp [f1] <;> omega)

theorem fire2' (a c e : Nat) :
    step M431 ⟨a, 0, c + 1, 0, e + 1⟩ = some ⟨a + 3, 0, c, 0, e⟩ :=
  step_of_first [f0, f1] f2 [f3, f4] (by simp [f0, f1]) (by simp [f2] <;> omega)

theorem fire3' (a d e : Nat) :
    step M431 ⟨a + 1, 0, 0, d, e⟩ = some ⟨a, 0, 0, d + 1, e⟩ :=
  step_of_first [f0, f1, f2] f3 [f4] (by simp [f0, f1, f2]) (by simp [f3] <;> omega)

theorem fire4' (d e : Nat) :
    step M431 ⟨0, 0, 0, d + 1, e⟩ = some ⟨0, 0, 1, d, e + 2⟩ :=
  step_of_first [f0, f1, f2, f3] f4 [] (by simp [f0, f1, f2, f3]) (by simp [f4] <;> omega)

end Demo
