# The machine-4 halt hunt: stopped, null result

**Verdict: no halt found. Machine 4 remains undecided.** The hunt was
stopped deliberately on Aug 3, 2026, on cost grounds, not because it
failed unexpectedly.

## What was run

Two tranches, both from the verified accelerated section map
(`m4_accel.py` / `m4_hunt.c`, step-exact against `m4_base.step`):

* **Tranche 1** (Aug 1): orbit extended from the project's 19 recorded
  section visits to **30**, frontier `a = 1,620,671,979,691` (2^40.6),
  about 7.7x10^11 exact base steps. No halt. 19 of 31 dispatches missed
  the halt line by exactly 1.
* **Tranche 2** (Aug 2-3, ~20 CPU-hours over 4 cores): continuation from
  the visit-30 frontier with a 1.2x10^14 round budget, plus decay sweeps
  at k = 34, 36, 38 (N = 500 each). **Neither produced a single further
  line**: the continuation did not complete visit 31, and no sweep shard
  completed its 500-sample batch. Logs `orbit_c3.log`, `sweep_k3*.log`
  are headers only, kept as the record.

## Why it was stopped

The measured law is the reason. Per-visit halt probability is flat at
**p = 0.111** over 30 octaves (no decay), so the machine halts almost
surely under the pseudorandom model, with a median halt around 48 bits.
But excursion cost is **Theta(a)** -- linear in the section value, i.e.
exponential in bit-size -- because the interior branch stream is itself
pseudorandom (mean rule-run 1.71, essentially all 12-grams distinct), so
no acceleration exists. Section values multiply by about 3 per visit, so
each visit costs roughly triple the last.

Together: **P(no halt | compute budget T) ~ T^-0.118**. Not "run until
certain" -- a power-law gamble whose odds per unit compute keep falling.
Tranche 2's silence is exactly what that law predicts at the 2^41
frontier; it is confirmation, not surprise.

## What the null result is worth

* The orbit record stands at **30 section visits, no halt**, up from 19.
  Under the measured p, a 30-visit miss has probability ~0.02, but ~19 of
  those visits are what made machine 4 a subject in the first place, so
  the unconditioned evidence is the 11 new visits: P ~ 0.27, unremarkable.
* Machine 4 stays the portfolio's only conjectured-*halting* machine and
  the only one whose proof would be finite. Nothing here changes that.
* **The one decision-relevant open number** remains whether the apparent
  dip in p at k >= 32 (11/189 = 0.058, ~2 sigma below pooled) is
  oscillation -- like the established dips at k = 6 and k = 20 -- or
  genuine decay. Settling it needs N ~ 500 at k = 34-38, which is what
  tranche 2 failed to deliver in 20 CPU-hours. It is embarrassingly
  parallel and would take a few core-days on more hardware.

## If resumed

Resume from the visit-30 frontier `a = 1,620,671,979,691`
(`./m4_hunt orbit 1620671979691 <budget>`), and run the k-sweeps
separately and in parallel (`./m4_hunt pvisit <k> <N> <cap> <seed>`).
Do not expect a decision; expect a coin-flip whose price doubles per
visit.
