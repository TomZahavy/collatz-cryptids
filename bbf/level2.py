"""Level-2 (cycle-jump) accelerated FRACTRAN simulation + phase detector.

Events: ('R', sym, klen)  explicit run (exact, level-1 machinery, verified)
        ('J', word, m)    the p-run word `word` repeated m more times (jump)

Jump length m is found by doubling + binary search on the exact predicate
"the next p runs from state + t*D reproduce `word`", then validated at 16
random interior t. The predicate check itself is exact; the interval
assumption (validity is a prefix set in t) is heuristic and disclosed --
flagged candidates get independent exact verification downstream.
"""
import sys, random
from fractran_accel import parse, compile_machine, classify_series
INF = float('inf')
rng = random.Random(12345)

def next_run(rules, state):
    """Exact level-1: (sym, k) of the next run from state, or None if halted.
    k may be INF (single fraction fires forever)."""
    j0 = None
    for j, (need, delta) in enumerate(rules):
        if all(state[i] >= e for i, e in need):
            j0 = j; break
    if j0 is None: return None
    need, delta = rules[j0]
    k_self = INF
    for i, e in need:
        d = delta[i]
        if d < 0: k_self = min(k_self, (state[i] - e) // (-d) + 1)
    s_pre = INF
    for e_need, _ in rules[:j0]:
        lo, hi = 1, INF
        for i, e in e_need:
            d = delta[i]; deficit = e - state[i]
            if d > 0:
                if deficit > 0: lo = max(lo, -((-deficit) // d))
            elif d == 0:
                if deficit > 0: lo = INF; break
            else:
                hi = min(hi, (state[i] - e) // (-d))
                if hi < lo: break
        if lo <= hi: s_pre = min(s_pre, lo)
    k = min(k_self, s_pre)
    return (j0, k)

def word_matches(rules, state, word):
    """Exact: do the next len(word) runs from `state` equal `word`?"""
    st = state[:]
    n = len(st)
    for (sym, klen) in word:
        r = next_run(rules, st)
        if r is None or r[0] != sym or r[1] != klen: return False
        d = rules[sym][1]
        for i in range(n): st[i] += klen * d[i]
    return True

def sim_events(rules, nprimes, max_events=4000, max_steps=10**60, maxp=6):
    state = [0] * nprimes; state[0] = 1
    events = []; total = 0
    window = []            # recent explicit runs (sym, k)
    while len(events) < max_events and total < max_steps:
        r = next_run(rules, state)
        if r is None: return events, state, 'halt', total
        sym, k = r
        if k is INF:
            events.append(('R', sym, INF)); return events, state, 'inf', total
        d = rules[sym][1]
        for i in range(nprimes): state[i] += k * d[i]
        total += k
        events.append(('R', sym, k)); window.append((sym, k))
        if len(window) > 12: window.pop(0)
        # try cycle jump: last 2p explicit runs = repeated block
        for p in range(1, maxp + 1):
            if len(window) >= 2 * p and window[-p:] == window[-2*p:-p]:
                word = window[-p:]
                D = [0] * nprimes
                wsteps = 0
                for (s2, k2) in word:
                    d2 = rules[s2][1]
                    for i in range(nprimes): D[i] += k2 * d2[i]
                    wsteps += k2
                if not word_matches(rules, state, word): break
                # doubling for first failure
                t = 1
                while word_matches(rules, [state[i] + t * D[i] for i in range(nprimes)], word):
                    t *= 2
                    if t > 10**40: break
                lo, hi = t // 2, t     # pred(lo)=T, pred(hi)=F (or cap)
                while hi - lo > 1:
                    mid = (lo + hi) // 2
                    if word_matches(rules, [state[i] + mid * D[i] for i in range(nprimes)], word):
                        lo = mid
                    else:
                        hi = mid
                m = lo + 1   # word valid to execute m more times (t=0..lo)
                # random interior validation
                ok = all(word_matches(rules, [state[i] + tt * D[i] for i in range(nprimes)], word)
                         for tt in (rng.randrange(0, m) for _ in range(16)))
                if ok and m >= 2:
                    for i in range(nprimes): state[i] += m * D[i]
                    total += m * wsteps
                    events.append(('J', tuple(word), m))
                    window.clear()
                break
    return events, state, 'cap', total

def replay_boundaries(rules, nprimes, events, bsym, skip_frac=4):
    """States and step-counts at starts of explicit runs of bsym."""
    st = [0] * nprimes; st[0] = 1
    steps = 0; bounds = []
    n0 = len(events) // skip_frac
    for ei, ev in enumerate(events):
        if ev[0] == 'R':
            _, sym, k = ev
            if sym == bsym and ei >= n0:
                bounds.append((steps, st[:]))
            d = rules[sym][1]
            for i in range(nprimes): st[i] += k * d[i]
            steps += k
        else:
            _, word, m = ev
            for (s2, k2) in word:
                d2 = rules[s2][1]
                for i in range(nprimes): st[i] += m * k2 * d2[i]
                steps += m * k2
    return bounds

def phase_detect2(fracs, max_events=4000, max_steps=10**60):
    primes, rules = compile_machine(fracs)
    nprimes = len(primes)
    events, state, status, total = sim_events(rules, nprimes, max_events, max_steps)
    out = {'status': status, 'total_steps': total, 'nevents': len(events),
           'primes': primes, 'rules': rules, 'events': events}
    if status == 'halt': out['class'] = 'HALTED'; return out
    if status == 'inf':  out['class'] = 'INF_RUN'; return out
    # symbol counts (jump-aware); boundary symbol must be explicit-only
    n0 = len(events) // 4
    cnt, incycle = {}, set()
    for ev in events[n0:]:
        if ev[0] == 'R': cnt[ev[1]] = cnt.get(ev[1], 0) + 1
        else:
            for (s2, _) in ev[1]: incycle.add(s2)
    cands = sorted((c, j) for j, c in cnt.items() if c >= 6 and j not in incycle)
    if not cands:
        cands = sorted((c, j) for j, c in cnt.items() if c >= 6)
    if not cands:
        out['class'] = 'FEWPHASE'; return out
    bsym = cands[0][1]
    out['bsym'] = bsym
    bounds = replay_boundaries(rules, nprimes, events, bsym)
    out['nphase'] = len(bounds)
    if len(bounds) < 6:
        out['class'] = 'FEWPHASE'; return out
    W = min(14, len(bounds) - 1)
    series = {'L': [bounds[i+1][0] - bounds[i][0] for i in range(len(bounds)-1)][-W:]}
    for c in range(nprimes):
        series[f'v{primes[c]}'] = [b[1][c] for b in bounds][-W:]
    kinds = {k: classify_series(v) for k, v in series.items()}
    out['kinds'] = kinds
    ks = [k for k, _ in kinds.values()]
    if any(k == 'irr' for k in ks):        cls = 'NONRIGID'
    elif any(k == 'georec' for k in ks):   cls = 'GEO'
    elif any(k in ('arith', 'quad') for k in ks): cls = 'POLY'
    else:                                   cls = 'MEGA_PER'
    out['class'] = cls
    return out

def main(path, max_events=4000):
    lines = [l for l in open(path) if l.strip()]
    stats, listed = {}, []
    for i, line in enumerate(lines):
        try:
            r = phase_detect2(parse(line), max_events)
        except Exception as ex:
            stats['ERROR'] = stats.get('ERROR', 0) + 1
            print(f"[{i}] ERROR {ex} {line.strip()}"); continue
        stats[r['class']] = stats.get(r['class'], 0) + 1
        if r['class'] in ('GEO', 'POLY', 'HALTED', 'INF_RUN', 'MEGA_PER', 'FEWPHASE'):
            listed.append((i, line.strip(), r))
    print(f"file={path} max_events={max_events} total={len(lines)}")
    for k in sorted(stats): print(f"  {k}: {stats[k]}")
    print()
    for i, line, r in listed:
        kk = r.get('kinds')
        ks = ' '.join(f"{n}:{kind}{par if par is not None else ''}"
                      for n, (kind, par) in kk.items()) if kk else ''
        print(f"[{i}] {r['class']} bsym={r.get('bsym')} nphase={r.get('nphase')} "
              f"steps={float(r['total_steps']):.3e} {line}")
        if ks: print(f"      {ks}")

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 4000)
