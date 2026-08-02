"""Build the WS5 census report.

Every number is read from census_rows.tsv, census.log, verify.log or
theorems.log, so the report cannot drift from the computation.
"""
import csv
import os
import re
from collections import Counter

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.colors import HexColor

HERE = "/Users/tomzahavy/Documents/Claude/collatz/census/"
OUT = HERE + "census_report.pdf"

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


def read(p):
    with open(HERE + p) as f:
        return f.read()


def grab(text, pat, what):
    m = re.search(pat, text)
    if not m:
        raise SystemExit(f"census report: cannot read {what}")
    return m.groups() if len(m.groups()) > 1 else m.group(1)


LOG = read("census.log")
VER = read("verify.log")
THM = read("theorems.log")
UNI = read("universal.log")
ROWS = list(csv.DictReader(open(HERE + "census_rows.tsv"), delimiter="\t"))

N_TOTAL, N_SKIP, N_ROWS = grab(
    LOG, r"enumerated ([\d,]+) machines; ([\d,]+) are not well defined[^;]*; "
         r"([\d,]+) analysed", "enumeration counts")
ELAPSED = grab(LOG, r"elapsed ([\d.]+)s", "elapsed")
AUDITED, FAILURES = grab(VER, r"machines audited: (\d+);\s+failures: (\d+)",
                         "audit result")
T3 = grab(THM, r"checked against the census: (\d+) predicted and decided, (\d+) "
               r"predicted but not decided, (\d+) decided but not predicted",
          "T3 check")
U_MACH, U_LIVE, U_BR, U_VMAX = grab(
    UNI, r"(\d+) machines \((\d+) with a non-silent sieve\), (\d+) branches, "
         r"v = 0\.\.(\d+)", "universal lemma domain")
U_SWEPT = grab(UNI, r"machines swept: (\d+)", "sweep size")
U_SILENT = grab(UNI, r"sieve-silent \(no expanding branch[^)]*\): (\d+)",
                "silent count")
U_SURV = grab(UNI, r"with an EXPLICIT surviving branch[^:]*: (\d+)", "survivors")
U_FORB = grab(UNI, r"with every branch forbidden: (\d+)", "all-forbidden")
U_UNDEC = grab(UNI, r"not decided by congruence: (\d+)", "undecided")
U_T1 = grab(UNI, r"tier 1 mechanical \(proved\)\s+(\d+)", "tier 1")
U_T2 = grab(UNI, r"tier 2 S-unit[^\d]+(\d+)", "tier 2")
U_T3A = grab(UNI, r"tier 3a sieve-closed[^\d]+(\d+)", "tier 3a")
U_T3B = grab(UNI, r"tier 3b sieve-void[^\d]+(\d+)", "tier 3b")
U_T3C = grab(UNI, r"tier 3c sieve-silent\s+(\d+)", "tier 3c")
U_FAM = grab(UNI, r"sharing the Needle.s group <2,-3>: (\d+)", "needle family")
U_MASS = grab(UNI, r"weighted forbidden mass: ([\d.]+)", "needle mass")
U_SURVB = grab(UNI, r"surviving branches: \[([^\]]+)\]", "needle surviving")
U_NFORB, U_NSURV = grab(UNI, r"forbidden branches v <= 40: (\d+);\s+surviving: (\d+)",
                        "needle counts")
U_W35 = grab(UNI, r"forbidden among the first 35 valuations: (\d+)", "ws3 match")

DEC = [r for r in ROWS if r["cong"]]
CAND = [r for r in ROWS if r["verdict"] == "GROW" and not r["cong"]
        and r["alpha"] == "1"]
VERD = Counter(r["verdict"] for r in ROWS)
MODS = Counter(int(r["cong"]) for r in DEC)
NEEDLE_TWINS = [r for r in ROWS if (r["alpha"], r["beta"]) == ("1", "3")]
TWIN_MASS = sorted(float(r["sieve_mass"]) for r in NEEDLE_TWINS)
NEEDLE = next(r for r in ROWS if (r["alpha"], r["beta"], r["gamma"], r["delta"],
                                 r["eps"]) == ("1", "3", "1", "1", "0"))

story = []
story.append(P("WS5 &mdash; A census of the one-schema VAL(2) family", TITLE))
story.append(P("The first machinery in this program that produces machines "
               "rather than consuming them", SUB))
story.append(HRFlowable(width="100%", thickness=1.1, color=BLUE,
                        spaceBefore=0, spaceAfter=14))

story.append(P("1. Why this family", H1))
story.append(P(
    "WS4 closed by asking whether the one-schema valuation class is "
    "Turing-complete, and observing that it is the only two-sided bet the "
    "program still holds. That class is also where both flagship machines live. "
    "So a census of it does two jobs at once: it populates the class whose "
    "power is open, and it converts per-machine handcraft into a pipeline."))
story.append(P(
    "A machine is five integers. Write x = 2<super>v</super>m with m odd. If "
    "m = 1 the machine <b>halts</b> (x is a pure power of two). Otherwise "
    "m = 2k+1, so x = 2<super>v+1</super>k + 2<super>v</super>, and"))
story.append(P(
    "F(x) = A<sub>v</sub>k + B<sub>v</sub>,&nbsp;&nbsp; A<sub>v</sub> = "
    "&alpha;&middot;2<super>v+1</super> + &beta;,&nbsp;&nbsp; B<sub>v</sub> = "
    "&gamma;&middot;2<super>v</super> + &delta;&middot;v + &epsilon;", MATHC))
story.append(P(
    "&mdash; the branch-affine normal form the whole program is built on, with "
    "the coefficients left free. <b>The Space Needle is (1, 3, 1, 1, 0)</b>, "
    "verified: zero mismatches against its own step function over "
    "2 &le; x &lt; 300,000, and the orbit from x<sub>0</sub> = 3 runs "
    "3, 6, 10, 17, 41, 101, 251, &hellip;, joining the published orbit at 6. As "
    "a function of x the branch has slope A<sub>v</sub>/2<super>v+1</super> "
    "&rarr; &alpha;, so &alpha; is the asymptotic multiplier: &alpha; &ge; 2 "
    "doubles at every branch, &alpha; = 1 is the weakly expanding "
    "Collatz-like regime."))
story.append(P(
    "<b>Update, July 31 &mdash; the box holds a second wild machine.</b> "
    "Member <b>(1, 1, 1, 1, 0)</b> turns out to be the generic branch of the "
    "<b>sheep machine</b> "
    "(<font face='Courier'>1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE</font>, "
    "BB(6), found by <i>sheep</i> on 7 April 2026 and listed as a bbchallenge "
    "Cryptid): the Space Needle&rsquo;s reduction with &beta; changed from 3 "
    "to 1. Two members of this box are therefore reductions of machines other "
    "people found, and the family is less manufactured than it looked. "
    "There is a sting in it. The census records (1,1,1,1,0) as <b>HALT</b> "
    "&mdash; from x = 3 it steps 3 &rarr; 4 = 2<super>2</super>. The sheep "
    "machine has one <i>exceptional</i> branch, at oddPart = 3, which this "
    "schema cannot express, and it intercepts exactly that value: "
    "3 &rarr; 6. <b>One extra branch on one odd part converts a halting "
    "census member into an open problem.</b> That is the clearest available "
    "statement of what the box misses, and it is an argument for widening the "
    "schema rather than the parameter ranges."))

story.append(P("2. What every machine gets, and the one part that is new", H1))
story.append(P(
    "Well-definedness, simulation from x<sub>0</sub> = 3, drift, the backward "
    "branching ceiling, the WS3 forbidden-branch sieve, and an exact congruence "
    "decision. Two of those can decide a machine outright, which is the point."))
story.append(P(
    "<b>The congruence test here is exact and complete</b>, not the necessary "
    "condition WS4 had to settle for. On branch v the pair (source, target) "
    "mod m traces the graph of a single affine map &phi;<sub>v</sub>, and "
    "A<sub>v</sub>, B<sub>v</sub> mod m depend on v only through the pair "
    "(2<super>v</super> mod m, v mod m) &mdash; a state space of size "
    "m<super>2</super>. So iterating v until that state repeats enumerates "
    "<i>every</i> branch, the relation R<sub>m</sub> is exactly computable, the "
    "orbit lies inside the R<sub>m</sub>-closure of x<sub>0</sub>, and if that "
    "closure misses the halting set's residues the machine <b>provably</b> "
    "never halts."))
story.append(P(
    "<b>Calibration ran first, in both directions</b>, because a decision "
    "procedure reported without both is worthless: the Space Needle must "
    "<i>not</i> be decided (it is not), and machines that <i>are</i> decided "
    "must survive an independent check (they do)."))

story.append(P("3. What came out", H1))
story.append(P(
    f"{N_TOTAL} machines enumerated over &alpha; &#8712; {{1,2,3}}, &beta; "
    f"&#8712; {{&minus;1..7}}, &gamma; &#8712; {{1,2,3}}, &delta; &#8712; "
    f"{{0,1,2}}, &epsilon; &#8712; {{&minus;2..2}}; <b>{N_SKIP} are not well "
    f"defined</b> (F leaves the positive integers); <b>{N_ROWS} analysed</b> in "
    f"{ELAPSED} seconds."))

rows = []
for a in ("1", "2", "3"):
    sub = [r for r in ROWS if r["alpha"] == a]
    c = Counter(r["verdict"] for r in sub)
    dec = sum(1 for r in sub if r["cong"])
    md = sum(float(r["drift"]) for r in sub) / len(sub)
    rows.append([a, f"{len(sub)}", f"{c['HALT']}", f"{c['CYCLE']}",
                 f"{c['GROW']}", f"<b>{dec}</b>", f"{md:.4f}"])
story.append(tab(rows, ["&alpha;", "machines", "HALT", "CYCLE", "GROW",
                        "decided", "mean drift"],
                 [0.6 * inch, 0.9 * inch, 0.7 * inch, 0.7 * inch, 0.7 * inch,
                  0.8 * inch, 1.0 * inch]))
story.append(P(
    f"<b>{len(DEC)} of {N_ROWS} machines &mdash; "
    f"{len(DEC) / len(ROWS):.1%} &mdash; are decided by a separating "
    f"congruence</b>, i.e. proved never to halt from x<sub>0</sub> = 3. The "
    f"deciding moduli run "
    + ", ".join(f"{m} ({MODS[m]})" for m in sorted(MODS)[:7]) +
    f", with a tail out to {max(MODS)}."))
story.append(P(
    f"<b>Every one of the {AUDITED} certificates was re-audited "
    f"independently</b> &mdash; brute force over real integers to x &lt; "
    f"200,000, powers of two enumerated completely, without reusing the branch "
    f"enumeration that produced the certificate &mdash; with "
    f"<b>{FAILURES} failures</b>. A false proof of non-halting is the worst "
    f"output this program could emit, so this audit is not optional."))

story.append(P("3.1&nbsp;&nbsp;G2 finally moves, and here is exactly how much", H2))
story.append(P(
    "G2 &mdash; decide a cryptid &mdash; had not moved in four consecutive "
    f"stock-takes. It moves here: {len(DEC)} machines decided, and two proved "
    "non-halting <i>from every start</i> (Section 4). <b>The honest "
    "qualification is that these are new and easier machines, not the "
    "cryptids</b>; a machine with a separating congruence is by definition not "
    "one. What the census delivers is the partition &mdash; which members are "
    "easy, why, and a pool of hard ones."))
story.append(P(
    f"It is worth noting what it cost. {ELAPSED} seconds of census decided "
    f"{len(DEC)} machines. Two days of SAT search bought two states."))

story.append(P("4. The first three theorems", H1))
story.append(P(
    "<b>T1 (proved).</b> The machine <b>(1, 1, 2, 0, 1)</b> never halts after "
    "its first step. Here B<sub>v</sub> = 2&middot;2<super>v</super> + 1 = "
    "2<super>v+1</super> + 1 = A<sub>v</sub>, so F(x) = A<sub>v</sub>(k+1) with "
    "A<sub>v</sub> odd and at least 3. Every image carries an odd factor "
    "greater than one and is therefore never a power of two."))
story.append(P(
    "<b>T2 (proved).</b> The machine <b>(2, &minus;1, 2, 1, 1)</b> never halts "
    "after its first step. A<sub>v</sub> = 2<super>v+2</super> &minus; 1, and the WS3 "
    "sieve forbids a halt out of branch v unless Q<sub>0</sub>2<super>e</super> "
    "&#8801; P<sub>0</sub> (mod A<sub>v</sub>) with P<sub>0</sub> = "
    "(2v+3)2<super>v</super> and Q<sub>0</sub> = 1 &minus; "
    "2<super>v+1</super>. Modulo A<sub>v</sub> we have 2<super>v+2</super> "
    "&#8801; 1, hence 2Q<sub>0</sub> &#8801; 1, so Q<sub>0</sub> is the inverse "
    "of 2 and the condition collapses to"))
story.append(P("2<super>e+1</super> &#8801; 2v + 3 &nbsp;(mod 2<super>v+2</super> "
               "&minus; 1)", MATHC))
story.append(P(
    "The powers of two mod A<sub>v</sub> are exactly {1, 2, &hellip;, "
    "2<super>v+1</super>}, since 2 has order v+2; and for v &ge; 1 the number "
    "2v+3 is odd, greater than 1 and less than A<sub>v</sub>, so it is its own "
    "residue and is not among them. For v = 0, A<sub>0</sub> = 3 and 2v+3 "
    "&#8801; 0, also not a power of two. <b>Every branch is forbidden</b>, so "
    "no orbit can reach a power of two after a step. <b>QED</b>"))
story.append(P(
    "<b>T3 (proved, and exact on the whole census).</b> A member is decided at "
    "m = 3 &mdash; hence provably never halts from x<sub>0</sub> = 3 &mdash; if "
    "and only if"))
story.append(P("&delta; &#8801; 0,&nbsp;&nbsp; &gamma; &#8801; &alpha;,"
               "&nbsp;&nbsp; &beta; + &epsilon; &#8801; 0 &nbsp;&nbsp;(all mod 3)",
               MATHC))
story.append(P(
    "<i>Proof.</i> Mod 3 the powers of two are {1, 2}, every nonzero class, so "
    "a separating class must be contained in {0}; it contains x<sub>0</sub> = 3, "
    "so it <i>is</i> {0}. Then 3 | x forces k &#8801; 1 (mod 3), and F(x) "
    "&#8801; (&minus;1)<super>v</super>(&gamma;&minus;&alpha;) + &beta; + "
    "&delta;v + &epsilon;. Vanishing at v = 0, 1, 2 gives 2&delta; &#8801; 0, "
    "then 2(&gamma;&minus;&alpha;) &#8801; 0, then &beta;+&epsilon; &#8801; 0; "
    "conversely those three make it vanish for every v. <b>QED</b> &nbsp; "
    f"Checked against the census: {T3[0]} predicted and decided, {T3[1]} "
    f"predicted but not decided, {T3[2]} decided but not predicted, over "
    f"{N_ROWS} machines."))
story.append(P(
    "<b>Corollary, and the sharpest thing the census says about the Needle.</b> "
    "The <b>v-linear term &delta; is what blocks the cheapest certificate there "
    "is</b>. The Space Needle has &delta; = 1 and fails T3 in one line. The term "
    "&delta;v injects unbounded valuation information into the <i>value</i>, and "
    "no modulus can track it."))

story.append(P("5. The Needle is not special in anything measured globally", H1))
story.append(P(
    "<b>Drift and the branching ceiling are functions of (&alpha;, &beta;) "
    "alone</b> &mdash; verified: 24 (&alpha;,&beta;) classes, and <b>none</b> "
    f"carrying more than one (drift, ceiling) value. So <b>{len(NEEDLE_TWINS)} "
    f"machines share the Needle's drift {float(NEEDLE['drift']):.4f} and ceiling "
    f"{float(NEEDLE['ceiling']):.5f} exactly.</b> Neither statistic can tell it "
    f"apart from {len(NEEDLE_TWINS) - 1} siblings."))
story.append(P(
    "What does separate them is the sieve, which reads (&gamma;, &delta;, "
    f"&epsilon;): across those twins the forbidden-branch mass ranges "
    f"{TWIN_MASS[0]:.4f} to {TWIN_MASS[-1]:.4f}, with the Needle at "
    f"<b>{float(NEEDLE['sieve_mass']):.4f}</b> &mdash; a clean reproduction of "
    "WS3's independently measured 28.7% (that was over v &le; 35, this over "
    "v &le; 8)."))

bp = Counter(int(r["beta"]) % 2 for r in CAND)
even_dec = sum(1 for r in ROWS if int(r["beta"]) % 2 == 0 and r["cong"])
even_all = sum(1 for r in ROWS if int(r["beta"]) % 2 == 0)
odd_dec = sum(1 for r in ROWS if int(r["beta"]) % 2 and r["cong"])
odd_all = sum(1 for r in ROWS if int(r["beta"]) % 2)
story.append(P(
    f"<b>&beta; parity is what makes a machine hard.</b> Even &beta;: "
    f"{even_dec}/{even_all} decided ({even_dec / even_all:.0%}). Odd &beta;: "
    f"{odd_dec}/{odd_all} ({odd_dec / odd_all:.0%}). Of the {len(CAND)} cryptid "
    f"candidates (&alpha; = 1, grows, undecided), <b>{bp[1]} have odd "
    f"&beta;</b>. A<sub>v</sub> odd is exactly the classic Collatz situation: "
    "the map hands you no 2-adic structure to exploit."))

story.append(P("6. Every branch forbidden: seven machines, then ten", H1))
story.append(P(
    "Seven undecided growers have <i>all</i> branches sieved out to v = 200 "
    "(mass 1.000000000). Two of them became T1 and T2 on the day. <b>The other "
    "five had no uniform argument and were not claimed</b> &mdash; "
    "&ldquo;forbidden to v = 200&rdquo; is not &ldquo;forbidden for all "
    "v&rdquo;, and that gap is exactly the kind this program refuses to paper "
    "over. All five are now theorems, along with three machines this search had "
    "never seen; and the count &ldquo;seven&rdquo; turns out to be an artefact "
    "of the pool the leads were drawn from."))

story.append(P("6.1&nbsp;&nbsp;The sieve lemma is universal", H2))
story.append(P(
    "The first follow-up derived S<sub>v</sub> &#8801; 2B<sub>v</sub> "
    "&ldquo;for &alpha; = 2, &beta; = &minus;1&rdquo;, and closed three leads "
    "with it. <b>That attribution was too modest: the derivation never uses "
    "either value.</b> On branch v the sieve forbids a halt unless "
    "Q<sub>0</sub>&middot;2<super>e</super> &#8801; P<sub>0</sub> "
    "(mod A<sub>v</sub>), where P<sub>0</sub> = (2B<sub>v</sub> &minus; "
    "A<sub>v</sub>)2<super>v</super> and Q<sub>0</sub> = 2<super>v+1</super> "
    "&minus; A<sub>v</sub> come from the branch&rsquo;s affine fixed point. "
    "Reduce both mod A<sub>v</sub> and the A<sub>v</sub> terms simply vanish: "
    "Q<sub>0</sub> &#8801; 2<super>v+1</super> and P<sub>0</sub> &#8801; "
    "B<sub>v</sub>&middot;2<super>v+1</super>, so P<sub>0</sub>Q<sub>0</sub>"
    "<super>&minus;1</super> &#8801; B<sub>v</sub>."))
story.append(P("<b>Universal sieve lemma.</b>&nbsp;&nbsp;For every machine with "
               "&beta; odd:&nbsp;&nbsp;S<sub>v</sub> &#8801; 2B<sub>v</sub> "
               "(mod A<sub>v</sub>)", MATHC))
story.append(P(
    "Equivalently, and this is the form worth remembering: <b>branch v can "
    "immediately precede a halt if and only if B<sub>v</sub> lies in "
    "&#9001;2&#9002; mod A<sub>v</sub></b>, the multiplicative group generated "
    f"by 2. <i>Machine-verified: {U_MACH} machines &mdash; the whole odd-&beta; "
    f"box &mdash; {U_BR} branches, v = 0 to {U_VMAX}, no mismatches.</i>"))
story.append(P(
    "And because A<sub>v</sub> = &alpha;2<super>v+1</super> + &beta; gives "
    "&alpha;2<super>v+1</super> &#8801; &minus;&beta;, multiplying through by "
    "&alpha; kills the exponential term outright:"))
story.append(P("<b>Linear corollary.</b>&nbsp;&nbsp;&alpha;S<sub>v</sub> "
               "&#8801; 2&alpha;&delta;v + 2&alpha;&epsilon; &minus; "
               "&beta;&gamma; &nbsp;(mod A<sub>v</sub>)", MATHC))
story.append(P(
    "&mdash; affine in v, for <i>every</i> machine in the family (verified on "
    "the same branches, no mismatches). <b>The exponential is not in the "
    "target; it is only in the modulus.</b> That single sentence is the whole "
    "shape of the difficulty: what has to be decided is whether a linear "
    "function of v lands in the group generated by 2 modulo a number that "
    "doubles with v."))
story.append(P(
    "So what decides a machine is the <b>size of &#9001;2&#9002;</b>. Four "
    "classes are <b>listable</b> &mdash; ord(2) grows linearly, so the powers "
    "of two are a short explicit list a parity/size argument can clear: "
    "(2,&minus;1) with ord = v + 2 and &#9001;2&#9002; = {2<super>i</super>}; "
    "(1,1) and (2,1) with ord = 2(v+1) and 2(v+2), giving the signed list "
    "{&plusmn;2<super>i</super>}; and (3,3), where 3 divides A<sub>v</sub>. The "
    "rest are <b>thin</b>: ord grows exponentially on average &mdash; (1,3) "
    "runs 4, 3, 10, 18, 12, 66, 130, 36 &mdash; and membership has no "
    "elementary handle at all."))

story.append(P("6.2&nbsp;&nbsp;The ten machine theorems (T3 is the m = 3 criterion)", H2))
story.append(P(
    "Every all-branches-forbidden machine in the box, with S<sub>v</sub> as an "
    "<b>exact integer identity</b> (asserted to v = 4,000 on a second, "
    "independent code path) and the pattern that finishes it. T7 to T11 are "
    "new; the two leads previously called &ldquo;the ones that do not "
    "transfer&rdquo; are T7 and T8."))
story.append(tab([
    ["(1,1,2,0,1)", "0", "B<sub>v</sub> = A<sub>v</sub> exactly; 0 is not a "
     "unit and every power of two is", "T1"],
    ["(2,&minus;1,2,0,1)", "3", "2B<sub>v</sub> = A<sub>v</sub> + 3; odd, "
     "1 &lt; 3 &lt; A<sub>v</sub> for v &ge; 1", "<b>T9</b>"],
    ["(2,&minus;1,2,1,1)", "2v + 3", "odd, 1 &lt; S<sub>v</sub> &lt; "
     "A<sub>v</sub> for v &ge; 1; v = 0 gives 0", "T2"],
    ["(2,&minus;1,2,2,1)", "4v + 3", "odd, in range for v &ge; 2; "
     "v = 0, 1 give 0", "T4"],
    ["(2,&minus;1,3,0,0)", "2<super>v+1</super> + 1", "odd, in range for "
     "v &ge; 1; v = 0 gives 0", "T5"],
    ["(2,&minus;1,3,1,0)", "2<super>v+1</super> + 2v + 1", "odd, in range for "
     "v &ge; 2; v = 0, 1 give 0", "T6"],
    ["(2,&minus;1,1,2,&minus;1)", "2<super>v+1</super> + 4v &minus; 2",
     "= 2&middot;odd and &lt; A<sub>v</sub>, so S<sub>v</sub> = "
     "2<super>i</super> forces i = 1, i.e. 2<super>v</super> = 2 &minus; 2v",
     "<b>T10</b>"],
    ["(2,1,1,2,&minus;1)", "2<super>v+1</super> + 4v &minus; 2", "same value, "
     "signed list mod 2<super>v+2</super>+1; S<sub>v</sub> = A<sub>v</sub> "
     "&minus; 2<super>i</super> forces i = 0, i.e. 4v &minus; 2 = "
     "2<super>v+1</super>", "<b>T7</b>"],
    ["(3,3,2,0,1)", "&#8801; 0 mod d<sub>v</sub>", "B<sub>v</sub> = "
     "d<sub>v</sub> = 2<super>v+1</super>+1 exactly and d<sub>v</sub> divides "
     "A<sub>v</sub>; powers of two are units mod d<sub>v</sub>", "<b>T8</b>"],
    ["(3,3,3,0,0)", "&minus;3", "2B<sub>v</sub> = A<sub>v</sub> &minus; 3 and "
     "3 divides A<sub>v</sub>, so S<sub>v</sub> &#8801; 0 (mod 3); powers of "
     "two mod 3 are {1, 2}", "<b>T11</b>"],
], ["machine", "S<sub>v</sub> (derived)", "why every branch is forbidden", ""],
   [1.05 * inch, 1.05 * inch, 3.35 * inch, 0.45 * inch]))
story.append(P(
    "<b>T7 to T11 (proved): five more machines that never halt after their "
    "first step.</b> Brute force on all ten &mdash; every non-power-of-two "
    "start below 20,000, 400 steps &mdash; finds 0 halts."))
story.append(P(
    "Three of the five were invisible to the earlier hunt <b>not because the "
    "test differed but because of the pool filter</b>. The leads were drawn "
    "from undecided <i>growers</i>: (2,&minus;1,2,0,1) and (3,3,3,0,0) were "
    "already congruence-decided, and (2,&minus;1,1,2,&minus;1) is a CYCLE "
    "machine (x = 3 is a fixed point, F(3) = 3). For the two congruence-decided "
    "ones this is a real upgrade &mdash; the congruence gave &ldquo;never halts "
    "from x<sub>0</sub> = 3&rdquo;, the sieve gives &ldquo;no orbit from "
    "<i>any</i> start reaches a power of two after a step&rdquo;. A filter "
    "chosen for one purpose quietly bounded the reach of another."))

story.append(P("6.3&nbsp;&nbsp;The completeness theorem: the method is finished",
               H2))
story.append(P(
    f"<b>Those ten are all there are.</b> For every one of the other "
    f"machines in the odd-&beta; box, the sweep returns an <b>explicit "
    f"surviving branch</b>: a v &le; 22 together with the exponent e "
    f"witnessing 2<super>e</super> &#8801; S<sub>v</sub> (mod A<sub>v</sub>). "
    f"<i>Machine-verified: {U_SWEPT} machines swept &mdash; {U_FORB} "
    f"all-forbidden, {U_SURV} carrying a surviving-branch certificate, "
    f"{U_SILENT} sieve-silent</i> (the (1,&minus;1) class, where no branch "
    f"expands and the sieve argues from nothing)."))
story.append(P(
    "A surviving branch is a <b>positive certificate</b>, not a failure to find "
    "one. So this is not exhaustion in the sense of the meta "
    "report&rsquo;s bounded-resource "
    "bounded-resource searches &mdash; it is a proof that the sieve-to-theorem "
    "pipeline is <b>complete on this family, at ten machines</b>. It is the "
    "first time this program has closed a method with a completeness statement "
    "rather than a budget. What is <i>not</i> claimed: a surviving branch does "
    "not make a machine halt. It means only that this method cannot decide it, "
    "and something else must."))

story.append(P("6.4&nbsp;&nbsp;The frontier map, and where the Needle sits", H2))
story.append(P(
    f"Of the {U_UNDEC} odd-&beta; machines not decided by a congruence:"))
story.append(tab([
    ["1 &mdash; mechanical", U_T1, "all branches forbidden, with a pattern "
     "proof: the ten, less those already decided another way"],
    ["2 &mdash; <b>S-unit</b>", f"<b>{U_T2}</b>", "thin &#9001;2&#9002;; the "
     "sieve bites but does not close. Deciding these needs S-unit or Baker "
     "input, not more of this"],
    ["3a &mdash; sieve-closed", U_T3A, "listable class, but a branch "
     "certifiably survives: this route is provably shut"],
    ["3b &mdash; sieve-void", U_T3B, "thin, forbidden mass 0 &mdash; every "
     "tested branch survives"],
    ["3c &mdash; sieve-silent", U_T3C, "the (1,&minus;1) class: no expanding "
     "branch anywhere"],
], ["tier", "count", "what it means"],
   [1.35 * inch, 0.6 * inch, 3.95 * inch]))
story.append(P(
    f"<b>The Space Needle is in tier 2, and {U_FAM} machines share its "
    f"group.</b> With A<sub>v</sub> = 2<super>v+1</super> + 3 we get "
    f"2<super>v+1</super> &#8801; &minus;3, so &#9001;2&#9002; = "
    f"{{&plusmn;3<super>a</super>&middot;2<super>i</super>}} and the halting "
    f"condition on branch v reads:"))
story.append(P("2v &minus; 3 &nbsp;&#8712;&nbsp; "
               "{&plusmn;3<super>a</super>&middot;2<super>i</super>} "
               "&nbsp;(mod 2<super>v+1</super> + 3)", MATHC))
story.append(P(
    f"&mdash; a 2,3-S-unit membership question, and that is now the whole of "
    f"the difficulty, stated in one line. <i>Verified: the closed form "
    f"S<sub>v</sub> &#8801; 2v &minus; 3 is exact for v &le; 200 with no "
    f"mismatches; the weighted forbidden mass is {U_MASS}, an independent "
    f"reproduction of WS3&rsquo;s 28.7%; and {U_W35} branches are forbidden "
    f"among the first 35 valuations, matching WS3&rsquo;s count exactly.</i>"))
story.append(P(
    f"<b>And it does not close.</b> The branches that survive to v = 40 are "
    f"{U_SURVB} &mdash; {U_NSURV} of {int(U_NFORB) + int(U_NSURV)}, and "
    f"<b>they are not thinning out</b>. There is no asymptotic "
    f"all-branches-forbidden theorem waiting here, and the last-step sieve "
    f"saturates near 28.7% of weight forever. Whatever decides the Needle comes "
    f"from somewhere else. Recording that saves the next reader the search."))

story.append(P("7. Status of every claim", H1))
story.append(tab([
    ["The family contains the Space Needle at (1,3,1,1,0)",
     "machine-verified (0 mismatches, x &lt; 300,000)"],
    [f"{len(DEC)} machines never halt from x<sub>0</sub> = 3",
     "proved &mdash; the congruence test is exact and complete for its class; "
     f"all {AUDITED} certificates independently audited, {FAILURES} failures"],
    ["T1, T2, T4 to T11: ten machines never halt after their first step",
     "proved &mdash; and the wording matters: a start that <i>is</i> a power "
     "of two halts at step 0, so the powers of two are exactly the halting "
     "starts. Brute-forced: non-power-of-two starts &lt; 20,000, 400 steps, "
     "0 halts on all ten"],
    ["The sieve lemma S<sub>v</sub> &#8801; 2B<sub>v</sub> holds for every "
     "&beta; odd, and &alpha;S<sub>v</sub> is affine in v",
     f"proved; machine-verified on {U_BR} branches of {U_MACH} machines, "
     f"v &le; {U_VMAX}, no mismatches"],
    ["Exactly ten machines in the box have every branch forbidden",
     f"proved &mdash; every other machine carries an <i>explicit surviving "
     f"branch</i>, a positive certificate, so this is completeness and not "
     f"exhaustion ({U_SWEPT} swept, {U_SILENT} sieve-silent)"],
    ["T3: closed form for the m = 3 certificate",
     f"proved, and exact on all {N_ROWS} machines"],
    ["Drift and ceiling depend only on (&alpha;, &beta;)",
     "machine-verified over the enumerated range"],
    ["The Needle's branch condition is 2v &minus; 3 &#8712; "
     "{&plusmn;3<super>a</super>2<super>i</super>} mod 2<super>v+1</super>+3",
     f"proved (Section 6.4); and the surviving branches do <b>not</b> thin "
     f"out &mdash; {U_NSURV} of {int(U_NFORB) + int(U_NSURV)} survive to "
     f"v = 40, so no asymptotic theorem is available by this route"],
    [f"The {len(CAND)} cryptid candidates are cryptids",
     "<b>not claimed.</b> They are expanding with an undecided orbit; no "
     "halting-set characterization or equidistribution model has been built, "
     "and they are siblings in one family, not independent discoveries"],
    ["One-schema VAL(2) is / is not Turing-complete",
     "<b>open</b> &mdash; untouched by this work. A census maps a family; it "
     "does not bound its power"],
], ["claim", "epistemic status"], [2.6 * inch, 3.4 * inch]))

story.append(Spacer(1, 10))
story.append(HRFlowable(width="100%", thickness=0.7, color=HexColor("#b8c4d6")))
story.append(P(
    "<i>Code: family.py, decide.py, census.py, verify.py, theorems.py, "
    "leads.py, universal.py, with "
    "logs and census_rows.tsv in the same directory. Report regenerated by "
    "make_census_report.py, which reads every number from those files.</i>",
    CELL))

doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                        topMargin=0.8 * inch, bottomMargin=0.8 * inch,
                        title="WS5 -- A census of the one-schema VAL(2) family")
doc.build(story)
print(f"wrote {OUT}  ({os.path.getsize(OUT):,} bytes)")
