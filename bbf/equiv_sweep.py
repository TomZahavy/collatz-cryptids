"""Can the holdout list be SHRUNK by proving machines equivalent?

Two FRACTRAN programs over the same prime basis are *conjugate* if some
permutation of the primes carries one program, fraction by fraction and
IN ORDER, onto the other.  Conjugate programs have literally the same
dynamics up to renaming the coordinates.

THE CATCH, and it is the whole content of the idea: every program starts
at n = 2.  A permutation pi maps the start state e_2 to e_{pi(2)}, so a
conjugacy transports the orbit-from-2 question only when

                          pi fixes the prime 2.

Permutations moving 2 give a conjugacy of the *dynamics* but relate
program A started at 2 to program B started at some other prime -- a true
statement about the maps, useless for the holdout question by itself.
(That weaker relation is what certificate-level template isomorphism in
decider.py captures: it allows the two machines to have different
transients and only requires their PHASE structure to correspond.  It is
strictly more general and strictly more expensive: it needs certificates,
hence a decision, for both machines.)

So there are two reductions, and only the first is free:

  R1  STRICT CONJUGACY (this file): pi fixes 2; purely syntactic;
      decidable by trying 4! = 24 permutations; needs no certificate, no
      simulation, no decision.  Deciding one member of a class decides
      every member.
  R2  POST-ENTRY ISOMORPHISM (decider.py): allows different transients;
      needs certificates for both machines, so it presupposes decisions
      and cannot reduce the *undecided* part of the list.

R1 is the one that could shrink a holdout list, and this file measures
exactly how much.  Method: canonicalise each program by taking the
lexicographically least image under the 24 permutations fixing 2, then
group.  Any class of size > 1 is a genuine reduction.
"""
import sys
from itertools import permutations

PRIMES = (2, 3, 5, 7, 11)
IDX = {p: i for i, p in enumerate(PRIMES)}


def fac(n):
    v = [0] * 5
    for k, p in enumerate(PRIMES):
        while n % p == 0:
            n //= p
            v[k] += 1
    return None if n != 1 else tuple(v)


def parse(line):
    out = []
    for t in line.strip().strip("[]").split(","):
        a, b = t.strip().split("/")
        fa, fb = fac(int(a)), fac(int(b))
        if fa is None or fb is None:
            return None
        out.append((fa, fb))
    return tuple(out)


def unfac(v):
    n = 1
    for p, e in zip(PRIMES, v):
        n *= p ** e
    return n


def apply_perm(prog, perm):
    """perm[i] = new index of axis i."""
    def mv(v):
        w = [0] * 5
        for i, x in enumerate(v):
            w[perm[i]] = x
        return tuple(w)
    return tuple((mv(a), mv(b)) for a, b in prog)


# the permutations of the five axes that FIX axis 0 (the prime 2)
PERMS_FIX2 = [(0,) + p for p in permutations((1, 2, 3, 4))]
PERMS_ALL = list(permutations(range(5)))


def canon(prog, perms):
    return min(apply_perm(prog, p) for p in perms)


def show(prog):
    return "[" + ", ".join(f"{unfac(a)}/{unfac(b)}" for a, b in prog) + "]"


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "bbf_sz23_21233.txt"
    rows = [l.strip() for l in open(path) if l.strip()]
    progs, bad = {}, 0
    for i, line in enumerate(rows, start=1):
        p = parse(line)
        if p is None:
            bad += 1
            continue
        progs[i] = p
    print("=" * 74)
    print(f"EQUIVALENCE SWEEP: {path}  ({len(progs)} parsed, {bad} skipped)")
    print("=" * 74)

    for name, perms, note in (
            ("R1  strict conjugacy (pi fixes prime 2) -- SOUND for the "
             "holdout question", PERMS_FIX2, ""),
            ("R2' all prime permutations -- NOT sound for start n = 2; "
             "shown only to size the gap", PERMS_ALL, "")):
        groups = {}
        for i, p in progs.items():
            groups.setdefault(canon(p, perms), []).append(i)
        multi = {k: v for k, v in groups.items() if len(v) > 1}
        saved = sum(len(v) - 1 for v in multi.values())
        print(f"\n{name}")
        print(f"    classes            : {len(groups)}")
        print(f"    classes of size > 1: {len(multi)}")
        print(f"    machines removable : {saved}"
              f"   ({100.0 * saved / len(progs):.2f}% of the list)")
        if perms is PERMS_FIX2 and multi:
            big = sorted(multi.values(), key=len, reverse=True)[:5]
            print("    largest classes (line numbers):")
            for g in big:
                print(f"      size {len(g)}: {g[:8]}"
                      f"{' ...' if len(g) > 8 else ''}")
            # exhibit one class in full, as a check
            g = big[0]
            print(f"    class of size {len(g)} in full:")
            for i in g[:6]:
                print(f"      line {i:6d}  {show(progs[i])}")
