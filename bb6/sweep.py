"""Sweep a list of Turing machines with the rigidity detector.

Usage:  python3 -u sweep.py <list file> [limit] [macro budget] [max blocks]

Prints one line per machine that is not NONRIGID, and a census at the
end.  The census is the point: it says what fraction of a holdout list
is even eligible for the certificate method.
"""
import sys
import time

from rigid import analyse, confirm


def main():
    path = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
    budget = int(sys.argv[3]) if len(sys.argv) > 3 else 300000
    blocks = int(sys.argv[4]) if len(sys.argv) > 4 else 4000

    codes = [ln.strip() for ln in open(path) if ln.strip()][:limit]
    census = {}
    t0 = time.time()
    for i, code in enumerate(codes):
        r = analyse(code, macro_budget=budget, max_blocks=blocks)
        c = r["cls"]
        census[c] = census.get(c, 0) + 1
        if c in ("GEO", "POLY"):
            # a fit is a conjecture until it survives phases it never
            # saw; anything that fails here is a transient, not structure
            nnew, bad = confirm(r, extra=5)
            if bad or nnew == 0:
                census[c] -= 1
                c = "UNCONFIRMED"
                census[c] = census.get(c, 0) + 1
        if c in ("GEO", "POLY", "HALTED", "INFINITE"):
            h = r.get("hit")
            extra = ""
            if h:
                extra = ("  b=%d skel=%s q=%s mod=%d nph=%d +%d ok"
                         % (r["blk"], fmt_skel(h["skel"]),
                            h["steps_fit"][1][0] if h["steps_fit"][0] == "geo"
                            else "-", h["mod"], h["nph"], nnew))
            print("  line %-5d %-8s %s%s" % (i + 1, c, code, extra),
                  flush=True)
        if (i + 1) % 100 == 0:
            print("  ... %d/%d  %.0fs  %s"
                  % (i + 1, len(codes), time.time() - t0, dict(census)),
                  flush=True)
    print("\ncensus over %d machines (%.0fs):" % (len(codes), time.time() - t0))
    for k in sorted(census, key=lambda k: -census[k]):
        print("  %-10s %6d  %5.1f%%"
              % (k, census[k], 100.0 * census[k] / len(codes)))


def fmt_skel(sk):
    lb, q, d, rb = sk
    return "%s|%s%s|%s" % (",".join(map(str, lb)), chr(65 + q),
                           ">" if d else "<", ",".join(map(str, rb)))


if __name__ == "__main__":
    main()
