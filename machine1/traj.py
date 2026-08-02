"""Whole-trajectory equivalence check + profiling of macro rule usage."""
import random
from collections import Counter
from collatz import base_step, HALT
from accel import acc_step, is_halt_state

def check_trajectory(start4, n_base_steps):
    """Run base for n steps, storing states; then run acc from the drained
    start and check every macro checkpoint lands exactly on the base state
    at the claimed step index."""
    traj = [start4]
    s = start4
    halted_at = None
    for i in range(n_base_steps):
        s = base_step(s)
        if s == HALT:
            halted_at = len(traj)  # step index of halting transition
            break
        traj.append(s)
    # drain start's c to get initial triple + offset
    a, b, c, d = start4
    t, pos = (a, b + c, d), c
    if pos >= len(traj) and halted_at is None:
        return
    assert traj[pos] == (t[0], t[1], 0, t[2]), ("drain mismatch", start4)
    while True:
        if is_halt_state(t):
            assert halted_at is not None and pos == halted_at - 1, ("halt mismatch", start4, pos, halted_at)
            return "halted"
        t2, k = acc_step(t)
        pos += k
        if halted_at is None and pos >= len(traj):
            return "ran out (ok)"
        assert pos < len(traj), ("overran halt", start4)
        assert traj[pos] == (t2[0], t2[1], 0, t2[2]), ("ckpt mismatch", start4, pos, t2, traj[pos])
        t = t2

def profile(start3, n_macro):
    t = start3
    uses = Counter(); base_total = 0
    for _ in range(n_macro):
        if is_halt_state(t): break
        a, b, d = t
        if d == 0: tag = "recharge"
        elif a >= 3: tag = "drain"
        elif a == 2: tag = "two"
        elif a == 1 and b > 0: tag = "pump"
        elif a == 1: tag = "jump"
        elif d == 1: tag = "seed"
        elif b >= d-1: tag = "expand"
        elif d == b+3: tag = "reset3"
        elif d == b+4: tag = "reset4"
        else: tag = "shrink"
        t, k = acc_step(t)
        uses[tag] += 1; base_total += k
    return uses, base_total, t

if __name__ == "__main__":
    rng = random.Random(7)
    n = 0
    for _ in range(60):
        s4 = tuple(rng.randint(0, 30) for _ in range(4))
        check_trajectory(s4, 300_000); n += 1
    for _ in range(20):
        s4 = tuple(rng.randint(0, 2000) for _ in range(4))
        check_trajectory(s4, 300_000); n += 1
    # include the halting example and tiny starts
    for s4 in [(5,0,0,7), (0,0,0,0), (1,0,0,0), (0,0,0,1), (0,1,0,2)]:
        check_trajectory(s4, 300_000); n += 1
    print("trajectory verification passed on", n, "starts")

    # profiling: which macro rules dominate?
    for s3 in [(0,0,0), (10,10,10), (0,0,5)]:
        uses, bt, last = profile(s3, 3000)
        print(s3, "macro=3000, base steps covered =", bt, dict(uses), "last:", last)
