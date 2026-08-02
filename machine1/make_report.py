"""Build the PDF report summarizing the Collatz-like system acceleration.

Structure (interpretability revision):
 1  Overview (terminology defined up front)
 2  The base system (all 13 original rules, R1-R13)
 3  Three structural observations (with derivations)
 4  Level 2 (named rules + how each is derived from the base rules)
 5  Level 3 (cascades, with derivations)      5.1 A, 5.2 B, 5.3 full system
 6  Level 4                                    6.1 G, 6.2 affine, 6.3 runner, 6.4 step 25
 7  Qualitative dynamics
 8  Does it halt?                              8.1-8.4
 9  Verification (+ erratum)
10  Performance
11  Code artifacts
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.graphics.shapes import (Drawing, Rect, String, Line, Polygon,
                                       PolyLine, Circle, Group)
from reportlab.lib.colors import HexColor

OUT = "/Users/tomzahavy/Documents/Claude/collatz/machine1/collatz_acceleration_report.pdf"

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=styles["Heading1"], spaceBefore=18, spaceAfter=8)
H2 = ParagraphStyle("H2x", parent=styles["Heading2"], spaceBefore=14, spaceAfter=6)
BODY = ParagraphStyle("Bodyx", parent=styles["Normal"], fontSize=10.5, leading=14.5,
                      spaceAfter=7)
MATH = ParagraphStyle("Mathx", parent=styles["Normal"], fontName="Times-Italic",
                      fontSize=10.5, leading=15)
MATHC = ParagraphStyle("MathCx", parent=MATH, alignment=TA_CENTER, spaceBefore=4,
                       spaceAfter=8)
CELL = ParagraphStyle("Cellx", parent=styles["Normal"], fontName="Times-Italic",
                      fontSize=10, leading=13)
CELLR = ParagraphStyle("CellRx", parent=CELL, fontName="Times-Roman")
TITLE = ParagraphStyle("Titlex", parent=styles["Title"], fontSize=20, leading=25,
                       spaceAfter=4)
SUB = ParagraphStyle("Subx", parent=styles["Normal"], alignment=TA_CENTER,
                     textColor=colors.HexColor("#555555"), fontSize=11, spaceAfter=18)
PART = ParagraphStyle("Partx", parent=styles["Heading1"], fontSize=15, leading=19,
                      spaceBefore=6, spaceAfter=2, textColor=colors.HexColor("#1a3c6e"))
PARTSUB = ParagraphStyle("PartSubx", parent=styles["Normal"], fontSize=10.5,
                         leading=14, textColor=colors.HexColor("#444444"),
                         spaceAfter=12)
FIGCAP = ParagraphStyle("FigCapx", parent=styles["Normal"], fontSize=8.8,
                        leading=12, alignment=TA_CENTER,
                        textColor=colors.HexColor("#444444"),
                        spaceBefore=3, spaceAfter=11)

def P(text, style=BODY):
    return Paragraph(text, style)

BLUE = HexColor("#1a3c6e")
FILLB = HexColor("#e8eef7")
GREY = HexColor("#666666")
ACCENT = HexColor("#b23b3b")

def _arrow(d, x0, y, x1, label=None, sub=None):
    d.add(Line(x0, y, x1 - 7, y, strokeColor=BLUE, strokeWidth=1.2))
    d.add(Polygon([x1, y, x1 - 7, y + 3.5, x1 - 7, y - 3.5], fillColor=BLUE,
                  strokeColor=BLUE))
    if label:
        d.add(String((x0 + x1) / 2, y + 5, label, fontName="Helvetica",
                     fontSize=7.2, fillColor=BLUE, textAnchor="middle"))
    if sub:
        d.add(String((x0 + x1) / 2, y - 11, sub, fontName="Helvetica-Oblique",
                     fontSize=6.6, fillColor=GREY, textAnchor="middle"))

def compression_diagram():
    """Figure 1: the 4 -> 3 -> 2 -> 1 variable compression pipeline."""
    W, H = 468, 150
    d = Drawing(W, H)
    boxes = [
        (8,   "(a, b, c, d)", "4 variables", "base machine", "13 rules"),
        (128, "(a, b, d)",    "3 variables", "Level 1", "drop buffer c"),
        (248, "(b, d)",       "2 variables", "anchors", "fix a = 0"),
        (368, "D",            "1 variable",  "return map F", "fix b = 1"),
    ]
    bw, bh, by = 92, 46, 86
    cy = by + bh / 2
    for (x, tup, nv, cap1, cap2) in boxes:
        d.add(Rect(x, by, bw, bh, rx=6, ry=6, fillColor=FILLB, strokeColor=BLUE,
                   strokeWidth=1))
        d.add(String(x + bw / 2, by + bh - 17, tup, fontName="Helvetica-Bold",
                     fontSize=12, fillColor=BLUE, textAnchor="middle"))
        d.add(String(x + bw / 2, by + 8, nv, fontName="Helvetica", fontSize=8,
                     fillColor=GREY, textAnchor="middle"))
        d.add(String(x + bw / 2, by - 12, cap1, fontName="Helvetica-Bold",
                     fontSize=7.5, fillColor=HexColor("#333333"),
                     textAnchor="middle"))
        d.add(String(x + bw / 2, by - 22, cap2, fontName="Helvetica-Oblique",
                     fontSize=7, fillColor=GREY, textAnchor="middle"))
    _arrow(d, 100 + 8, cy, 128, "eliminate")
    _arrow(d, 220 + 8, cy, 248, "restrict")
    _arrow(d, 340 + 8, cy, 368, "restrict")
    # time-compression note spanning the middle (levels 2-3 batch rules)
    d.add(Line(8, 34, 460, 34, strokeColor=HexColor("#c9b45a"), strokeWidth=0.6,
               strokeDashArray=[2, 2]))
    d.add(String(234, 22, "Levels 2–3 batch rules along the way: each "
                 "firing-run or two-rule cascade collapses to one closed-form jump",
                 fontName="Helvetica-Oblique", fontSize=7, fillColor=HexColor("#8a7a2a"),
                 textAnchor="middle"))
    d.add(String(234, 11, "(compressing steps, not variables — the 10^60-step "
                 "simulations of the Overview)", fontName="Helvetica-Oblique",
                 fontSize=7, fillColor=HexColor("#8a7a2a"), textAnchor="middle"))
    d.hAlign = "CENTER"
    return d

# log10(D_k) along the orbit of 17, k = 0..24 (hardcoded, from onedim.py)
_ORBIT_LOG = [1.23, 1.756, 2.267, 2.779, 3.355, 3.772, 4.207, 4.546, 4.856,
              5.222, 5.525, 5.909, 6.291, 6.684, 7.157, 7.59, 8.079, 8.641,
              9.185, 9.534, 9.976, 10.351, 10.598, 11.072, 11.642]

def orbit_diagram():
    """Figure 2: the F-orbit of 17 -- log10(D_k) vs cycle k."""
    W, H = 468, 226
    d = Drawing(W, H)
    ox, oy = 40, 34          # plot origin
    pw, ph = 400, 168        # plot area
    kmax = len(_ORBIT_LOG) - 1
    ymax = 12.0
    def px(k): return ox + pw * k / kmax
    def py(v): return oy + ph * v / ymax
    # axes
    d.add(Line(ox, oy, ox, oy + ph, strokeColor=HexColor("#888888"), strokeWidth=1))
    d.add(Line(ox, oy, ox + pw, oy, strokeColor=HexColor("#888888"), strokeWidth=1))
    # y gridlines/labels (log10 D = number of digits)
    for v in range(0, 13, 2):
        d.add(Line(ox - 3, py(v), ox + pw, py(v),
                   strokeColor=HexColor("#eeeeee"), strokeWidth=0.5))
        d.add(String(ox - 6, py(v) - 3, str(v), fontName="Helvetica", fontSize=7,
                     fillColor=GREY, textAnchor="end"))
    for k in range(0, kmax + 1, 4):
        d.add(String(px(k), oy - 12, str(k), fontName="Helvetica", fontSize=7,
                     fillColor=GREY, textAnchor="middle"))
    # axis titles
    d.add(String(ox + pw / 2, oy - 26, "super-cycle k", fontName="Helvetica",
                 fontSize=8, fillColor=HexColor("#333333"), textAnchor="middle"))
    g = Group(String(0, 0, "log10 Dk   (= digits of Dk)",
                     fontName="Helvetica", fontSize=8, fillColor=HexColor("#333333"),
                     textAnchor="middle"))
    g.translate(11, oy + ph / 2); g.rotate(90)
    d.add(g)
    # halting-scale reference line (first reachable halting value 124313)
    yv = 5.095
    d.add(Line(ox, py(yv), ox + pw, py(yv), strokeColor=ACCENT, strokeWidth=0.8,
               strokeDashArray=[3, 2]))
    d.add(String(ox + pw, py(yv) + 4, "scale of first reachable halting value (124313)",
                 fontName="Helvetica-Oblique", fontSize=6.8, fillColor=ACCENT,
                 textAnchor="end"))
    # the orbit polyline + points
    pts = []
    for k, v in enumerate(_ORBIT_LOG):
        pts.extend([px(k), py(v)])
    d.add(PolyLine(pts, strokeColor=BLUE, strokeWidth=1.4))
    for k, v in enumerate(_ORBIT_LOG):
        d.add(Circle(px(k), py(v), 1.6, fillColor=BLUE, strokeColor=BLUE))
    # annotation of geometric growth
    d.add(String(px(2), py(9.6), "Dk grows x2.4 per cycle on average",
                 fontName="Helvetica-Bold", fontSize=7.5, fillColor=BLUE,
                 textAnchor="start"))
    d.add(String(px(2), py(9.0), "(never below x1.0002) - a jagged, "
                 "geometric escape that never settles",
                 fontName="Helvetica-Oblique", fontSize=7, fillColor=GREY,
                 textAnchor="start"))
    d.hAlign = "CENTER"
    return d

def _arc(A, B, lift, n=16):
    """Sample an upward-bulging arc from screen point A to B (for excursions)."""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = A[0] + (B[0] - A[0]) * t
        y = A[1] + (B[1] - A[1]) * t + 4 * lift * t * (1 - t)
        pts.extend([x, y])
    return pts

def anchors_diagram():
    """Figure 3: the a = 0 plane of anchors, with excursions leaving and returning."""
    W, H = 468, 250
    d = Drawing(W, H)
    # oblique projection of the a = 0 plane: (b, d) -> screen
    ox, oy = 58, 52
    bs, dxd, dyd = 250.0, 95.0, 66.0     # b-extent, depth vector
    BMAX, DMAX = 10.0, 10.0
    def pl(b, dd, a=0.0):
        return (ox + bs * b / BMAX + dxd * dd / DMAX,
                oy + dyd * dd / DMAX + 7.0 * a)
    P00, P10, P11, P01 = pl(0, 0), pl(BMAX, 0), pl(BMAX, DMAX), pl(0, DMAX)
    d.add(Polygon([*P00, *P10, *P11, *P01], fillColor=HexColor("#eef3fa"),
                  strokeColor=BLUE, strokeWidth=1))
    d.add(String(P11[0] + 4, P11[1] - 4, "a = 0 plane", fontName="Helvetica-Bold",
                 fontSize=8, fillColor=BLUE, textAnchor="start"))
    # in-plane axes
    d.add(String((P00[0] + P10[0]) / 2, P00[1] - 13, "b", fontName="Helvetica-Oblique",
                 fontSize=9, fillColor=GREY, textAnchor="middle"))
    d.add(String((P00[0] + P01[0]) / 2 - 14, (P00[1] + P01[1]) / 2, "d",
                 fontName="Helvetica-Oblique", fontSize=9, fillColor=GREY,
                 textAnchor="middle"))
    # the a axis rising out of the plane
    d.add(Line(P00[0], P00[1], P00[0], P00[1] + 118, strokeColor=GREY,
               strokeWidth=0.8, strokeDashArray=[2, 2]))
    d.add(Polygon([P00[0], P00[1] + 125, P00[0] - 3, P00[1] + 117,
                   P00[0] + 3, P00[1] + 117], fillColor=GREY, strokeColor=GREY))
    d.add(String(P00[0] - 5, P00[1] + 116, "a", fontName="Helvetica-Oblique",
                 fontSize=9, fillColor=GREY, textAnchor="end"))
    # the section b = 1, where F lives
    S0, S1 = pl(1.0, 0), pl(1.0, DMAX)
    d.add(Line(S0[0], S0[1], S1[0], S1[1], strokeColor=ACCENT, strokeWidth=1.4))
    d.add(String(150, 136, "section b = 1", fontName="Helvetica-Bold",
                 fontSize=7.5, fillColor=ACCENT, textAnchor="end"))
    # anchors: two on the section (start/end of a super-cycle) + interior ones
    A0 = pl(1.0, 1.6)                    # (1, D_k)
    A1, A2, A3 = pl(4.2, 3.1), pl(7.4, 5.2), pl(3.0, 7.4)
    A4 = pl(1.0, 8.8)                    # (1, D_k+1)
    for pt in (A1, A2, A3):
        d.add(Circle(pt[0], pt[1], 2.6, fillColor=BLUE, strokeColor=BLUE))
    for pt in (A0, A4):
        d.add(Circle(pt[0], pt[1], 3.4, fillColor=ACCENT, strokeColor=ACCENT))
    d.add(String(A0[0] - 6, A0[1] - 3, "(1, D_k)", fontName="Helvetica-Bold",
                 fontSize=7.5, fillColor=ACCENT, textAnchor="end"))
    d.add(String(A4[0] - 6, A4[1] - 3, "(1, D_k+1)", fontName="Helvetica-Bold",
                 fontSize=7.5, fillColor=ACCENT, textAnchor="end"))
    # excursions: each leaves the plane (a > 0) and lands on the next anchor
    for (S, E, lf) in ((A0, A1, 26), (A1, A2, 20), (A2, A3, 30), (A3, A4, 22)):
        d.add(PolyLine(_arc(S, E, lf), strokeColor=BLUE, strokeWidth=1.2))
    d.add(String(147, 84, "G", fontName="Helvetica-BoldOblique",
                 fontSize=8, fillColor=BLUE, textAnchor="middle"))
    d.add(String(234, 232, "Anchors live on a = 0; every rule chain leaves the plane "
                 "(a > 0) and lands back on it",
                 fontName="Helvetica-Bold", fontSize=8, fillColor=HexColor("#333333"),
                 textAnchor="middle"))
    d.add(String(234, 220, "one super-cycle = the excursions from one b = 1 anchor "
                 "to the next  ->  D_k+1 = F(D_k)",
                 fontName="Helvetica-Oblique", fontSize=7.5, fillColor=GREY,
                 textAnchor="middle"))
    d.add(String(252, 132, "excursion: a > 0",
                 fontName="Helvetica-Oblique", fontSize=7, fillColor=BLUE,
                 textAnchor="middle"))
    d.hAlign = "CENTER"
    return d

def f_cases_diagram():
    """Figure 4: the three possible fates of a super-cycle."""
    W, H = 468, 222
    d = Drawing(W, H)
    d.add(Line(52, 24, 52, 196, strokeColor=ACCENT, strokeWidth=1.2))
    d.add(String(52, 202, "section b = 1", fontName="Helvetica-Bold", fontSize=7.5,
                 fillColor=ACCENT, textAnchor="middle"))
    start = (52, 112)
    d.add(Circle(*start, 4, fillColor=ACCENT, strokeColor=ACCENT))
    d.add(String(46, 108, "(1, D_k)", fontName="Helvetica-Bold", fontSize=8,
                 fillColor=ACCENT, textAnchor="end"))
    rows = [
        (178, "(i)  hits H", "HALT", HexColor("#a33"),
         "machine halts;  D_k is in H"),
        (112, "(ii)  returns", "(1, D_k+1)", BLUE,
         "F is defined here;  continue to the next cycle"),
        (46, "(iii)  never returns", "wanders forever", HexColor("#777777"),
         "infinite run among anchors with b != 1;  never halts"),
    ]
    for (y, lab, box, col, note) in rows:
        d.add(PolyLine(_arc(start, (236, y), 10 if y != 112 else 0),
                       strokeColor=col, strokeWidth=1.2))
        d.add(Polygon([243, y, 235, y + 3.5, 235, y - 3.5], fillColor=col,
                      strokeColor=col))
        d.add(String(150, y + (10 if y != 112 else 6), lab,
                     fontName="Helvetica-Bold", fontSize=8, fillColor=col,
                     textAnchor="middle"))
        d.add(Rect(248, y - 11, 108, 22, rx=4, ry=4,
                   fillColor=HexColor("#f6f8fb"), strokeColor=col, strokeWidth=1))
        d.add(String(302, y - 3, box, fontName="Helvetica-Bold", fontSize=8.5,
                     fillColor=col, textAnchor="middle"))
        d.add(String(302, y - 21, note, fontName="Helvetica-Oblique", fontSize=6.9,
                     fillColor=GREY, textAnchor="middle"))
    # case (ii) loops back to the section
    d.add(PolyLine([302, 101, 302, 78, 52, 78, 52, 104], strokeColor=BLUE,
                   strokeWidth=0.9, strokeDashArray=[3, 2]))
    d.add(Polygon([52, 100, 49, 108, 55, 108], fillColor=BLUE, strokeColor=BLUE))
    d.add(String(104, 70, "iterate", fontName="Helvetica-Oblique", fontSize=7,
                 fillColor=BLUE, textAnchor="middle"))
    d.add(Line(8, 14, 460, 14, strokeColor=HexColor("#c9b45a"), strokeWidth=0.6,
               strokeDashArray=[2, 2]))
    d.add(String(234, 4, "(ii) and (iii) are both non-halting, so \"halts iff the "
                 "orbit meets H\" needs no assumption that returns happen",
                 fontName="Helvetica-Oblique", fontSize=7.2,
                 fillColor=HexColor("#8a7a2a"), textAnchor="middle"))
    d.hAlign = "CENTER"
    return d

# Collatz trajectory of 27 (log10), and our orbit (log10) — computed once
_COLLATZ27 = [1.43, 1.91, 1.61, 2.09, 1.79, 1.49, 1.97, 1.67, 2.15, 1.85, 2.33,
              2.03, 2.51, 2.21, 2.68, 2.38, 2.08, 2.56, 2.26, 1.96, 2.44, 2.14,
              2.61, 2.31, 2.01, 2.49, 2.19, 2.67, 2.37, 2.85, 2.54, 2.24, 2.72,
              2.42, 2.9, 2.6, 3.07, 2.77, 3.25, 2.95, 2.65, 3.13, 2.82, 2.52,
              2.22, 2.7, 2.4, 2.88, 2.58, 3.05, 2.75, 2.45, 2.93, 2.63, 3.11,
              2.8, 2.5, 2.98, 2.68, 3.16, 2.86, 3.33, 3.03, 3.51, 3.21, 3.69,
              3.39, 3.86, 3.56, 3.26, 2.96, 3.44, 3.14, 3.61, 3.31, 3.79, 3.49,
              3.97, 3.66, 3.36, 3.06, 2.76, 3.24, 2.94, 2.64, 3.11, 2.81, 2.51,
              2.99, 2.69, 2.39, 2.09, 1.79, 2.26, 1.96, 1.66, 1.36, 1.85, 1.54,
              2.03, 1.72, 2.2, 1.9, 1.6, 1.3, 1.0, 0.7, 1.2, 0.9, 0.6, 0.3, 0.0]
# log10 of every element of H below 3e6 (the targets this machine must dodge)
_H_LOG = [0.3, 0.48, 0.95, 1.2, 1.28, 1.41, 1.45, 1.59, 1.64, 1.69, 1.96, 2.01,
          2.21, 2.25, 2.34, 2.53, 2.54, 2.66, 2.88, 2.93, 2.94, 2.97, 3.12,
          3.28, 3.46, 3.52, 3.56, 3.58, 3.74, 3.84, 3.88, 4.02, 4.14, 4.19,
          4.2, 4.36, 4.49, 4.7, 4.75, 4.79, 4.81, 5.06, 5.09, 5.09, 5.32, 5.36,
          5.39, 5.65, 5.69, 5.7, 5.83, 5.87, 5.9, 5.92, 5.92, 5.99, 6.0, 6.29,
          6.44, 6.47]
_H_REACH_LOG = [0.95, 5.09]        # the two reachable (9 mod 16) targets

def collatz_vs_machine_diagram():
    """Figure 5: a fixed target that must be HIT vs a growing target set to be MISSED."""
    W, H = 468, 246
    d = Drawing(W, H)
    pw, ph, oy = 196, 150, 44
    for (ox, title, sub) in ((30, "Collatz (3n+1), start 27",
                              "wanders, then must come DOWN to a fixed target"),
                             (256, "This machine, start D = 17",
                              "climbs, and must DODGE targets that grow with it")):
        d.add(Line(ox, oy, ox, oy + ph, strokeColor=HexColor("#888888")))
        d.add(Line(ox, oy, ox + pw, oy, strokeColor=HexColor("#888888")))
        d.add(String(ox + pw / 2, oy + ph + 26, title, fontName="Helvetica-Bold",
                     fontSize=8.5, fillColor=HexColor("#333333"), textAnchor="middle"))
        d.add(String(ox + pw / 2, oy + ph + 14, sub, fontName="Helvetica-Oblique",
                     fontSize=7.2, fillColor=GREY, textAnchor="middle"))

    # ---- left panel: Collatz(27), own vertical scale ----
    ox, ymaxL = 30, 4.3
    n = len(_COLLATZ27) - 1
    def lx(i): return ox + pw * i / n
    def ly(v): return oy + ph * v / ymaxL
    for t in range(0, 5):
        d.add(String(ox - 5, ly(t) - 3, str(t), fontName="Helvetica", fontSize=6.5,
                     fillColor=GREY, textAnchor="end"))
    d.add(Line(ox, ly(0), ox + pw, ly(0), strokeColor=ACCENT, strokeWidth=1.1,
               strokeDashArray=[3, 2]))
    d.add(String(ox + pw, ly(0) + 5, "target: 1  (a single fixed point)",
                 fontName="Helvetica-BoldOblique", fontSize=6.8, fillColor=ACCENT,
                 textAnchor="end"))
    pts = []
    for i, v in enumerate(_COLLATZ27):
        pts.extend([lx(i), ly(v)])
    d.add(PolyLine(pts, strokeColor=BLUE, strokeWidth=1.0))
    d.add(Circle(lx(n), ly(0), 3, fillColor=ACCENT, strokeColor=ACCENT))
    d.add(String(ox + pw / 2, oy - 13, "step  (111 of them)", fontName="Helvetica",
                 fontSize=7, fillColor=GREY, textAnchor="middle"))
    d.add(String(ox + 4, oy + ph - 8, "reaches it: HALT", fontName="Helvetica-Bold",
                 fontSize=7.2, fillColor=ACCENT, textAnchor="start"))

    # ---- right panel: this machine, own vertical scale ----
    ox, ymaxR, K = 256, 7.6, 14
    orb = _ORBIT_LOG[:K + 1]
    def rx(k): return ox + pw * k / K
    def ry(v): return oy + ph * v / ymaxR
    for t in range(0, 8, 2):
        d.add(String(ox - 5, ry(t) - 3, str(t), fontName="Helvetica", fontSize=6.5,
                     fillColor=GREY, textAnchor="end"))
    for v in _H_LOG:                       # the target field, at every scale
        if v <= ymaxR:
            d.add(Line(ox + 2, ry(v), ox + pw, ry(v),
                       strokeColor=HexColor("#dcdcdc"), strokeWidth=0.6))
    for v in _H_REACH_LOG:
        d.add(Line(ox + 2, ry(v), ox + pw, ry(v), strokeColor=ACCENT,
                   strokeWidth=0.9, strokeDashArray=[2, 2]))
    pts = []
    for k, v in enumerate(orb):
        pts.extend([rx(k), ry(v)])
    d.add(PolyLine(pts, strokeColor=BLUE, strokeWidth=1.5))
    for k, v in enumerate(orb):
        d.add(Circle(rx(k), ry(v), 1.7, fillColor=BLUE, strokeColor=BLUE))
    d.add(String(ox + pw / 2, oy - 13, "super-cycle k", fontName="Helvetica",
                 fontSize=7, fillColor=GREY, textAnchor="middle"))
    d.add(String(ox + 4, oy + ph - 8, "misses every one: no halt",
                 fontName="Helvetica-Bold", fontSize=7.2, fillColor=BLUE,
                 textAnchor="start"))
    d.add(String(ox + pw, oy + 7, "grey: H      red: reachable H (9 mod 16)",
                 fontName="Helvetica-Oblique", fontSize=6.8, fillColor=GREY,
                 textAnchor="end"))

    g = Group(String(0, 0, "log10 of the value", fontName="Helvetica", fontSize=7.5,
                     fillColor=HexColor("#333333"), textAnchor="middle"))
    g.translate(12, oy + ph / 2); g.rotate(90)
    d.add(g)
    d.add(Line(8, 16, 460, 16, strokeColor=HexColor("#c9b45a"), strokeWidth=0.6,
               strokeDashArray=[2, 2]))
    d.add(String(234, 6, "Collatz asks whether a wandering orbit HITS one fixed "
                 "point; this machine asks whether a growing orbit MISSES an "
                 "infinite, growing set - forever",
                 fontName="Helvetica-Oblique", fontSize=7.2,
                 fillColor=HexColor("#8a7a2a"), textAnchor="middle"))
    d.hAlign = "CENTER"
    return d

def add_part(story, label, subtitle):
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1.2,
                            color=colors.HexColor("#1a3c6e"),
                            spaceBefore=2, spaceAfter=6))
    story.append(P(label, PART))
    story.append(P(subtitle, PARTSUB))

def table_style(header=True):
    s = [
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c4d6")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        s += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef7")),
              ("ROWBACKGROUNDS", (0, 1), (-1, -1),
               [colors.white, colors.HexColor("#f6f8fb")])]
    else:
        s += [("ROWBACKGROUNDS", (0, 0), (-1, -1),
               [colors.white, colors.HexColor("#f6f8fb")])]
    return TableStyle(s)

def rule_table(rows, header, widths, italic_cols=None):
    """rows: list of tuples of cell strings; italic_cols: set of column indices
    rendered in the math (italic) style."""
    italic_cols = italic_cols if italic_cols is not None else set()
    data = [[P(f"<b>{h}</b>", CELLR) for h in header]]
    for r in rows:
        data.append([P(c, CELL if i in italic_cols else CELLR)
                     for i, c in enumerate(r)])
    t = Table(data, colWidths=list(widths), repeatRows=1)
    t.setStyle(table_style())
    return t

story = []

# ============================== Title ==================================
story.append(P("Acceleration and Cryptid Structure of a Collatz-Like Machine", TITLE))
story.append(P("Compressing a 13-rule machine to a one-integer map &mdash; and the "
               "open halting problem at its core", SUB))

# ========================== 1. Overview ================================
story.append(P("1. Overview", H1))
story.append(P(
    "The subject of this report is the deterministic rewriting system "
    "<i>NextConfig(a, b, c, d)</i>: a machine whose <b>configuration</b> is a "
    "quadruple of non-negative integers and whose evolution is given by 13 "
    "<b>guarded rules</b>. A guarded rule is a statement &ldquo;if the current "
    "configuration satisfies condition X (the <i>guard</i>), replace it by "
    "expression Y&rdquo;; a rule whose guard holds is said to <i>fire</i>. The 13 "
    "guards are mutually exclusive and cover every configuration, so exactly one "
    "rule fires at each step and the system is deterministic. One rule is "
    "<b>HALT</b>: when its guard holds, the machine stops. The full rule set is "
    "reproduced in Section 2."))
story.append(P(
    "The report has two goals, and they are the same investigation seen from "
    "two ends. The first is to <b>accelerate</b> the machine: from most starts "
    "its counters grow geometrically, so a direct step-by-step simulation "
    "dies within a few thousand steps, and we replace it by an exactly "
    "equivalent but exponentially faster system. The second is to use that "
    "acceleration to <b>determine what the machine does</b> &mdash; in "
    "particular whether it halts from the all-zero start &mdash; and the "
    "answer is that it is a <b>cryptid</b>: a tiny, fully explicit program "
    "whose halting question is provably equivalent to an open problem of "
    "Collatz type. These goals are not independent. The acceleration is what "
    "makes the halting question <i>sayable</i>: only after compressing the "
    "machine to a single integer can one see the map, the exceptional set, "
    "and the pseudorandom orbit whose analysis reveals the cryptid. The "
    "hierarchy does not stall short of an answer; it runs until its next step "
    "and the halting question become literally the same object."))
story.append(P(
    "The engine of the acceleration is <b>batching</b>: when the same rule (or "
    "a fixed sequence of rules) provably fires many times in a row, the whole "
    "run is replaced by a single <b>closed-form</b> jump &mdash; one formula "
    "evaluated in place of an iteration. Every accelerated rule carries an "
    "exact <b>step certificate</b> counting the base steps it replaces, so the "
    "equivalence is <i>step-exact</i>, not merely behavioral: the accelerated "
    "systems visit exactly the states the original machine visits, at exactly "
    "the claimed step numbers. Every technical claim about this machine was "
    "verified mechanically against the original rules (Section 10)."))
story.append(P("<b>Part I</b> builds a four-level acceleration hierarchy:"))
lvl_rows = [
    ("<b>Level 1</b> &mdash; variable elimination", "c is a pure transfer buffer",
     "4 variables &rarr; 3"),
    ("<b>Level 2</b> &mdash; loop batching", "single-rule loops replaced by closed forms",
     "each rule O(1) arithmetic"),
    ("<b>Level 3</b> &mdash; cascade batching",
     "two-rule loops batched geometrically (2<super>n</super>, 4<super>n</super>)",
     "~9&times; fewer macro steps"),
    ("<b>Level 4</b> &mdash; start-specific reduction",
     "from (0, 0, 0, 0) the machine is a one-integer return map D &rarr; F(D)",
     "~60&times; faster deep runs"),
]
t = Table([[P(a, CELLR), P(b, CELLR), P(c, CELLR)] for a, b, c in lvl_rows],
          colWidths=[2.4*inch, 2.7*inch, 1.8*inch])
t.setStyle(table_style(header=False))
story.append(t)
story.append(Spacer(1, 10))
story.append(compression_diagram())
story.append(P(
    "<b>Figure 1.</b> The variable compression. Level 1 eliminates the buffer "
    "c; restricting to the states the orbit actually revisits &mdash; anchors "
    "(a = 0), then the section b = 1 &mdash; removes a and then b, leaving the "
    "single integer D whose map is F. Levels 2&ndash;3 do not remove variables "
    "but batch rules, turning astronomically long step-runs into single "
    "closed-form jumps.", FIGCAP))
story.append(P(
    "To cover 10<super>60</super> base steps from a typical start, the level-2 "
    "system needs about 8,700 of its own steps and the level-3 system about "
    "1,000 &mdash; each of constant cost &mdash; so total simulation work is "
    "polylogarithmic in the base step count. <b>Part II</b> then turns the "
    "compressed machine on itself. It proves an exact halting criterion "
    "(Section 8.1), reduces halting from (0, 0, 0, 0) to a single "
    "orbit-avoidance question (Section 8.3), certifies that the machine does "
    "not halt within its first 10<super>150,514</super> steps (Section 8.4), "
    "and shows in Section 9 why the residual question &mdash; like the Collatz "
    "conjecture &mdash; is believed but not provable: the machine is a cryptid. "
    "Three closing sections (10&ndash;12) collect the verification, "
    "performance, and code."))

# ======================= PART I =======================================
add_part(story, "Part I &mdash; Accelerating the machine",
         "Four levels of exact reduction turn an intractable 13-rule machine into "
         "the iteration of one integer. Each rule of each level carries a "
         "certificate for the base steps it replaces, so equivalence is "
         "step-exact throughout.")

# ======================= 2. The base system ============================
story.append(P("2. The base system", H1))
story.append(P(
    "The original system, exactly as specified &mdash; with each guard&rsquo;s "
    "conditions restated in variable order a, b, c, d for readability (a guard "
    "is a conjunction, so ordering does not change its meaning). Each "
    "configuration is "
    "(a, b, c, d), four non-negative integers; the guards below are mutually "
    "exclusive (their order does not matter) and complete (every configuration "
    "satisfies exactly one). We give each rule two labels, used interchangeably "
    "throughout the report: a number R1&ndash;R13, and a mnemonic name:"))
story.append(Spacer(1, 4))
story.append(rule_table([
    ("R1", "transfer", "(a, b + 1, c &minus; 1, d)", "c &gt; 0"),
    ("R2", "recharge", "(a + 1, 0, 0, 2b + 2)", "c = 0, d = 0"),
    ("R3", "drain", "(a &minus; 3, b + 2, 0, d &minus; 1)",
     "a &ge; 3, c = 0, d &gt; 0"),
    ("R4", "two", "(0, 0, b + 1, d &minus; 1)", "a = 2, c = 0, d &gt; 0"),
    ("R5", "pump", "(1, 1, b + 1, d &minus; 1)",
     "a = 1, b &gt; 0, c = 0, d &gt; 0"),
    ("R6", "jump", "(0, 0, 0, d + 2)", "a = 1, b = 0, c = 0, d &gt; 0"),
    ("R7", "seed", "(0, 0, 2, 5)", "a = 0, b = 0, c = 0, d = 1"),
    ("R8", "seed", "(0, 0, 2, 2b + 1)", "a = 0, b &gt; 0, c = 0, d = 1"),
    ("R9", "expand", "(3d &minus; 4, 1, 2, 2b &minus; 2d + 3)",
     "a = 0, b &ge; d &minus; 1, c = 0, d &ge; 2"),
    ("R10", "reset3", "(3b + 2, 0, 0, 6)", "a = 0, c = 0, d &ge; 2, d = b + 3"),
    ("R11", "reset4", "(3b + 4, 0, 0, 4)", "a = 0, c = 0, d &ge; 2, d = b + 4"),
    ("R12", "shrink", "(3b + 3, 2, 0, d &minus; b &minus; 5)",
     "a = 0, c = 0, d &ge; 2, d &ge; b + 5"),
    ("R13", "halt", "<b>HALT</b>", "a = 0, c = 0, d &ge; 2, d = b + 2"),
], header=("#", "Name", "Next configuration", "Guard"),
   widths=(0.5*inch, 0.8*inch, 2.75*inch, 2.85*inch), italic_cols={2, 3}))
story.append(Spacer(1, 6))
story.append(P(
    "The names describe what each rule does to the configuration: "
    "<b>transfer</b> moves one unit from c to b; <b>recharge</b> refills d "
    "(with 2b + 2) when it is empty, resetting b and incrementing a; "
    "<b>drain</b> drains a, three at a time, into b, consuming d; <b>two</b> "
    "is the a = 2 case, handing b onward through c; <b>pump</b> pumps b up "
    "while d ticks down; <b>jump</b> jumps d up by 2; <b>seed</b> seeds a "
    "fresh d from b when d = 1 (two guard cases, same role); <b>expand</b> "
    "expands a to about 3d and d to about 2b; <b>reset3</b>/<b>reset4</b> "
    "reset b to 0 with a small fixed d; <b>shrink</b> shrinks d by b + 5 while "
    "tripling b into a."))
story.append(P(
    "A <b>trajectory</b> is the sequence of configurations produced by firing "
    "rules repeatedly; the machine <b>halts</b> if it ever reaches a "
    "configuration satisfying R13&rsquo;s guard. Note the scale of the problem: "
    "from most starts the values grow without bound (Section 7), so direct "
    "simulation quickly becomes impossible &mdash; from (0, 0, 0, 0) the values "
    "are astronomically large within a few thousand of the accelerated steps "
    "defined below."))

# ================ 3. Three structural observations =====================
story.append(P("3. Three structural observations", H1))
story.append(P("3.1&nbsp;&nbsp;The variable c is a transfer buffer (Level 1)", H2))
story.append(P(
    "R1 (transfer) is the only rule that fires when c &gt; 0, and it simply moves one unit "
    "from c to b. Applying it c times in a row telescopes:"))
story.append(P(
    "(a, b, c, d) &rarr; (a, b + 1, c &minus; 1, d) &rarr; &#8230; &rarr; "
    "(a, b + c, 0, d)&nbsp;&nbsp;&nbsp;&nbsp;[c base steps],", MATHC))
story.append(P(
    "and every rule that writes a positive c (R4, R5, R7, R8, R9) is immediately "
    "followed by exactly this transfer, because no other rule can fire while "
    "c &gt; 0. So c never carries information: the system is fully described on "
    "triples via the projection (a, b, c, d) &rarr; (a, b + c, d). This "
    "eliminates one variable and the transfer rule outright &mdash; that is Level 1."))

story.append(P("3.2&nbsp;&nbsp;Two rules are unary loops", H2))
story.append(P(
    "Call a rule a <b>unary loop</b> if firing it re-establishes its own guard, "
    "so the <i>same</i> rule fires again and again until a counter runs out "
    "(&ldquo;unary&rdquo; because the loop body is a single rule; Level 3 will "
    "handle loops whose body is a fixed <i>sequence</i> of rules). A unary loop "
    "is what makes batching possible: the whole run of consecutive firings is a "
    "predictable arithmetic progression, so it collapses to one formula."))
story.append(P(
    "<b>Why R3 (drain) is a unary loop.</b> R3&rsquo;s guard is a &ge; 3, c = 0, "
    "d &gt; 0, and its update adds (&minus;3, +2, 0, &minus;1) to "
    "(a, b, c, d). Two things follow. First, the update leaves c = 0, so no "
    "other rule can interpose. Second, the update moves only a and d toward "
    "their guard boundaries, by fixed amounts &mdash; so whether the guard "
    "still holds after a firing depends only on how far a and d were from those "
    "boundaries. Concretely, after j consecutive firings the configuration is, "
    "by induction,"))
story.append(P(
    "(a, b, 0, d) &rarr; (a &minus; 3j, b + 2j, 0, d &minus; j),", MATHC))
story.append(P(
    "and firing number j + 1 is allowed exactly when a &minus; 3j &ge; 3 and "
    "d &minus; j &gt; 0 &mdash; equivalently j + 1 &le; floor(a/3) and "
    "j + 1 &le; d. So the run has length exactly"))
story.append(P(
    "k = min( floor(a/3), d ),", MATHC))
story.append(P(
    "and the entire run collapses to the single jump (a, b, d) &rarr; "
    "(a &minus; 3k, b + 2k, d &minus; k), with step certificate k. Two small "
    "examples: from (11, 0, 2): (11, 0, 2) &rarr; (8, 2, 1) &rarr; (5, 4, 0), "
    "stopped by d hitting 0, and indeed k = min(floor(11/3), 2) = min(3, 2) = "
    "2. From (7, 0, 5): (7, 0, 5) &rarr; (4, 2, 4) &rarr; (1, 4, 3), stopped by "
    "a dropping below 3, and k = min(2, 5) = 2."))
story.append(P(
    "<b>R5 (pump) is a loop one level up.</b> R5 alone does not re-establish its own "
    "guard (it sets c = b + 1 &gt; 0), but the c &gt; 0 it creates forces "
    "exactly b + 1 firings of R1, after which the configuration has returned to "
    "the original <i>shape</i>:"))
story.append(P(
    "(1, b, 0, d) &rarr;<super>R5</super> (1, 1, b + 1, d &minus; 1) "
    "&rarr;<super>R1&times;(b+1)</super> (1, b + 2, 0, d &minus; 1),", MATHC))
story.append(P(
    "&mdash; same a = 1, b grown by 2 (so still positive), same c = 0, d shrunk "
    "by 1. The loop body is thus the fixed sequence (R5, R1&times;(b+1)), and "
    "only d moves toward a boundary, so the loop runs exactly d rounds. "
    "Section 4.1 turns this into the pump rule and sums its cost. Batching "
    "these two loops is the heart of Level 2."))

story.append(P("3.3&nbsp;&nbsp;The long-run dynamics is a linear map", H2))
story.append(P(
    "Empirically, about 85% of all level-2 steps consist of one particular "
    "two-rule alternation: R12 (shrink) followed by a full drain run. Why does that run "
    "return to a = 0? Because R12 outputs a = 3b + 3 = 3(b + 1), a multiple of "
    "3 &mdash; so the drain loop of Section 3.2, which subtracts 3 per firing, can "
    "consume a completely (when d lasts long enough, which the guard "
    "d &ge; 2b + 6 guarantees; Section 5.1 does the arithmetic). The "
    "composition is the <b>affine map</b> (a linear map plus constants)"))
story.append(P("(b, d) &rarr; (2b + 4, d &minus; 2b &minus; 6)"
               "&nbsp;&nbsp;&nbsp;&nbsp;while d &ge; 2b + 6,", MATHC))
story.append(P(
    "and iterating an affine map n times has a geometric closed form (powers of "
    "2 appear because b is doubled each round). Batching such two-rule loops "
    "&mdash; we call them <b>cascades</b> &mdash; is Level 3."))

# ==================== 4. Level 2: the compressed system ================
story.append(P("4. The compressed system (Level 2)", H1))
story.append(P(
    "The level-2 system acts on triples (a, b, d); an original configuration "
    "embeds as (a, b, c, d) &rarr; (a, b + c, d). We call its states <b>macro "
    "states</b> and its rule applications <b>macro steps</b>; each macro step "
    "bundles one or more base steps. The guards below are, like the base "
    "table&rsquo;s, mutually exclusive and complete, so order does not matter "
    "(provable by a short case analysis of d against b &mdash; the partition "
    "lemma of Section 6.1 shows the pattern &mdash; and machine-checked on "
    "60,000 states); "
    "we list the rules in base order with halt last, exactly as in Section 2. "
    "Each rule keeps the <b>index and name</b> of the base rule it "
    "accelerates (new rules at later levels will receive fresh indices R14, "
    "R15, &hellip;). The marker after the name records the rule&rsquo;s "
    "relation to the previous level, in a convention used for every table from "
    "here on: &#8226; = carried over verbatim (here: the identical base rule, "
    "with c dropped); <b>(batch)</b> = the same rule, all consecutive firings "
    "collapsed into one jump; <b>(fuse)</b> = the rule together with the "
    "forced steps that always follow it. The <b>Built from</b> column gives "
    "the exact base composition, and the last column the step certificate:"))
story.append(Spacer(1, 4))
story.append(rule_table([
    ("R2", "recharge &#8226;", "(a + 1, 0, 2b + 2)", "d = 0", "R2", "1"),
    ("R3", "drain (batch)",
     "(a &minus; 3k, b + 2k, d &minus; k),<br/>k = min(floor(a/3), d)",
     "a &ge; 3, d &gt; 0", "R3 &times; k", "k"),
    ("R4", "two (fuse)", "(0, b + 1, d &minus; 1)", "a = 2, d &gt; 0",
     "R4, R1&times;(b+1)", "b + 2"),
    ("R5", "pump (batch+fuse)", "(2, 0, 2b + 4d + 2)",
     "a = 1, b &gt; 0, d &gt; 0",
     "(R5, R1&times;&#183;)&times;d, R2", "bd + d<super>2</super> + d + 1"),
    ("R6", "jump &#8226;", "(0, 0, d + 2)", "a = 1, b = 0, d &gt; 0",
     "R6", "1"),
    ("R7/8", "seed (fuse)", "(0, 2, 2b + 1); (0, 2, 5) if b = 0",
     "a = 0, d = 1", "R8/R7, R1&times;2", "3"),
    ("R9", "expand (fuse)", "(3d &minus; 4, 3, 2b &minus; 2d + 3)",
     "a = 0, b &ge; d &minus; 1, d &ge; 2", "R9, R1&times;2", "3"),
    ("R10", "reset3 &#8226;", "(3b + 2, 0, 6)", "a = 0, d = b + 3, d &ge; 2",
     "R10", "1"),
    ("R11", "reset4 &#8226;", "(3b + 4, 0, 4)", "a = 0, d = b + 4, d &ge; 2",
     "R11", "1"),
    ("R12", "shrink &#8226;", "(3b + 3, 2, d &minus; b &minus; 5)",
     "a = 0, d &ge; b + 5, d &ge; 2", "R12", "1"),
    ("R13", "<b>halt</b> &#8226;", "<b>HALT</b>",
     "a = 0, d = b + 2, d &ge; 2", "R13", "&mdash;"),
], header=("#", "Name", "Next macro state", "Guard", "Built from", "Steps"),
   widths=(0.45*inch, 1.0*inch, 2.05*inch, 1.6*inch, 1.0*inch, 0.8*inch),
   italic_cols={2, 3}))
story.append(Spacer(1, 6))
story.append(P("4.1&nbsp;&nbsp;Where each level-2 rule comes from", H2))
story.append(P(
    "The &#8226; rows (halt, recharge, jump, reset3, reset4, shrink) are single "
    "base rules that neither read nor write c &mdash; they pass to the triple "
    "form unchanged. "
    "The others are compositions, with c eliminated by Section 3.1:"))
story.append(P(
    "<b>two</b> = R4 then the c-transfer: (2, b, 0, d) &rarr; (0, 0, b + 1, "
    "d &minus; 1) &rarr;<super>R1&times;(b+1)</super> (0, b + 1, 0, d &minus; 1); "
    "total 1 + (b + 1) = b + 2 base steps. <b>seed</b> and <b>expand</b> are "
    "R7/R8 and R9 followed by their two c-transfers (3 steps each)."))
story.append(P(
    "<b>drain</b> = R3 iterated. Each firing does (a, b, d) &rarr; (a &minus; 3, "
    "b + 2, d &minus; 1) and R3&rsquo;s guard keeps holding until a &lt; 3 or "
    "d = 0, i.e. for exactly k = min(floor(a/3), d) firings; summing gives "
    "(a &minus; 3k, b + 2k, d &minus; k) in k steps."))
story.append(P(
    "<b>pump</b> = d rounds of (R5 + transfers), then R2. One round: "
    "(1, b, 0, d) &rarr;<super>R5</super> (1, 1, b + 1, d &minus; 1) "
    "&rarr;<super>R1&times;(b+1)</super> (1, b + 2, 0, d &minus; 1) &mdash; net "
    "effect: b becomes b + 2, d becomes d &minus; 1, at cost b + 2. After d rounds "
    "the state is (1, b + 2d, 0, 0); R2 (recharge) then always fires, giving "
    "(2, 0, 0, 2(b + 2d) + 2) = (2, 0, 0, 2b + 4d + 2). Total cost "
    "&Sigma;<sub>i&lt;d</sub>(b + 2i + 2) + 1 = bd + d<super>2</super> + d + 1. "
    "Because the recharge is forced, it is fused into the pump rule."))
story.append(P(
    "Compared with the original: one variable and one rule eliminated, both "
    "loops replaced by closed forms, and every rule now costs a constant amount "
    "of integer arithmetic regardless of the values involved."))

# ==================== 5. Level 3: cascades =============================
story.append(P("5. Cascade super-rules (Level 3)", H1))
story.append(P(
    "Two <i>compositions</i> of level-2 rules are themselves loops: each "
    "composition returns to a state where the same composition applies again. "
    "We write (X; Y)<super>n</super> for n consecutive rounds of firing rule X "
    "then rule Y; such iterates have geometric closed forms. In both cases n is the "
    "largest round count whose guard still holds; because one quantity grows "
    "geometrically while the comparison side moves slowly, n is found by binary "
    "search over a monotone inequality."))

story.append(P("5.1&nbsp;&nbsp;Cascade A: shrink&ndash;drain (~85% of all macro steps)", H2))
story.append(P(
    "One round, derived from the level-2 table: from (0, b, d) with "
    "d &ge; 2b + 6, shrink gives (3b + 3, 2, d &minus; b &minus; 5). Now "
    "floor((3b + 3)/3) = b + 1 and the guard implies d &minus; b &minus; 5 &ge; "
    "b + 1, so the drain runs its full k = b + 1 and lands back on a = 0:"))
story.append(P(
    "(0, b, d) &rarr;<super>shrink</super> (3b + 3, 2, d &minus; b &minus; 5) "
    "&rarr;<super>drain</super> (0, 2 + 2(b + 1), d &minus; b &minus; 5 &minus; "
    "(b + 1)) = (0, 2b + 4, d &minus; 2b &minus; 6),", MATHC))
story.append(P(
    "which is the affine map of Section 3.3, at cost (b + 2) base steps per "
    "round. Iterating while the guard holds &mdash; b doubles-plus-4 each round "
    "&mdash; and summing the geometric series:"))
story.append(P(
    "b<sub>n</sub> = 2<super>n</super>(b + 4) &minus; 4,&nbsp;&nbsp;&nbsp;&nbsp;"
    "d<sub>n</sub> = d &minus; 2(b + 4)(2<super>n</super> &minus; 1) + 2n,&nbsp;&nbsp;&nbsp;&nbsp;"
    "cost = (b + 4)(2<super>n</super> &minus; 1) &minus; 2n base steps.", MATHC))
story.append(P(
    "(To check the first: b<sub>1</sub> = 2(b + 4) &minus; 4 = 2b + 4. The 2n "
    "term in d<sub>n</sub> collects the +4-then-doubled constants.) The batched "
    "rule &mdash; all n rounds in one jump &mdash; is named <b>cascadeA</b>."))

story.append(P("5.2&nbsp;&nbsp;Cascade B: sweep (full-drain + recharge)", H2))
story.append(P(
    "When a &ge; 3d, the drain&rsquo;s k = min(floor(a/3), d) equals d, so the "
    "drain exhausts d completely and recharge is forced next:"))
story.append(P(
    "(a, b, d) &rarr;<super>drain</super> (a &minus; 3d, b + 2d, 0) "
    "&rarr;<super>recharge</super> (a &minus; 3d + 1, 0, 2b + 4d + 2).", MATHC))
story.append(P(
    "Here d roughly quadruples per round while a shrinks, so a cascade has at "
    "most ~log<sub>4</sub>(a) rounds. The first round zeroes b, so later rounds are the b = 0 case; writing w = 6b + 12d + 8 (three times the d-value after round 1, plus 2) and T<sub>j</sub> = "
    "(4<super>j</super> &minus; 1)/3, the state after n rounds is:"))
story.append(P(
    "a<sub>n</sub> = a &minus; 3d + 3n &minus; 2 &minus; wT<sub>n&minus;1</sub>,&nbsp;&nbsp;&nbsp;&nbsp;"
    "d<sub>n</sub> = (w&middot;4<super>n&minus;1</super> &minus; 2)/3 &mdash; check n = 1: (a &minus; 3d + 1, 0, 2b + 4d + 2) as above; these match the sweep row of the table below exactly.", MATHC))
story.append(P("The batched rule is named <b>sweep</b>."))

story.append(P("5.3&nbsp;&nbsp;The complete level-3 system in closed form", H2))
story.append(P(
    "The full accelerated system, with both cascades folded in, is again a "
    "13-rule guarded system &mdash; the same size as the original, but with "
    "every rule a closed-form expression. The sweep captures every state with a &ge; 3d, so "
    "the drain that remains carries the conjunct a &lt; 3d, under which its k simplifies to "
    "floor(a/3). Abbreviations:"))
story.append(P(
    "q = floor(a/3),&nbsp;&nbsp;&nbsp;&nbsp;w = 6b + 12d + 8,&nbsp;&nbsp;&nbsp;&nbsp;"
    "T<sub>j</sub> = (4<super>j</super> &minus; 1)/3,", MATHC))
story.append(P(
    "n<sub>A</sub> = max{ m &ge; 1 : (b + 4)&middot;2<super>m+1</super> &le; "
    "d + 2(b + 4) + 2m },", MATHC))
story.append(P(
    "n<sub>B</sub> = max{ m &ge; 1 : w&middot;4<super>m&minus;1</super> &le; "
    "3(a &minus; 3d) + w + 9(m &minus; 1) }.", MATHC))
story.append(P(
    "n<sub>A</sub> and n<sub>B</sub> are the numbers of rounds the two cascades "
    "run before their guards fail: the inequalities say &ldquo;round m is still "
    "allowed&rdquo;, and since each is monotone in m the maxima are computable "
    "by binary search (up to &plusmn;1 they equal "
    "floor(log<sub>2</sub>((d + 2b + 8)/(2b + 8))) and "
    "floor(log<sub>4</sub>(3(a &minus; 3d)/w)) + 1). In the table, n stands for "
    "n<sub>A</sub> or n<sub>B</sub> as appropriate. Guards are again mutually "
    "exclusive (order-free), listed in base order with halt last; rules keep "
    "their base indices and the two new rules receive the fresh indices R14 "
    "and R15, placed beside the rules they grew out of. Markers as in "
    "Section 4 (&#8226; = carried over from Level 2 verbatim), plus two more: "
    "<b>(new)</b> = a batched two-rule composition that exists only from this "
    "level on, and <b>(mod.)</b> = a Level-2 rule whose formula or guard "
    "changed here &mdash; the changed conjunct is visible in the guard. The "
    "<b>Built from</b> column gives each rule&rsquo;s level-2 origin: for "
    "modified rules, which part of the old guard survives; for new rules, the "
    "batched composition:"))
story.append(Spacer(1, 4))
story.append(rule_table([
    ("R2", "recharge &#8226;", "(a + 1, 0, 2b + 2)", "d = 0", "R2", "1"),
    ("R3", "drain (mod.)", "(a mod 3, b + 2q, d &minus; q)",
     "a &ge; 3, a &lt; 3d, d &gt; 0", "R3<br/>(a &lt; 3d part)", "q"),
    ("R14", "<b>sweep</b> (new)", "(a &minus; 3d + 3n &minus; 2 &minus; "
     "wT<sub>n&minus;1</sub>, 0, (w&middot;4<super>n&minus;1</super> &minus; 2)/3)",
     "a &ge; 3, a &ge; 3d, d &gt; 0", "(R3; R2)<super>n</super>",
     "d + 1 + (wT<sub>n&minus;1</sub> + n &minus; 1)/3"),
    ("R4", "two &#8226;", "(0, b + 1, d &minus; 1)", "a = 2, d &gt; 0", "R4",
     "b + 2"),
    ("R5", "pump &#8226;", "(2, 0, 2b + 4d + 2)", "a = 1, b &gt; 0, d &gt; 0",
     "R5", "bd + d<super>2</super> + d + 1"),
    ("R6", "jump &#8226;", "(0, 0, d + 2)", "a = 1, b = 0, d &gt; 0", "R6", "1"),
    ("R7/8", "seed &#8226;", "(0, 2, 2b + 1); (0, 2, 5) if b = 0",
     "a = 0, d = 1", "R7/8", "3"),
    ("R9", "expand &#8226;", "(3d &minus; 4, 3, 2b &minus; 2d + 3)",
     "a = 0, b &ge; d &minus; 1, d &ge; 2", "R9", "3"),
    ("R10", "reset3 &#8226;", "(3b + 2, 0, 6)", "a = 0, d = b + 3, d &ge; 2",
     "R10", "1"),
    ("R11", "reset4 &#8226;", "(3b + 4, 0, 4)", "a = 0, d = b + 4, d &ge; 2",
     "R11", "1"),
    ("R12", "shrink (mod.)", "(3b + 3, 2, d &minus; b &minus; 5)",
     "a = 0, b + 5 &le; d &le; 2b + 5", "R12<br/>(band part)", "1"),
    ("R15", "<b>cascadeA</b> (new)", "(0, 2<super>n</super>(b + 4) &minus; 4, "
     "d &minus; 2(b + 4)(2<super>n</super> &minus; 1) + 2n)",
     "a = 0, d &ge; 2b + 6", "(R12; R3)<super>n</super>",
     "(b + 4)(2<super>n</super> &minus; 1) &minus; 2n"),
    ("R13", "halt &#8226;", "<b>HALT</b>", "a = 0, d = b + 2, d &ge; 2",
     "R13", "&mdash;"),
], header=("#", "Name", "Next macro state", "Guard", "Built from",
           "Base steps"),
   widths=(0.45*inch, 0.9*inch, 2.15*inch, 1.5*inch, 0.95*inch, 0.95*inch),
   italic_cols={2, 3}))
story.append(Spacer(1, 6))
story.append(P(
    "Exactly four rows differ from Level 2. <b>sweep</b> is new: it is the "
    "batched loop (drain; recharge)<super>n</super> = (R3; R2)<super>n</super> "
    "of Section 5.2. "
    "<b>cascadeA</b> is new: the batched loop (shrink; drain)<super>n</super> "
    "= (R12; R3)<super>n</super> of Section 5.1. <b>drain</b> (R3) is "
    "modified: only its a &lt; 3d part survives (sweep takes the rest), and "
    "under that conjunct k = min(floor(a/3), d) simplifies to "
    "q = floor(a/3). "
    "<b>shrink</b> (R12) is modified only in its guard: cascadeA (R15) captures "
    "d &ge; 2b + 6, so shrink&rsquo;s guard narrows from d &ge; b + 5 to the "
    "band b + 5 &le; d &le; 2b + 5 where cascadeA runs zero rounds; its formula "
    "and cost are untouched. Every other rule (halt, recharge, two, pump, jump, "
    "seed, expand, reset3, reset4) carries over verbatim. The closed forms "
    "&mdash; round counts n, resulting states, and base-step costs &mdash; were "
    "verified against loop implementations on 50,000 random states per cascade "
    "(round counts up to n = 46), and the assembled system on a further 20,000 "
    "random states and full trajectories."))

# ==================== 6. Level 4 =======================================
story.append(P("6. Level 4: the one-dimensional system from (0, 0, 0, 0)", H1))
story.append(P(
    "When the start is fixed at (0, 0, 0, 0), the system compresses one level "
    "further &mdash; to a single integer. This section is the hinge of the "
    "report: it completes the acceleration (Part I) and hands Part II a "
    "one-variable map to interrogate. Because so much rests on it, it "
    "separates definitions, proofs, and verified observations explicitly. Roadmap: <b>6.1</b> defines anchors, "
    "shows that the whole dynamics reduces to an anchor-to-anchor map G given "
    "by a finite closed-form table (including exactly what happens "
    "<i>between</i> anchors), then defines the one-variable return map F and "
    "states precisely which parts of that definition are proved and which are "
    "verified. <b>6.2</b> defines branch words and proves that F is piecewise "
    "affine with countably many pieces &mdash; the exact sense in which F has "
    "no closed form. <b>6.3</b> explains the runner&rsquo;s algorithmics and "
    "why it sits at the complexity floor. <b>6.4</b> assembles the final "
    "11-rule system."))
story.append(P(
    "The logical structure of the reduction deserves emphasis, because its "
    "parts have different statuses. Reduction to anchors is a <i>theorem</i> "
    "(6.1). Reduction to one variable rests on the orbit returning to b = 1 "
    "each cycle &mdash; a property we can verify massively but, as 6.1 "
    "explains, cannot prove. Section 6.1 therefore closes with a case-split "
    "proposition: exactly one of three things can happen to the machine."))
story.append(P(
    "<b>The halting set H, in plain terms.</b> Once the machine is a map "
    "D &rarr; F(D) on a single integer, its whole fate hinges on which "
    "values of D lead, sooner or later, to the HALT rule. Collect those "
    "values into one set:"))
story.append(P(
    "H = { D : starting a super-cycle from D eventually halts }.", MATHC))
story.append(P(
    "H is small and scattered &mdash; the smallest members are 2, 3, 9, 16, "
    "19, &hellip; (from D = 2, for instance, one super-cycle runs "
    "(1, 2) &rarr; (4, 0) &rarr; (0, 12) &rarr; (4, 6) &rarr; HALT). The "
    "machine starts at D = 17 and each super-cycle jumps it to a new value "
    "F(D); halting from (0, 0, 0, 0) is nothing more than the question "
    "<i>does this jumping ever land on a value in H?</i> That single "
    "question is what the rest of the report circles: 6.2&ndash;6.4 build "
    "the machinery of F, Section 8 pins down H exactly and searches for a "
    "landing, and Section 9 explains why &mdash; like the Collatz problem "
    "&mdash; no one can currently prove that it never does. It is worth "
    "saying at the outset where each of the three cases is dealt with:"))
case_rows = [
    ("(i) some super-cycle halts",
     "the machine halts; the D<sub>k</sub> opening that cycle lies in the "
     "halting set H",
     "studied in Section 8; verified never to occur in the first 200,000 "
     "cycles"),
    ("(ii) every super-cycle returns",
     "F is total on the orbit; the machine halts iff the F-orbit ever "
     "meets H",
     "the working hypothesis of 6.2&ndash;6.4 (structure and runner of F); "
     "the open question of Sections 8&ndash;9"),
    ("(iii) some super-cycle never returns",
     "the machine runs forever inside that cycle",
     "<b>fully closed in 6.1</b>: implies non-halting outright; never "
     "observed"),
]
t = Table([[P("<b>Case</b>", CELLR), P("<b>What it means</b>", CELLR),
            P("<b>Where it is handled</b>", CELLR)]] +
          [[P(a, CELLR), P(b, CELLR), P(c, CELLR)] for a, b, c in case_rows],
          colWidths=[1.85*inch, 2.35*inch, 2.7*inch])
t.setStyle(table_style())
story.append(t)
story.append(Spacer(1, 8))
story.append(f_cases_diagram())
story.append(P(
    "<b>Figure 2.</b> The three fates of a super-cycle, and why the reduction "
    "survives the one gap in it. Only case (i) halts; cases (ii) and (iii) are "
    "both infinite runs. So &ldquo;the machine halts iff the orbit meets "
    "H&rdquo; holds whether or not returns to the section can be guaranteed "
    "&mdash; a failure to return would itself certify non-halting.", FIGCAP))
story.append(P(
    "So the only case requiring further work is (i) versus (ii) &mdash; does "
    "the F-orbit meet H? &mdash; and that question is insensitive to the "
    "unproved return property: whichever way case (iii) could have gone, "
    "&ldquo;the machine halts iff the F-orbit meets H&rdquo; stands, and a "
    "failure to return would itself certify non-halting. Everything after "
    "6.1 develops the tools to pursue that one question."))
story.append(P(
    "The motivating observation, from direct simulation: the trajectory "
    "reaches (0, 1, 0, 17) at base step 25, and from then on repeatedly "
    "passes through states of the form (0, 1, 0, D):"))
story.append(P(
    "D: 17, 57, 185, 601, 2265, 5913, 16121, 35177, 71833, &hellip;", MATHC))
story.append(P(
    "Because the system is deterministic and three of the four coordinates "
    "are pinned (a = 0, b = 1, c = 0), the entire future from such a state is "
    "a function of D alone &mdash; two visits with the same D have identical "
    "futures. We call the stretch from one such state to the next a "
    "<b>super-cycle</b>, and write F(D) for the value of d at the next such "
    "state. The <b>F-orbit of 17</b> is the resulting sequence D<sub>0</sub> "
    "= 17, D<sub>k+1</sub> = F(D<sub>k</sub>); D<sub>k</sub> denotes the "
    "value after k super-cycles. Whether the machine is <i>guaranteed</i> to "
    "keep returning to b = 1 states is a fair question; Section 6.1 addresses "
    "it head-on."))
story.append(P("6.1&nbsp;&nbsp;Formalization: the anchor map G", H2))
story.append(P(
    "<b>Definition.</b> An <b>anchor</b> is a macro state with a = 0 (c = 0 "
    "always holds at this level); we write it as the pair (b, d). Anchors are "
    "the right waypoints because the halt state is an anchor, and because the "
    "dynamics keeps producing them, as we now show."))
story.append(Spacer(1, 6))
story.append(anchors_diagram())
story.append(P(
    "<b>Figure 3.</b> Anchors are the states lying in the a = 0 plane. Every "
    "rule chain lifts the state off that plane (a &gt; 0) and provably lands "
    "back on it, so the dynamics is a walk from anchor to anchor &mdash; the "
    "map G. The section b = 1 is a line inside the plane; the excursions "
    "between two of its points make up one super-cycle, and the map it induces "
    "on the remaining coordinate is F.", FIGCAP))
story.append(P(
    "<b>What happens between anchors.</b> Start at any anchor. Exactly one "
    "row of the table below applies &mdash; that is the partition lemma, "
    "proved just below. Each row summarizes a stretch of ordinary level-2/3 execution, "
    "and its <b>Built from</b> column spells that stretch out: it lists, in "
    "order, the level-2/3 rules that fire between this anchor and the next "
    "one. For example, row R17&rsquo;s entry &ldquo;R9; R3; R4&rdquo; means: "
    "from any anchor satisfying R17&rsquo;s guard, the machine fires expand, "
    "then drain, then two, and is then back at an anchor."))
story.append(P(
    "Two facts make this a meaningful summary. <i>The chain is fixed:</i> "
    "although the machine simply fires whichever rule&rsquo;s guard holds, "
    "each row&rsquo;s guard provably forces the <i>same</i> rule sequence "
    "for every anchor satisfying it &mdash; each intermediate state "
    "satisfies the guard of the next rule in the listed chain (this is the "
    "content of the row derivations; the worked example below traces one in "
    "full). The batched rules inside a chain may run for zero or more "
    "iterations, with counts determined by the entering values, but the "
    "pattern of rules never varies. <i>No anchor is skipped:</i> an anchor "
    "is a state with a = 0, and every intermediate state of these chains has "
    "a &gt; 0 (including the d = 0 states, which occur only with a &gt; 0 "
    "there) &mdash; so the chain&rsquo;s endpoint is the <i>first</i> anchor "
    "after the start, and G(b, d) genuinely is the next-anchor map. The one "
    "exception proves the rule: inside a SWEEP, a cascade-B round can land "
    "exactly on a = 0 mid-chain (the A&prime; = 3&Delta;&prime; equality "
    "described below); the SWEEP definition detects this case (A* = 1) and "
    "stops G at that interior anchor, preserving the property. That anchors "
    "always lead to anchors is worth stating as a theorem:"))
story.append(P(
    "<b>Lemma (the guards partition the plane).</b> For every pair (b, d) of "
    "non-negative integers, exactly one of the twelve guards in the table "
    "holds."))
story.append(P(
    "<i>Proof.</i> If d = 0 or d = 1, the first two rows apply and no other "
    "guard can hold: the remaining guards all force d &ge; 2 &mdash; the "
    "explicit conjuncts do so directly; 3d = 2b + 5 has no solution with "
    "d &le; 1 and b &ge; 0; 3d &gt; 2b + 5 with d &le; 1 would force "
    "b &lt; 0; and the rows on and beyond the line d = b + 2 have d &ge; 2 "
    "outright. Now let d &ge; 2 and compare d with b; exactly one of four "
    "cases holds. <b>(1)</b> d &le; b + 1: the rows requiring d &ge; b + 2 "
    "are excluded, and the trichotomy of 3d against 2b + 5 selects exactly "
    "one of R17 (below), R18 (equal), or the pair R19/R20 (above), the last "
    "two split by the dichotomy of 11d against 10b + 24. Conversely, "
    "3d &le; 2b + 5 with d &ge; 2 already implies d &le; b + 1 (since "
    "d &ge; b + 2 gives 3d &ge; 3b + 6 &gt; 2b + 5), which is why R17 and "
    "R18 need not carry that conjunct. <b>(2)</b> d &#8712; {b + 2, b + 3, "
    "b + 4}: exactly one of halt, R21, R22 &mdash; and every other guard "
    "fails there: 3d &ge; 3b + 6 &gt; 2b + 5 excludes R17/R18, "
    "d &gt; b + 1 excludes R19/R20, d &lt; b + 5 excludes R23/R24, and "
    "d &ge; 2b + 6 would force b &le; &minus;2. <b>(3)</b> b + 5 &le; d "
    "&le; 2b + 5: the dichotomy of 15d against 18b + 61 selects exactly one "
    "of R23, R24; all other guards fail as in case (2). <b>(4)</b> "
    "d &ge; 2b + 6: only R25 holds. The four cases cover every d &ge; 2. "
    "<b>QED</b> (The lemma is also machine-checked on 60,000 random "
    "pairs.)"))
story.append(P(
    "<b>Theorem (anchor recurrence).</b> From every anchor other than the "
    "halt state, the machine reaches another anchor after finitely many macro "
    "steps: at most 6 for the non-SWEEP rows, and at most 2n<sub>B</sub> + 6 "
    "for the SWEEP rows. Consequently every trajectory that starts at an "
    "anchor either halts or visits anchors forever, and the anchor map "
    "G(b, d) = next anchor captures the dynamics completely."))
story.append(P(
    "<i>Proof.</i> The partition lemma gives exactly "
    "one applicable row. For the eight non-SWEEP rows, the Built-from chain "
    "is an explicit composition of at most six level-2 rules whose "
    "intermediate states all have a &gt; 0 (the worked example below traces "
    "one), and each such chain ends on a = 0 by the row&rsquo;s derivation "
    "&mdash; verified against composed level-2 steps on 40,000 random "
    "anchors. A SWEEP row runs its prefix of at most three rules, then "
    "cascade B: each round more than quadruples the d-value "
    "(d &rarr; 4d + 2) while a decreases, so the round guard a &ge; 3d fails "
    "after at most log<sub>4</sub> a rounds &mdash; n<sub>B</sub> is finite "
    "&mdash; and the exit chain of at most three further rules again ends on "
    "a = 0. Every case lands on an anchor after finitely many macro steps. "
    "<b>QED</b>"))
story.append(P(
    "Table conventions: guards are mutually exclusive (order-free), listed "
    "with halt last; seed and halt keep their base indices, and the new "
    "anchor-level compositions receive fresh indices R16&ndash;R25, ordered "
    "by the base index of their leading rule. The Base steps column is the "
    "exact certificate; P(&beta;, &delta;) = &beta;&delta; + "
    "&delta;<super>2</super> + &delta; + 1 abbreviates the pump certificate, "
    "and &ldquo;+ sweep&rdquo; adds the certificate of the SWEEP continuation "
    "(closed forms in afterstep25.py):"))
story.append(Spacer(1, 4))
story.append(rule_table([
    ("R16", "recharge+", "(0, 2b + 4)", "d = 0",
     "R2; R6<br/>(recharge; jump)", "2"),
    ("R7/8", "seed &#8226;", "(2, 2b + 1); (2, 5) if b = 0", "d = 1",
     "R7/8 (seed)", "3"),
    ("R17", "expand+", "(2d, 2b &minus; 3d + 4)", "d &ge; 2, 3d &lt; 2b + 5",
     "R9; R3; R4<br/>(expand; drain; two)", "3d + 2"),
    ("R18", "boundary", "(2, 4d &minus; 1)", "3d = 2b + 5",
     "R9; R3; R2; R3<br/>(a, d hit 2, 0 together)", "d + 3"),
    ("R19", "expand-deep", "(6d &minus; 4b &minus; 8, 10b &minus; 11d + 24)",
     "d &le; b + 1, 3d &gt; 2b + 5,<br/>11d &le; 10b + 24",
     "R9; R3; R2; R3<br/>(expand; drain; recharge; drain)", "d + 3"),
    ("R20", "expand-sweep", "SWEEP(9d &minus; 6b &minus; 12, 8b &minus; 8d + 20)",
     "d &le; b + 1, 11d &gt; 10b + 24",
     "R9; R3; R2<br/>(expand; drain; recharge)",
     "2b &minus; 2d + 7 + sweep"),
    ("R21", "reset3+", "SWEEP(3b + 2, 6)", "d = b + 3", "R10 (reset3)",
     "1 + sweep"),
    ("R22", "reset4+", "SWEEP(3b + 4, 4)", "d = b + 4", "R11 (reset4)",
     "1 + sweep"),
    ("R23", "<b>exit</b>", "(1, 16(d &minus; b) &minus; 55)",
     "b + 5 &le; d &le; 2b + 5,<br/>15d &gt; 18b + 61",
     "R12; R3; R2; R3; R5; R4<br/>(shrink; drain; recharge; drain; pump; two)",
     "b + 5 +<br/>P(4b &minus; 2d + 12,<br/>5d &minus; 6b &minus; 20)"),
    ("R24", "shrink-sweep", "SWEEP(6b &minus; 3d + 19, 4d &minus; 4b &minus; 14)",
     "b + 5 &le; d &le; 2b + 5,<br/>15d &le; 18b + 61",
     "R12; R3; R2<br/>(shrink; drain; recharge)",
     "d &minus; b &minus; 3 + sweep"),
    ("R25", "round", "(2b + 4, d &minus; 2b &minus; 6)", "d &ge; 2b + 6",
     "R12; R3 (shrink; drain):<br/>one R15 round", "b + 2"),
    ("R13", "halt &#8226;", "<b>HALT</b>", "d = b + 2", "R13 (halt)",
     "&mdash;"),
], header=("#", "Name", "Next anchor G(b, d)", "Guard", "Built from",
           "Base steps"),
   widths=(0.45*inch, 0.85*inch, 1.7*inch, 1.4*inch, 1.55*inch, 0.95*inch),
   italic_cols={2, 3}))
story.append(Spacer(1, 6))
story.append(P(
    "SWEEP(A, &Delta;) abbreviates the continuation from the state "
    "(A, 0, &Delta;): cascade B runs its n<sub>B</sub> closed-form rounds to the "
    "exit (A*, 0, &Delta;*); A* = 1 signals that the last round began at values A&prime;, &Delta;&prime; with "
    "A&prime; = 3&Delta;&prime; exactly, so G stops at the interior anchor "
    "((&Delta;* &minus; 2)/2, 0); otherwise the exit drains fully with "
    "q = floor(A*/3) and, by A* mod 3, the next anchor is "
    "(2q, &Delta;* &minus; q), or (2q + 1, &Delta;* &minus; q &minus; 1), or "
    "&mdash; via pump &mdash; (1, 4&Delta;* + 1), a second F-exit. Naming: "
    "seed and halt carry over from Level 2 unchanged (&#8226;), merely restated "
    "on anchors; round is a single cascadeA round left un-batched (each round "
    "is an anchor step here); every other row is a new anchor-level "
    "composition."))
story.append(P(
    "<b>Worked example (one anchor step).</b> Take row R17 from an anchor "
    "(0, b, d) with d &ge; 2 and 3d &lt; 2b + 5. Its chain runs: expand to "
    "(3d &minus; 4, 3, 2b &minus; 2d + 3); drain &mdash; running its full "
    "k = floor(a/3) = d &minus; 2, which the guard 3d &lt; 2b + 5 keeps "
    "below the current d-value 2b &minus; 2d + 3 &mdash; to "
    "(2, 2d &minus; 1, 2b &minus; 3d + 5); two to (0, 2d, 2b &minus; 3d + 4) "
    "&mdash; an anchor again, three macro rules and 3d + 2 base steps later, "
    "with every intermediate state having a &gt; 0. Every row of the table "
    "compresses such a chain."))
story.append(P(
    "<b>Definition (the return map).</b> The <b>section</b> {b = 1} is the "
    "set of anchors whose b-component equals 1. F is the <b>first-return "
    "map</b> of G to this section: from the anchor (1, D), apply G repeatedly "
    "until the b-component is again 1; F(D) is the d-component of that "
    "anchor. The section is the natural finishing line because only three of "
    "the twelve outcomes can output b&prime; = 1 &mdash; exit (R23) and two "
    "of SWEEP&rsquo;s exit cases &mdash; and each of them is the final, "
    "pump-driven step of a growth phase."))
story.append(P(
    "<b>Is the return to b = 1 guaranteed?</b> The theorem guarantees an "
    "endless anchor sequence; the open part is whether it must revisit "
    "b = 1. A reformulation sharpens the question: inspecting the twelve "
    "rows, a b&prime; = 1 anchor arises in exactly three ways &mdash; the "
    "exit row and SWEEP&rsquo;s pump exit (both contain a pump firing), and "
    "SWEEP&rsquo;s A* = 2 exit (a two firing) &mdash; and conversely every "
    "pump firing yields a b = 1 anchor two macro steps later. So guaranteed "
    "return says: the anchor dynamics can never avoid these three outcomes "
    "forever."))
story.append(P(
    "The evidence is strong and uniform: every anchor with b, d &le; 400 "
    "(160,000+ states) and over 9,000 random anchors with coordinates up to "
    "320 bits reached the section or halted, never taking more than 80 "
    "anchor steps, and the observed maximum shows no growth with scale "
    "(52, 43, 41, 50, 45, 69, 48 at 10&ndash;320 bits); this check is now "
    "part of formal.py&rsquo;s verification suite. We nevertheless do "
    "<i>not</i> state guaranteed return as a theorem, for two principled "
    "reasons. First, <b>return time is provably unbounded</b>, so no finite "
    "case analysis can settle the question: the expand+ row acts on the "
    "ratio x = d/b as x &rarr; (2 &minus; 3x)/(2x), which has a repelling "
    "fixed point at x = 1/2, and anchors constructed near the line b = 2d "
    "wander for &Theta;(log d) steps before exiting &mdash; measured "
    "expand+ chain lengths 5, 9, 19, 39, 79 at d = 2<super>10</super>, "
    "2<super>20</super>, 2<super>40</super>, 2<super>80</super>, "
    "2<super>160</super>. Second, in the same ratio coordinate the tail "
    "rows form an <b>expanding piecewise interval map</b>, and returning "
    "means eventually landing in fixed exit windows; orbits of expanding "
    "maps that avoid fixed windows forever form a thin, Cantor-like, "
    "measure-zero set &mdash; a set sampling cannot rule out, with exactly "
    "the thin-set-avoidance character of the halting question itself "
    "(Section 9). Even this bookkeeping lemma, in other words, is "
    "Collatz-adjacent."))
story.append(P(
    "<b>Proposition (the reduction is unconditional).</b> Started at "
    "(0, 0, 0, 0), exactly one of the following holds. <b>(i)</b> Some "
    "super-cycle ends in the halt anchor; then the machine halts, and the "
    "value D<sub>k</sub> opening that cycle lies in the halting set H of "
    "Section 8.3. <b>(ii)</b> Every super-cycle returns; then the F-orbit "
    "D<sub>0</sub>, D<sub>1</sub>, &hellip; is infinite, avoids H, and the "
    "machine never halts. <b>(iii)</b> Some super-cycle neither halts nor "
    "returns; then the machine runs forever inside that cycle &mdash; an "
    "endless wander among anchors with b &ne; 1 &mdash; and again never "
    "halts. In particular, <b>the machine halts if and only if the F-orbit "
    "reaches H</b>, with no assumption that returns are guaranteed; a "
    "failure of return, far from undermining the analysis, would itself "
    "certify non-halting."))
story.append(P(
    "<i>Proof.</i> By the recurrence theorem, the trajectory from the anchor "
    "(1, 17) is an infinite sequence of anchors unless it reaches the halt "
    "anchor. List its (possibly finite) visits to the section b = 1; these "
    "open super-cycles with values D<sub>0</sub> = 17, D<sub>1</sub>, "
    "&hellip;. If the halt anchor is reached, it is reached inside some "
    "cycle k, which is precisely the statement D<sub>k</sub> &#8712; H "
    "&mdash; case (i). Otherwise the anchor sequence is infinite: if it "
    "visits the section infinitely often, case (ii); if only finitely "
    "often, case (iii). The three cases are exhaustive and mutually "
    "exclusive, and in (ii) and (iii) the machine, running through "
    "infinitely many anchors, never halts. <b>QED</b>"))
story.append(P(
    "The proposition is also why the verification architecture never relies "
    "on returns: the "
    "halting criterion of Section 8 is checked at <i>every anchor</i>, so "
    "the section is bookkeeping &mdash; it delimits super-cycles and defines "
    "F &mdash; not an assumption. A hypothetical non-returning run would "
    "appear as one unboundedly long, still fully checked super-cycle, never "
    "as an unsound conclusion. On the actual orbit of 17, all 200,000 "
    "verified super-cycles returned, with median 3 and maximum 42 anchor "
    "steps. Verification of this subsection: the table against composed "
    "level-2 steps on 40,000 random anchors across ten orders of magnitude; "
    "the induced F against the level-4 runner for 800 orbit cycles; section "
    "return on the 40,401-anchor box plus 2,000 scale-spread random anchors "
    "(formal.py)."))
story.append(P("6.2&nbsp;&nbsp;Branch words; why F is piecewise affine, not a single formula", H2))
story.append(P(
    "<b>Definition (branch word).</b> Fix a super-cycle starting at (1, D), "
    "and let r<sub>1</sub>, r<sub>2</sub>, &hellip;, r<sub>L</sub> be the "
    "indices of the G-rows fired, in order, until the step that lands back on "
    "b = 1. The <b>branch word</b> w(D) is this sequence &mdash; enriched, "
    "for each SWEEP row, with its cascade-B round count n<sub>B</sub> and "
    "exit case, which the row index alone does not determine. The <b>word "
    "length</b> |w(D)| = L is the number of anchor steps in the cycle. "
    "Because G is deterministic, w(D) and F(D) are functions of D."))
story.append(P(
    "<b>Why word lengths grow along the orbit.</b> From (1, D) with "
    "D &ge; 8, the round row R25 applies (its guard d &ge; 2b + 6 reads "
    "D &ge; 8 here), and by the closed forms of Section 5.1 with b + 4 = 5 "
    "it keeps applying for exactly n<sub>A</sub>(1, D) consecutive anchor "
    "steps. Hence |w(D)| &ge; n<sub>A</sub>(1, D), and by the logarithm "
    "formula of Section 5.3, n<sub>A</sub>(1, D) &#8776; "
    "log<sub>2</sub>(D/10). Along the orbit, D<sub>k</sub> increases "
    "strictly (F(D) &gt; D on every verified cycle; minimum observed ratio "
    "1.0002, average &times;2.4), reaching 250,005 bits by cycle 200,000 "
    "&mdash; so cycle k&rsquo;s word has roughly 1.25k letters and word "
    "lengths grow without bound. Measured directly: at least 865 distinct "
    "words occur in the first 3,000 cycles."))
story.append(P(
    "<b>Proposition (piecewise affinity).</b> For each word w there are "
    "integers &alpha;<sub>w</sub>, &beta;<sub>w</sub> with F(D) = "
    "&alpha;<sub>w</sub>D + &beta;<sub>w</sub> for <i>every</i> D whose "
    "branch word is w. <i>Proof.</i> Fixing w fixes, at each of the L anchor "
    "steps, which row fires and (for SWEEP rows) its round count and exit "
    "case; each step is then one fixed affine map of (b, d), and a "
    "composition of affine maps is affine; restricting to the start (1, D) "
    "leaves an affine function of D alone. <b>QED</b> Moreover the set "
    "{D : w(D) = w} is cut out by finitely many linear inequalities and "
    "congruences &mdash; the guards met along the way, translated back to D "
    "&mdash; so each piece is explicitly definable."))
story.append(P(
    "<b>Why countably many pieces, not finitely many.</b> Word length grows "
    "with D (previous paragraph), so no finite set of words covers all "
    "starting values: the affine pieces are countably infinite. This &mdash; "
    "and nothing deeper &mdash; is the precise content of &ldquo;F has no "
    "closed form&rdquo;: F is exactly computable, but only piece by piece, "
    "and the pieces never end. Equivalently, each cycle reads the binary "
    "expansion of D from the top: the opening R25 run consumes the leading "
    "bits (its length is the bit length, up to a constant), and the tail "
    "rows dispatch on what remains. Example: on the dominant word "
    "w = (R25 repeated n times, then R23) &mdash; 1,096 of the first 3,000 "
    "cycles, the formula verified on each &mdash;"))
story.append(P(
    "F|<sub>w</sub>(D) = 16D &minus; 240&middot;2<super>n</super> + 32n + 169,"
    "&nbsp;&nbsp;&nbsp;&nbsp;n = n<sub>A</sub>(1, D).", MATHC))

story.append(P("6.3&nbsp;&nbsp;The runner: the linear scan and the binary-search fix", H2))
story.append(P(
    "Once per cascade, the runner must evaluate n<sub>A</sub>(b, d) = "
    "max{m &ge; 1 : (b + 4)&middot;2<super>m+1</super> &le; d + 2(b + 4) + "
    "2m}. The <b>linear scan</b> is the obvious algorithm: test m = 1, 2, 3, "
    "&hellip; and stop at the first failure. It performs n<sub>A</sub> "
    "comparisons, each touching integers as large as d, i.e. ~bits(d) bit "
    "operations per comparison &mdash; so one cascade costs about "
    "n<sub>A</sub> &middot; bits(D). On this orbit n<sub>A</sub> &#8776; "
    "bits(D) &#8776; 1.25k at cycle k (Section 6.2), so the scan costs "
    "~(1.25k)<super>2</super> per cycle and &Theta;(k<super>3</super>) over "
    "k cycles; profiling showed this &mdash; not the arithmetic &mdash; "
    "dominated the level-3 deep run. The fix: the difference between the two "
    "sides of the guard inequality is strictly increasing in m, so the "
    "largest satisfying m can be found by <b>binary search</b> over "
    "m &#8712; {1, &hellip;, bits(d) + 2} &mdash; about log<sub>2</sub> "
    "bits(d) probes instead of n<sub>A</sub>. (The same applies to "
    "n<sub>B</sub>.) This removes the cubic term."))
story.append(P(
    "What remains is optimal up to constants. Representing D<sub>k</sub> "
    "takes ~1.25k bits (measured: 250,005 bits at k = 200,000), so merely "
    "<i>writing</i> the state of cycle k costs &Theta;(k) bit operations, "
    "and any simulator of k cycles must spend at least "
    "&Sigma;<sub>j&le;k</sub> &Theta;(j) = &Theta;(k<super>2</super>). The "
    "level-4 runner performs a handful of shift-and-add operations per cycle "
    "on numbers of exactly that size &mdash; it sits at this floor."))
lvl4 = [
    ("Level 3 runner", "584 s", "10<super>16,460</super> (300,000 macro steps)"),
    ("<b>Level 4 runner</b>", "<b>10 s</b>", "same point, ~60&times; faster"),
    ("<b>Level 4, deep run</b>", "<b>27 min</b>",
     "<b>200,000 cycles: no halt in first 10<super>150,514</super> steps</b>"),
]
t = Table([[P("<b>Runner</b>", CELLR), P("<b>Time</b>", CELLR),
            P("<b>Base steps covered (verified)</b>", CELLR)]] +
          [[P(a, CELLR), P(b, CELLR), P(c, CELLR)] for a, b, c in lvl4],
          colWidths=[1.6*inch, 1.0*inch, 4.3*inch])
t.setStyle(table_style())
story.append(t)
story.append(Spacer(1, 6))
story.append(P(
    "<b>Verification.</b> The binary-search round counts agree with the "
    "linear-scan versions on 3,000 random states per cascade, and F agrees with "
    "the composed level-3 steps &mdash; both resulting states and exact "
    "base-step counts &mdash; for the first 1,000 orbit cycles. The deep run "
    "checks the halting criterion of Section 8 at every level-2 macro state it "
    "passes, so the 10<super>150,514</super> bound is certified, not sampled. "
    "Implementation: <font face='Courier'>onedim.py</font>."))

story.append(P("6.4&nbsp;&nbsp;The system after step 25", H2))
story.append(P(
    "Fixing the start allows one final simplification: after exactly 25 base "
    "steps the machine is at (0, 1, 0, 17), and from then on its entire future is the anchor "
    "dynamics of Section 6.1. The whole machine is therefore "
    "equivalent to the following two-variable system with initial state "
    "<b>(b, d) = (1, 17), entered at base step 25</b>. The rules are those of "
    "the anchor map G (Section 6.1) with exactly two changes, marked as in "
    "Section 5.3: <b>cascadeA</b> &mdash; keeping its level-3 index R15 &mdash; "
    "replaces the round row R25 (all rounds re-batched, now with the "
    "interior-halt equation below), and <b>expand-deep</b> (R19) absorbs the "
    "boundary row R18 by widening its guard from 3d &gt; 2b + 5 to "
    "3d &ge; 2b + 5 (merge proved below); every row marked &#8226; carries "
    "over from G unchanged, keeping its index. Guards remain mutually "
    "exclusive and order-free, halt last. The <b>Built from</b> column gives "
    "each row&rsquo;s origin in G, and each row carries its exact base-step "
    "certificate, with P and the &ldquo;+ sweep&rdquo; convention as in "
    "Section 6.1:"))
story.append(Spacer(1, 4))
story.append(rule_table([
    ("R16", "recharge+ &#8226;", "(0, 2b + 4)", "d = 0&nbsp;&nbsp;(&#8224;)",
     "R16", "2"),
    ("R7/8", "seed &#8226;", "(2, 2b + 1); (2, 5) if b = 0",
     "d = 1&nbsp;&nbsp;(&#8224;)", "R7/8", "3"),
    ("R17", "expand+ &#8226;", "(2d, 2b &minus; 3d + 4)",
     "d &ge; 2, 3d &lt; 2b + 5", "R17", "3d + 2"),
    ("R19", "expand-deep (mod.)",
     "(6d &minus; 4b &minus; 8, 10b &minus; 11d + 24)",
     "d &le; b + 1, 3d &ge; 2b + 5,<br/>11d &le; 10b + 24",
     "R19, absorbs<br/>R18", "d + 3"),
    ("R20", "expand-sweep &#8226;", "SWEEP(9d &minus; 6b &minus; 12, "
     "8b &minus; 8d + 20)", "d &le; b + 1, 11d &gt; 10b + 24",
     "R20", "2b &minus; 2d + 7<br/>+ sweep"),
    ("R21", "reset3+ &#8226;", "SWEEP(3b + 2, 6)", "d = b + 3", "R21",
     "1 + sweep"),
    ("R22", "reset4+ &#8226;", "SWEEP(3b + 4, 4)",
     "d = b + 4&nbsp;&nbsp;(&#8224;)", "R22", "1 + sweep"),
    ("R23", "<b>exit</b> &#8226;", "(1, 16(d &minus; b) &minus; 55)",
     "b + 5 &le; d &le; 2b + 5,<br/>15d &gt; 18b + 61", "R23",
     "b + 5 +<br/>P(4b &minus; 2d + 12,<br/>5d &minus; 6b &minus; 20)"),
    ("R24", "shrink-sweep &#8226;", "SWEEP(6b &minus; 3d + 19, "
     "4d &minus; 4b &minus; 14)",
     "b + 5 &le; d &le; 2b + 5,<br/>15d &le; 18b + 61", "R24",
     "d &minus; b &minus; 3<br/>+ sweep"),
    ("R15", "<b>cascadeA</b> (mod.)", "(2<super>n</super>(b + 4) &minus; 4, "
     "d &minus; 2(b + 4)(2<super>n</super> &minus; 1) + 2n),<br/>"
     "n = n<sub>A</sub>(b, d)", "d &ge; 2b + 6",
     "R25<super>n</super> =<br/>(R12; R3)<super>n</super>",
     "(b + 4)(2<super>n</super> &minus; 1)<br/>&minus; 2n"),
    ("R13", "halt &#8226;", "<b>HALT</b>", "d = b + 2", "R13", "&mdash;"),
], header=("#", "Name", "Next state (b&prime;, d&prime;)", "Guard",
           "Built from", "Base steps"),
   widths=(0.45*inch, 0.9*inch, 1.85*inch, 1.5*inch, 1.05*inch, 1.15*inch),
   italic_cols={2, 3}))
story.append(Spacer(1, 6))
story.append(P(
    "The cascade rule halts internally iff 3(b + 4)&middot;2<super>i</super> = "
    "d + 2b + 10 + 2i has an integer solution 0 &le; i &le; n (the round-i "
    "anchor then has d = b + 2); at anchor granularity this single equation "
    "subsumes both interior halting lines of Section 8.2, since the shrink-line "
    "value &psi;<sub>i</sub> equals &phi;<sub>i+1</sub>. The boundary case "
    "3d = 2b + 5 (R18) needs no rule of its own: R19&rsquo;s remaining conjunct "
    "always holds there (11d &le; 15d &minus; 1) and R19&rsquo;s formula "
    "specializes to (2, 4d &minus; 1) with the same cost d + 3, even though "
    "the underlying rule path differs &mdash; so the system has 11 rules. "
    "Rows marked "
    "(&#8224;) never fired in a 20,000-cycle census (usage: cascadeA 41,362; "
    "expand+ 29,382; exit 17,785; expand-deep 7,893; shrink-sweep 5,478; "
    "expand-sweep 2,605; reset3+ exactly once &mdash; the "
    "orbit&rsquo;s closest approach to halting), but they are near-diagonal "
    "cases of the same nature as HALT itself and equivalence requires keeping "
    "them. Verification (afterstep25.py): states and exact costs against "
    "composed level-2 steps on 40,000 random anchors, the boundary merge on "
    "3,000 boundary states, and the orbit&rsquo;s D-sequence with exact "
    "cumulative base-step totals (including the +25 offset) reproduced for "
    "1,000 cycles."))
story.append(P(
    "<b>This system is at the computational floor.</b> Per cycle it performs a "
    "handful of anchor steps (median 3, mean 4.6, maximum 42 across 20,000 "
    "cycles; expand chains have length &le; 8, so batching them &mdash; the "
    "expand map is linear with eigenvalues 1 and &minus;4 &mdash; would save "
    "under 5%), and every state update is shift-and-add, linear in the bit "
    "length of D; the exact-cost certificates add no measurable time at this "
    "scale (4.4 s vs 4.5 s for 20,000 cycles). Since D<sub>k</sub> occupies "
    "~1.25k bits, merely writing the state of cycle k costs &Theta;(k) bit "
    "operations and simulating k cycles costs &Theta;(k<super>2</super>) &mdash; "
    "which this system already achieves. The only conceivable &ldquo;level "
    "5&rdquo; would be jumping straight to F<super>k</super>(17) without "
    "iterating, i.e. a closed form across branch words &mdash; and that is "
    "precisely the open Collatz-type core of Section 8.4. In other words: "
    "<b>further acceleration of this system is the open problem.</b> The "
    "acceleration hierarchy terminates here not for lack of effort but because "
    "its next rung and the halting question have become the same mathematical "
    "object."))

# ======================= PART II ======================================
add_part(story, "Part II &mdash; The halting question, and why the machine is a cryptid",
         "With the machine reduced to a one-integer map, its halting from "
         "(0, 0, 0, 0) becomes a sharp question about a single orbit. We answer "
         "everything answerable &mdash; a halting criterion, an exact "
         "reduction, a verified non-halting bound, a mod-16 confinement "
         "&mdash; and locate precisely the one question that remains open, and "
         "why.")

# ==================== 7. Qualitative dynamics ==========================
story.append(P("7. Qualitative dynamics", H1))
story.append(P(
    "From almost every initial configuration the system never halts: each "
    "super-cycle (pump &rarr; cascadeA &rarr; sweep &rarr; pump &hellip;) "
    "multiplies d by roughly a constant factor, so the state grows "
    "geometrically forever. The HALT rule (R13) is reachable only from a thin "
    "set of initial conditions &mdash; for example (5, 0, 0, 7), which halts "
    "after 6 steps at (0, 3, 0, 5). This unbounded growth is precisely why "
    "acceleration is essential: 3,000 level-2 macro steps from (0, 0, 0, 0) "
    "already cover about 2.95 &times; 10<super>35</super> base steps."))

# ==================== 8. Halting =======================================
story.append(P("8. Does it halt from (0, 0, 0, 0)?", H1))
story.append(P(
    "<b>Answer: no halt within the first 10<super>150,514</super> base steps "
    "(exact count verified), and almost certainly never &mdash; but a complete "
    "non-halting proof reduces to a Collatz-type problem that remains open.</b> "
    "This section states precisely what is proved and what is heuristic."))

story.append(P("8.1&nbsp;&nbsp;An exact halting criterion", H2))
story.append(P("Define, on level-2 macro states,"))
story.append(P("&phi;(a, b, d) = d &minus; b &minus; a.", MATHC))
story.append(P(
    "<b>Theorem.</b> From any c = 0 configuration, the system halts if and only "
    "if its trajectory contains a macro state with &phi; = 2 and a mod 3 &ne; 1; "
    "such a state halts within at most 2 further macro steps."))
story.append(P(
    "<b>Proof.</b> (&#8656;) If &phi; = 2 and a = 0 then d = b + 2 &ge; 2: the "
    "halt state itself. If a = 2 then d = b + 4 &gt; 0 and the two rule yields "
    "(0, b + 1, b + 3): a halt state. If a &ge; 3 then d = a + b + 2 &gt; "
    "floor(a/3), so the drain runs fully, k = floor(a/3), to (a mod 3, b + 2k, d &minus; k); "
    "&phi; is invariant under the drain (each R3 firing changes d, b, a by "
    "(&minus;1, +2, &minus;3), so &Delta;&phi; = &minus;1 &minus; 2 + 3 = 0), and a mod 3 &#8712; {0, 2} "
    "reduces to the previous cases. (&#8658;) A halt state has &phi; = 2 and "
    "a = 0. The only rules that can output an a = 0 state with &phi; = 2 are "
    "the drain (from a &#8801; 0 mod 3) and the two rule &mdash; the other "
    "producers of a = 0 states miss &phi; = 2 identically (jump gives &phi; = "
    "d + 2 &ge; 3; seed gives &phi; odd). Both preserve &phi; and have "
    "a mod 3 &ne; 1, so walking back through the maximal drain/two suffix "
    "reaches a macro state satisfying the criterion. <b>QED</b>"))
story.append(P(
    "The theorem was machine-checked against direct base-rule simulation on "
    "10,932 states (an exhaustive box, random states, and adversarial states on "
    "and adjacent to the line &phi; = 2), with horizon-exact accounting: 1,467 "
    "of them halt, and each halted at precisely the base step certified by the "
    "criterion &mdash; zero violations."))

story.append(P("8.2&nbsp;&nbsp;Corollary: four explicit halting lines", H2))
story.append(P(
    "Checking which rules can <i>create</i> &phi; = 2 (pump gives &phi; = "
    "2b + 4d &ge; 6; jump &ge; 3; seed odd; the two resets give 4 &minus; 3b "
    "and &minus;3b, never 2), the system halts iff it ever reaches"))
story.append(P(
    "a = 0 with d = b + 2,&nbsp;&nbsp;&nbsp; a = 0 with d = 4b + 12,&nbsp;&nbsp;&nbsp; "
    "a = 0 with 5d = 2b + 2 (d &ge; 2),&nbsp;&nbsp;&nbsp; "
    "d = 0 with a = 2b &minus; 1, b mod 3 &ne; 2.", MATHC))
story.append(P(
    "This four-line characterization reproduced direct halting behavior exactly "
    "for every start (0, 1, D), D &le; 20,000."))

story.append(P("8.3&nbsp;&nbsp;Reduction to a Collatz-type problem", H2))
story.append(P(
    "By the unconditional-reduction proposition of Section 6.1, halting "
    "from (0, 0, 0, 0) is equivalent to: <i>does the "
    "F-orbit of 17 (the sequence D<sub>0</sub> = 17, D<sub>k+1</sub> = "
    "F(D<sub>k</sub>) of Section 6) ever enter the halting set H</i> = "
    "{2, 3, 9, 16, 19, 26, 28, "
    "39, 44, 49, 92, 102, 161, &hellip;} of values D for which the super-cycle "
    "from (0, 1, D) halts? H is sparse: |H &#8745; [1, 10<super>6</super>]| = "
    "57, roughly 10 elements per decade (density ~4/x). No congruence "
    "obstruction exists &mdash; the orbit visits every <b>residue class</b> of "
    "d &minus; b modulo 4 and 12 (that is, d &minus; b attains every possible "
    "remainder on division by 4 and by 12) &mdash; so no simple invariant can separate "
    "the orbit from H. This is precisely the structure of Collatz-type open "
    "problems: a deterministic orbit growing geometrically must forever avoid a "
    "sparse exceptional set."))
story.append(P(
    "<b>Theorem (H is infinite).</b> For every i &ge; 0 the machine halts from "
    "(0, 1, 0, D) with D = 15&middot;2<super>i</super> &minus; 2i &minus; 12; "
    "hence H &#8839; {3, 16, 44, 102, 220, 458, 936, 1894, &hellip;} is "
    "infinite. <i>Proof.</i> Cascade A from (0, 1, D) has round-i anchor "
    "(b<sub>i</sub>, d<sub>i</sub>) with d<sub>i</sub> &minus; b<sub>i</sub> = "
    "D + 12 + 2i &minus; 15&middot;2<super>i</super> (Section 5.1 closed forms "
    "with b + 4 = 5), which equals 2 exactly for this D &mdash; and an anchor "
    "with d = b + 2 is the halt state. Round i is reached because "
    "n<sub>A</sub>(1, D) &ge; i reduces to 10&middot;2<super>i</super> &le; "
    "15&middot;2<super>i</super> &minus; 2, true for all i &ge; 0. <b>QED</b> "
    "(Machine-verified for i = 0..29.) This explains the observed geometric "
    "spacing of H, and rules out settling non-halting by any finite "
    "computation: the orbit must avoid an infinite, geometrically spaced set "
    "forever. More generally, every halting branch word w contributes the "
    "solution set of one explicit affine equation in (D, 2<super>n</super>, n) "
    "&mdash; H is exactly the countable union of these explicit families."))
story.append(P(
    "<b>Theorem (mod-16 confinement).</b> For every non-halting D, "
    "F(D) &#8801; 9 (mod 16); hence D<sub>k</sub> &#8801; 9 (mod 16) for every "
    "k &ge; 1. The first statement is about the map itself &mdash; whatever "
    "integer is fed in, F returns one that leaves remainder 9 on division by "
    "16 &mdash; and the second is its consequence for the orbit, since every "
    "D<sub>k</sub> with k &ge; 1 is an output of F. (The seed D<sub>0</sub> = "
    "17 &#8801; 1 is the sole exception, as it is not itself an F-output; from "
    "there 57, 185, 601, 2265, &hellip; are all &#8801; 9.) <i>Proof.</i> F(D) "
    "is the d-value of the b = 1 anchor closing "
    "the super-cycle, and a b = 1 anchor is produced only by exit (R23), "
    "giving 16(d &minus; b) &minus; 55 &#8801; 9 (mod 16) identically, or by "
    "SWEEP&rsquo;s pump-exit, giving 4&Delta;* + 1 with "
    "&Delta;* = (w&middot;4<super>n&minus;1</super> &minus; 2)/3, w = "
    "12&Delta; + 8; since &Delta;* &#8801; 2 (mod 4) in every case (for n = 1, "
    "&Delta;* = 4&Delta; + 2; for n &ge; 2, w&middot;4<super>n&minus;1</super> "
    "&#8801; 0 mod 16 forces it), this too is &#8801; 9 (mod 16). <b>QED</b> "
    "(Machine-verified universally.)"))
story.append(P(
    "<b>What this buys, and what it does not.</b> Recall that H is a countable "
    "union of families, one per halting branch word (previous theorem). The "
    "orbit lives in the single class 9 mod 16, so it can only ever hit the "
    "part of H lying in that class. Two successive filters cut H down to that "
    "part, and it helps to see them separately."))
story.append(P(
    "<b>Filter 1 &mdash; parity.</b> The class 9 mod 16 is odd, but H is "
    "mostly even: of the 57 members below 1.5&times;10<super>6</super>, "
    "45 are even and only 12 are odd. Every even member is unreachable at a "
    "stroke. This already disposes of the very family that proved H infinite: "
    "in 15&middot;2<super>i</super> &minus; 2i &minus; 12 every term with "
    "i &ge; 1 is even, and the lone odd term (i = 0, giving D = 3) is "
    "&#8801; 3, not 9. So the infinitude established in Section 8.3 lives "
    "entirely off the orbit &mdash; it says nothing about how many reachable "
    "targets exist."))
story.append(P(
    "<b>Filter 2 &mdash; residue.</b> The 12 odd members spread across five "
    "odd classes mod 16 &mdash; residues 1, 3, 7, 9, 15 &mdash; and the orbit "
    "is pinned to just one of them, 9. What survives both filters is "
    "H &#8745; {9 mod 16}, which below 1.2&times;10<super>7</super> is only "
    "{9, 124313}; and since the orbit merely grows from 17, even 9 is behind "
    "it, so 124313 is the first value it could conceivably hit. Net effect: "
    "of every 57 elements of H, about 2 are reachable &mdash; a roughly "
    "thirty-fold thinning of the target set, and correspondingly of the "
    "heuristic hitting-probability in Section 8.4."))
story.append(P(
    "This is the tightest confinement a congruence can give: a single residue "
    "mod 16. Yet it settles nothing, for two honest reasons. First, H still "
    "meets the class &mdash; 124313 &#8712; H &#8745; {9 mod 16} &mdash; so the "
    "orbit is not separated from H; and an exhaustive search confirms no "
    "modulus m &le; 256 separates them either (mod16.py). Second, whether the "
    "reachable set H &#8745; {9 mod 16} is even infinite is itself open: the "
    "Section 8.3 family is the wrong parity to help, no odd family "
    "&#8801; 9 mod 16 is known to be infinite, and only two elements have ever "
    "been found. Heuristically it should be infinite (each occupied odd class "
    "ought to receive its share), which is why the confinement strengthens the "
    "non-halting heuristic without proving it &mdash; but were it ever shown "
    "<i>finite</i>, checking the growing orbit against a finite list would "
    "settle non-halting outright. That we cannot decide even this is a "
    "miniature of the whole problem."))

story.append(Spacer(1, 8))
story.append(orbit_diagram())
story.append(P(
    "<b>Figure 4.</b> The F-orbit of 17 (D<sub>0</sub> = 17, D<sub>k+1</sub> = "
    "F(D<sub>k</sub>)), plotted as log<sub>10</sub> D<sub>k</sub> &mdash; the "
    "number of digits &mdash; against the cycle index k. The climb is roughly "
    "linear (geometric growth) but visibly jagged, the fingerprint of the "
    "pseudorandom branch words of Section 6.2. Halting would require the orbit "
    "to land <i>exactly</i> on a value in H; the dashed line marks the scale "
    "of the first reachable such value, 124313, which the orbit sails past "
    "&mdash; passing a target&rsquo;s magnitude is not hitting it.", FIGCAP))

story.append(P("8.4&nbsp;&nbsp;Verified bound and heuristic conclusion", H2))
story.append(P(
    "Checking the criterion at every level-2 macro state (including all states "
    "internal to cascades, located by exact binary search on the monotone "
    "&phi;-sequences), the level-3 runner verified no halt within "
    "10<super>16,460</super> base steps, and the level-4 runner extended this "
    "to <b>200,000 full super-cycles: the original system does not halt within "
    "its first 10<super>150,514</super> steps</b> (the exact step count, a "
    "150,515-digit number, is computed by the certificates; D then has 75,259 "
    "digits). Heuristically, cycle k has chance ~4/D<sub>k</sub> of landing in "
    "H; summed over the surviving orbit this leaves total remaining halting "
    "&ldquo;probability&rdquo; below 10<super>&minus;75,000</super>. The honest "
    "summary: <b>the system almost certainly never halts, this is verified "
    "beyond any physically simulable horizon, and a complete proof would "
    "require solving a Collatz-type orbit-avoidance problem.</b>"))
story.append(P(
    "<b>Why no proof is available in either direction.</b> A halting proof "
    "would exhibit k with D<sub>k</sub> &#8712; H; none exists for k &le; "
    "200,000 and the heuristic expectation is that none exists at all. A "
    "non-halting proof is blocked by three machine-checked facts: (i) no affine "
    "congruence invariant exists (symbolic check over the 12 non-halting base "
    "rules: only the trivial one survives); (ii) no residue class separates "
    "the orbit from H &mdash; and this is now known sharply, not just for a "
    "few moduli: the orbit is confined to the single tightest class 9 mod 16 "
    "(the mod-16 confinement theorem of Section 8.3), yet an exhaustive search "
    "of every modulus m &le; 256 finds H meeting the orbit&rsquo;s residues at "
    "all of them, so even the best congruence still fails to separate; "
    "(iii) growth arguments "
    "cannot help: F(D) &gt; D empirically for every non-halting D &le; 300,000 "
    "(minimum ratio 1.0002), but since H is provably infinite with geometric "
    "spacing (Section 8.3), the growing orbit passes through H&rsquo;s scale "
    "range forever. Membership of D<sub>k</sub> in H is an exact equality "
    "between D<sub>k</sub> and closed forms such as 15&middot;2<super>i</super> "
    "&minus; 2i &minus; 12 &mdash; deciding it for all k requires bit-level "
    "control of the orbit of a piecewise-affine expanding map, which is "
    "precisely the open core of Collatz-type problems. The minimal open "
    "question is: <i>does the F-orbit of 17 avoid the countable union of "
    "explicit affine families that constitute H?</i>"))

# ==================== 9. Verification ==================================
story.append(P("9. Why this machine is a cryptid", H1))
story.append(P(
    "The preceding sections answered every question about this machine that "
    "can currently be answered. This section explains the nature of the one "
    "that remains: why it is not merely unsolved, but belongs to a class of "
    "problems that mathematics has so far been unable to touch &mdash; and how "
    "the acceleration program of Sections 3&ndash;6 is exactly what brought "
    "that fact into view."))

story.append(P("9.1&nbsp;&nbsp;What &ldquo;Collatz-like&rdquo; means", H2))
story.append(P(
    "The Collatz map sends n to n/2 when n is even and to 3n + 1 when n is "
    "odd. The conjecture &mdash; that every positive start eventually reaches "
    "1 &mdash; dates to 1937, is numerically verified far beyond "
    "10<super>20</super>, and remains open; Erd&ouml;s remarked that "
    "&ldquo;mathematics may not be ready for such problems.&rdquo; What makes "
    "it hard is not the specific constants but three structural features, and "
    "a single-orbit question deserves the name <b>Collatz-like</b> when it has "
    "all three:"))
story.append(P(
    "(i) <b>Piecewise-affine dynamics</b>: finitely many affine branches, "
    "selected by simple conditions on the current value. Here: every G-case is "
    "affine (Section 6.2). (ii) <b>Expansion</b>: the map grows its argument "
    "on average, so orbits never revisit and never settle. Here: F grows "
    "D by a factor of 2.4 per cycle on average (and never shrinks it: minimum factor 1.0002 in 20,000 measured cycles). (iii) <b>Digit consumption</b>: which branch "
    "fires next depends on ever-deeper digits of the value, so the branch "
    "sequence behaves like a pseudo-random stream and no bounded summary of "
    "the state determines the future. Here: one cycle&rsquo;s branch word has "
    "length ~log<sub>2</sub> D, at least 865 distinct words occur in the first 3,000 "
    "cycles, and the affine piece F|<sub>w</sub> is indexed by the entire "
    "word (Section 6.2, where words are defined). Feature (iii) is the fatal one: it is why no "
    "congruence, no automaton, and no invariant of bounded size can track the "
    "orbit."))
story.append(P(
    "This class is not merely mysterious; it is provably beyond general "
    "methods. Conway showed in 1972 that generalized Collatz maps &mdash; "
    "exactly the piecewise-affine, condition-dispatched maps above &mdash; can "
    "simulate arbitrary computation, so their termination problem is "
    "<b>undecidable in general</b>. No algorithm decides all instances. Every "
    "instance ever solved was solved by an instance-specific insight &mdash; "
    "an invariant, a potential function, a finite-state abstraction. "
    "Sections 8.3&ndash;8.4 record the systematic search for such an insight "
    "here, and its outcome: none of the known kinds exists for this machine."))

story.append(P("9.2&nbsp;&nbsp;The pseudorandom heuristic, and why it is only a heuristic", H2))
story.append(P(
    "Feature (iii) is worth developing carefully, because it is the engine "
    "behind both why these problems are believed and why they resist proof. "
    "A deterministic sequence is called <b>pseudorandom</b> for a class of "
    "statistical tests if its statistics &mdash; frequencies, correlations, "
    "digit distributions &mdash; match those an independent random sequence "
    "would produce, even though the sequence is fully determined. The notion "
    "is always relative to a class of tests: no fixed deterministic sequence "
    "is &ldquo;random&rdquo;, yet many pass every test one can devise. The "
    "distinction that matters below is between a <i>proved</i> "
    "equidistribution statement (a theorem that certain averages converge to "
    "the random prediction) and an <i>unproved</i> hypothesis that a single "
    "prescribed orbit obeys those averages."))
story.append(P(
    "<b>The Collatz heuristic, precisely.</b> Restrict the map to odd n via "
    "the shortcut T(n) = (3n + 1)/2<super>v</super>, where "
    "2<super>v</super> exactly divides 3n + 1. Model the exponent v as "
    "geometric &mdash; P(v = k) = 2<super>&minus;k</super> for k &ge; 1, the "
    "prediction if the higher bits of 3n + 1 were fair coin flips &mdash; so "
    "that E[v] = 2. The expected multiplicative change per odd step is then"))
story.append(P(
    "E[ log(T(n)/n) ] &#8776; log 3 &minus; E[v] log 2 = log 3 &minus; "
    "2 log 2 = log(3/4) &lt; 0,", MATHC))
story.append(P(
    "a contraction by a factor 3/4: the heuristic predicts almost every orbit "
    "drifts downward and hence reaches 1. What is genuinely <i>proved</i> "
    "supports the model but stops short of the conjecture. The Collatz map "
    "extends to a measure-preserving, ergodic transformation of the 2-adic "
    "integers, so its parity sequence is equidistributed for almost every "
    "start; and Tao (2019) showed that almost all orbits (in logarithmic "
    "density) attain almost bounded values. Both are <b>almost-everywhere</b> "
    "statements. The conjecture asks about the orbit of <i>every</i> n "
    "&mdash; each a single point, a measure-zero set &mdash; and an "
    "almost-everywhere theorem says nothing about any prescribed point. That "
    "gap between &ldquo;almost every orbit&rdquo; and &ldquo;this "
    "orbit&rdquo; is the whole of what remains open."))
story.append(P(
    "<b>The same heuristic here.</b> Our map F grows rather than shrinks: its "
    "average log-drift is log 2.4 &#8776; 0.88 &gt; 0, so the orbit almost "
    "surely escapes to infinity. The live question is therefore not descent "
    "but sparse hitting &mdash; does the escaping orbit ever land in H? The "
    "pseudorandom hypothesis supplies the estimate: if the arithmetic of "
    "D<sub>k</sub> that decides H-membership equidistributes, then "
    "P(D<sub>k</sub> &#8712; H) is the local density of H at scale "
    "D<sub>k</sub>. That density is measurable: fitting the counts "
    "(|H &#8745; [1, 10<super>6</super>]| = 57) gives "
    "|H &#8745; [1, x]| &#8776; 4.1 ln x, i.e. a local density &#8776; "
    "4/D<sub>k</sub>. The expected number of hits from cycle k onward is then "
    "&Sigma;<sub>j &ge; k</sub> 4/D<sub>j</sub>; since the D<sub>j</sub> grow "
    "geometrically on average, the sum is controlled by its first term "
    "4/D<sub>k</sub>. Past the verified horizon k = 200,000, where "
    "D<sub>k</sub> already has 75,259 digits, the whole remaining sum is "
    "below 10<super>&minus;75,000</super> &mdash; the figure quoted in "
    "Section 8.4. The model&rsquo;s verdict: the orbit almost surely never "
    "meets H, and the machine never halts."))
story.append(P(
    "<b>Why the sequence is pseudorandom here &mdash; the mechanism.</b> The "
    "structural reason is proved, in Section 6.2: F reads the binary "
    "expansion of D from the top. Each super-cycle&rsquo;s opening R25 run "
    "consumes the leading ~log<sub>2</sub> D bits, and the tail rows dispatch "
    "on the digits that remain; so the branch word is literally a function of "
    "the digit string of D, and advancing the orbit is an intricate "
    "digit-mixing operation &mdash; exactly as the Collatz parity sequence is "
    "a readout of the 2-adic digits of n. That is why the branch sequence "
    "carries no exploitable regularity, and the measurements confirm it: at "
    "least 865 distinct branch words in the first 3,000 cycles, anchors "
    "hitting every residue class of d &minus; b modulo 4 and 12, and a "
    "symbolic search returning only the trivial affine invariant (Section "
    "8.4). These are precisely the statistics an equidistributed sequence "
    "would produce &mdash; the operational content of &ldquo;pseudorandom&rdquo; "
    "&mdash; and precisely why no invariant of bounded size can track the "
    "orbit."))
story.append(P(
    "<b>The unbridgeable step.</b> One honest asymmetry sharpens the "
    "difficulty. For Collatz the pseudorandom backbone is partly a theorem "
    "(2-adic ergodicity, Tao&rsquo;s density-one result); for this machine we "
    "have no such theorem &mdash; no proved ergodicity for F &mdash; only the "
    "empirical signatures above. So the machine offers <i>less</i> rigorous "
    "structure than Collatz, not more, while exhibiting the same behavior. In "
    "both cases the final step is identical and unbridged: the heuristic is an "
    "assumption about one specific orbit, and every rigorous equidistribution "
    "result is almost-everywhere, silent on any single trajectory. The "
    "heuristic makes the answer (never halts) morally certain and even "
    "quantifies the certainty (below 10<super>&minus;75,000</super>); it "
    "cannot make it a theorem, because turning &ldquo;almost every orbit&rdquo; "
    "into &ldquo;this orbit&rdquo; is exactly the open problem &mdash; here as "
    "for Collatz."))

story.append(P("9.3&nbsp;&nbsp;Cryptids", H2))
story.append(P(
    "The term <b>cryptid</b> comes from the Busy Beaver community "
    "(bbchallenge.org), which classifies small Turing machines by whether "
    "their halting can be decided. The fifth Busy Beaver number was settled "
    "in 2024 only after the last holdout machines were resolved by bespoke "
    "proofs; at six states there remain explicit machines &mdash; the most "
    "famous is <i>Antihydra</i>, which iterates n &rarr; 3n/2 with a parity "
    "side-count &mdash; whose halting is equivalent to an open Collatz-type "
    "orbit question. Such machines are called cryptids: <b>small, fully "
    "explicit programs whose halting question is an open problem of Collatz "
    "type</b>. They matter because they mark the exact frontier where program "
    "size meets unprovability."))
story.append(P(
    "This machine is a cryptid in precisely that sense. It has 13 rules over "
    "four counters; every step is elementary arithmetic; and by the reduction "
    "of Sections 6 and 8 &mdash; unconditional, by the proposition of "
    "Section 6.1 &mdash; halting from (0, 0, 0, 0) is <i>equivalent</i> to "
    "&ldquo;the F-orbit of 17 avoids the halting set H&rdquo; &mdash; with "
    "F expanding, piecewise affine with countably many digit-indexed pieces, "
    "and H an infinite, geometrically spaced union of explicit affine "
    "families. That claim deserves auditing rather than asserting. Each row "
    "below names one thing that makes this family of problems hard, what "
    "is actually <i>known</i> for Collatz, and what we were able to "
    "establish here:"))
cryptid_rows = [
    ("Piecewise-affine dynamics",
     "two affine branches, picked by a single parity bit.",
     "every anchor rule is affine, and F is affine on each branch word "
     "&mdash; but with countably many pieces, not two (Section 6.2)."),
    ("Expansion: orbits never settle",
     "contracts by &times;3/4 per odd step on the standard heuristic, which is "
     "why it is expected to fall to 1; orbits are famously non-monotone.",
     "expands and <b>provably never shrinks on the dominant word</b>: "
     "F(D) &minus; D &ge; 2n + 19 (Section 9.6) &mdash; a monotonicity Collatz "
     "does not have."),
    ("Digit consumption &rarr; pseudorandom branching",
     "the branch is the next 2-adic digit of n; the parity stream is provably "
     "equidistributed on the 2-adic integers.",
     "each cycle consumes the ~log<sub>2</sub> D leading bits; at least 865 "
     "distinct branch words in 3,000 cycles, every residue class visited "
     "(measured, not proved &mdash; Section 9.2)."),
    ("Belongs to an undecidable class",
     "Conway (1972): generalized Collatz maps simulate arbitrary computation, "
     "so termination is undecidable for the class &mdash; no general algorithm "
     "exists.",
     "the same class, so only an instance-specific insight could ever settle "
     "it; Sections 8.3&ndash;8.4 record the search for one, and its failure."),
    ("The hard event is an exact coincidence",
     "the orbit must reach exactly 1.",
     "the orbit must land exactly on a member of H &mdash; an explicit affine "
     "family such as 15&middot;2<super>i</super> &minus; 2i &minus; 12."),
    ("Statistical theorems cannot reach it",
     "Tao (2019): almost all orbits attain almost bounded values (logarithmic "
     "density one) &mdash; yet this says nothing about any single n.",
     "the pseudorandom estimate puts the remaining chance below "
     "10<super>&minus;75,000</super> &mdash; yet says nothing about this orbit "
     "(Section 9.5a)."),
    ("No bounded-state invariant survives",
     "no congruence or finite-automaton invariant is known.",
     "symbolic search returns only the trivial invariant; the orbit is "
     "<i>provably</i> confined to 9 mod 16, yet no modulus m &le; 256 "
     "separates it from H (Section 9.5b)."),
    ("Growth arguments cannot close it",
     "not applicable &mdash; the map contracts; the difficulty runs the other "
     "way.",
     "escaping to infinity does not help: H is infinite with the same "
     "geometric spacing, so the orbit climbs through targets forever "
     "(Section 9.5c)."),
    ("Verified far, proved not at all",
     "checked far beyond 10<super>20</super>; open since 1937.",
     "no halt in the first 10<super>150,514</super> steps; open."),
    ("Proved structural backbone",
     "2-adic ergodicity, plus Tao&rsquo;s density-one theorem &mdash; the "
     "branch is n mod 2, so the map lives on Z<sub>2</sub>.",
     "<b>provably unavailable by that route</b>: the branch is a "
     "leading-digit quantity, and F has no continuous extension to "
     "Z<sub>2</sub> at all (Section 9.6)."),
]
t = Table([[P("<b>what makes these problems hard</b>", CELLR),
            P("<b>Collatz &mdash; what is known</b>", CELLR),
            P("<b>This machine &mdash; what we established</b>", CELLR)]] +
          [[P(f"<b>{a}</b>", CELLR), P(b, CELLR), P(c, CELLR)]
           for a, b, c in cryptid_rows],
          colWidths=[1.5*inch, 2.3*inch, 2.9*inch], repeatRows=1)
t.setStyle(table_style())
story.append(t)
story.append(Spacer(1, 6))
story.append(P(
    "Read down the table, the verdict is not close: every structural feature "
    "that makes Collatz hard is present here, every avenue that fails for "
    "Collatz fails here for the same reason, and the last row runs the wrong "
    "way &mdash; Collatz at least has a proved ergodic backbone, and for this "
    "machine that route is provably closed (Section 9.6). A tiny, fully "
    "explicit program whose halting is "
    "equivalent to an open orbit-avoidance problem of exactly this kind is "
    "what the word <b>cryptid</b> names."))
story.append(P(
    "One difference is worth drawing out, because it inverts the question "
    "rather than restating it. Collatz sets a <i>wandering</i> orbit against a "
    "single <i>fixed</i> target and asks whether it ever arrives. This machine "
    "sets a <i>growing</i> orbit against a target set that <i>grows with it</i> "
    "and asks whether it forever fails to arrive. Both are open; the shapes "
    "are opposite:"))
story.append(Spacer(1, 8))
story.append(collatz_vs_machine_diagram())
story.append(P(
    "<b>Figure 5.</b> Two Collatz-type questions of opposite shape. "
    "<i>Left:</i> the Collatz orbit of 27 wanders for 111 steps and must come "
    "down to the single fixed target 1 &mdash; it does. <i>Right:</i> this "
    "machine climbs away geometrically through a field of halting values that "
    "itself extends to every scale (grey; the two reachable 9-mod-16 targets "
    "in red), and halting would require landing exactly on one. Passing a "
    "target&rsquo;s magnitude is not hitting it &mdash; which is why the "
    "verified bound of Section 8.4 settles nothing.", FIGCAP))

story.append(P("9.4&nbsp;&nbsp;How the acceleration program exposed the core", H2))
story.append(P(
    "The route matters, because it is itself the evidence. The hierarchy of "
    "Sections 3&ndash;6 acted as a lens: each level removed structure that was "
    "provably mechanical. Level 1 removed bookkeeping (the transfer buffer c). "
    "Level 2 removed arithmetic progressions (the unary loops R3 and R5, "
    "collapsed by their own regularity). Level 3 removed geometric series "
    "(the two-rule cascades). Level 4 removed everything except one integer. "
    "At no point was anything difficult encountered &mdash; every reduction "
    "was exact, certified, and machine-verified; at every level the machine "
    "looked tame."))
story.append(P(
    "The hard core appeared at the precise moment nothing removable remained. "
    "When the whole machine had become the iteration of F on a single "
    "integer, the next question &mdash; does F itself have a finite closed "
    "form? &mdash; received a measured answer: no; its branch words grow "
    "without bound because F reads the binary expansion of D (Section 6.2). "
    "That is feature (iii) of Section 9.1 appearing exactly where all "
    "mechanical structure ran out &mdash; though, as Section 9.7 records, a "
    "first sign of it had already surfaced one level earlier, while merely "
    "defining F. The halting criterion (Section 8.1) then "
    "sharpened &ldquo;does it halt&rdquo; into hitting explicit affine lines; "
    "the H-is-infinite theorem (Section 8.3) closed the door on settling the "
    "question by any finite computation; and the three machine-checked "
    "obstructions (Section 8.4) closed the doors marked invariants, residues, "
    "and growth."))
story.append(P(
    "The terminal observation of Section 6.4 ties it together: the only "
    "conceivable further acceleration &mdash; a closed form for "
    "F<super>k</super> across branch words &mdash; would <i>be</i> a solution "
    "to the halting problem. &ldquo;This machine is a cryptid&rdquo; and "
    "&ldquo;the acceleration hierarchy terminates here&rdquo; are the same "
    "fact seen from two sides. That suggests an operational definition worth "
    "stating: <b>accelerate a machine until only closed forms remain; what "
    "is left is its irreducible mathematical content. For a tame machine the "
    "residue is empty &mdash; the accelerations run to a full solution. A "
    "cryptid is a machine whose residue is an open problem.</b>"))

story.append(P("9.5&nbsp;&nbsp;The anatomy of the hardness", H2))
story.append(P(
    "<b>(a) Exact events defeat statistical tools.</b> The strongest modern "
    "result in this area &mdash; Tao&rsquo;s 2019 theorem that almost all "
    "Collatz orbits attain almost bounded values &mdash; is a statement about "
    "density-one sets of starting points (statements true for 100% of starts "
    "in the limiting-fraction sense). Halting here demands an exact "
    "equality, D<sub>k</sub> = 15&middot;2<super>i</super> &minus; 2i &minus; "
    "12 or a sibling, for one specific orbit: a measure-zero coincidence "
    "&mdash; an event a randomly drawn orbit would satisfy with probability "
    "zero. "
    "Statistical methods discard, by construction, exactly the information "
    "that decides the question."))
story.append(P(
    "<b>(b) Digit consumption destroys invariants.</b> For any congruence or "
    "finite-automaton invariant to exist, the branch taken must factor "
    "through a bounded amount of state. It does not: branch selection "
    "involves magnitude comparisons (n<sub>A</sub> &#8776; "
    "log<sub>2</sub> D of them per cycle) that residues cannot express, the "
    "orbit&rsquo;s anchors hit every residue class of d &minus; b modulo 4 "
    "and 12, and the symbolic search over affine invariants returns only the "
    "trivial one (the digit-mixing mechanism behind this is developed in "
    "Section 9.2). These are measurements (Section 8.4), not impressions."))
story.append(P(
    "<b>(c) Growth cannot save.</b> F(D) &gt; D on every non-halting tested "
    "start, so the orbit escapes to infinity &mdash; but H is provably "
    "infinite with the same geometric spacing as the orbit&rsquo;s growth "
    "(Section 8.3): the orbit climbs <i>through</i> H&rsquo;s scale range "
    "forever, and escape arguments are structurally useless. This is exactly "
    "why the H-is-infinite theorem matters: it converts &ldquo;we have not "
    "found a proof&rdquo; into &ldquo;whole categories of proof are "
    "impossible.&rdquo;"))
story.append(P(
    "<b>(d) The heuristic&ndash;proof gap.</b> By the pseudorandom estimate "
    "of Section 9.2 the expected number of future hits on H is below "
    "10<super>&minus;75,000</super> &mdash; overwhelming "
    "certainty by any scientific standard. Yet for a deterministic orbit, "
    "probability zero is not impossibility. Collatz-like problems are "
    "precisely where these two notions diverge maximally: the orbit is "
    "random enough to make the answer morally obvious, and deterministic "
    "enough to make that answer unprovable with current mathematics. That "
    "gap &mdash; verified to 10<super>150,514</super> steps and provable by "
    "no known method &mdash; is what this report ultimately documents."))

story.append(P("9.6&nbsp;&nbsp;What can be proved after all", H2))
story.append(P(
    "Two entries in the scorecard were, for most of this report, mere "
    "measurements where Collatz has theorems. Both can be improved &mdash; one "
    "into a proof, the other into an <i>obstruction</i> &mdash; a third, "
    "natural conjecture turns out to be false, and a fourth result &mdash; "
    "found later, prompted by the second machine in this collection &mdash; "
    "closes the cycle question outright. Verification: gaps.py for "
    "(a)&ndash;(c), potential.py for (d)."))

story.append(P(
    "<b>(a) Expansion is a theorem on the dominant word, with an exact "
    "margin.</b> On w = (R25<super>n</super>, R23) the closed form of "
    "Section 6.2 gives F(D) = 16D &minus; 240&middot;2<super>n</super> + 32n + "
    "169 with n = n<sub>A</sub>(1, D). Writing D = 16&middot;2<super>n</super> "
    "+ &delta;,"))
story.append(P(
    "F(D) &minus; D = 15&delta; + 32n + 169.", MATHC))
story.append(P(
    "The exit row R23 fires only while its guard 15d &gt; 18b + 61 holds, and "
    "after n cascade-A rounds b = 5&middot;2<super>n</super> &minus; 4 and "
    "d = 6&middot;2<super>n</super> + &delta; + 10 + 2n, so that guard reads "
    "15&delta; + 30n + 161 &gt; 0. Substituting, F(D) &minus; D &gt; "
    "(&minus;30n &minus; 161) + 32n + 169 = 2n + 8 &gt; 0; and since &delta; "
    "is an integer the minimum is attained at &delta; = &minus;(2n + 10):"))
story.append(P(
    "F(D) &minus; D &ge; 2n + 19,&nbsp;&nbsp;&nbsp;&nbsp;attained at "
    "D = 16&middot;2<super>n</super> &minus; (2n + 10).", MATHC))
story.append(P(
    "<b>QED</b> (verified for n = 6..39.) So the dominant word cannot "
    "contract &mdash; and only just: the guard fails exactly 11 units before "
    "the contraction region begins. This also explains the puzzling "
    "measurement the report carried earlier, that the minimum growth ratio "
    "creeps toward 1: the margin 2n + 19 grows logarithmically while D grows "
    "exponentially. No contraction occurs anywhere else we can reach either "
    "(no F(D) &le; D among ~450,000 values spanning eighteen orders of "
    "magnitude, plus a systematic probe of the boundaries c&middot;2"
    "<super>n</super>). Note this is a monotonicity <i>Collatz does not "
    "have</i>: its orbits go up and down, while this one provably climbs."))

story.append(P(
    "<b>(b) The missing backbone is not absent but obstructed.</b> Collatz's "
    "2-adic ergodicity exists for a reason: its branch is chosen by n mod 2 "
    "&mdash; low-order, 2-adic data &mdash; so the map extends continuously to "
    "the 2-adic integers and carries an ergodic measure. This machine's branch "
    "count is n<sub>A</sub>(1, D) = bits(D) &minus; 4 + &epsilon;, with "
    "&epsilon; &#8712; {&minus;1, 0} fixed by the leading digits: an "
    "<b>Archimedean</b> quantity, not a 2-adic one. Agreeing on low-order bits "
    "therefore says nothing about which branch fires, and continuity fails at "
    "every level."))
story.append(P(
    "<b>Theorem.</b> For every N there exist D &#8801; D&prime; (mod "
    "2<super>N</super>) with F(D) &ne; F(D&prime;) (mod 32). Hence F admits "
    "no continuous extension to Z<sub>2</sub>. <i>Proof (construction).</i> "
    "Near base = 16&middot;2<super>n</super> the exit guard flips at "
    "&delta; = &minus;(2n + 10), by (a). Take"))
story.append(P(
    "D&prime; = base &minus; (2n + 11)&nbsp;&nbsp;(the word has switched), "
    "&nbsp;&nbsp;&nbsp;D = D&prime; + 2<super>N</super>&nbsp;&nbsp;(back on the "
    "dominant word).", MATHC))
story.append(P(
    "They agree mod 2<super>N</super> by construction, lie in different branch "
    "words, and give F &#8801; 25 and 9 (mod 32) respectively. <b>QED</b> "
    "(constructed and checked for N up to 2<super>128</super>.) The "
    "consequence is worth stating plainly: <b>the Collatz 2-adic argument "
    "provably cannot be transplanted here.</b> The last row of the scorecard "
    "is therefore not an admission of missing work but a structural fact about "
    "this machine."))

story.append(P(
    "<b>(c) The natural replacement conjecture is false.</b> If the branch is "
    "Archimedean, the right analogue of the 2-adic circle should be the "
    "<b>mantissa circle</b>, frac(log<sub>2</sub> D) &mdash; and the obvious "
    "conjecture is that the orbit equidistributes on it. It does not: over "
    "20,000 cycles a 20-bin test gives &chi;<super>2</super> &#8776; 162 "
    "against a 95% critical value of about 30. The mantissa instead carries a "
    "genuine non-uniform stationary density. So a backbone for F would have to "
    "identify <i>that</i> density; the naive equidistribution statement is "
    "already refuted. This is the most concrete target we can hand to a future "
    "attempt &mdash; and a reminder that the honest move, when a conjecture is "
    "cheap to test, is to test it."))
story.append(P(
    "<b>(d) A monotone potential: the machine cannot cycle.</b> The "
    "after-step-25 system of Section 6.4 admits an exact potential. Write "
    "&Phi; = 2b + d. Then <b>every non-halting rule increases &Phi; by at "
    "least 2</b>. For the direct rules this is a computation: the cascade "
    "gives &Delta;&Phi; = 2n exactly (its (b+4)(2<super>n</super> &minus; 1) "
    "terms cancel two-for-one); the exit rule gives &Delta;&Phi; = 15d "
    "&minus; 18b &minus; 53 &ge; 9, its guard 15d &gt; 18b + 61 being "
    "precisely the potential&rsquo;s positivity condition &mdash; the same "
    "guard-sits-just-above-zero phenomenon as the margin in (a); the "
    "expansion rules give +4 and +8 exactly. The sweep rules rest on a "
    "conservation lemma: if SWEEP(A, &Delta;) runs its cascade for n rounds, "
    "its pre-drain outputs satisfy A* + &Delta;* = A + &Delta; + 3n, and "
    "each drain case then lands within 3 of that sum (the pump case "
    "exceeds it). Finally, the guards of the two sweep-entry rules turn out "
    "to be <i>equivalent</i> to their cascade running at least once, which "
    "supplies the needed +3n. Minimum increment over all rules: 2, attained "
    "by a one-round cascade &mdash; matching the measured minimum exactly."))
story.append(P(
    "<b>Corollary.</b> The system admits no cycles, and the trajectory from "
    "(0, 0, 0, 0) never repeats a state after step 25. This closes "
    "unconditionally the one scenario that no amount of simulation could "
    "exclude: an eventually-periodic orbit with an astronomically long "
    "transient. The scenario is not hypothetical &mdash; the Busy Beaver "
    "machine Skelet #1 looked chaotic yet proved to be a translated cycler "
    "with a preperiod near 5.4 &times; 10<super>51</super> steps &mdash; and "
    "before this theorem, the report&rsquo;s no-cycling evidence was only "
    "the measured expansion ratio. Verified: the lemma on 60,000 cascades, "
    "the increment on ~150,000 transitions spanning ten orders of magnitude "
    "(minimum found: 2), and 300,000 anchor steps of the true orbit."))

story.append(P(
    "None of this touches the halting question, which remains exactly as open "
    "as before. What changes is the shape of the ignorance: one empirical "
    "claim became a theorem, one gap became a proved obstruction, one "
    "plausible route was closed by counterexample rather than left untried "
    "&mdash; and the cycling alternative is now excluded by proof, so the "
    "dichotomy of Section 8 is clean: the machine halts, or it escapes to "
    "infinity; it cannot wander periodically."))

story.append(P("9.7&nbsp;&nbsp;The hardness is nested", H2))
story.append(P(
    "One structural fact, uncovered while formalizing Section 6, sharpens the "
    "whole picture: the halting question is not the only Collatz-type question "
    "this machine raises &mdash; it is the outermost of two."))
story.append(P(
    "The inner one appeared while merely <i>defining</i> F. Turning the "
    "anchor dynamics into a one-variable map needed the orbit to return to the "
    "section {b = 1} each super-cycle (Section 6.1). That return is guaranteed "
    "by no theorem, and for a telling reason: in the ratio coordinate "
    "x = d/b the tail rows act as an expanding interval map, and returning "
    "means eventually landing in fixed exit windows &mdash; so "
    "&ldquo;returns forever&rdquo; is precisely &ldquo;an expanding orbit that "
    "never avoids a fixed target,&rdquo; the same shape as a Collatz orbit "
    "avoiding a sparse set. The return question is Collatz-like in its own "
    "right, one level below the halting question that governs the orbit of "
    "super-cycles."))
story.append(P(
    "Two things set the inner question apart from the outer one, and together "
    "they are the reason the report can conclude anything at all. It is "
    "<b>dispensable</b>: the unconditional-reduction proposition (Section 6.1) "
    "shows a non-returning orbit would simply be one more non-halting run, so "
    "the inner question can be sidestepped without being solved &mdash; "
    "whereas the outer question cannot be sidestepped, only left open. And it "
    "is a <b>structural analogy</b>, not a proven equivalence: unlike the "
    "halting question, which reduces to an exact, explicitly described "
    "orbit-avoidance problem (Section 8), the return question merely has the "
    "same expanding-map-avoids-thin-set form."))
story.append(P(
    "So the machine is Collatz-hard not at a single isolated point but through "
    "a nested pair of same-shaped questions &mdash; one dispensable, one "
    "essential. This is the precise sense in which its difficulty is "
    "intrinsic rather than incidental, and it refines the operational picture "
    "of Section 9.4. Accelerating a machine does not always reduce it to one "
    "irreducible question; it can peel the machine into a stack of "
    "Collatz-type questions. What makes this machine a cryptid is not merely "
    "that the stack is non-empty, but that it does not bottom out at anything "
    "solvable: the essential layer is an open problem, and the acceleration "
    "hierarchy terminates there because the only way past it is to solve it."))

story.append(P("10. Verification", H1))
story.append(P(
    "All verification is against the original 13-rule system, executed "
    "literally, and all checks are step-exact: a macro rule claiming k base "
    "steps must land on the identical configuration after exactly k "
    "applications of the original rules. (&ldquo;Checkpoints&rdquo; below are "
    "the states an accelerated system visits, located at their certified "
    "positions inside the base trajectory.)"))
vrows = [
    ("Per-rule exactness (level 2)",
     "~49,600 states: exhaustive over all triples with values &lt; 25, plus random "
     "states with values up to 10<super>6</super>, covering every guard", "pass"),
    ("Whole-trajectory vs. base (level 2)",
     "85 random/adversarial starts, 300,000 base steps each; every macro checkpoint "
     "matches the base state at the claimed step index", "pass"),
    ("Level 3 vs. level 2 checkpoints", "60 starts, 4,000 macro steps each", "pass"),
    ("Closed-form cascades (Section 5.3)",
     "round counts, states and costs vs. loop implementations: 50,000 random states "
     "per cascade; assembled system: 20,000 further states + trajectories", "pass"),
    ("Level 3 vs. base directly",
     "41 starts including large states, up to 500,000 base steps each", "pass"),
    ("Halting behavior",
     "halting starts (e.g. (5, 0, 0, 7)) halt at the same configuration after the "
     "same number of steps at every level", "pass"),
    ("Halting criterion (Section 8.1)",
     "criterion vs. direct base simulation, horizon-exact: 10,932 states (exhaustive "
     "box + random + near-line adversarial), 1,467 halts each at the certified step; "
     "four-line corollary vs. direct halting on all (0, 1, D), D &le; 20,000", "pass"),
    ("Anchor map G (Section 6.1)",
     "G vs. composed level-2 steps on 40,000 random anchors across ten orders of "
     "magnitude; F-as-first-return vs. the level-4 runner on 800 orbit cycles; the "
     "dominant affine piece on 1,096 cycles", "pass"),
    ("Cascade-internal line checks (Section 8.4)",
     "binary-search checks vs. brute-force cascade expansion on 60,000 random states; "
     "3,896 engineered on-line states all flagged", "pass"),
    ("Monotone potential (Section 9.6d)",
     "conservation lemma A* + &Delta;* = A + &Delta; + 3n on 60,000 cascades; "
     "guard&ndash;cascade equivalences for both sweep rules exhaustively to 2,000; "
     "&Delta;&Phi; &ge; 2 on ~150,000 transitions (minimum 2) and 300,000 orbit "
     "anchor steps", "pass"),
]
t = Table([[P("<b>Check</b>", CELLR), P("<b>Scope</b>", CELLR), P("<b>Result</b>", CELLR)]] +
          [[P(a, CELLR), P(b, CELLR), P(c, CELLR)] for a, b, c in vrows],
          colWidths=[2.1*inch, 4.0*inch, 0.8*inch], repeatRows=1)
t.setStyle(table_style())
story.append(t)
story.append(Spacer(1, 6))
story.append(P(
    "<b>Erratum (found and fixed).</b> Verifying the anchor map of Section 6.1 "
    "against the base rules exposed a bug in the level-3 implementation: the "
    "seed rule had been written as (0, 2, max(2b + 1, 5)), which is wrong at "
    "exactly b = 1 (the correct successor of (0, 1, 0, 1) is (0, 2, 0, 3), "
    "confirmed against the original 13 rules). The error affects only the "
    "single state (0, 1, 1) &mdash; a cycle boundary with D = 1, which the "
    "orbit of D = 17 never visits &mdash; and all code and tables have been "
    "corrected. The full 200,000-cycle deep run was re-executed with the "
    "corrected rule and reproduces the original run exactly (identical "
    "step-count exponents at every 50,000-cycle checkpoint and identical final "
    "D), so the 10<super>150,514</super> bound of Section 8.4 stands as "
    "stated."))

# ==================== 10. Performance ==================================
story.append(P("11. Performance", H1))
prows = [
    ("Base system", "10<super>60</super>", "&mdash; (infeasible)"),
    ("Level 2", "~8,700", "~8,200&ndash;8,900 across starts"),
    ("Level 3", "~1,000", "~980&ndash;1,030 across starts"),
    ("Level 4 (from (0,0,0,0))", "~80 cycles",
     "one cycle &#8776; 10 rule applications; see Section 6"),
]
t = Table([[P("<b>System</b>", CELLR),
            P("<b>Steps to cover 10<super>60</super> base steps</b>", CELLR),
            P("<b>Range observed</b>", CELLR)]] +
          [[P(a, CELLR), P(b, CELLR), P(c, CELLR)] for a, b, c in prows],
          colWidths=[1.6*inch, 2.9*inch, 2.4*inch])
t.setStyle(table_style())
story.append(t)
story.append(Spacer(1, 6))
story.append(P(
    "Because each accelerated step is constant-cost integer arithmetic and "
    "cascades cover exponentially many base steps, simulating N base steps "
    "requires only polylogarithmic work in N."))

# ==================== 11. Artifacts ====================================
story.append(P("12. Code artifacts", H1))
arows = [
    ("collatz.py", "the original 13-rule base system, exactly as specified"),
    ("accel.py", "level-2 accelerated system with per-rule step-exact verification"),
    ("accel2.py", "level-3 cascade super-rules, verified against level 2"),
    ("accel3.py", "the complete closed-form level-3 system of Section 5.3, verified"),
    ("criterion.py", "the halting criterion of Section 8.1, proof notes and full verification"),
    ("orbit.py", "the deep verified run from (0, 0, 0, 0) with cascade-internal line checks"),
    ("onedim.py", "level 4: the one-dimensional return-map system for the fixed start, verified"),
    ("formal.py", "the anchor map G of Section 6.1 and the piecewise-affine structure of F, verified"),
    ("afterstep25.py", "the after-step-25 system of Section 6.4 with exact cost certificates, verified"),
    ("mod16.py", "the mod-16 confinement theorem of Section 8.3 and the modulus-search, verified"),
    ("gaps.py", "the three results of Section 9.6: the expansion margin, the 2-adic obstruction, and the mantissa disproof"),
    ("potential.py", "the monotone potential &Phi; = 2b + d of Section 9.6(d): conservation lemma, per-rule increments, no-cycle corollary"),
    ("traj.py", "whole-trajectory equivalence checks and rule-usage profiling"),
]
t = Table([[P(f"<font face='Courier'>{a}</font>", CELLR), P(b, CELLR)] for a, b in arows],
          colWidths=[1.4*inch, 5.5*inch])
t.setStyle(table_style(header=False))
story.append(t)
story.append(Spacer(1, 4))
story.append(P("Each file re-runs its own verification suite when executed with "
               "<font face='Courier'>python3 &lt;file&gt;</font>."))

doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=0.9*inch, rightMargin=0.9*inch,
                        topMargin=0.8*inch, bottomMargin=0.8*inch,
                        title="Acceleration of a Collatz-Like System")
doc.build(story)
print("wrote", OUT)
