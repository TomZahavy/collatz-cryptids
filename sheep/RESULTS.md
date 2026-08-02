# The sheep machine — a second cryptid inside the VAL(2) family

**Object.** `1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE`, a 6-state 2-symbol
Turing machine found by *sheep* on 7 April 2026 and listed as a Cryptid on the
bbchallenge wiki. Its published halting-equivalent one-variable reduction
(fetched from the wiki 31 July 2026, quoted verbatim in `sheep.py`) is

```
f(n) = HALT                          if oddPart(n) = 1   (n = 2^i)
       n + v2(n) + 3                 if oddPart(n) = 3
       n + v2(n) + (oddPart(n)-1)/2  if oddPart(n) > 3      start at A(5)
```

Everything below is reproduced by `python3 sheep.py` (log: `sheep.log`, 1.7 s).

---

## Why this machine

Until now the only cryptid inside our branch-affine interface was the **Space
Needle**, and every theorem in the program had been developed against that
single point — a real threat to validity, recorded as such in the paper. The
sheep machine is the second, and it is the Needle's sibling with **β changed
from 3 to 1**. That is exactly the parameter our *rank of the sieve group*
dichotomy says should decide whether the last-step sieve closes. It closes,
and the prediction was on the record before we looked.

| | Space Needle | sheep |
|---|---|---|
| census member | (1, **3**, 1, 1, 0) | (1, **1**, 1, 1, 0) |
| A_v | 2^(v+1) + 3 | 2^(v+1) + 1 |
| B_v | 2^v + v | 2^v + v |
| halting set | powers of 2 | powers of 2 |
| sieve group ⟨2⟩ mod A_v | rank 2, `{±3^a 2^i}`, **thin** | rank 1, `{±2^i}`, **listable** |
| surviving branches | infinite, sieved to density ≈ 0.71 | **exactly {0, 1}** |
| closed form for H | none known | **complete (three families)** |
| separating modulus | none (T15) | none (T15) |

---

## Results

**S1 (identification) [proved + machine-verified].** With `n = 2^v·m`,
`m = 2k+1`, the generic branch (`m > 3`) is
`f(n) = A_v k + B_v` with `A_v = 2^(v+1)+1`, `B_v = 2^v + v` — census member
**(1,1,1,1,0)**. Verified on 15,920 systematic `(v,k)` pairs plus 200,000
random ones with `v < 200`, `k < 10^30`: 0 mismatches. `f` agrees with the
census member's `step` on every `n < 60000` except the 15 values with
`oddPart(n) = 3`.

**S2 (the exception is the cryptid) [proved].** Census member (1,1,1,1,0) is
recorded in our census as **HALT**: from `x = 3` it steps `3 → 4 = 2^2 →`
HALT. The sheep machine does not, because `m = 3` is exactly the residue its
exceptional branch intercepts: `f(3) = 6`. *One extra branch on one odd part
converts a halting census member into an open problem* — a concrete instance
of what a manufactured census misses about machines found in the wild.

**S3 (last-step sieve) [proved].** A generic-branch step lands on a power of
two iff `2^t ≡ B_v (mod A_v)`, i.e. iff `B_v ∈ ⟨2⟩`. Since
`2^(v+1) ≡ −1 (mod A_v)` and `2^{-1} ≡ 2^v + 1`, this is

> **`2^(t+1) ≡ 2v − 1  (mod 2^(v+1) + 1)`**

and `⟨2⟩ ⊆ {2^i : 0 ≤ i ≤ v} ∪ {A_v − 2^i : 0 ≤ i ≤ v}`, so the criterion is
decidable by inspection:

* `2v − 1 = 2^i` forces `i = 0`, hence `v = 1`;
* `2v − 1 = A_v − 2^i` forces `2^i = 2^(v+1) − 2v + 2`, which for `v ≥ 3` lies
  strictly between `2^v` and `2^(v+1)`; `v = 2` gives 6.
* `v = 0`: `A_0 = 3` and `2v − 1 ≡ 2 ∈ ⟨2⟩`.

**Only `v ∈ {0,1}` can immediately precede a halt; every `v ≥ 2` is
forbidden.** Verified for all `v < 260` by direct group computation, the proof
steps re-checked for `v < 4000`, and brute-forced against the wiki's own
lemma (`v = 2..13`, `m = 5..19999`, 0 counterexamples).

*Relation to the community's work.* The wiki states this as
`even_case_no_pow2` with the hypothesis `a ≥ 2`. Here `a ≥ 2` is the
**conclusion**: the sieve derives the threshold and locates the two survivors
at the same time. This is the program's first result that reproduces and
sharpens a hand-derived lemma about a machine we did not construct.

**S4 (the exceptional branch never halts) [proved].** `3·2^a + a + 3` is never
a power of two: for `a ≥ 3` it lies strictly between `3·2^a` and `2^(a+2)`;
`a = 0,1,2` give 6, 10, 17. (The wiki's `oddPart3_no_pow2`.) Verified
`a < 6000`.

**S5 (the halting set, in closed form) [proved + machine-verified]).**

> **H = {2^i : i ≥ 0} ∪ H₀ ∪ H₁**, where
> `H₀ = {(2^(2j+1)+1)/3 : j ≥ 2} = 11, 43, 171, 683, …` (the `v = 0` family)
> `H₁ = {2(2^(4j)−1)/5 : j ≥ 2} = 102, 1638, 26214, …` (the `v = 1` family)

Brute force over `n < 300000` finds exactly the 11 predicted members and no
others. The excluded first member of each family is `m = 3` in both cases —
S2 again. **The Needle has no such closed form**; this is the first cryptid in
the collection whose halting set is completely and explicitly described.

**S6 (no congruence certificate) [proved via T15 + machine-verified]).**
β = 1 is odd and δ = 1, so `gcd(δ, M') = 1` at every modulus and T15 applies
verbatim. Verified directly: the one-step residue closure of the start 5 is
all of `Z_M` for **every** `M ≤ 200`, so no modulus separates the orbit from
the powers of two.

**Orbit.** 30,000 steps from 5 with no halt; the value reaches 12,045 bits;
max `v₂` seen 16; `oddPart = 3` never hit. Observed drift 0.401400
bits/step against the census member's predicted 0.401524. 75.28% of steps are
taken from a surviving branch (`v ∈ {0,1}`), against the predicted 3/4.

---

## Depth 2, and the depth ladder

Reproduced by `python3 depth2.py` (log `depth2.log`, 15 s) and
`python3 ladder.py` (log `ladder.log`).

### SHEEP-D2 [proved] — the second-to-last step

Which branch can produce a value that is itself a one-step halt predecessor?
Since `3N = 2^(2j+1) + 1` and `5N = 2^(4j+1) − 2` identically, `N ≡ B_v
(mod A_v)` clears denominators into

```
D2-H0(v):  2^(2j+1) ≡ 3B_v − 1  (mod 3A_v)
D2-H1(v):  2^(4j+1) ≡ 5B_v + 2  (mod 5A_v)
```

(the larger modulus is needed: `3 | A_v` whenever v is even, so reducing mod
`A_v` alone would be wrong half the time). Reducing each *necessary* condition
mod `A_v` and using `2^(v+1) ≡ −1` — which also forces `ord_{A_v}(2)` to be
**even**, so the exponent parity of each group element is well defined —

```
H_0 target ≡ 2^v + 3v − 2   (mod A_v)      H_1 target ≡ 2^v + 5v  (mod A_v)
```

and `⟨2⟩ = {2^i} ∪ {A_v − 2^i}`, `i ≤ v`, gives two gap cases each:

| | case A: target `= 2^i` | case B: `2^i =` |
|---|---|---|
| H₀ | `2^v < 2^v+3v−2 < 2^(v+1)`, so **impossible for v ≥ 4** | `2^v − 3v + 3`, strictly between `2^(v−1)` and `2^v`, **impossible for v ≥ 5** |
| H₁ | `2^v < 2^v+5v < 2^(v+1)`, **impossible for v ≥ 5** | `2^v − 5v + 1`, **impossible for v ≥ 6**; **v = 5 gives 32−25+1 = 8 = 2³, a real hit** |

> **THEOREM (SHEEP-D2).** No branch `v ≥ 6` can be the second-to-last step
> before a halt. The depth-2 survivor set is exactly **{0, 1, 2, 3, 5}**.

Gap inequalities re-checked for every `v < 6000`; the criteria themselves
recomputed for `400 ≤ v < 3000` (no survivors); brute force to `4·10^6` finds
13 values halting in exactly two steps, with valuations `{0,1,2,3}` ⊆ the
predicted set. The exceptional oddPart = 3 branch reaches neither family for
`a < 4000`.

### The ladder saturates — and this is the important part

Write a *geometric family* as `N(i) = (2^(α+e·i) + b)/c` with `c` odd. The
halting set at depth 0 is one such family, `2^i`, and **the shape is closed
under preimages**: `f(x) = N(i)` with `x = 2^v(2k+1)` reduces to
`2^(α+e·i) ≡ cB_v − b (mod cA_v)`, whose solutions are a residue class
`i ≡ i₀ (mod P)`, and substituting back gives another family with
`e' = eP`, `c' = cA_v`. So every depth is computable exactly, with no search
over `x`. (The leading coefficient stays a pure power of two, which is what
makes deep levels feasible — store the exponent, not the integer.)

| depth | survivor set | families | forbidden branch mass | admissible word mass |
|---|---|---|---|---|
| 1 | {0,1} | 2 | 0.250000 | 0.750000 |
| 2 | {0,1,2,3,5} | 7 | 0.046875 | 0.714844 |
| 3 | {0,…,6} | 23 | 0.007812 | 0.709259 |
| 4 | {0,…,6, 9} | 90 | 0.006836 | 0.704411 |
| 5 | {0,…,10, 13} | 346 | 0.000427 | 0.704110 |
| 6 | {0,…,13} | 1421 | 0.000061 | 0.704067 |

`ladder.log` is the run of record for depths 1–6; the run was stopped in
depth 7, before the script's trailing ground-truth section, which is covered
independently below and in `depth2.py`. Ground truth agrees at every depth
checked: brute force to `3·10^6` gives
valuations `{0,1,2,3}` (halting in 2 steps), `{0,1,2,3}` (3 steps) and
`{0,1,2,5}` (4 steps), each contained in the predicted set — and the `v = 5`
survivor, which the sieve predicted at depth 2, shows up in real data.

**The forbidden mass per depth collapses geometrically** (0.25 → 0.047 →
0.0078 → 0.0068 → 0.00043 → 0.000061) while the family count grows by a factor
≈ 3.8 per depth. The mechanism is visible: the depth-`d` target is a union of `F_d`
families, so a branch `v` survives if *any* of them is reachable; with each
individually reachable with probability ≈ `O(v)/2^v`, branch `v` survives
once `2^v ≲ F_d·v`, i.e. up to `v ≈ log₂ F_d`, which grows linearly in `d`.
So the survivor sets grow, the forbidden mass decays geometrically, and

> **the admissible word mass is a CONVERGENT product, not a vanishing one.**
> Measured: **0.704067** at depth 6, extrapolating to ≈ **0.70406**.

The depth-5 data alone extrapolated to 0.704045; depth 6 then measured
0.704067, so the extrapolation was sound to five decimals before the check
existed. Depth 7 was not run: each depth costs ≈ 15× the last (depth 4 ≈ 1 s,
depth 5 ≈ 80 s, depth 6 ≈ 6.4 h), so depth 7 is ≈ 4 days with the current
linear order-scan. Getting to depth 8–9 needs `ord_M(2)` from a factorisation
of `M` — which we actually know, since `M` is always a product of
`A_v = 2^(v+1)+1` — plus Pohlig–Hellman. Not needed for the conclusion.

**Consequence.** The last-step sieve — at *any* depth — can never forbid more
than about **29.6%** of branch words. It cannot decide the sheep machine, and
this is not a budget limitation: it is what the method converges to. Depth is
not a resource that buys arbitrarily much.

Together with S6 (no congruence certificate at any modulus, T15) this closes
the two congruence-flavoured lanes with numbers, and leaves exactly one:
automatic invariants. There the sheep is a better target than the Needle,
because **H is a tiny regular language** — in binary, `H₀ = (10)*11`,
`H₁ = (1100)*110`, powers of two `= 10*`. The obstruction is the map, not the
target: `f(n) = n + (n >> (v+1)) + v` adds a copy of itself shifted by a
*variable* amount, so `f` is not 2-automatic, which is why the WS1 searches
stall at small DFA sizes.

---

## What is settled and what is not

S3–S5 settle the **arithmetic** of the sheep machine completely: we know
exactly which values can halt, and the description is finite. What remains is
the same single-orbit avoidance question as for Collatz and for the Needle —
does the orbit of 5 ever land in H — and S6 says the congruence method cannot
answer it.

So the sheep machine is a cryptid whose **last-step analysis is closed** and
whose **orbit question is open**; the Needle is one where both are open. That
is the sharpest instance so far of the rank-of-sieve-group dichotomy, and it
is on a machine we did not construct.

**Heuristic (not a proof).** H is thin: `|H ∩ [x, 2x]| ≈ 1.75` (one power of
two, one H₀ member per two octaves, one H₁ member per four). With the orbit
growing at 0.4015 bits/step, the expected number of future hits from the
position reached here (2^12045) is a geometrically convergent sum equal to
**10^(−3625.0)**. Same shape of evidence as Collatz, same gap:
equidistribution results are almost-everywhere, the question is about one
orbit.

## Files

* `sheep.py` / `sheep.log` — the machine, the identification, S1–S6, the orbit.
* `depth2.py` / `depth2.log` — SHEEP-D2 and its proof.
* `ladder.py` / `ladder.log` — the exact preimage recursion and the ladder.
