"""Machine 3 — base rules, implemented exactly as specified.

State A(a, b), a >= 1, b >= 1.

  A(1, 3k)    -> HALT                        k >= 1   (b divisible by 3, b >= 3)
  A(1, 3k+1)  -> A(3k+4, 1)                           (b = 1 mod 3)
  A(1, 3k+2)  -> A(3k+3, 2)                           (b = 2 mod 3)
  A(3k,   b)  -> A(k, b + 2k + 1)            k >= 1, b >= 1   (a = 0 mod 3)
  A(3k+1, b)  -> A(4k + b + 3, 1)            k >= 1, b >= 1   (a = 1 mod 3, a >= 4)
  A(3k+2, b)  -> A(4k + b + 5, 1)            b >= 1           (a = 2 mod 3, a >= 2)

Start: A(1, 1).

Dispatch: a = 1 is handled by the first three rules (dispatch on b mod 3);
a >= 2 by the last three (dispatch on a mod 3).  The a = 1 mod 3 rule needs
k >= 1, i.e. a >= 4, so a = 1 never falls through to it.
"""

HALT = "HALT"


def step(s):
    a, b = s
    if a == 1:
        r = b % 3
        if r == 0:
            return HALT                        # A(1, 3k), k >= 1
        if r == 1:
            k = (b - 1) // 3
            return (3 * k + 4, 1)              # A(1, 3k+1) -> A(3k+4, 1)
        k = (b - 2) // 3
        return (3 * k + 3, 2)                  # A(1, 3k+2) -> A(3k+3, 2)
    r = a % 3
    if r == 0:
        k = a // 3
        return (k, b + 2 * k + 1)              # A(3k, b) -> A(k, b+2k+1)
    if r == 1:
        k = (a - 1) // 3
        return (4 * k + b + 3, 1)              # A(3k+1, b) -> A(4k+b+3, 1)
    k = (a - 2) // 3
    return (4 * k + b + 5, 1)                  # A(3k+2, b) -> A(4k+b+5, 1)


def run(s=(1, 1), n=100):
    out = [s]
    for _ in range(n):
        s = step(s)
        out.append(s)
        if s == HALT:
            break
    return out


if __name__ == "__main__":
    for i, s in enumerate(run((1, 1), 30)):
        print(f"  {i:3d}: {s}")
