from sat_generalq import search_sat
from search_m3 import reset_orbit
from machine3_map import branch
import sys
orb = reset_orbit(40)
halts = [27 ** i for i in range(1, 12)]
brs = []
for j in range(5):
    for r in (1, 2):
        A, B = branch(j, r)
        brs.append(([0] * j + [r], A, B, r == 2))
print("machine 3, base 3, branches j<=4, minimal-word convention")
for n in range(4, 10):
    if search_sat(n, 3, brs, orb, halts):
        print("   *** CERTIFICATE FOUND ***")
        break
