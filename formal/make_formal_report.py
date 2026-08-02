"""Build the formal treatment: Collatz-equivalence and a hardness ordering."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.colors import HexColor

OUT = "/Users/tomzahavy/Documents/Claude/collatz/formal/collatz_equivalence_report.pdf"
styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=styles["Heading1"], spaceBefore=17, spaceAfter=7)
H2 = ParagraphStyle("H2x", parent=styles["Heading2"], spaceBefore=12, spaceAfter=5)
BODY = ParagraphStyle("Bodyx", parent=styles["Normal"], fontSize=10.5, leading=14.5, spaceAfter=7)
MATHC = ParagraphStyle("MathCx", parent=styles["Normal"], fontName="Times-Italic",
                       fontSize=10.5, leading=15, alignment=TA_CENTER, spaceBefore=4, spaceAfter=8)
CELL = ParagraphStyle("Cellx", parent=styles["Normal"], fontName="Times-Roman", fontSize=9.3, leading=12)
CELLI = ParagraphStyle("CellIx", parent=CELL, fontName="Times-Italic")
TITLE = ParagraphStyle("Titlex", parent=styles["Title"], fontSize=18, leading=23, spaceAfter=4)
SUB = ParagraphStyle("Subx", parent=styles["Normal"], alignment=TA_CENTER,
                     textColor=colors.HexColor("#555555"), fontSize=11, spaceAfter=16)
BLUE = HexColor("#1a3c6e")


def P(text, style=BODY):
    return Paragraph(text, style)


def tab(rows, header, widths, hdr=True):
    data = [[P(f"<b>{h}</b>", CELL) for h in header]] + [[P(c, CELL) for c in r] for r in rows]
    t = Table(data, colWidths=list(widths), repeatRows=1)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c4d6")),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
          ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f8fb")])]
    if hdr:
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef7")))
    t.setStyle(TableStyle(st))
    return t


story = []
story.append(P("Collatz-Equivalence and a Hardness Ordering for the Collection", TITLE))
story.append(P("A formal treatment: in what precise sense our machines are "
               "&ldquo;Collatz-like,&rdquo; whether they are equally hard, and "
               "an explicit ranking", SUB))

# 0
story.append(P("0. The question, made precise", H1))
story.append(P(
    "&ldquo;Is our machine equivalent to Collatz, and are the machines equally "
    "hard?&rdquo; splits into three formally distinct questions, which the "
    "informal &ldquo;cryptid = Collatz-like&rdquo; slogan runs together:"))
story.append(tab([
    ("(i) Same map?", "Is the machine (a conjugate of) the 3n + 1 map itself?"),
    ("(ii) Same class?", "Is it a member of the class Conway and "
     "Kurtz&ndash;Simon proved undecidable &mdash; the formal content of "
     "&ldquo;Collatz-like&rdquo;?"),
    ("(iii) Same hardness?", "Is deciding its halting as hard as the Collatz "
     "conjecture &mdash; in logical complexity, or in proof obstruction?"),
], ("", ""), (1.2 * inch, 5.5 * inch), hdr=False))
story.append(Spacer(1, 4))
story.append(P(
    "The short answers, developed below: <b>(i) No</b> &mdash; none of our "
    "machines is the Collatz map. <b>(ii) Yes</b> &mdash; all are generalized "
    "Collatz functions, and that is exactly what makes them Collatz-like. "
    "<b>(iii) Equal at the core, ranked on the shell</b> &mdash; their "
    "non-halting statements sit at the same logical level (one quantifier "
    "<i>below</i> the Collatz conjecture, not at it) and are blocked by the "
    "same pseudorandom-orbit obstruction, so on the deepest axis they tie; but "
    "a genuine partial order appears on secondary structure, and it is "
    "explicit (Section 4)."))

# 1
story.append(P("1. Same class: all are generalized Collatz functions", H1))
story.append(P(
    "<b>Definition</b> (Kurtz&ndash;Simon [2], after Conway [1]). A "
    "<i>Collatz function</i> is g with a modulus p and rationals "
    "a<sub>i</sub>, b<sub>i</sub> such that g(x) = a<sub>i</sub>x + "
    "b<sub>i</sub> whenever x &#8801; i (mod p), always integer-valued. "
    "Matthews&ndash;Watts [4] give the standard d-branch form "
    "T(x) = (m<sub>i</sub>x + r<sub>i</sub>)/d for x &#8801; i (mod d). Each "
    "is <b>piecewise-affine with the branch chosen by a residue modulo a "
    "fixed number</b> &mdash; finitely many affine pieces."))
story.append(P(
    "Every machine in the collection is of this form at the base level: each "
    "rule is affine in the state, and the rule is selected by residues (and, "
    "in machines 1 and 4, magnitude comparisons) of the current state. So all "
    "belong to the class whose halting problem Conway [1] proved undecidable, "
    "and whose totality set {g : &#8704;x &#8707;i g<super>(i)</super>(x) = 1} "
    "Kurtz&ndash;Simon [2] proved <b>&Pi;<super>0</super><sub>2</sub>-"
    "complete</b>. This membership <i>is</i> the formal meaning of "
    "&ldquo;Collatz-like&rdquo;; the bbchallenge notion of &ldquo;cryptid&rdquo; "
    "is admittedly informal [6], and the class above is the only precise "
    "formalization in the vicinity."))
story.append(P(
    "A subtlety our own analysis exposes. The <b>reduced</b> return maps "
    "(machine 1&rsquo;s F, the reset maps, the Space "
    "Needle&rsquo;s step) branch not on a fixed residue but on a q-adic "
    "<b>valuation</b> or a whole <b>digit word</b> &mdash; unboundedly many "
    "affine pieces. Valuation-branched maps are <i>not</i> in the strict "
    "finite-residue class [confirmed against 2, 4]; they are a broader family "
    "(Conway&rsquo;s functional / FRACTRAN model still contains them). So the "
    "acceleration is what <i>exposes</i> the machines&rsquo; true branch "
    "complexity: finite-residue at the base, valuation/digit at the section. "
    "The lone exception is the Hydra function H(n) = floor(3n/2), which "
    "branches only on parity &mdash; a <b>strict</b> Kurtz&ndash;Simon Collatz "
    "function; Hydra and Antihydra are its two boundary conditions."))
story.append(P(
    "<b>(i) None is the Collatz map.</b> The maps are pairwise distinct and "
    "none is affinely conjugate to n &rarr; n/2, 3n+1. Two internal "
    "coincidences are worth recording as genuine equivalences: "
    "<b>Hydra &#8801; Antihydra</b> (the same map H, differing only in start "
    "and in the direction of the count), and <b>machine 3 &#8776; Space "
    "Needle</b> (the same multiplicative structure, base 3 versus base 2 "
    "&mdash; machine 3 was built as the analogue). Machines 1 and 4 are "
    "distinct singletons."))

# 2
story.append(P("2. Same hardness? The arithmetical level is not the same", H1))
story.append(P(
    "The load-bearing clarification. Fix the start; write the halting question "
    "as a logical sentence:"))
story.append(tab([
    ("our machine halts from s<sub>0</sub>",
     "&#8707;k [halted by step k]", "&Sigma;<super>0</super><sub>1</sub>",
     "single orbit"),
    ("our machine never halts",
     "&#8704;k [not halted by step k]", "&Pi;<super>0</super><sub>1</sub>",
     "single orbit"),
    ("a single Collatz orbit reaches 1",
     "&#8707;i [g<super>i</super>(n)=1]", "&Sigma;<super>0</super><sub>1</sub>",
     "single orbit"),
    ("the Collatz <b>conjecture</b>",
     "&#8704;n &#8707;i [g<super>i</super>(n)=1]",
     "&Pi;<super>0</super><sub>2</sub>", "all orbits"),
], ("statement", "logical form", "level", "scope"),
   (2.35 * inch, 1.9 * inch, 1.15 * inch, 1.3 * inch)))
story.append(Spacer(1, 4))
story.append(P(
    "So each machine&rsquo;s non-halting is a <b>&Pi;<super>0</super>"
    "<sub>1</sub></b> statement &mdash; a single universal quantifier over "
    "one orbit &mdash; exactly as for the Busy Beaver cryptid Antihydra, whose "
    "non-halting is &#8704;n[#odd(n) &le; 2&middot;#even(n)] over one iteration "
    "of floor(3n/2) [6], and exactly the form Aaronson&ndash;Yedidia [5] "
    "use for a specific machine independent of ZFC. The Collatz "
    "<b>conjecture</b>, by contrast, is <b>&Pi;<super>0</super><sub>2</sub></b> "
    "(&#8704;n&#8707;i), and is <i>not</i> known to drop a level: that would "
    "require a proven computable bound on stopping times, and none exists "
    "(the &le; 41.68 log n bound is a heuristic prediction of stochastic "
    "models, not a theorem [3])."))
story.append(P(
    "<b>Consequence.</b> &ldquo;As hard as Collatz&rdquo; is <i>false</i> read "
    "as arithmetical complexity: our machines (and Antihydra) are one "
    "quantifier <i>simpler</i> than the conjecture. The honest same-level "
    "comparison is <b>single cryptid orbit &#8596; single Collatz orbit</b> "
    "(both &Sigma;<super>0</super><sub>1</sub>/&Pi;<super>0</super><sub>1</sub>). "
    "What &ldquo;as hard as Collatz&rdquo; correctly names is the shared "
    "<b>proof obstruction</b>, not the logical form."))

# 3
story.append(P("3. Why single-instance equivalence is vacuous &mdash; and "
               "where the real content is", H1))
story.append(P(
    "A single fixed instance (&ldquo;does Antihydra halt?&rdquo;, &ldquo;does "
    "Collatz hold?&rdquo;) has a definite truth value: it is one bit, hence "
    "<b>trivially decidable</b> by a constant algorithm. Many-one and Turing "
    "reductions are only defined between <i>parametrized families</i>, never "
    "between two fixed bits. This is precisely why every undecidability result "
    "is stated over the <i>class</i> of Collatz functions and never for 3n + 1 "
    "alone [1, 2], and why Conway&rsquo;s theorem &ldquo;does not directly "
    "imply&rdquo; anything about the Collatz conjecture itself [3]."))
story.append(P(
    "So the formal content of &ldquo;equivalent to Collatz&rdquo; is: (a) our "
    "machines are members of the same undecidable class (Section 1); (b) that "
    "class is &Pi;<super>0</super><sub>2</sub>-complete, so <i>as a "
    "family</i> it is exactly as hard as anything definable at that level [2]; "
    "but (c) any <i>individual</i> member &mdash; ours, Antihydra, or 3n + 1 "
    "&mdash; is a single sentence whose difficulty is not a reduction-degree "
    "but the <b>obstruction to proving it</b>. There is no established "
    "many-one ordering among specific Collatz-like instances; the literature "
    "offers none [6]. The ordering in Section 4 is therefore ours to propose, "
    "and we mark it as such."))

# 4
story.append(P("4. The shared obstruction, and the ranking", H1))
story.append(P(
    "<b>The obstruction is uniform.</b> A proof for any of these machines must "
    "resolve a <i>single</i> orbit of a mixing, pseudorandom process. This is "
    "Lagarias&rsquo;s diagnosis of Collatz verbatim: the pseudorandomness "
    "&ldquo;supports the conjecture and at the same time deprives us of any "
    "obvious mechanism to prove it, since mathematical arguments exploit the "
    "existence of structure, rather than its absence&rdquo; [3]. The 2-adic "
    "map is conjugate to the shift (maximum entropy, parities are coin flips), "
    "but the integers are a measure-zero subset, so ergodicity decides no "
    "single orbit [3]. Our explorations report makes this exact for the "
    "collection: the branch word is orbit-determined and grows without bound, "
    "and the process generating it is mixing with a positive spectral gap. "
    "The calibration is 5x + 1, where <i>not one</i> divergent orbit has been "
    "proven [3] &mdash; the same wall. <b>On this primary axis all our "
    "machines, Antihydra, and Collatz tie.</b>"))
story.append(P(
    "<b>A partial order does appear on secondary structure.</b> Since the "
    "core ties, we rank by how much is <i>provable</i> around it &mdash; how "
    "certainly each machine is beyond elementary methods, and how close it "
    "sits to a named open problem."))

story.append(P("4.1&nbsp;&nbsp;Axis A &mdash; certified vs candidate cryptid", H2))
story.append(P(
    "For the <b>multiplicative</b> machines (3 and the Space Needle) it is a "
    "<b>theorem</b> that no congruence can decide halting: the branch is the "
    "q-adic valuation, which is independent of x mod M for every M coprime to "
    "q, so no congruence closure even exists (explorations, Finding 3). They "
    "are <b>certified</b> irreducible to the elementary decider. For the "
    "<b>sparse-coincidence</b> machines (1 and 4) the same is only "
    "<b>empirical</b>: no separating modulus was found (m &le; 256 / 628), but "
    "none is proven impossible &mdash; an elementary decision is not ruled "
    "out. So:"))
story.append(P("certified (3, Space Needle) &nbsp;&gt;&nbsp; candidate "
               "(1, 4),", MATHC))
story.append(P(
    "where &gt; reads &ldquo;more certainly a genuine cryptid.&rdquo; This "
    "is not a claim that the core is harder for the multiplicative machines "
    "&mdash; it is that we have <i>proven</i> they resist the one elementary "
    "tool, whereas for the sparse machines that resistance is conjectural."))

story.append(P("4.2&nbsp;&nbsp;Axis B &mdash; distance to a named open problem", H2))
story.append(P(
    "Some machines&rsquo; halting is <i>analogous</i> to an established open "
    "problem, which imports difficulty of known provenance. <b>Hydra / "
    "Antihydra</b> and <b>machine 1&rsquo;s mantissa</b> live in the "
    "(3/2)<super>n</super>-equidistribution circle around <b>Mahler&rsquo;s "
    "Z-number problem</b> [7]: the bbchallenge wiki states the analogy "
    "explicitly (parity of floor(c&middot;(3/2)<super>n</super>)) &mdash; "
    "though as an <i>analogy</i>, not a proven equivalence, and the "
    "equidistribution itself is open [6, 7]. The <b>multiplicative</b> "
    "machines&rsquo; &ldquo;does the orbit hit an exact power?&rdquo; is "
    "perfect-powers-in-sequences territory (Baker; explorations Finding 6). "
    "Machine <b>4</b> is freestanding. So Axis B ranks "
    "Hydra/Antihydra and machine 1 closest to established hard number theory."))

story.append(P("4.3&nbsp;&nbsp;The ordering, assembled", H2))
story.append(tab([
    ("machine 1", "sparse / digit-word", "candidate", "Mahler (via mantissa)",
     "&mdash; (singleton)"),
    ("machine 3", "multiplicative / v<sub>3</sub>", "<b>certified</b>",
     "perfect powers", "&#8776; Space Needle"),
    ("machine 4", "sparse / magnitude", "candidate", "freestanding", "&mdash;"),
    ("Space Needle", "multiplicative / v<sub>2</sub>", "<b>certified</b>",
     "perfect powers", "&#8776; machine 3"),
    ("Hydra / Antihydra", "walk / parity (strict)", "n/a (count, not "
     "congruence)", "<b>Mahler</b> (analogy)", "Hydra &#8801; Antihydra"),
], ("machine", "type / branch", "Axis A", "Axis B", "equiv. class"),
   (1.15 * inch, 1.5 * inch, 1.05 * inch, 1.45 * inch, 1.35 * inch)))
story.append(Spacer(1, 4))
story.append(P(
    "<b>Reading the table.</b> There is no single total order &mdash; hardness "
    "here is genuinely multi-dimensional, and the primary (logical / "
    "obstruction) axis is flat. The defensible statements are: all six are "
    "generalized Collatz functions (Section 1); all are "
    "&Pi;<super>0</super><sub>1</sub> single-orbit, one level below the "
    "&Pi;<super>0</super><sub>2</sub> conjecture (Section 2); and among them "
    "the multiplicative pair {machine 3, Space Needle} is the only one "
    "<i>proven</i> beyond congruences, while the Hydra pair sits closest to a "
    "named open problem. That is the honest content of &ldquo;are they equally "
    "hard, or is there a ranking&rdquo;: <b>equal at the core, ordered on the "
    "shell.</b>"))

# 5
story.append(P("5. Answers, in one place", H1))
story.append(tab([
    ("Is any machine Collatz (the 3n+1 map)?", "No &mdash; distinct maps; two "
     "internal equivalence classes (Hydra&#8801;Antihydra; machine 3&#8776;Needle)."),
    ("Are they &ldquo;Collatz-like&rdquo; formally?", "Yes &mdash; all are "
     "generalized Collatz functions (Conway / Kurtz&ndash;Simon); Hydra is "
     "strict, the reduced maps are valuation/digit-branched (broader)."),
    ("Equally hard as the Collatz conjecture?", "Not in logical level: "
     "&Pi;<super>0</super><sub>1</sub> single-orbit vs the conjecture&rsquo;s "
     "&Pi;<super>0</super><sub>2</sub>. Equal only in the proof obstruction."),
    ("Equally hard as each other?", "At the core yes (uniform single-orbit "
     "pseudorandom wall); a partial order on secondary structure (Section 4)."),
    ("Is there a ranking?", "Yes, and explicit: certified (3, Needle) &gt; "
     "candidate (1, 4) on Axis A; Hydra/Antihydra, machine 1 nearest a "
     "named problem on Axis B. No literature precedent &mdash; ours to propose."),
], ("question", "answer"), (2.35 * inch, 4.3 * inch)))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=0.8, color=BLUE))
story.append(Spacer(1, 3))
refs = ("<b>References.</b> [1] Conway, Unpredictable iterations, 1972; "
        "FRACTRAN, 1987. [2] Kurtz &amp; Simon, The undecidability of the "
        "generalized Collatz problem, TAMC 2007 (Def. 1.2; Thm 1.5, "
        "&Pi;<super>0</super><sub>2</sub>-completeness). [3] Lagarias, The "
        "3x+1 problem: an overview, arXiv:2111.02635 (pseudorandomness; 2-adic "
        "conjugacy; 5x+1 not one orbit proven). [4] Matthews &amp; Watts, "
        "Acta Arith. 43 (1984). [5] Aaronson &amp; Yedidia, A relatively small "
        "Turing machine independent of set theory, arXiv:1605.04343 "
        "(&Pi;<sub>1</sub> non-halting). [6] bbchallenge wiki, Cryptids / "
        "Antihydra (informal cryptid notion; no ranking; Mahler analogy). "
        "[7] Mahler, An unsolved problem on the powers of 3/2, 1968; "
        "Flatto&ndash;Lagarias&ndash;Pollington 1995. Machine-side claims: "
        "collatz/formal/classify.py, ranking.py; explorations report "
        "(Findings 3, 6). Flags: the &Pi;<sub>1</sub>-vs-&Pi;<sub>2</sub> "
        "contrast and the ranking are our syntheses; the Antihydra&ndash;"
        "Mahler tie is an analogy, not a theorem.")
story.append(P(refs, ParagraphStyle("Ref", parent=BODY, fontSize=8.3, leading=10.8,
                                     textColor=colors.HexColor("#444444"))))

doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.85 * inch,
                        rightMargin=0.85 * inch, topMargin=0.8 * inch,
                        bottomMargin=0.7 * inch,
                        title="Collatz-Equivalence and a Hardness Ordering")
doc.build(story)
print("wrote", OUT)
