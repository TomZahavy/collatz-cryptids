"""Machine 4 -- a genre correction: it is NOT a thin-halting-set machine, and
its own heuristic predicts that it HALTS.

Every other machine in this collection has a thin halting target: the orbit
has to hit a geometric set (powers of two, powers of 27, an affine family
c*2^j - ...), the per-step hit probability decays geometrically, the expected
number of hits over the whole future is a convergent sum totalling less than
10^(-huge), and "probably never halts" is the honest reading.

Machine 4 is different in both factors, and the two differences point the
same way.

T11 (H4 is not thin) [machine-verified].  On the section {b = 1} the event
    "the excursion from (a,1) halts before returning"
has empirical probability in the 2%-25% band across a in [2^6, 2^23) --
noisy, but with no decay over nine octaves.  Contrast: for the Space Needle
the analogous per-step probability at value x is O(log x / x).

T12 (the orbit visits the section only logarithmically often)
[machine-verified].  From the true start A(1,1) the section is visited 19
times in the first 6*10^7 base steps, at exponentially spaced step counts.
So over T base steps the orbit gets about c*log T halting OPPORTUNITIES, not
c*T of them.

CONSEQUENCE (heuristic, and it inverts the usual verdict).  Expected number
of halts over N section visits is about p*N with p bounded away from 0, so
it DIVERGES.  Under the same pseudorandom model that makes every other
machine here "probably never halts", machine 4 is "probably halts".  The
observed 19 visits with no halt is unremarkable: (1-p)^19 with p ~ 0.12 is
about 8%.

WHAT THIS CHANGES.  The open question for machine 4 should be read as FIND
THE HALT, not PROVE NON-HALTING; and the collection's taxonomy line for it
("sparse coincidence", "linear growth") is wrong twice over -- the
coincidence is not sparse, and while a + b does grow linearly per base step,
the SECTION values grow geometrically, which is what governs the opportunity
count.  Machine 4 is the collection's only probviously-halting machine.
"""
import random
import time

from m4_base import step, HALT
from m4_mod16 import R4

if __name__ == "__main__":
    t0 = time.time()
    P = lambda *a: print(*a, flush=True)
    P("=" * 74)
    P("MACHINE 4: not a thin-H machine; the heuristic predicts a halt")
    P("=" * 74)

    # ---- T12: the true orbit's section visits -----------------------------
    NBASE = 60_000_000
    s, sec = (1, 1), []
    halted = None
    for i in range(NBASE):
        if s[1] == 1:
            sec.append((s[0], i))
        s = step(s)
        if s == HALT:
            halted = i
            break
    P(f"\nT12 orbit from A(1,1), {NBASE:,} base steps: "
      f"{'HALTED at ' + str(halted) if halted else 'no halt'}")
    P(f"      section visits: {len(sec)}")
    P(f"      values: {[v for v, _ in sec]}")
    P(f"      at steps: {[t for _, t in sec]}")
    gaps = [sec[i + 1][1] / max(sec[i][1], 1) for i in range(4, len(sec) - 1)]
    P(f"      step-count ratios between consecutive visits (from the 5th): "
      f"min {min(gaps):.2f}, median {sorted(gaps)[len(gaps) // 2]:.2f}, "
      f"max {max(gaps):.2f}")
    P(f"      -> visits are exponentially spaced: about "
      f"{len(sec) / (NBASE.bit_length()):.2f} per doubling of the step budget")

    # ---- T11: the density does not decay ----------------------------------
    P(f"\nT11 P(excursion from (a,1) halts) for random odd a, by octave")
    rng = random.Random(5)
    rows = []
    for e, want in ((6, 300), (8, 300), (10, 300), (12, 300), (14, 300),
                    (16, 300), (18, 250), (20, 200), (22, 100)):
        lo, hi = 1 << e, 1 << (e + 1)
        n = h = cap = 0
        while n < want:
            a = rng.randrange(lo, hi) | 1
            out, _ = R4(a, cap=4_000_000)
            if out is None:
                cap += 1
                continue
            n += 1
            if out is HALT:
                h += 1
        rows.append((e, h, n, cap))
        P(f"      a in [2^{e:2d}, 2^{e + 1:2d}): halt {h:3d}/{n:3d} = "
          f"{h / n:.4f}   (excursions over the 4M-step cap: {cap})"
          f"   [{time.time() - t0:5.0f}s]")
    ps = [h / n for _, h, n, _ in rows]
    P(f"      band over nine octaves: {min(ps):.4f} .. {max(ps):.4f}; "
      f"no decay")
    assert min(ps) > 0.01, ps

    # ---- the consequence --------------------------------------------------
    pbar = sum(h for _, h, _, _ in rows) / sum(n for _, _, n, _ in rows)
    k = len(sec)
    P(f"\n    pooled p = {pbar:.4f} over {sum(n for _, _, n, _ in rows)} "
      f"sampled excursions")
    P(f"    P(no halt in the {k} observed section visits) = "
      f"(1-p)^{k} = {(1 - pbar) ** k:.4f}  -- unremarkable")
    P(f"    expected halts over N visits = {pbar:.3f}*N, which DIVERGES:")
    P(f"      the pseudorandom heuristic predicts machine 4 HALTS.")
    P(f"    (every other machine in the collection has a CONVERGENT expected "
      f"hit count, totalling < 10^-huge)")

    P(f"\n[{time.time() - t0:6.1f}s] done")
