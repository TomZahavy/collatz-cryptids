"""Sweep a machine list for CRYPTID-SHAPED outer maps.

Usage:  python3 -u sweep_cryptid.py <list file> [limit] [macro budget]

This is the sweep that answers the question the rigidity census cannot:
not "is this machine easy" but "has this machine's halting problem been
reduced to a Collatz-type orbit question, and does that question have the
shape that makes such questions open".

Reports every machine with a two-level section, its measured verdict, and
-- for the cryptid-shaped ones -- the outer map itself, so the finding can
be checked and worked on independently of this code.
"""
import sys
import time

from cryptid import analyse


def main():
    path = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
    bud = int(sys.argv[3]) if len(sys.argv) > 3 else 150000
    blocks = (1, 2, 3, 4)

    codes = [ln.strip() for ln in open(path) if ln.strip()][:limit]
    census = {}
    hits = []
    t0 = time.time()
    for i, code in enumerate(codes):
        try:
            rs = analyse(code, blocks=blocks, macro_budget=bud)
        except Exception as exc:                       # noqa: BLE001
            census["ERROR"] = census.get("ERROR", 0) + 1
            print("  line %-5d ERROR %s  %s" % (i + 1, code, exc), flush=True)
            continue
        if not rs:
            census["no-two-level"] = census.get("no-two-level", 0) + 1
        else:
            for r in rs:
                v = r["verdict"]
                census[v] = census.get(v, 0) + 1
                if v in ("CRYPTID-SHAPED", "PREDICTABLE-BRANCHES", "NOT-EXPANDING", "CLOSED-FORM"):
                    hits.append((i + 1, r))
                    m = r["meas"]
                    print("  line %-5d %-22s b=%d  inner x -> %s*x + %s"
                          % (i + 1, v, r["blk"], r["recur"][0], r["recur"][1]),
                          flush=True)
                    print("        R_n %s" % (m["R"][:8],), flush=True)
                    print("        k_n %s   affine=%s expanding=%s"
                          % (m["k"][:8], m["affine"] is not None,
                             m["expanding"]), flush=True)
        if (i + 1) % 50 == 0:
            print("  ... %d/%d  %.0fs  %s"
                  % (i + 1, len(codes), time.time() - t0, dict(census)),
                  flush=True)
    print("\ncensus over %d machines (%.0fs):" % (len(codes),
                                                  time.time() - t0))
    for k in sorted(census, key=lambda k: -census[k]):
        print("  %-22s %6d  %5.1f%%"
              % (k, census[k], 100.0 * census[k] / len(codes)))
    print("\n%d cryptid-shaped or near-miss machines" % len(hits))
    for ln, r in hits:
        print("  line %d  %s  %s" % (ln, r["code"], r["verdict"]))


if __name__ == "__main__":
    main()
