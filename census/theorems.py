"""Theorems the census produced, with their proofs machine-checked.

The census decides 318 machines by separating congruence; those certificates
are audited in verify.py.  This file holds the two results that came out of the
OTHER decision route -- the WS3 forbidden-branch sieve -- because each needed a
uniform argument over all v that no automatic search supplies, and each is a
statement about every start, not just x0 = 3.

Run: python3 theorems.py
"""
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/census")

from family import Machine, HALT                            # noqa: E402


def t1(hi=400000, vmax=400):
    """T1.  The machine (1, 1, 2, 0, 1) never halts after its first step.

    Here A_v = 2^(v+1) + 1 and B_v = 2*2^v + 1 = 2^(v+1) + 1 = A_v, so

        F(x) = A_v k + B_v = A_v (k + 1),

    and A_v is odd and at least 3.  So F(x) always carries an odd factor
    greater than 1 and is never a power of two: the machine cannot halt after
    any step, from any start.  (It halts only if the START is a power of two.)
    """
    M = Machine(1, 1, 2, 0, 1)
    assert all(M.B(v) == M.A(v) for v in range(vmax)), "B_v = A_v fails"
    bad = 0
    for x in range(2, hi):
        y = M.step(x)
        if y is HALT:
            continue
        v = (x & -x).bit_length() - 1
        if y % M.A(v) or (y > 1 and y & (y - 1) == 0):
            bad += 1
    return bad, hi


def t2(vmax=400):
    """T2.  The machine (2, -1, 2, 1, 1) never halts after its first step.

    A_v = 2^(v+2) - 1 and B_v = 2^(v+1) + v + 1.  On branch v the map is affine
    with fixed point P0/Q0, P0 = (2v+3)2^v and Q0 = 1 - 2^(v+1), and the WS3
    sieve forbids a halt out of that branch unless Q0*2^e = P0 (mod A_v) for
    some e.

    Modulo A_v we have 2^(v+2) = 1, hence 2*Q0 = 2 - 2^(v+2) = 1, so
    Q0 = 2^(-1) and the condition collapses to

        2^(e+1) = 2v + 3   (mod 2^(v+2) - 1).

    The powers of two mod A_v are exactly {1, 2, 4, ..., 2^(v+1)} -- the order
    of 2 is v+2 -- and for v >= 1 the number 2v+3 is odd, greater than 1, and
    strictly less than A_v, so it is its own residue and is not among them.
    For v = 0, A_0 = 3 and 2v+3 = 3 = 0, which is not a power of two mod 3.

    Every branch is forbidden, so no orbit of this machine, after a step, at
    any scale, can ever halt.
    """
    bad = 0
    for v in range(vmax):
        N = (1 << (v + 2)) - 1
        Q0 = 1 - (1 << (v + 1))
        if (2 * Q0 - 1) % N:                     # Q0 = 2^-1 mod N
            bad += 1
        powers = {pow(2, j, N) for j in range(v + 2)}   # complete: ord(2) = v+2
        if ((2 * v + 3) % N) in powers:
            bad += 1
    return bad, vmax


def t3():
    """T3.  Closed form for the modulus-3 certificate.

    A member (alpha, beta, gamma, delta, epsilon) is decided at m = 3 -- that
    is, provably never halts from x0 = 3 -- if and only if

        delta = 0,   gamma = alpha,   beta + epsilon = 0     (all mod 3).

    Proof.  Mod 3 the powers of two are {1, 2}, every nonzero class, so a class
    avoiding H must be contained in {0}; it must contain x0 = 3, so it IS {0}.
    Now 3 | x with x = 2^(v+1)k + 2^v forces k = 1 (mod 3), since
    2^v = (-1)^v, and then

        F(x) = (-1)^v (gamma - alpha) + beta + delta*v + epsilon   (mod 3).

    Requiring this to vanish at v = 0, 1, 2 gives 2*delta = 0, then
    2*(gamma - alpha) = 0, then beta + epsilon = 0; and those three conditions
    conversely make it vanish for every v.  QED

    Corollary, and the reason it matters: the v-LINEAR term is what blocks the
    cheapest certificate there is.  The Space Needle has delta = 1 and so fails
    the very first test, for a reason visible in one line.
    """
    import csv
    path = "/Users/tomzahavy/Documents/Claude/collatz/census/census_rows.tsv"
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    fp = fn = tp = 0
    for r in rows:
        a, b, g, d, e = (int(r[k]) for k in
                         ("alpha", "beta", "gamma", "delta", "eps"))
        pred = d % 3 == 0 and (g - a) % 3 == 0 and (b + e) % 3 == 0
        got = r["cong"] == "3"
        tp += pred and got
        fp += pred and not got
        fn += got and not pred
    return tp, fp, fn, len(rows)


def main():
    print("CENSUS THEOREMS -- non-halting proved, for every start\n")
    bad, hi = t1()
    print(f"T1  machine (1,1,2,0,1):  F(x) = A_v (k+1) with A_v = 2^(v+1)+1 odd")
    print(f"    counterexamples to 'A_v divides F(x), and F(x) is not a power of "
          f"2' over x < {hi:,}: {bad}")
    print(f"    => never halts after its first step.\n")
    bad, vmax = t2()
    print(f"T2  machine (2,-1,2,1,1):  every branch forbidden by the WS3 sieve")
    print(f"    counterexamples to 'Q0 = 2^-1 and 2v+3 is not a power of 2 mod "
          f"2^(v+2)-1' over v < {vmax}: {bad}")
    print(f"    => never halts after its first step.\n")
    tp, fp, fn, n = t3()
    print("T3  closed form: decided at m = 3  iff  delta = 0, gamma = alpha and")
    print("    beta + epsilon = 0, all mod 3.")
    print(f"    checked against the census: {tp} predicted and decided, {fp} "
          f"predicted but not decided, {fn} decided but not predicted, over "
          f"{n:,} machines.")
    print("    Corollary: the v-linear term blocks the cheapest certificate "
          "there is.")
    print("    The Space Needle has delta = 1 and fails it in one line.\n")
    print("STATUS.  T1 is proved outright.  T2 is proved outright for the sieve's")
    print("halt condition; it inherits the WS3 sieve theorem, which is itself")
    print("proved.  Of the other five machines whose branches were all forbidden")
    print("to v = 200, THREE were closed the next day as T4, T5, T6 -- see")
    print("leads.py, which derives S_v = 2*B_v (mod A_v) for the alpha=2,")
    print("beta=-1 corner.  TWO remain unclaimed, their modulus having no")
    print("listable power-of-two set:")
    print("    (2,1,1,2,-1)   ord_{A_v}(2) = 2(v+2)")
    print("    (3,3,2,0,1)    ord_{A_v}(2) v-dependent: 4, 18, 8, 30, 12, 42")
    print()
    print("WORDING.  'Never halts from any start' would be wrong: a start that")
    print("IS a power of two halts at step 0.  The powers of two are exactly the")
    print("halting starts of these machines.")


if __name__ == "__main__":
    main()
