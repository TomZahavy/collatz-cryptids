"""Machine 3's reset map in the WS1 branch-affine form, base 3.

Machine 3 (A(a,b), start A(1,1)) has b = 1 at every reset (its T4), so the
a-values at resets follow a one-variable map.  Writing a = 3^j (3m + r) with
j = v_3(a) and r in {1,2} -- i.e. the base-3 LSB word of a is 0^j r w(m) --
the accelerated step (divide chain, then reset) gives

    G(a) = a + m + j + c_r  =  (3^{j+1} + 1) m + (r*3^j + j + c_r),
    c_1 = 3, c_2 = 4,

the exact base-3 analogue of the Needle's (2^{v+1}+3)k + (2^v+v).  The
excluded case m = 0, r = 1 is a = 3^j, a pure power of 3: it halts when 3 | j
(the halting set is the powers of 27) and otherwise passes through A(1, .).
Those spine branches are simply OMITTED from the invariant search, which only
weakens the constraint set and so keeps any refutation sound.
"""
import sys

sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/machine3")
from m3_accel import cstep, v3                             # noqa: E402


def branch(j, r):
    """(A, B) with G(a) = A*m + B on the branch a = 3^j (3m + r)."""
    return 3 ** (j + 1) + 1, r * 3 ** j + j + (3 if r == 1 else 4)


def G(a):
    """The reset map, straight from the verified accelerated step."""
    j, M = v3(a)
    m, r = divmod(M, 3)
    assert r in (1, 2) and not (m == 0 and r == 1), "spine value"
    A, B = branch(j, r)
    return A * m + B


def reference(a):
    """Same step, but taken from machine 3's own verified cstep."""
    st = cstep(a, 1)
    if st[0] in ("HALT", "A1"):
        return st
    a2, b2 = st
    if b2 == 1:
        return a2
    st2 = cstep(a2, b2)                    # a divide chain follows; b resets
    return st2


def _tests():
    ok = 0
    for a in range(2, 60000):
        j, M = v3(a)
        m, r = divmod(M, 3)
        if r == 0 or (m == 0 and r == 1):
            continue                       # r==0 impossible; spine excluded
        st = cstep(a, 1)                   # divide chain (if 3 | a) ...
        assert st[0] not in ("HALT", "A1"), a
        if st[1] != 1:
            st = cstep(*st)                # ... then the reset
        a2, b2 = st
        assert b2 == 1, (a, st)            # T4: b is 1 at every reset
        assert G(a) == a2, (a, G(a), a2)
        ok += 1
    print(f"  branch-affine form G(a) = (3^(j+1)+1)m + (r*3^j + j + c_r) "
          f"matches machine 3's verified cstep on {ok} values a < 60000: OK")

    # the halting set really is the powers of 27, in base-3 spine form
    for j in range(1, 12):
        st = cstep(3 ** j, 1)
        assert (st[0] == "HALT") == (j % 3 == 0), (j, st)
    print("  a = 3^j halts iff 3 | j (powers of 27), j <= 11: OK")
    print("all machine-3 map tests passed")


if __name__ == "__main__":
    _tests()
