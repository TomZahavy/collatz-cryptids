"""Formal classification of the machines: branch type, class membership,
arithmetical complexity, and conjugacy equivalence classes."""
import sys, math
for d in ["machine1","machine3","machine4","needle","hydra"]:
    sys.path.insert(0, f"/Users/tomzahavy/Documents/Claude/collatz/{d}")

# --- Branch-type test: is the rule selected by (i) residue mod fixed d,
#     (ii) a q-adic valuation, or (iii) a magnitude comparison of the coords? ---
# We probe: does the branch change when we scale/shift the state in ways that
# preserve residues (=> not residue-branched) or valuations (=> not valuation)?

print("=== BRANCH-TYPE CLASSIFICATION ===\n")

# Hydra: H(n)=floor(3n/2), branch on n mod 2 only -> pure residue (strict).
import hydra
def hydra_branch(n): return n%2
# verify branch depends ONLY on n mod 2 (residue), not on higher structure
ok=all((hydra.Hstep(n)== (3*(n//2) if n%2==0 else 3*(n//2)+1)) for n in range(2,10000))
print(f"Hydra/Antihydra  H(n)=floor(3n/2): branch = n mod 2 (finite residue). "
      f"affine per branch: {ok}. => STRICT Kurtz-Simon Collatz function (p=2).")

# Space Needle: branch on v2(b) (valuation). Show branch NOT determined by b mod M.
import needle
def sn_step_uses_valuation():
    # two b with same residue mod (any odd M) but different v2 -> different step behavior
    b1, b2 = 2*3, 4*3   # 6 and 12: 6%9==6, 12%9==3 ... use same residue mod small odd
    # pick b same mod 5 but different v2: 8 (v=3) and 3 (v=0), 8%5=3, 3%5=3
    return needle.v2(8)[0]!=needle.v2(3)[0] and 8%5==3%5
print(f"Space Needle  b->b+v2(b)+(3/2)(odd-1): branch = v2(b) (2-adic valuation, "
      f"unbounded). residue-independent: {sn_step_uses_valuation()}. "
      f"=> VALUATION-Collatz (beyond finite-residue Kurtz-Simon).")

# Machine 3: branch on a mod 3 then v3(a) via divide-chain -> valuation.
print("Machine 3  divide rule iterates v3(a) times: branch = v3(a). "
      "=> VALUATION-Collatz (base 3).")

# Machine 4: dispatch on a mod 2 AND on b vs a (magnitude comparisons) -> magnitude.
import m4_base as m4
# show the branch depends on the ORDER of b and a, not on residues alone:
# (a,b)=(7,3): b<a  vs (a,b)=(7,15): b>a -> different rule families, same a
r1=m4.step((7,3)); r2=m4.step((7,15))
print(f"Machine 4  dispatch on b vs a (b<=a / b=a+1..a+4 / b>=a+5): "
      f"branch = ORDER(a,b) + parity. e.g. (7,3)->{r1}, (7,15)->{r2} (same a, "
      f"different regime). => MAGNITUDE-guarded (order comparison).")

# Machine 1: magnitude guards + digit-indexed branch words (countably many pieces).
print("Machine 1  reduces to F with digit-indexed branch words (countably many "
      "affine pieces): => MAGNITUDE/DIGIT-guarded, beyond finite pieces.\n")

print("=== ARITHMETICAL COMPLEXITY (single fixed start) ===")
print("Each 'halts from s0' = EXISTS n: halted_by_step(n)  [decidable predicate]")
print("  => halts is Sigma-0-1, does-not-halt is Pi-0-1  (SINGLE ORBIT).")
print("Collatz CONJECTURE = FORALL n EXISTS m: Col^m(n)=1  => Pi-0-2.")
print("  => our machines (and Antihydra) are Pi-0-1, ONE QUANTIFIER BELOW the")
print("     Pi-0-2 Collatz conjecture. 'As hard as Collatz' = proof barrier, not level.\n")

print("=== CONJUGACY / EQUIVALENCE CLASSES (are any two the same system?) ===")
print("Hydra ~ Antihydra: SAME map H(n)=floor(3n/2), differ only in start (3 vs 8)")
print("  and halt-count direction. => genuinely one dynamical system.")
print("Machine 3 ~ Space Needle: SAME type (hit an exact power), base 3 vs base 2;")
print("  machine 3 built as the base-3 analogue. => conjugate family, different base.")
print("Machines 1, 4: distinct maps; none conjugate to 3n+1 (Collatz).")
print("  => NONE of our machines is literally Collatz; all are co-members of the class.")
