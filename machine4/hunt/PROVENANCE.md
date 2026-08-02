# Provenance — the machine-4 halt hunt (round 10, Aug 1 2026)

Produced by a research subagent in the Aug 1 2026 five-agent review; copied
from session scratchpad. VERIFICATION STATUS: the agent's chain (documented
in verify_accel.log and the report) is:
- m4_accel.py vs m4_base.step: step-exact (values AND base-step counts),
  exhaustive all odd a <= 2000 + 400 random to 2^22, 0 mismatches;
- m4_hunt.c vs m4_accel.py: 10,301 uncapped excursions + 200 state-exact
  capped comparisons to 2^60, 0 mismatches;
- three-way orbit agreement with the project's published 19 visits.
INDEPENDENTLY RE-VERIFIED by the main session (Aug 1, 2026): m4_accel.py
self-check re-run (exhaustive odd a <= 2000 + 400 random to 2^22, 0
mismatches, step-exact incl. base counts) and crosscheck_c.py re-run
(Set A 10,301 starts + Set B state-exact at 2^28..2^60, 0 mismatches).
Numbers are safe to cite with their [measured] labels.

TRANCHE (approved Aug 1): orbit hunt relaunched from the visit-30 frontier
a = 1,620,671,979,691 with budget 1.2e14 rounds (~2 weeks, orbit_c3.log;
the first budget of 1.5e12 exhausted mid-excursion — visit 31's excursion
is heavy-tailed, already >2.5x the mean cost). Decay sweep k = 34/36/38,
N = 500 each, caps 16*2^k (sweep_k3?.log) — settles dip-vs-decay.

Headline numbers (agent-measured): per-visit halt probability pooled
p = 0.111 (Wilson +/- 0.004), flat over k = 6..36 bits, deterministic
oscillation band 0.03-0.25; orbit extended 19 -> 30 section visits,
frontier a = 1,620,671,979,691 (2^40.6), ~7.7e11 exact base steps, no halt;
E[rounds/excursion] ~ (0.7-1.5)*2^k => cost doubles per ~1.31-bit visit;
P(no halt | budget T) ~ T^-0.118. Lucy's Moonlight: reduction implemented
(lucy.py), reproduces published checkpoints 14 / 11,292 / 10^2901.92;
per-checkpoint p ~ 0.20 but tetrational spacing => unexhibitable.
A live continuation hunt may be running (orbit_c2.log in scratchpad).
