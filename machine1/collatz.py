"""Base system exactly as specified, plus exploration helpers."""
import random, sys

HALT = "HALT"

def base_step(s):
    a, b, c, d = s
    if c > 0:                       return (a, b+1, c-1, d)
    if d == 0:                      return (a+1, 0, 0, 2*b+2)
    # c == 0, d > 0
    if a >= 3:                      return (a-3, b+2, 0, d-1)
    if a == 2:                      return (0, 0, b+1, d-1)
    if a == 1 and b > 0:            return (1, 1, b+1, d-1)
    if a == 1:                      return (0, 0, 0, d+2)
    # a == 0
    if d == 1 and b == 0:           return (0, 0, 2, 5)
    if d == 1:                      return (0, 0, 2, 2*b+1)
    # a == 0, d >= 2
    if b >= d-1:                    return (3*d-4, 1, 2, 2*b-2*d+3)
    if d == b+2:                    return HALT
    if d == b+3:                    return (3*b+2, 0, 0, 6)
    if d == b+4:                    return (3*b+4, 0, 0, 4)
    return (3*b+3, 2, 0, d-b-5)     # d >= b+5

def run_base(s, max_steps):
    """Return (trajectory list incl. start, halted?)"""
    traj = [s]
    for _ in range(max_steps):
        s = base_step(s)
        if s == HALT:
            return traj, True
        traj.append(s)
    return traj, False

if __name__ == "__main__":
    # quick look: behavior from small starts
    random.seed(0)
    for start in [(0,0,0,0), (1,0,0,0), (0,0,0,5), (2,3,1,4), (5,0,0,7), (10,10,10,10)]:
        traj, halted = run_base(start, 2_000_000)
        print(start, "->", ("HALT after %d steps" % (len(traj)) if halted else "no halt in %d steps" % (len(traj)-1)),
              "last:", traj[-1])
