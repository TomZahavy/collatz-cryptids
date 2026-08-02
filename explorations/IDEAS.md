# Out-of-the-box next steps (zoom-out, July 2026)

Reviewing the meta report + 4 machines + Hydra/Needle, what we have NOT tried:

1. **Matthews-Watts multiplier / generalized-Collatz drift dichotomy.**
   The gen-Collatz literature (Matthews-Watts 1984, in Lagarias's book) predicts
   eventual-cyclic (contracting) vs divergent (expanding) from the geometric-mean
   multiplier of the return map. Our divergent (1,3,Needle) vs convergent (2,4)
   dichotomy should map onto super-critical (drift>0) vs critical (drift=0).
   NEW: prove the convergent machines are EXACTLY critical (geo-mean multiplier=1),
   which explains linear growth structurally. Connect P8 to established theory.

2. **The mantissa stationary density (machine 1's open "backbone").**
   Our report flagged: frac(log2 D_k) is NOT uniform (chi^2~162) and "the true
   density is the missing ergodic backbone." NOBODY computed it. Attack directly:
   high-resolution empirical density + try to identify it (piecewise? related to
   the branch-word structure?). Attacks a stated open problem from our own work.

3. **Perfect powers in the orbit (machine 3 / Space Needle) via Baker/BHV.**
   Halting = "orbit value is an exact power of q". This is literally the
   "perfect powers in a sequence" problem (Baker's method, Bilu-Hanrot-Voutier).
   Check whether any subsequence is a linear recurrence / S-unit; set up the
   linear-form-in-logs and estimate the Baker bound; at minimum characterize
   rigorously WHY no congruence separates (valuation orthogonal to residues).

4. **Backward reachability from the halting set (the reverse decider).**
   bbchallenge's backward-reasoning/halting-segment applied to our explicit H.
   Compute preimage tree of H; if the start is provably outside the
   backward-reachable set, non-halting is PROVED.

5. **Self-similarity / renormalization.** Is the return map to a sub-region
   conjugate to the whole map? Would enable induction.

---
## STATUS (all tried)
1. Drift dichotomy -> Finding 1 (correction, folded into meta).
2. Mantissa backbone -> Finding 2 (circle map, breakpoint log2(5/4), transfer operator).
3. No-congruence for multiplicative -> Finding 3 (theorem).
4. Backward reachability -> Finding 5 (halting set ~log-many, start excluded).
5. Self-similarity -> Finding 4 (step(2b)=step(b)+b+1).
+ Baker/perfect-powers -> Finding 6 (orbit not S-unit; per-run LTE finiteness;
  unconditional no-interior-of-run halts; obstruction = unbounded branch words).
What's left: the open problem itself.
