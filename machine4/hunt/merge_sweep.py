"""Merge sweep shards into the p(k) table with Wilson CIs and trend test."""
import math
import re
import sys
from collections import defaultdict

PAT = re.compile(
    r"k=\s*(\d+) n=(\d+) decided=(\d+) halts=(\d+) p=[\d.]+ cap=(\d+) "
    r"ovf=(\d+)\s+d\[-1,1,2,3,4,5\]=(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)\s+"
    r"m8\[3\]=(\d+) m8\[7\]=(\d+)\s+E\[l2ratio\]=([-\d.]+) max_l2=([-\d.]+)\s+"
    r"E\[rounds\]=([\d.e+]+) max_rounds=([\d.e+]+) E\[base\]=([\d.e+]+)")

agg = defaultdict(lambda: [0] * 12 + [0.0, 0.0, 0.0, 0.0, 0.0])
# idx: 0 n,1 dec,2 halt,3 cap,4 ovf,5..10 dhist,11 m83(+m87 in 12?) -- use dict
rows = defaultdict(lambda: {"n": 0, "dec": 0, "halt": 0, "cap": 0, "ovf": 0,
                            "d": [0] * 6, "m83": 0, "m87": 0,
                            "l2w": 0.0, "maxl2": 0.0, "rw": 0.0, "bw": 0.0,
                            "maxr": 0.0})

for ln in open("sweep_shards.txt"):
    m = PAT.search(ln)
    if not m:
        continue
    g = m.groups()
    k = int(g[0])
    r = rows[k]
    n, dec, halt, cap, ovf = (int(g[i]) for i in range(1, 6))
    d = [int(g[i]) for i in range(6, 12)]
    m83, m87 = int(g[12]), int(g[13])
    l2, maxl2 = float(g[14]), float(g[15])
    er, maxr, eb = float(g[16]), float(g[17]), float(g[18])
    r["n"] += n; r["dec"] += dec; r["halt"] += halt
    r["cap"] += cap; r["ovf"] += ovf
    for i in range(6):
        r["d"][i] += d[i]
    r["m83"] += m83; r["m87"] += m87
    rets = dec - halt
    r["l2w"] += l2 * rets
    r["maxl2"] = max(r["maxl2"], maxl2)
    r["rw"] += er * n; r["bw"] += eb * n
    r["maxr"] = max(r["maxr"], maxr)


def wilson(h, n, z=1.96):
    if n == 0:
        return (0, 0)
    p = h / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    hw = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(c - hw, 0), c + hw)


print(f"{'k':>3} {'n':>5} {'dec':>5} {'halt':>4} {'p':>7} "
      f"{'95% CI':>15} {'cap':>4} {'d[-1,1,2,3,4,5]':>28} {'f(m8=3)':>7} "
      f"{'E[l2]':>6} {'E[rnd]/2^k':>10}")
ks, ps, ws = [], [], []
for k in sorted(rows):
    r = rows[k]
    dec, halt = r["dec"], r["halt"]
    p = halt / dec if dec else 0
    lo, hi = wilson(halt, dec)
    rets = dec - halt
    f3 = r["m83"] / (r["m83"] + r["m87"]) if (r["m83"] + r["m87"]) else 0
    print(f"{k:>3} {r['n']:>5} {dec:>5} {halt:>4} {p:>7.4f} "
          f"[{lo:.4f},{hi:.4f}] {r['cap']:>4} "
          f"{','.join(str(x) for x in r['d']):>28} {f3:>7.3f} "
          f"{r['l2w']/rets if rets else 0:>6.3f} "
          f"{r['rw']/r['n']/2**k if r['n'] else 0:>10.4f}")
    if dec >= 30:
        ks.append(k); ps.append(p); ws.append(dec)

# weighted least-squares trend of p on k
if len(ks) >= 3:
    W = sum(ws)
    mk = sum(w * k for w, k in zip(ws, ks)) / W
    mp = sum(w * p for w, p in zip(ws, ps)) / W
    cov = sum(w * (k - mk) * (p - mp) for w, k, p in zip(ws, ks, ps)) / W
    var = sum(w * (k - mk) ** 2 for w, k in zip(ws, ks)) / W
    slope = cov / var
    # rough standard error via binomial variance
    se = math.sqrt(sum(w * w * (p * (1 - p) / w) * (k - mk) ** 2
                       for w, k, p in zip(ws, ks, ps))) / (W * var)
    print(f"\nweighted trend: dp/dk = {slope:+.5f} +- {se:.5f} per bit "
          f"(over k={min(ks)}..{max(ks)})")
    pool = sum(rows[k]["halt"] for k in rows) / sum(rows[k]["dec"]
                                                   for k in rows)
    print(f"pooled p = {pool:.4f} over {sum(rows[k]['dec'] for k in rows)} "
          f"decided excursions")
