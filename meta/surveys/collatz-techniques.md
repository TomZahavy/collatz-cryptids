# Literature Survey: Rigorous Collatz Techniques and Transferability to Expanding Single-Orbit Avoidance

Agent-produced survey, July 25, 2026. Setting: our machines reduce to a single
expanding integer return map F (log-drift +0.33 to +0.99); halting = the one orbit
from the fixed start hits a sparse set H (powers of q, or thin affine families
indexed by branch words). Already have: no cycles; no congruence invariant separates
orbit from H (multiplicative machines); Baker/LTE log-log bound on halting runs
inside geometric ascents. Open question: Pi-0-1 single-orbit avoidance.

---

## 1. Tao 2019: "Almost all orbits of the Collatz map attain almost bounded values"

**(i) What is proved.** T. Tao, arXiv:1909.03562, *Forum of Mathematics, Pi* 10 (2022), e12. For any f with f(N) -> ∞: Col_min(N) ≤ f(N) for almost all N in **logarithmic density**. Strengthens Korec (1994) (Col_min(N) ≤ N^θ, θ > log3/log4 ≈ 0.7924, natural density).

**(ii) Technique and hypotheses.** Syracuse (odd-to-odd) map. Key objects: **Syracuse random variables** on Z/3^n Z driven by i.i.d. geometric 2-adic valuations (entropy ~ n·log4 > n·log3 forces mixing); a **stabilization proposition** — approximate scale-invariance of these distributions, a substitute for an invariant measure; a **first-passage/renewal argument** via characteristic-function decay on the 3-adic cyclic group ("triangles" of bad frequencies). **Load-bearing hypothesis: negative drift** — mass transports from scale N to N^{1−c}; iterated contraction propagates the almost-invariant measure downward.

**Gonçalves–Greenfeld–Madrid** (arXiv:2111.06170; *Indiana Univ. Math. J.* 74 (2025), 1–46) makes hypotheses explicit for C(N) = N/p (p | N), qN + r(N mod p) otherwise: (a) gcd(p,q) = 1; (b) **q < p^{p/(p−1)}**; (c) qj + r(j) ≡ 0 mod p for j ≠ 0. Condition (b) is *exactly* negative logarithmic drift, noted as seemingly necessary. Logarithmic density only; upgrading to natural density open even for 3x+1.

**(iii) Transferability: essentially none for the direct statement — but the dual question is much easier.** Tao's machinery cannot run on an expanding map (no downward transport). However, for expanding maps the analogous a.e. statement flips difficulty class: the set of halting starts is ∪_n F^{-n}(H), and under expansion the preimage tree of a sparse set is counted by branch words with an exponential deficit — a first-moment computation. Expected yield: **"halting starts have counting function O(x^c), c < 1 explicit from the drift"** — probably within reach with existing acceleration + LTE bookkeeping. What it can never give: anything about the *one* fixed start (Tao says this explicitly about Collatz; identical in mirror image). Read Tao for the renewal/characteristic-function toolkit (possibly reusable for branch-word equidistribution mod q^k), not the headline theorem.

---

## 2. Krasikov–Lagarias difference inequalities (the x^0.84 bound)

**(i) What is proved.** Krasikov–Lagarias, "Bounds for the 3x+1 problem using difference inequalities", *Acta Arith.* 109.3 (2003), 237–258 (arXiv:math/0205002): #{n ≤ x : orbit reaches 1} ≥ x^{0.84}. Ladder: Crandall 1978 (x^0.05), Sander (x^0.25), Krasikov 1989 (x^{3/7}), Wirsching 1993 (x^0.48), Applegate–Lagarias *Math. Comp.* 64 (1995) — tree-search method and Krasikov inequalities reaching x^0.81 — then 0.84, still the record. (Liu, arXiv:2512.13760, Dec 2025, reaches only x^0.3227 by a different construction; not an advance.)

**(ii) Technique.** Count predecessors of 1 stratified by residues mod 3^k; backward map branches (2y always; (2y−1)/3 when y ≡ 2 mod 3); derive *difference inequalities* between counts at different scales across residue classes; certify a feasible exponential growth profile by computer-aided nonlinear programming (0.84 used mod 3^9). Inputs: exact backward branching + elementary counting; no probabilistic model.

**(iii) Transferability: high, in the direction we want.** Sign flip: for 3x+1 the forward map contracts so the backward tree of 1 is *thick* (lower bounds); for our expanding F the backward tree of H is *thin*, and the same stratified counting gives **upper** bounds — "halting set is small". Concretely: (a) H-predecessor counting is a direct analog of Applegate–Lagarias tree search — enumerate branch words with value ≤ x; drift deficit makes the count x^c, c < 1; our LTE bound controls within-ascent structure; remaining work is a generating-function/large-deviation count over branch words. **The most concrete theorem available to us.** (b) The Krasikov inequality-system refinement would sharpen c toward the true exponent, with congruence stratification mod q^k — our no-congruence-invariant theorem does not obstruct this (it forbids *separating*, not counting). (c) Cannot say anything about the fixed start's orbit.

---

## 3. Transfer operators and functional equations

**(i) What is proved, rigorously.**
- Berg–Meinardus, *Results in Mathematics* 25 (1994), 16–23; *Rostock. Math. Kolloq.* 48 (1995): Collatz conjecture ⟺ the solution space of a pair of linear functional equations on the unit disk is exactly 2-dimensional (eigenvalue-1 multiplicity 2). Exact equivalence, but a *reformulation* with no independent spectral input.
- Neklyudov, arXiv:2106.11859, *Results in Mathematics* (2024): Berg–Meinardus-type operator on H^2(D); cycles and divergent trajectories correspond to fixed-point classes; index of Id − T bounds cycle counts; adjoint has no nontrivial H^2 fixed points. The conjecture is re-expressed as absence of extra spectrum; no mechanism to exclude it. (Opfer's 2011 claimed proof along these lines had a fatal gap — cautionary tale.)
- Wirsching, *The Dynamical System Generated by the 3n+1 Function*, Springer LNM 1681 (1998): rigorous predecessor-counting machinery, 3-adic averages, asymptotically homogeneous Markov chain on residues; the spectral/mixing statement that would close it is exactly what is open.
- **Certified spectral gaps** as technology: Lasota–Yorke inequalities + validated numerics now yield *certified* spectral data — most recently "Certified spectral approximation of transfer operators and the Gauss map" (arXiv:2602.19435, 2026); earlier: Galatolo–Nisoli–Saussol rigorous invariant densities.

**(ii) Hypotheses.** Certified-spectrum methods need a quasi-compact transfer operator: genuinely expanding piecewise map with bounded distortion, on *real* spaces — not the integer orbit.

**(iii) Transferability: medium for a sub-goal, nil for halting.** Our mantissa backbone is where this bites: if the real model is a pure irrational **rotation**, no spectral gap (use continued-fraction/discrepancy arithmetic: three-distance, Ostrowski); if the real extension is piecewise-affine **expanding**, the certified pipeline could give "real-extension transfer operator has spectral gap γ, hence exponential equidistribution of typical real orbits and quantitative avoidance statistics for the windows encoding H" — a publishable rigorous component making the randomness heuristic a theorem *for a.e. real seed*. Berg–Meinardus-style reformulations: difficulty-preserving; low priority.

---

## 4. 2-adic and automata-theoretic formulations

**(i) What is proved.**
- **2-adic conjugacy.** Lagarias, *Amer. Math. Monthly* 92 (1985): T extends to a 2-adic isometry; parity-vector map conjugates T to the shift; Haar preserved. Matthews–Watts (*Acta Arith.* 1984/85), Möller: for generalized mappings of relatively-prime type, the d-adic extension preserves Haar and is **strongly mixing, hence ergodic** (K. Matthews's survey "Generalized 3x+1 mappings: Markov chains and ergodic theory"). Consequence: branch sequences of Haar-a.e. d-adic points are normal — while every integer question lives in a Haar-null set. Bernstein (1994) explicit inverse; **Bernstein–Lagarias, "The 3x+1 conjugacy map", *Canad. J. Math.* 48 (1996), 1154–1169**: Φ mod 2^n has order 2^{n−4} (n ≥ 6); Conjugacy Finiteness Conjecture. Rigidity: Φ is not structured enough to transport density statements (Monks–Yazinski constraints on shift-induced conjugacies).
- **Automata.** Shallit–Wilson, *Bull. EATCS* 46 (1992), 182–185: for fixed iteration budget t, {n : some iterate within t reaches 1} is **regular** (doubly-exponential DFA; singly exponential via Stérin, RP 2020, LNCS 12448). Stérin–Woods (arXiv:2007.06979): Collatz on mixed base-2/3 strings *is* base conversion — why space-time diagrams resist finite-state analysis. Full predecessor set of 1 not known (or expected) to be regular. Conway 1972 / Kurtz–Simon 2007: generalized Collatz halting undecidable, so no uniform automaton for the class.
- **Mahler / Mendès France.** Mahler's Z-number problem (1968) — is there x > 0 with {x(3/2)^n} < 1/2 for all n — open; automatic-sequence methods prove Collatz-type parity data is not p-automatic in any useful sense.

**(iii) Transferability: two usable pieces.** (a) Haar-ergodicity of the q-adic extension of our return maps is likely provable verbatim (Matthews–Watts hypotheses checkable) — gives "for Haar-a.e. q-adic start, branch sequence normal, orbit a.s. never hits H": the correct formalization of the randomness heuristic (with the standard Z-is-null caveat). (b) Shallit–Wilson/Stérin bounded-budget regularity transfers directly: {starts halting within t accelerated steps} is regular, size exp(O(t)) — a rigorous complexity certificate for the verified-search frontier and a transfer-matrix exact-counting tool for the halting-basin exponent c of item 2.

---

## 5. Baker's method, S-unit equations, Pillai gaps

**(i) What is proved.**
- **Cycles.** Steiner (1977): no nontrivial 1-cycles (first Baker application). Simons–de Weger, *Acta Arith.* 117 (2005), 51–70: no m-cycles for m ≤ 68 (Laurent–Mignotte–Nesterenko two-log bounds, Rhin's estimate, continued-fraction reduction, verified range). **Hercher, *J. Integer Seq.* 26 (2023), art. 23.3.5 (arXiv:2201.00406): no m-cycles, m ≤ 91**; verification frontier reduced to n ≤ 3·2^69. Eliahou (*Discrete Math.* 1993): any nontrivial cycle has length ≥ 17,087,915 (continued fraction of log2 3). Cycle equation is S-unit-type; Evertse–Győry qualitative; all quantitative work runs through two/three-log Baker bounds.
- **Pillai gaps.** |2^a − 3^b| > 2^a·a^{−13.3} for large a effectively (Rhin's |u log2 + v log3| > e^{−13.3(1.77 + log L)}); |2^a − 3^b| > 2^{(1−ε)a} ineffectively (Ridout/Roth). Stroeker–Tijdeman (1982): Pillai's specific (3,2) conjecture. Bennett, *J. Number Theory* 98 (2003) / *Canad. J. Math.* 53 (2001): |p^a − q^b| = c has ≤ 2 solutions. Mihailescu (2004): Catalan. General Pillai open.
- **Halting-type precedent.** No precedent inside Collatz literature for Baker applied to *reaching a power of 2* (all applications are cycles). The genuine precedent is next door: **perfect powers / S-units in recurrence orbits** — Pethő (1982), Shorey–Stewart (1983): nondegenerate binary recurrences contain finitely many perfect powers, effectively. Bugeaud–Mignotte–Siksek, *Ann. of Math.* 163 (2006): perfect powers in Fibonacci = {0, 1, 8, 144} (Baker + modularity). Ostafe–Shparlinski: polynomial-dynamics analogs.

**(ii) Key inputs.** Baker: |a log p − b log q| > exp(−C log a·log b). To use on an orbit you need an *exact algebraic identity* (cycle equation, recurrence closed form) reducing "orbit hits target" to "small linear form in logs". Effective; constants combine well with verified computation.

**(iii) Transferability: our home turf, best-developed lever.** Our LTE/Baker run bound is precisely the Pethő/Shorey–Stewart pattern. Realistic extensions:
- Push from "log-log length of halting runs" to **effective finiteness of halting opportunities within any single structured run family** (Bennett's ≤ 2 solutions as model statement).
- The m-cycle program's *architecture* (Baker bound above + continued-fraction reduction + verified computation below, meeting in the middle) transfers to bounding **halting within any branch-word family with bounded block count** — a graded family of Pi-0-1 statements closable one by one, exactly as m = 1..91 fell. In the agent's assessment, **the only known technology proving unconditional statements about the actual orbit**.
- Hard limit: Baker cannot handle unboundedly many alternations — same reason cycles are only excluded to m ≤ 91.

---

## 6. Recent (2023–2026) rigorous Collatz-adjacent work

- Gonçalves–Greenfeld–Madrid (*Indiana UMJ* 2025) — contraction threshold q < p^{p/(p−1)}.
- Hercher (2023) — m ≤ 91. Barina (*J. Supercomputing* 2021, ongoing) — convergence verified for all n ≤ ~2^71.
- **Yolcu–Aaronson–Heule** (CADE 2021 / *JAR* 67 (2023), arXiv:2105.14697): Collatz ⟺ termination of a string rewriting system over mixed binary–ternary representations; *negative result* — natural matrix interpretations (even with dependency pairs) cannot prove termination of the unary Collatz system — while automatically proving weakenings. Warns which automated termination certificates are structurally too weak.
- **Carelli**, "Loop termination and generalized Collatz sequences", ICALP 2026 (arXiv:2605.15094): termination of one-variable linear-constraint loops decidable in PTIME *conditional on* a generalized-Collatz conjecture; cyclic-trace structure theorem. Places our machine class at the decidability frontier of program termination.
- bbchallenge / Antihydra (2024–): the community's finite-state toolset provably cannot see cryptid halting — matching our no-congruence theorem. Our program is effectively producing the theory these cryptids need; cite both ways.
- Certified transfer-operator spectra (arXiv:2602.19435, 2026); Neklyudov (2024).
- **ccchallenge.org** (2025–): community formalization of the Collatz literature (363-paper catalog; Böhm–Sontacchi formalized). Infrastructure if we want theorems machine-checked.
- Cautionary: steady stream of claimed proofs (Lyapunov, "spectral calculus", 2-adic measure "proofs") — none survive; the 2-adic ones founder on Haar-null-ness of Z.

---

## 7. "Orbit avoids sparse set" as a subject

- **Affine sieve** (Bourgain–Gamburd–Sarnak, *Invent. Math.* 179 (2010); Salehi Golsefidy–Sarnak, *JAMS* 2013): saturation for orbits of Zariski-dense subgroups; engine = expansion of congruence quotients of the *group*.
- **Shrinking targets / dynamical Borel–Cantelli** (Chernov–Kleinbock, *Israel J. Math.* 122 (2001) +): for expanding/hyperbolic maps with Gibbs measures, divergent-measure targets are hit i.o. for a.e. point; convergent direction gives a.e. avoidance.
- **Thin-set-hitting in arithmetic dynamics**: Pethő, Shorey–Stewart, Bugeaud–Mignotte–Siksek; Silverman (integer points in orbits, 1993); Ostafe–Shparlinski; dynamical Mordell–Lang (Bell–Ghioca–Tucker, AMS Surveys 2016).
- **Trapped-orbit rigidity for ×3/2**: **Flatto–Lagarias–Pollington, *Acta Arith.* 70 (1995), 125–147: for every real ξ > 0, limsup {ξ(3/2)^n} − liminf {ξ(3/2)^n} ≥ 1/3** — no orbit of ×3/2 is trapped in a window of length < 1/3. Mahler's Z-number question (window [0,1/2)) open; Dubickas refinements (2008–2019).

**Transferability map:** Affine sieve **inapplicable** — a single orbit of a single map is the degenerate case where the sieve's engine vanishes; sharper, our no-congruence theorem proves the congruence quotients carry *zero* information — the sieve's only fuel provably does not exist. Worth writing as a short "no-sieve" meta-theorem. Dynamical Borel–Cantelli: right theorem about the wrong points — plain BC already gives a.e. q-adic avoidance; strong-BC upgrades to precise hitting statistics for typical seeds (provable version of the stochastic model); integer start is measure zero, no help beyond. Diophantine orbit results: the only genuine single-orbit technology. **FLP deserves special attention** for the multiplicative machines: "halting = mantissa orbit enters shrinking windows around powers of q" is dual to FLP's trapped-window setting; their carry-combinatorics is one of very few unconditional single-orbit-family theorems for a ×(p/q)-type expanding map. An FLP-style theorem for our orbits would be the first non-Baker unconditional constraint.

---

## Recommendations (agent's ranking)

1. **Backward-tree / branch-word counting for a halting-basin density theorem.** Provable now with existing acceleration + LTE inputs: "#{starts ≤ x whose orbit halts} = O(x^c), c < 1 explicit" — the expanding-regime mirror of Krasikov–Lagarias, with Kontorovich–Lagarias's η5 ≈ 0.65049 for the 5x+1 tree (arXiv:0910.1944, *The Ultimate Challenge*, AMS 2010) as template; Shallit–Wilson/Stérin bounded-budget regular structure supplies transfer-matrix counting to pin c. Deliverable: rigorous quantitative "almost all starts never halt"; formalizes why the fixed start is a needle in a haystack.

2. **Baker/S-unit escalation along the m-cycle architecture.** Exclude halting for all branch words with ≤ B blocks (alternations), via two/three-log bounds (Rhin, Laurent–Mignotte–Nesterenko, Matveev) + continued-fraction reduction + verified orbit prefix — the Steiner -> Simons–de Weger -> Hercher escalation aimed at halting instead of cycles. The only known route to unconditional statements about *the* orbit; novelty claim: first transfer of the m-cycle program to a halting/avoidance question.

3. **Rigorous stochastic-model theorem for the real/q-adic extension.** Prove Haar-ergodicity (Matthews–Watts hypotheses) for the q-adic extension; where the real model is expanding, a certified spectral gap (Lasota–Yorke + interval arithmetic, following arXiv:2602.19435) for the mantissa return map — "for a.e. seed, hitting statistics of H are Poisson with the measured intensity". Stretch goal in the same cluster: an FLP-style carry-combinatorics bound — the one candidate for an unconditional non-Baker constraint on actual orbits.

Explicitly *not* recommended: Tao/GGM transport (provably blocked by expansion), Berg–Meinardus reformulations (difficulty-preserving), affine sieve (fuel provably absent — but write the short no-sieve meta-theorem), full-generality automata deciders (Yolcu–Aaronson–Heule negative result + ambient undecidability).

Key sources: [Tao arXiv:1909.03562](https://arxiv.org/abs/1909.03562) · [GGM arXiv:2111.06170](https://arxiv.org/abs/2111.06170) · [Krasikov–Lagarias arXiv:math/0205002](https://arxiv.org/abs/math/0205002) · [Lagarias 3x+1 page](https://dept.math.lsa.umich.edu/~lagarias/3x+1.html) · [Bernstein–Lagarias](https://cr.yp.to/papers/3x1conjmap-19960215-retypeset20220326.pdf) · [Matthews survey](http://www.numbertheory.org/PDFS/matthews-final-revised.pdf) · [Stérin–Woods arXiv:2007.06979](https://arxiv.org/pdf/2007.06979) · [Hercher m ≤ 91](https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html) · [Bennett Pillai](https://personal.math.ubc.ca/~bennett/B-Pillai.pdf) · [Kontorovich–Lagarias arXiv:0910.1944](https://arxiv.org/abs/0910.1944) · [Neklyudov 2024](https://link.springer.com/article/10.1007/s00025-024-02167-7) · [Certified spectra arXiv:2602.19435](https://arxiv.org/abs/2602.19435) · [Yolcu–Aaronson–Heule](https://link.springer.com/article/10.1007/s10817-022-09658-8) · [Carelli arXiv:2605.15094](https://arxiv.org/abs/2605.15094) · [FLP Acta Arith. 70](http://matwbn.icm.edu.pl/ksiazki/aa/aa70/aa7023.pdf) · [ccchallenge.org](https://ccchallenge.org/)
