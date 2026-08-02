# DRAFT — proposed additions to the bbchallenge wiki page for the sheep machine

**Machine:** `1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE` (BB(6) Cryptid, found
by *sheep*, 7 Apr 2026)

**Status of this document: LOCAL DRAFT for Tom's review. Nothing has been
published.** On approval it would be converted to MediaWiki markup and added
to the machine's existing page as new sections (the page currently has the
reduction, `even_case_no_pow2`, `oddPart3_no_pow2`, and the two "dangerous
families"). Two placeholders need Tom's decision before publication:
**attribution** and the **public code link** (marked ⟦TODO⟧ below).

Everything here is stated against the page's own reduction, in its notation
(`n`, `a = v2(n)`, oddPart), and every claim carries an epistemic label. All
results reproduce from three short scripts (⟦TODO: public repo link⟧),
runtime ≈ 20 s except the depth ladder (≈ 6.5 h).

---

## Proposed new section: "Which steps can reach a power of 2"

The page's reduction: with `oddPart(n) = 1` the machine halts; with
`oddPart(n) = 3`, `f(n) = n + v2(n) + 3`; otherwise
`f(n) = n + v2(n) + (oddPart(n)−1)/2`, starting from 5.

**Lemma A (sharpens `even_case_no_pow2`; proof: elementary, ~10 lines).**
Write `n = 2^v·(2k+1)`, `2k+1 > 3`. Then `f(n)` is a power of two **iff**

> `2^(t+1) ≡ 2v − 1 (mod 2^(v+1) + 1)` for some `t ≥ 0`,

and this has solutions **only for `v ∈ {0, 1}`**. Every step from `v ≥ 2`
provably cannot reach a power of two.

*Proof sketch.* The generic branch is affine in `k`:
`f(n) = (2^(v+1)+1)·k + 2^v + v`. Landing on `2^t` is a congruence on
`2^t mod A_v` where `A_v = 2^(v+1)+1`; since `2^(v+1) ≡ −1 (mod A_v)`, the
subgroup `⟨2⟩` is contained in `{2^i} ∪ {A_v − 2^i}` for `i ≤ v`, and the
target `2v − 1` falls in a gap of that short list for every `v ≥ 2` (two
one-line inequalities). ∎

*Relation to the page:* `even_case_no_pow2` assumes the threshold `a ≥ 2` as
a hypothesis. Lemma A derives the threshold and locates the two surviving
cases at the same time, from one congruence. [proved; additionally verified
by direct group computation for all `v < 260`, the gap inequalities for
`v < 4000`, and brute force against the reduction for `v = 2..13`,
`oddPart = 5..19999` — 0 counterexamples]

**Lemma B (= the page's `oddPart3_no_pow2`, unchanged).** `3·2^a + a + 3` is
never a power of two: for `a ≥ 3` it lies strictly between `3·2^a` and
`2^(a+2)`; `a = 0, 1, 2` give 6, 10, 17. [proved]

## Proposed new section: "The dangerous families are complete"

**Theorem C.** The set of values from which the machine halts in exactly one
step is **exactly**

> `H = {2^i : i ≥ 0} ∪ H₀ ∪ H₁`,
> `H₀ = {(2^(2j+1)+1)/3 : j ≥ 2} = 11, 43, 171, 683, 2731, …`
> `H₁ = {2·(2^(4j)−1)/5 : j ≥ 2} = 102, 1638, 26214, …`

i.e. the two "dangerous families" already on this page are **all** the
dangerous families — the list is complete, with `H₀` the `v = 0` solutions
of Lemma A and `H₁` the `v = 1` solutions. (The `j = 1` members 3 and 6 are
excluded: their oddPart is 3, so they take the exceptional branch, Lemma B.)
[proved; brute force over `n < 300,000` finds exactly the predicted members
and no others]

The halting problem for this machine is therefore exactly: **does the orbit
of 5 ever enter H?** — with H a completely explicit set (in binary:
`10*`, `(10)*11`, `(1100)*110`, a regular language). Nothing below decides
this; the remaining sections close off proof routes.

## Proposed new section: "No congruence invariant can decide it"

**Theorem D.** For every modulus `M ≥ 2`, the closure of `{5 mod M}` under
the reduction's one-step reachability relation is all of `Z_M`. Consequently
**no congruence invariant at any modulus separates the orbit from H** — a
CTL/FAR-style certificate whose state is `n mod M` cannot prove this machine
non-halting, for any `M`.

*Method:* this is an instance of a general theorem for maps of the shape
`(2^(v+1)+β)k + γ2^v + δv + ε` with β odd and gcd(δ, M′) = 1 (proof by a
2-adic lifting/descent argument; ⟦TODO: repo link⟧ has the write-up and a
machine verification). For this machine it was also verified directly for
every `M ≤ 200`. [proved, computer-assisted]

**Theorem E (second-to-last step).** By the same sieve applied to the
preimages of `H₀` and `H₁` (moduli `3A_v` and `5A_v`), no branch `v ≥ 6` can
be the second-to-last step before a halt; the depth-2 survivor set is exactly
`{0, 1, 2, 3, 5}`. The lone `v = 5` survivor is a genuine near-coincidence
(`2^5 − 5·5 + 1 = 8 = 2³`) and shows up in real data: brute force to
`4·10^6` finds 13 values halting in exactly two steps, with `v2` values
`{0, 1, 2, 3}`. [proved; inequalities re-checked to `v < 6000`]

## Proposed new section: "How far the sieve method can ever go" (measurement)

Iterating the preimage computation is exact at every depth (the targets stay
finite unions of geometric families `(2^(α+ei)+b)/c`). Running it to depth 6:

| depth | surviving branches | families | admissible word mass |
|---|---|---|---|
| 1 | {0,1} | 2 | 0.750000 |
| 2 | {0,1,2,3,5} | 7 | 0.714844 |
| 3 | {0,…,6} | 23 | 0.709259 |
| 4 | {0,…,6,9} | 90 | 0.704411 |
| 5 | {0,…,10,13} | 346 | 0.704110 |
| 6 | {0,…,13} | 1421 | 0.704067 |

The admissible mass converges to ≈ **0.70406**: the last-steps sieve, at
*any* depth, never forbids more than ≈ 29.6% of branch words. The mechanism:
the depth-`d` target has `F_d ≈ 3.8^d` families, each reachable from branch
`v` with probability `≈ O(v)/2^v`, so branches survive up to
`v ≈ log₂ F_d` — the survivor set grows exactly as fast as the sieve
tightens. **Finite-depth sieving cannot decide this machine, and that is a
property of the method, not a compute budget.** [measured, depths 1–6; the
depth-5 extrapolation predicted 0.704045 before depth 6 measured 0.704067]

## Proposed closing remark for the page

The machine's arithmetic is now closed — the halting set is explicit and
complete, and congruence/sieve certificates are provably insufficient at
every modulus and depth. What remains open is exactly the single-orbit
question (does the orbit of 5 avoid the regular set H), with the orbit
verified halt-free to 30,000 reduction steps (value at 12,045 bits, drift
0.4014 bits/step vs 0.4015 predicted). A useful contrast: the Space Needle's
analogous reduction (`(2^(v+1)+3)k + 2^v + v`) has none of this structure —
its sieve group `{±3^a·2^i mod 2^(v+1)+3}` has rank 2, its survivor set is
infinite, and no closed form for its halting set is known. The two machines
differ only in the constant `β` (1 vs 3); the pair is a clean controlled
experiment in what makes these reductions tractable.

---

## Not for the wiki — reviewer notes for Tom

1. **What we are and are not claiming.** No decision. Lemmas A/B and
   Theorems C/E are elementary and self-contained; Theorem D cites our T15 —
   on the wiki I propose stating it as above with the proof in the linked
   repo, since the general theorem's proof (saturation + descent + reach) is
   several pages. The heuristic 10^(−3625) residual-risk figure is **left
   off the page** deliberately (the community computes these per-machine
   anyway, and it adds no mathematics).
2. **Placeholders needing your call:** (a) attribution — how to credit
   you/the AI workflow (community precedent exists: machines credit "Jason
   Yuen (@-d) and Claude Opus 4.6"); (b) the public repo link — the scripts
   (`sheep.py`, `depth2.py`, `ladder.py`) need a public home before the page
   can cite them; (c) whether to also propose a short Lean formalization of
   Lemma A + Theorem C (the rwst/bbchallenge repo already has a directory
   for this machine — it would materially strengthen acceptance).
3. **Verification independence caveat** (stated here, not on the wiki): all
   verification is by our own scripts. Lemma A was additionally checked
   against the wiki's own hand-derived lemma and agrees; Theorem C's brute
   force is an independent path through the raw reduction.
4. **Publication mechanics** when approved: wiki edit adding the sections
   above (converted to MediaWiki markup), linked from the machine page's
   analysis section; optionally a short note on the Discord analysis channel.
   I will not publish anything until you say go.
