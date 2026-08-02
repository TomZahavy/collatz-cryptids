"""Space Needle (BB(6)) — exact implementations.

Machine (bbchallenge): 1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD
Discovered by mxdys, Jan 2025; the wiki gives two high-level forms.

ONE-VARIABLE FORM (Katelyn Doucette), the halting-equivalent reduction.
Let v(b) = 2-adic valuation of b and m = b >> v(b) its odd part.
  Start b = 6.
  HALT if b is an exact power of 2 (m == 1).
  else  b -> b + v(b) + (3/2)(b/2^v(b) - 1) = b + v(b) + 3(m-1)/2.
Published sequence: 6, 10, 17, 41, 101, 251, 626, 1095, 2736, 2995, ...
Halting <=> the orbit hits an exact power of 2.

LOW-LEVEL FORM (Andrew Ducharme), config 0^inf <A 1^b 0 0 1^c 0^inf = (b, c).
  Start (3, 1).
  (1, c)     -> HALT
  (2b, c)    -> (2 + 5b + c, 1)
  (2b+1, c)  -> (b - 1, 3 + b + c)

Sources: wiki.bbchallenge.org Space Needle page (accessed July 2026).
"""

HALT = "HALT"


def v2(b):
    """(2-adic valuation, odd part) of b >= 1."""
    v = 0
    while b % 2 == 0:
        b //= 2
        v += 1
    return v, b


def is_pow2(b):
    return b >= 1 and (b & (b - 1)) == 0


def step1(b):
    """Doucette one-variable step; returns next b or HALT."""
    if is_pow2(b):
        return HALT
    v, m = v2(b)                       # m odd, >= 3 here
    return b + v + 3 * (m - 1) // 2


def step_ll(s):
    """Ducharme low-level (b, c) step; returns next state or HALT."""
    b, c = s
    if b == 1:
        return HALT
    if b % 2 == 0:
        bp = b // 2
        return (2 + 5 * bp + c, 1)
    bp = (b - 1) // 2
    return (bp - 1, 3 + bp + c)


def run1(b=6, n=100):
    out = [b]
    for _ in range(n):
        b = step1(b)
        out.append(b)
        if b == HALT:
            break
    return out


if __name__ == "__main__":
    # ---- fidelity: the published one-variable sequence ----
    want = [6, 10, 17, 41, 101, 251, 626, 1095, 2736, 2995]
    got = run1(6, 9)
    assert got == want, got
    print("one-variable form reproduces the wiki sequence "
          "6, 10, 17, 41, 101, 251, 626, 1095, 2736, 2995: OK")

    # the (3/2)(odd part - 1) term is always an integer (odd part - 1 is even)
    for b in range(3, 200000):
        if is_pow2(b):
            continue
        v, m = v2(b)
        assert (m - 1) % 2 == 0
    print("integrality: 3(m-1)/2 exact for all non-power-of-2 b < 200000: OK")

    # ---- low-level form runs without early halt (consistency) ----
    s = (3, 1)
    for i in range(2000):
        s = step_ll(s)
        if s == HALT:
            print(f"low-level halted at step {i} (state before)"); break
    else:
        print(f"low-level form (Ducharme) ran 2000 steps without halting; "
              f"b has {s[0].bit_length()} bits")
