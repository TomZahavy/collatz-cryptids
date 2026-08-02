"""Build the WS3-transfer report: the forbidden-branch sieve across all machines."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.colors import HexColor

OUT = "/Users/tomzahavy/Documents/Claude/collatz/baker/sweep_report.pdf"

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
story.append(P("The forbidden-branch sieve, across the collection", TITLE))
story.append(P("WS3 transfer sweep &mdash; machine 3&rsquo;s halting branch is "
               "pinned to a single valuation, and the sieve&rsquo;s reach is "
               "governed by the thinness of the halting set &mdash; "
               "July 26, 2026", SUB))
story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=12))

story.append(P("1. The sieve in machine-independent form", H1))
story.append(P(
    "WS3&rsquo;s exclusion was derived for the Space Needle from that "
    "machine&rsquo;s own algebra. Stripped to its skeleton it needs only that "
    "the return map be affine on each branch. Let F act on branch b as "
    "F(x) = &alpha;<sub>b</sub>x + &beta;<sub>b</sub> with "
    "&alpha;<sub>b</sub> = N<sub>b</sub>/D<sub>b</sub> in lowest terms and "
    "fixed point x*<sub>b</sub> = P<sub>b</sub>/Q<sub>b</sub>, also in lowest "
    "terms. A single step on branch b satisfies "
    "D<sub>b</sub>(Q<sub>b</sub>x<sub>1</sub> &minus; P<sub>b</sub>) = "
    "N<sub>b</sub>(Q<sub>b</sub>x<sub>0</sub> &minus; P<sub>b</sub>), and "
    "since gcd(N<sub>b</sub>, D<sub>b</sub>) = 1 this forces"))
story.append(P("N<sub>b</sub> &nbsp;divides&nbsp; Q<sub>b</sub>x<sub>1</sub> "
               "&minus; P<sub>b</sub>&nbsp;&nbsp;&nbsp;&nbsp;(*)", MATHC))
story.append(P(
    "If the step ends in a halt then x<sub>1</sub> lies in the halting set H, "
    "so a halt can follow a b-step only if some h in H satisfies "
    "Q<sub>b</sub>h &equiv; P<sub>b</sub> (mod N<sub>b</sub>). When that has "
    "no solution the branch is <b>forbidden</b>: no orbit, from any start, at "
    "any scale, at any time, can halt out of it. No run is needed &mdash; a "
    "single step already carries the content, and iterating (*) n times gives "
    "the run version used for the Needle."))
story.append(P(
    "Each machine supplies only its branch data (N, D, P, Q) and a decision "
    "procedure for membership in H. Everything else is shared code."))

story.append(P("2. Machine 3: the halting branch is a single valuation", H1))
story.append(P(
    "Machine 3&rsquo;s reset map, verified against its own accelerated step, "
    "is G(a) = (3<super>j+1</super>+1)m + (r&middot;3<super>j</super> + j + "
    "c<sub>r</sub>) on the branch a = 3<super>j</super>(3m + r), r in {1,2}, "
    "c<sub>1</sub> = 3, c<sub>2</sub> = 4. In affine form N = "
    "3<super>j+1</super>+1, D = 3<super>j+1</super>, and the fixed point is "
    "an <i>integer</i>, x* = r&middot;3<super>j</super> &minus; "
    "3<super>j+1</super>(j + c<sub>r</sub>), so Q = 1. The halting set is the "
    "powers of 27. The sieve condition is therefore"))
story.append(P("27<super>k</super> &equiv; r&middot;3<super>j</super> + j + "
               "c<sub>r</sub>&nbsp;&nbsp;(mod 3<super>j+1</super> + 1)",
               MATHC))
story.append(P(
    "using 3<super>j+1</super> &equiv; &minus;1. Exact discrete logarithm says "
    "every branch with j &le; 20 fails except (1,1) and (1,2). The reason is "
    "visible and gives a proof for <i>all</i> j. Because 3<super>j+1</super> "
    "&equiv; &minus;1, the group generated by 3 modulo N is exactly "
    "{3<super>i</super>} together with {N &minus; 3<super>i</super>} for "
    "i &le; j &mdash; only 2(j+1) residues, and every power of 27 is one of "
    "them. Sorted, those residues leave a <b>large gap</b>: nothing lies "
    "strictly between 3<super>j</super> and 2&middot;3<super>j</super>+1, and "
    "nothing between 2&middot;3<super>j</super>+1 and "
    "2&middot;3<super>j</super> + 2&middot;3<super>j&minus;1</super>+1. For "
    "j &ge; 2 the fixed point lands strictly inside one of those gaps: "
    "r = 1 gives 3<super>j</super> + j + 3 in the first (since j+2 &lt; "
    "3<super>j</super>), r = 2 gives 2&middot;3<super>j</super> + j + 4 in the "
    "second (since j+3 &lt; 2&middot;3<super>j&minus;1</super>). And j = 0 is "
    "excluded because N = 4 there while every power of 27 is odd."))
story.append(P(
    "<b>Theorem (machine 3&rsquo;s halting branch).</b> Machine 3 can halt "
    "only out of a step whose branch has v<sub>3</sub>(a) = 1. Unconditional, "
    "every start, every scale, every time."))
story.append(P(
    "This is qualitatively stronger than the Needle result. There the excluded "
    "valuations were a scattered 19 of the first 35, leaving an infinite "
    "allowed tail; here the allowed set is a <b>single valuation</b>. Since "
    "P(v<sub>3</sub> = 1) = 2/9, it removes 7/9 = 77.78% of all steps &mdash; "
    "measured 77.61% over the orbit&rsquo;s first 100,000 steps."))

story.append(P("3. The sieve iterates: the last two steps are both pinned", H1))
story.append(P(
    "Because H is geometric and the branches are affine, the preimage of a "
    "geometric family is again a geometric family, so the sieve can be run "
    "backwards. Solving (*) exactly gives the depth-1 halting seeds in closed "
    "form &mdash; two families, with R = 27<super>4</super>:"))
story.append(P("F<sub>1</sub> = { (3<super>5</super>R<super>t</super> &minus; "
               "33)/10 } = {21, 12914013, &hellip;} &nbsp;&nbsp;&nbsp; "
               "F<sub>2</sub> = { (3<super>14</super>R<super>t</super> &minus; "
               "39)/10 } = {478293, &hellip;}", MATHC))
story.append(P(
    "Sieving these in turn pins the next-to-last step as well. A closed-form "
    "<b>parity lemma</b> does half of it outright: every member of "
    "F<sub>1</sub> and F<sub>2</sub> is odd and N = 3<super>j+1</super>+1 is "
    "always even, so (*) forces P odd; P has parity r + j + c<sub>r</sub> and "
    "r + c<sub>r</sub> is even for both r, hence <b>j must be odd</b> "
    "&mdash; which alone kills j = 0, the branch carrying two thirds of all "
    "steps. The remaining odd j are cleared by a fast exact test: multiplying "
    "(*) by 10 gives 3<super>e+12t</super> &equiv; 10P + C (mod N), whose left "
    "side ranges over at most 2(j+1) known residues, so membership is a tiny "
    "finite check. No j other than 1 survives, for j &le; 500."))
story.append(P(
    "<b>Result (step &minus;2, machine-verified).</b> The next-to-last branch "
    "before a halt also has v<sub>3</sub> = 1. So the last two steps before "
    "any halt both have valuation 1 &mdash; excluding "
    "1 &minus; (2/9)<super>2</super> = <b>95.06%</b> of consecutive step "
    "pairs, measured 95.07% on the orbit."))
story.append(P(
    "<b>And it stops there.</b> Continuing the backward family enumeration "
    "shows the pinning has depth exactly 2: three steps back the valuation may "
    "be 0 or 1, four steps back 0, 1 or 2, five steps back 0 to 4. The family "
    "count grows 2, 4, 6, 17, 80 with depth, so the backward tree does not "
    "die and no decision follows. The constraint is a sharp local condition on "
    "how a halt must be approached, not a global obstruction."))
story.append(tab([
    ("&minus;1", "{1}", "PROVED for all j (gap argument), verified j &le; 400"),
    ("&minus;2", "{1}", "Parity lemma proved for all even j; verified j &le; 500"),
    ("&minus;3", "{0, 1}", "backward family enumeration, j &le; 24"),
    ("&minus;4", "{0, 1, 2}", "backward family enumeration, j &le; 24"),
    ("&minus;5", "{0, 1, 2, 3, 4}", "backward family enumeration, j &le; 24"),
], ("step before halt", "possible v<sub>3</sub>", "status"),
    (1.3 * inch, 1.5 * inch, 3.5 * inch)))

story.append(P("4. The sweep: where the sieve bites and where it cannot", H1))
story.append(tab([
    ("Space Needle", "{2<super>m</super>}", "geometric",
     "19 of the first 35 valuations forbidden; 28.7% of steps"),
    ("Machine 3", "{27<super>k</super>}", "geometric",
     "<b>v<sub>3</sub> pinned to 1</b> at each of the last two steps; 77.78% "
     "of steps, 95.06% of step pairs"),
    ("Fenrir", "{n : 4 divides n}", "a congruence class",
     "<b>vacuous</b> &mdash; gcd(4, 5) = 1, so both branches are solvable and "
     "nothing is excluded"),
    ("Hydra / Antihydra", "first passage of a walk", "not a set of values",
     "<b>vacuous</b> &mdash; halting is not a condition on the iterate&rsquo;s "
     "value, so (*) says nothing"),
    ("Machine 4", "b = a + 3, a odd", "a line in two variables",
     "out of scope as stated: no one-variable return map, so there is no "
     "single branch-affine coordinate to sieve"),
], ("machine", "halting set H", "shape of H", "what the sieve gives"),
    (1.0 * inch, 1.35 * inch, 1.25 * inch, 2.7 * inch)))
story.append(Spacer(1, 6))
story.append(P(
    "<b>The pattern.</b> The sieve&rsquo;s strength is governed by how thin H "
    "is <i>as a set of values</i>, and nothing else. A geometric H makes (*) a "
    "discrete-logarithm condition that can fail, and the sparser the group "
    "generated by the base modulo N, the more often it does &mdash; which is "
    "why base 3 beats base 2 so decisively here: modulo "
    "3<super>j+1</super>+1 the powers of 3 collapse to 2(j+1) residues with "
    "huge gaps between them, whereas modulo 2<super>v+1</super>+3 the powers "
    "of 2 are spread out. A congruence-class H is immune, because a congruence "
    "class meets every residue class of any coprime modulus. And a halting "
    "condition that is not about the iterate&rsquo;s value at all &mdash; a "
    "first passage, a coincidence between two counters &mdash; is outside the "
    "method entirely. This also says where to look next: the sieve is a tool "
    "for multiplicative-coincidence cryptids, and only for those."))

story.append(P("5. Verification ledger", H1))
story.append(tab([
    ("The general form (*)",
     "PROVED (affine conjugation to the fixed point; gcd(N, D) = 1). The "
     "derived branch data and (*) were machine-checked against machine "
     "3&rsquo;s own verified map on 39,989 values a &lt; 40,000."),
    ("Machine 3: v<sub>3</sub> = 1 at the halting step",
     "PROVED for all j by the gap argument, with each step of the proof "
     "machine-checked (the description of the group generated by 3, the two "
     "gaps, and the inequalities placing the fixed point inside one) for "
     "j &le; 400; and cross-checked by direct membership test, no gap "
     "argument used, for j &le; 59."),
    ("Machine 3: v<sub>3</sub> = 1 at the next-to-last step",
     "PARTLY PROVED. The parity lemma (j odd) is closed form for all j. The "
     "elimination of the remaining odd j is MACHINE-VERIFIED for j &le; 500 "
     "by an exact finite test, not proved in general."),
    ("Independent confirmation",
     "MACHINE-VERIFIED by brute force with no sieve theory used: over all "
     "a &lt; 4,000,000, every value halting within three steps has "
     "v<sub>3</sub> = 1 at the last step and at the next-to-last step. The "
     "only two-step seed found is 15 &rarr; 21 &rarr; 27."),
    ("Orbit measurements",
     "MACHINE-VERIFIED over 100,000 steps of the true reset orbit: 77.61% of "
     "steps and 95.07% of consecutive pairs excluded, against asymptotic "
     "77.78% and 95.06%. No halt; the orbit never touched the spine."),
    ("Depth of the pinning",
     "MACHINE-VERIFIED for branches j &le; 24 at depths up to 5. The "
     "loosening at step &minus;3 is a positive finding (explicit surviving "
     "families exist), not a failure to exclude."),
    ("Non-halting", "OPEN for every machine here. The sieve constrains how a "
     "halt must be approached; it excludes no orbit."),
], ("claim", "status"), (1.9 * inch, 4.4 * inch)))
story.append(Spacer(1, 8))
story.append(P("Code: sieve.py (the general sieve), sieve_m3.py (machine 3 "
               "branch data and brute-force check), m3_theorem.py (the gap "
               "proof), m3_step2.py (parity lemma and the large-j test), "
               "m3_deep.py (backward family enumeration).", CODE))

doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.85 * inch,
                        rightMargin=0.85 * inch, topMargin=0.8 * inch,
                        bottomMargin=0.8 * inch,
                        title="The forbidden-branch sieve across the collection")
doc.build(story)
print(f"wrote {OUT}")
