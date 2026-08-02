"""Does the encoding ADMIT a certificate of size k?  Answered directly.

The impossibility theorems all rest on completed UNSAT runs.  A completed UNSAT
cannot be undermined by solver slowness -- it is a complete refutation.  The
failure mode that WOULD hollow them out is an encoding that is accidentally
over-constrained, so that machines which do have certificates are also reported
UNSAT.  calibrate.py probes that by asking the solver to find planted
certificates, but the SAT side of a search space this size is far slower than
the UNSAT side, so the probe stalls exactly where it matters (n >= 11).

This settles the same question without any search: take the planted certificate,
build the full variable assignment it induces (transitions, acceptance, and the
true product reachability), and check every clause of the formula.  If every
clause holds, the encoding admits that certificate -- so an UNSAT verdict at
that size is a real theorem about the machine and not an artefact.

Usage:  python3 adequacy.py
"""
import sys

from calibrate import machine, step                         # noqa: E402
from msb_search import MsbEncoder, msb_word, const_and_bound  # noqa: E402


def canonicalize(delta, acc):
    """Relabel into the BFS-canonical numbering the symmetry breaking demands.

    Slots are visited in the order (0,0), (0,1), (1,0), ...; a state is given
    the next index at its first appearance.  This is the ICDFA canonical form,
    so the canonical copy is the one the formula keeps.
    """
    n = len(delta)
    order, seen = [0], {0: 0}
    i = 0
    while i < len(order):
        s = order[i]
        for d in (0, 1):
            t = delta[s][d]
            if t not in seen:
                seen[t] = len(order)
                order.append(t)
        i += 1
    assert len(order) == n, "planted DFA is not initially connected"
    new = [[seen[delta[order[i]][d]] for d in (0, 1)] for i in range(n)]
    return new, sorted(seen[s] for s in acc)


def residue_certificate(m):
    """Multiples of m, MSB-first: delta(r, d) = 2r + d mod m, accept r = 0."""
    return [[(2 * r + d) % m for d in (0, 1)] for r in range(m)], [0]


def product_reach(delta, v, a, b):
    """The TRUE reachable product states for this delta -- the values the R
    variables must take."""
    C, M = const_and_bound(v, a, b)
    mask = (1 << (v + 1)) - 1
    start = (0, 0, 0, 0)
    seen, stack = {start}, [start]
    while stack:
        px, py, r, sh = stack.pop()
        for d in (0, 1):
            for e in (0, 1):
                r2 = 2 * r + (1 << (v + 1)) * e - a * d
                if abs(r2) > M:
                    continue
                nxt = (delta[px][d], delta[py][e], r2, ((sh << 1) | d) & mask)
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    return seen


def assignment_satisfies(n, vmax, branches, orb, delta, acc):
    """Check the planted assignment against the formula, clause family by
    clause family, without materialising the CNF (which is |shape| * 4n^4
    clauses and blows up for the larger planted machines).

    The formula has exactly five families, and the planted assignment
    T[s][d][delta[s][d]] = 1, A[s] = [s in acc], R = the true product reach
    satisfies them iff:

      transitions (exactly-one)  -- by construction, delta is a function;
      symmetry breaking          -- iff delta is in BFS-canonical form;
      orbit units                -- iff every orbit element lands in acc;
      halt units                 -- iff no power of 2 lands in acc;
      product closure + emission -- the closure clauses hold because R is the
                                    true reach (closed by definition), and the
                                    emission clauses hold iff every emitted
                                    pair (px, py) with px in acc has py in acc.

    So checking those four semantic conditions is equivalent, and cheap.
    """
    def state(x):
        s = 0
        for d in msb_word(x):
            s = delta[s][d]
        return s

    fails = []
    if canonicalize(delta, acc)[0] != delta:
        fails.append("not BFS-canonical")
    for x in orb:
        if state(x) not in acc:
            fails.append(f"orbit element {x} rejected")
    for e in range(2 * n + 6):
        if state(1 << e) in acc:
            fails.append(f"halt value 2^{e} accepted")
    npairs = 0
    for v in range(vmax + 1):
        a, b = branches(v)
        C, _ = const_and_bound(v, a, b)
        for (px, py, r, sh) in product_reach(delta, v, a, b):
            if r == C and sh == (1 << v):
                npairs += 1
                if px in acc and py not in acc:
                    fails.append(f"branch {v}: emitted pair ({px},{py}) "
                                 f"breaks closure")
    return npairs, fails[:5]


def lsb_residue_certificate(m):
    """Multiples of m read LSB-first: state (r, p) with r = value so far mod m
    and p = 2^len mod m; accept r = 0."""
    start = (0, 1 % m)
    idx, stack = {start: 0}, [start]
    while stack:
        r, p = stack.pop()
        for d in (0, 1):
            nxt = ((r + d * p) % m, (2 * p) % m)
            if nxt not in idx:
                idx[nxt] = len(idx)
                stack.append(nxt)
    delta = [[0, 0] for _ in idx]
    for (r, p), i in idx.items():
        for d in (0, 1):
            delta[i][d] = idx[((r + d * p) % m, (2 * p) % m)]
    acc = [i for (r, _p), i in idx.items() if r == 0]
    return minimize(delta, acc)


def minimize(delta, acc):
    """Moore refinement, returning the quotient automaton.  The adequacy claim
    has to be about a certificate of the MINIMAL size k, not about the
    unminimised construction (which is ~k^2 states and would prove far less)."""
    accs = set(acc)
    part = [0 if i in accs else 1 for i in range(len(delta))]
    while True:
        sig, new = {}, []
        for i in range(len(delta)):
            key = (part[i], part[delta[i][0]], part[delta[i][1]])
            new.append(sig.setdefault(key, len(sig)))
        if len(set(new)) == len(set(part)):
            break
        part = new
    # relabel so the start block is 0
    order, seen = [part[0]], {part[0]: 0}
    i = 0
    while i < len(order):
        blk = order[i]
        rep = next(j for j in range(len(delta)) if part[j] == blk)
        for d in (0, 1):
            nb = part[delta[rep][d]]
            if nb not in seen:
                seen[nb] = len(order)
                order.append(nb)
        i += 1
    n = len(order)
    nd = [[0, 0] for _ in range(n)]
    for blk, i in seen.items():
        rep = next(j for j in range(len(delta)) if part[j] == blk)
        for d in (0, 1):
            nd[i][d] = seen[part[delta[rep][d]]]
    na = sorted({seen[part[j]] for j in accs})
    return nd, na


def check_lsb(m, vmax=1):
    """Same question for the LSB encoding, where the headline theorems live.

    The minimal-word convention's exact pair set is dfa_invariant's
    branch_pairs_min, the same routine the exhaustive search used; the planted
    assignment satisfies the formula iff the orbit is accepted, no power of 2
    is, and every emitted pair preserves acceptance.
    """
    from dfa_invariant import branch_pairs_min, lsb_word as lsb, run
    brs = machine(m, vmax)
    delta, acc = lsb_residue_certificate(m)
    accs = set(acc)
    fails, npairs = [], 0
    orb, x = [], m
    for _ in range(40):
        orb.append(x)
        x = step(m, x)
    for o in orb:
        if run(delta, 0, lsb(o)) not in accs:
            fails.append(f"orbit element {o} rejected")
    for e in range(2 * m + 8):
        if run(delta, 0, lsb(1 << e)) in accs:
            fails.append(f"halt value 2^{e} accepted")
    for v in range(vmax + 1):
        for (p, q) in branch_pairs_min(delta, v, brs[v][1], brs[v][2]):
            npairs += 1
            if p in accs and q not in accs:
                fails.append(f"branch {v}: pair ({p},{q}) breaks closure")
    return len(delta), npairs, fails[:5]


def main():
    vmax = 1
    print("Encoding adequacy: does the formula ADMIT the planted certificate "
          "at each size?")
    print("(checked by construction, not by search -- no solver involved)")
    print()
    print("LSB-first, minimal-word convention (the >= 10-state theorem):")
    for m in (3, 5, 7, 11, 13, 17, 19, 23):
        n, npairs, bad = check_lsb(m)
        print(f"  k={m:>3}:  DFA {n:>3} states, {npairs:>5,} emitted pairs   "
              f"{'SATISFIED' if not bad else '*** VIOLATED ***'}")
        if bad:
            print(f"          {bad}")
    print()
    print("MSB-first, leading-zero-invariant convention:")
    for m in (3, 5, 7, 11, 13, 17, 19, 23):
        brs = machine(m, vmax)
        table = {v: (brs[v][1], brs[v][2]) for v in range(vmax + 1)}
        orb, x = [], m
        for _ in range(40):
            orb.append(x)
            x = step(m, x)
        delta, acc = canonicalize(*residue_certificate(m))
        npairs, bad = assignment_satisfies(m, vmax, lambda v: table[v], orb,
                                           delta, acc)
        print(f"  k={m:>3}:  {npairs:>6,} emitted closure pairs   "
              f"{'SATISFIED -- the encoding admits this certificate' if not bad else '*** VIOLATED ***'}")
        if bad:
            print(f"          {bad}")
            sys.exit(1)


if __name__ == "__main__":
    main()
