"""Phase-level rigid-tail detector.

Level 1: exact run-accelerated simulation (fractran_accel, verified vs ground truth).
Level 2: segment the run list at firings of the RAREST fraction in the tail
(phase boundaries). Record per phase: step length L_i and boundary exponent
vector v_i. Classify the trailing series of each (L and every coordinate of v):
  const / arith (x_{i+1}=x_i+d) / georec (x_{i+1}=a*x_i+b, a>=2, exact) / irr

Machine classes:
  HALTED     halted within horizon
  INF_RUN    provably infinite tail run (single fraction fires forever)
  GEO        some series georec, none irr  -> BW/rigid-orbit candidate
  POLY       some series arith/quad, none georec/irr -> polynomial closed form
  MEGA_PER   all series const -> exact mega-periodic (linear growth)
  NONRIGID   some series irregular -> state-dependent branching
  FEWPHASE   fewer than 5 complete phases observed -> undetermined
"""
import sys
from fractran_accel import parse, compile_machine, sim_runs, classify_series

def phase_detect(fracs, max_runs=60000, max_steps=10**14):
    primes, rules = compile_machine(fracs)
    runs, state, status, total = sim_runs(rules, len(primes), max_runs, max_steps)
    out = {'status': status, 'total_steps': total, 'nruns': len(runs),
           'primes': primes, 'rules': rules, 'runs': runs}
    if status == 'halt':
        out['class'] = 'HALTED'; return out
    if status == 'inf':
        out['class'] = 'INF_RUN'; return out
    # tail = last 3/4 of runs
    t0 = len(runs) // 4
    cnt = {}
    for j, k in runs[t0:]:
        cnt[j] = cnt.get(j, 0) + 1
    # boundary symbol: rarest fraction with >= 5 occurrences in tail
    cands = sorted((c, j) for j, c in cnt.items() if c >= 5)
    if not cands:
        out['class'] = 'FEWPHASE'; return out
    bsym = cands[0][1]
    out['bsym'] = bsym
    # replay runs to get states at boundaries (start of each bsym run)
    nprimes = len(primes)
    st = [0] * nprimes; st[0] = 1
    bounds = []   # (run_index, steps_so_far, state_copy)
    steps = 0
    deltas = [rules[j][1] for j in range(len(rules))]
    for ri, (j, k) in enumerate(runs):
        if j == bsym and ri >= t0:
            bounds.append((ri, steps, st[:]))
        d = deltas[j]
        for i in range(nprimes): st[i] += k * d[i]
        steps += k
    if len(bounds) < 6:
        out['class'] = 'FEWPHASE'; out['nphase'] = len(bounds); return out
    # phase lengths in steps, and boundary exponent series
    W = min(14, len(bounds) - 1)
    Ls = [bounds[i + 1][1] - bounds[i][1] for i in range(len(bounds) - 1)][-W:]
    series = {'L': Ls}
    for c in range(nprimes):
        series[f'v{primes[c]}'] = [b[2][c] for b in bounds][-W:]
    kinds = {k: classify_series(v) for k, v in series.items()}
    out['kinds'] = kinds
    out['nphase'] = len(bounds)
    ks = [k for k, _ in kinds.values()]
    if any(k == 'irr' for k in ks):        cls = 'NONRIGID'
    elif any(k == 'georec' for k in ks):   cls = 'GEO'
    elif any(k in ('arith', 'quad') for k in ks): cls = 'POLY'
    else:                                   cls = 'MEGA_PER'
    out['class'] = cls
    return out

def main(path, max_runs=60000):
    lines = [l for l in open(path) if l.strip()]
    stats, listed = {}, []
    for i, line in enumerate(lines):
        r = phase_detect(parse(line), max_runs)
        stats[r['class']] = stats.get(r['class'], 0) + 1
        if r['class'] in ('GEO', 'POLY', 'HALTED', 'INF_RUN', 'MEGA_PER', 'FEWPHASE'):
            listed.append((i, line.strip(), r))
    print(f"file={path} max_runs={max_runs} total={len(lines)}")
    for k in sorted(stats): print(f"  {k}: {stats[k]}")
    print()
    for i, line, r in listed:
        kk = r.get('kinds')
        ks = ' '.join(f"{n}:{kind}{par if par is not None else ''}"
                      for n, (kind, par) in kk.items()) if kk else ''
        print(f"[{i}] {r['class']} bsym={r.get('bsym')} nphase={r.get('nphase')} "
              f"steps={r['total_steps']:.3e} {line}")
        if ks: print(f"      {ks}")

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 60000)
