"""Build the Space Needle report (the multiplicative archetype)."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.colors import HexColor

OUT = "/Users/tomzahavy/Documents/Claude/collatz/needle/needle_report.pdf"
styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=styles["Heading1"], spaceBefore=18, spaceAfter=8)
H2 = ParagraphStyle("H2x", parent=styles["Heading2"], spaceBefore=14, spaceAfter=6)
BODY = ParagraphStyle("Bodyx", parent=styles["Normal"], fontSize=10.5, leading=14.5, spaceAfter=7)
MATHC = ParagraphStyle("MathCx", parent=styles["Normal"], fontName="Times-Italic",
                       fontSize=10.5, leading=15, alignment=TA_CENTER, spaceBefore=4, spaceAfter=8)
CELL = ParagraphStyle("Cellx", parent=styles["Normal"], fontName="Times-Roman", fontSize=9.5, leading=12.5)
TITLE = ParagraphStyle("Titlex", parent=styles["Title"], fontSize=19, leading=24, spaceAfter=4)
SUB = ParagraphStyle("Subx", parent=styles["Normal"], alignment=TA_CENTER,
                     textColor=colors.HexColor("#555555"), fontSize=11, spaceAfter=18)
BLUE = HexColor("#1a3c6e")


def P(text, style=BODY):
    return Paragraph(text, style)


def tab(rows, header, widths):
    data = [[P(f"<b>{h}</b>", CELL) for h in header]] + [[P(c, CELL) for c in r] for r in rows]
    t = Table(data, colWidths=list(widths), repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c4d6")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef7")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f8fb")])]))
    return t


story = []
story.append(P("The Space Needle Through the Toolkit", TITLE))
story.append(P("The BB(6) cryptid that machine 3 was built to mirror &mdash; "
               "halting on an exact power of 2", SUB))

story.append(P("1. Overview", H1))
story.append(P(
    "The Space Needle is a Busy Beaver BB(6) cryptid (machine "
    "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD, discovered by mxdys, "
    "January 2025). It is the <b>multiplicative-coincidence</b> archetype of "
    "the bbchallenge catalogue &mdash; and the machine our own machine 3 was "
    "constructed to mirror, with powers of 2 in place of powers of 3. This "
    "note runs the collection&rsquo;s toolkit over it, both to characterize "
    "it and to check that the tools built on our machines reproduce the "
    "community&rsquo;s findings on a genuine catalogued cryptid. They do, "
    "exactly."))
story.append(P(
    "Results: the one-variable form reproduces the wiki&rsquo;s published "
    "trajectory exactly; the machine provably cannot cycle (the state is its "
    "own potential); halting is equivalent to the orbit hitting an exact "
    "power of 2 (Theorem 1); the branch statistic is the 2-adic valuation "
    "law; and the measured per-step log-growth is 0.6515, matching the "
    "wiki&rsquo;s 0.652355 (so b &#8776; 1.918<super>n</super> vs the "
    "wiki&rsquo;s 1.92006). It is a divergent cryptid, probviously "
    "non-halting; the open core is the same single-orbit question as "
    "everywhere."))

story.append(P("2. The machine", H1))
story.append(P(
    "The wiki gives two high-level forms. <b>Doucette&rsquo;s one-variable "
    "form</b> is the halting-equivalent reduction we analyze. Writing v(b) "
    "for the 2-adic valuation of b and m = b / 2<super>v(b)</super> for its "
    "odd part, from b<sub>0</sub> = 6:"))
story.append(P("HALT if b is an exact power of 2 (m = 1); else "
               "b &rarr; b + v(b) + (3/2)(m &minus; 1).", MATHC))
story.append(P(
    "(The term (3/2)(m&minus;1) is always an integer because m is odd.) "
    "<b>Fidelity:</b> the implementation reproduces the wiki&rsquo;s "
    "sequence 6, 10, 17, 41, 101, 251, 626, 1095, 2736, 2995 exactly. "
    "<b>Ducharme&rsquo;s low-level form</b> A(b, c) &mdash; (1, c) halts, "
    "(2b, c) &rarr; (2+5b+c, 1), (2b+1, c) &rarr; (b&minus;1, 3+b+c), start "
    "(3, 1) &mdash; is also implemented and runs without halting, as a "
    "cross-check on the machine level."))

story.append(P("3. Analysis", H1))
story.append(P("3.1&nbsp;&nbsp;Theorem 1: halting is hitting a power of 2", H2))
story.append(P(
    "The map halts precisely when b is an exact power of 2, so the halting "
    "question is: does the orbit of 6 ever land on {1, 2, 4, 8, 16, "
    "&hellip;}? This is the <b>multiplicative-coincidence</b> type &mdash; a "
    "geometric target of exact powers, spaced by a factor of 2. It is machine "
    "3&rsquo;s halting criterion (a = 3<super>j</super>) with base 2 in place "
    "of base 3, and without machine 3&rsquo;s exponent congruence: here every "
    "power of 2 halts."))
story.append(P("3.2&nbsp;&nbsp;Theorem 2: no cycles (the state is its own "
               "potential)", H2))
story.append(P(
    "For any non-halting b the odd part m &ge; 3, so b &rarr; b + v(b) + "
    "(3/2)(m&minus;1) increases b by at least 3. Thus b is strictly "
    "increasing and the machine cannot cycle: it halts or escapes to "
    "infinity. This is simpler than machine 3, whose a was not monotone and "
    "needed the potential &Phi; = a + b; here the single state variable "
    "serves directly, exactly as for the Hydra family. (Verified: minimum "
    "increment 3 over all non-power-of-2 b &lt; 300,000, and strict increase "
    "along 200,000 orbit steps.)"))
story.append(P("3.3&nbsp;&nbsp;Branch statistic and growth", H2))
story.append(P(
    "The branch is v(b), the 2-adic valuation. Measured over 200,000 steps it "
    "matches the geometric law P(v = k) = 2<super>&minus;(k+1)</super> "
    "(0.498, 0.252, 0.125, 0.063, &hellip; vs 0.5, 0.25, 0.125, 0.0625) "
    "&mdash; the same valuation law behind machine 3 (base 3) and "
    "the Collatz shortcut. From it the growth constant follows: when b is odd "
    "(half the time) b &rarr; ~5b/2, and averaging over the valuation law the "
    "per-step log-growth is"))
story.append(P("mean &Delta; log b = 0.6515 (measured)&nbsp;&nbsp;vs&nbsp;"
               "&nbsp;0.652355 (wiki),&nbsp;&nbsp;so b &#8776; 1.918"
               "<super>n</super>.", MATHC))
story.append(P(
    "Powers of 2 are spaced by &times;2 while b grows by about &times;1.92 "
    "per step, so the orbit passes roughly one power-of-2 scale per step; the "
    "chance of landing <i>exactly</i> on one decays like 1/b, a convergent "
    "sum. So Space Needle is a <b>divergent-type</b> cryptid, probviously "
    "non-halting &mdash; the same shape as machine 3, and the reason machine "
    "3 was a faithful analogue to build."))

story.append(P("4. Status and verification", H1))
story.append(tab([
    ("one-variable form vs wiki", "reproduces 6, 10, 17, 41, 101, 251, 626, "
     "1095, 2736, 2995 exactly", "pass"),
    ("Theorem 1 (halt = power of 2)", "by construction of the map", "pass"),
    ("Theorem 2 (no cycles)", "min increment 3 for b &lt; 300,000; strict "
     "increase over 200,000 orbit steps", "pass"),
    ("branch statistic", "v(b) matches 2<super>&minus;(k+1)</super> to three "
     "decimals over 200,000 steps", "pass"),
    ("growth constant", "0.6515 measured vs 0.652355 (wiki); b reached "
     "187,989 bits in 200,000 steps, no power of 2 hit", "pass"),
], ("check", "scope", "result"), (1.9 * inch, 4.1 * inch, 0.7 * inch)))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=0.8, color=BLUE))
story.append(Spacer(1, 4))
story.append(P(
    "Artifacts: needle.py (both forms + wiki fidelity), theorems.py "
    "(T1&ndash;T4 and measurements). This report is deliberately kept "
    "separate from the collection meta report for now. <b>Status: "
    "unchanged &mdash; open (divergent, multiplicative-coincidence cryptid); "
    "the toolkit reproduces the community&rsquo;s findings and adds the "
    "no-cycle proof beneath them.</b>",
    ParagraphStyle("Foot", parent=BODY, fontSize=9.5,
                   textColor=colors.HexColor("#555555"))))

doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.9 * inch,
                        rightMargin=0.9 * inch, topMargin=0.8 * inch,
                        bottomMargin=0.8 * inch,
                        title="The Space Needle Through the Toolkit")
doc.build(story)
print("wrote", OUT)
