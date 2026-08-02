import tree_deficit as td
print("CONTROL: same backward tree, GENERIC roots (ceiling %.4f)" % td.ceiling())
for bits, n in ((800, 2000), (1600, 2000)):
    roots, dn, dc = td.run_random(bits, n)
    td._report(f"RANDOM roots, {bits} bits", roots, dn, dc, td.ceiling())
