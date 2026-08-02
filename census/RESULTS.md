# WS5 — Census of the one-schema VAL(2) family

Executed July 27, 2026. Code and logs of record in this directory.

This is the first thing the program has built that **produces** machines instead
of consuming them. WS4 ended by asking whether the one-schema valuation class is
Turing-complete and noting it is the only two-sided bet left; that class is also
where both flagship machines live. So a census of it populates the class whose
power is open *and* turns the per-machine handcraft into a pipeline.

## The family

A machine is five integers. Write `x = 2^v · m` with m odd. If m = 1 the machine
**halts** (x is a pure power of two). Otherwise m = 2k+1, so `x = 2^(v+1)k + 2^v`,
and

```
F(x) = A_v·k + B_v ,    A_v = α·2^(v+1) + β ,    B_v = γ·2^v + δ·v + ε
```

the branch-affine normal form the whole program is built on, coefficients left
free. **The Space Needle is (1, 3, 1, 1, 0)** — verified: 0 mismatches against
`needle.step1` over 2 ≤ x < 300,000, and the orbit from x₀ = 3 is
3, 6, 10, 17, 41, 101, 251, … , joining the published orbit at 6.

As a function of x the branch has slope `A_v/2^(v+1) → α`, so α is the
asymptotic multiplier: α ≥ 2 doubles at every branch, α = 1 is the weakly
expanding Collatz-like regime.

> **Update, July 31 — the box contains a second wild machine.** Member
> **(1, 1, 1, 1, 0)** is the generic branch of the **sheep machine**
> (`1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE`, BB(6), a listed bbchallenge
> Cryptid), the Space Needle's reduction with β = 3 → 1. So two of the box's
> members are reductions of machines found by other people, and the family is
> not as manufactured as it looked. See `../sheep/RESULTS.md`.
>
> The census records (1,1,1,1,0) as **HALT** — from x = 3 it steps 3 → 4 = 2².
> The sheep machine's *exceptional* branch (oddPart = 3, absent from our
> schema) intercepts exactly that value and sends 3 → 6. **One extra branch on
> one odd part converts a halting census member into an open problem** — the
> clearest statement available of what the box misses.

## What every machine gets, automatically

Well-definedness · simulation from x₀ = 3 · drift · backward branching ceiling ·
**exact congruence decision** · WS3 forbidden-branch sieve mass. Two of these can
decide a machine outright.

The **congruence test is exact and complete**, not the necessary condition WS4
had to settle for. On branch v the pair (source, target) mod m traces the graph
of one affine map φ_v, and A_v, B_v mod m depend on v only through
`(2^v mod m, v mod m)` — a state space of size m² — so iterating v until that
state repeats enumerates *every* branch. The relation R_m is therefore exactly
computable, the orbit lies in the R_m-closure of x₀, and if that closure misses
H's residues the machine **provably** never halts.

**Calibration ran first, both directions** (a decision procedure reported without
both is worthless): the Needle must *not* be decided — PASS — and machines that
*are* decided must survive an independent check — PASS on all three sampled.

## Results

1,080 machines enumerated over α∈{1,2,3}, β∈{−1..7}, γ∈{1,2,3}, δ∈{0,1,2},
ε∈{−2..2}; **3 are not well defined** (F leaves the positive integers);
**1,077 analysed** in 220 s.

| α | machines | HALT | CYCLE | GROW | decided | mean drift |
|---|---|---|---|---|---|---|
| 1 | 357 | 116 | 21 | 220 | 105 | 0.8809 |
| 2 | 360 | 80 | 6 | 274 | 103 | 1.5529 |
| 3 | 360 | 61 | 0 | 299 | 110 | 1.9933 |

**318 of 1,077 machines (29.5%) are decided by a separating congruence** —
proved never to halt from x₀ = 3. **Every one of the 318 certificates was
re-audited independently** (`verify.py`: brute force over real integers to
x < 200,000, powers of two enumerated completely, without reusing the branch
enumeration that produced it) — **0 failures**. A false non-halting proof is the
worst output this program could emit, so the audit is not optional.

Deciding moduli: 3 (41), 4 (105), 6 (68), **7 (3)**, 8 (18), 10 (34), 12 (17),
14 (2), 16 (14), 20 (6), 22 (1), 24 (2), 32 (1), 36 (1), 40 (2), 56 (3).

*(Corrected July 29: an earlier version of this list omitted m = 7 — the three
machines (1,7,1,0,0), (2,7,2,0,0), (3,7,3,0,1) — which is why 41+105+68+18 did
not reconcile with the count of machines decided at m ≤ 8. Found while proving
the criteria below.)*

### G2 finally moves — and here is exactly how much

G2 ("decide a cryptid") had not moved in four consecutive stock-takes. It moves
here: 318 machines decided, and two proved non-halting after their first step
(five, counting the follow-up below). The
honest qualification is that these are *new and easier* machines, not the
cryptids — a machine with a separating congruence is by definition not a
cryptid. What the census delivers is the **partition**: which members are easy,
*why* they are easy, and a pool of hard ones.

It is worth noting what it cost. 220 seconds of census decided 318 machines;
two days of SAT search bought two states.

## Theorems T1-T3 (from the census proper)

**T1 (proved).** The machine **(1, 1, 2, 0, 1)** never halts after its first step.
Here B_v = 2·2^v + 1 = 2^(v+1) + 1 = A_v, so `F(x) = A_v·(k+1)` and A_v is odd
and ≥ 3. Every image carries an odd factor > 1 and is never a power of two.
*(0 counterexamples over x < 400,000.)*

**T2 (proved).** The machine **(2, −1, 2, 1, 1)** never halts after its first step.
A_v = 2^(v+2) − 1, and on branch v the WS3 sieve forbids a halt unless
`Q₀·2^e ≡ P₀ (mod A_v)` with P₀ = (2v+3)2^v, Q₀ = 1 − 2^(v+1). Mod A_v we have
2^(v+2) ≡ 1, hence 2Q₀ ≡ 1, so Q₀ ≡ 2^(−1) and the condition collapses to

> `2^(e+1) ≡ 2v + 3   (mod 2^(v+2) − 1)`

The powers of two mod A_v are exactly {1, 2, …, 2^(v+1)} (the order of 2 is
v+2), and for v ≥ 1 the number 2v+3 is odd, > 1 and < A_v, so it is its own
residue and is not among them; v = 0 gives 3 ≡ 0 mod 3, also not a power of two.
**Every branch is forbidden**, so no orbit can reach a power of two after a step.
*(0 counterexamples over v < 400.)*

**T3 (proved, and exact on the whole census).** A member is decided at m = 3 —
hence provably never halts from x₀ = 3 — **iff**

> `δ ≡ 0`,  `γ ≡ α`,  `β + ε ≡ 0`   (all mod 3)

*Proof.* Mod 3 the powers of two are {1, 2}, every nonzero class, so a
separating class must be ⊆ {0}, and it contains x₀ = 3, so it **is** {0}. Then
3 | x forces k ≡ 1 (mod 3), and
`F(x) ≡ (−1)^v(γ−α) + β + δv + ε (mod 3)`. Vanishing at v = 0, 1, 2 gives
2δ ≡ 0, then 2(γ−α) ≡ 0, then β+ε ≡ 0; conversely those three make it vanish for
every v. ∎ **Checked: 41 predicted, 41 decided, 0 discrepancies over 1,077
machines.**

**Corollary — and this is the sharpest thing the census says about the Needle.**
The **v-linear term δ is what blocks the cheapest certificate there is**. The
Space Needle has δ = 1 and fails T3 in one line. The term δ·v injects unbounded
valuation information into the *value*, and no modulus can track it.

## The Needle is not special in anything we can measure globally

**Drift and the branching ceiling are functions of (α, β) alone** — verified: 24
(α,β) classes, **0** of them carrying more than one (drift, ceiling) value. So
**45 machines share the Needle's drift 0.9411 and ceiling 0.54528 exactly.**
Neither statistic can distinguish it from 44 siblings.

What does separate them is the sieve, which sees (γ, δ, ε): across those 45
twins the forbidden-branch mass ranges **0.0000 to 0.7988**, with the Needle at
**0.2852** — a clean reproduction of WS3's independently measured 28.7% (that
was over v ≤ 35, this over v ≤ 8).

**β parity is what makes a machine hard.** β even → 64–79% decided; β odd →
3.7–8.1%. Of the 120 cryptid candidates (α = 1, grows, undecided), **108 have
odd β**. A_v odd is exactly the classic Collatz situation: the map hands you no
2-adic structure to exploit.

## Seven machines with every branch forbidden

Seven undecided growers have **all** branches sieved out to v = 200 (mass
1.000000000): (1,1,2,0,1), (2,−1,2,1,1), (2,−1,2,2,1), (2,−1,3,0,0),
(2,−1,3,1,0), (2,1,1,2,−1), (3,3,2,0,1). Two became T1 and T2 on the day.
The other five were recorded as leads and **explicitly not claimed** —
"forbidden to v = 200" is not "forbidden for all v", and the gap is exactly the
kind this program refuses to paper over. **All five are now theorems**, together
with three more the search for them had never seen; see the two follow-ups
below. The count "seven" is itself an artefact of the pool filter — the true
number of all-branches-forbidden machines in the box is **ten**.

### Follow-up (July 28, morning): three of them are now theorems

`leads.py`, `leads.log`. The leads were recorded one at a time; checked against
*each other* they collapse. **Four have `A_v = 2^(v+2) − 1` identically** — the
entire α = 2, β = −1 corner — which is T2's modulus, where `ord(2) = v+2` makes
the powers of two the listable set {1, 2, …, 2^(v+1)}. Writing branch v's
condition as `2^e ≡ S_v (mod A_v)`, the fixed point plus `2^(v+2) ≡ 1` collapses
it to `S_v ≡ 2·B_v (mod A_v)`, giving **T4, T5, T6** and correcting the
statement of T1/T2 ("never halts *after its first step*" — a start that *is* a
power of two halts at step 0). Two leads were left open.

**That attribution was too modest, and the two open leads were not open.** See
below.

### Follow-up (July 28, evening): the lemma is universal, and the method is complete

`universal.py`, `universal.log`. The derivation above never uses α = 2 or
β = −1. Reducing the sieve's fixed point `P₀ = (2B_v − A_v)2^v`,
`Q₀ = 2^(v+1) − A_v` modulo A_v simply deletes the `A_v` terms:
`Q₀ ≡ 2^(v+1)`, `P₀ ≡ B_v·2^(v+1)`, so `P₀Q₀⁻¹ ≡ B_v`.

> **Universal sieve lemma (proved).** For every machine with β odd,
> **`S_v ≡ 2·B_v (mod A_v)`** — equivalently, branch v can immediately precede a
> halt **iff `B_v ∈ ⟨2⟩ mod A_v`**, the multiplicative group generated by 2.

*Machine-verified: 672 machines (the whole odd-β box), 51,030 branches,
v = 0..80, 0 mismatches.*

> **Linear corollary (proved).** Since `α·2^(v+1) ≡ −β (mod A_v)`, multiplying
> through by α kills the exponential:
> **`α·S_v ≡ 2αδv + 2αε − βγ (mod A_v)`** — affine in v, for every machine.
> The exponential is not in the target; it is only in the modulus.

*Machine-verified on the same 51,030 branches, 0 mismatches.*

**What decides a machine is therefore the size of ⟨2⟩ mod A_v.** Four classes
are **listable** — ord(2) grows linearly, so ⟨2⟩ is a short explicit list a
parity/size argument can clear: (2,−1) with ord = v+2 and ⟨2⟩ = {2^i}; (1,1) and
(2,1) with ord = 2(v+1), 2(v+2) and the signed list {±2^i}; and (3,3), where
3 | A_v. The other classes are **thin** — ord grows exponentially on average
(e.g. (1,3): 4, 3, 10, 18, 12, 66, 130, 36) and membership has no elementary
handle.

### The ten machine theorems (labels T1–T11; T3 is the m = 3 criterion)

Every all-branches-forbidden machine in the box, with S_v as an **exact integer
identity** (asserted to v ≤ 4,000 on a second, independent code path) and the
pattern that closes it. T7–T11 are new; the two "leads that do not transfer" are
T7 and T8.

| machine | S_v (derived) | why every branch is forbidden | |
|---|---|---|---|
| (1,1,2,0,1) | 0 | B_v = A_v exactly; 0 is not a unit, powers are | T1 |
| (2,−1,2,0,1) | 3 | 2B_v = A_v + 3; odd, 1 < 3 < A_v for v ≥ 1 | **T9** |
| (2,−1,2,1,1) | 2v + 3 | odd, 1 < S_v < A_v for v ≥ 1; v = 0 gives 0 | T2 |
| (2,−1,2,2,1) | 4v + 3 | odd, in range for v ≥ 2; v = 0,1 give 0 | T4 |
| (2,−1,3,0,0) | 2^(v+1) + 1 | odd, in range for v ≥ 1; v = 0 gives 0 | T5 |
| (2,−1,3,1,0) | 2^(v+1) + 2v + 1 | odd, in range for v ≥ 2; v = 0,1 give 0 | T6 |
| (2,−1,1,2,−1) | 2^(v+1) + 4v − 2 | = 2·odd < A_v, so S_v = 2^i forces i = 1, i.e. 2^v = 2−2v | **T10** |
| (2,1,1,2,−1) | 2^(v+1) + 4v − 2 | same, signed list mod 2^(v+2)+1; S_v = A_v − 2^i forces i = 0, i.e. 4v−2 = 2^(v+1) | **T7** |
| (3,3,2,0,1) | ≡ 0 mod d_v | B_v = d_v = 2^(v+1)+1 exactly, and d_v \| A_v; powers of 2 are units mod d_v | **T8** |
| (3,3,3,0,0) | −3 | 2B_v = A_v − 3 and 3 \| A_v, so S_v ≡ 0 (mod 3); powers of 2 mod 3 are {1,2} | **T11** |

**T7–T11 (proved): five more machines that never halt after their first step.**
Brute force on all ten: non-power-of-two starts below 20,000, 400 steps,
**0 halts**.

Three of the five were invisible to the earlier hunt not because the test
differed but because of the **pool filter**: the leads were drawn from undecided
*growers*, and (2,−1,2,0,1) and (3,3,3,0,0) were already congruence-decided,
while (2,−1,1,2,−1) is a CYCLE machine (x = 3 is a fixed point: F(3) = 3). For
the two congruence-decided ones this is a genuine upgrade — congruence gave
"never halts *from x₀ = 3*", the sieve gives "no orbit *from any start* reaches
a power of two after a step".

### The completeness theorem — the method is finished, and provably

> **Proved.** Those ten are all there are. For **every** other well-defined
> odd-β machine in the census box, the sweep returns an **explicit surviving
> branch**: a v ≤ 22 together with the exponent e witnessing
> `2^e ≡ S_v (mod A_v)`.

*Machine-verified: 672 machines swept — 10 all-forbidden, 620 with a positive
surviving-branch certificate, 42 sieve-silent (the (1,−1) class, where no branch
expands and the sieve argues from nothing).*

A surviving branch is a **positive certificate**, not a failure to find one. So
this is not exhaustion, it is a proof that the sieve-to-theorem pipeline is
**complete on this family at ten machines**. What is *not* claimed: a
surviving branch does not make a machine halt — it means only that this method
cannot decide it, and something else must.

### The frontier map

Of the 636 odd-β machines not decided by a congruence:

| tier | count | what it means |
|---|---|---|
| 1 — mechanical | 8 | all branches forbidden + pattern proof (the ten, minus the two already congruence-decided) |
| 2 — **S-unit** | **399** | thin ⟨2⟩, sieve bites but does not close: deciding needs S-unit / Baker input |
| 3a — sieve-closed | 164 | listable class, but a branch certifiably survives: this route is provably shut |
| 3b — sieve-void | 24 | thin, forbidden mass 0 — every tested branch survives |
| 3c — sieve-silent | 41 | (1,−1): no expanding branch |

**The Space Needle is in tier 2, and 120 machines share its group.** With
A_v = 2^(v+1)+3 we get 2^(v+1) ≡ −3, so ⟨2⟩ = {±3^a·2^i} and the condition reads

> **`2v − 3 ∈ {±3^a·2^i}  (mod 2^(v+1)+3)`**

*Verified: closed form S_v ≡ 2v − 3 exact for v ≤ 200, 0 mismatches; weighted
forbidden mass 0.2868, an independent reproduction of WS3's 28.7%; 19 forbidden
among the first 35 valuations, matching WS3's count exactly.*

**And it does not close.** The surviving branches to v = 40 are
0, 2, 3, 5, 6, 8, 11, 14, 15, 16, 17, 20, 27, 29, 30, 34, 37, 38 — 18 of 41,
**not thinning out**. There is no asymptotic all-branches-forbidden theorem for
the Needle, and the last-step sieve saturates near 28.7% weighted forever.
Whatever decides the Needle comes from somewhere else. This is a 2,3-S-unit
membership question, which is exactly where the frontier now sits.

## Why no congruence decides the Needle — a theorem, not a search bound

Executed July 29, 2026. `saturation.py`, `saturation.log`.

WS4 swept every modulus m ≤ 20,000 and found no separating congruence for the
Space Needle. That is a *bounded resource* — the kind of result P9 warns is
silent past its budget. An infinite slice of it is now a proof.

> **T12 — the δ-saturation theorem (proved).** Let M be **odd** with
> `gcd(δ, M) = 1` and `gcd(ord_M(2), M) = 1`. Then for **every** residue c the
> one-step image `{φ_v(c) : v ≥ 0}` is **all of Z_M**.

*Proof.* M odd makes 2^(v+1) invertible, so branch v is one affine map
`φ_v(c) = μ_v c + a_v` with `μ_v = A_v(2^(v+1))⁻¹`, `a_v = B_v − μ_v 2^v`. Fix v₀
and restrict to `v ≡ v₀ (mod ord_M(2))`: there `2^v` is constant, hence so are
`A_v mod M`, `μ_v`, and `γ2^v`. The **only** surviving v-dependence is `δ·v`:

> `a_v − a_(v₀) ≡ δ·(v − v₀)  (mod M)`

As v runs over `v₀ + ord_M(2)·Z`, the difference runs over the subgroup generated
by `gcd(ord_M(2), M) = 1` — all of Z_M — and `gcd(δ,M) = 1` keeps it so. ∎

> **Corollary (the Space Needle).** δ = 1, and `ord_p(2) | p−1` makes the second
> hypothesis automatic for primes. **No odd prime modulus can ever separate the
> Needle** — not "none below the search bound": none, unconditionally. Already
> the one-step image from any residue is everything, so no branch can even be
> excluded.

*Machine-verified: the proof's steps on 4,000 (machine, odd M) pairs meeting the
hypotheses — 0 violations; end-to-end image = Z_M in 265 cases with M < 62 and
on the 45 primes below 200 — 0 failures; all 549 odd primes below 4,000 satisfy
the hypotheses.*

**This sharpens T3's corollary.** T3 said the v-linear term blocks the *cheapest*
certificate (m = 3). T12 says δ blocks **every prime certificate totally, in a
single step**, for reasons independent of the size of the prime.

**Falsifier (run, because a theorem this strong should be attacked).** Every one
of the 318 separating certificates must violate a hypothesis or T12 is false:
274 have an even modulus, 44 fail a gcd condition, **0 would refute**.

**The honest boundary: even M.** 2 is not invertible there, so a branch stops
being a single affine map and the argument does not run. That matters —
**274 of the 318 certificates live at even moduli**, so if a certificate for a
hard machine exists at all, that is where it must be.

### The congruence criteria at m = 4, 6, 8

T3 gave a closed form at m = 3 and nothing was known at the moduli that decide
more machines. Separation at m depends on (α,β,γ,δ,ε) only through their
residues mod m, so each criterion is a finite object on (Z_m)⁵ and is checked
**completely**, not sampled. Write `A₀ = 2α+β`, `B₀ = γ+ε`, `T = A₀+B₀`.

> **C4 (proved).** Separates at 4 ⟺ **β even and `2α+β+γ+ε ≡ 3 (mod 4)`.**
> Mod 4 the powers of two are {1,2,0}, so the only allowed class is {3}, which
> holds x₀ = 3; the closure must be exactly {3}. Only v = 0 has odd sources, and
> `x ≡ 3 (mod 4)` ⟺ k odd, giving targets `A₀+B₀` and `3A₀+B₀`; both ≡ 3 iff
> `2A₀ ≡ 0` and `T ≡ 3`.

> **C6 (proved).** H = {1,2,4}. Separates at 6 ⟺ one of: (a) A₀ even and
> `T ≡ 3 (mod 6)`; (b) `A₀ ≡ 0,4 (mod 6)` and `T ≡ 5`; (c) **T3 itself**;
> (d) `A₀ ≡ B₀ ≡ 0 (mod 6)`, `δ ≡ 0 (mod 3)`, `γ+δ ≡ β+5 (mod 6)`.

> **C8 (proved).** H = {0,1,2,4}. Only v = 0 and v = 1 can occur, and A₀ must be
> even; the question then reduces to the forward orbit of 3 under an explicit
> four-node map.

*Verified completely: C4 on all 1,024 residue tuples mod 4 (128 separate,
0 mismatches); C6 on all 7,776 mod 6 (1,308 separate, 0 mismatches). Against the
census, all 1,077 machines: T3 41, C4 105, C6 68 — **0 discrepancies in either
direction**, exactly the standard T3 was held to.*

### What did not work, and why it is worth recording

The route in was **Skolem's conjecture** — an unsolvable exponential Diophantine
equation should be unsolvable modulo some witness — and the Bertók–Hajdu
algorithm that constructs such a witness. **It does not apply.** Their class
admits only *exponents* as unknowns; our halting equation `A_v·k + B_v = 2^E`
carries k linearly, and every open machine carries v linearly through `δ·v`.
Reducing mod A_v eliminates k and is an *equivalence*, so our local-to-global
step is a theorem with a **forced** modulus, not a conjecture with a searched
one. Run on 16 known-forbidden branches, their greedy returns a power of two
every time and never A_v: it certifies "B_v is not a power of two", where we need
"not a power of two **mod A_v**".

Recorded because the failure was productive: asking *why no witness modulus
exists* instead of *which one works* is what produced T12.

## The even half: T14, and why β odd closes the hatch

Executed July 29, 2026. `even_saturation.py`, `even_saturation.log`.

T12's falsifier located its own gap in one line: **274 of the 318 certificates
live at even moduli**, so if a certificate for a hard machine exists at all, that
is where it has to be. This closes that half — and identifies exactly what an
even modulus buys.

### The mechanism, in one sentence

Write M = 2^s·M' with M' odd. A source residue c mod M with `v₂(c) = v < s`
**pins the branch index v exactly** — the low bits of the value *are* the
valuation. That is precisely the information T12 proves an odd modulus can never
have. For `v ≥ s` the source is 0 mod 2^s, every branch `v ≥ s` is
simultaneously available, and the odd part is back in T12's situation.

That predicts where the escape hatch is. On a source ≡ 0 (mod 2^s) the multiplier
k is **free mod 2^s** (pinned only mod M'), and since `v ≥ s`,

> `target = A_v·k + B_v ≡ β·k + δv + ε  (mod 2^s)`

**β odd ⟹ β·k sweeps all of Z_(2^s) and the 2-adic information is destroyed in
one step. β even ⟹ it sweeps only ⟨gcd(β,2^s)⟩ — the hatch stays open.**

> **T14 — even-modulus saturation (proved).** Let M = 2^s·M', M' odd, s ≥ 1, and
> suppose (i) β odd; (ii) `gcd(δ,M') = 1`; (iii) `gcd(ord_{M'}(2), M') = 1`;
> (iv) the closure of x₀ contains some `c₀ ≡ 0 (mod 2^s)`. Then the closure is
> **all of Z_M** — no separation, and no branch can be excluded either.

*Proof.* All branches `v ≥ s` are available from c₀ (2^v is invertible mod M',
and M' odd lets an odd representative be chosen). Splitting the source congruence
by CRT: mod 2^s it holds identically, so **k is unconstrained mod 2^s**; mod M'
the factor 2^(v+1) is invertible, so **k is determined mod M'**. Since v+1 > s we
have `A_v ≡ β` and `B_v ≡ δv + ε (mod 2^s)`, so the target is `βk + δv + ε` and
β is a unit — the 2-adic component sweeps all of Z_(2^s) while the M'-component
stays at `μ_v c₀' + a_v`. Union over `v ≥ s`: the M'-components run over T12's
set restricted to `v ≥ s`, which costs nothing since each class mod `ord_{M'}(2)`
still holds infinitely many such v. So the targets are Z_(2^s) × Z_(M') = Z_M. ∎

*Machine-verified: the mechanism (502 residues, s = 1..8); the three proof steps
on 3,000 instances meeting the hypotheses — 0 failures each; and the conclusion
on 7,840 (β-odd machine, even modulus) pairs — closure not all of Z_M in **0**.*

**Falsifier — and the census confirms the mechanism without being asked.** Every
even-modulus certificate must break a hypothesis or T14 is false:

| | count |
|---|---|
| (i) **β even** — the escape hatch | **267** |
| (ii) `gcd(δ,M') > 1` (all seven have δ = 0) | 7 |
| (iii) or (iv) fail | 0 |
| **would refute T14** | **0** |

### T14′ — the sharp form, and it is an *iff*

Hypothesis (iii) is sufficient but far from necessary. Two simplifications make
the exact condition cheap. Working mod M', `μ_v·2^v = A_v/2`, so

> `a_v = B_v − A_v/2 = (γ−α)2^v + δv + (ε − β/2)`,  `μ_v = α + β/2^(v+1)`

— no hidden v-dependence. Writing `v = v₀ + j·ord` with `ord = ord_{M'}(2)`, on
such a class `2^v` is constant so `μ_v` and the `(γ−α)2^v` term are constant, and
the only surviving v-dependence is `δv`:

> `φ_v(c) = φ_(v₀)(c) + δ·ord·j`

As j ranges over the integers this sweeps `⟨gcd(δ·ord, M')⟩ = ⟨g⟩` with
`g := gcd(ord, M')`. So the reachable set is a union of at most `ord` cosets of
⟨g⟩, and Z_(M') has exactly g of them. Hence:

> **T14′ (proved).** The closure is all of Z_(M') **iff** the `ord` base points
> `φ_(v₀)(c)`, v₀ = 0..ord−1, cover all g cosets of ⟨g⟩.

An equivalence, decidable per (machine, modulus) in O(ord) work; **(iii) is
exactly its trivial case g = 1**. *Verified: the two simplifications and the
equivalence on 4,000 (machine, M') instances — 0 violations, 0 mismatches; and it
accounts for all 6,720 β-odd cases at moduli (iii) does not cover.*

### What is now proved, and what is only reduced

- **β = 3 is odd and δ = 1, so (i) and (ii) hold for the Needle at every M.**
  Combining T12 and T14: **no modulus whose odd part satisfies
  `gcd(ord_{M'}(2), M') = 1` can separate the Space Needle** — odd or even, with
  **no upper bound on M**. That is **12,916 of the 19,999 moduli ≤ 20,000
  (64.58%)**, by a one-line gcd test, where WS4 had only a computation.
- The other ~35% are covered by T14′ in **every case tested** (the first
  uncovered moduli are 9, 18, 21, 25, 27, 36, …; the Needle's closure is all of
  Z_M at each). But T14′ is a **per-modulus test, not a closed form** in
  (α,…,ε). So **"no modulus whatever separates the Needle" is now *reduced* to a
  coset-covering statement, not proved.**
- A descent is visible — `g₁ := gcd(ord_g(2), g)` satisfies `g₁ < g` whenever
  g > 1, so the condition recurses on a strictly smaller modulus — but turning
  that into a proof needs the base points controlled at every level, and that is
  not done. **The gap is named rather than papered over: this is a reduction.**

## The descent closes: hypothesis (iii) was never needed

Executed July 30, 2026. `descent.py`, `descent.log`.

T12 and T14 were both stated with `gcd(ord_{M'}(2), M') = 1`, covering 64.58% of
the moduli below 20,000. It is **unnecessary**, and the reason is a descent that
closes itself.

**What exposed it.** The proof used a *single* step from c₀ — but the object is a
**closure**, so composition is free. Testing two composed steps on the uncovered
set showed something better: the **one-step** image was already all of Z_{M'} in
every case (6,336 of 6,336). The coset analysis had been too pessimistic.

> **Descent lemma (proved).** Let M be odd with `gcd(δ, M) = 1`. Then for every
> residue c the one-step image `{φ_v(c) : v ≥ 0}` is **all of Z_M** — with no
> condition whatever on `ord_M(2)`.

*Proof.* Put `g₀ = M`, `g_(j+1) = gcd(ord_{g_j}(2), g_j)`, and let `I_j` be the
image in Z_{g_j}.

1. **The chain descends and terminates.** For odd g ≥ 3, `ord_g(2) ≤ λ(g) < g`,
   so `g_(j+1) ≤ ord_{g_j}(2) < g_j`. *(Verified: 0 violations for every odd
   g < 6,000; longest chain there has length 7.)*
2. **One level in terms of the next.** Mod g_j, with `h = ord_{g_j}(2)`: on a
   class `v ≡ w (mod h)` the quantity 2^v is constant, so `μ_v` and the
   `(γ−α)2^v` term are constant and the only surviving v-dependence is `δv`.
   Since v runs over an **infinite** progression `w + hZ`, `δv` sweeps the *full*
   subgroup `⟨gcd(δh, g_j)⟩ = ⟨g_(j+1)⟩`. So `I_j` is a union of h cosets of
   `⟨g_(j+1)⟩`, and reducing the whole image mod `g_(j+1)` annihilates those
   shifts and leaves exactly the base points. Hence
   **`I_j = Z_{g_j} ⟺ I_(j+1) = Z_{g_(j+1)}`**.
3. **The chain of equivalences bottoms out favourably.** At the last level
   `g_k = 1` and `I_k = Z_1` trivially. Walking back up gives `I_0 = Z_M`. ∎

**The point the first attempt missed:** the shifts sweep a *full* subgroup
because v ranges over infinitely many integers. Restricting v to one period —
what a finite search does, and what the conservative version implicitly assumed —
loses exactly that.

*Machine-verified: 2,500 (machine, odd M, c) instances with `gcd(δ,M) = 1`, of
which **708 have `gcd(ord_M(2), M) > 1`** — precisely the cases (iii) excluded —
and the one-step image failed to be all of Z_M in **0**.*

### Final forms

> **T12.** M odd, `gcd(δ, M) = 1` ⟹ no separation at M.
>
> **T14.** M = 2^s·M'; β odd; `gcd(δ, M') = 1`; and the closure reaches a residue
> ≡ 0 (mod 2^s) ⟹ no separation at M.
>
> **Corollary — the Space Needle.** β = 3 is odd and δ = 1, so `gcd(δ, M') = 1`
> at **every** modulus. **No modulus separates the Space Needle** — odd or even,
> with no upper bound and no arithmetic side condition.

*Machine-verified: every modulus 2..400 — closure is all of Z_M in every case, 0
separate. Falsifier: of the 318 certificates, 267 fail (i) β even, 51 fail (ii),
0 fail 2-adic reach, and **0 are explained by (iii) alone**.*

### What is still a hypothesis, stated plainly

**2-adic reach is verified, not proved** (8,512 β-odd × even-modulus cases, 0
failures). It is a condition on the *closure* rather than on the parameters, so
it is decidable per (machine, modulus) — but "decidable for each M" is not "true
for all M", and that distinction is exactly what this program does not paper
over.

**The honest summary: the arithmetic side is closed; one reachability hypothesis
remains.** The congruence-certificate question for the Space Needle — open since
WS4's sweep, and answered until now only by "nothing below 20,000" — is now
answered by a theorem, modulo that single verified condition.

*(That condition fell the same day — see below.)*

## The reach lemma: the last hypothesis falls

Executed July 30, 2026. `reach.py`, `reach.log`.

> **Reach lemma (proved).** β odd, A_v > 0 (every odd-β census member
> qualifies). For every residue c mod M = 2^s·M' there is a lift x ≡ c (mod M)
> whose **actual F-orbit** reaches a value ≡ 0 (mod 2^s) within s + 1 steps. In
> particular the closure of every residue contains a residue divisible by 2^s.

*Proof — the exponent ledger.* Choose `x = c + 2^s·M'·T` with T free and iterate
F **exactly**. The T-dependence stays affine, `y_n = p_n + q_n·T`, and each step
spends `v_n + 1` bits of the coefficient's valuation:

> `e_(n+1) = e_n − (v_n + 1)`

— the same precision accounting the confinement analysis met from the other
side (a confinement certificate *exhausts* its 2-adic pin; here the orbit
exhausts it). Two events are exhaustive: **done-event** — some p_n is divisible
by 2^(e_n); one congruence in T lands y_n on 0 mod 2^s. **Ledger-event** — e
reaches 0; the multiplier k becomes a *unit times T*, and A_v odd makes the next
value sweep every residue mod 2^s. While neither has fired, `v_n < e_n` keeps
the branch sequence T-independent and the ledger strictly decreases from ≤ s−1,
so the process ends within s + 1 steps. β odd is used exactly twice: the A's
never feed the ledger, and the final free multiplier is a unit. ∎

*Machine-verified constructively: the recipe **built** the witness lift and its
orbit was **run** — 4,000 (machine, modulus, residue) instances, a hit on 0 mod
2^s every time, deepest hit 9 steps against the bound s + 1 ≤ 10; the ledger
bookkeeping checked in isolation on 3,000 chains, 0 violations; T-independence
of the branch sequence confirmed (T = 0 vs T = 13, 0 differences).*

**Falsifier.** β-even machines with even-modulus certificates are 2-adically
confined, so reach must *fail* for them or the β-odd hypothesis is decoration:
tested on 40 such machines — **reach fails in all 40**. Load-bearing.

## T15 — the no-certificate theorem, final and unconditional form

> **T15 (proved).** β odd, A_v > 0, `gcd(δ, M') = 1` (M' the odd part of M) ⟹
> the closure of **every** residue is **all** of Z_M: no modulus M separates,
> and no branch can be excluded.
>
> Assembly: M odd — the descent lemma alone. M even — the reach lemma supplies
> a closure element ≡ 0 (mod 2^s), and T14's argument with the descent lemma on
> the M'-part gives everything.
>
> **Corollary. No modulus separates the Space Needle — and there are no
> hypotheses left.** β = 3 odd, δ = 1, A_v = 2^(v+1)+3 > 0: every hypothesis
> holds at every modulus.

*Verified: 7,616 (β-odd machine, modulus) pairs meeting T15's hypotheses,
closure short of Z_M in 0; the Needle at every modulus 2..400, 0 not-saturated.*

The question "is there a congruence certificate for the Needle?" — open since
WS4 swept m ≤ 20,000 — is **closed: there is none.** The reason is δ = 1 and
β odd, exactly the two parameters T3 flagged on the census's first day. What
began as "the v-linear term blocks the cheapest certificate" is, five theorems
later, "the v-linear term blocks every certificate, and here is the mechanism
at every modulus."
