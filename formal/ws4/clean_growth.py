"""WS4 measurement hygiene: re-measure the per-state cost of the automatic-
invariant searches under ONE load condition.

Why this exists.  RESULTS.md quotes per-state growth factors (the "rising g"
observation) assembled from runs that were executed CONCURRENTLY on a 10-core
box at varying load, with a recorded ~+-30% cross-run uncertainty.  WS4.3's
whole content is "here is the growth constant of each bound", so the numbers it
leans on must not be contaminated by which other jobs happened to be running.
The n=12 -> n=13 MSB step is the concrete trigger: it measured 10.18x under
heavy load and 5.47x after two competing multi-day jobs were killed, and those
two readings cannot be separated after the fact.

Protocol: ONE process, strictly sequential, nothing else of ours running.  Every
timing in the output file is therefore comparable to every other timing in it.
Load average is sampled before and after each instance so the condition is on
the record rather than assumed.

Usage:  python3 clean_growth.py > clean_growth.log
"""
import os
import sys
import time

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/automatic")

import msb_search
import sat_search


def stamp():
    return "load %.2f %.2f %.2f" % os.getloadavg()


def run(label, fn, n):
    t0 = time.time()
    got = fn(n)
    dt = time.time() - t0
    verdict = "SAT" if got else "UNSAT"
    print(f"  {label}  n={n:2d}  {verdict:<5}  {dt:9.1f}s   [{stamp()}]", flush=True)
    return dt


def series(label, fn, ns):
    print(f"--- {label} ---  [{stamp()}]", flush=True)
    ts = {}
    for n in ns:
        ts[n] = run(label, fn, n)
    print(f"  factors {label}:", flush=True)
    ks = sorted(ts)
    for a, b in zip(ks, ks[1:]):
        # guard against division by a sub-resolution timing
        if ts[a] >= 0.05:
            print(f"    n={a}->{b}: {ts[b] / ts[a]:6.2f}x", flush=True)
        else:
            print(f"    n={a}->{b}: (n={a} below timer resolution, skipped)", flush=True)
    print(flush=True)
    return ts


def main():
    print("WS4 clean growth measurement -- single process, strictly sequential")
    print(f"cores={os.cpu_count()}  start {time.strftime('%Y-%m-%d %H:%M:%S')}  [{stamp()}]")
    print()

    # MSB-first, leading-zero-invariant convention, Needle, branches v=0..1.
    msb = series("MSB", lambda n: msb_search.search(n, 1, "needle", verbose=False),
                 range(8, 14))

    # LSB-first, minimal-word (general) convention, Needle, branches v=0..1.
    lsb = series("LSB", lambda n: sat_search.search("needle", n, 1, True, verbose=False),
                 range(6, 11))

    print("--- cross-encoding ratio at equal n (same load condition) ---")
    for n in sorted(set(msb) & set(lsb)):
        print(f"  n={n:2d}  LSB/MSB = {lsb[n] / msb[n]:8.2f}")
    print()
    print(f"done {time.strftime('%Y-%m-%d %H:%M:%S')}  [{stamp()}]")


if __name__ == "__main__":
    main()
