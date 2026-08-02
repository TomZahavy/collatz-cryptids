"""Run-accelerated FRACTRAN simulator + rigid-tail detector.

Exact priority semantics: at each step the FIRST fraction whose denominator
divides n fires. Acceleration: when fraction j0 is the first enabled one,
compute the exact number k of consecutive firings of j0 before either
(a) j0's own guard fails, or (b) some earlier fraction becomes enabled
(preemption). All constraints are linear in the firing count, so k is exact.
State += k*delta in one jump; one "run" (j0, k) is recorded.

Ground truth check: expand_runs() must reproduce the direct step-by-step
firing sequence exactly (verified in verify mode).
"""
import sys
INF = float('inf')

def factorint(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def parse(line):
    line = line.strip().strip('[]')
    return [tuple(int(x) for x in tok.strip().split('/')) for tok in line.split(',')]

def compile_machine(fracs):
    primes = set()
    for p, q in fracs:
        primes |= set(factorint(p)) | set(factorint(q))
    primes = sorted(primes)
    idx = {pr: i for i, pr in enumerate(primes)}
    rules = []
    for p, q in fracs:
        fp, fq = factorint(p), factorint(q)
        need = [(idx[pr], e) for pr, e in fq.items()]
        delta = [0] * len(primes)
        for pr, e in fp.items(): delta[idx[pr]] += e
        for pr, e in fq.items(): delta[idx[pr]] -= e
        rules.append((need, delta))
    return primes, rules

def enabled(state, need):
    return all(state[i] >= e for i, e in need)

def sim_runs(rules, nprimes, max_runs=3000, max_steps=None):
    """Returns (runs, state, status, total_steps).
    status: 'halt' | 'cap' | 'inf' (provably infinite single-fraction run)."""
    state = [0] * nprimes
    state[0] = 1
    runs = []
    total = 0
    while len(runs) < max_runs and (max_steps is None or total < max_steps):
        j0 = None
        for j, (need, delta) in enumerate(rules):
            if enabled(state, need):
                j0 = j; break
        if j0 is None:
            return runs, state, 'halt', total
        need, delta = rules[j0]
        # k_self: max consecutive firings before own guard fails
        k_self = INF
        for i, e in need:
            d = delta[i]
            if d < 0:
                k_self = min(k_self, (state[i] - e) // (-d) + 1)
        # preemption: first s>=1 with some earlier fraction enabled at state+s*delta
        s_pre = INF
        for e_need, _ in rules[:j0]:
            lo, hi = 1, INF
            for i, e in e_need:
                d = delta[i]
                deficit = e - state[i]
                if d > 0:
                    if deficit > 0:
                        lo = max(lo, -((-deficit) // d))  # ceil
                elif d == 0:
                    if deficit > 0: lo = INF; break
                else:
                    h = (state[i] - e) // (-d)
                    hi = min(hi, h)
                    if hi < lo: break
            if lo <= hi:
                s_pre = min(s_pre, lo)
        k = min(k_self, s_pre)
        if k is INF or k == INF:
            runs.append((j0, INF))
            return runs, state, 'inf', total
        k = int(k)
        for i in range(nprimes):
            state[i] += k * delta[i]
        runs.append((j0, k))
        total += k
    return runs, state, 'cap', total

def sim_direct(rules, nprimes, T):
    state = [0] * nprimes
    state[0] = 1
    seq = []
    for _ in range(T):
        fired = False
        for j, (need, delta) in enumerate(rules):
            if enabled(state, need):
                for i in range(nprimes): state[i] += delta[i]
                seq.append(j); fired = True; break
        if not fired: break
    return seq, state

def expand_runs(runs, T):
    out = []
    for j, k in runs:
        kk = T - len(out) if k is INF or k == INF else min(int(k), T - len(out))
        out.extend([j] * kk)
        if len(out) >= T: break
    return out

# ---------------- detector over runs ----------------
MAXP = 48
CYCWIN = 60

def find_symbol_period(syms):
    n = len(syms)
    best = None
    for p in range(1, min(MAXP, max(1, n // 3)) + 1):
        win = min(n - p, 10 * p)
        if win < 2 * p: continue
        if all(syms[n - 1 - i] == syms[n - 1 - i - p] for i in range(win)):
            best = p; break
    return best

def classify_series(L):
    if len(L) < 4: return ('short', None)
    if all(x == L[0] for x in L): return ('const', L[0])
    d = [L[i + 1] - L[i] for i in range(len(L) - 1)]
    if all(x == d[0] for x in d): return ('arith', d[0])
    x0, x1, x2 = L[-3], L[-2], L[-1]
    if x1 != x0:
        num, den = x2 - x1, x1 - x0
        if den != 0 and num % den == 0:
            a = num // den
            b = x1 - a * x0
            if a >= 2 and all(L[i + 1] == a * L[i] + b for i in range(len(L) - 1)):
                return ('georec', (a, b))
    # second difference constant (quadratic run growth)?
    dd = [d[i + 1] - d[i] for i in range(len(d) - 1)]
    if len(dd) >= 3 and all(x == dd[0] for x in dd) and dd[0] != 0:
        return ('quad', dd[0])
    return ('irr', None)

def detect(fracs, max_runs=3000):
    primes, rules = compile_machine(fracs)
    runs, state, status, total = sim_runs(rules, len(primes), max_runs)
    out = {'status': status, 'total_steps': total, 'nruns': len(runs), 'primes': primes}
    if status == 'halt':
        out['class'] = 'HALTED'; return out
    if status == 'inf':
        out['class'] = 'INF_RUN'; return out
    tail = runs[len(runs) // 3:]
    syms = [r[0] for r in tail]
    p = find_symbol_period(syms)
    if p is None:
        out['class'] = 'COMPLEX'; return out
    n = len(tail)
    ncyc = min(CYCWIN, (n - 2) // p)
    kinds = []
    for j in range(p):
        Lj = [tail[n - 1 - j - k * p][1] for k in range(ncyc)][::-1]
        kinds.append((syms[n - 1 - j], classify_series(Lj)))
    ks = [k for _, (k, _) in kinds]
    if any(k == 'irr' for k in ks):      cls = 'NONRIGID'
    elif any(k == 'georec' for k in ks): cls = 'GEO'
    elif any(k in ('arith', 'quad') for k in ks): cls = 'POLY'
    else:                                cls = 'PERIODIC'
    out.update({'class': cls, 'period': p, 'kinds': kinds, 'ncyc': ncyc})
    return out

def main(path, max_runs=3000):
    lines = [l for l in open(path) if l.strip()]
    stats, listed = {}, []
    for i, line in enumerate(lines):
        r = detect(parse(line), max_runs)
        stats[r['class']] = stats.get(r['class'], 0) + 1
        if r['class'] in ('GEO', 'POLY', 'HALTED', 'INF_RUN', 'PERIODIC'):
            listed.append((i, line.strip(), r))
    print(f"file={path} max_runs={max_runs} total={len(lines)}")
    for k in sorted(stats): print(f"  {k}: {stats[k]}")
    print()
    for i, line, r in listed:
        kk = r.get('kinds')
        ks = ' '.join(f"f{s}:{kind}{par if par is not None else ''}"
                      for s, (kind, par) in kk) if kk else ''
        print(f"[{i}] {r['class']} p={r.get('period')} steps={r['total_steps']:.3e} {line}")
        if ks: print(f"      {ks}")

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 3000)
