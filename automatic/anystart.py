"""WS1, start-free variant: does ANY nonempty automatic F-invariant avoid H?

The search in search.py asks whether the specific orbit of 6 has an automatic
certificate.  This asks the stronger, start-free question:

    is there a nonempty 2-automatic I with F(I) subset of I and I cap H = empty?

A "no" at <= n states is a stronger impossibility theorem (it says automatic
certificates cannot decide ANY start of this map, not just 6).  A "yes" is
better still: every x in I then has a provably non-halting orbit, which would
be a new unconditional theorem about the Space Needle family.

Method: for a fixed transition structure, take each state s reachable by a
minimal word (i.e. s = delta(p,1)) as a seed, force acc(s) = TRUE, and Horn-
propagate the branch implications.  The least model is the smallest candidate
invariant containing a number whose word ends at s; it works iff it forces no
state of a power of 2.  Since every nonempty I contains some number, and that
number's state is such a seed, checking all seeds is complete.

Usage:  python3 anystart.py [nmax] [vmax]
"""
import sys
import time

from dfa_invariant import branch_pairs_min, icdfas, lsb_word, needle_branch, run


def candidates(delta, n, branches, vmax, false_states):
    """Yield (seed, forced) for every seed whose least model avoids H."""
    seeds = {s for s in {delta[p][1] for p in range(n)} if s not in false_states}
    imp = [set() for _ in range(n)]
    out = []
    for v in range(vmax + 1):                    # incremental: most die at v=0
        a, b = branches(v)
        for p, q in branch_pairs_min(delta, v, a, b):
            imp[p].add(q)
        out, alive = [], set()
        for seed in seeds:
            forced, stack, bad = {seed}, [seed], False
            while stack and not bad:
                p = stack.pop()
                for q in imp[p]:
                    if q not in forced:
                        if q in false_states:
                            bad = True
                            break
                        forced.add(q)
                        stack.append(q)
            if not bad:
                alive.add(seed)
                out.append((seed, frozenset(forced)))
        seeds = alive
        if not seeds:
            return []
    return out


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    vmax = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    print(f"start-free search: nonempty 2-automatic I with F(I) subset I, "
          f"I cap H = empty;  branches v = 0..{vmax}")
    for n in range(1, nmax + 1):
        false_states_words = [lsb_word(1 << v) for v in range(2 * n + 3)]
        t0, hits, tried = time.time(), [], 0
        for delta in icdfas(n):
            tried += 1
            fs = {run(delta, 0, w) for w in false_states_words}
            c = candidates(delta, n, needle_branch, vmax, fs)
            if c:
                hits.append((delta, c))
        dt = time.time() - t0
        tag = ("NONE (impossibility proved)" if not hits
               else f"{len(hits)} structure(s) with a candidate")
        print(f"n={n:2d}  structures={tried:>9,}  {tag:<34} {dt:6.1f}s")
        for delta, c in hits[:3]:
            print(f"        delta={delta}  seeds/models={[(s, sorted(f)) for s, f in c][:3]}")


if __name__ == "__main__":
    main()
