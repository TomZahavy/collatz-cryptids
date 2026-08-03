"""Run the miner over a whole holdout list: how many machines does the
certificate method decide, end to end?

Each machine is mined; every proposed certificate is (re-)checked by
decider.check, which is the sole authority.  Accepted machines are then
independently sanity-checked by direct big-integer FRACTRAN simulation
(a machine that halts early would expose a checker bug at once).

Usage:  python3 sweep_mine.py [list.txt] [nsteps]
"""
import sys
import time

from decider import M, check, Reject
from miner import mine

LIST = sys.argv[1] if len(sys.argv) > 1 else "bbf_sz23_694_unofficial.txt"
NSTEPS = int(sys.argv[2]) if len(sys.argv) > 2 else 40000
SANITY = 200000            # brute-force steps for accepted machines


def parse(line):
    return [tuple(int(x) for x in t.strip().split("/"))
            for t in line.strip().strip("[]").split(",")]


def halts_within(fr, nsteps):
    n = 2
    for s in range(nsteps):
        for a, b in fr:
            if n % b == 0:
                n = n * a // b
                break
        else:
            return s
    return None


if __name__ == "__main__":
    rows = [l.strip() for l in open(LIST) if l.strip()]
    t0 = time.time()
    decided, failed, bad = [], 0, []
    for i, line in enumerate(rows, start=1):
        try:
            fr = parse(line)
            mach = M(fr)
        except Exception:
            failed += 1
            continue
        try:
            cert = mine(fr, nsteps=NSTEPS)
        except Exception:
            cert = None
        if cert is None:
            failed += 1
            continue
        # re-check independently, then sanity-simulate
        try:
            idx0 = check(mach, cert)
        except (Reject, AssertionError):
            bad.append((i, line, "checker disagreed on re-check"))
            continue
        h = halts_within(fr, SANITY)
        if h is not None:
            bad.append((i, line, f"SIMULATION HALTS at step {h}"))
            continue
        decided.append((i, line, cert, idx0))
        print(f"  line {i:5d}  DECIDED  n>={idx0}  "
              f"{len(cert['br'])} branch(es)  {line}", flush=True)
        if i % 100 == 0:
            print(f"    ... {i}/{len(rows)} scanned, {len(decided)} decided, "
                  f"{time.time()-t0:.0f}s", flush=True)

    print()
    print("=" * 74)
    print(f"list      : {LIST}  ({len(rows)} machines)")
    print(f"DECIDED   : {len(decided)}")
    print(f"no cert   : {failed}")
    print(f"anomalies : {len(bad)}")
    for i, line, why in bad:
        print(f"    line {i}: {why}  {line}")
    print(f"time      : {time.time()-t0:.0f}s")
    with open("mined_decided.txt", "w") as f:
        for i, line, cert, idx0 in decided:
            f.write(f"{i}\t{line}\t{idx0}\t{len(cert['br'])}\n")
    print("decided machines written to mined_decided.txt")
