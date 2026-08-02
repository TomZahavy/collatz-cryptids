"""Return-map multipliers across the collection (Matthews-Watts drift)."""
import sys, math
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/machine1")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/machine3")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/machine4")
sys.path.insert(0, "/Users/tomzahavy/Documents/Claude/collatz/needle")

def drift(seq):
    """mean log-ratio between consecutive terms (>1)."""
    ls = [math.log(x) for x in seq if x > 1]
    d = [ls[i+1]-ls[i] for i in range(len(ls)-1)]
    return sum(d)/len(d), len(d)

# --- machine 1: F-orbit (return to section) ---
import onedim
D = 17; seq=[]
for _ in range(3000):
    seq.append(D); D = onedim.F(D)[0]
m1, n1 = drift(seq)
print(f"machine 1  F-orbit (per cycle):   mean dlog = {m1:.4f}  ({n1} returns)")

# --- machine 3: reset values (a-not-div-3, b=1) ---
import m3_accel as m3
a,b=1,1; res3=[]; steps=0
while steps<300000 and len(res3)<3000:
    r=m3.cstep(a,b)
    if r[0]=="HALT": break
    if r[0]=="A1": a,b=1,r[1]; steps+=1; continue
    a,b=r; steps+=1
    if b==1 and a%3!=0: res3.append(a)
m3d, n3 = drift(res3)
print(f"machine 3  reset a-values:         mean dlog = {m3d:.4f}  ({n3} resets)")

# --- machine 4: reset a-values (b=1 states) ---
import m4_base as m4
s=(1,1); res4=[]; steps=0
while steps<2000000 and len(res4)<3000:
    s=m4.step(s)
    if s==m4.HALT: break
    steps+=1
    if s[1]==1: res4.append(s[0])
m4d, n4 = drift(res4)
print(f"machine 4  reset a-values (b=1):    mean dlog = {m4d:.4f}  ({n4} resets)")

# --- Space Needle: step1 is the map ---
import needle
b=6; seqN=[]
for _ in range(20000):
    seqN.append(b); b=needle.step1(b)
    if b==needle.HALT: break
mN, nN = drift(seqN)
print(f"Space Needle  b-orbit (per step):  mean dlog = {mN:.4f}  ({nN} steps)")

print("\n>0 = supercritical (expanding return map); ~0 = critical (random-walk)")
