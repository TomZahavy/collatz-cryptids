"""WS4.3 -- putting the certificate families in one currency.

The program has refuted three different families of non-halting certificate,
each measured in its own unit: DFA states (WS1), modulus (WS4.3c), backward
depth (WS2).  Those units are not comparable as written, which makes it easy to
mistake a big number in one unit for a strong result.  This file converts the
two that CAN be compared -- automatic sets and congruences -- into each other.

THE CONVERSION.  A congruence certificate is a union of residue classes mod m.
Such a set is recognised by the canonical residue tracker:

  MSB-first  state = x mod m,  delta(c, d) = (2c + d) mod m        -> m states
  LSB-first  state = (x so far mod m, 2^i mod m),
             delta((s,p), d) = ((s + d*p) mod m, 2p mod m)         -> T(m) states

so "no automatic certificate at <= n states" rules out every modulus whose
tracker fits in n states.  The two directions are wildly asymmetric: MSB needs
m states, LSB needs m times the multiplicative order of 2, and that asymmetry
is the same one the SAT searches measured in seconds.

WHAT COMES OUT.  The automatic bounds are the WEAKER statement about
congruences by three orders of magnitude -- and the STRONGER statement overall,
because almost no automatic set is a union of residue classes.  Each family is
exact inside its own bound and silent outside it, and neither contains the
other.  That, not any single number, is the shape of the negative result.

Run: python3 certificate_classes.py
"""


def lsb_tracker(m):
    """Reachable states of the LSB-first residue tracker for modulus m."""
    start = (0, 1 % m)
    seen, frontier = {start}, [start]
    while frontier:
        s, p = frontier.pop()
        for d in (0, 1):
            t = ((s + d * p) % m, 2 * p % m)
            if t not in seen:
                seen.add(t)
                frontier.append(t)
    return len(seen)


def order_of_2(m):
    """Multiplicative order of 2 mod the odd part of m (0 if that part is 1)."""
    odd = m
    while odd % 2 == 0:
        odd //= 2
    if odd == 1:
        return 0
    k, x = 1, 2 % odd
    while x != 1:
        x = x * 2 % odd
        k += 1
    return k


MSB_BOUND = 13          # no MSB certificate for the Needle at <= 13 states
LSB_BOUND = 11          # no LSB minimal-word certificate at <= 11 states
SWEEP_BOUND = 20000     # no congruence certificate at any modulus <= this


def main():
    print("WS4.3  THREE CERTIFICATE FAMILIES IN ONE CURRENCY\n")

    print("  m   MSB states   LSB states   ord_2   killed by MSB<=%d / LSB<=%d"
          % (MSB_BOUND, LSB_BOUND))
    msb_killed, lsb_killed = [], []
    for m in range(2, 41):
        t = lsb_tracker(m)
        km = m <= MSB_BOUND
        kl = t <= LSB_BOUND
        if km:
            msb_killed.append(m)
        if kl:
            lsb_killed.append(m)
        if m <= 20:
            print(f"  {m:2d}   {m:>10d}   {t:>10d}   {order_of_2(m):>5d}   "
                  f"{'MSB' if km else '   '} {'LSB' if kl else ''}")
    print("  ...")
    print()
    print(f"  moduli ruled out by the MSB bound (<= {MSB_BOUND} states): "
          f"{msb_killed[0]}..{msb_killed[-1]}  ({len(msb_killed)} moduli)")
    print(f"  moduli ruled out by the LSB bound (<= {LSB_BOUND} states): "
          f"{lsb_killed}  ({len(lsb_killed)} moduli)")
    print(f"  moduli ruled out by the direct sweep: 2..{SWEEP_BOUND:,} "
          f"({SWEEP_BOUND - 1:,} moduli)")
    print()
    print("  Read it the right way round:")
    print(f"   * on congruences the direct sweep beats the SAT bounds by "
          f"{SWEEP_BOUND // MSB_BOUND:,}x;")
    print("   * on everything else the SAT bounds are the only statement there is,")
    print("     since a union of residue classes is a vanishing fraction of the")
    print("     2-automatic sets of any given size;")
    print("   * the LSB bound, the headline for most of this program, is the")
    print(f"     weakest of the three on this axis: {len(lsb_killed)} moduli.")
    print("  The MSB/LSB gap here is the SAME asymmetry the solver timings")
    print("  measured -- m states against m*ord_2(m) -- showing up as a")
    print("  statement about content rather than about seconds.")


if __name__ == "__main__":
    main()
