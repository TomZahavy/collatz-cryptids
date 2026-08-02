"""WS1 in any base: automatic-invariant search for branch-affine maps.

A machine qualifies when, writing x in base q as  prefix . tail, every branch
is affine in the tail:

    x  =  q^|p| * m + val(p)          (p a fixed digit prefix, read LSB-first)
    F(x) =  A_p * m + B_p

The Space Needle is q = 2 with p = 0^v 1, A = 2^{v+1}+3, B = 2^v+v; machine 3
is q = 3 with p = 0^j r, A = 3^{j+1}+1, B = r*3^j + j + c_r.  Given that table
the search is identical: exact branch pair sets by a (state x carry x state)
product, then Horn propagation over acceptance labellings, over every
canonical initially-connected DFA of a given size.

Imposing only some branches is sound for refutation, since the branch
conditions are a subset of full closure.
"""


def lsb_word(x, q):
    """Minimal base-q word of x >= 1, least significant digit first."""
    w = []
    while x:
        w.append(x % q)
        x //= q
    return w


def run(delta, s, word):
    for d in word:
        s = delta[s][d]
    return s


def icdfas(n, q):
    """Canonical initially-connected DFAs, n states, alphabet size q."""
    delta = [[0] * q for _ in range(n)]
    slots = [(s, a) for s in range(n) for a in range(q)]

    def rec(i, nxt):
        if i == len(slots):
            if nxt == n:
                yield [row[:] for row in delta]
            return
        s, a = slots[i]
        if s >= nxt:
            return
        for t in range(min(nxt + 1, n)):
            delta[s][a] = t
            yield from rec(i + 1, nxt + 1 if t == nxt else nxt)

    yield from rec(0, 1)


def branch_pairs(delta, q, prefix, A, B, allow_empty):
    """Exact {(state on x, state on F(x))} for one branch, minimal words.

    x runs over q^|prefix| * m + val(prefix) for every admissible tail m, and
    F(x) = A*m + B.  Membership is on minimal words, so the y-side tracks the
    state just after the last nonzero digit emitted.
    """
    sx0 = run(delta, 0, prefix)
    pairs = set()

    def finish(px, c, ry, rlast):
        r, rl, cc = ry, rlast, c
        while cc:
            r = delta[r][cc % q]
            if cc % q:
                rl = r
            cc //= q
        if rl is not None:
            pairs.add((px, rl))

    if allow_empty:                          # the tail may be m = 0
        finish(sx0, B, 0, None)
    start = (sx0, B, 0, None)
    seen = {start}
    stack = [start]
    while stack:
        px, c, ry, rlast = stack.pop()
        for d in range(q):
            t = A * d + c
            dig = t % q
            ry2 = delta[ry][dig]
            nxt = (delta[px][d], t // q, ry2, ry2 if dig else rlast)
            if d:                            # a minimal tail ends nonzero
                finish(nxt[0], nxt[1], nxt[2], nxt[3])
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return pairs


def refute(delta, n, q, branches, true_words, false_words):
    """True iff no acceptance labelling of this structure is a certificate."""
    false_states = {run(delta, 0, w) for w in false_words}
    forced, stack = set(), []

    def push(s):
        if s in forced:
            return False
        if s in false_states:
            return True
        forced.add(s)
        stack.append(s)
        return False

    for w in true_words:
        if push(run(delta, 0, w)):
            return True
    imp = [set() for _ in range(n)]
    for (prefix, A, B, allow_empty) in branches:
        for p, qq in branch_pairs(delta, q, prefix, A, B, allow_empty):
            imp[p].add(qq)
            if p in forced and push(qq):
                return True
        while stack:
            p = stack.pop()
            for qq in imp[p]:
                if push(qq):
                    return True
    return False


def search(q, branches, orbit, halt_values, nmax, label, nmin=1):
    import time
    tw = [lsb_word(x, q) for x in orbit]
    print(f"{label}: base {q}, {len(branches)} branch conditions, "
          f"{len(orbit)} orbit units, {len(halt_values)} halting units")
    for n in range(nmin, nmax + 1):
        fw = [lsb_word(h, q) for h in halt_values]
        t0, tried, alive = time.time(), 0, 0
        for delta in icdfas(n, q):
            tried += 1
            if not refute(delta, n, q, branches, tw, fw):
                alive += 1
        tag = "REFUTED (no certificate)" if not alive else f"{alive} SURVIVOR(S)"
        print(f"  n={n:2d}  structures={tried:>12,}  transitions={n * q:>3}  "
              f"{tag:<26} {time.time() - t0:7.1f}s")
