"""The six sibling GEO holdouts of BBf(23): ALL NEVER HALT.

THEOREM (M-SIBLINGS).  Each of the following FRACTRAN programs, started at
n = 2, never halts:

    673:  [9/35, 5/6, 8/55, 7/2, 605/7]     (431 with f0,f1 swapped)
    502:  [7/15, 9/14, 125/77, 2/5, 847/2]  (431 under pi = (2 5 7))
    623:  [9/10, 5/21, 343/55, 2/7, 605/2]  (431 under (2 7), f0,f1 swapped)
    574:  [8/15, 147/22, 35/2, 11/49, 3/7]  (own template: pair mode)
    570:  [77/30, 88/21, 9/2, 5/11, 7/3]    (own template: 455-like rotated)
    680:  [9/70, 44/15, 25/2, 7/55, 3/5]    (678 with f1,f2 swapped;
                                             own template, rotated phase)

With m431_proof.py, m455_proof.py, m678_proof.py this decides ALL NINE
rigid-orbit (GEO) machines on the refined BBf(23) holdout list.

METHOD.  Same architecture as the three primary proofs: a boundary family
B(idx) in exponent-vector space, a one-phase lemma giving the exact firing
word from B(idx) to B(idx+1) (with parity case splits where the discovery
showed them), guard + priority conditions checked at the corners of every
affine block rectangle (sound because every guard value is jointly affine
in the block index and within-run counter), an entry lemma by direct
simulation, and induction.  IMPORTANT: the three "transports" are NOT
assumed correct by symmetry -- each machine's walk is verified against its
OWN rule list and priority order (a priority swap can change the word, and
did for 574/680: their templates differ genuinely from 455/678's).

Boundaries and phase words (all verified; X := 2^i, W := 2^(i+1)-1):

  673/502/623 (431's template, axes/rules mapped):
      B_i = W on the '2'-axis image, i on the 11-axis; steps 2^(i+3)-5.
  574:  B_k = (0, 0, 2^(k-1)+k-1, 2^k-1, 0), k >= 4;  phase
      f3^(2^(k-1)-1) f4 (f0 f1)^(2^(k-1)-1) f0 f2^(2^k+1); 5*2^(k-1) steps.
      Halt criterion: v2=0 & v7=0 & (v3=0 | v5=0).
  570:  B_m = (0, 2^(m+1)+2m, 0, 0, x), x := 2^m-1, m >= 4;  phase
      f3^x f4 f1 (f0^3 f1)^q [f0^1] f1^L f2^C, split on x mod 3;
      5*2^m steps.  Halt criterion: v2=0 & v3=0 & v11=0.
  680:  B_m = (2^m, 0, 0, 0, 2^m-1), m >= 4;  phase
      f2^X f3^(X-1) f4 f1 (f0^2 f1)^P [f0^1] Q-blocks T-blocks, split on
      X mod 3 (even m: Q = f2 f0 f1; odd m: Q = f2 f1 f0); 6*2^m-3 steps.
      Halt criterion: v2=0 & v5=0.

Every machine: V0 vector==bigint (200k steps), V1 halt criterion on the
full 0..5 box, V2 entry by direct simulation, V3 block walk to idx = 2000,
V4 word-for-word vs ground truth over the small-idx phases.
"""

PRIMES = (2, 3, 5, 7, 11)


def fac(n):
    v = [0] * 5
    for k, p in enumerate(PRIMES):
        while n % p == 0:
            n //= p
            v[k] += 1
    assert n == 1, "prime outside (2,3,5,7,11)"
    return tuple(v)


class M:
    def __init__(self, fracs):
        self.fracs = fracs
        self.DELTA, self.GUARD = [], []
        for a, b in fracs:
            na, nb = fac(a), fac(b)
            self.DELTA.append(tuple(x - y for x, y in zip(na, nb)))
            self.GUARD.append(tuple((k, e) for k, e in enumerate(nb) if e))

    def enabled(self, v, j):
        return all(v[c] >= t for c, t in self.GUARD[j])

    def fire_next(self, v):
        for j in range(5):
            if self.enabled(v, j):
                return j
        return None

    def vstep(self, v):
        j = self.fire_next(v)
        if j is None:
            return None, None
        return tuple(a + d for a, d in zip(v, self.DELTA[j])), j

    def run_word(self, v, nsteps):
        word = []
        for _ in range(nsteps):
            v2, j = self.vstep(v)
            if j is None:
                return v, word + ["HALT"]
            v = v2
            word.append(j)
        return v, word

    def apply_run(self, v, rule, count):
        """count firings of rule; guard + priority at both run ends."""
        def ok(state):
            assert self.enabled(state, rule), (rule, state)
            for h in range(rule):
                assert not self.enabled(state, h), ("prio", h, rule, state)
        d = self.DELTA[rule]
        end = tuple(a + count * x for a, x in zip(v, d))
        if count > 0:
            ok(v)
            ok(tuple(a + (count - 1) * x for a, x in zip(v, d)))
            assert all(x >= 0 for x in end), (rule, end)
        return end

    def check_block(self, start_of, word, K):
        if K == 0:
            return start_of(0)
        for k in ([0] if K == 1 else [0, K - 1]):
            v = start_of(k)
            for rule, count in word:
                v = self.apply_run(v, rule, count)
            assert v == start_of(k + 1), ("block chain", k)
        if K >= 3:
            a, b, c = start_of(0), start_of(1), start_of(2)
            assert all(2 * y == x + z for x, y, z in zip(a, b, c))
        return start_of(K)

    def sim_bigint_check(self, nsteps=200000):
        n, v = 2, (1, 0, 0, 0, 0)
        for s in range(nsteps):
            for a, b in self.fracs:
                if n % b == 0:
                    n = n * a // b
                    break
            else:
                n = None
            v, j = self.vstep(v)
            assert (n is None) == (j is None), s
            if n is None:
                return
            x = 1
            for p, e in zip(PRIMES, v):
                x *= p ** e
            assert x == n, s


# ======================= 431-like: 673, 502, 623 =========================
# Abstract states live on 431's axes (a2, a3, a5, a7, a11); axmap sends
# axis t to the sibling's axis axmap[t]; rulemap sends 431's rule index to
# the sibling's.  All guard checking happens in SIBLING space with the
# sibling's own priority order.

def emb(axmap):
    def f(st):
        out = [0] * 5
        for t, x in enumerate(st):
            out[axmap[t]] = x
        return tuple(out)
    return f


def B431(i):
    return ((1 << (i + 1)) - 1, 0, 0, 0, i)


def walk_431like(mach, i, rulemap, axmap):
    E = emb(axmap)
    W, m = (1 << (i + 1)) - 1, (1 << i) - 1
    u = i + 2 * m + 1
    R = lambda r: rulemap[r]
    v = mach.apply_run(E(B431(i)), R(3), W)
    assert v == E((0, 0, 0, W, i))
    v = mach.check_block(lambda k: E((0, 2 * k, 0, W - 2 * k, i + 2 * k)),
                         [(R(4), 1), (R(1), 1)], m)
    v = mach.apply_run(v, R(4), 1)
    v = mach.apply_run(v, R(2), 1)
    assert v == E((3, 2 * m, 0, 0, u))
    if i % 2 == 0:
        q = (2 * m) // 3
        v = mach.check_block(
            lambda r: E((3, 2 * m - 3 * r, 2 * r, 0, u - r)),
            [(R(0), 3), (R(2), 1)], q)
        v = mach.apply_run(v, R(2), 2 * q)
        steps4 = 6 * q
    else:
        q = (2 * m - 2) // 3
        v = mach.check_block(
            lambda r: E((3, 2 * m - 3 * r, 2 * r, 0, u - r)),
            [(R(0), 3), (R(2), 1)], q)
        v = mach.apply_run(v, R(0), 2)
        v = mach.apply_run(v, R(2), 2 * q + 2)
        steps4 = 6 * q + 4
    assert v == E(B431(i + 1)), i
    return v, W + (2 * m + 1) + 1 + steps4


def runs_431like(i, rulemap):
    W, m = (1 << (i + 1)) - 1, (1 << i) - 1
    R = lambda r: rulemap[r]
    runs = [(R(3), W)] + [(R(4), 1), (R(1), 1)] * m + [(R(4), 1), (R(2), 1)]
    if i % 2 == 0:
        q = (2 * m) // 3
        runs += [(R(0), 3), (R(2), 1)] * q + [(R(2), 2 * q)]
    else:
        q = (2 * m - 2) // 3
        runs += [(R(0), 3), (R(2), 1)] * q + [(R(0), 2), (R(2), 2 * q + 2)]
    return [(r, c) for r, c in runs if c > 0]


# ============================== 574 ======================================
def B574(k):
    return (0, 0, (1 << (k - 1)) + k - 1, (1 << k) - 1, 0)


def walk_574(mach, k):
    s, w = (1 << (k - 1)) + k - 1, (1 << (k - 1)) - 1
    v = mach.apply_run(B574(k), 3, w)
    assert v == (0, 0, s, 1, w)
    v = mach.apply_run(v, 4, 1)
    assert v == (0, 1, s, 0, w)
    v = mach.check_block(lambda j: (2 * j, 1, s - j, 2 * j, w - j),
                         [(0, 1), (1, 1)], w)
    v = mach.apply_run(v, 0, 1)
    C = 2 * w + 3
    assert v == (C, 0, s - w - 1, 2 * w, 0)
    v = mach.apply_run(v, 2, C)
    assert v == B574(k + 1), k
    return v, 5 * (1 << (k - 1))


def runs_574(k):
    s, w = (1 << (k - 1)) + k - 1, (1 << (k - 1)) - 1
    return [(3, w), (4, 1)] + [(0, 1), (1, 1)] * w + [(0, 1), (2, 2 * w + 3)]


# ============================== 570 ======================================
def B570(m):
    return (0, (1 << (m + 1)) + 2 * m, 0, 0, (1 << m) - 1)


def walk_570(mach, m):
    x, y = (1 << m) - 1, (1 << (m + 1)) + 2 * m
    v = mach.apply_run(B570(m), 3, x)
    assert v == (0, y, x, 0, 0)
    v = mach.apply_run(v, 4, 1)
    v = mach.apply_run(v, 1, 1)
    assert v == (3, y - 2, x, 0, 1)
    rs = lambda r: (3, y - 2 - 4 * r, x - 3 * r, 2 * r, 1 + 4 * r)
    if m % 2 == 0:                     # x = 0 (mod 3)
        q = x // 3
        v = mach.check_block(rs, [(0, 3), (1, 1)], q)
        assert v == (3, y - 2 - 4 * q, 0, 2 * q, 1 + 4 * q)
        L, extra = 2 * q, 0
    else:                              # x = 1 (mod 3)
        q = (x - 1) // 3
        v = mach.check_block(rs, [(0, 3), (1, 1)], q)
        v = mach.apply_run(v, 0, 1)
        assert v == (2, y - 3 - 4 * q, 0, 2 * q + 1, 2 + 4 * q)
        L, extra = 2 * q + 1, 1
    v = mach.apply_run(v, 1, L)
    C = v[0]
    v = mach.apply_run(v, 2, C)
    assert v == B570(m + 1), m
    return v, x + 2 + 4 * q + extra + L + C


def runs_570(m):
    x = (1 << m) - 1
    runs = [(3, x), (4, 1), (1, 1)]
    if m % 2 == 0:
        q = x // 3
        runs += [(0, 3), (1, 1)] * q + [(1, 2 * q), (2, 3 + 6 * q)]
    else:
        q = (x - 1) // 3
        runs += [(0, 3), (1, 1)] * q + [(0, 1), (1, 2 * q + 1),
                                        (2, 6 * q + 5)]
    return runs


# ============================== 680 ======================================
def B680(m):
    return (1 << m, 0, 0, 0, (1 << m) - 1)


def walk_680(mach, m):
    X = 1 << m
    v = mach.apply_run(B680(m), 2, X)
    assert v == (0, 0, 2 * X, 0, X - 1)
    v = mach.apply_run(v, 3, X - 1)
    assert v == (0, 0, X + 1, X - 1, 0)
    v = mach.apply_run(v, 4, 1)
    v = mach.apply_run(v, 1, 1)
    assert v == (2, 0, X - 1, X - 1, 1)
    rs = lambda r: (2, 3 * r, X - 1 - 3 * r, X - 1 - 2 * r, 1 + r)
    if m % 2 == 0:                     # X - 1 = 0 (mod 3)
        P = (X - 1) // 3
        v = mach.check_block(rs, [(0, 2), (1, 1)], P)
        assert v == (2, 3 * P, 0, X - 1 - 2 * P, 1 + P)
        Q = X - 1 - 2 * P
        v = mach.check_block(
            lambda j: (2, 3 * P + j, 0, X - 1 - 2 * P - j, 1 + P + j),
            [(2, 1), (0, 1), (1, 1)], Q)
        y0, extra = 3 * P + Q, 0
        v0, x0 = 2, 1 + P + Q
    else:                              # X - 1 = 1 (mod 3)
        P = (X - 2) // 3
        v = mach.check_block(rs, [(0, 2), (1, 1)], P)
        v = mach.apply_run(v, 0, 1)
        assert v == (1, 3 * P + 2, 0, X - 2 - 2 * P, 1 + P)
        Q = X - 2 - 2 * P
        v = mach.check_block(
            lambda j: (1, 3 * P + 2 + j, 0, X - 2 - 2 * P - j, 1 + P + j),
            [(2, 1), (1, 1), (0, 1)], Q)
        y0, extra = 3 * P + 2 + Q, 1
        v0, x0 = 1, 1 + P + Q
    T = y0 // 2
    assert y0 == 2 * T
    v = mach.check_block(
        lambda t: (v0 + 3 * t, y0 - 2 * t, 0, 0, x0 + 2 * t),
        [(2, 1), (1, 2)], T)
    assert v == B680(m + 1), m
    return v, X + (X - 1) + 2 + 3 * P + extra + 3 * Q + 3 * T


def runs_680(m):
    X = 1 << m
    runs = [(2, X), (3, X - 1), (4, 1), (1, 1)]
    if m % 2 == 0:
        P = (X - 1) // 3
        Q = X - 1 - 2 * P
        runs += [(0, 2), (1, 1)] * P + [(2, 1), (0, 1), (1, 1)] * Q
        T = (3 * P + Q) // 2
    else:
        P = (X - 2) // 3
        Q = X - 2 - 2 * P
        runs += [(0, 2), (1, 1)] * P + [(0, 1)]
        runs += [(2, 1), (1, 1), (0, 1)] * Q
        T = (3 * P + 2 + Q) // 2
    runs += [(2, 1), (1, 2)] * T
    return runs


# ============================== specs ====================================
SPECS = {
    673: dict(fr=[(9, 35), (5, 6), (8, 55), (7, 2), (605, 7)],
              halt=lambda v: v[0] == 0 and v[3] == 0 and
              (v[2] == 0 or v[4] == 0),
              entry=(3, 1), i_hi=2000, small_hi=12,
              B=lambda i: emb((0, 1, 2, 3, 4))(B431(i)),
              walk=lambda M_, i: walk_431like(
                  M_, i, {0: 1, 1: 0, 2: 2, 3: 3, 4: 4}, (0, 1, 2, 3, 4)),
              runs=lambda i: runs_431like(i, {0: 1, 1: 0, 2: 2, 3: 3, 4: 4}),
              steps=lambda i: (1 << (i + 3)) - 5),
    502: dict(fr=[(7, 15), (9, 14), (125, 77), (2, 5), (847, 2)],
              halt=lambda v: v[2] == 0 and v[0] == 0 and
              (v[3] == 0 or v[4] == 0),
              entry=(2, 1), i_hi=2000, small_hi=12,
              B=lambda i: emb((2, 1, 3, 0, 4))(B431(i)),
              walk=lambda M_, i: walk_431like(
                  M_, i, {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}, (2, 1, 3, 0, 4)),
              runs=lambda i: runs_431like(i, {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}),
              steps=lambda i: (1 << (i + 3)) - 5),
    623: dict(fr=[(9, 10), (5, 21), (343, 55), (2, 7), (605, 2)],
              halt=lambda v: v[3] == 0 and v[0] == 0 and
              (v[2] == 0 or v[4] == 0),
              entry=(2, 1), i_hi=2000, small_hi=12,
              B=lambda i: emb((3, 1, 2, 0, 4))(B431(i)),
              walk=lambda M_, i: walk_431like(
                  M_, i, {0: 1, 1: 0, 2: 2, 3: 3, 4: 4}, (3, 1, 2, 0, 4)),
              runs=lambda i: runs_431like(i, {0: 1, 1: 0, 2: 2, 3: 3, 4: 4}),
              steps=lambda i: (1 << (i + 3)) - 5),
    574: dict(fr=[(8, 15), (147, 22), (35, 2), (11, 49), (3, 7)],
              halt=lambda v: v[0] == 0 and v[3] == 0 and
              (v[1] == 0 or v[2] == 0),
              entry=(36, 4), i_hi=2000, small_hi=14,
              B=B574, walk=walk_574, runs=runs_574,
              steps=lambda k: 5 * (1 << (k - 1))),
    570: dict(fr=[(77, 30), (88, 21), (9, 2), (5, 11), (7, 3)],
              halt=lambda v: v[0] == 0 and v[1] == 0 and v[4] == 0,
              entry=(76, 4), i_hi=2000, small_hi=13,
              B=B570, walk=walk_570, runs=runs_570,
              steps=lambda m: 5 * (1 << m)),
    680: dict(fr=[(9, 70), (44, 15), (25, 2), (7, 55), (3, 5)],
              halt=lambda v: v[0] == 0 and v[2] == 0,
              entry=(78, 4), i_hi=2000, small_hi=13,
              B=B680, walk=walk_680, runs=runs_680,
              steps=lambda m: 6 * (1 << m) - 3),
}


if __name__ == "__main__":
    import itertools
    import time
    for mid, sp in SPECS.items():
        t0 = time.time()
        mach = M(sp["fr"])
        print("=" * 74, flush=True)
        print(f"MACHINE {mid} = {sp['fr']}", flush=True)

        mach.sim_bigint_check()
        print("  V0  vector == big-int FRACTRAN, 200,000 steps: OK",
              flush=True)

        bad = sum((mach.fire_next(v) is None) != bool(sp["halt"](v))
                  for v in itertools.product(range(6), repeat=5))
        assert bad == 0
        print("  V1  halt criterion exact on the full 0..5 box: OK",
              flush=True)

        E, i0 = sp["entry"]
        v, word = mach.run_word((1, 0, 0, 0, 0), E)
        assert "HALT" not in word and v == sp["B"](i0), (mid, v)
        print(f"  V2  entry: n=2 reaches B({i0}) at step {E}: OK", flush=True)

        for i in range(i0, sp["i_hi"] + 1):
            v, steps = sp["walk"](mach, i)
            assert v == sp["B"](i + 1), (mid, i)
            assert steps == sp["steps"](i), (mid, i)
        print(f"  V3  block walk idx = {i0}..{sp['i_hi']}: corner checks, "
              f"exact landings, exact step counts: OK", flush=True)

        v = sp["B"](i0)
        for i in range(i0, sp["small_hi"] + 1):
            pred = []
            for rule, count in sp["runs"](i):
                pred += [rule] * count
            v_end, got = mach.run_word(v, len(pred))
            assert got == pred, (mid, i, "word mismatch")
            assert v_end == sp["B"](i + 1), (mid, i)
            v = v_end
        print(f"  V4  firing word == ground truth, phases {i0}.."
              f"{sp['small_hi']}: OK", flush=True)
        print(f"  THEOREM M{mid}: never halts from n = 2.  "
              f"[{time.time()-t0:.1f}s]", flush=True)
