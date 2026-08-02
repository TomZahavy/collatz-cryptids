"""WS5 census: enumerate the one-schema VAL(2) family and run the pipeline.

This is the first thing the program has built that PRODUCES machines instead of
consuming them.  Every machine gets the same treatment, automatically:

  well-definedness  -> F must land in the positive integers
  simulation        -> HALT / CYCLE / GROW from the canonical start x0 = 3
  drift             -> expected log2 growth per step (heuristic model)
  ceiling           -> sum_v 1/A_v, the backward branching bound (proved)
  congruence proof  -> exact and complete for its class; a hit DECIDES the
                       machine (proved non-halting)
  sieve mass        -> fraction of steps out of which no halt can follow (proved
                       per branch, over the branches tested)

Calibration is mandatory and is run first: the decision tool must fail on the
Space Needle, which is (1,3,1,1,0) here and is known to admit no separating
congruence, and must succeed on a machine whose separation can be checked by
hand.  A decision procedure reported without both is worthless.

Usage:  python3 census.py > census.log
"""
import sys
import time

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/census")

import decide                                               # noqa: E402
from family import Machine, HALT                            # noqa: E402

X0 = 3                     # canonical start: the smallest non-halting value
RUN_CAP = 3000
CONG_MMAX = 64             # cheap filter; survivors get a deeper pass
SIEVE_VMAX = 8

ALPHA = (1, 2, 3)
BETA = (-1, 1, 2, 3, 4, 5, 6, 7)
GAMMA = (1, 2, 3)
DELTA = (0, 1, 2)
EPS = (-2, -1, 0, 1, 2)

NEEDLE = Machine(1, 3, 1, 1, 0)


def calibrate():
    """Both directions, before any result is reported."""
    print("CALIBRATION")
    got = decide.congruence_proof(NEEDLE, X0, CONG_MMAX)
    print(f"  Space Needle (1,3,1,1,0) must NOT be decided: "
          f"{'PASS' if got is None else 'FAIL -- ' + str(got)}")

    # A machine we can check by hand: alpha=1, beta=1, gamma=1, delta=0, eps=0
    # gives A_v = 2^(v+1)+1 and B_v = 2^v, so F(x) = x + k + 1 with x odd-part
    # 2k+1 -- run it and see whether the tool's verdict matches a direct check.
    hits = 0
    for mach in (Machine(a, b, g, d, e) for a in ALPHA for b in BETA
                 for g in GAMMA for d in DELTA for e in EPS):
        if not mach.well_defined(400):
            continue
        got = decide.congruence_proof(mach, X0, 24)
        if got is None:
            continue
        m, reach = got
        # independent check: simulate and confirm the orbit stays in `reach`
        x, ok = X0, True
        for _ in range(400):
            if x % m not in reach:
                ok = False
                break
            y = mach.step(x)
            if y is HALT:
                ok = False          # a proof of non-halting that halts: fatal
                break
            x = y
        print(f"  decided machine {mach} at m={m}: orbit stays in the "
              f"separating class for 400 steps: {'PASS' if ok else 'FAIL'}")
        hits += 1
        if hits == 3:
            break
    if hits == 0:
        print("  no machine was decided at m <= 24 -- the positive direction of "
              "the calibration is UNTESTED, so treat any 'decided' below with "
              "suspicion")
    print()


def classify(mach):
    verdict, steps, extra = mach.run(X0, RUN_CAP)
    row = {
        "m": mach, "verdict": verdict, "steps": steps, "extra": extra,
        "drift": mach.drift(), "ceiling": mach.ceiling(),
    }
    got = decide.congruence_proof(mach, X0, CONG_MMAX)
    row["cong"] = got[0] if got else None
    _, forb, tested, mass = decide.sieve_proof(mach, SIEVE_VMAX)
    row["sieve"] = (forb, tested, mass)
    return row


def main():
    t0 = time.time()
    print("WS5 CENSUS -- the one-schema VAL(2) family\n")
    print(f"  F(x) = (alpha*2^(v+1) + beta)k + (gamma*2^v + delta*v + eps),")
    print(f"  x = 2^(v+1)k + 2^v,  halt iff x is a power of 2,  start x0 = {X0}")
    print(f"  parameters: alpha{ALPHA} beta{BETA} gamma{GAMMA} delta{DELTA} "
          f"eps{EPS}\n")
    calibrate()

    rows, skipped = [], 0
    for a in ALPHA:
        for b in BETA:
            for g in GAMMA:
                for d in DELTA:
                    for e in EPS:
                        mach = Machine(a, b, g, d, e)
                        if not mach.well_defined():
                            skipped += 1
                            continue
                        rows.append(classify(mach))
    total = len(rows) + skipped
    print(f"enumerated {total:,} machines; {skipped:,} are not well defined "
          f"(F leaves the positive integers); {len(rows):,} analysed\n")

    from collections import Counter
    print("VERDICT BY ASYMPTOTIC MULTIPLIER alpha")
    print(f"  {'alpha':>5} {'machines':>9} {'HALT':>6} {'CYCLE':>6} {'GROW':>6} "
          f"{'decided':>8} {'mean drift':>11}")
    for a in ALPHA:
        sub = [r for r in rows if r["m"].a == a]
        c = Counter(r["verdict"] for r in sub)
        dec = sum(1 for r in sub if r["cong"])
        md = sum(r["drift"] for r in sub) / len(sub) if sub else 0.0
        print(f"  {a:>5} {len(sub):>9,} {c['HALT']:>6} {c['CYCLE']:>6} "
              f"{c['GROW']:>6} {dec:>8} {md:>11.4f}")
    print()

    decided = [r for r in rows if r["cong"]]
    print(f"DECIDED BY SEPARATING CONGRUENCE: {len(decided)} of {len(rows)}")
    for r in sorted(decided, key=lambda r: (r["cong"], str(r["m"])))[:25]:
        print(f"  {str(r['m']):>18}  m={r['cong']:>3}  drift {r['drift']:+.3f}  "
              f"ceiling {r['ceiling']:.4f}")
    if len(decided) > 25:
        print(f"  ... and {len(decided) - 25} more")
    print()

    halters = [r for r in rows if r["verdict"] == "HALT"]
    cyclers = [r for r in rows if r["verdict"] == "CYCLE"]
    print(f"HALTS from x0={X0}: {len(halters)};  CYCLES: {len(cyclers)}")
    for r in halters[:10]:
        print(f"  {str(r['m']):>18}  halts after {r['steps']} steps at {r['extra']}")
    for r in cyclers[:10]:
        print(f"  {str(r['m']):>18}  cycle of length {r['extra']} entered at "
              f"step {r['steps']}")
    print()

    # ---- structural readings, tested rather than eyeballed -----------------
    print("STRUCTURE 1: which parameter carries decidability?")
    print(f"  {'param':>7} {'value':>6} {'machines':>9} {'decided':>8} {'rate':>7}")
    for name, key in (("alpha", lambda m: m.a), ("beta", lambda m: m.b),
                      ("gamma", lambda m: m.g), ("delta", lambda m: m.d),
                      ("eps", lambda m: m.e)):
        for val in sorted({key(r["m"]) for r in rows}):
            sub = [r for r in rows if key(r["m"]) == val]
            dec = sum(1 for r in sub if r["cong"])
            print(f"  {name:>7} {val:>6} {len(sub):>9,} {dec:>8} "
                  f"{dec / len(sub):>7.1%}")
        print()

    print("STRUCTURE 2: drift and the ceiling are functions of (alpha, beta) "
          "alone --")
    print("  they cannot tell the Needle apart from its siblings.  Check:")
    groups = {}
    for r in rows:
        groups.setdefault((r["m"].a, r["m"].b), set()).add(
            (round(r["drift"], 12), round(r["ceiling"], 12)))
    bad = {k: v for k, v in groups.items() if len(v) > 1}
    print(f"    (alpha,beta) classes: {len(groups)};  classes with more than one "
          f"(drift, ceiling) value: {len(bad)}")
    needle_twins = [r for r in rows if (r["m"].a, r["m"].b) == (1, 3)]
    print(f"    machines sharing the Needle's drift and ceiling: "
          f"{len(needle_twins)}")
    print()

    print("STRUCTURE 3: the sieve separates what drift cannot.  Among those "
          "twins,")
    ms = sorted(r["sieve"][2] for r in needle_twins)
    nm = next(r for r in needle_twins if str(r["m"]) == "(1,3,1,1,0)")
    print(f"    sieve mass ranges {ms[0]:.4f} to {ms[-1]:.4f}; the Needle sits "
          f"at {nm['sieve'][2]:.4f}")
    print(f"    (WS3 measured 28.7% for the Needle over v <= 35; this is v <= "
          f"{SIEVE_VMAX})")
    heavy = sorted((r for r in rows if r["verdict"] == "GROW" and not r["cong"]),
                   key=lambda r: -r["sieve"][2])[:8]
    print("    heaviest sieves among undecided growers -- the best leads for a "
          "hand proof:")
    for r in heavy:
        print(f"      {str(r['m']):>18}  {r['sieve'][2]:>7.4f}  "
              f"({r['sieve'][0]}/{r['sieve'][1]} branches forbidden)")
    print()

    with open("/Users/tomzahavy/Documents/Claude/collatz/census/census_rows.tsv",
              "w") as f:
        f.write("alpha\tbeta\tgamma\tdelta\teps\tverdict\tsteps\tdrift\t"
                "ceiling\tcong\tsieve_forb\tsieve_tested\tsieve_mass\n")
        for r in rows:
            m = r["m"]
            f.write(f"{m.a}\t{m.b}\t{m.g}\t{m.d}\t{m.e}\t{r['verdict']}\t"
                    f"{r['steps']}\t{r['drift']:.6f}\t{r['ceiling']:.6f}\t"
                    f"{r['cong'] or ''}\t{r['sieve'][0]}\t{r['sieve'][1]}\t"
                    f"{r['sieve'][2]:.6f}\n")

    cand = [r for r in rows if r["verdict"] == "GROW" and not r["cong"]
            and r["m"].a == 1]
    print(f"CRYPTID CANDIDATES (alpha = 1, grows, undecided): {len(cand)}")
    print(f"  {'machine':>18} {'drift':>8} {'ceiling':>9} {'sieve mass':>11}  note")
    for r in sorted(cand, key=lambda r: r["drift"])[:30]:
        note = "the Space Needle" if str(r["m"]) == "(1,3,1,1,0)" else ""
        print(f"  {str(r['m']):>18} {r['drift']:>8.4f} {r['ceiling']:>9.5f} "
              f"{r['sieve'][2]:>11.4f}  {note}")
    if len(cand) > 30:
        print(f"  ... and {len(cand) - 30} more")

    print(f"\nelapsed {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
