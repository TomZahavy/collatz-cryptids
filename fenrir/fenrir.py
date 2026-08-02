"""Fenrir (first FRACTRAN cryptid, March 2026) -- machine 7 of the collection.

SOURCE.  wiki.bbchallenge.org/wiki/Fenrir, fetched July 26, 2026.  Three size-22
FRACTRAN programs, e.g. [1/15, 27/77, 49/3, 10/49, 33/2], all equivalent to a
two-counter guarded walk.  With S(x,y) = [x,0,0,2,y]:

    [1,0,0,0,0] -> S(0,1)          (the start)
    S(0, 2y)    =  halt
    S(x, 2y)    -> S(x-1, 5y+2)
    S(x, 2y+1)  -> S(x+2, 5y)

Published trajectory: S(0,1), S(2,0), S(1,2), S(0,7), S(2,15), S(4,35), ...

ONE-LINE READING.  Writing the second counter as n:

    n odd :  n -> (5n-5)/2 = floor(5n/2) - 2,   x -> x + 2
    n even:  n -> 5n/2 + 2  = floor(5n/2) + 2,  x -> x - 1   (halt if x = 0)

so n follows a 5/2-map and x is a walk driven by n's parity stream.  That is
the Antihydra architecture with the multiplier 3/2 replaced by 5/2 and the
parity roles exchanged -- Fenrir is Antihydra's 5/2 sibling.
"""
HALT = "HALT"


def step(s):
    """One Fenrir step on S(x, n)."""
    x, n = s
    if n % 2:                                   # n = 2y+1
        return (x + 2, 5 * ((n - 1) // 2))
    if x == 0:                                  # S(0, even) is the halt
        return HALT
    return (x - 1, 5 * (n // 2) + 2)


def run(s=(0, 1), steps=20):
    out = [s]
    for _ in range(steps):
        s = step(s)
        out.append(s)
        if s == HALT:
            break
    return out


def _tests():
    # fidelity to the published trajectory
    want = [(0, 1), (2, 0), (1, 2), (0, 7), (2, 15), (4, 35)]
    got = run((0, 1), 5)
    assert got == want, got
    print(f"  reproduces the wiki trajectory {want}: OK")

    # T1 (no cycles): n is strictly increasing once n >= 2
    for n in range(2, 200000):
        nn = step((5, n))[1]
        assert nn > n, n
    print("  T1 no-cycle: n strictly increases for every n >= 2 "
          "(checked to 200000; proof in the report): OK")

    # T2 (the counting form): x_k = 3*O_k - k, O_k = #odd n_j for j < k
    x, n, odd = 0, 1, 0
    for k in range(4000):
        assert x == 3 * odd - k, (k, x, odd)
        if n % 2:
            odd += 1
        s = step((x, n))
        assert s != HALT
        x, n = s
    print("  T2 counting form x_k = 3*O_k - k verified for k < 4000: OK")
    print("all Fenrir machine tests passed")


if __name__ == "__main__":
    _tests()
