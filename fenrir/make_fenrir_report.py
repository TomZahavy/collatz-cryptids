"""Build the Fenrir case file (machine 7 of the collection)."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.colors import HexColor

OUT = "/Users/tomzahavy/Documents/Claude/collatz/fenrir/fenrir_report.pdf"

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=styles["Heading1"], spaceBefore=15, spaceAfter=7,
                    fontSize=13.5)
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


story = []
story.append(P("Fenrir: the first FRACTRAN cryptid, as machine 7", TITLE))
story.append(P("WS5a &mdash; the collection&rsquo;s pipeline applied to a "
               "community machine four months old &mdash; July 26, 2026", SUB))
story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=12))

story.append(P("1. The machine", H1))
story.append(P(
    "Fenrir (March 22, 2026; Jason Yuen with Claude Opus 4.6) is three size-22 "
    "FRACTRAN programs, e.g. [1/15, 27/77, 49/3, 10/49, 33/2], found in the "
    "BBf(22) cleanup and left open. The wiki gives the high-level form, and "
    "it is <i>literally a two-counter guarded affine machine</i> &mdash; our "
    "class exactly. With S(x,y) = [x,0,0,2,y]:"))
story.append(P(
    "[1,0,0,0,0] &rarr; S(0,1)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; "
    "S(0,2y) = halt&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; "
    "S(x,2y) &rarr; S(x&minus;1, 5y+2)&nbsp;&nbsp;&nbsp;|"
    "&nbsp;&nbsp;&nbsp; S(x,2y+1) &rarr; S(x+2, 5y)", CODE))
story.append(P(
    "Our implementation reproduces the published trajectory S(0,1), S(2,0), "
    "S(1,2), S(0,7), S(2,15), S(4,35) exactly. Writing the second counter as "
    "n, the rules read"))
story.append(P(
    "n odd:&nbsp; n &rarr; floor(5n/2) &minus; 2, x &rarr; x + 2"
    "&nbsp;&nbsp;&nbsp;&nbsp; n even:&nbsp; n &rarr; floor(5n/2) + 2, "
    "x &rarr; x &minus; 1 (halt if x = 0)", MATHC))
story.append(P(
    "so <b>n follows a 5/2-map and x is a walk driven by n&rsquo;s parity "
    "stream</b>. That is the Antihydra architecture with the multiplier 3/2 "
    "replaced by 5/2 and the parity roles exchanged: Fenrir is "
    "Antihydra&rsquo;s 5/2 sibling. The wiki says only that it &ldquo;follows "
    "a biased random walk&rdquo;; everything below is new."))

story.append(P("2. Reduction and theorems", H1))
story.append(tab([
    ("T1. No cycles",
     "n is strictly increasing for every n &ge; 2: if n is even, "
     "5n/2 + 2 &gt; n; if n is odd, (5n&minus;5)/2 &gt; n exactly when "
     "3n &gt; 5. The orbit enters n &ge; 2 at its second step, so no cycle "
     "exists and the only possible outcome besides halting is divergence. "
     "PROVED (checked to n = 200,000)."),
    ("T2. The counting form",
     "x is not an independent counter: x<sub>k</sub> = 3&middot;O<sub>k</sub> "
     "&minus; k where O<sub>k</sub> counts the odd n<sub>j</sub> with j &lt; "
     "k. So the whole two-counter machine collapses to the 5/2-map on n plus "
     "a counting functional of its parity stream &mdash; the analogue of the "
     "collection&rsquo;s reduction to a single integer. PROVED (verified for "
     "k &lt; 4,000)."),
    ("T3. Exact halting criterion",
     "<b>Fenrir halts if and only if its orbit reaches x = 1 with n &equiv; 0 "
     "(mod 4)</b>. Reason: x = 0 is reachable only from (1, even) by the "
     "decrement, and the new second counter 5(n/2) + 2 is even exactly when "
     "4 | n. Equivalently, by T2: some k has 3&middot;O<sub>k</sub> = k + 1 "
     "and n<sub>k</sub> &equiv; 0 (mod 4). PROVED, and brute-force verified "
     "against direct simulation on 13,500 starts (1,426 of which halt) with "
     "no mismatch."),
], ("theorem", "statement"), (1.2 * inch, 5.1 * inch)))

story.append(P("3. Taxonomy, and the opportunity stream (P8)", H1))
story.append(P(
    "Fenrir is a <b>coincidence-type</b> machine in our taxonomy: halting "
    "requires two independent conditions to coincide &mdash; a walk at a "
    "specific level and a congruence on the other counter. T3 makes the "
    "opportunity stream explicit and much sharper than a generic "
    "large-deviation estimate: <b>the opportunities are exactly the visits to "
    "x = 1</b>, each halting with model probability 1/4."))
story.append(P(
    "The walk moves +2 on odd steps and &minus;1 on even ones, so it descends "
    "one level with probability q satisfying q = 1/2 + q<super>3</super>/2, "
    "i.e. q = (&radic;5 &minus; 1)/2 = 0.618034 &mdash; the golden-ratio "
    "conjugate the meta report already records for Antihydra, arising here "
    "for the same reason. From height x the chance of ever revisiting level 1 "
    "is q<super>x&minus;1</super>, so &Sigma;p<sub>n</sub> converges "
    "geometrically: probviously non-halting, on the P8 dichotomy&rsquo;s "
    "convergent side, with every other machine in the collection."))
story.append(P(
    "<b>The verified run makes this unusually concrete.</b> In 1,000,000 "
    "steps (n reaches 1,321,927 bits, matching log<sub>2</sub>(5/2) per step "
    "to one part in 10<super>6</super>), the odd fraction is 0.50022 and "
    "x<sub>k</sub>/k is 0.50067 &mdash; both at their model values. The walk "
    "visits x = 1 <b>exactly once in the machine&rsquo;s entire history</b>, "
    "at step 2, in state (1, 2); it missed because 4 does not divide 2. So "
    "Fenrir has had precisely one halting opportunity, ever, and the residual "
    "risk beyond the verified prefix is (1/4)q<super>500,668</super>/(1 "
    "&minus; q) &asymp; 10<super>&minus;104,633</super>."))

story.append(P("4. What is open, and what this adds", H1))
story.append(P(
    "Open exactly where every machine in the collection is open: T3 turns "
    "halting into a single-orbit statement about the parity stream of the "
    "5/2-map from n = 1, and the pseudorandomness that makes the risk "
    "estimate persuasive is an almost-everywhere fact, not a fact about this "
    "one orbit. Fenrir is a certified cryptid of the coincidence type, "
    "&Pi;<sub>1</sub><super>0</super> as a single-orbit question."))
story.append(P(
    "Against the community&rsquo;s current page, this case file adds: the "
    "no-cycle theorem, the counting form, the exact halting criterion T3 "
    "(which replaces &ldquo;biased random walk&rdquo; with a checkable "
    "arithmetic condition), the taxonomy placement, the golden-ratio "
    "opportunity accounting, and the observation that <b>Fenrir and Antihydra "
    "have the identical walk and the identical constant, differing only in "
    "the digit source (5/2 versus 3/2) and in Fenrir needing an exact hit of "
    "x = 0 where Antihydra needs a first passage below its threshold</b>. "
    "That is a controlled comparison of the kind the meta report&rsquo;s "
    "cross-machine patterns are built from: same architecture, same risk "
    "profile, different "
    "arithmetic engine."))
story.append(P(
    "For the program, the transfer is the point. Fenrir was published four "
    "months ago in a different formalism (FRACTRAN) by a different community, "
    "and the collection&rsquo;s pipeline &mdash; reduce to a single stream, "
    "prove no cycles, extract an exact halting criterion, type it, count the "
    "opportunities &mdash; applied without modification and produced results "
    "the original analysis does not have."))

story.append(P("5. Verification ledger", H1))
story.append(tab([
    ("Rules and start", "From wiki.bbchallenge.org/wiki/Fenrir, fetched July "
     "26, 2026; our implementation reproduces the published trajectory "
     "term-for-term."),
    ("T1, T2, T3", "PROVED, and machine-verified: T1 to n = 200,000, T2 to "
     "k = 4,000, T3 against direct simulation on 13,500 starts."),
    ("q = (&radic;5 &minus; 1)/2", "PROVED (root in (0,1) of "
     "q<super>3</super> &minus; 2q + 1 = 0)."),
    ("1,000,000 steps without halting; one visit to x = 1",
     "MACHINE-VERIFIED (exact big-integer simulation, 247 s)."),
    ("Residual risk 10<super>&minus;104,633</super>",
     "HEURISTIC. It assumes the parity stream behaves like fair coin flips; "
     "that assumption is exactly what is unproved."),
    ("Non-halting", "OPEN. Nothing here proves it."),
], ("claim", "status"), (2.1 * inch, 4.2 * inch)))
story.append(Spacer(1, 8))
story.append(P("Code: fenrir.py (rules, fidelity, T1&ndash;T2 checks), "
               "analysis.py (long run, opportunity stream, P8 accounting).",
               CODE))

doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.85 * inch,
                        rightMargin=0.85 * inch, topMargin=0.8 * inch,
                        bottomMargin=0.8 * inch, title="Fenrir: machine 7")
doc.build(story)
print(f"wrote {OUT}")
