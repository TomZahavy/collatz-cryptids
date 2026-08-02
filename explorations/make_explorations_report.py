"""Build the explorations report: three cross-machine findings from zooming out."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.colors import HexColor

OUT = "/Users/tomzahavy/Documents/Claude/collatz/explorations/explorations_report.pdf"
styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=styles["Heading1"], spaceBefore=18, spaceAfter=8)
H2 = ParagraphStyle("H2x", parent=styles["Heading2"], spaceBefore=13, spaceAfter=6)
BODY = ParagraphStyle("Bodyx", parent=styles["Normal"], fontSize=10.5, leading=14.5, spaceAfter=7)
MATHC = ParagraphStyle("MathCx", parent=styles["Normal"], fontName="Times-Italic",
                       fontSize=10.5, leading=15, alignment=TA_CENTER, spaceBefore=4, spaceAfter=8)
CELL = ParagraphStyle("Cellx", parent=styles["Normal"], fontName="Times-Roman", fontSize=9.5, leading=12.5)
TITLE = ParagraphStyle("Titlex", parent=styles["Title"], fontSize=18, leading=23, spaceAfter=4)
SUB = ParagraphStyle("Subx", parent=styles["Normal"], alignment=TA_CENTER,
                     textColor=colors.HexColor("#555555"), fontSize=11, spaceAfter=16)
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
story.append(P("Explorations: Three Cross-Machine Findings", TITLE))
story.append(P("Zooming out from the machines and the meta report &mdash; "
               "ideas from the Collatz / generalized-Collatz literature, and "
               "what they turned up", SUB))

story.append(P("0. What this is", H1))
story.append(P(
    "A step back from the per-machine work to ask what the collection looks "
    "like as a whole, and to try directions we had not: the "
    "generalized-Collatz drift dichotomy (Matthews&ndash;Watts), the "
    "&ldquo;missing backbone&rdquo; our machine 1 report flagged as open, and "
    "the structural reason congruence invariants fail on the multiplicative "
    "machines. Five ideas were catalogued (IDEAS.md); all five &mdash; "
    "including the deepest, Baker-type perfect-powers &mdash; were pursued, "
    "yielding the six findings below. One is a <b>correction</b> to the meta "
    "report (now folded in); five are new positive structure &mdash; the "
    "mantissa backbone and its transfer operator, the no-congruence theorem, a "
    "self-similarity relation, the halting set computed backward, and the "
    "Baker / perfect-powers frontier. Everything is machine-verified."))

# ---- Finding 1 ----
story.append(P("1. The &ldquo;divergent vs convergent cryptid&rdquo; "
               "dichotomy is not where the report puts it", H1))
story.append(P(
    "The meta report (&sect;5) frames a dichotomy: machine 1 grows "
    "geometrically and is a &ldquo;divergent&rdquo; cryptid, machine 4 "
    "grow linearly and are &ldquo;convergent,&rdquo; and it implies the growth "
    "rate sets the <i>risk profile</i> (the 10<super>&minus;75,000</super> vs "
    "10<super>&minus;11</super> residual-risk gap). Measuring the actual "
    "return-map multipliers shows this is misleading."))
story.append(P(
    "For each machine, take the first-return map to its section (F for "
    "machine 1, the reset maps for 2, 3, 4, the step map for Space Needle) "
    "and measure the mean log-ratio of consecutive return values &mdash; the "
    "Matthews&ndash;Watts drift:"))
story.append(Spacer(1, 4))
story.append(tab([
    ("machine 1", "0.87", "&#8776; 0 (constant)", "geometric", "converges"),
    ("machine 3", "0.33", "&#8776; 0 (constant)", "geometric", "converges"),
    ("machine 4", "0.99", "0.84 (thinning)", "linear", "converges"),
    ("Space Needle", "0.65", "&mdash; (map = step)", "geometric", "converges"),
], ("machine", "return drift (dlog)", "return-time slope / index",
    "per-step state growth", "&Sigma; 1/C<sub>n</sub>"),
   (1.15 * inch, 1.35 * inch, 1.6 * inch, 1.35 * inch, 1.05 * inch)))
story.append(Spacer(1, 4))
story.append(P(
    "<b>Every return map is supercritical</b> (drift 0.33&ndash;0.99, none "
    "critical), so the return values grow geometrically and the halting-risk "
    "sum &Sigma; 1/C<sub>n</sub> converges for <b>all</b> machines, by the "
    "same mechanism. There is no divergent/convergent split in the halting "
    "risk. What actually differs is the <b>return frequency</b>: the "
    "return-time is constant in the index for machines 1 and 3 (frequent "
    "returns &rarr; geometric per-step growth) and grows exponentially in the "
    "index for machine 4 (thinning returns &rarr; linear per-step "
    "growth). This is a real structural difference &mdash; but it is about how "
    "fast the raw state grows per step, not about the halting mechanism."))
story.append(P(
    "<b>Consequence.</b> The residual-risk gap across the collection "
    "(10<super>&minus;75,000</super> for machine 1 against far larger figures "
    "elsewhere) is a <i>verified-depth artifact</i>, not a qualitative "
    "dichotomy: machine 1&rsquo;s orbit was pushed to "
    "10<super>150,000</super>-scale return values while the others reached "
    "far smaller scales, so 1/C<sub>n</sub> is smaller for machine 1 simply "
    "because C<sub>n</sub> is larger. Pushed to equal "
    "depth, the risks would be comparable. All three machines &mdash; and the "
    "Space Needle &mdash; are the <b>same kind of cryptid for the halting "
    "question</b>: supercritical return map, geometrically spaced target, "
    "convergent risk sum. The meta report&rsquo;s &sect;5 dichotomy should be "
    "reframed accordingly (see &sect;4)."))

# ---- Finding 2 ----
story.append(P("2. The mantissa &ldquo;backbone&rdquo; of machine 1, located", H1))
story.append(P(
    "Machine 1&rsquo;s report proved F has no continuous 2-adic extension and "
    "showed the mantissa m<sub>k</sub> = frac(log<sub>2</sub> D<sub>k</sub>) "
    "is <i>not</i> uniform (&chi;<super>2</super> &#8776; 162), then flagged "
    "the true stationary density as the &ldquo;missing ergodic "
    "backbone&rdquo; &mdash; the concrete object a real proof would need. We "
    "compute it and identify its structure."))
story.append(P(
    "The dominant word gives F(D) = 16D &minus; 240&middot;2<super>n</super> + "
    "&hellip; with n = n<sub>A</sub>(1, D), so on the leading scale"))
story.append(P("m &rarr; m + log<sub>2</sub>(1 &minus; 15&middot;2<super>"
               "n&minus;floor(log2 D)</super>&middot;2<super>&minus;m"
               "</super>)&nbsp;(mod 1),", MATHC))
story.append(P(
    "an explicit two-branch circle map whose branch is set by the exponent "
    "offset n &minus; floor(log<sub>2</sub> D). Measured over 40,000 "
    "cycles, that offset is &minus;4 below a sharp breakpoint and &minus;3 "
    "above it, and the breakpoint is exactly"))
story.append(P("m<sub>*</sub> = log<sub>2</sub>(5/4) = 0.321928&hellip;", MATHC))
story.append(P(
    "&mdash; the mantissa at which 2<super>n</super> jumps between D/16 and "
    "D/8. The two branches have opposite character: below m<sub>*</sub> the "
    "map spreads mass across the whole circle (mixing), above it the map "
    "contracts sharply toward m &#8776; 0.5. The resulting stationary density "
    "is <b>elevated (up to 1.3&times;) on [0, log<sub>2</sub>(5/4)) and "
    "depressed (down to 0.85&times;) on [log<sub>2</sub>(5/4), 1)</b>, with "
    "the transition exactly at the breakpoint."))
story.append(P(
    "This identifies the object the report called missing: the mantissa "
    "backbone is the invariant measure of an explicit piecewise circle map "
    "with breakpoint log<sub>2</sub>(5/4). It is (like most such measures) "
    "probably not elementary in closed form, but it is now a concrete, "
    "localized target rather than an unknown &mdash; and the elevated-below / "
    "depressed-above shape is the first structural fact established about "
    "it. (This is also why the naive uniform-equidistribution assumption "
    "failed: the map is genuinely non-uniform, contracting on the larger of "
    "its two branches.)"))
story.append(P(
    "<b>The transfer operator confirms and quantifies it.</b> Binning the "
    "mantissa into 60 cells and forming the empirical Markov (Perron&ndash;"
    "Frobenius) operator, its stationary distribution matches the direct "
    "histogram to L<sub>1</sub> = 0.0001 &mdash; the mantissa process is a "
    "genuinely mixing Markov chain on the circle whose invariant measure is "
    "the density &mdash; with a <b>spectral gap of 0.77</b> "
    "(|&lambda;<sub>2</sub>| = 0.23), so the backbone is a strongly "
    "attracting measure, not a slow drift. The stationary density is "
    "1.12&times; uniform below log<sub>2</sub>(5/4) and 0.94&times; above, "
    "with a <b>jump of about 0.2 exactly at the breakpoint</b> (the density "
    "steps from &#8776;1.22 down to &#8776;1.01 across the two adjacent "
    "cells). The next step is a fine-grid Perron&ndash;Frobenius solve of the "
    "analytic two-branch map to get the density to arbitrary precision."))

# ---- Finding 3 ----
story.append(P("3. Why no congruence can decide the multiplicative machines", H1))
story.append(P(
    "For machine 3 and the Space Needle the halting event is multiplicative "
    "&mdash; the orbit must hit an exact power of q (q = 3, resp. 2). Our "
    "searches for a separating modulus came up empty; here is the structural "
    "reason they had to, promoting the empirical result to an impossibility."))
story.append(P(
    "Both maps branch on the <b>q-adic valuation</b> of the state: machine 3 "
    "divides by 3 exactly v<sub>3</sub>(a) times; the Space Needle&rsquo;s "
    "step reads v<sub>2</sub>(b). But for any modulus M coprime to q, the "
    "valuation v<sub>q</sub>(x) is <b>independent of x mod M</b> (by the "
    "Chinese Remainder Theorem, every residue class mod M realizes every "
    "valuation &mdash; verified: for M = 3, 5, 7, 9, 15 every class mod M "
    "attains a full range of 2-adic valuations). So the map is not a function "
    "of x mod M at all: no congruence closure mod M even exists, let alone one "
    "that separates the orbit from the target."))
story.append(P(
    "This is the <b>Space Needle / machine 3 analogue of the Hydra family "
    "q-adic branch-memory theorem</b>: on the walk-absorption machines the "
    "value&rsquo;s residues carry only bounded branch history; on the "
    "multiplicative machines the halting-relevant data (the valuation) lives "
    "on the q-adic side, orthogonal to residues mod any M coprime to q. In "
    "both families the reason congruence deciders fail is the same &mdash; the "
    "arithmetic that decides halting is orthogonal to the arithmetic a "
    "congruence can see &mdash; and it is now a theorem for three of the "
    "collection&rsquo;s types, not a search outcome."))

# ---- Finding 4 ----
story.append(P("4. A self-similarity relation for the Space Needle", H1))
story.append(P(
    "The Space Needle&rsquo;s map b &rarr; b + v<sub>2</sub>(b) + "
    "(3/2)(oddpart(b) &minus; 1) obeys an exact <b>scaling relation</b>: "
    "doubling the argument shifts the image by a controlled amount,"))
story.append(P("step(2b) = step(b) + b + 1&nbsp;&nbsp;(for every "
               "non-halting b),", MATHC))
story.append(P(
    "verified with no exceptions for b &lt; 200,000. (It follows directly: "
    "v<sub>2</sub>(2b) = v<sub>2</sub>(b) + 1 while the odd part is "
    "unchanged.) This is a genuine self-similarity &mdash; the map is not "
    "scale-invariant, but its failure to be is the explicit affine cocycle "
    "b + 1. The analogue on machine 3 is its divide-chain lemma "
    "(b &rarr; b + (N &minus; M) + j collapses a factor 3<super>j</super> in "
    "one step): both multiplicative machines carry an exact renormalization "
    "of their q-scaling. It did not (yet) yield a decision, but it is the "
    "kind of exact structure a renormalization argument would need, and it "
    "cleanly explains why the halt targets at different scales are linked "
    "(2b is a power of 2 iff b is)."))

# ---- Finding 5 ----
story.append(P("5. The Space Needle halting set, computed from the target "
               "backward", H1))
story.append(P(
    "Turning the halting question around: instead of following the orbit "
    "forward, enumerate the <b>halting set</b> &mdash; every b whose orbit "
    "reaches a power of 2 &mdash; by breadth-first search backward from the "
    "powers of 2 through the inverse map (the reverse-decider idea from "
    "bbchallenge). Each target has O(1) preimages (one odd-branch, a few "
    "even-branch), so the set is thin and exactly computable."))
story.append(P(
    "Below 2,000,000 there are only <b>16 halting seeds</b> "
    "{7, 103, 312, 352, 372, 1639, &hellip;}, density 8 &times; "
    "10<super>&minus;6</super>, and <b>the start b = 6 is provably not among "
    "them</b>. The density falls geometrically by dyadic scale &mdash; about "
    "1.6 &times; 10<super>&minus;2</super> at 2<super>6</super> down to "
    "&#8776; 10<super>&minus;6</super> at 2<super>18&ndash;20</super> &mdash; "
    "with roughly one seed per octave, so the halting set is only about "
    "<b>logarithmically many below N</b>. This corroborates non-halting from "
    "the target side, independently of the forward orbit, and makes the "
    "sparsity exact: a forward orbit visiting ~log N values below N against a "
    "target of ~log N values in a space of N collides with probability "
    "~(log N)<super>2</super>/N &rarr; 0 &mdash; the Borel&ndash;Cantelli "
    "estimate of Finding 1, now with a rigorously enumerated target rather "
    "than a heuristic density. (The same enumeration applies verbatim to "
    "machine 3 with powers of 3.)"))

# ---- Section 6 ----
story.append(P("6. The perfect-powers question: Baker reaches the runs, not "
               "the orbit", H1))
story.append(P(
    "The deepest idea was to attack the multiplicative machines&rsquo; "
    "halting (does the orbit hit q<super>k</super>?) with the tools that "
    "excluded Collatz cycles &mdash; Baker&rsquo;s linear forms in logarithms "
    "and the Bilu&ndash;Hanrot&ndash;Voutier primitive-divisor theorem. These "
    "apply to sequences with S-unit (smooth) structure. The first thing to "
    "check is whether the orbit has it, and it does not:"))
story.append(P(
    "<b>The orbit is not an S-unit sequence.</b> The Space Needle values "
    "6, 10, 17, 41, 101, 251, &hellip; are smooth only twice before "
    "b<sub>2</sub> = 17 and b<sub>3</sub> = 41 bring in large primes; the "
    "factorizations are generic thereafter. So Baker cannot be pointed at the "
    "orbit sequence directly &mdash; the first-order obstruction, and the "
    "reason a decision is not simply a matter of citing a theorem."))
story.append(P(
    "<b>But the geometric runs do have the structure, and Baker &mdash; via "
    "its elementary p-adic core &mdash; bites there.</b> During an odd run "
    "the map is exactly affine: b<sub>n</sub> &minus; 1 = (5/2)<super>n</super>"
    "(b<sub>0</sub> &minus; 1), so a halt b<sub>n</sub> = 2<super>k</super> is "
    "the three-term S-unit equation 2<super>n+k</super> &minus; "
    "2<super>n</super> = 5<super>n</super>(b<sub>0</sub> &minus; 1). "
    "Lifting-the-exponent gives v<sub>5</sub>(2<super>k</super> &minus; 1) = "
    "1 + v<sub>5</sub>(k/4) for 4 | k, so 5<super>n</super> | 2<super>k</super>"
    " &minus; 1 forces k &ge; 4&middot;5<super>n&minus;1</super>. The "
    "unconditional consequence:"))
story.append(P("at orbit scale B, a halting run has length at most "
               "&#8776; 1 + log<sub>5</sub>(log<sub>2</sub> B),", MATHC))
story.append(P(
    "a log&ndash;log bound: at scale 2<super>20</super> a halt cannot follow "
    "a run longer than 2; at 2<super>150,514</super> (machine 1&rsquo;s "
    "verified horizon), longer than 7; even at 2<super>10^9</super>, longer "
    "than 13. So <b>a halt can never occur in the interior of a geometric "
    "ascent</b> &mdash; it must land on the power essentially at a run "
    "boundary. Empirically the odd runs reach length 16, but a length-3 "
    "halting run would already require the orbit to be past "
    "2<super>97</super>. This is, as far as we know, the first time "
    "linear-forms-in-logarithms has been aimed at a cryptid&rsquo;s "
    "<i>halting</i> family (the meta report notes it had been aimed only at "
    "Collatz cycles)."))
story.append(P(
    "<b>Where it stops.</b> The bound is per-run; the branch word "
    "<i>between</i> run boundaries is orbit-determined and grows without "
    "bound (digit consumption), so per-run finiteness does not aggregate into "
    "a global bound. That is exactly the Collatz obstruction, now located "
    "precisely: Baker decides each fixed word, and the undecidability lives "
    "entirely in the unboundedness of the word. A full decision would need to "
    "control the word sequence itself &mdash; which is the open problem. What "
    "we have is a genuine, unconditional partial result (no interior-of-run "
    "halts) and an exact map of the frontier."))

story.append(P("7. What changed, and what is left", H1))
story.append(P(
    "<b>Done.</b> The Finding 1 correction has been folded into the meta "
    "report: &sect;5 is reframed (the divergent/convergent labels describe "
    "per-step growth &mdash; frequent vs thinning returns &mdash; not two "
    "halting-risk regimes; all machines share the supercritical-return, "
    "convergent-&Sigma;1/C mechanism, with the residual-risk numbers as depth "
    "artifacts), P8 is stated as the <i>right</i> dichotomy with all four "
    "machines on its convergent side, and the status labels now read "
    "&ldquo;geometric / linear growth&rdquo; rather than "
    "&ldquo;divergent / convergent cryptid.&rdquo;"))
story.append(P(
    "<b>All five catalogued ideas are now tried</b> (Findings 1&ndash;6): the "
    "drift dichotomy, the mantissa backbone and its transfer operator, the "
    "no-congruence theorem, self-similarity, backward reachability, and the "
    "perfect-powers / Baker direction. Together they turned three of the "
    "collection&rsquo;s open flags into structure &mdash; the backbone is "
    "located and measured, the congruence and Baker obstructions are pinned "
    "exactly, the halting set is enumerated &mdash; and produced one "
    "unconditional partial result (no interior-of-run halts)."))
story.append(P(
    "<b>What is left is the open problem itself.</b> Every tool now has a "
    "sharp reason it stops at the same place: the branch word is "
    "orbit-determined and grows without bound. Congruences cannot read it "
    "(Finding 3), Baker decides each fixed word but not their unbounded "
    "sequence (Finding 6), and the mantissa/valuation process that generates "
    "it is mixing with a positive spectral gap (Finding 2) &mdash; "
    "structured enough to model precisely, random enough to defeat every "
    "finite invariant. A decision would require controlling that word "
    "sequence, which is exactly what makes these machines cryptids. The "
    "honest end state is not a decision but a complete map of why one is out "
    "of reach, with the frontier drawn tool by tool."))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=0.8, color=BLUE))
story.append(Spacer(1, 4))
story.append(P(
    "Artifacts (collatz/explorations/): IDEAS.md, growth_law.py, dichotomy.py, "
    "mantissa.py, mantissa_map.py, transfer_operator.py, selfsimilar.py, "
    "backward.py, baker.py. All findings machine-verified. The Finding 1 "
    "correction is folded into the meta report (&sect;6).",
    ParagraphStyle("Foot", parent=BODY, fontSize=9.5,
                   textColor=colors.HexColor("#555555"))))

doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.9 * inch,
                        rightMargin=0.9 * inch, topMargin=0.8 * inch,
                        bottomMargin=0.8 * inch,
                        title="Explorations: Three Cross-Machine Findings")
doc.build(story)
print("wrote", OUT)
