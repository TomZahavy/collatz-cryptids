"""Build the machine-3 report (A(a,b) system, the multiplicative cryptid)."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.colors import HexColor

OUT = "/Users/tomzahavy/Documents/Claude/collatz/machine3/machine3_halting_report.pdf"

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=styles["Heading1"], spaceBefore=18, spaceAfter=8)
H2 = ParagraphStyle("H2x", parent=styles["Heading2"], spaceBefore=14, spaceAfter=6)
BODY = ParagraphStyle("Bodyx", parent=styles["Normal"], fontSize=10.5,
                      leading=14.5, spaceAfter=7)
MATH = ParagraphStyle("Mathx", parent=styles["Normal"], fontName="Times-Italic",
                      fontSize=10.5, leading=15)
MATHC = ParagraphStyle("MathCx", parent=MATH, alignment=TA_CENTER,
                       spaceBefore=4, spaceAfter=8)
CELL = ParagraphStyle("Cellx", parent=styles["Normal"], fontName="Times-Italic",
                      fontSize=10, leading=13)
CELLR = ParagraphStyle("CellRx", parent=CELL, fontName="Times-Roman")
TITLE = ParagraphStyle("Titlex", parent=styles["Title"], fontSize=19,
                       leading=24, spaceAfter=4)
SUB = ParagraphStyle("Subx", parent=styles["Normal"], alignment=TA_CENTER,
                     textColor=colors.HexColor("#555555"), fontSize=11,
                     spaceAfter=18)
BLUE = HexColor("#1a3c6e")


def P(text, style=BODY):
    return Paragraph(text, style)


def tstyle(header=True):
    s = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c4d6")),
         ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
         ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
         ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if header:
        s += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef7")),
              ("ROWBACKGROUNDS", (0, 1), (-1, -1),
               [colors.white, colors.HexColor("#f6f8fb")])]
    else:
        s += [("ROWBACKGROUNDS", (0, 0), (-1, -1),
               [colors.white, colors.HexColor("#f6f8fb")])]
    return TableStyle(s)


def rtable(rows, header, widths, italic=None):
    italic = italic or set()
    data = [[P(f"<b>{h}</b>", CELLR) for h in header]]
    for r in rows:
        data.append([P(c, CELL if i in italic else CELLR)
                     for i, c in enumerate(r)])
    t = Table(data, colWidths=list(widths), repeatRows=1)
    t.setStyle(tstyle())
    return t


DEEP = "no halt in 3,000,000 composite steps, a exceeding 700,000 bits"

story = []
story.append(P("Machine 3: A Multiplicative-Coincidence Cryptid", TITLE))
story.append(P("The A(a, b) system &mdash; halting reduced to hitting an exact "
               "power of 3", SUB))

# 1
story.append(P("1. Overview", H1))
story.append(P(
    "Machine 3 is the deterministic system A(a, b) on positive-integer pairs "
    "defined by six guarded rules (Section 2), started at A(1, 1). It is the "
    "third machine in this collection, and it fills a gap the meta report "
    "predicted would eventually appear: a <b>multiplicative-coincidence</b> "
    "cryptid, the type of the bbchallenge machine Space Needle, where "
    "halting requires the orbit to land on an exact power rather than on a "
    "sparse affine family (machine 1) or to trip a cumulative walk "
    "(the Hydra family)."))
story.append(P(
    "The analysis is clean and largely complete except for the open core. "
    "<b>Halting is equivalent to a single, sharply stated event</b> (Theorem "
    "1): the a-coordinate must reach an exact power of 3 whose exponent is "
    "divisible by 3. The divide-chains that dominate the running time have a "
    "closed form (Theorem 2); an affine potential proves the machine cannot "
    "cycle (Theorem 3) &mdash; another machine in the collection to yield "
    "one, by the same recipe; and the branch statistic is the base-3 "
    "valuation law, the exact base-3 analogue of Collatz. Verified: no halt in 3,000,000 composite steps &mdash; the a-coordinate reaching 708,337 bits over 2,249,864 resets, and the orbit never once landing on a power of 3 (no a = 1 event at all). The machine almost certainly never halts, "
    "for the Space-Needle reason &mdash; but a proof would require deciding "
    "whether one orbit ever hits a power, which is exactly the open "
    "Collatz-type obstacle."))

# 2
story.append(P("2. The machine", H1))
story.append(P("State A(a, b), a &ge; 1, b &ge; 1. The rules (first match; "
               "k &ge; 1 and b &ge; 1 where written):"))
story.append(Spacer(1, 4))
story.append(rtable([
    ("R1", "A(1, 3k) &rarr; <b>halt</b>", "k &ge; 1", "b divisible by 3"),
    ("R2", "A(1, 3k+1) &rarr; A(3k+4, 1)", "&mdash;", "b = 1 (mod 3)"),
    ("R3", "A(1, 3k+2) &rarr; A(3k+3, 2)", "&mdash;", "b = 2 (mod 3)"),
    ("R4", "A(3k, b) &rarr; A(k, b + 2k + 1)", "k &ge; 1", "a = 0 (mod 3): divide"),
    ("R5", "A(3k+1, b) &rarr; A(4k + b + 3, 1)", "k &ge; 1", "a = 1 (mod 3): reset"),
    ("R6", "A(3k+2, b) &rarr; A(4k + b + 5, 1)", "&mdash;", "a = 2 (mod 3): reset"),
], ("#", "rule", "guard", "role"),
   (0.4 * inch, 2.6 * inch, 0.9 * inch, 2.4 * inch), italic={1}),)
story.append(Spacer(1, 6))
story.append(P(
    "Dispatch: a = 1 uses R1&ndash;R3 (on b mod 3); a &ge; 2 uses "
    "R4&ndash;R6 (on a mod 3). Two behaviors alternate. When a &ne; 0 "
    "(mod 3) the <b>reset</b> rules R5/R6 map a to roughly 4a/3, adding the "
    "current b and setting b back to 1. When a &#8801; 0 (mod 3) the "
    "<b>divide</b> rule R4 replaces a by a/3 and pumps b upward. Halting is "
    "possible only from a = 1, and only when b &#8801; 0 (mod 3)."))
story.append(P(
    "<b>Fidelity.</b> The implementation reproduces the hand-computed "
    "trajectory A(1,1) &rarr; A(4,1) &rarr; A(8,1) &rarr; A(14,1) &rarr; "
    "&hellip;, and the accelerated form (Section 4) matches the base machine "
    "state-for-state on the first 177,717 composite steps of the real orbit "
    "before it outruns the base horizon."))

# 3
story.append(P("3. The halting criterion", H1))
story.append(P(
    "The gateway to halting is a = 1, and a = 1 is reached only by the "
    "divide rule R4 grinding a down. R4 divides a by 3, so it reaches 1 "
    "<b>only from an exact power of 3</b>: if a = 3<super>j</super>&middot;M "
    "with M not divisible by 3, the divide chain stops at M, and M = 1 iff "
    "a was a pure power 3<super>j</super>. Section 4 (Theorem 2) gives the "
    "value of b there: b = 3<super>j</super> + j. Since 3<super>j</super> "
    "&#8801; 0 (mod 3) for j &ge; 1, b &#8801; j (mod 3), and R1 halts iff "
    "b &#8801; 0 (mod 3). Hence:"))
story.append(P(
    "<b>Theorem 1.</b> Started at A(1, 1), the machine halts <b>if and only "
    "if</b> the a-coordinate reaches an exact power of 3 whose exponent is "
    "divisible by 3:"))
story.append(P("a &#8712; {3<super>j</super> : j &#8801; 0 (mod 3)} = "
               "{27, 729, 19683, &hellip;} = {27<super>m</super> : m &ge; 1}.",
               MATHC))
story.append(P(
    "(Verified: for j = 1..15, placing the machine at (3<super>j</super>, 1) "
    "halts exactly when j &#8801; 0 mod 3.) This is the multiplicative "
    "analogue of machine 1&rsquo;s affine halting family: the "
    "target is a <b>geometric set of exact powers</b>, spaced by a factor of "
    "27, precisely the shape of Space Needle&rsquo;s power-of-2 target on "
    "the bbchallenge wiki &mdash; but with an added congruence (exponent "
    "&#8801; 0 mod 3) selecting one third of the powers."))

# 4
story.append(P("4. Acceleration and the potential", H1))
story.append(P("4.1&nbsp;&nbsp;Theorem 2: the divide-chain closed form", H2))
story.append(P(
    "The divide chain is the only expensive event. From (N, b<sub>0</sub>) "
    "with N = 3<super>j</super>&middot;M, M &ne; 0 (mod 3), applying R4 "
    "j times gives"))
story.append(P("(N, b<sub>0</sub>) &rarr; (M, b<sub>0</sub> + (N &minus; M) "
               "+ j),", MATHC))
story.append(P(
    "since level i adds 2(N/3<super>i</super>) + 1 and the geometric sum "
    "telescopes to (N &minus; M) + j. This collapses an O(N)-long chain to "
    "one jump (30,000 randomized checks). With it, the machine simulates to "
    "millions of composite steps in seconds. When M = 1 the state is "
    "A(1, N &minus; 1 + j) = A(1, 3<super>j</super> + j), which is where "
    "Theorem 1 reads off the halt."))
story.append(P("4.2&nbsp;&nbsp;Theorem 3: a monotone potential, no cycles", H2))
story.append(P(
    "<b>Theorem 3.</b> &Phi; = a + b increases by at least 1 at every "
    "non-halting step. <i>Proof.</i> R4 (divide) sends a + b = 3k + b to "
    "k + (b + 2k + 1) = 3k + b + 1, exactly +1. For the resets, b cancels: "
    "R5 gives &Phi; &rarr; (4(a&minus;1)/3 + b + 3) + 1, an increment of "
    "(a + 8)/3 &gt; 0; R6 gives (a + 10)/3 &gt; 0; and the a = 1 exits "
    "R2/R3 give +3 and +2. The minimum, 1, is attained by divides. "
    "<b>QED</b> (verified on ~358,000 transitions across ten orders of "
    "magnitude, and 300,000 steps of the true orbit)."))
story.append(P(
    "<b>Corollary.</b> The machine cannot cycle; from A(1, 1) it halts or "
    "escapes to infinity. This is another affine potential in the "
    "collection &mdash; alongside machine 1&rsquo;s &Phi; = 2b + d "
    "&mdash; and it was found the same way: look "
    "for an affine combination in which the reset rules&rsquo; fed-back "
    "variable cancels. The recipe now has a perfect record. As with the "
    "other two, this excludes the one scenario simulation can never rule "
    "out: an eventually-periodic orbit with an astronomically long "
    "transient (bbchallenge&rsquo;s Skelet #1)."))

# 5
story.append(P("5. Why it (almost certainly) never halts", H1))
story.append(P(
    "Two independent rarities protect the machine. First, reaching a = 1 at "
    "all requires the reset stream to produce an <b>exact power of 3</b> "
    "&mdash; a measure-zero coincidence, and in the deep run the orbit never "
    "hit one (no a = 1 event in 3,000,000 composite steps). Second, even a "
    "power of 3 only halts if its exponent is divisible by 3, killing two "
    "thirds of the already-rare hits."))
story.append(P(
    "The branch statistic makes the rarity quantitative. The depth j of each "
    "divide chain is the 3-adic valuation of a reset value, and it follows "
    "the geometric law"))
story.append(P("P(j) = (2/3)(1/3)<super>j&minus;1</super>&nbsp;&nbsp;&nbsp;"
               "(measured: 0.669, 0.219, 0.075, 0.025, &hellip; vs 0.667, "
               "0.222, 0.074, 0.025),", MATHC))
story.append(P(
    "the base-3 analogue of the coin-flip behind the Collatz heuristic. The a-orbit grows "
    "geometrically (about 0.48 bits per reset, roughly &times;4/3 from the "
    "reset map net of the divide losses), so it passes the target scale "
    "27<super>m</super> after O(m) resets. Modeling the reset values as "
    "arithmetically generic at their scale, the probability of landing "
    "exactly on 27<super>m</super> decays geometrically in m, so the "
    "expected number of hits is a convergent sum &mdash; a "
    "<b>divergent-type cryptid</b> in the collection&rsquo;s dichotomy: "
    "geometric growth outrunning a geometrically sparse target, exactly like "
    "machine 1 and Space Needle. Non-halting is overwhelmingly likely; a "
    "proof is not available, for the usual single-orbit reason."))

# 6
story.append(P("6. Status and verification", H1))
story.append(rtable([
    ("implementation vs base rules",
     "hand-derived prefix A(1,1)..A(14,1); accelerated form matches base "
     "state-for-state on 177,717 composite steps of the real orbit", "pass"),
    ("Theorem 1 (halting criterion)",
     "a = 3<super>j</super> halts iff j &#8801; 0 (mod 3), for j = 1..15; "
     "halting set {27<super>m</super>}", "pass"),
    ("Theorem 2 (divide-chain closed form)",
     "(N, b<sub>0</sub>) &rarr; (M, b<sub>0</sub> + (N&minus;M) + j) on "
     "30,000 constructed chains", "pass"),
    ("Theorem 3 (potential, no cycles)",
     "&Phi; = a + b increment &ge; 1 on ~358,000 transitions (min 1) and "
     "300,000 orbit steps", "pass"),
    ("branch statistic",
     "divide depth = 3-adic valuation, P(j) = (2/3)(1/3)<super>j&minus;1</super> "
     "to three decimals over 100,000 chains", "pass"),
    ("deep run", "3,000,000 composite steps from A(1,1), no halt; a reaches 708,337 bits; no power-of-3 (a = 1) event", "pass"),
], ("check", "scope", "result"),
   (1.75 * inch, 4.25 * inch, 0.7 * inch)))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=0.8, color=BLUE))
story.append(Spacer(1, 4))
story.append(P(
    "Artifacts: m3_base.py (the six rules), m3_accel.py (the composite step "
    "with batched divide-chains, self-verified against the base), "
    "m3_theorems.py (Theorems 1&ndash;3 and the measurements), "
    "make_report3.py (this report). <b>Status: open (divergent, "
    "multiplicative-coincidence cryptid); halts or escapes &mdash; "
    "periodicity excluded by proof.</b>",
    ParagraphStyle("Foot", parent=BODY, fontSize=9.5,
                   textColor=colors.HexColor("#555555"))))

doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                        topMargin=0.8 * inch, bottomMargin=0.8 * inch,
                        title="Machine 3: A Multiplicative-Coincidence Cryptid")
# fill deep-run placeholders
import sys
doc_story = []
for fl in story:
    doc_story.append(fl)
doc.build(story)
print("wrote", OUT)
