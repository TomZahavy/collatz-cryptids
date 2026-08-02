"""WS6: explain the backward-tree branching deficit.

THE OBSERVATION (density/tree_branching.log).  The average backward branching
of F over an INTERVAL sits exactly on its rigorous ceiling

    c = sum_{v>=0} 1/(2^{v+1}+3) = 0.54528...

(forced, not evidence -- see the retraction in the meta report), but the
branching measured ALONG THE BACKWARD TREE rooted at the halting set is only
about 0.433 on the Needle and 0.563 on machine 3 against a ceiling of 0.808.
A 20% / 30% deficit, so far unexplained.

THE HYPOTHESIS TESTED HERE.  The pooled estimator 1 - seeds/nodes averages the
offspring count over EVERY node of the tree, and a subcritical tree is mostly
root.  Its roots are not generic integers: they are the halting set itself --
powers of 2 (Needle), powers of 27 (machine 3).  Branching off a power of 2 is
not governed by 1/A_v at all.

    EXACT BACKWARD CRITERION (proved below, verified against density.preimages):
    y has a preimage of valuation v  <=>  y = 2^v + v  (mod A_v),  A_v = 2^{v+1}+3.

    So a power of 2 admits branch v iff 2^M = 2^v + v (mod A_v) -- a question
    about the cyclic group <2> mod A_v, not about a residue class.  The density
    of such M is 1/ord_{A_v}(2) when 2^v + v lies in <2>, and ZERO when it does
    not.  Two of the first five branches are outright impossible:

      v=1: need 2^M = 3 (mod 7), but <2> mod 7 = {1,2,4}.      IMPOSSIBLE
      v=4: need 2^M = 20 (mod 35), and gcd(20,35)=5 while 2^M
           is a unit.                                          IMPOSSIBLE

    and the survivors are re-weighted (v=0 fires at density 1/4, not 1/5).

If the hypothesis is right the deficit is not a new phenomenon: it is the
already-proved forbidden-valuation structure (WS3) showing up in an estimator
that is dominated by depth 0.
"""
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/machine3")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/automatic")
from needle import is_pow2, v2                             # noqa: E402
import density as ws2                                      # noqa: E402
import density_m3 as ws2m3                                 # noqa: E402


# ---------------------------------------------------------------- Needle ----

def A(v):
    return (1 << (v + 1)) + 3


def c(v):
    """y has a valuation-v preimage iff y = c(v) mod A(v)."""
    return (1 << v) + v


def ceiling(vmax=400):
    return sum(1.0 / A(v) for v in range(vmax))


def check_criterion(hi=60000):
    """The congruence criterion agrees with the explicit backward formula."""
    bad = 0
    for y in range(3, hi):
        got = {v2(b)[0] for b in ws2.preimages(y)}
        want = {v for v in range(y.bit_length() + 2) if y % A(v) == c(v) % A(v)}
        # the formula's extra guards (b >= 3, b not a power of 2) can only
        # remove branches, never add them
        if not got <= want:
            bad += 1
    return bad


def order_of_2(n):
    """Multiplicative order of 2 mod n (n odd), or None if 2 is not a unit."""
    if n % 2 == 0:
        return None
    o, t = 1, 2 % n
    while t != 1:
        t = (t * 2) % n
        o += 1
        if o > n:
            return None
    return o


def seed_branching_predicted(vmax=20):
    """E[d(2^M)] over M, exactly, branch by branch, for v < vmax.

    Density of M with 2^M = c(v) mod A(v) is 1/ord when c(v) is in <2>, else 0.
    Only v < vmax: ord_{A_v}(2) is computed by walking the subgroup, which is
    O(A_v) = O(2^v).  The branches beyond are measured empirically instead
    (they are individually bounded by 1/A_v <= 2^-v under the interval model,
    and the exact tail is visible in the depth-0 row of the measurement).
    """
    total, rows = 0.0, []
    for v in range(vmax):
        n, target = A(v), c(v) % A(v)
        o = order_of_2(n)
        # walk the cyclic subgroup <2> mod n and look for the target
        dens, t = 0.0, 1 % n
        for _ in range(o):
            if t == target:
                dens = 1.0 / o
                break
            t = (t * 2) % n
        total += dens
        rows.append((v, n, target, o, dens, 1.0 / n))
    return total, rows


def seed_branching_measured(mmax):
    """E[d(2^M)] for M < mmax, computed straight from the congruence criterion."""
    tot = 0
    for M in range(mmax):
        y = 1 << M
        tot += sum(1 for v in range(M + 2) if y % A(v) == c(v) % A(v))
    return tot / mmax


def tree_by_depth(cap_bits, preimages, seeds):
    """Full backward tree from `seeds`; returns per-depth (nodes, children)."""
    depth_nodes, depth_children = [], []
    frontier = list(seeds)
    while frontier:
        kids = []
        for y in frontier:
            kids.extend(preimages(y))
        depth_nodes.append(len(frontier))
        depth_children.append(len(kids))
        frontier = kids
    return depth_nodes, depth_children


def run_needle(exp10):
    cap = 10 ** exp10
    seeds = []
    m = 0
    while (1 << m) <= cap:
        seeds.append(1 << m)
        m += 1
    dn, dc = tree_by_depth(cap, ws2.preimages, seeds)
    return seeds, dn, dc


# -------------------------------------------------------------- machine 3 ----

def run_m3(exp3):
    cap = 3 ** exp3
    seeds = [27 ** i for i in range(1, 400) if 27 ** i <= cap]
    dn, dc = tree_by_depth(cap, ws2m3.preimages, seeds)
    return seeds, dn, dc


def _generic_roots(bits, count, seed=12345):
    """`count` random non-power-of-2 integers of exactly `bits` bits."""
    import random
    rng = random.Random(seed)
    out = []
    while len(out) < count:
        y = rng.randrange(1 << (bits - 1), 1 << bits)
        if not is_pow2(y):
            out.append(y)
    return out


def run_random(bits, count, seed=12345):
    """CONTROL: the same backward tree, rooted at GENERIC integers instead.

    This is the experiment that decides the question.  If the deficit is caused
    by the roots being powers of 2, generic roots of the same size must sit on
    the interval ceiling at EVERY depth.  If generic roots show the same
    deficit, the effect belongs to the backward tree itself and the halting set
    has nothing to do with it.
    """
    import random
    rng = random.Random(seed)
    roots = []
    while len(roots) < count:
        y = rng.randrange(1 << (bits - 1), 1 << bits)
        if not is_pow2(y):
            roots.append(y)
    dn, dc = tree_by_depth(None, ws2.preimages, roots)
    return roots, dn, dc


def _report(name, seeds, dn, dc, ceil):
    nodes = sum(dn)
    print(f"\n{name}: {len(seeds)} seeds, {nodes} nodes, "
          f"interval ceiling {ceil:.4f}")
    print(f"  pooled 1 - seeds/nodes = {1 - len(seeds) / nodes:.4f}")
    print("  depth   nodes   children   mean offspring")
    for d, (n, k) in enumerate(zip(dn, dc)):
        print(f"  {d:>5}   {n:>5}   {k:>8}   {k / n:>14.4f}")
    deep_n = sum(dn[1:])
    deep_k = sum(dc[1:])
    if deep_n:
        print(f"  depth >= 1 pooled: {deep_k}/{deep_n} = "
              f"{deep_k / deep_n:.4f}   (vs ceiling {ceil:.4f})")


if __name__ == "__main__":
    print("=" * 70)
    print("STEP 1  the congruence criterion  y = 2^v + v (mod 2^{v+1}+3)")
    bad = check_criterion()
    print(f"  disagreements with density.preimages for 3 <= y < 60000: {bad}")
    print(f"  ceiling c = sum 1/A(v) = {ceiling():.6f}")

    print("\n" + "=" * 70)
    print("STEP 2  predicted branching off a POWER OF 2 (roots of the tree)")
    tot, rows = seed_branching_predicted()
    print("      v    A(v)   c(v) mod A   ord_A(2)     density   vs 1/A(v)")
    part = 0.0
    for v, n, t, o, d, inv in rows:
        flag = "   IMPOSSIBLE" if d == 0 else ""
        part += inv
        if v < 12:
            print(f"  {v:>5}  {n:>6}   {t:>10}   {str(o):>8}   {d:>9.6f}  "
                  f"{inv:>9.6f}{flag}")
    print(f"  v < 20 subtotal: powers-of-2 density {tot:.4f}   "
          f"interval model {part:.4f}")
    for mm in (400, 1600, 3200):
        print(f"  measured E[d(2^M)], M < {mm:>5}: "
              f"{seed_branching_measured(mm):.4f}")
    print(f"  interval ceiling (all v) = {ceiling():.4f}")

    print("\n" + "=" * 70)
    print("STEP 3  measured tree, by depth")
    for e in (240, 480, 960):
        seeds, dn, dc = run_needle(e)
        _report(f"NEEDLE cap 10^{e}", seeds, dn, dc, ceiling())
    for e in (200, 400, 800):
        seeds, dn, dc = run_m3(e)
        ceil3 = sum(2.0 / (3 ** (j + 1) + 1) for j in range(200))
        _report(f"MACHINE 3 cap 3^{e}", seeds, dn, dc, ceil3)

    print("\n" + "=" * 70)
    print("STEP 4  CONTROL: identical trees rooted at GENERIC integers")
    for bits, n in ((800, 1600), (1600, 1600), (3200, 1600)):
        roots, dn, dc = run_random(bits, n)
        _report(f"RANDOM roots, {bits} bits", roots, dn, dc, ceiling())

    print("\n" + "=" * 70)
    print("STEP 5  the mechanism, seen directly in the residues")
    print("  A node admits branch v iff it lies in ONE class mod A(v).  Powers")
    print("  of 2 do not visit those classes uniformly -- they visit the cyclic")
    print("  subgroup <2>.  If that is the whole story, the skew must persist")
    print("  at every depth for the halting tree and be absent for generic roots.")
    for mod in (5, 7):
        v = 0 if mod == 5 else 1
        print(f"\n  --- node residues mod A({v}) = {mod}; branch {v} needs "
              f"class {c(v) % mod}; uniform would be {1/mod:.3f} ---")
        for name, roots in (("halting tree (powers of 2)",
                             [1 << m for m in range(3190)]),
                            ("control (generic roots)",
                             _generic_roots(1600, 3190))):
            print(f"  {name}:")
            frontier = roots
            for d in range(4):
                if not frontier:
                    break
                n = len(frontier)
                cnt = [0] * mod
                for y in frontier:
                    cnt[y % mod] += 1
                print(f"    depth {d}  n={n:>5}   " +
                      "  ".join(f"{k / n:.3f}" for k in cnt))
                frontier = [b for y in frontier for b in ws2.preimages(y)]

    print("\n" + "=" * 70)
    print("STEP 6  machine 3: the same order arithmetic at the root")
    from machine3_map import branch as m3branch
    tot_pred = tot_int = 0.0
    print("      j  r      A     B mod A   ord_A(27)    density     vs 1/A")
    for j in range(14):
        for r in (1, 2):
            Am, Bm = m3branch(j, r)
            tgt = Bm % Am
            o, t = 1, 27 % Am
            while t != 1 % Am and o <= Am:
                t = (t * 27) % Am
                o += 1
            t, hit = 1 % Am, False
            for _ in range(o):
                if t == tgt:
                    hit = True
                    break
                t = (t * 27) % Am
            dens = 1.0 / o if hit else 0.0
            tot_pred += dens
            tot_int += 1.0 / Am
            if j < 7:
                print(f"  {j:>5}  {r}  {Am:>7}  {tgt:>10}  {o:>9}   "
                      f"{dens:>8.5f}  {1.0 / Am:>9.5f}"
                      f"{'   IMPOSSIBLE' if dens == 0 else ''}")
    print(f"  predicted root branching {tot_pred:.4f} (j <= 13)   "
          f"interval model {tot_int:.4f}")
