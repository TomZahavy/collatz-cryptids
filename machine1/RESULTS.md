# Machine 1 — the congruence question, closed

Reproduced by `python3 m1_congruence.py` (log: `m1_congruence.log`, 37 s).
This round revisits the oldest case file with the machinery built for the
census, and finishes one question about it completely.

## The erratum

`mod16.py` states: *"For every non-halting D, F(D) ≡ 9 (mod 16)."* This is
**false**: `F(5) = 17 ≡ 1 (mod 16)`.

The proof there enumerates two producers of a `b = 1` anchor. A trace of the
anchor map finds **four**:

| producer | output | forced residue | fires (2 ≤ D < 400000) |
|---|---|---|---|
| R23 | `d' = 16(d−b) − 55` | ≡ 9 (mod 16) — **proved** | 354,928 |
| pump, cascade B ran | `d' = 4D*+1`, `D* ≡ 2 (mod 4)` | ≡ 9 (mod 16) — **proved** | 45,016 |
| pump, cascade B did **not** run | `d' = 4·Dl + 1`, `Dl` free | nothing | 1 (at D = 5) |
| "two", cascade B ran | `d' = D* − 1`, `D* ≡ 2 (mod 4)` | only ≡ 1 (mod 4) | 6 |

The gap is the `sweep()` else-branch: when the guard `3·Dl ≤ A` fails there
are no cascade-B rounds, `D* = Dl` directly, and `Dl ≡ 2 (mod 4)` is not
forced. `G(1,5) = sweep(7,4)`, `3·4 = 12 > 7`, so `D* = 4` and the exit is
`(1, 17)`.

**Corrected statement [machine-verified, 2 ≤ D < 400000]:** `F(D) ≡ 9
(mod 16)` for every `D` in that range **except D = 5**. The "two" producer
fires at D = 162, 7202, 22182, 50076, 121890, 388320 and gave 9 each time,
but its closed form only forces ≡ 1 (mod 4) — so the universal statement is
verified, not proved.

**The orbit corollary is unaffected**: `D₀ = 17` never meets D = 5, so
`D_k ≡ 9 (mod 16)` for all `k ≥ 1` still stands.

## T16 — a machine-independent saturation lemma [proved]

> Let `M ≥ 1` and `A, δ, ε, κ, ρ` be integers with `gcd(δ, M) = 1` and
> `gcd(ρ, M) = 1`. Put `f(n) = δn + ε + κρⁿ` and
> `R = {(c, A·c + f(n)) mod M : n ≥ n_min}`. Then from every `c₀ ∈ Z_M`, the
> residues reachable in **at least one** R-step are all of `Z_M`.

No hypothesis on `A`, none on `κ`, and `n_min` is irrelevant. Proof by strong
induction on M using `T = ord_M(ρ)` and `g = gcd(T, M) < M`: one step reaches
a full coset of `⟨g⟩`; the quotient `Z_M/⟨g⟩ ≅ Z_g` carries the same shape, so
induction gives every coset. This is the descent from `census/descent.py`,
stripped of the VAL(2) branch schema and of the multiplier hypothesis — the
first time the saturation machinery has been stated for a machine outside the
family.

Verified: 1,705 random parameter tuples with `M < 400`, all saturate;
falsifier with `gcd(δ,M) > 1` fails in 437 of 671 instances, so the
hypothesis is load-bearing.

## M1-D — the dominant branch [proved]

> For `n ≥ 1` and every integer `D` with
> `16·2ⁿ − 2n − 10 ≤ D ≤ 20·2ⁿ − 2n − 13`,
> the anchor map runs exactly `n` cascade-A rounds and then the R23 exit, and
> `F(D) = 16D − 240·2ⁿ + 32n + 169`.

Both interval endpoints are *derived*, not fitted: `15·d_n > 18·b_n + 61`
gives the lower one and `n_A(1,D) = n` the upper. Verified at 1,988 points
over `n = 1..21` (interval ends, 40 random interior points each, and both
endpoints ± 1 excluded).

## M1-N1 — no odd modulus separates machine 1 [proved]

The M1-D interval has length `4·2ⁿ − 2`, so once `2ⁿ ≥ (M+2)/4` it contains a
complete residue system mod M. Hence the **true** F-edge relation mod M
contains `{(c, 16c + 32n − 240·2ⁿ + 169) : c ∈ Z_M}`, which is T16 with
`A = 16, δ = 32, ε = 169, κ = −240, ρ = 2`. For odd M, `gcd(32,M) = gcd(2,M)
= 1`, so the closure of any residue is all of `Z_M`.

**No congruence certificate at any odd modulus can prove machine 1
non-halting** — and this already holds for the single dominant branch, so no
refinement using the other branch words can help. Verified exhaustively for
every odd `M ≤ 401` plus 25 random odd `M < 1200`.

## The complete congruence content

| direction | content |
|---|---|
| odd part | **nothing at all** (M1-N1, proved) |
| 2-part | **exactly one class, 9 (mod 16)** |

The dominant branch alone pins the closure mod 2^e to the class 25 (mod 32)
for `e ≥ 5` (closure sizes 1, 2, 4, 8, 16, 32 at `e = 5..10`); taking all
branches together restores the second lift 9 (mod 32), so no `2^e` with
`e ≥ 5` says more than mod 16 does.

Every congruence fact about machine 1's orbit is therefore "`D ≡ 9 (mod 16)`",
and `mod16.py` item 4 already showed that this does not separate the orbit
from H. **The congruence method is closed on machine 1**, and machine 1 is
the first case-file machine placed on the β-even side of the program's parity
dichotomy: a genuine 2-adic confinement, and no odd-side information at all.

## Files

* `m1_congruence.py`, `m1_congruence.log` — this round.
* `mod16.py` — the earlier confinement analysis (see the erratum above).
* `formal.py` — the anchor map `G` and its verification against step
  composition; `onedim.py` — the return map `F`.
