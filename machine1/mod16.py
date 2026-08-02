"""A mod-16 confinement theorem for the return map F, and its consequences.

THEOREM. For every non-halting D, F(D) = 9 (mod 16). Hence the orbit of 17
satisfies D_k = 9 (mod 16) for every k >= 1.

PROOF. F(D) is the d-component of the b=1 anchor that ends the super-cycle.
A b=1 anchor is produced only in two reachable ways (Section 6.1):
  - exit R23:      d' = 16(d - b) - 55  = -55 = 9 (mod 16), identically.
  - SWEEP pump-exit: d' = 4*Dstar + 1,  Dstar = (w*4^{n-1} - 2)/3, w = 12*Delta + 8.
        n = 1: Dstar = (12*Delta + 6)/3 = 4*Delta + 2 = 2 (mod 4).
        n >= 2: w*4^{n-1} = 0 (mod 16), and (16j - 2)/3 = 2 (mod 4) throughout,
        so Dstar = 2 (mod 4) and d' = 4*Dstar + 1 = 9 (mod 16).
  (SWEEP's two-exit would need q = 0, which is not reachable with b'=1.)
Both cases give 9 (mod 16).  QED

CONSEQUENCES (verified below).
  1. The orbit lives in the single residue class 9 (mod 16) -- the tightest
     congruence confinement possible.
  2. The primary halting family D_i = 15*2^i - 2i - 12 is entirely EVEN, hence
     disjoint from the orbit: it can never be hit.
  3. Only H' := H cap {9 mod 16} is reachable; H' is far sparser than H
     (H is ~4/5 even; its odd part spreads over residues {1,3,7,9,15} mod 16).
  4. Yet no congruence separates the orbit from H: for every modulus m <= 256,
     H meets the orbit's residue set mod m. So this refines the non-halting
     heuristic (smaller effective density) but proves nothing.
"""
from onedim import F, n_B
from formal import G

def Fd(D):
    try:
        return F(D)[0]
    except RuntimeError:
        return "HALT"

def halts(D, cap=8000):
    b, d = 1, D
    first = True
    for _ in range(cap):
        if b == 1 and not first:
            return False
        first = False
        r = G(b, d)
        if r == "HALT":
            return True
        b, d = r
    return None

if __name__ == "__main__":
    import random
    rng = random.Random(0)

    # 1) F(D) = 9 (mod 16) universally
    resid = set()
    for _ in range(300000):
        D = rng.randint(8, 10**14)
        fd = Fd(D)
        if fd != "HALT":
            resid.add(fd % 16)
    assert resid == {9}, resid
    print(f"F(D) = 9 (mod 16) on 300k random D  (residues seen: {resid})")

    # 1b) the pump-exit half of the proof: Dstar = 2 (mod 4) always
    bad = 0
    for _ in range(300000):
        Dl = rng.randint(1, 10**7); n = rng.randint(1, 25)
        num = (12*Dl + 8) * 4**(n - 1) - 2
        if num % 3 == 0 and (num // 3) % 4 != 2:
            bad += 1
    assert bad == 0
    print("pump-exit certificate: Dstar = 2 (mod 4) with no exceptions")

    # 2) the real orbit stays in {9 mod 16}; primary family is even
    D = 17
    orb_res = set()
    for k in range(20000):
        if k >= 1:
            orb_res.add(D % 16)
        D = Fd(D)
        if D == "HALT":
            break
    assert orb_res == {9}, orb_res
    fam = {(15*2**i - 2*i - 12) % 2 for i in range(1, 40)}
    assert fam == {0}
    print("orbit of 17: D_k = 9 (mod 16) for all k>=1; primary family all even")

    # 3) H residues; the reachable part H cap {9 mod 16}
    Hlist = [D for D in range(2, 1500000) if halts(D)]
    odd = [h for h in Hlist if h % 2 == 1]
    H9 = [h for h in Hlist if h % 16 == 9]
    print(f"|H cap [2,1.5e6]| = {len(Hlist)} ({len(Hlist)-len(odd)} even, {len(odd)} odd); "
          f"reachable H cap {{9 mod 16}} = {H9}")

    # 4) no separating modulus <= 256
    D, Ms = 17, range(2, 257)
    orb = {m: set() for m in Ms}
    for k in range(20000):
        if k >= 1:
            for m in Ms:
                orb[m].add(D % m)
        D = Fd(D)
        if D == "HALT":
            break
    sep = [m for m in Ms if orb[m].isdisjoint({h % m for h in Hlist})]
    assert sep == [], sep
    print("no separating modulus m <= 256: H meets the orbit's residues at every m")
    print("\nAll checks passed: mod-16 confinement holds and refines (does not settle) halting.")
