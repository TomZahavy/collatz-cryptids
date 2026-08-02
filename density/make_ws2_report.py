"""Build the WS2 report: how many starts below x halt (depth-graded)."""
import math

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.colors import HexColor

from density import bound, halting_seeds

OUT = "/Users/tomzahavy/Documents/Claude/collatz/density/ws2_report.pdf"

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=styles["Heading1"], spaceBefore=16, spaceAfter=7,
                    fontSize=14)
BODY = ParagraphStyle("Bodyx", parent=styles["Normal"], fontSize=10.5, leading=14.5,
                      spaceAfter=7)
MATHC = ParagraphStyle("MathCx", parent=styles["Normal"], fontName="Times-Italic",
                       fontSize=10.5, leading=15, alignment=TA_CENTER,
                       spaceBefore=4, spaceAfter=8)
CELL = ParagraphStyle("Cellx", parent=styles["Normal"], fontName="Times-Roman",
                      fontSize=9.5, leading=12.5)
CODE = ParagraphStyle("Codex", parent=styles["Normal"], fontName="Courier",
                      fontSize=8.8, leading=11.5, spaceAfter=7,
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
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#e8eef7")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, HexColor("#f6f8fb")])]))
    return t


L = 5
XS = [10 ** 6, 10 ** 12, 10 ** 24, 10 ** 48, 10 ** 96, 10 ** 192]
DATA = [(x, [len(s) for s in halting_seeds(x, L)]) for x in XS]

story = []
story.append(P("How many starts below x halt? The Space Needle, counted", TITLE))
story.append(P("WS2, first execution &mdash; an unconditional depth-graded "
               "density theorem &mdash; July 26, 2026", SUB))
story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=12))

story.append(P("1. Result", H1))
story.append(P(
    "Let A<sub>j</sub>(x) count the b &le; x whose orbit first reaches a power "
    "of 2 after exactly j steps. The workstream asked for "
    "#{b &le; x : b halts} = O(x<super>c</super>) with c &lt; 1. What is "
    "actually provable, and is proved here, is sharper in one direction and "
    "weaker in another:"))
story.append(P(
    "<b>Theorem.</b> For every L, "
    "&Sigma;<sub>j&le;L</sub> A<sub>j</sub>(x) &le; "
    "(L+1)&middot;(log<sub>2</sub>x + 1.585L + 2)<super>L+1</super>.",
    MATHC))
story.append(P(
    "Sharper: at bounded depth the halting starts are <b>polylogarithmic</b>, "
    "not merely of density x<super>c</super>. Weaker: it says nothing at "
    "unbounded depth, and Section 5 explains why that gap is the cryptid "
    "difficulty itself rather than a missing lemma. The proof needs only two "
    "facts about the map, both proved below, and it comes with an exact "
    "computation: the depth-graded backward enumeration is <b>complete</b> "
    "(no ceiling assumption), so the true counts can be evaluated at "
    "astronomical x &mdash; up to 10<super>192</super> in a fraction of a "
    "second &mdash; and they grow like (log<sub>2</sub>x)<super>1.0</super>, "
    "about 1.7 seeds per octave."))

story.append(P("2. A premise of the plan, corrected", H1))
story.append(P(
    "NEXT_STEPS.md justified this workstream with &ldquo;the Needle map is "
    "strictly increasing, so H is exactly backward-enumerable&rdquo;. The map "
    "is <b>not</b> increasing: F(9) = 21 &gt; F(10) = 17, and there are 990 "
    "inversions below 2000. The property the argument actually needs is "
    "<b>expansion</b> &mdash; each step strictly grows its argument &mdash; "
    "which is true and is what makes preimages smaller than their images, "
    "hence the backward walk finite. Everything downstream survives the "
    "correction; the plan text has been fixed."))

story.append(P("3. The three lemmas", H1))
story.append(tab([
    ("L1. Expansion",
     "x + 3 &le; F(x) &le; 2.5x + v &le; 3x for every x &ge; 3 that is not a "
     "power of 2. <i>Proof:</i> F(x) = x + 3k + v with k = x &gt;&gt; (v+1) "
     "&ge; 1, giving the lower bound; and k &le; x/2 with v &le; "
     "floor(log<sub>2</sub>x) &le; x/2 gives the upper. Machine-verified for "
     "x &lt; 200,000."),
    ("L2. Exact backward step",
     "y = F(b) with v<sub>2</sub>(b) = v holds iff b = (2<super>v+1</super>y "
     "+ 2<super>v</super>(3 &minus; 2v)) / (2<super>v+1</super> + 3). So each "
     "valuation contributes <i>at most one</i> preimage, only v &le; "
     "log<sub>2</sub>(2y) can contribute, and therefore d(y) := "
     "#F<super>&minus;1</super>(y) &le; log<sub>2</sub>y + 1. "
     "Machine-verified: the formula inverts F for all x &lt; 60,000, and the "
     "largest d(y) seen below 60,000 is 4."),
    ("L3. Subcritical branching on average",
     "&Sigma;<sub>y&le;Y</sub> d(y) &le; cY + O(log Y) with c = "
     "&Sigma;<sub>v&ge;0</sub> 1/(2<super>v+1</super>+3) = 0.5453&hellip; "
     "&lt; 1, because branch v produces a preimage only for y in one residue "
     "class mod 2<super>v+1</super>+3. Measured average over y &lt; 200,000: "
     "<b>0.5452</b> &mdash; the rigorous ceiling is essentially attained, so "
     "the backward tree is thin for a reason that can be written down, not "
     "just observed."),
    ("L4. Completeness (the cutoff lemma)",
     "If b &le; x and F<super>j</super>(b) = 2<super>m</super> with j &le; L, "
     "then 2<super>m</super> &le; 3<super>L</super>x by L1. So seeding the "
     "backward walk with every power of 2 up to 3<super>L</super>x, and "
     "pruning layer i at 3<super>L&minus;i</super>x, enumerates <i>every</i> "
     "such b and no others. This is what replaces the heuristic ceiling "
     "(CEIL = 2<super>44</super>) in explorations/backward.py: the counts "
     "below are theorems about the map, not about a search budget."),
], ("lemma", "statement and proof"), (1.35 * inch, 4.95 * inch)))
story.append(P(
    "The theorem follows: A<sub>0</sub>(x) &le; log<sub>2</sub>x + 1, and a "
    "depth-(j+1) seed below x is a preimage of a depth-j seed below 3x (L1), "
    "of which there are at most log<sub>2</sub>(3x) + 1 per node (L2), so "
    "A<sub>j+1</sub>(x) &le; A<sub>j</sub>(3x)&middot;(log<sub>2</sub>(3x)+1); "
    "unwinding gives the stated bound."))

story.append(P("4. The exact counts", H1))
rows = []
for x, c in DATA:
    rows.append((f"10<super>{len(str(x)) - 1}</super>",
                 " &nbsp;".join(str(v) for v in c), str(sum(c)),
                 f"{bound(x, L):.2g}", f"{sum(c) / math.log2(x):.2f}"))
story.append(tab(rows, ("x", "A<sub>0</sub> &hellip; A<sub>5</sub>",
                        "total (depth &le; 5)", "the theorem&rsquo;s bound",
                        "total / log<sub>2</sub>x"),
                 (0.75 * inch, 1.9 * inch, 1.15 * inch, 1.2 * inch, 1.3 * inch)))
story.append(P(
    "Every entry is exact and complete by L4, and the whole table takes 0.3 "
    "seconds. Consecutive rows give a growth exponent in log<sub>2</sub>x of "
    "1.04, 0.97, 0.97, 1.01, 0.99 &mdash; so the depth-bounded halting seeds "
    "grow <b>linearly in log x</b>, about 1.7 per octave, which is the exact "
    "form of the &ldquo;one halting seed per octave&rdquo; observation "
    "(Finding 5) that was previously only empirical. The rigorous bound is "
    "loose by many orders of magnitude, as expected: it pays "
    "log<sub>2</sub>x per level of depth where the truth pays a factor of "
    "about 0.43."))
story.append(P(
    "Two structural facts fall out of the same computation. The layer sizes "
    "decay geometrically in depth (at x = 10<super>192</super>: 638, 276, "
    "105, 43, 25, 21), which is L3&rsquo;s subcriticality visible in the tree "
    "rather than on average. And the tree is genuinely shallow at small x: "
    "below 10<super>6</super> the depth-14 enumeration finds exactly the same "
    "35 seeds as the depth-3 one &mdash; 20 powers of 2 and 15 non-trivial "
    "seeds, the smallest being 7, 103, 312, 352, 372.", BODY))

story.append(P("5. What is not proved, and why that is the interesting part", H1))
story.append(P(
    "The bound degrades as depth grows and goes trivial at depth about "
    "log x / log log x. To close the gap to an unconditional "
    "O(x<super>c</super>) for <i>all</i> depths one would need the branching "
    "to stay subcritical along the tree, not merely on average over all "
    "integers &mdash; i.e. that the tree&rsquo;s nodes are equidistributed "
    "among the residue classes mod 2<super>v+1</super>+3 that L3 counts. That "
    "is precisely the equidistribution-of-one-orbit wall that makes these "
    "machines cryptids: the same gap as Collatz&rsquo;s, in the same place. "
    "It is worth being explicit that this is not a missing technical lemma. "
    "An unconditional O(x<super>c</super>) with c &lt; 1 would assert that "
    "all but x<super>c</super> starts never halt, a statement about "
    "individual orbits of every start &mdash; strictly stronger than any "
    "almost-everywhere result the field currently has for any expanding "
    "Collatz-like map."))
story.append(P(
    "The productive reading is that depth is the right grading, and it is the "
    "same grading WS3 uses for the Baker ladder (block count). The two "
    "workstreams meet: WS2 bounds how many seeds can halt within L steps, WS3 "
    "aims to exclude halting for branch words of bounded complexity. A "
    "combined statement &mdash; nothing of bounded depth halts, and only "
    "polylog many things of bounded depth exist &mdash; is the realistic "
    "shape of an unconditional partial decision for this machine."))

story.append(P("6. Verification ledger", H1))
story.append(tab([
    ("L1, L2, L4 and the theorem", "PROVED. L1 and L2 also machine-verified "
     "(x &lt; 200,000 and 60,000 respectively); L4 is the induction from L1."),
    ("L3 constant c = 0.5453",
     "PROVED as an upper bound (one residue class per branch). The measured "
     "average 0.5452 is an observation, not part of the proof."),
    ("The exact counts in Section 4",
     "MACHINE-VERIFIED and complete by L4. Cross-checked against forward "
     "brute-force simulation of every b &le; 60,000 &mdash; the backward "
     "enumeration and the forward scan agree set-for-set, not just in count."),
    ("&ldquo;About 1.7 seeds per octave&rdquo; and the geometric layer decay",
     "OBSERVED (exactly, at the listed x), not proved. The proved bound is "
     "polynomial of degree L+1 in log x."),
    ("Anything at unbounded depth",
     "OPEN, and equivalent to a single-orbit equidistribution statement of "
     "Collatz strength. Nothing here is evidence for it."),
    ("The plan&rsquo;s monotonicity premise",
     "FALSE, corrected here and in NEXT_STEPS.md. Expansion is the property "
     "the argument uses."),
], ("claim", "status"), (2.2 * inch, 4.1 * inch)))
story.append(Spacer(1, 8))
story.append(P(
    "Code: density.py (lemmas, exact preimages, complete depth-graded "
    "enumeration, tests including the forward/backward cross-check), "
    "counts.py (the table). Both runnable standalone.", CODE))

doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.85 * inch,
                        rightMargin=0.85 * inch, topMargin=0.8 * inch,
                        bottomMargin=0.8 * inch,
                        title="WS2: halting density for the Space Needle")
doc.build(story)
print(f"wrote {OUT}")
