"""Build the machine-4 report (A(a,b) system with the recovery potential)."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.colors import HexColor

OUT = "/Users/tomzahavy/Documents/Claude/collatz/machine4/machine4_halting_report.pdf"
styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=styles["Heading1"], spaceBefore=18, spaceAfter=8)
H2 = ParagraphStyle("H2x", parent=styles["Heading2"], spaceBefore=14, spaceAfter=6)
BODY = ParagraphStyle("Bodyx", parent=styles["Normal"], fontSize=10.5, leading=14.5, spaceAfter=7)
MATHC = ParagraphStyle("MathCx", parent=styles["Normal"], fontName="Times-Italic",
                       fontSize=10.5, leading=15, alignment=TA_CENTER, spaceBefore=4, spaceAfter=8)
CELL = ParagraphStyle("Cellx", parent=styles["Normal"], fontName="Times-Italic", fontSize=10, leading=13)
CELLR = ParagraphStyle("CellRx", parent=CELL, fontName="Times-Roman")
TITLE = ParagraphStyle("Titlex", parent=styles["Title"], fontSize=19, leading=24, spaceAfter=4)
SUB = ParagraphStyle("Subx", parent=styles["Normal"], alignment=TA_CENTER,
                     textColor=colors.HexColor("#555555"), fontSize=11, spaceAfter=18)
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
              ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f8fb")])]
    else:
        s += [("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f6f8fb")])]
    return TableStyle(s)


def rtable(rows, header, widths, italic=None):
    italic = italic or set()
    data = [[P(f"<b>{h}</b>", CELLR) for h in header]]
    for r in rows:
        data.append([P(c, CELL if i in italic else CELLR) for i, c in enumerate(r)])
    t = Table(data, colWidths=list(widths), repeatRows=1)
    t.setStyle(tstyle())
    return t


story = []
story.append(P("Machine 4: A Sparse-Coincidence Cryptid with a Recovery Potential", TITLE))
story.append(P("The A(a, b) system &mdash; halting on the line b = a + 3, and a "
               "no-cycle proof the plain recipe could not give", SUB))

story.append(P("1. Overview", H1))
story.append(P(
    "Machine 4 is the deterministic system A(a, b) on positive-integer pairs, "
    "ten guarded rules (Section 2), started at A(1, 1). It is an instance of "
    "the <b>sparse-coincidence</b> type: halting requires the "
    "orbit to land exactly on a line. Two things make it worth its own report. "
    "First, its no-cycle proof does <i>not</i> come from the collection&rsquo;s "
    "usual affine-potential recipe &mdash; no linear combination of a and b is "
    "monotone &mdash; but from a strictly weaker <b>potential-with-recovery</b> "
    "argument (Theorem 4), the first time the collection has needed it. Second, "
    "its growth is linear and its orbit comes startlingly close to halting "
    "(within distance 1 of the halt line), making it the collection&rsquo;s "
    "sharpest convergent cryptid."))
story.append(P(
    "Results: a stays odd forever, so the even-a rules never fire (Theorem 1); "
    "halting is exactly the line b = a + 3 with a odd (Theorem 2); the "
    "dominant rule cascades in closed form (Theorem 3); the "
    "machine provably cannot cycle (Theorem 4); and it did not halt in "
    "3,000,000 steps, growing only linearly. The open core &mdash; whether "
    "the orbit ever lands on b = a + 3 &mdash; is the same single-orbit "
    "question as everywhere in this collection."))

story.append(P("2. The machine", H1))
story.append(P("State A(a, b). Dispatch: even a = 2k uses the first three "
               "rules; odd a = 2k+1 uses the rest (on b relative to a)."))
story.append(Spacer(1, 4))
story.append(rtable([
    ("A(2k, 1) &rarr; A(3, 2k+2)", "even a, b = 1"),
    ("A(2k, 2) &rarr; A(2k+1, 1)", "even a, b = 2"),
    ("A(2k, b) &rarr; A(2k+3, b&minus;2), b &ge; 3", "even a"),
    ("A(2k+1, 2m) &rarr; A(4m+3, 2k&minus;2m+1)", "odd a, b = 2m &le; a&minus;1"),
    ("A(2k+1, 2m+1) &rarr; A(4m+3, 2k&minus;2m+3)", "odd a, b = 2m+1 &le; a"),
    ("A(2k+1, 2k+2) &rarr; A(4k+1, 1)", "b = a+1"),
    ("A(2k+1, 2k+3) &rarr; A(4k+7, 1)", "b = a+2"),
    ("A(2k+1, 2k+4) &rarr; <b>HALT</b>", "b = a+3"),
    ("A(2k+1, 2k+5) &rarr; A(4k+5, 1)", "b = a+4"),
    ("A(2k+1, b) &rarr; A(4k+7, b&minus;2k&minus;5), b &ge; 2k+6", "b &ge; a+5"),
], ("rule", "region"), (4.1 * inch, 2.5 * inch), italic={0}))
story.append(Spacer(1, 6))
story.append(P(
    "<b>Fidelity.</b> The implementation reproduces the hand-computed prefix "
    "A(1,1) &rarr; A(3,3) &rarr; A(7,3) &rarr; A(7,7) &rarr; A(15,3) &rarr; "
    "A(7,15) &rarr; A(19,4) &rarr; &hellip;"))

story.append(P("3. Invariant and halting criterion", H1))
story.append(P(
    "<b>Theorem 1 (a is always odd).</b> Every odd-a rule outputs an odd a "
    "(each right-hand side is 4m+3, 4k+1, 4k+5 or 4k+7), and a<sub>0</sub> = 1 "
    "is odd. So a is odd at every step and the even-a rules A(2k, &middot;) are "
    "unreachable from A(1, 1). (Verified: 300,000 random odd-a states and "
    "200,000 orbit steps.)"))
story.append(P(
    "<b>Theorem 2 (halting criterion).</b> With a odd, the only halting rule "
    "is A(2k+1, 2k+4) &rarr; HALT, i.e."))
story.append(P("the machine halts iff it reaches a state with a odd and "
               "b = a + 3.", MATHC))
story.append(P(
    "(Verified exhaustively for a &lt; 4000.) Since a is odd, b = a + 3 is "
    "even. This is the sparse-coincidence signature: halting is an exact "
    "landing on one line in the (a, b) plane. The four rules on the neighbouring offsets "
    "b = a+1, a+2, a+4 and b &ge; a+5 all continue, threading around the halt "
    "line."))

story.append(P("4. Acceleration and no cycles", H1))
story.append(P("4.1&nbsp;&nbsp;Theorem 3: the dominant cascade", H2))
story.append(P(
    "The rule for b &ge; a+5, (a, b) &rarr; (2a+5, b&minus;a&minus;4), is "
    "iterable in closed form: after j rounds"))
story.append(P("a<sub>j</sub> = 2<super>j</super>(a+5) &minus; 5,"
               "&nbsp;&nbsp;&nbsp;&nbsp;b<sub>j</sub> = b &minus; "
               "(2<super>j</super>&minus;1)(a+5) + j,", MATHC))
story.append(P(
    "valid while b<sub>j</sub> &ge; a<sub>j</sub> + 5. a doubles while b drops "
    "by about a each round, so a long run of the dominant rule collapses to one "
    "jump, with an interior landing on the halt line detected in closed form "
    "(20,000 runs verified against the base rule)."))
story.append(P("4.2&nbsp;&nbsp;Theorem 4: no cycles, by a potential with recovery", H2))
story.append(P(
    "Here machine 4 departs from its predecessors. No affine combination "
    "p&middot;a + q&middot;b is monotone: the small-b rules "
    "(a, b) &rarr; (2b+3, a&minus;b) and (2b+1, a&minus;b+3) shrink a "
    "sharply, and the b = a+1 rule lowers a + b by 1. The collection&rsquo;s "
    "affine-potential recipe (pattern P6) simply fails. But a + b is a "
    "<b>potential with recovery</b>:"))
story.append(rtable([
    ("Lemma A", "&Delta;(a+b) &le; 0 only for b = a+1 (&Delta; = &minus;1) and "
     "b = a+4 (&Delta; = 0); both land on a state with b = 1."),
    ("Lemma B", "from any (a, 1) with a odd, &Delta;(a+b) = +4."),
], ("", ""), (0.7 * inch, 5.9 * inch)))
story.append(Spacer(1, 6))
story.append(P(
    "<b>Theorem 4.</b> The machine cannot cycle. <i>Proof.</i> By Lemma A "
    "every non-increasing step is isolated (it lands on b = 1, and by Lemma B "
    "the next step increases a + b by 4) and is immediately followed by a +4 "
    "step. Around any cycle the total change of a + b is zero; but pairing each "
    "non-positive step with the following +4 gives a net &ge; +3 for that pair, "
    "and every remaining step contributes &ge; +1, so the total is strictly "
    "positive &mdash; a contradiction. Hence there are no cycles: the machine "
    "halts or escapes to infinity. <b>QED</b> (both lemmas verified on 400,000 "
    "random states and, for Lemma B, exhaustively to a = 200,000.)"))
story.append(P(
    "This <b>extends the collection&rsquo;s no-cycle pattern</b>: the affine "
    "quantity need not decrease-free step by step, only over a bounded "
    "recovery window. It is worth recording as a reusable technique for the "
    "next machine whose guards defeat a plain potential."))

story.append(P("5. Behavior and status", H1))
story.append(P(
    "The orbit grows <b>linearly</b>: a + b drifts upward by about 2.34 per "
    "step (in 500,000 steps it decreased only once, by 1), reaching only "
    "~23-bit values after 3,000,000 steps. So machine 4 is a "
    "<b>convergent-type</b> cryptid. It did not halt in "
    "3,000,000 steps. Notably its closest approach to the halt line was "
    "|b &minus; (a+3)| = 1 &mdash; it repeatedly reaches the immediately "
    "adjacent lines b = a+2 and b = a+4 (both of which continue), so the "
    "halt line is threaded rather than distant. Whether the orbit ever lands "
    "exactly on b = a + 3 is the open core; the branch that decides it reads "
    "ever-deeper digits of the state, the same single-orbit obstruction as "
    "the rest of the collection."))
story.append(rtable([
    ("Theorem 1 (a odd)", "300,000 random + 200,000 orbit steps", "pass"),
    ("Theorem 2 (halt iff b = a+3)", "exhaustive for a &lt; 4000", "pass"),
    ("Theorem 3 (cascade)", "closed form vs base rule, 20,000 runs", "pass"),
    ("Theorem 4 (no cycles)", "Lemmas A, B on 400,000 states + a &le; 200,000",
     "pass"),
    ("deep run", "3,000,000 steps, no halt, linear growth (~23 bits), "
     "closest |b&minus;(a+3)| = 1", "pass"),
], ("check", "scope", "result"), (2.0 * inch, 4.0 * inch, 0.7 * inch)))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=0.8, color=BLUE))
story.append(Spacer(1, 4))
story.append(P(
    "Artifacts: m4_base.py (the ten rules), m4_theorems.py (Theorems "
    "1&ndash;4 and measurements). <b>Status: open (convergent, "
    "sparse-coincidence cryptid); halts or escapes &mdash; periodicity "
    "excluded by proof (via the recovery potential).</b>",
    ParagraphStyle("Foot", parent=BODY, fontSize=9.5,
                   textColor=colors.HexColor("#555555"))))

doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.9 * inch,
                        rightMargin=0.9 * inch, topMargin=0.8 * inch,
                        bottomMargin=0.8 * inch,
                        title="Machine 4: A Sparse-Coincidence Cryptid")
doc.build(story)
print("wrote", OUT)
