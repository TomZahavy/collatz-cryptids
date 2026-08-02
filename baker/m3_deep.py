"""Machine 3: iterating the sieve backwards -- the halting basin, explicitly.

The v_3 = 1 theorem (m3_theorem.py) pins the LAST step.  Because machine 3's
halting set is geometric and the branch maps are affine, the preimage of a
geometric family is again a geometric family, so the sieve ITERATES.  This file
computes the exact families at each depth and sieves each one.

A family is  {(A*R^t + B)/M : t >= t0}  -- all members integers by construction.
For a branch with data (N, D, P) [see sieve.py], a member h has a preimage iff
N | h - P, i.e.  A*R^t = M*P - B  (mod M*N), and then

    a = P + D(h - P)/N = (D*A*R^t + D(B - M*P) + M*N*P) / (M*N),

which is a family of the same shape with R -> R^w, w = ord(R, M*N).  The
preimage must ALSO satisfy the branch guard v_3(a) = j and (a/3^j) mod 3 = r;
that is checked directly on the produced integers.
"""
import sys
from math import gcd

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/machine3")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/automatic")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/baker")
from m3_accel import v3                                    # noqa: E402
from machine3_map import G                                 # noqa: E402
from sieve_m3 import affine                                # noqa: E402

JMAX = 24
DEPTH = int(sys.argv[1]) if len(sys.argv) > 1 else 4


class Fam:
    """{(A*R^t + B)/M : t >= t0}, with a human-readable provenance."""

    def __init__(self, A, R, B, M, t0, path):
        g = gcd(gcd(A, B), M)
        self.A, self.B, self.M = A // g, B // g, M // g
        self.R, self.t0, self.path = R, t0, path

    def val(self, t):
        num = self.A * pow(self.R, t) + self.B
        assert num % self.M == 0, "family not integral"
        return num // self.M

    def contains(self, y):
        """Exact membership: is y = (A*R^t + B)/M for some integer t >= t0?"""
        x = self.M * y - self.B
        if x <= 0 or x % self.A:
            return False
        x //= self.A
        t = 0
        while x % self.R == 0:
            x //= self.R
            t += 1
        return x == 1 and t >= self.t0

    def __repr__(self):
        return (f"({self.A}*{self.R}^t {'+' if self.B >= 0 else '-'} "
                f"{abs(self.B)})/{self.M}, t>={self.t0}")


def order(a, n):
    a %= n
    o, x = 1, a
    while x != 1:
        x = x * a % n
        o += 1
        if o > n:
            return None
    return o


def dlog_scan(A, R, C, mod, limit):
    """least t with A*R^t = C (mod mod), scanning one full rho of R^t."""
    seen, val, t = {}, 1, 0
    while val not in seen and t <= limit:
        if (A * val - C) % mod == 0:
            return t
        seen[val] = t
        val = val * R % mod
        t += 1
    return None


def preimage_family(fam, j, r):
    """The subfamily of `fam` reachable from branch (j, r), or None."""
    N, D, P, _ = affine(j, r)
    mod = fam.M * N
    if gcd(fam.R, mod) != 1:
        return None                                  # (never happens here)
    w = order(fam.R, mod)
    if w is None:
        return None
    tau = dlog_scan(fam.A, fam.R, fam.M * P - fam.B, mod, w + 1)
    if tau is None:
        return None                                  # branch (j,r) is forbidden
    if tau < fam.t0:                                 # shift up by whole periods
        tau += ((fam.t0 - tau + w - 1) // w) * w
    A2 = D * fam.A * pow(fam.R, tau)
    B2 = D * (fam.B - fam.M * P) + fam.M * N * P
    return Fam(A2, pow(fam.R, w), B2, fam.M * N, 0, fam.path + [(j, r)])


def sieve_family(fam, jmax=JMAX):
    """All branches that can produce a member of `fam`, with guard check."""
    kids = []
    for j in range(jmax + 1):
        for r in (1, 2):
            child = preimage_family(fam, j, r)
            if child is None:
                continue
            # verify: the produced integers really are on branch (j, r) and
            # really do map into `fam`
            good = True
            for t in range(child.t0, child.t0 + 2):
                a = child.val(t)
                if a < 2:
                    good = False
                    break
                jj, MM = v3(a)
                mm, rr = divmod(MM, 3)
                if (jj, rr) != (j, r) or (mm == 0 and rr == 1):
                    good = False
                    break
                if not fam.contains(G(a)):           # exact membership, no window
                    good = False
                    break
            if good:
                kids.append(child)
    return kids


if __name__ == "__main__":
    # depth 0: the halting set H = {27^k : k >= 1} = {27 * 27^t : t >= 0}
    root = Fam(27, 27, 0, 1, 0, [])
    print(f"depth 0 (the halting set H): {root}")
    print(f"  members: {[root.val(t) for t in range(3)]}\n")

    level, hist = [root], []
    for d in range(1, DEPTH + 1):
        nxt = []
        for fam in level:
            nxt.extend(sieve_family(fam))
        if not nxt:
            print(f"\n  *** THE BACKWARD TREE DIES AT DEPTH {d} ***")
            break
        # which valuations can occur at each position back from the halt?
        pos = [sorted({f.path[i][0] for f in nxt}) for i in range(d)]
        hist.append((d, len(nxt), pos))
        print(f"depth {d}: {len(level)} -> {len(nxt)} families;  valuations "
              f"possible at each step back from the halt:")
        for i, s in enumerate(pos):
            print(f"     step -{i + 1}:  v_3 in {s}"
                  f"{'   <== PINNED' if len(s) == 1 else ''}")
        smallest = min(nxt, key=lambda f: f.val(f.t0))
        v = smallest.val(smallest.t0)
        print(f"   smallest member at this depth: {v:,}"
              if v < 10 ** 18 else
              f"   smallest member at this depth: ~10^{len(str(v)) - 1} "
              f"({len(str(v))} digits)")
        print(f"     via branch path (last step first) {smallest.path}\n")
        level = nxt

    print("SUMMARY  depth : #families : valuations at the last step / next-to-last")
    for d, n, pos in hist:
        print(f"  {d:>4}  : {n:>4}      : {pos[0]}"
              f"{' / ' + str(pos[1]) if len(pos) > 1 else ''}")
