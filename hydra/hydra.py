"""The Hydra function family — exact implementations.

The value map (pure form):    H(n) = 3*floor(n/2) + (n mod 2) = floor(3n/2)
  - H(2m)   = 3m      (even branch)
  - H(2m+1) = 3m+1    (odd branch)

HYDRA (BB(2,5), Daniel Yuan 2024): start n = 3.  Counter b, b0 = 0:
  odd n:  b += 2;  even n: if b == 0 -> HALT else b -= 1.
  (Halts iff at some point #even terms exceed 2 * #odd terms.)
  TM form C(N, b): N -> (3N+6)/2 (N even), (3N+3)/2 (N odd), start C(3, 0).
  Conjugacy: N_t = 3*n_t - 6 with n the pure orbit from 3 (verified below).

ANTIHYDRA (BB(6), mxdys 2024): start n = 8.  Counter a, a0 = 0:
  even n: a += 2;  odd n: if a == 0 -> HALT else a -= 1.
  (Halts iff at some point #odd terms exceed 2 * #even terms.)
  TM form A(a, b): b_t = n_t - 4 (verified below against the wiki trajectory).

FENRIR (FRACTRAN-22, Yuen 2026): S(x, y), start S(0, 1):
  y even: if x == 0 -> HALT else x -= 1, y -> 5*(y//2) + 2
  y odd :  x += 2,               y -> 5*(y//2)
  Same skeleton with q = 5: value ~ *5/2, counter walks +2/-1.

Sources: wiki.bbchallenge.org pages Hydra, Antihydra, Hydra_function,
Fenrir (accessed July 2026); the Coq-BB5 paper's Antihydra wording.
"""

HALT = "HALT"


def Hstep(n):
    """The pure Hydra function."""
    return 3 * (n // 2) + (n & 1)


def hydra_step(n, b):
    if n & 1:
        return Hstep(n), b + 2
    if b == 0:
        return HALT
    return Hstep(n), b - 1


def antihydra_step(n, a):
    if n & 1:
        if a == 0:
            return HALT
        return Hstep(n), a - 1
    return Hstep(n), a + 2


def fenrir_step(x, y):
    if y & 1:
        return x + 2, 5 * (y // 2)
    if x == 0:
        return HALT
    return x - 1, 5 * (y // 2) + 2


def run(step, s, t):
    """t steps (or until HALT); returns final state or HALT."""
    for _ in range(t):
        s = step(*s)
        if s == HALT:
            return HALT
    return s


if __name__ == "__main__":
    # ---- wiki trajectory checks -------------------------------------
    # Antihydra page: blank tape -> A(0,4); trajectory of (a, b):
    want = [(0, 4), (2, 8), (4, 14), (6, 23), (5, 36), (7, 56), (9, 86)]
    n, a = 8, 0
    got = []
    for _ in want:
        got.append((a, n - 4))
        r = antihydra_step(n, a)
        n, a = r
    assert got == want, got
    print("Antihydra: wiki trajectory A(0,4)...A(9,86) reproduced (b = n - 4)")

    # Hydra page: C(3,0) -> C(6,2) -> C(12,1) -> C(21,0) -> C(33,2)
    #             -> C(51,4) -> C(78,6);  TM form N = 3n - 6.
    wantH = [(3, 0), (6, 2), (12, 1), (21, 0), (33, 2), (51, 4), (78, 6)]
    n, b = 3, 0
    gotH = []
    for _ in wantH:
        gotH.append((3 * n - 6, b))
        r = hydra_step(n, b)
        n, b = r
    assert gotH == wantH, gotH
    print("Hydra: wiki trajectory C(3,0)...C(78,6) reproduced (N = 3n - 6)")

    # TM-form step (3N+6)/2 or (3N+3)/2 agrees with the conjugacy
    N, n = 3, 3
    for _ in range(2000):
        N = (3 * N + 6) // 2 if N % 2 == 0 else (3 * N + 3) // 2
        n = Hstep(n)
        assert N == 3 * n - 6
    print("Hydra: conjugacy N = 3n - 6 verified for 2,000 steps")

    # Fenrir page trajectory: S(0,1) S(2,0) S(1,2) S(0,7) S(2,15) S(4,35)
    wantF = [(0, 1), (2, 0), (1, 2), (0, 7), (2, 15), (4, 35)]
    s = (0, 1)
    gotF = [s]
    for _ in range(5):
        s = fenrir_step(*s)
        gotF.append(s)
    assert gotF == wantF, gotF
    print("Fenrir: wiki trajectory S(0,1)...S(4,35) reproduced")
