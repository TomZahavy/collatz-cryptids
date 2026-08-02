"""WS3: unconditional exclusions for halts at the end of a constant-valuation run.

THE ALGEBRA.  On the branch v_2(x) = v the Needle map is affine,
F(x) = (2^{v+1}+3)x/2^{v+1} + (v - 3/2), with fixed point x* = 2^v(3-2v)/3.  So
a run of n consecutive steps all of valuation v satisfies

    2^{(v+1)n} (3 x_n - 2^v(3-2v))  =  q_v^n (3 x_0 - 2^v(3-2v)),   q_v = 2^{v+1}+3.

If that run ENDS IN A HALT, x_n = 2^m, and since q_v is odd,

    q_v^n  |  3*2^{m-v} - 3 + 2v        (*)          [assuming m >= v]

which is a pure congruence condition -- no Baker needed for a single block.
For v = 0 it reduces to 5^n | 2^m - 1, the known LTE case (m >= 4*5^{n-1}).
For general v it is a discrete-logarithm condition, and it can be UNSOLVABLE:
then no halt can ever follow a run of that valuation, at any length and any
scale.  That is an unconditional, infinite-time exclusion.
"""
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
from needle import step1, is_pow2, v2                      # noqa: E402


def qv(v):
    return (1 << (v + 1)) + 3


def target(v, mod):
    """The residue 2^t must hit: 3*2^t = 3-2v (mod q^n)  =>  2^t = (3-2v)/3."""
    return ((3 - 2 * v) * pow(3, -1, mod)) % mod


def order(a, mod):
    o, x = 1, a % mod
    while x != 1:
        x = x * a % mod
        o += 1
        if o > 4 * mod:
            return None
    return o


def dlog(a, b, mod, bound=None):
    """Least t >= 0 with a^t = b (mod mod), by baby-step giant-step, or None."""
    n = 1
    while n * n < (bound or mod):
        n += 1
    tbl, cur = {}, 1
    for j in range(n + 1):
        tbl.setdefault(cur, j)
        cur = cur * a % mod
    factor = pow(pow(a, n, mod), -1, mod)
    cur = b % mod
    for i in range(n + 1):
        if cur in tbl:
            return i * n + tbl[cur]
        cur = cur * factor % mod
    return None


def min_exponent(v, n):
    """Least t = m - v allowed by (*), or None if the congruence is unsolvable."""
    mod = qv(v) ** n
    return dlog(2, target(v, mod), mod)


def _tests():
    # (*) is exactly the halting condition at the end of a v-run: check it
    # against real single-step halts (n = 1) found by brute force.
    found = {}
    for x in range(3, 3 * 10 ** 6):
        if is_pow2(x):
            continue
        y = step1(x)
        if is_pow2(y):
            v = v2(x)[0]
            m = y.bit_length() - 1
            assert (3 * 2 ** (m - v) - 3 + 2 * v) % qv(v) == 0, (x, v, m)
            found.setdefault(v, []).append(x)
    print(f"  every single-step halting seed below 3,000,000 satisfies (*): OK")
    print(f"    seeds by valuation: "
          f"{ {v: len(s) for v, s in sorted(found.items())} }")
    print(f"    valuations that actually occur: {sorted(found)}")

    # the closed form for a run
    for v in (0, 1, 2, 3):
        for _ in range(200):
            import random
            k = random.randrange(1, 10 ** 5)
            x = (k << (v + 1)) + (1 << v)
            if v2(x)[0] != v:
                continue
            y = step1(x)
            assert 2 ** (v + 1) * (3 * y - 2 ** v * (3 - 2 * v)) == \
                   qv(v) * (3 * x - 2 ** v * (3 - 2 * v)), (v, x)
    print("  run closed form 2^{(v+1)n}(3x_n - 2^v(3-2v)) = q_v^n(...) at n=1: OK")
    print("all run-algebra tests passed")


if __name__ == "__main__":
    _tests()
    print("\nSOLVABILITY OF (*) PER VALUATION (n = 1):")
    forbidden = []
    for v in range(0, 26):
        t = min_exponent(v, 1)
        if t is None:
            forbidden.append(v)
        print(f"  v={v:2d}  q_v={qv(v):>12,}  "
              f"{'NO SOLUTION - halt after a v-run is IMPOSSIBLE' if t is None else f'least m-v = {t} (mod ord {order(2, qv(v))})'}")
    print(f"\n  forbidden valuations below 26: {forbidden}")
