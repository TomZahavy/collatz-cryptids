"""Refutation witnesses: turn each impossibility into concrete integers.

A refutation found by search.py is not just a state-level contradiction.  Since
membership depends only on the state a number's minimal word reaches, a forced
chain of states can be realised by actual numbers:

    x_1 in I  (a known orbit element),
    state(F(x_1)) = state(x_2)  =>  x_2 in I  =>  F(x_2) in I,   ...
    state(F(x_r)) = state(2^m)  =>  2^m in I  --  contradiction with I cap H = 0.

Every link is checked here by running needle.step1 on the actual integer and
the DFA on the actual binary word, so a witness can be audited without trusting
any of the automaton machinery.
"""
import random
import sys

from dfa_invariant import icdfas, lsb_word, needle_branch, run, state_of
from search import orbit

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")
from needle import step1                                  # noqa: E402


def pairs_with_witness(delta, v, a, b):
    """{(p, q): k} -- as branch_pairs_min, but BFS keeps a smallest witness k."""
    sx0 = run(delta, 0, [0] * v + [1])
    start = (sx0, b, 0, None)
    seen = {start: []}                       # product state -> bits of k so far
    frontier = [start]
    out = {}
    while frontier:
        nxt_frontier = []
        for st in frontier:
            px, c, ry, rlast = st
            bits = seen[st]
            for kappa in (0, 1):
                t = a * kappa + c
                bit = t & 1
                ry2 = delta[ry][bit]
                nst = (delta[px][kappa], t >> 1, ry2, ry2 if bit else rlast)
                nbits = bits + [kappa]
                if kappa == 1:
                    r, rl, cc = nst[2], nst[3], nst[1]
                    while cc:
                        r = delta[r][cc & 1]
                        if cc & 1:
                            rl = r
                        cc >>= 1
                    key = (nst[0], rl)
                    if key not in out:
                        out[key] = sum(bit_ << i for i, bit_ in enumerate(nbits))
                if nst not in seen:
                    seen[nst] = nbits
                    nxt_frontier.append(nst)
        frontier = nxt_frontier
    return out


def find_witness(delta, n, vmax=6, orb=None, vpow=None):
    """Return a concrete chain refuting the structure, or None if it survives."""
    orb = orb or orbit(6, 60)
    vpow = vpow or list(range(2 * n + 3))
    bad = {}                                  # state -> exponent m with 2^m there
    for m in vpow:
        bad.setdefault(state_of(delta, 1 << m), m)

    wit = {}                                  # (p, q) -> (v, k)
    for v in range(vmax + 1):
        a, b = needle_branch(v)
        for (p, q), k in pairs_with_witness(delta, v, a, b).items():
            wit.setdefault((p, q), (v, k))

    parent, forced, stack = {}, {}, []
    for x in orb:                             # units: orbit elements are in I
        s = state_of(delta, x)
        if s not in forced:
            forced[s] = x
            stack.append(s)
            if s in bad:
                return {"kind": "unit-collides-with-power", "x": x,
                        "m": bad[s], "chain": []}
    chain_src = {}
    while stack:
        p = stack.pop()
        for (pp, q), (v, k) in wit.items():
            if pp != p or q in forced:
                continue
            x = (k << (v + 1)) + (1 << v)
            forced[q] = None
            chain_src[q] = (p, x)
            stack.append(q)
            if q in bad:
                # unwind to a unit
                chain, cur = [], q
                while cur in chain_src:
                    prev, xw = chain_src[cur]
                    chain.append((prev, xw, step1(xw), cur))
                    cur = prev
                chain.reverse()
                return {"kind": "forced-power", "m": bad[q], "seed": forced[cur],
                        "seed_state": cur, "chain": chain}
    return None


def audit(delta, w):
    """Re-verify a witness from scratch: needle.step1 + the DFA on integers."""
    if w["kind"] == "unit-collides-with-power":
        assert state_of(delta, w["x"]) == state_of(delta, 1 << w["m"])
        return True
    s = state_of(delta, w["seed"])
    assert s == w["seed_state"], "seed state mismatch"
    for (p, x, y, q) in w["chain"]:
        assert state_of(delta, x) == p, "witness x is not at the claimed state"
        assert step1(x) == y, "y is not F(x)"
        assert state_of(delta, y) == q, "F(x) is not at the claimed state"
        s = q
    assert state_of(delta, 1 << w["m"]) == s, "final state is not a power of 2's"
    return True


def main():
    random.seed(20260726)
    for n in (3, 4, 5, 6):
        pool = list(icdfas(n)) if n <= 5 else None
        if pool is None:                      # n=6: sample without materialising
            pool = []
            for i, d in enumerate(icdfas(n)):
                if random.random() < 0.00006:
                    pool.append(d)
                if len(pool) >= 300:
                    break
        sample = pool if len(pool) <= 300 else random.sample(pool, 300)
        lens, kinds = [], {}
        for delta in sample:
            w = find_witness(delta, n)
            assert w is not None, f"structure survived: {delta}"
            assert audit(delta, w)
            lens.append(len(w["chain"]))
            kinds[w["kind"]] = kinds.get(w["kind"], 0) + 1
        print(f"n={n}: {len(sample)} sampled structures, every one refuted with "
              f"an audited witness; chain lengths {min(lens)}-{max(lens)}, "
              f"kinds={kinds}")

    # show one full witness
    delta = [[0, 1], [1, 2], [1, 3], [1, 2]]
    w = find_witness(delta, 4)
    audit(delta, w)
    print(f"\nexample witness for delta={delta}:")
    print(f"  seed (orbit element in I): {w['seed']}  -> state {w['seed_state']}")
    for (p, x, y, q) in w["chain"]:
        print(f"  state {p}: {x} in I  =>  F({x}) = {y} in I  -> state {q}")
    print(f"  state of 2^{w['m']} = {1 << w['m']} is that same state "
          f"=> 2^{w['m']} in I, contradicting I cap H = empty")


if __name__ == "__main__":
    main()
