"""Machine 4 — base rules, implemented exactly as specified.

State A(a, b), a >= 1, b >= 1.  Start A(1, 1).

EVEN a = 2k:
  A(2k, 1)   -> A(3, 2k+2)                       (b = 1)
  A(2k, 2)   -> A(2k+1, 1)                        (b = 2)
  A(2k, b)   -> A(2k+3, b-2)          b >= 3

ODD a = 2k+1:
  A(2k+1, 2m)    -> A(4m+3, 2k-2m+1)   k >= m >= 0   (b = 2m even, b <= a-1)
  A(2k+1, 2m+1)  -> A(4m+3, 2k-2m+3)   k >= m >= 0   (b = 2m+1 odd, b <= a)
  A(2k+1, 2k+2)  -> A(4k+1, 1)                        (b = a+1)
  A(2k+1, 2k+3)  -> A(4k+7, 1)                        (b = a+2)
  A(2k+1, 2k+4)  -> HALT                              (b = a+3)
  A(2k+1, 2k+5)  -> A(4k+5, 1)                        (b = a+4)
  A(2k+1, b)     -> A(4k+7, b-2k-5)    b >= 2k+6      (b >= a+5)

So halting requires a odd and b = a + 3.
"""

HALT = "HALT"


def step(s):
    a, b = s
    if a % 2 == 0:                                    # a = 2k
        if b == 1:
            return (3, a + 2)
        if b == 2:
            return (a + 1, 1)
        return (a + 3, b - 2)                          # b >= 3
    # a = 2k+1 odd
    k = (a - 1) // 2
    if b <= a:                                         # the two "m" rules
        if b % 2 == 0:                                # b = 2m
            m = b // 2
            return (4 * m + 3, 2 * k - 2 * m + 1)
        m = (b - 1) // 2                               # b = 2m+1
        return (4 * m + 3, 2 * k - 2 * m + 3)
    d = b - a                                          # b = a + d, d >= 1
    if d == 1:
        return (4 * k + 1, 1)                          # b = a+1
    if d == 2:
        return (4 * k + 7, 1)                          # b = a+2
    if d == 3:
        return HALT                                    # b = a+3
    if d == 4:
        return (4 * k + 5, 1)                          # b = a+4
    return (4 * k + 7, b - 2 * k - 5)                  # b >= a+5


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
