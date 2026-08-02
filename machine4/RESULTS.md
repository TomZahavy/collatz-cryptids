# Machine 4 — a 2-adic image theorem, and a genre correction

Two scripts this round:

* `m4_mod16.py` (log `m4_mod16.log`, 150 s) — theorems T5–T10.
* `m4_heuristic.py` (log `m4_heuristic.log`) — T11–T12 and what they mean.

## T5 — the clean rule table [proved + machine-verified]

Substituting `a = 2k+1` into `m4_base.step` removes every `k` from the
statement of the rules:

| condition (a odd) | successor |
|---|---|
| `b ≤ a`, b even | `(2b+3, a−b)` |
| `b ≤ a`, b odd | `(2b+1, a−b+3)` |
| `b = a+1` | `(2a−1, 1)` |
| `b = a+2` | `(2a+5, 1)` |
| `b = a+3` | **HALT** |
| `b = a+4` | `(2a+3, 1)` |
| `b ≥ a+5` | `(2a+5, b−a−4)` |

Verified against the base rules exhaustively for `a < 2000`, `b ≤ a+11`, plus
300,000 random pairs to `10^12`: 0 mismatches. Note `b = a+5` lands on
`b' = 1` — it is a *return*, not a cascade step.

The section is `S = {(a,1) : a odd}`; `R4(a)` is the a-value at the first
return.

## T6 — interior confinement [proved]

**Every interior state (strictly between two section visits) has `a ≡ 3
(mod 4)`.** The first step out of the section is `(a,1) → (3, a+2)`; the three
non-returning rules produce `2b+3` (b even), `2b+1` (b odd), `2a+5` (a odd),
all ≡ 3 (mod 4); the two rules producing `a' ≡ 1 (mod 4)` both output `b' = 1`,
so their targets are section states.

## T7 — the parity lock [proved]

**Every interior state with `a ≡ 7 (mod 8)` has `b` odd.** Only the two
`b ≤ a` rules can produce `a' ≡ 7 (mod 8)` (the others give `a' ≡ 3 (mod 8)`
by T6), and both output an odd `b'` — `a−b` with b even, `a−b+3` with b odd.

Checked at the rule level over 450,000 random transitions to `10^12`
(102,568 of them landing on `a ≡ 7 (mod 8)`), and on every one of the
362,327,921 interior states visited from starts `a < 30001`.

## T8 — the image theorem [proved]

> **`R4(a) ≢ 13, 15 (mod 16)`. The image of R4 lies in {1,3,5,7,9,11}
> (mod 16).**

A return comes from exactly five configurations; writing the interior source
as `a = 4s+3` (T6):

| exit | `a'` | |
|---|---|---|
| `b = a+1` | `2a−1 = 8s+5` | |
| `b = a−1` | `2b+3 = 2a+1 = 8s+7` | |
| `b = a+4` | `2a+3 = 8s+9` | |
| `b = a+2` | `2a+5 = 8s+11` | |
| `b = a+5` | `2a+5 = 8s+11` | |

If `a ≡ 3 (mod 8)` then `s` is even and these give `{5,7,9,11}` (mod 16). If
`a ≡ 7 (mod 8)` then `b` is odd by T7, so the three even-`b` exits (`a±1`,
`a+5`) are impossible; the remaining two, with `s` odd, give `{1,3}` (mod 16).

Observed exactly this split over starts `a < 30001`: from `a ≡ 3 (mod 8)`,
exits `b = a−1` ×1996, `a+1` ×1682, `a+2` ×1274, `a+4` ×1533, `a+5` ×1338;
from `a ≡ 7 (mod 8)`, only `b = a+2` ×915 and `b = a+4` ×4371.

A corollary worth noting: **`b = a+3` is even, so a state with `a ≡ 7 (mod 8)`
can never halt directly.**

## T9 — the unreachable quarter [proved]

The primary halting family is `h_j = 16·2^j − j − 12`, `j` odd (every member
halts in one R4-step; verified for `j = 1..17`). Since `16·2^j ≡ 0 (mod 16)`,

  `h_j ≡ 4 − j (mod 16)`,

so `h_j ≡ 15` iff `j ≡ 5 (mod 16)` and `h_j ≡ 13` iff `j ≡ 7 (mod 16)`. By T8
those are never return values.

> **Exactly a quarter of the primary halting family — the `j ≡ 5, 7 (mod 16)`,
> two of the eight odd classes — is unreachable by any orbit after its first
> return to the section, from any start.**

126 of the 500 odd `j < 1000` are blocked, all ≡ 5 or 7 (mod 16); the first
are `j = 5, 7, 21, 23, 37, 39, 53, 55`, i.e. `h = 495, 2029, …`.

This does **not** decide machine 4 — three quarters of the family survives,
and the deeper halts outnumber the primary family by ~1000:1.

## T10–T12 — the genre correction

Every other machine in this collection has a **thin** halting target: the
per-step hit probability decays geometrically, the expected number of hits
over the whole future is a convergent sum below `10^-huge`, and "probably
never halts" is the honest reading.

Machine 4 is different in both factors — see `m4_heuristic.log` for the
numbers — and the two differences point the same way:

* **T11 [machine-verified].** The probability that an excursion from `(a,1)`
  halts before returning, by octave of `a` (random odd `a`):

  | `a ∈` | 2^6 | 2^8 | 2^10 | 2^12 | 2^14 | 2^16 | 2^18 | 2^20 | 2^22 |
  |---|---|---|---|---|---|---|---|---|---|
  | halt rate | .037 | .073 | .077 | .183 | .067 | .170 | .240 | .035 | .080 |
  | sample | 300 | 300 | 300 | 300 | 300 | 300 | 250 | 200 | 100 |

  Band 0.035–0.240 over nine octaves, pooled `p = 0.1094` over 2,350
  excursions. Noisy, but **no decay**. (Contrast the Space Needle, where the
  analogous probability at value `x` is `O(log x / x)`.)
  *Caveat:* excursions exceeding a 4·10^6-step cap were discarded (0 below
  2^18, 11 / 3 / 54 in the last three octaves); if long excursions halt at a
  different rate the top-octave estimates are biased. The claim that survives
  cleanly is the absence of geometric decay, not the exact value of `p`.
* **T12 [machine-verified].** From the true start `A(1,1)` the section is
  visited only **19 times in the first 6·10^7 base steps**, at exponentially
  spaced step counts (0, 8, 105, 222, 356, 1722, 1757, 3127, 3491, 122610,
  477258, 661107, 663109, 855564, 4469796, 5965440, 8774394, 11555885,
  54331591) — about 0.73 visits per doubling of the step budget. So the orbit
  gets `c·log T` halting *opportunities* over `T` steps, not `c·T`.

**Consequence (heuristic).** Expected halts over `N` section visits is `≈ p·N`
with `p` bounded away from 0, which **diverges**. Under the same pseudorandom
model that makes every other machine here "probably never halts", machine 4
is **probably halts**. The observed 19 visits with no halt is unremarkable:
`(1−p)^19 = 0.111`.

### What this changes

1. The collection's taxonomy row for machine 4 — "sparse coincidence",
   "linear growth ≈2.34" — is wrong twice. The coincidence is not sparse; and
   while `a + b` does grow linearly per *base step*, the **section** values
   grow geometrically, and it is the section that governs the opportunity
   count.
2. The open question for machine 4 should be read as **find the halt**, not
   prove non-halting. That is a search problem with a concrete accelerator
   available (the T3 cascade closed form), not a barrier problem.
3. Machine 4 is the collection's only *probviously-halting* machine — the
   same genre as Lucy's Moonlight on the bbchallenge side, and the first one
   we hold.
