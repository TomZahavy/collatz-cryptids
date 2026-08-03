"""Equivalence sweep over an ARBITRARY prime basis (no 5-prime cap)."""
import sys
from itertools import permutations
from collections import defaultdict


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def parse(line):
    out = []
    for t in line.strip().strip("[]").split(","):
        a, b = t.strip().split("/")
        out.append((factor(int(a)), factor(int(b))))
    return out


def primes_of(prog):
    s = set()
    for a, b in prog:
        s |= set(a) | set(b)
    return sorted(s)


def relabel(prog, mapping):
    def mv(d):
        return tuple(sorted((mapping[p], e) for p, e in d.items()))
    return tuple((mv(a), mv(b)) for a, b in prog)


def canon(prog, fix2):
    """Least image under permutations of the non-2 primes (fix2=True) or
    of all primes (fix2=False).  Primes are renamed to 0,1,2,... by rank
    so that programs over different actual primes can still match."""
    ps = primes_of(prog)
    if fix2:
        others = [p for p in ps if p != 2]
        best = None
        for perm in permutations(range(len(others))):
            m = {2: 0}
            for i, p in enumerate(others):
                m[p] = perm[i] + 1
            img = relabel(prog, m)
            if best is None or img < best:
                best = img
        return best
    best = None
    for perm in permutations(range(len(ps))):
        m = {p: perm[i] for i, p in enumerate(ps)}
        img = relabel(prog, m)
        if best is None or img < best:
            best = img
    return best


if __name__ == "__main__":
    path = sys.argv[1]
    rows = [l.strip() for l in open(path) if l.strip()]
    progs = {}
    for i, line in enumerate(rows, start=1):
        try:
            p = parse(line)
            if len(primes_of(p)) <= 7:      # keep permutation count sane
                progs[i] = p
        except Exception:
            pass
    print(f"{path}: {len(rows)} rows, {len(progs)} usable "
          f"(<=7 distinct primes)")
    for fix2, label in ((True, "R1 pi fixes 2  [SOUND for start n=2]"),
                        (False, "R2' all prime perms  [NOT sound]")):
        g = defaultdict(list)
        for i, p in progs.items():
            g[canon(p, fix2)].append(i)
        multi = {k: v for k, v in g.items() if len(v) > 1}
        saved = sum(len(v) - 1 for v in multi.values())
        print(f"  {label}")
        print(f"      classes {len(g)}   multi-classes {len(multi)}   "
              f"removable {saved}  ({100.0*saved/len(progs):.2f}%)")
        if fix2 and multi:
            for k, v in list(sorted(multi.items(),
                                    key=lambda kv: -len(kv[1])))[:3]:
                print(f"        class {v[:6]}")
