"""Cross-check the C port against the (base-verified) Python acceleration.

Set A: all odd a <= 20001 plus 300 random a in [2^12, 2^24), uncapped:
       compare (out, val, base, rounds, exit_d).
Set B: 200 random a in [2^28, 2^60), both sides capped at 100,000 rounds:
       compare full outcome, and for CAP the exact interior state (x, y) and
       base counts -- a state-exact agreement over 100k accelerated rounds
       exercises the u128 cascade path at real sizes.
"""
import random
import subprocess
import sys
from m4_accel import excursion

CC = "./m4_hunt"


def run_c(starts, cap=None):
    inp = "\n".join(str(a) for a in starts) + "\n"
    cmd = [CC, "verify"] + ([str(cap)] if cap else [])
    out = subprocess.run(cmd, input=inp, capture_output=True, text=True,
                         check=True).stdout.strip().splitlines()
    return out


rng = random.Random(777)

# ---- Set A ----
starts = list(range(1, 20002, 2)) + \
    [rng.randrange(1 << 12, 1 << 24) | 1 for _ in range(300)]
lines = run_c(starts)
assert len(lines) == len(starts)
bad = 0
for a, ln in zip(starts, lines):
    f = ln.split()
    r = excursion(a)
    exp = (r["out"], str(r["val"]) if r["out"] == "RETURN" else "-",
           str(r["base"]), str(r["rounds"]), str(r["exit_d"]))
    got = (f[0], f[1], f[2], f[3], f[4])
    if exp != got:
        bad += 1
        print("MISMATCH A", a, exp, got)
print(f"Set A: {len(starts)} starts, {bad} mismatches")

# ---- Set B ----
CAP = 100_000
startsB = [rng.randrange(1 << 28, 1 << 60) | 1 for _ in range(200)]
linesB = run_c(startsB, cap=CAP)
badB = 0
for a, ln in zip(startsB, linesB):
    f = ln.split()
    r = excursion(a, cap=CAP)
    if r["out"] == "CAP":
        exp = ("CAP", str(r["state"][0]), str(r["state"][1]),
               str(r["base"]), str(r["rounds"]))
        got = tuple(f[:5])
    else:
        exp = (r["out"], str(r["val"]) if r["out"] == "RETURN" else "-",
               str(r["base"]), str(r["rounds"]), str(r["exit_d"]))
        got = tuple(f[:5])
    if exp != got:
        badB += 1
        print("MISMATCH B", a, exp, got)
print(f"Set B: {len(startsB)} starts (cap {CAP}), {badB} mismatches")
sys.exit(1 if bad or badB else 0)
