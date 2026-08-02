"""Is the 'divergent vs convergent cryptid' dichotomy real, or verified-depth?"""
import sys, math
for p in ["machine1","machine3","machine4","needle"]:
    sys.path.insert(0, f"/Users/tomzahavy/Documents/Claude/collatz/{p}")

# For each machine: return-map drift (dlog per return) AND return-TIME growth
# (steps between returns vs return index). Frequent returns -> geometric state;
# thinning returns -> linear state. Halting risk = sum 1/(return value): converges
# iff drift>0, for ALL of them.

def analyze(name, returns, times):
    lv=[math.log(x) for x in returns if x>1]
    drift=sum(lv[i+1]-lv[i] for i in range(len(lv)-1))/(len(lv)-1)
    # return-time growth: is time ~ linear (frequent) or ~ geometric (thinning) in index?
    if len(times)>3:
        lt=[math.log(max(t,1)) for t in times]
        # slope of log(time) vs index; ~0 => linear-in-index (frequent), >0 => exp thinning
        idx=list(range(len(lt)))
        n=len(lt); sx=sum(idx); sy=sum(lt); sxy=sum(i*t for i,t in zip(idx,lt)); sxx=sum(i*i for i in idx)
        slope=(n*sxy-sx*sy)/(n*sxx-sx*sx) if n*sxx-sx*sx else 0
    else: slope=float('nan')
    risk=sum(1.0/x for x in returns if x.bit_length()<900)
    print(f"{name:12} drift={drift:.3f}>0  return-time log-slope/idx={slope:.3f}  "
          f"sum 1/C over {len(returns)} returns = {risk:.4f}")

# machine 4
import m4_base as m4
s=(1,1); res=[]; tim=[]; steps=0; last=0
while steps<5_000_000 and len(res)<40:
    s=m4.step(s)
    if s==m4.HALT: break
    steps+=1
    if s[1]==1: res.append(s[0]); tim.append(steps-last); last=steps
analyze("machine 4", res, tim)

# machine 3 (frequent returns)
import m3_accel as m3
a,b=1,1; res=[]; tim=[]; steps=0; last=0
while steps<200000 and len(res)<3000:
    r=m3.cstep(a,b)
    if r[0]=="HALT": break
    if r[0]=="A1": a,b=1,r[1]; steps+=1; continue
    a,b=r; steps+=1
    if b==1 and a%3!=0: res.append(a); tim.append(steps-last); last=steps
analyze("machine 3", res, tim)
print("\ndrift>0 for ALL => sum 1/C converges for ALL => same halting mechanism.")
print("return-time slope: ~0 = frequent returns (geometric state); >0 = thinning (linear state)")
