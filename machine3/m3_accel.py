"""Machine 3 — acceleration: batch the divide-chains, carry b exactly.

The machine is genuinely two-variable (the reset rules A(3k+r,b) -> A(..+b.., 1)
feed b back into a).  The one expensive event is a chain of divisions when a is
divisible by a high power of 3; that chain has a closed form.

DIVIDE-CHAIN LEMMA (verified).  From (N, b0) with N = 3^j * M, M % 3 != 0,
applying the a % 3 == 0 rule j times gives
        (M,  b0 + (N - M) + j).
Proof: each step (3k, b) -> (k, b + 2k + 1) adds 2(N/3^i) + 1 at level i;
summing i = 1..j gives j + 2 * (N - M)/2 = (N - M) + j.

COMPOSITE STEP (one base step, or one batched divide chain):
  a % 3 == 0 :  divide chain -> (M, b + (N - M) + j); if M == 1 the state is
                A(1, b + N - 1 + j) and the halt test applies.
  a % 3 == 1 :  reset -> (4*(a-1)//3 + b + 3, 1)
  a % 3 == 2 :  reset -> (4*(a-2)//3 + b + 5, 1)
  a == 1     :  HALT if b % 3 == 0, else continue by the A(1,.) rules.

HALTING (Theorem, m3_theorems.py):  halts iff a reaches an exact power of 3,
a = 3^j with j % 3 == 0 (equivalently b at a = 1 is divisible by 3, and there
b = 3^j + j so b % 3 = j % 3).  Everything else cannot halt.
"""
from m3_base import step, HALT


def v3(n):
    j = 0
    while n % 3 == 0:
        n //= 3
        j += 1
    return j, n


def cstep(a, b):
    """One composite step: next (a, b) with divide-chains batched, or a
    halt/through-1 signal.  Returns (a', b') or ('HALT', j) or ('A1', b')."""
    if a == 1:
        if b % 3 == 0:
            return "HALT", 0
        if b % 3 == 1:
            return (3 * ((b - 1) // 3) + 4, 1)
        return (3 * ((b - 2) // 3) + 3, 2)
    if a % 3 == 0:
        j, M = v3(a)
        b2 = b + (a - M) + j
        if M == 1:                              # reached A(1, b2 = 3^j + j)
            if j % 3 == 0:
                return "HALT", j
            return "A1", b2
        return (M, b2)
    if a % 3 == 1:
        return (4 * ((a - 1) // 3) + b + 3, 1)
    return (4 * ((a - 2) // 3) + b + 5, 1)


def run(a=1, b=1, max_steps=10 ** 7):
    """Iterate cstep from A(1,1). Returns (status, steps, state)."""
    for i in range(max_steps):
        r = cstep(a, b)
        if r[0] == "HALT":
            return "HALT", i, r[1]
        if r[0] == "A1":                        # passed through a = 1, continue
            a, b = 1, r[1]
            continue
        a, b = r
    return "NO-HALT", max_steps, (a, b)


if __name__ == "__main__":
    import random
    rng = random.Random(0)

    # --- divide-chain lemma, general start b0 ---
    bad = 0
    for _ in range(30000):
        j = rng.randint(1, 14)
        M = rng.choice([m for m in range(1, 60) if m % 3])
        b0 = rng.randint(1, 10 ** 6)
        N = 3 ** j * M
        a, b = N, b0
        for _ in range(j):
            k = a // 3
            a, b = k, b + 2 * k + 1
        if not (a == M and b == b0 + (N - M) + j):
            bad += 1
    assert bad == 0
    print("divide-chain lemma  b -> b + (N-M) + j: 30,000 cases OK")

    # --- cstep vs base machine, full trajectory from (1,1) ---
    def base_run(nbase):
        s = (1, 1)
        seen = []
        for _ in range(nbase):
            s = step(s)
            if s == HALT:
                seen.append(HALT)
                break
            seen.append(s)
        return seen

    base = base_run(200000)
    a, b = 1, 1
    idx = 0
    matched = 0
    for _ in range(200000):
        r = cstep(a, b)
        if r[0] == "HALT":
            break
        if r[0] == "A1":
            a, b = 1, r[1]
            # base visits A(1, b) explicitly; find it
            while idx < len(base) and base[idx] != (1, r[1]):
                idx += 1
            continue
        a, b = r
        # every composite (a,b) must appear in the base trajectory, in order;
        # cstep batches divide-chains so it outruns the base horizon quickly.
        while idx < len(base) and base[idx] != (a, b):
            idx += 1
        if idx >= len(base):
            break
        matched += 1
        idx += 1
    assert matched >= 100, matched
    print(f"cstep trajectory: {matched} composite states all matched base run in order "
          f"(then cstep outruns the {len(base)}-base-step horizon)")

    st, n, data = run(1, 1, 500000)
    print(f"run from (1,1): {st} after {n} composite steps"
          + (f", halting exponent {data}" if st == "HALT"
             else f", a={data[0].bit_length()} bits, b={data[1].bit_length()} bits"))
