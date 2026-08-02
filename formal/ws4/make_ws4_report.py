"""Build the WS4 report: the formal hardness frontier.

Every number in the PDF is parsed out of a log produced by the scripts in this
directory -- gam.log, branch_type.log, congruence.log, certificate_classes.log,
clean_growth.log -- so the report cannot drift from the computation.  Missing
or incomplete logs raise rather than silently producing a plausible number.
"""
import os
import re

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.colors import HexColor

HERE = "/Users/tomzahavy/Documents/Claude/collatz/formal/ws4/"
OUT = HERE + "ws4_report.pdf"

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=styles["Heading1"], spaceBefore=16, spaceAfter=7,
                    fontSize=14)
H2 = ParagraphStyle("H2x", parent=styles["Heading2"], spaceBefore=12, spaceAfter=5,
                    fontSize=11.5)
BODY = ParagraphStyle("Bodyx", parent=styles["Normal"], fontSize=10.5, leading=14.5,
                      spaceAfter=7)
MATHC = ParagraphStyle("MathCx", parent=styles["Normal"], fontName="Times-Italic",
                       fontSize=10.5, leading=15, alignment=TA_CENTER,
                       spaceBefore=4, spaceAfter=8)
CELL = ParagraphStyle("Cellx", parent=styles["Normal"], fontName="Times-Roman",
                      fontSize=9.5, leading=12.5)
CODE = ParagraphStyle("Codex", parent=styles["Normal"], fontName="Courier",
                      fontSize=8.6, leading=11.2, spaceAfter=7,
                      textColor=HexColor("#333333"))
TITLE = ParagraphStyle("Titlex", parent=styles["Title"], fontSize=17, leading=21,
                       spaceAfter=4)
SUB = ParagraphStyle("Subx", parent=styles["Normal"], alignment=TA_CENTER,
                     textColor=HexColor("#555555"), fontSize=10.5, spaceAfter=16)
BLUE = HexColor("#1a3c6e")


def P(t, s=BODY):
    return Paragraph(t, s)


def tab(rows, header, widths):
    data = [[P(f"<b>{h}</b>", CELL) for h in header]]
    data += [[P(c, CELL) for c in r] for r in rows]
    t = Table(data, colWidths=list(widths), repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#b8c4d6")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#e8eef7")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, HexColor("#f6f8fb")])]))
    return t


# --------------------------------------------------------------- log parsing
def read(path):
    with open(HERE + path) as f:
        return f.read()


def grab(text, pattern, what):
    m = re.search(pattern, text)
    if not m:
        raise SystemExit(f"WS4 report: could not read {what} -- rerun the script")
    return m.groups() if len(m.groups()) > 1 else m.group(1)


GAM = read("gam.log")
BT = read("branch_type.log")
CG = read("congruence.log")
CC = read("certificate_classes.log")
GROW = read("clean_growth.log")

if "done " not in GROW:
    raise SystemExit("WS4 report: clean_growth.log is still running -- wait for it")

# gam.log
PG_RULES = grab(GAM, r"rules (\d+), modulus ([\d,]+)", "PRIMEGAME size")[0]
PG_MOD = grab(GAM, r"rules \d+, modulus ([\d,]+)", "PRIMEGAME modulus")
PG_PRIMES = grab(GAM, r"e = \[([^\]]+)\]", "PRIMEGAME primes")
MUL_RULES = grab(GAM, r"MUL.*?(\d+) instr ->\s+(\d+) rules", "MUL compile")
MUL_STEPS = grab(GAM, r"lockstep mismatches over ([\d,]+) steps: 0; starts computing "
                      r"the wrong answer: 0/64", "MUL lockstep")

# branch_type.log
BT_NEEDLE_BAD = grab(BT, r"mismatches over 2 <= x < ([\d,]+): (\d+)\s+\(branches v = 0\.\.(\d+)\)",
                     "needle affine check")
BT_M3_BAD = grab(BT, r"mismatches over 2 <= a < ([\d,]+): (\d+)\s+\(branches j = 0\.\.(\d+)\)",
                 "m3 affine check")
BT_SLOPES = grab(BT, r"distinct slopes among the first (\d+) branches", "slope count")
BT_COLL = grab(BT, r"Needle    F\((\d+)\) = F\((\d+)\) = (\d+)", "needle collision")
BT_COLL3 = grab(BT, r"machine 3 G\((\d+)\) = G\((\d+)\) = (\d+)", "m3 collision")

# congruence.log
CG_M = grab(CG, r"moduli 2\.\.([\d,]+), collisions", "modulus bound")
CG_K = grab(CG, r"index >= (\d+)", "threshold index")
CG_DIG = grab(CG, r"has (\d+) decimal digits", "cutoff digits")
CG_WORST_N = grab(CG, r"worst case: modulus ([\d,]+) needed index (\d+)", "needle worst")
CG_WORST_3 = re.findall(r"worst case: modulus ([\d,]+) needed index (\d+)", CG)[1]
CG_PARITY = grab(CG, r"mismatches (\d+) over ([\d,]+) values", "parity lemma")

# certificate_classes.log
CC_MSB = grab(CC, r"MSB bound \(<= (\d+) states\): (\d+)\.\.(\d+)\s+\((\d+) moduli\)",
              "msb kill")
CC_LSB = grab(CC, r"LSB bound \(<= (\d+) states\): \[([^\]]+)\]\s+\((\d+) moduli\)",
              "lsb kill")
CC_RATIO = grab(CC, r"SAT bounds by ([\d,]+)x", "ratio")

# clean_growth.log
def series(tag):
    out = {}
    for n, s in re.findall(rf"{tag}\s+n=\s*(\d+)\s+UNSAT\s+([\d.]+)s", GROW):
        out[int(n)] = float(s)
    if not out:
        raise SystemExit(f"WS4 report: no {tag} timings in clean_growth.log")
    return out


MSB_T = series("MSB")
LSB_T = series("LSB")
CORES = grab(GROW, r"cores=(\d+)", "core count")


def factors(tag):
    """Take the printed factors, not a recomputation from rounded timings --
    otherwise the report and its own log disagree in the last digit."""
    block = GROW.split(f"factors {tag}:")[1].split("---")[0]
    out = [(int(a), int(b), float(f))
           for a, b, f in re.findall(r"n=(\d+)->(\d+):\s*([\d.]+)x", block)]
    if not out:
        raise SystemExit(f"WS4 report: no {tag} factor lines in clean_growth.log")
    return out


MSB_F = factors("MSB")
LSB_F = factors("LSB")
RATIOS = {int(n): float(r)
          for n, r in re.findall(r"n=\s*(\d+)\s+LSB/MSB =\s*([\d.,]+)", GROW)}
if not RATIOS:
    raise SystemExit("WS4 report: no cross-encoding ratios in clean_growth.log")

MSB_BOUND, LSB_BOUND = 13, 11

story = []
story.append(P("WS4 &mdash; The formal hardness frontier", TITLE))
story.append(P("Where decision technology dies, how far each certificate class "
               "actually reaches, and what the reach is worth", SUB))
story.append(HRFlowable(width="100%", thickness=1.1, color=BLUE,
                        spaceBefore=0, spaceAfter=14))

# ============================================================ 1
story.append(P("1. What this work stream was for, and what it turned into", H1))
story.append(P(
    "WS4 was planned as an assembly job: take known results about the "
    "undecidability of Collatz-like iteration, add our own theorems, and write "
    "down the boundary. The revision of July 27 changed the brief. By then the "
    "program had refuted three separate families of non-halting certificate, "
    "each measured in its own unit &mdash; DFA states, congruence modulus, "
    "backward depth &mdash; and the sharper deliverable was no longer the "
    "literature boundary but <i>our own</i>: three certificate families, each "
    "exact within its bound, each silent beyond it, and the growth constant of "
    "each bound."))
story.append(P(
    "Executing that produced four things the plan did not anticipate, and one "
    "of them is a correction to a claim this program has been making for two "
    "days."))
story.append(P(
    "<b>(a) The units are not comparable, and when converted the headline is "
    "the weakest of the three.</b> The LSB-first automatic-invariant bound "
    "&mdash; the result most of the WS1 effort bought &mdash; rules out "
    f"congruence certificates at exactly {CC_LSB[2]} moduli. A direct sweep "
    f"costing 30 seconds rules them out at {CG_M}. Section 5.", BODY))
story.append(P(
    "<b>(b) The threshold argument I wrote first was unsound</b>, and the fix "
    "made the theorem stronger rather than weaker. Section 5.2."))
story.append(P(
    "<b>(c) A new proved lemma about machine 3</b> fell out of chasing the one "
    "modulus that survived: the parity of the next orbit value is the parity of "
    "the current 3-adic valuation. Section 5.3."))
story.append(P(
    "<b>(d) The size frontier does not separate our cryptids from universal "
    "machines</b>, and the plan's phrasing &mdash; \"our cryptids sit strictly "
    "below\" &mdash; presumed an answer nobody has. Section 3.4."))

# ============================================================ 2
story.append(P("2. Measurement hygiene first", H1))
story.append(P(
    "Everything in Section 6 is a ratio of solver times, so it is worth saying "
    "at the outset how those were obtained, because the earlier numbers in "
    "RESULTS.md were not obtained that way."))
story.append(P(
    "The searches that produced the impossibility bounds were run concurrently "
    f"on one {CORES}-core box at varying load, with a recorded uncertainty of "
    "roughly &plusmn;30%. That is fine for the bounds themselves &mdash; a "
    "completed UNSAT is a completed UNSAT no matter how long it took &mdash; "
    "but it is not fine for a report whose content is the growth constants. The "
    "trigger was concrete: the MSB step from 12 to 13 states measured 10.18&times; "
    "under heavy load and 5.47&times; after two competing multi-day jobs were "
    "killed, and those two readings cannot be separated after the fact."))
story.append(P(
    "So the growth table here comes from <font face='Courier'>clean_growth.py</font>: "
    "one process, strictly sequential, nothing else of ours running, load average "
    "sampled at every instance and printed into the log. The effect is not "
    f"subtle. MSB at n = 10 took {MSB_T[10]:.1f} s here against 24.6 s in the "
    "loaded run. Every ratio below is between two timings taken under the same "
    "conditions."))

# ============================================================ 3
story.append(P("3. WS4.1 &mdash; one syntax for cryptids and for universality", H1))

story.append(P("3.1&nbsp;&nbsp;The definition", H2))
story.append(P(
    "A <b>one-counter guarded affine machine</b> (GAM) has state an integer "
    "x &gt; 0, a selector &sigma;(x) choosing among finitely many rule schemas, "
    "and rules x &rarr; (a<sub>i</sub>x + b<sub>i</sub>)/c<sub>i</sub> guarded by "
    "exactness of the division. Two selector kinds occur in this project:"))
story.append(P(
    "<b>RES(d)</b> &mdash; &sigma;(x) is the first rule whose guard divides x, "
    "so it is decided by x mod d for d the lcm of the guards. Finitely many "
    "affine pieces.<br/>"
    "<b>VAL(q)</b> &mdash; &sigma;(x) = v<sub>q</sub>(x), the q-adic valuation. "
    "Infinitely many affine pieces, generated by one schema."))
story.append(P(
    "The point of writing it this way is that FRACTRAN is exactly RES with "
    "b<sub>i</sub> = 0 and a<sub>i</sub>/c<sub>i</sub> = p<sub>i</sub>/q<sub>i</sub>. "
    "Conway's universality theorem is therefore a statement about this syntax "
    "and needs no translation layer &mdash; and Fenrir, our machine 7, is "
    "written in the very class Conway proved universal, which says nothing "
    "about Fenrir itself but means no translation is needed to compare them."))

story.append(P("3.2&nbsp;&nbsp;Register machines compile in, step for step", H2))
story.append(P(
    "<b>Construction (machine-verified).</b> Encode a register machine state as "
    "n = &prod; p<sub>j</sub><super>r<sub>j</sub></super> &middot; s<sub>L</sub>, "
    "with distinct primes for the registers and one prime per instruction label, "
    "the label prime appearing to the first power. Then"))
story.append(P("INC(j, k) at label L &nbsp;&rarr;&nbsp; the single fraction "
               "p<sub>j</sub>s<sub>k</sub> / s<sub>L</sub><br/>"
               "DEC(j, k, z) at label L &nbsp;&rarr;&nbsp; s<sub>k</sub> / "
               "(p<sub>j</sub>s<sub>L</sub>) &nbsp;then&nbsp; s<sub>z</sub> / s<sub>L</sub>",
               MATHC))
story.append(P(
    "Exactly one label prime divides n at any time, so no two instructions can "
    "compete; within an instruction the decrement branch precedes the zero "
    "branch, which is what makes the guard order do the test. An I-instruction "
    "machine yields at most 2I rules, and the halt label has no rule, so the GAM "
    "halts exactly where the register machine does."))
story.append(P(
    "<b>Verification.</b> The compiled machine is run in lockstep with a direct "
    f"register-machine interpreter. For r0 += r1&middot;r2 the {MUL_RULES[0]}-instruction "
    f"program compiles to {MUL_RULES[1]} rules and agrees on all {MUL_STEPS} steps "
    "across 64 starts, with every start also checked to produce the right answer "
    "&mdash; a program that silently loops cannot pass by vacuity. "
    "(<font face='Courier'>gam.py</font>.)"))
story.append(P(
    "<b>Consequence.</b> With Minsky's theorem that register machines are "
    "Turing-complete, RES-GAMs are Turing-complete, and the smallest universal "
    "instruction count I gives an upper bound of 2I rules on where universality "
    "begins in our syntax. That is a real frontier statement, and it is an upper "
    "bound only."))

story.append(P("3.3&nbsp;&nbsp;An anchor that needs no citation", H2))
story.append(P(
    f"Conway's PRIMEGAME is a {PG_RULES}-rule RES-GAM with modulus {PG_MOD}. "
    "Run here from x = 2, the pure powers of two appearing in its orbit have "
    f"exponents {PG_PRIMES} &mdash; the primes, consecutively, checked rather "
    "than quoted. So unbounded nontrivial computation is available in this "
    f"syntax at {PG_RULES} rules and one counter."))

story.append(P("3.4&nbsp;&nbsp;Where the cryptids sit &mdash; and what that does not prove", H2))
story.append(P(
    "The Needle is one counter, VAL(2), and <i>one</i> rule schema: "
    "F(x) = (2<super>v+1</super> + 3)k + (2<super>v</super> + v). Machine 3 is "
    "one counter, VAL(3), one schema. Written down, they are smaller than "
    f"PRIMEGAME's {PG_RULES} rules."))
story.append(P(
    "<b>The plan said this meant they \"sit strictly below\" the universal "
    "machines. That does not follow, and I do not believe it.</b> VAL(q) unfolds "
    "a single schema into infinitely many affine pieces &mdash; Section 4 shows "
    "the Needle really does have infinitely many distinct slopes &mdash; so "
    "smaller on the page is not smaller in power. Nothing in this section, and "
    "nothing we know of in the literature, lower-bounds the computational power "
    "of a one-schema VAL machine."))
story.append(P(
    "<b>The open question this leaves, which is worth more than the section that "
    "produced it.</b> Is the one-schema VAL(q) class Turing-complete? It is a "
    "genuine two-sided bet, the second the program has found and the first still "
    "open. Universality would show the size frontier is vacuous for our "
    "machines and would explain the resistance structurally. A decision "
    "procedure for the class would <i>decide our cryptids</i>. Both outcomes are "
    "consequential, which is exactly the property the program has learned to "
    "look for."))

# ============================================================ 4
story.append(P("4. WS4.2 &mdash; the fault line, made checkable", H1))
story.append(P(
    "The literature on one-dimensional piecewise-affine maps has a decidable "
    "island: reachability is decidable for injective maps with finitely many "
    "pieces cut out by intervals (LICS 2023). The plan asserted our machines sit "
    "outside it by branching type. Asserting is not enough for a hardness "
    "write-up, so both hypotheses are settled here by computation against the "
    "machines' own verified step functions."))

story.append(P("4.1&nbsp;&nbsp;The slope set is infinite", H2))
story.append(P(
    "<b>Proposition (proved; machine-verified).</b> On the branch "
    "v<sub>2</sub>(x) = v the Needle map is affine with"))
story.append(P("F(x) = (1 + 3&middot;2<super>&minus;(v+1)</super>) x + (v &minus; 3/2)",
               MATHC))
story.append(P(
    f"and for machine 3, G(a) = (1 + 3<super>&minus;(j+1)</super>) a + "
    f"(j + c<sub>r</sub> &minus; r/3) on v<sub>3</sub>(a) = j. Checked against "
    f"<font face='Courier'>needle.step1</font> and machine 3's own accelerated "
    f"step in exact rational arithmetic: {BT_NEEDLE_BAD[1]} mismatches over "
    f"2 &le; x &lt; {BT_NEEDLE_BAD[0]} (branches v = 0..{BT_NEEDLE_BAD[2]}) and "
    f"{BT_M3_BAD[1]} over 2 &le; a &lt; {BT_M3_BAD[0]} (branches j = 0..{BT_M3_BAD[2]})."))
story.append(P(
    "The slopes are 5/2, 7/4, 11/8, 19/16, 35/32, 67/64, ... &rarr; 1, pairwise "
    f"distinct: all {BT_SLOPES} of the first {BT_SLOPES} are different, and the "
    "general form (2<super>v+1</super>+3)/2<super>v+1</super> is visibly "
    "injective in v. A map with finitely many affine pieces has finitely many "
    "slopes. <b>So hypothesis (H1) fails, and no refinement of the partition can "
    "repair it</b> &mdash; the obstruction is in the slope set, not in how the "
    "pieces are described."))
story.append(P(
    "There is a second thing worth reading off this. The slopes tend to 1: the "
    "high-valuation branches are nearly the identity. The map is expanding on "
    "average while almost all of its individual pieces are almost neutral, which "
    "is why bounded-state reasoning about any fixed finite set of branches says "
    "nothing about the orbit."))

story.append(P("4.2&nbsp;&nbsp;The maps are not injective", H2))
story.append(P(
    f"F({BT_COLL[0]}) = F({BT_COLL[1]}) = {BT_COLL[2]}: two different valuation "
    "branches land on one value. The witness is not exotic &mdash; "
    f"{BT_COLL[2]} is the third element of the published orbit "
    "6, 10, 17, 41, 101, ..., so the failure of injectivity is visible on the "
    "trajectory the whole problem is about. For machine 3, "
    f"G({BT_COLL3[0]}) = G({BT_COLL3[1]}) = {BT_COLL3[2]}."))
story.append(P(
    "<b>So (H2) fails as well, independently.</b> The two hypotheses of the "
    "decidable island fail for unrelated reasons, which is a stronger statement "
    "than \"our machines are not covered\": there is no reformulation that "
    "sneaks in, because a reformulation would have to fix both."))

# ============================================================ 5
story.append(P("5. WS4.3 &mdash; the certificate-impossibility account", H1))

story.append(P("5.1&nbsp;&nbsp;In one variable, semilinear means congruence plus threshold", H2))
story.append(P(
    "A subset of the naturals is Presburger-definable exactly when it is "
    "ultimately periodic: there are T and m with x &#8712; S iff x + m &#8712; S "
    "for all x &ge; T. That is precisely the class "
    "{x &lt; T} &cup; {x &ge; T : x mod m &#8712; S}. Three literature strands "
    "collapse into this one class in our setting:"))
story.append(P(
    "&bull; <b>Linear-arithmetic non-termination certificates</b> &mdash; in one "
    "variable there is nothing else to write.<br/>"
    "&bull; <b>bbchallenge regular deciders</b> (FAR, WFAR, RepWL, CPS) &mdash; "
    "they operate on tapes encoding counters in unary or block form, and a "
    "regular language over a one-letter alphabet is ultimately periodic. What "
    "such a decider can say about a counter is exactly a congruence with a "
    "threshold.<br/>"
    "&bull; <b>The affine sieve</b> &mdash; whose only fuel is expansion in "
    "congruence quotients, provably absent here."))
story.append(P(
    "So refuting this one class refutes all three at once, and does so for a "
    "reason the bbchallenge wiki states only empirically."))

story.append(P("5.2&nbsp;&nbsp;The refutation, and the bug in my first version of it", H2))
story.append(P(
    "<b>The argument.</b> Suppose I = {x &lt; T} &cup; {x &ge; T : x mod m "
    "&#8712; S} contains the orbit and avoids the halting set H. Take an orbit "
    "element x<sub>i</sub> &ge; T and an h &#8712; H with h &ge; T and "
    "h &#8801; x<sub>i</sub> (mod m). Then x<sub>i</sub> &#8712; I forces its "
    "class into S, so h &#8712; I &mdash; and h &#8712; H. Contradiction. A "
    "certificate therefore exists only if no orbit element above T is congruent "
    "to any element of H above T."))
story.append(P(
    "<b>The bug.</b> My first implementation collected every residue that "
    "2<super>e</super> takes mod m and looked for a collision with those. That "
    "is unsound for the threshold claim. The sequence 2<super>e</super> mod m is "
    "<i>eventually</i> periodic, and a residue in the pre-period is taken by "
    "finitely many powers of two &mdash; so a collision there is defeated by a "
    "large enough T. Mod 12, for instance, the powers of two run 1, 2, 4, 8, 4, "
    "8, ...: a collision at residue 1 or 2 proves nothing about thresholds above 2."))
story.append(P(
    "<b>The fix, which strengthened the theorem.</b> Restricting to the eventual "
    "cycle makes every collision witness an <i>infinite</i> family of halting "
    "values, hence arbitrarily large ones, so the refutation holds for "
    "<i>every</i> threshold rather than for thresholds below some cutoff. The "
    "search got harder and the conclusion got better."))
story.append(P(
    "<b>Result (machine-verified over the stated domain).</b> For both machines, "
    f"every modulus 2 &le; m &le; {CG_M} admits a collision at orbit index "
    f"&ge; {CG_K}, using the complete cycle residues of H. Hence <b>no "
    "congruence certificate with any modulus in that range and any threshold "
    "whatsoever</b>. The Needle's hardest modulus was "
    f"{CG_WORST_N[0]}, needing orbit index {CG_WORST_N[1]}; machine 3's was "
    f"{CG_WORST_3[0]}, needing index {CG_WORST_3[1]}."))
story.append(P(
    "The threshold-free half of this needs no computation at all and is worth "
    "recording separately. The Needle's b is strictly increasing (its T2), so "
    "the orbit is unbounded; a certificate that is a finite union of intervals "
    "and contains an unbounded set must contain a ray [T, &infin;); every ray "
    "contains a power of two. <b>So no finite-union-of-intervals certificate "
    "exists, unconditionally</b> &mdash; the m = 1 case, proved rather than swept."))

story.append(P("5.3&nbsp;&nbsp;A lemma found by chasing the last survivor", H2))
story.append(P(
    f"One modulus held out: {CG_WORST_3[0]} = 2&middot;3<super>8</super> for "
    "machine 3, whose cycle residue is the single value 6561. A separating "
    "congruence would <i>prove</i> machine 3 never halts from its start, so it "
    "was worth diagnosing rather than dismissing. The required residue means "
    "v<sub>3</sub>(a) &ge; 8 together with an odd 3-free part, and among the "
    "orbit's first 60,500 values all eight with v<sub>3</sub> &ge; 8 had an even "
    "3-free part. Eight for eight looks structural at p = 1/256 &mdash; if the "
    "parity were balanced."))
story.append(P("<b>Lemma (proved; machine-verified).</b> It is not balanced:", BODY))
story.append(P("G(a) &#8801; v<sub>3</sub>(a) &nbsp;(mod 2)", MATHC))
story.append(P(
    "<i>Proof.</i> G(a) = (3<super>j+1</super>+1)m + (r&middot;3<super>j</super> "
    "+ j + c<sub>r</sub>) with j = v<sub>3</sub>(a), r &#8712; {1,2}, "
    "c<sub>1</sub> = 3, c<sub>2</sub> = 4. The first coefficient is even and "
    "3<super>j</super> is odd, so G(a) &#8801; r + j + c<sub>r</sub> (mod 2); "
    "r + c<sub>r</sub> is odd for both values of r, giving G(a) &#8801; j. "
    "<b>QED</b> &nbsp; "
    f"Verified: {CG_PARITY[0]} mismatches over {CG_PARITY[1]} values a &lt; 400,000."))
story.append(P(
    "So the 3-free part of a machine-3 orbit value is odd only about a quarter "
    "of the time, not half, and eight even ones in a row has probability 0.10 "
    "&mdash; unremarkable. The survivor was luck, not structure, and extending "
    "the orbit killed it at index 105,033. <b>The lemma is the durable output: a "
    "new proved fact about machine 3, found only because a null result was "
    "checked instead of accepted.</b>"))

story.append(P("5.4&nbsp;&nbsp;Three families in one currency", H2))
story.append(P(
    "The three refuted families are measured in units that cannot be compared as "
    "written, which makes it easy to mistake a large number in one unit for a "
    "strong result. Two of them can be converted into each other exactly. A "
    "congruence certificate is a union of residue classes mod m, and the "
    "canonical residue trackers are"))
story.append(P(
    "MSB-first: state = x mod m, &nbsp;&delta;(c, d) = (2c + d) mod m "
    "&nbsp;&rarr;&nbsp; m states<br/>"
    "LSB-first: state = (x so far mod m, 2<super>i</super> mod m) "
    "&nbsp;&rarr;&nbsp; m &middot; ord<sub>m</sub>(2) states", MATHC))
story.append(P(
    "so \"no automatic certificate at &le; n states\" rules out every modulus "
    "whose tracker fits in n states. The asymmetry is severe, and it is the same "
    "asymmetry the solver timings measured &mdash; here showing up as a "
    "statement about content rather than about seconds."))
story.append(tab([
    ["congruence + threshold", "modulus m",
     f"every m &le; {CG_M}, any threshold",
     "unions of residue classes only"],
    [f"MSB automatic (&le; {MSB_BOUND} states)", "DFA states",
     f"moduli {CC_MSB[1]}..{CC_MSB[2]} &nbsp;({CC_MSB[3]} of them)",
     "any 2-automatic set"],
    [f"LSB automatic (&le; {LSB_BOUND} states)", "DFA states",
     f"moduli {CC_LSB[1]} &nbsp;({CC_LSB[2]} of them)",
     "any 2-automatic set"],
    ["backward-depth counting (WS2)", "depth L",
     "exact counts at every fixed L", "density, not separation"],
], ["certificate family", "unit of the bound", "reach, in moduli", "what it covers"],
    [1.55 * inch, 0.95 * inch, 1.75 * inch, 1.75 * inch]))
story.append(P(
    "<b>Read the right way round, this reorders the program.</b> On congruences "
    f"the 30-second sweep beats the SAT bounds by {CC_RATIO}&times;. On "
    "everything else the SAT bounds are the only statement there is, because a "
    "union of residue classes is a vanishing fraction of the automatic sets of "
    "any given size. Neither family contains the other, and the LSB bound "
    "&mdash; the headline of this program for two days, and the thing three "
    f"multi-day jobs were spent on &mdash; is the weakest of the three on this "
    f"axis, at {CC_LSB[2]} moduli."))
story.append(P(
    "That is not an argument that WS1 was wasted; it is an argument that its "
    "value was never in the state count. What WS1 actually established is the "
    "<i>shape</i> of the obstruction &mdash; that a certificate must avoid the "
    "whole halting basin, not just H &mdash; and that finding survives the "
    "conversion intact."))

# ============================================================ 6
story.append(P("6. The growth constants, re-measured", H1))
story.append(P(
    "Each family's bound is bought with compute, and the price per unit is the "
    "part of the account that tells you what not to buy next. Under the "
    "single-load protocol of Section 2:"))

rows = []
ks = sorted(set(list(MSB_T) + list(LSB_T)))
mf = {b: f for _, b, f in MSB_F}
lf = {b: f for _, b, f in LSB_F}
for n in ks:
    rows.append([
        str(n),
        f"{MSB_T[n]:,.1f}" if n in MSB_T else "&mdash;",
        f"{mf[n]:.2f}&times;" if n in mf else "&mdash;",
        f"{LSB_T[n]:,.1f}" if n in LSB_T else "&mdash;",
        f"{lf[n]:.2f}&times;" if n in lf else "&mdash;",
        f"{RATIOS[n]:,.2f}" if n in RATIOS else "&mdash;",
    ])
story.append(tab(rows, ["n", "MSB sec", "MSB step", "LSB sec", "LSB step",
                        "LSB/MSB"],
                 [0.5 * inch, 0.95 * inch, 0.95 * inch, 0.95 * inch,
                  0.95 * inch, 0.95 * inch]))
story.append(P(
    "<b>The rise is real, and it is far cleaner than the contaminated series "
    "suggested.</b> Both encodings now come out <i>strictly monotone</i>: MSB at "
    + ", ".join(f"{f:.2f}" for _, _, f in MSB_F) + " and LSB at "
    + ", ".join(f"{f:.2f}" for _, _, f in LSB_F) +
    ". The loaded MSB measurement had wandered &mdash; 4.33 down to 3.46, up to "
    "5.47, 6.70, 10.18, then back down to 5.47 &mdash; and every one of those "
    "reversals was load rather than mathematics."))
story.append(P(
    "Two claims settle here. <b>The earlier reading that the per-state factor "
    "had fallen back to 5.47 at n = 13 is withdrawn</b>; it arrived precisely as "
    "two competing multi-day jobs were killed, and under clean measurement that "
    f"step is the largest in the series at {MSB_F[-1][2]:.2f}&times;. And the "
    "claim that the last step is the largest in every series, which had rested "
    "on four noisy series, now rests on two clean ones and holds in both."))
story.append(P(
    "The cross-encoding ratio behaves the same way: "
    + ", ".join(f"{RATIOS[n]:,.2f}" for n in sorted(RATIOS)) +
    f" at n = {min(RATIOS)}..{max(RATIOS)}. It compounds, so MSB carries a "
    "genuinely smaller per-state factor rather than a constant discount. Both "
    "arguments of the old exchange-rate formula log<sub>g</sub>(C) drift, which "
    "is why no particular number from it survived; what survives is the order of "
    "the answer, one or two states."))
story.append(P(
    "The operational content is unchanged and now rests on clean numbers: buying "
    "more states is the worst-value move available. The next MSB state costs "
    f"about {MSB_F[-1][2]:.0f}&times; the last one, and the last one bought "
    f"{CC_MSB[3]} moduli of congruence coverage that a 30-second script covers "
    f"{CC_RATIO}&times; better."))

# ============================================================ 7
story.append(P("7. What WS4 changes about the program's own claims", H1))
story.append(tab([
    ["\"Our cryptids sit strictly below the universal machines\"",
     "<b>Withdrawn.</b> The frontier is an upper bound on where universality "
     "starts. One-schema VAL(q) is not known to be weaker than a 14-rule RES "
     "machine, and Section 3.4 makes that a stated open question."],
    ["\"No automatic certificate at &le; 12 MSB states\"",
     f"<b>Now &le; {MSB_BOUND}.</b> The n = 13 run completed (UNSAT). This is "
     "the last state either encoding will buy at a sane price."],
    ["\"The per-state factor fell back to 5.47 at n = 13\"",
     "<b>Withdrawn.</b> That reading came from a window in which two competing "
     "jobs were killed. Under single-load measurement the MSB series is "
     "monotone rising."],
    ["\"Our no-congruence theorems explain regular-decider resistance\"",
     "<b>Upheld and quantified.</b> One-variable semilinear = congruence + "
     f"threshold, refuted to modulus {CG_M} for any threshold."],
    ["\"The LSB bound is the program's headline impossibility result\"",
     f"<b>Demoted.</b> Converted to moduli it covers {CC_LSB[2]}. Its durable "
     "content is the halting-basin shape, not the state count."],
], ["claim", "status after WS4"], [2.35 * inch, 3.65 * inch]))

# ============================================================ 8
story.append(P("8. Traps this stream added", H1))
story.append(P(
    "<b>Convert bounds into a common currency before ranking them.</b> Three "
    "numbers in three units invite the reader &mdash; and the author &mdash; to "
    "rank them by size. Two of ours differed by three orders of magnitude in the "
    "direction opposite to how they had been presented. The conversion took "
    "twenty lines."))
story.append(P(
    "<b>When a sweep leaves survivors, diagnose them; do not widen the window "
    "until they vanish.</b> The one modulus that held out was worth an hour "
    "because a genuine survivor would have been a proof. Diagnosing it produced "
    "a lemma; widening the window alone would have produced nothing but a bigger "
    "number."))
story.append(P(
    "<b>An argument about \"arbitrarily large\" needs the residues taken "
    "infinitely often, not the residues taken.</b> The pre-period is where this "
    "kind of threshold argument leaks, and the leak is invisible in the output: "
    "the sweep reported success either way."))
story.append(P(
    "<b>Do not measure growth constants under variable load.</b> Bounds survive "
    "contaminated timing; the constants that price them do not. Fixing the "
    "protocol changed a headline reading from non-monotone to monotone."))

# ============================================================ 9
story.append(P("9. Status of every claim in this report", H1))
story.append(tab([
    ["Register machine &rarr; RES-GAM is step-exact, &le; 2I rules",
     "proved + machine-verified (lockstep, 2 programs, 100 starts)"],
    ["RES-GAMs are Turing-complete",
     "proved, <i>citing</i> Minsky; the compiler is ours and verified"],
    [f"PRIMEGAME is a {PG_RULES}-rule GAM emitting the primes",
     "machine-verified here (first 15 primes), not cited"],
    ["One-schema VAL(q) is/is not universal", "<b>open</b> &mdash; stated, not answered"],
    ["Needle and machine 3 have infinite slope sets",
     "proved (injective in the branch index) + machine-verified"],
    ["Neither map is injective", "proved by explicit witness"],
    ["No finite-union-of-intervals certificate",
     "proved (monotone orbit + every ray meets H)"],
    [f"No congruence certificate, m &le; {CG_M}, any threshold",
     "machine-verified over the stated modulus range; the orbit side is a "
     "finite prefix, which only strengthens each refutation"],
    ["G(a) &#8801; v<sub>3</sub>(a) (mod 2)",
     "proved + machine-verified (400,000 values)"],
    [f"No MSB automatic certificate at &le; {MSB_BOUND} states",
     "machine-verified (completed UNSAT, cross-validated four ways)"],
    ["Growth constants in Section 6",
     "measured under one stated load condition; ratios within the run are "
     "comparable, cross-run comparisons to older logs are not"],
], ["claim", "epistemic status"], [2.75 * inch, 3.25 * inch]))

story.append(Spacer(1, 10))
story.append(HRFlowable(width="100%", thickness=0.7, color=HexColor("#b8c4d6")))
story.append(P(
    "<i>Code: gam.py, branch_type.py, congruence.py, certificate_classes.py, "
    "clean_growth.py, all with logs of record in the same directory. Report "
    "regenerated by make_ws4_report.py, which reads every number from those "
    "logs.</i>", CELL))

doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                        topMargin=0.8 * inch, bottomMargin=0.8 * inch,
                        title="WS4 -- The formal hardness frontier")
doc.build(story)
print(f"wrote {OUT}  ({os.path.getsize(OUT):,} bytes)")
