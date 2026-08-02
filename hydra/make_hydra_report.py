"""Build the Hydra-family report (program step 1 of the meta plan)."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.colors import HexColor

OUT = "/Users/tomzahavy/Documents/Claude/collatz/hydra/hydra_report.pdf"

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=styles["Heading1"], spaceBefore=18, spaceAfter=8)
H2 = ParagraphStyle("H2x", parent=styles["Heading2"], spaceBefore=14, spaceAfter=6)
BODY = ParagraphStyle("Bodyx", parent=styles["Normal"], fontSize=10.5,
                      leading=14.5, spaceAfter=7)
MATH = ParagraphStyle("Mathx", parent=styles["Normal"], fontName="Times-Italic",
                      fontSize=10.5, leading=15)
MATHC = ParagraphStyle("MathCx", parent=MATH, alignment=TA_CENTER,
                       spaceBefore=4, spaceAfter=8)
CELL = ParagraphStyle("Cellx", parent=styles["Normal"], fontName="Times-Roman",
                      fontSize=9.5, leading=12.5)
TITLE = ParagraphStyle("Titlex", parent=styles["Title"], fontSize=19,
                       leading=24, spaceAfter=4)
SUB = ParagraphStyle("Subx", parent=styles["Normal"], alignment=TA_CENTER,
                     textColor=colors.HexColor("#555555"), fontSize=11,
                     spaceAfter=18)

BLUE = HexColor("#1a3c6e")


def P(text, style=BODY):
    return Paragraph(text, style)


def table_style():
    return TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c4d6")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef7")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f6f8fb")])])


def tab(rows, header, widths):
    data = [[P(f"<b>{h}</b>", CELL) for h in header]]
    data += [[P(c, CELL) for c in r] for r in rows]
    t = Table(data, colWidths=list(widths), repeatRows=1)
    t.setStyle(table_style())
    return t


story = []
story.append(P("The Hydra Family Through the Toolkit", TITLE))
story.append(P("Hydra, Antihydra and Fenrir as one system &mdash; program "
               "step 1 of the collection&rsquo;s research plan", SUB))

# ---------------- 1 ----------------
story.append(P("1. Overview", H1))
story.append(P(
    "This report applies the toolkit developed on machine 1 (see the meta report and the machine reports in this collection) to the "
    "closest catalogued relatives: the Busy Beaver cryptids <b>Hydra</b> "
    "(BB(2,5)) and <b>Antihydra</b> (BB(6)), which iterate the same value "
    "map with mirrored halting conditions, and the FRACTRAN holdout family "
    "<b>Fenrir</b>, which turns out to be the same machine in base 5. All "
    "three are <i>walk-absorption</i> cryptids in the taxonomy of the meta "
    "report (&sect;6.1) &mdash; a different halting-condition type from "
    "machine 1, which is exactly why it was chosen: to see which "
    "tools survive the type change."))
story.append(P(
    "Results: the implementations are verified against every trajectory "
    "the bbchallenge wiki publishes, including two affine conjugacies "
    "(Section 2); the family provably cannot cycle (T1); a <b>q-adic "
    "branch-memory theorem</b> (T2) explains structurally why congruence "
    "invariants cannot decide these machines &mdash; the sharpest "
    "&ldquo;what makes them hard&rdquo; statement in this collection; the "
    "even-run acceleration is exact (T3); the golden-ratio absorption "
    "model is made rigorous about itself (T4); and the branch statistic "
    "matches Geom(1/2) to three decimals (P4). Deep runs reproduce and "
    "extend the wiki&rsquo;s checkpoints. The open cores remain open, as "
    "expected; what changed is that the reasons are now theorems."))

# ---------------- 2 ----------------
story.append(P("2. One family, three machines", H1))
story.append(P(
    "The value map is H(n) = floor(3n/2): H(2m) = 3m, "
    "H(2m+1) = 3m + 1. Each machine couples it to a counter that walks "
    "+2 on one parity and &minus;1 on the other, halting when the walk "
    "would go below zero:"))
story.append(Spacer(1, 4))
story.append(tab([
    ("Hydra", "BB(2,5)", "n<sub>0</sub> = 3", "+2 on odd, &minus;1 on even",
     "#even &gt; 2&middot;#odd", "undecided"),
    ("Antihydra", "BB(6)", "n<sub>0</sub> = 8", "+2 on even, &minus;1 on odd",
     "#odd &gt; 2&middot;#even", "undecided"),
    ("Fenrir", "FRACTRAN-22", "y<sub>0</sub> = 1",
     "+2 on odd, &minus;1 on even", "x = 0 at even y",
     "probv. non-halting"),
], ("machine", "domain", "start", "counter walk", "halts when", "status"),
   (0.85 * inch, 1.0 * inch, 0.8 * inch, 1.75 * inch, 1.35 * inch,
    0.95 * inch)))
story.append(Spacer(1, 4))
story.append(P(
    "Fenrir&rsquo;s value map is y &rarr; 5&middot;floor(y/2) + 2&middot;"
    "[y even]: the same divide-by-2, multiply-by-q skeleton with q = 5. "
    "Everything below is proved for q = 3 and, where stated, for q = 5 "
    "verbatim."))
story.append(P(
    "<b>Fidelity.</b> The implementations reproduce every published "
    "trajectory: Antihydra&rsquo;s A(0,4) &rarr; &hellip; &rarr; A(9,86) "
    "with the conjugacy b = n &minus; 4; Hydra&rsquo;s C(3,0) &rarr; "
    "&hellip; &rarr; C(78,6) with the conjugacy N = 3n &minus; 6 (2,000 "
    "steps verified against the TM-form map (3N+6)/2, (3N+3)/2); and "
    "Fenrir&rsquo;s S(0,1) &rarr; &hellip; &rarr; S(4,35). Both "
    "conjugacies appear to be unstated on the wiki; they pin the "
    "one-variable forms to the machine-level forms exactly."))

# ---------------- 3 ----------------
story.append(P("3. Theorems", H1))
story.append(P("3.1&nbsp;&nbsp;T1: the family cannot cycle", H2))
story.append(P(
    "H(n) &gt; n for every n &ge; 2, and Fenrir&rsquo;s map exceeds y for "
    "y &ge; 2 (the small values escape explicitly: 1 &rarr; 0 &rarr; 2 "
    "&rarr; 7). So all three machines halt or escape to infinity; "
    "periodic behavior is impossible. For machine 1 this trichotomy collapse required the potential theorems; here it is "
    "immediate &mdash; the value itself is the potential. The Skelet #1 "
    "scenario is excluded across the whole family."))

story.append(P("3.2&nbsp;&nbsp;T2: q-adic branch memory &mdash; why "
               "congruence invariants are blind", H2))
story.append(P(
    "<b>Theorem.</b> For the Hydra map, n<sub>t</sub> mod 3<super>k</super> "
    "is an explicit function of the last k parities (p<sub>t&minus;k</sub>, "
    "&hellip;, p<sub>t&minus;1</sub>) and of nothing older. <i>Proof.</i> "
    "n<sub>t</sub> = 3&middot;floor(n<sub>t&minus;1</sub>/2) + "
    "p<sub>t&minus;1</sub>, and halving is invertible mod 3<super>k</super>, "
    "so mod 3<super>k</super> the recursion is r &rarr; 3(r &minus; p)/2 + "
    "p: the factor 3 pushes the unknown older state up one 3-adic digit per "
    "step, annihilating it after k steps. The same holds mod "
    "5<super>k</super> for Fenrir. (30,000 randomized checks each, plus a "
    "direct check that the start residue does not influence the result.)"))
story.append(P(
    "<b>Why this matters.</b> It is the sharpest structural answer this "
    "collection has to &ldquo;what makes these machines undecidable in "
    "practice.&rdquo; The halting condition is a <i>cumulative count</i> of "
    "branches; the theorem says the value&rsquo;s residue to any fixed "
    "modulus built from q carries only a <i>bounded window</i> of branch "
    "history. So no congruence invariant of the value can track the walk: "
    "the q-adic side of n stores the recent past, the 2-adic side decides "
    "the future, and the halting condition lives in neither. On machine 1 the analogous fact was an empirical search result (no "
    "separating modulus &le; 256 / &le; 628); here, for the value alone, "
    "it is a theorem with a two-line proof. It also explains the "
    "community&rsquo;s experience that regular-language deciders fail on "
    "exactly these machines: a DFA over digits is a bounded-memory "
    "observer of a process whose halting depends on an unbounded count."))

story.append(P("3.3&nbsp;&nbsp;T3: exact acceleration", H2))
story.append(P(
    "H<super>s</super>(2<super>s</super>t) = 3<super>s</super>t, so a "
    "maximal run of even steps collapses to one jump with certificate s. "
    "An orbit is then a sequence of <b>blocks</b> &mdash; one odd step "
    "followed by v even steps, v the 2-adic valuation of the odd "
    "step&rsquo;s output &mdash; with per-block walk increment 2 &minus; v "
    "for Hydra&rsquo;s counter and 2v &minus; 1 for Antihydra&rsquo;s. "
    "This is the family&rsquo;s version of the cascade batching of machine 1, verified block-runner against single steps."))

story.append(P("3.4&nbsp;&nbsp;T4: the absorption model, exact", H2))
story.append(P(
    "For the model walk (+2 or &minus;1, probability 1/2 each) the "
    "probability of ever reaching &minus;1 from height h is "
    "q<super>h+1</super> where q is the root in (0,1) of q = "
    "(1 + q&sup3;)/2:"))
story.append(P("q&sup3; &minus; 2q + 1 = 0,&nbsp;&nbsp;&nbsp;&nbsp;"
               "q = (&radic;5 &minus; 1)/2 &#8776; 0.618034,", MATHC))
story.append(P(
    "the golden-ratio conjugate &mdash; the constant behind every "
    "probvious verdict on this family. Verified as the minimal solution "
    "of the hitting system by monotone iteration (agreement to "
    "10<super>&minus;6</super>, and q<super>h+1</super> matches the "
    "iterated values for h &le; 40). The statement is exact <i>about the "
    "model</i>; whether the parity stream justifies the model for the one "
    "orbit that matters is the single-orbit gap, as everywhere in this "
    "collection."))

# ---------------- 4 ----------------
story.append(P("4. Measurements", H1))
story.append(P(
    "<b>P4 (branch statistic).</b> Over 200,000 blocks of the pure map, "
    "the valuation distribution matches Geom(1/2) to three decimals "
    "(v = 0: 0.5000; 1: 0.2498; 2: 0.1259; 3: 0.0621; &hellip;), with "
    "E[v] = 0.998 against the model&rsquo;s 1. The family thus shares "
    "the collection&rsquo;s geometric branch law &mdash; the same law the "
    "Collatz heuristic assumes for the valuation of 3n + 1. P4 now holds "
    "in every machine of this collection."))
story.append(P(
    "<b>Deep runs.</b> Hydra ran 2,000,000 pure-map steps (counter b = 1,003,573, exactly the drift b &#8776; t/2 the wiki reports at 4M, no halt); Antihydra 2,000,000 (counter a = 996,805, minimum a = 2 &mdash; it never approached 0, hence never halted); Fenrir 1,500,000 (x = 751,413, no halt). Values reached 10<super>350,000</super>&ndash;10<super>600,000</super>. All reproduce the wiki&rsquo;s reported drifts."))

# ---------------- 5 ----------------
story.append(P("5. What transferred, what did not", H1))
story.append(tab([
    ("no-cycle proof (P6)", "transferred trivially",
     "the value is its own potential; T1"),
    ("exact acceleration (P1/P5 machinery)", "transferred",
     "T3 blocks = the cascade batching, with certificates"),
    ("branch statistic (P4)", "transferred",
     "Geom(1/2) to three decimals; now seen in all machines"),
    ("congruence analysis (P3)", "transferred and upgraded",
     "from a search result to a theorem: T2 proves no congruence "
     "invariant of the value can decide halting"),
    ("explicit halting set (P2)", "does not apply",
     "walk-absorption type: the halting event is cumulative, not "
     "positional &mdash; as the taxonomy predicted"),
    ("P8 accounting", "applies via T4",
     "per-opportunity probabilities q<super>h+1</super>; "
     "&Sigma;p convergent along the drifting walk"),
], ("tool", "outcome", "note"),
   (2.1 * inch, 1.6 * inch, 3.0 * inch)))
story.append(Spacer(1, 4))
story.append(P(
    "The taxonomy of the meta report made two predictions for this type: "
    "that P2&rsquo;s sparse-set machinery would not apply, and that the "
    "walk model would govern the risk accounting. Both held. The genuine "
    "surprise is T2: on the coincidence-type machines the impossibility "
    "of congruence separation was only ever an empirical search result, "
    "but on the absorption type it is a provable structural fact. Whether "
    "a T2-style theorem exists for machine 1 &mdash; some precise "
    "sense in which their orbit residues carry only bounded history "
    "&mdash; is now the sharpest question the transfer raises."))

# ---------------- 6 ----------------
story.append(P("6. Status and verification", H1))
story.append(tab([
    ("implementations vs wiki trajectories",
     "Antihydra A(0,4)..A(9,86); Hydra C(3,0)..C(78,6) + conjugacy over "
     "2,000 steps; Fenrir S(0,1)..S(4,35)", "pass"),
    ("T1", "value increase exhaustive to 100,000 + small-case escapes",
     "pass"),
    ("T2", "30,000 randomized checks each for q = 3 and q = 5; "
     "start-independence direct", "pass"),
    ("T3", "20,000 identity checks; block runner vs single steps", "pass"),
    ("T4", "minimal-solution iteration to 10^-6; algebraic root exact",
     "pass"),
    ("deep runs", "Hydra 2M / Antihydra 2M / Fenrir 1.5M steps, no halt; drifts match the wiki", "pass"),
], ("check", "scope", "result"),
   (2.0 * inch, 4.0 * inch, 0.7 * inch)))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=0.8, color=BLUE))
story.append(Spacer(1, 4))
story.append(P(
    "Artifacts: hydra.py (implementations + wiki fidelity), theorems.py "
    "(T1&ndash;T4 + measurements), make_hydra_report.py (this report). "
    "Sources: wiki.bbchallenge.org pages Hydra, Antihydra, Hydra function, "
    "Fenrir (accessed July 2026); the Coq-BB5 paper for Antihydra&rsquo;s "
    "statement. Status of all three machines: unchanged &mdash; open; "
    "this report adds proofs beneath the community&rsquo;s simulations, "
    "not a decision.",
    ParagraphStyle("Foot", parent=BODY, fontSize=9.5,
                   textColor=colors.HexColor("#555555"))))

doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                        topMargin=0.8 * inch, bottomMargin=0.8 * inch,
                        title="The Hydra Family Through the Toolkit")
doc.build(story)
print("wrote", OUT)
