"""WS1: automatic (base-2 regular) non-halting invariants for valuation-branched maps.

CERTIFICATE SOUGHT.  For a map F on the positive integers with halting set H,
a set I is a *non-halting certificate* for the start x0 when

    x0 in I,      F(I \\ H) subset of I,      I cap H = empty.

If such an I exists the orbit of x0 never halts.  We ask for I to be
2-automatic: recognised by a DFA reading the binary expansion of x
least-significant-bit first.  Then the certificate is finite and checkable.

WHY THIS IS DECIDABLE PER BRANCH.  Write x = 2^v * (2k+1), v = v_2(x), so the
LSB-first word of x is  0^v 1 w(k).  For the Space Needle
(needle.step1, x -> x + v + 3(m-1)/2) the identity

    F(x) = x + 3*(x >> (v+1)) + v = (2^{v+1} + 3) k + (2^v + v)          (*)

(machine-verified against needle.step1) makes every valuation branch an AFFINE
map k -> a_v k + b_v.  The set of state pairs (state on x, state on F(x)) that
a fixed DFA can exhibit inside branch v is therefore computed exactly by a
product automaton: DFA-state on x, times the carry of the multiply-add, times
DFA-state on y.  Carries are bounded by max(a_v, b_v), so the product is finite.

THE SEARCH.  Fix a transition structure delta (states, no acceptance yet).
Every branch pair (p, q) is an implication  acc(p) => acc(q).  Trailing-zero
invariance (a number-language must satisfy acc(p) = acc(delta(p,0))) adds
implications both ways.  Orbit elements are units acc = TRUE; elements of H are
units acc = FALSE.  This is a Horn system: propagate TRUE forward from the
units; the structure admits a certificate iff no FALSE unit is forced.  That
decision is exact for the branches used, so using only branches v <= V gives a
sound NECESSARY condition -- failure at every structure of size <= n is a
theorem ("no 2-automatic invariant with <= n states"), while a survivor is a
candidate to be checked on all branches.

Enumeration of structures is over canonical initially-connected DFAs (BFS
numbering), which visits each isomorphism class exactly once.
"""
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
from needle import step1, is_pow2, v2, HALT          # noqa: E402


# ---------------------------------------------------------------- words -----
def lsb_word(x):
    """Binary word of x >= 1, least-significant bit first, minimal (ends in 1)."""
    assert x >= 1
    w = []
    while x:
        w.append(x & 1)
        x >>= 1
    return w


def value(word):
    return sum(b << i for i, b in enumerate(word))


def run(delta, s, word):
    for b in word:
        s = delta[s][b]
    return s


def state_of(delta, x):
    return run(delta, 0, lsb_word(x))


# --------------------------------------------------------------- branches ---
def needle_branch(v):
    """(a, b) with F(x) = a*k + b on the branch v_2(x) = v, x = 2^{v+1} k + 2^v."""
    return (1 << (v + 1)) + 3, (1 << v) + v


def times4_branch(v):
    """Calibration map C(x) = 4x, written in the same branch form."""
    return 1 << (v + 3), 1 << (v + 2)


# ------------------------------------------------- exact per-branch pairs ---
def branch_pairs(delta, v, a, b):
    """All pairs (state(x), state(y-word)) over x with v_2(x) = v, x not in H.

    x = 2^{v+1} k + 2^v with k >= 1; y = a k + b emitted LSB-first with carry.
    Returns a set of (p, q).  Exact (no approximation) for this branch.
    """
    sx0 = run(delta, 0, [0] * v + [1])            # state after the 0^v 1 prefix
    start = (sx0, b, 0)                           # (x-state, carry, y-state)
    seen = {start}
    stack = [start]
    pairs = set()
    while stack:
        px, c, ry = stack.pop()
        for kappa in (0, 1):
            t = a * kappa + c
            nxt = (delta[px][kappa], t >> 1, delta[ry][t & 1])
            if kappa == 1:                        # a minimal word for k ends in 1
                pairs.add((nxt[0], flush(delta, nxt[2], nxt[1])))
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return pairs


def flush(delta, r, c):
    """Emit the remaining carry, LSB-first, through the DFA."""
    while c:
        r = delta[r][c & 1]
        c >>= 1
    return r


def branch_pairs_min(delta, v, a, b):
    """As branch_pairs, but membership is decided on MINIMAL words only.

    A 2-automatic set need not be given by a trailing-zero-invariant DFA: it
    suffices that the minimal (no trailing zeros) words of its members are
    accepted.  That convention is strictly more general -- it admits automata
    the invariant one cannot express at the same size -- so the impossibility
    theorem must be proved against it.  The emitted word for y may carry
    trailing zeros, so the product also tracks the y-state immediately after
    the most recent emitted 1; that is the state at the end of y's minimal
    word.  (y >= 1 always, so some 1 is emitted.)
    """
    sx0 = run(delta, 0, [0] * v + [1])
    start = (sx0, b, 0, None)                 # (x-state, carry, y-state, y-last)
    seen = {start}
    stack = [start]
    pairs = set()
    while stack:
        px, c, ry, rlast = stack.pop()
        for kappa in (0, 1):
            t = a * kappa + c
            bit = t & 1
            ry2 = delta[ry][bit]
            nxt = (delta[px][kappa], t >> 1, ry2, ry2 if bit else rlast)
            if kappa == 1:                    # k's minimal word ends in 1
                r, rl, cc = nxt[2], nxt[3], nxt[1]
                while cc:                     # flush the carry, tracking last 1
                    r = delta[r][cc & 1]
                    if cc & 1:
                        rl = r
                    cc >>= 1
                assert rl is not None
                pairs.add((nxt[0], rl))
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return pairs


def min_reference(delta, v, a, b, k):
    """Reference: (state on min word of x, state on min word of y)."""
    x = (k << (v + 1)) + (1 << v)
    y = a * k + b
    return run(delta, 0, lsb_word(x)), run(delta, 0, lsb_word(y))


def emit_reference(delta, v, a, b, k):
    """Reference simulation of one (v, k): returns (x, y, x-state, y-state)."""
    x = (k << (v + 1)) + (1 << v)
    px, c, ry, out = run(delta, 0, [0] * v + [1]), b, 0, []
    for kappa in lsb_word(k):
        t = a * kappa + c
        out.append(t & 1)
        px, ry, c = delta[px][kappa], delta[ry][t & 1], t >> 1
    while c:
        out.append(c & 1)
        ry = delta[ry][c & 1]
        c >>= 1
    return x, value(out), px, ry


# --------------------------------------------------- Horn feasibility test ---
def implications(delta, n, branches, vmax):
    """Implication multimap acc(p) => acc(q): branch pairs + 0-invariance."""
    imp = [set() for _ in range(n)]
    for v in range(vmax + 1):
        a, b = branches(v)
        for p, q in branch_pairs(delta, v, a, b):
            imp[p].add(q)
    for p in range(n):                            # acc(p) <=> acc(delta(p,0))
        z = delta[p][0]
        imp[p].add(z)
        imp[z].add(p)
    return imp


def feasible(delta, n, branches, vmax, units_true, units_false):
    """Horn propagation. Returns the forced-TRUE set, or None if infeasible."""
    imp = implications(delta, n, branches, vmax)
    forced = set(units_true)
    stack = list(forced)
    while stack:
        p = stack.pop()
        for q in imp[p]:
            if q not in forced:
                forced.add(q)
                stack.append(q)
    if forced & units_false:
        return None
    return forced


# ------------------------------------------------------------ enumeration ---
def icdfas(n):
    """Canonical initially-connected DFAs on n states over {0,1} (BFS numbering).

    Each isomorphism class of initially-connected DFA transition structures is
    generated exactly once: transitions are assigned in the order (0,0), (0,1),
    (1,0), ..., and a target may be a fresh state only if it is the next unused
    index.  All n states must be used.
    """
    delta = [[0, 0] for _ in range(n)]
    slots = [(s, a) for s in range(n) for a in (0, 1)]

    def rec(i, nxt):
        if i == len(slots):
            if nxt == n:
                yield [row[:] for row in delta]
            return
        s, a = slots[i]
        if s >= nxt:                              # state s not discovered yet
            return
        for t in range(min(nxt + 1, n)):
            delta[s][a] = t
            yield from rec(i + 1, nxt + 1 if t == nxt else nxt)

    yield from rec(0, 1)


# ------------------------------------------------------------------ tests ---
def _tests():
    # (1) the branch form reproduces the Needle map exactly
    for x in range(2, 20000):
        if is_pow2(x):
            continue
        v, _ = v2(x)
        a, b = needle_branch(v)
        assert a * (x >> (v + 1)) + b == step1(x), x
    print("  branch form (a_v k + b_v) == needle.step1 for x < 20000: OK")

    # (2) emitted word equals y, for many (v, k), and the pair is in branch_pairs
    d = [[1, 2], [2, 0], [0, 1]]                  # an arbitrary 3-state structure
    for v in range(0, 7):
        a, b = needle_branch(v)
        P = branch_pairs(d, v, a, b)
        for k in range(1, 400):
            x, y, px, ry = emit_reference(d, v, a, b, k)
            assert v2(x)[0] == v and step1(x) == y, (v, k, x, y)
            assert (px, ry) in P, (v, k)
    print("  branch_pairs: emitted word == F(x) and all (v,k<400, v<=6) pairs "
          "present: OK")

    # (3) branch_pairs is not over-approximating: every pair is realised
    for v in range(0, 5):
        a, b = needle_branch(v)
        P = branch_pairs(d, v, a, b)
        got = set()
        for k in range(1, 20000):
            _, _, px, ry = emit_reference(d, v, a, b, k)
            got.add((px, ry))
        assert got <= P and P <= got, (v, P - got, got - P)
    print("  branch_pairs exact (== realised pairs, k < 20000, v <= 4): OK")

    # (3b) branch_pairs_min is exact for the minimal-word convention
    for d2 in ([[1, 2], [2, 0], [0, 1]], [[0, 1], [2, 1], [1, 0]],
               [[1, 1], [2, 0], [0, 2]]):
        for v in range(0, 5):
            a, b = needle_branch(v)
            P = branch_pairs_min(d2, v, a, b)
            got = {min_reference(d2, v, a, b, k) for k in range(1, 20000)}
            assert got <= P, (v, got - P)
            assert P <= got, (v, P - got)
    print("  branch_pairs_min exact (minimal-word convention, 3 structures, "
          "k < 20000, v <= 4): OK")

    # (4) canonical enumeration counts match the known ICDFA sequence
    counts = [len(list(icdfas(n))) for n in range(1, 6)]
    assert counts == [1, 12, 216, 5248, 160675], counts
    print(f"  ICDFA enumeration counts {counts} match the known "
          "initially-connected-DFA counts for a 2-letter alphabet: OK")
    print("all machinery tests passed")


if __name__ == "__main__":
    _tests()
