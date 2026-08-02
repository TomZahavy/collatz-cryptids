"""Build the meta report: Collatz-like machines and cryptids across the collection."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, BaseDocTemplate,
                                PageTemplate, Frame, PageBreak)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import (Drawing, Rect, String, Line, Polygon)
from reportlab.lib.colors import HexColor

OUT = "/Users/tomzahavy/Documents/Claude/collatz/meta/collatz_meta_report.pdf"

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=styles["Heading1"], spaceBefore=18, spaceAfter=8)
H2 = ParagraphStyle("H2x", parent=styles["Heading2"], spaceBefore=14, spaceAfter=6)
BODY = ParagraphStyle("Bodyx", parent=styles["Normal"], fontSize=10.5, leading=14.5,
                      spaceAfter=7)
MATH = ParagraphStyle("Mathx", parent=styles["Normal"], fontName="Times-Italic",
                      fontSize=10.5, leading=15)
MATHC = ParagraphStyle("MathCx", parent=MATH, alignment=TA_CENTER, spaceBefore=4,
                       spaceAfter=8)
CELL = ParagraphStyle("Cellx", parent=styles["Normal"], fontName="Times-Roman",
                      fontSize=9.5, leading=12.5)
TITLE = ParagraphStyle("Titlex", parent=styles["Title"], fontSize=19, leading=24,
                       spaceAfter=4)
SUB = ParagraphStyle("Subx", parent=styles["Normal"], alignment=TA_CENTER,
                     textColor=colors.HexColor("#555555"), fontSize=11, spaceAfter=18)
FIGCAP = ParagraphStyle("FigCapx", parent=styles["Normal"], fontSize=8.8, leading=12,
                        alignment=TA_CENTER, textColor=colors.HexColor("#444444"),
                        spaceBefore=3, spaceAfter=11)

BLUE = HexColor("#1a3c6e"); FILLB = HexColor("#e8eef7")
GREY = HexColor("#666666"); ACCENT = HexColor("#b23b3b"); GREEN = HexColor("#2e7d4f")


def P(text, style=BODY):
    return Paragraph(text, style)


def table_style():
    return TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8c4d6")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef7")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f6f8fb")])])


def tab(rows, header, widths):
    data = [[P(f"<b>{h}</b>", CELL) for h in header]]
    data += [[P(c, CELL) for c in r] for r in rows]
    t = Table(data, colWidths=list(widths), repeatRows=1)
    t.setStyle(table_style())
    return t


def pipeline_diagram():
    """The standard workflow, distilled from both machines."""
    stages = [
        ("1  Close halt routes with invariants",
         "mod-4 / mod-3 alternations kill most halt rules outright"),
        ("2  Find the section the orbit revisits",
         "anchors (a = 0, b = 1) or resets (a = 1) -- pin coordinates"),
        ("3  Accelerate exactly, with certificates",
         "batch unary loops and geometric cascades; verify step-exact"),
        ("4  Reduce to one integer map",
         "F(D) on the section / R(C) on resets -- the machine is one orbit"),
        ("5  Make the halting set explicit",
         "classify first (6.1): explicit family / walk boundary / mult. target"),
        ("6  Hunt congruence obstructions",
         "expect confinement (a provable pruning); do not expect separation"),
        ("7  Run deep; account risk honestly",
         "verified horizon != proof; state what is average-case"),
    ]
    W = 468; rh = 30; gap = 8
    Hh = len(stages) * rh + (len(stages) - 1) * gap + 8
    d = Drawing(W, Hh)
    y = Hh - rh
    for i, (label, note) in enumerate(stages):
        d.add(Rect(10, y, 218, rh - 4, rx=4, ry=4, fillColor=FILLB,
                   strokeColor=BLUE, strokeWidth=1))
        d.add(String(18, y + rh / 2 - 1, label, fontName="Helvetica-Bold",
                     fontSize=8, fillColor=BLUE, textAnchor="start"))
        d.add(String(240, y + rh / 2 - 1, note, fontName="Helvetica-Oblique",
                     fontSize=7.4, fillColor=GREY, textAnchor="start"))
        if i < len(stages) - 1:
            cx = 119
            d.add(Line(cx, y - 1, cx, y - gap + 2, strokeColor=BLUE, strokeWidth=1))
            d.add(Polygon([cx, y - gap, cx - 3, y - gap + 4, cx + 3, y - gap + 4],
                          fillColor=BLUE, strokeColor=BLUE))
        y -= rh + gap
    d.hAlign = "CENTER"
    return d


story = []

story.append(P("Collatz-Like Machines and Cryptids: Field Notes", TITLE))
story.append(P("A living research map &mdash; goals, results, and open "
               "questions across the collection (five machines), for humans "
               "and agents continuing the work", SUB))

# ---- table of contents (auto-populated from H1 headings) ----
TOCH = ParagraphStyle("TOCHx", parent=styles["Heading2"], fontSize=12,
                      spaceBefore=2, spaceAfter=6, textColor=HexColor("#1a3c6e"))
story.append(P("Contents", TOCH))
toc = TableOfContents()
toc.levelStyles = [ParagraphStyle("TOC1", parent=styles["Normal"], fontSize=10.5,
                                  leading=16, leftIndent=14, firstLineIndent=-14)]
story.append(toc)
story.append(PageBreak())

# ================= 1. purpose =================
story.append(P("1. How to use this document", H1))
story.append(P(
    "This is the shared, living layer above the machine-specific reports "
    "&mdash; the place for a new contributor, human or agent, to start. It is "
    "ordered to be read straight through, in five movements:"))
story.append(tab([
    ("Goals", "why the program exists and what it is trying to do "
     "(Section 2)."),
    ("Background", "the domain and the related literature a newcomer needs "
     "(Sections 3&ndash;4)."),
    ("Results", "the machines and what has been proved about them (Sections "
     "5&ndash;6); the patterns that generalize (Section 7); the cross-machine "
     "structure found by zooming out (Section 8); and the formal "
     "Collatz-equivalence and hardness ordering (Section 9)."),
    ("Methodology", "the workflow and traps for doing more, i.e. how to "
     "continue (Sections 10&ndash;11)."),
    ("Status", "the consolidated workstream board and the goal-by-goal "
     "score (Section 2.10) &mdash; <b>read this first if you want the "
     "current state</b> &mdash; then the standing open questions, which "
     "are the entry points for new work (Section 12)."),
], ("movement", "what it covers"), (1.5 * inch, 5.2 * inch)))
story.append(Spacer(1, 5))
story.append(P(
    "<b>To continue the program.</b> Read the status board (Section 2.10) and then Sections 2.11 to 2.16, which supersede its ranking, "
    "for where things stand and what is ranked next, then pick from it "
    "or from the standing open questions (Section 12). To <b>add a new "
    "machine</b>: run the workflow (Section 10) to reduce it and prove what "
    "you can, then (i) add a case file in Section 5 and a row to the "
    "side-by-side table (Section 6); (ii) test every pattern P1&ndash;P9 "
    "(Section 7) against it &mdash; promoting those that hold, demoting those "
    "that break; (iii) classify it in the halting-condition taxonomy "
    "(Section 7.1) and place it in the hardness ordering (Section 9); and "
    "(iv) record its open core in Section 12. To <b>explore a direction</b> "
    "across machines, the cross-machine section (Section 8) is the model: "
    "state the idea, try it on every machine, keep it honest about proved vs "
    "measured. Full proofs, verification logs and code live with each "
    "machine:"))
story.append(Spacer(1, 4))
story.append(tab([
    ("machine 1", "NextConfig(a, b, c, d), 13 rules",
     "machine1/collatz_acceleration_report.pdf"),
    ("machine 3", "A(a, b), 6 rules",
     "machine3/machine3_halting_report.pdf"),
    ("machine 4", "A(a, b), 10 rules",
     "machine4/machine4_halting_report.pdf"),
    ("Hydra family", "Hydra, Antihydra, Fenrir",
     "hydra/hydra_report.pdf"),
], ("id", "system", "full report (under collatz/)"),
   (0.9 * inch, 2.6 * inch, 3.2 * inch)))

# ================= 2. domain =================
story.append(P("2. Goals: the research program", H1))
story.append(P(
    "This section states what the program is for; the machines, the patterns "
    "it names (P1&ndash;P9), and the results it cites are developed in "
    "Sections 5&ndash;9, and a first-time reader may prefer to skim here and "
    "return. The aims, in the order they compound: establish <b>new "
    "observations</b> on Collatz-like functions (the halting-condition "
    "taxonomy and P8 are "
    "the first two); <b>decide halting</b> for specific machines where "
    "instance structure permits; sharpen the account of <b>what makes the "
    "hard ones hard</b> (the regular-invariant boundary of Section 4.4, "
    "made quantitative); and grow a toolkit that <b>transfers</b> between "
    "machines. That last aim is now the best-evidenced of the four. The "
    "affine-potential recipe has closed the cycle "
    "question on machines 1 and 3 alike; and the transfer runs "
    "both ways in time, too &mdash; machine 4 could not be closed by the "
    "existing recipe, so it produced a new one (the recovery potential, P6) "
    "that now returns to the kit for the next machine, and the Hydra "
    "family&rsquo;s q-adic theorem retroactively upgraded P3 for all. Every "
    "machine has been improved by another&rsquo;s tools, and two machines "
    "have improved the tools themselves. The three subsections that follow do "
    "different jobs and should be read in order: <b>2.1</b> is the ranked plan "
    "as commissioned, annotated with what each workstream returned; "
    "<b>2.2</b> is the execution log, one entry per piece of work, in the "
    "order it happened; and <b>2.3</b> assesses where that leaves the program "
    "against the four goals and revises what to do next. Where 2.1 and 2.3 "
    "disagree on priority, 2.3 is current."))

story.append(P("2.1&nbsp;&nbsp;The ranked plan (July 2026)", H2))
story.append(P(
    "The plan below replaces the earlier six-item next-steps list, whose "
    "first two items are done (the Hydra family and the Space Needle are "
    "Sections 5.5&ndash;5.6) and whose remaining four are absorbed into the "
    "workstreams as marked. It was produced from three independently "
    "commissioned literature surveys &mdash; the bbchallenge ecosystem, "
    "Collatz technique, and the decidability/termination literature "
    "(archived in <font face=\"Courier\">meta/surveys/</font>, with the full "
    "rationale in <font face=\"Courier\">meta/NEXT_STEPS.md</font>). The "
    "three surveys converged, from different literatures, on the same top "
    "idea: <b>automatic (base-q regular) sets are the one non-halting "
    "certificate class our no-congruence theorems do not exclude</b>, they "
    "are what decides bbchallenge holdouts in practice (FAR/WFAR), and "
    "nobody has ever pointed them at an arithmetic Collatz-like map. They "
    "converged again on the second: the halting-basin <b>density theorem</b> "
    "is the most provable-right-now new theorem available, because for an "
    "expanding map the Krasikov&ndash;Lagarias backward-tree count runs in "
    "the useful direction (upper bounds, not lower)."))
story.append(tab([
    ("WS1", "Automatic-invariant certificates &mdash; &ldquo;FAR for "
     "arithmetic maps&rdquo;",
     "<b>executed;<br/>both halves</b>",
     "Search for a q-automatic set I with start &isin; I, F(I) &sube; I, "
     "I &cap; Halt = &empty;: a complete, finite, machine-checkable "
     "non-halting proof. SAT over small DFAs (LSB-first), as FAR&rsquo;s "
     "mitm_dfa does over tape languages. Two-sided bet: a certificate decides "
     "a cryptid-grade map for the first time; bounded-size failure is itself a "
     "theorem (G3). <b>Outcome: the negative half landed</b> &mdash; no "
     "certificate at &le; 11 states for the Needle (13 in the 0-invariant "
     "convention) or &le; 7 for machine 3, by exhaustive enumeration to 7 "
     "states and SAT beyond (Section 2.2). <b>The MSB-first half has since "
     "been run too</b> &mdash; no certificate at &le; 13 states, on a size "
     "measure the LSB bounds do not constrain (Section 2.2), and the bounds "
     "are certified non-vacuous by a direct adequacy check (Section 2.5). "
     "What remains open is unbounded size, which no search can reach. "
     "Subsumes old item 3."),
    ("WS2", "The halting-density theorem",
     "<b>executed;<br/>bounded depth</b>",
     "Prove #{starts &le; x whose orbit halts} = O(x<super>c</super>) with "
     "explicit c &lt; 1 (target: polylog for the Needle). The Needle map "
     "<i>expands</i>, F(x) &ge; x + 3 &mdash; the plan first said &ldquo;is "
     "strictly increasing&rdquo;, which is false and is corrected in Section "
     "2.2 &mdash; so H is exactly backward-enumerable, and backward branching "
     "is subcritical: expected preimages per node = &Sigma;<sub>v&ge;0</sub> "
     "1/(2<super>v+1</super> + 3) = 0.5453 &lt; 1 (the v = 0 term is the 1/5 "
     "an earlier draft added on top, double-counting it), matching the "
     "observed one halting seed per octave (Finding 5). Template: "
     "Kontorovich&ndash;Lagarias&rsquo;s &eta;<sub>5</sub> &asymp; 0.65049 "
     "backward-tree exponent. <b>Outcome: proved depth-graded</b> &mdash; "
     "polylogarithmic counts, exact and complete for each fixed L, plus the "
     "completeness cutoff lemma; the unbounded-depth statement is Collatz-hard "
     "and stays open (Section 2.2)."),
    ("WS3", "Baker escalation: block-graded halting exclusions",
     "<b>executed;<br/>one rung</b>",
     "Grade halting branch words by block count B (ascent/valuation "
     "alternations) and exclude halting for all words with &le; B blocks via "
     "two- and three-log bounds (Rhin, Laurent&ndash;Mignotte&ndash;"
     "Nesterenko, Matveev) plus continued-fraction reduction and the "
     "verified prefix &mdash; the Steiner &rarr; Simons&ndash;de Weger "
     "&rarr; Hercher m-cycle architecture, aimed at halting instead of "
     "cycles. Our LTE bound is already the B = 1 case; April 2026 saw a "
     "BB(6) machine proved non-halting by Baker&ndash;W&uuml;stholz. The "
     "only technology that yields unconditional statements about the "
     "<i>actual</i> orbit. <b>Outcome: the congruence rung is unconditional "
     "but solitary</b> &mdash; 28.7% of Needle steps can never precede a halt, "
     "and the machine-independent form of the argument pins machine 3&rsquo;s "
     "last two steps to v<sub>3</sub> = 1 (95.06% of pairs); the ladder does "
     "not climb further, because the congruence constrains the last block "
     "alone and everything beyond it is Baker proper (Section 2.2)."),
    ("WS4", "The formal hardness frontier",
     "<b>next;<br/>content revised</b>",
     "Three write-ups: (a) the size frontier &mdash; smallest universal "
     "machine in our exact guarded-counter syntax (Ben-Amram&rsquo;s "
     "fixed-modulus theorem), placing our cryptids strictly below it; (b) "
     "the MSB/LSB fault line &mdash; interval-branched 1D reachability is "
     "open and decidable when injective, valuation-branched is "
     "&Sigma;<sub>1</sub><super>0</super>-complete, so our machines sit on "
     "the undecidable side by branching type rather than dimension; (c) "
     "certificate-impossibility meta-theorems (no-sieve; "
     "Presburger/semialgebraic/geometric inexpressiveness; unary-coded "
     "regular deciders collapse to congruence-plus-threshold). Subsumes old "
     "item 4, whose negative outcome it explains. <b>Revised, and promoted to "
     "first place:</b> (c) should now be built around this program&rsquo;s own "
     "three impossibility results and their <i>measured</i> resource-growth "
     "rates (pattern P9, Section 7) rather than assembled from the "
     "literature."),
    ("WS5", "Join the ecosystem",
     "<b>5a done;<br/>census next</b>",
     "Fenrir &mdash; the first FRACTRAN cryptid (March 2026) &mdash; is "
     "literally a 2-counter guarded affine machine: run the full pipeline on "
     "it as machine 7. Then the missing <b>census</b> of small guarded-affine "
     "machines (MBB covers only inc/dec Minsky machines and expects counter "
     "cryptids at size 8&ndash;10, unreached; BBf has 21,295 public BBf(23) "
     "holdouts), a Lean formalization of one flagship result, and "
     "contribution of our hardness ranking, which fills a gap the community "
     "states it has. Subsumes old items 2 and 6. <b>Fenrir is machine 7</b> "
     "(Section 2.2), and the census is now unblocked: the whole pipeline turned "
     "out to be branch-table-generic, so it can be run over an enumeration "
     "rather than by hand."),
    ("WS6", "The rigorous stochastic backbone",
     "<b>not started</b>",
     "Make the risk accounting a theorem about a proved model: "
     "Matthews&ndash;Watts Haar ergodicity of the q-adic extension (the "
     "hypotheses are checkable for our rules) formalizing P5; a certified "
     "spectral gap for the mantissa circle map via Lasota&ndash;Yorke plus "
     "interval arithmetic, upgrading Finding 2&rsquo;s numerics to theorems; "
     "and, as a stretch, Flatto&ndash;Lagarias&ndash;Pollington carry "
     "combinatorics &mdash; the one candidate for a non-Baker unconditional "
     "constraint on single orbits. Subsumes old item 5. <b>The specific "
     "target it briefly had is gone:</b> the backward-branching deficit "
     "against the interval ceiling was an artefact of the powers-of-2 roots, "
     "not a departure from randomness, and it is closed rather than open "
     "(Section 2.7)."),
], ("", "workstream", "status", "content"),
   (0.5 * inch, 1.25 * inch, 0.8 * inch, 4.15 * inch)))
story.append(P(
    "<b>Sequencing, as planned and as it went.</b> Phase 1, mutually "
    "independent: WS1 on the Needle (transducer plus SAT search), WS2 on the "
    "Needle (density theorem), and the Fenrir case file &mdash; <i>all three "
    "done</i>. Phase 2: extend WS1 and WS2 to machine 3 and the coincidence "
    "machines, plus the Baker ladder &mdash; <i>done, with the ladder "
    "saturating at one rung</i>; the WS4 write-ups slipped and are now the "
    "next item. Phase 3, as planned: census, Lean, community contribution, and "
    "the WS6 backbone. "
    "<b>Deliberately not pursued</b>, recorded so the effort is not spent "
    "twice: Tao/GGM almost-all transport (provably blocked by expansion, "
    "which needs q &lt; p<super>p/(p&minus;1)</super>, and unnecessary once "
    "WS2 reaches the same statement cheaply); Berg&ndash;Meinardus "
    "functional-equation reformulations (exact but difficulty-preserving); "
    "the affine sieve (its only fuel, congruence-quotient expansion, is "
    "provably absent here); Skolem-hardness reductions (our halting "
    "equations are dominant-root &mdash; the decidable case); and "
    "off-the-shelf non-termination provers, whose certificate classes are "
    "provably inexpressive for these machines. <b>This sequencing has since "
    "been revised:</b> Phases 1 and 2 are executed (Section 2.2), and Section "
    "2.3 reorders what remains in the light of what they produced."))

story.append(P("2.2&nbsp;&nbsp;Execution log", H2))
story.append(P(
    "<b>WS1, Space Needle (July 26, 2026) &mdash; the negative half of the "
    "two-sided bet landed.</b> The map&rsquo;s valuation branches are affine "
    "in the tail k = x &gt;&gt; (v+1): F(x) = x + 3k + v = "
    "(2<super>v+1</super> + 3)k + (2<super>v</super> + v), verified against "
    "needle.step1 below 300,000. That makes branch closure for a fixed "
    "automaton computable exactly by a (state &times; carry &times; state) "
    "product, and whether <i>any</i> acceptance labelling of a given "
    "transition structure works is then decided by Horn propagation. "
    "Searching every isomorphism class up to 7 states &mdash; 256,182,290 of "
    "them, a count that independently matches the known "
    "initially-connected-DFA totals &mdash; there is <b>no 2-automatic "
    "non-halting certificate for the orbit of 6 with at most 7 states</b>, "
    "and no nonempty 2-automatic F-invariant avoiding the powers of 2 at all "
    "with at most 6 states (the start-free strengthening). The obstruction is "
    "dynamical rather than a failure of small automata to see: at 3, 4 and 5 "
    "states, 4, 100 and 2,887 structures do separate the orbit from the "
    "halting set, and closure kills every one of them at the first step, each "
    "with a witness audited by direct simulation. The mechanism identifies "
    "what a certificate must really avoid &mdash; not H but the whole halting "
    "basin &cup;<sub>j</sub> F<super>&minus;j</super>(H) &mdash; and makes "
    "this the automatic generalisation of the collection&rsquo;s "
    "no-congruence theorems (a congruence class being the degenerate "
    "automatic set). Calibration: the same code finds a 2-state certificate "
    "for the control machine x &rarr; 4x. Full write-up: "
    "<font face=\"Courier\">automatic/ws1_report.pdf</font>. Open: "
    "certificates of unbounded size, and the MSB-first state count."))

story.append(P(
    "<b>WS2, Space Needle (July 26, 2026) &mdash; a density theorem, graded "
    "by depth.</b> First a correction: the plan justified this workstream by "
    "&ldquo;the map is strictly increasing&rdquo;, which is false (F(9) = 21 "
    "&gt; F(10) = 17; 990 inversions below 2000). The property the counting "
    "needs is expansion, x + 3 &le; F(x) &le; 3x, and that does hold. From it "
    "and the exact backward step &mdash; y = F(b) with v<sub>2</sub>(b) = v "
    "iff b = (2<super>v+1</super>y + 2<super>v</super>(3 &minus; 2v)) / "
    "(2<super>v+1</super>+3), so each valuation gives at most one preimage and "
    "d(y) &le; log<sub>2</sub>y + 1 &mdash; comes the bound "
    "#{b &le; x halting within L steps} &le; (L+1)(log<sub>2</sub>x + 1.585L "
    "+ 2)<super>L+1</super>: at bounded depth the halting starts are "
    "<i>polylogarithmic</i>, not merely sparse. Expansion also supplies the "
    "cutoff lemma the plan wanted: a seed b &le; x halting within L steps "
    "reaches a power of 2 below 3<super>L</super>x, so the depth-graded "
    "backward enumeration is complete rather than budget-limited &mdash; "
    "replacing the heuristic ceiling in explorations/backward.py. The exact "
    "counts (validated set-for-set against forward simulation below 60,000) "
    "run to x = 10<super>192</super> in a fraction of a second and grow like "
    "(log<sub>2</sub>x)<super>1.0</super>, about 1.7 seeds per octave &mdash; "
    "which is Finding 5&rsquo;s &ldquo;one per octave&rdquo; made exact. The "
    "average backward branching over an interval has a rigorous ceiling "
    "&Sigma;<sub>v</sub>1/(2<super>v+1</super>+3) = 0.5453, and the measured "
    "average is 0.5452 &mdash; an agreement which is <i>forced</i>, not "
    "evidence of anything; see Section 2.4. What is not proved is the "
    "unbounded-depth statement, "
    "and that gap is not a missing lemma: an unconditional "
    "O(x<super>c</super>) would assert that all but x<super>c</super> starts "
    "never halt &mdash; a single-orbit claim of Collatz strength. Write-up: "
    "<font face=\"Courier\">density/ws2_report.pdf</font>."))

story.append(P(
    "<b>WS5a, Fenrir (July 26, 2026) &mdash; machine 7, and the pipeline "
    "transferred without modification.</b> Fenrir (March 2026) is the first "
    "FRACTRAN cryptid and is literally a two-counter guarded affine machine: "
    "S(x,2y) &rarr; S(x&minus;1, 5y+2), S(x,2y+1) &rarr; S(x+2, 5y), start "
    "S(0,1), halt at S(0,even). Writing the second counter as n, it is the "
    "5/2-map n &rarr; floor(5n/2) &plusmn; 2 driving a walk that moves +2 on "
    "odd n and &minus;1 on even n &mdash; <b>Antihydra&rsquo;s architecture "
    "with 5/2 in place of 3/2</b>. Results, none of which the community page "
    "has: <i>T1</i>, no cycles (n strictly increases for n &ge; 2); "
    "<i>T2</i>, the counter is not independent &mdash; x<sub>k</sub> = "
    "3O<sub>k</sub> &minus; k with O<sub>k</sub> the number of odd "
    "n<sub>j</sub> so far, collapsing the machine to one stream plus a "
    "counting functional; and <i>T3</i>, the exact halting criterion "
    "<b>Fenrir halts iff its orbit reaches x = 1 with n &equiv; 0 (mod 4)</b> "
    "(proved, and checked against direct simulation on 13,500 starts, 1,426 "
    "of which halt). T3 turns the wiki&rsquo;s &ldquo;biased random "
    "walk&rdquo; into a checkable arithmetic condition and identifies the "
    "opportunity stream exactly: the visits to x = 1, each halting with "
    "probability 1/4. The walk descends a level with probability "
    "q = (&radic;5 &minus; 1)/2, the same golden-ratio constant P8 records "
    "for Antihydra &mdash; so &Sigma;p<sub>n</sub> converges and Fenrir joins "
    "the collection on the probviously-non-halting side. In 1,000,000 "
    "verified steps (n reaches 1,321,927 bits) the walk visits x = 1 "
    "<i>exactly once</i>, at step 2 in state (1,2), missing because 4 does "
    "not divide 2: one halting opportunity in the machine&rsquo;s entire "
    "history, with residual risk about "
    "10<super>&minus;104,633</super>. Write-up: "
    "<font face=\"Courier\">fenrir/fenrir_report.pdf</font>."))

story.append(P(
    "<b>Phase 2, machine 3 (July 26, 2026) &mdash; the machinery transfers, "
    "and the branching constant is the finding.</b> Machine 3&rsquo;s own T4 "
    "(b = 1 at every reset) collapses it to a one-variable reset map which, "
    "in base 3, is G(a) = (3<super>j+1</super>+1)m + (r&middot;3<super>j"
    "</super> + j + c<sub>r</sub>) on a = 3<super>j</super>(3m + r) &mdash; "
    "the exact analogue of the Needle&rsquo;s form, verified against machine "
    "3&rsquo;s accelerated step on 59,988 values. The property both machines "
    "share, and the one the whole apparatus needs, is being "
    "<b>branch-affine in base q</b>: writing x = q<super>|p|</super>m + "
    "val(p) for a digit prefix p, every branch is F(x) = A<sub>p</sub>m + "
    "B<sub>p</sub>. With only a branch table supplied, WS1 gives no "
    "3-automatic certificate for machine 3 at &le; 4 states (2,128,064 "
    "structures), and WS2 gives #{a &le; x halting within L} &le; "
    "(L+1)(2log<sub>3</sub>x + 2L + 2)<super>L+1</super> with complete exact "
    "counts. Each machine&rsquo;s average backward branching over an interval "
    "has a rigorous ceiling (the sum of 1/A over branches, each being one "
    "residue class), and both measurements sit on it &mdash; Needle 0.5452 "
    "against 0.5453, machine 3 0.8080 against 0.8081. This was read at the "
    "time as the divisibility conditions behaving in aggregate as independent "
    "events. <b>It is not: the agreement is forced, and Section 2.4 proves "
    "it.</b> The quantity that is not forced &mdash; branching along the "
    "backward tree &mdash; sits well below the ceiling on both machines. "
    "Write-up: "
    "<font face=\"Courier\">meta/transfer_report.pdf</font>."))
story.append(P(
    "<b>WS3, Space Needle (July 26, 2026) &mdash; forbidden valuations, and a "
    "ladder that saturates at its first rung.</b> On the branch "
    "v<sub>2</sub>(x) = v the map is affine with fixed point "
    "x* = 2<super>v</super>(3&minus;2v)/3, so a halt at the end of a run of "
    "valuation v forces q<sub>v</sub><super>n</super> | 3&middot;2<super>m"
    "&minus;v</super> &minus; 3 + 2v with q<sub>v</sub> = 2<super>v+1</super> "
    "+ 3. For v = 0 that is the known LTE case; the new observation is that "
    "for many v the congruence is <b>unsolvable</b>, because "
    "3<super>&minus;1</super>(3 &minus; 2v) need not lie in the subgroup "
    "generated by 2 mod q<sub>v</sub>. <b>Theorem: a halt can never follow a "
    "step of valuation v = 1, 4, 7, 9, 10, 12, 13, 18, 19, 21, 22, 23, 24, "
    "25, 26, 28, 31, 32 or 33</b> &mdash; at any scale, at any time; 19 of "
    "the first 35 valuations. Since valuation v has frequency 2<super>&minus;"
    "(v+1)</super>, that is an asymptotic 28.7% of all steps removed as "
    "possible halt-predecessors, and on the actual orbit 28.91% of the first "
    "200,000 steps are unconditionally excluded. Brute force independently "
    "confirms it: single-step halting seeds below 3,000,000 occur only at "
    "valuations {0, 2, 3, 6}. The accompanying position bound &mdash; "
    "m &ge; t<sub>min</sub>(v,n) + v against m &le; 1.585N + 2.6 &mdash; is "
    "nearly vacuous, excluding 8 further steps in 200,000, because "
    "t<sub>min</sub> grows like q<sub>v</sub><super>n&minus;1</super> while m "
    "grows only linearly in the step index. The congruence method has exactly "
    "one rung, because (*) constrains m through the last block alone; blocks "
    "beyond it enter only as a small linear form in logarithms, which is "
    "Baker proper and a separate undertaking. Write-up: "
    "<font face=\"Courier\">baker/ws3_report.pdf</font>."))
story.append(P(
    "<b>WS3 transfer sweep (July 26, 2026) &mdash; the sieve is "
    "machine-independent, and it is far sharper in base 3.</b> Stripped to its "
    "skeleton the WS3 argument needs only branch-affineness: with "
    "&alpha;<sub>b</sub> = N<sub>b</sub>/D<sub>b</sub> in lowest terms and "
    "fixed point P<sub>b</sub>/Q<sub>b</sub>, one step forces N<sub>b</sub> | "
    "Q<sub>b</sub>x<sub>1</sub> &minus; P<sub>b</sub>, so a halt out of branch "
    "b requires some h in H with Q<sub>b</sub>h &equiv; P<sub>b</sub> (mod "
    "N<sub>b</sub>). Run across the collection this gives a clean law: <b>the "
    "sieve&rsquo;s strength is governed by how thin H is as a set of "
    "values</b>. Fenrir and the Hydra family are immune (their halting "
    "conditions are a congruence class and a first passage, neither a thin set "
    "of values); and <b>machine 3 is pinned hard</b>. "
    "There N = 3<super>j+1</super>+1 makes 3<super>j+1</super> &equiv; "
    "&minus;1, so the powers of 3 collapse to just 2(j+1) residues with large "
    "gaps between them, and the fixed point lands strictly inside a gap for "
    "every j &ge; 2 while j = 0 fails on parity. <b>Theorem: machine 3 can "
    "halt only out of a step with v<sub>3</sub>(a) = 1</b> &mdash; a single "
    "allowed valuation rather than the Needle&rsquo;s scattered tail, "
    "excluding 7/9 = 77.78% of all steps. Because H is geometric the sieve "
    "also runs backwards: the depth-1 seeds are two explicit families, and "
    "sieving those pins the next-to-last branch to v<sub>3</sub> = 1 as well "
    "(a parity lemma kills every even j in closed form; the odd j are "
    "machine-verified to j &le; 500), so the last two steps before any halt "
    "both have valuation 1 &mdash; 95.06% of consecutive step pairs excluded, "
    "measured 95.07%. The pinning has depth exactly 2: three steps back "
    "v<sub>3</sub> may be 0 or 1, and the backward family count grows 2, 4, 6, "
    "17, 80, so the tree does not die and no decision follows. Write-up: "
    "<font face=\"Courier\">baker/sweep_report.pdf</font>."))
story.append(P(
    "<b>WS1 past the enumeration wall (July 27, 2026) &mdash; the search "
    "becomes a SAT instance.</b> Exhaustive enumeration of transition "
    "structures ends near 7 states because the ICDFA count grows faster than "
    "any pruning; the fix is to make the transition structure itself the "
    "unknown. Encoding T[s][c][t] and the acceptance bits as variables, with a "
    "reachability variable per product state, reproduces bbchallenge&rsquo;s "
    "FAR mitm_dfa for arithmetic maps. Two design points matter. First, only "
    "the <i>forward</i> closure of product reachability is encoded: that forces "
    "R to contain the reachable set while still permitting R = reach, so a real "
    "certificate always yields a satisfying assignment and UNSAT stays a sound "
    "impossibility proof &mdash; an over-approximating R would impose the pair "
    "implication on unreachable states and could report UNSAT spuriously. "
    "Second, BFS-canonical symmetry breaking (the ICDFA canonical form, as "
    "clauses) removes the n! relabellings, and took n = 7 from 47.8 s to 0.1 s. "
    "The reach, all UNSAT: <b>the Space Needle has no 2-automatic non-halting "
    "certificate at &le; 11 states</b> in the minimal-word convention and "
    "&le; 13 in the trailing-zero-invariant one, and <b>machine 3 none in base "
    "3 at &le; 7 states</b> &mdash; against 7 and 4 by enumeration, with "
    "machine 3&rsquo;s n = 5 taking 18 s where enumeration needed an estimated "
    "hour. The two conventions are different size <i>measures</i>, not "
    "different classes of set, so neither bound subsumes the other. Method "
    "note, and the reason to trust these numbers at all: the encoding is "
    "cross-validated rather than trusted &mdash; it is compared against the "
    "exhaustive search at every machine, size and branch depth where both can "
    "run (30 of 30 agreements in base 2, 12 of 12 in base 3) and every "
    "certificate it produces is re-verified by direct simulation. That caught "
    "two encoding bugs which would each have produced a fake headline: on a "
    "nonzero digit the product must branch into both &ldquo;the tail ends "
    "here&rdquo; and &ldquo;the tail continues&rdquo;, and taking only the "
    "first gave a spurious <i>certificate</i>; and an over-strong symmetry "
    "break forced &delta;(0,0) = 0, giving spurious <i>UNSAT</i>. Cost still "
    "grows by a factor of 5.5 to 10.2 per state (Section 2.3), so this moves "
    "the wall by a few states rather than removing it. Files: "
    "<font face=\"Courier\">automatic/sat_search.py</font>, "
    "<font face=\"Courier\">sat_generalq.py</font>, "
    "<font face=\"Courier\">sat_validate.py</font>."))

story.append(P(
    "<b>Phase 3 opening (July 27, 2026, afternoon) &mdash; the MSB-first "
    "search, and the wall re-measured from two new directions.</b> Three items "
    "were executed against the revised ranking. <i>First, MSB-first automatic "
    "invariants</i>, which the plan had ranked second but described as blocked "
    "because the branch relation is not MSB-synchronous. <b>That premise was "
    "false, and for every machine in the family.</b> Eliminating m from "
    "x = q<super>|p|</super>m + val(p) and F(x) = A<sub>p</sub>m + "
    "B<sub>p</sub> leaves a single linear relation with constant right-hand "
    "side, q<super>|p|</super>F(x) &minus; A<sub>p</sub>x = "
    "q<super>|p|</super>B<sub>p</sub> &minus; A<sub>p</sub>val(p) =: "
    "C<sub>p</sub>; reading x and F(x) in parallel MSB-first, the running "
    "remainder is bounded by |C<sub>p</sub>| + q<super>|p|</super> + "
    "A<sub>p</sub>, since anything outside that box doubles away and can never "
    "return to C<sub>p</sub>. So the relation is letter-to-letter with finitely "
    "many states &mdash; no lookahead, no delay (verified on both machines, "
    "299,987 and 299,980 values, no violations). The product is O(n<super>2"
    "</super>) against the LSB encoding&rsquo;s O(n<super>3</super>), worth 42 "
    "times per instance at equal size (n = 10 costs 24.6 s against "
    "1041 s), and the result is <b>no MSB-first certificate for the Needle at "
    "&le; 13 states</b>. Since every earlier bound was on LSB state count and "
    "an MSB automaton can be exponentially smaller, this closes a gap the "
    "report had listed as wide open &mdash; though it moves the wall rather "
    "than removing it: MSB pays 10.18&times; per state at n = 11 to 12, and "
    "the LSB search, which has since completed n = 11, paid 15.89&times; at "
    "the same point in its own series (Section 2.6). Both figures come from "
    "concurrent runs; re-measured one process at a time the MSB series is "
    "monotone rising (Section 2.8). "
    "<i>Second, the impossibility results were checked for vacuity.</i> A "
    "completed UNSAT cannot be undermined by a slow solver, but an "
    "over-constrained encoding would make every such theorem empty, and the "
    "only calibration on record was a machine whose certificate has two "
    "states. Planted machines G<sub>m</sub> keeping the Needle&rsquo;s own "
    "multipliers and moving only the additive constant have "
    "{x : m | x} invariant for prime m, so a certificate exists at exactly m "
    "states; checking the induced assignment against the formula directly "
    "&mdash; by construction, no solver &mdash; shows both encodings admit "
    "certificates at k = 3, 5, 7, 11, 13, 17, 19 and 23, covering every size "
    "at which this program claims an impossibility. <i>Third, a prediction "
    "that failed.</i> Handing the solver the halting basin, which Section 2.2 "
    "identified as the real obstruction and WS2 enumerates exactly, was "
    "expected to move the wall several states; the clauses are implied, so the "
    "theorem is unchanged, and the measured effect is a reproducible 25 to 30% "
    "&mdash; about one eighth of a state. Adding halt values that carry no new "
    "information is actively worse. The wall is not made of missing "
    "information; it is made of search space. Write-up: "
    "<font face=\"Courier\">automatic/RESULTS.md</font>."))

story.append(P("2.3&nbsp;&nbsp;Stock-take: what Phases 1 and 2 established", H2))
story.append(P(
    "With WS1, WS2, WS3 and the two transfer sweeps executed, the plan&rsquo;s "
    "first two phases are complete enough to assess, and the assessment is "
    "more informative than any single result. <b>Every workstream produced a "
    "theorem, and every one of them stopped at a wall of the same shape.</b> "
    "WS1 decides certificate existence exactly up to a bound on automaton "
    "size, and is silent above it. WS2 counts halting starts exactly and "
    "completely up to a bound on backward depth, and is silent beyond it. WS3 "
    "excludes halting unconditionally out of a bounded number of steps &mdash; "
    "one for the Needle, two for machine 3 &mdash; and is silent past that. "
    "Three methods, three different resources, one pattern: <b>exact within "
    "the bound, provably silent beyond it</b>. This is not three coincidences "
    "but one phenomenon, and it can be quantified, which is what makes it a "
    "contribution to G3 rather than an apology. The cost of one more unit of "
    "resource is measured in each case: a factor of 5.5 to 10.2 in solver time "
    "per automaton state (geometric mean 7.1 over n = 6 to 10 on the Needle, "
    "and <i>rising</i> &mdash; the last step, n = 9 to 10, cost 10.2), a factor "
    "of (log x) per unit of backward depth, and q<sub>b</sub><super>n&minus;1"
    "</super> per congruence rung &mdash; the last being why the sieve&rsquo;s "
    "ladder saturates at its first rung instead of climbing. That the SAT "
    "factor is itself growing matters: it means the wall is not merely far "
    "away but accelerating away, and no constant-factor engineering reaches "
    "the sizes at which the question would become interesting."))
story.append(Spacer(1, 4))
story.append(tab([
    ("WS1 &mdash; automatic certificates", "DFA states (LSB-first)",
     "Needle 11 states (minimal-word), 13 (0-invariant), 13 (MSB-first); "
     "machine 3, 7 states in base 3 &mdash; all UNSAT",
     "&times;3.4 to &times;53.2 solver time per state, and the factor is "
     "rising in every series (Section 2.6)"),
    ("WS2 &mdash; halting density", "backward depth L",
     "exact, complete counts for every fixed L; polylogarithmic in x, run to "
     "x = 10<super>192</super>",
     "&times;(log x) on the bound per unit of depth"),
    ("WS3 &mdash; congruence sieve", "composed steps (rungs)",
     "1 rung on the Needle (28.7% of steps excluded); 2 on machine 3 (95.06% "
     "of consecutive pairs)",
     "q<sub>b</sub><super>n&minus;1</super> on the position bound per rung "
     "&mdash; saturates at once"),
], ("method", "bounding resource", "reach attained", "cost of one more unit"),
   (1.5 * inch, 1.15 * inch, 2.25 * inch, 1.85 * inch)))
story.append(P(
    "<b>Table.</b> The same wall in three resources. Read across: each method "
    "is exact everywhere inside its bound, and the rightmost column &mdash; "
    "not the reach &mdash; is what says whether pushing further is worth "
    "anything.", FIGCAP))
story.append(P(
    "Read against the four goals, the picture is uneven in a way worth stating "
    "plainly. <b>G1 is where the yield is</b>: the depth-graded density "
    "theorem with its completeness cutoff lemma, the forbidden-valuation "
    "theorem, machine 3&rsquo;s pinning to a single valuation for the last two "
    "steps before any halt, Fenrir&rsquo;s exact halting criterion, and the "
    "thin-H law are all new statements that did not exist before this program. "
    "<b>G2 did not move.</b> WS3 produced the collection&rsquo;s first "
    "unconditional statements about the <i>actual</i> orbit at infinite time, "
    "which is a real advance in kind, but it caps at 28.7% of steps for the "
    "Needle and 95.1% of consecutive pairs for machine 3, and the backward "
    "family count grows (2, 4, 6, 17, 80) rather than dying &mdash; so no "
    "cryptid has been decided, and none of the three methods can compose into "
    "a decision. <b>G3 is the surprise.</b> The negative results have stopped "
    "being a list and become an account: a certificate must avoid the whole "
    "halting basin rather than the halting set (WS1&rsquo;s mechanism), the "
    "sieve&rsquo;s strength is governed by how thin H is as a set of values "
    "(the sweep&rsquo;s law), and each certificate family fails by exhausting "
    "a measurable resource rather than by bad luck. <b>G4 is settled.</b> The "
    "branch-affine form F(x) = A<sub>p</sub>m + B<sub>p</sub> on "
    "x = q<super>|p|</super>m + val(p) is now the interface: supply a branch "
    "table and the sieve, the SAT search and the density counting all run "
    "unmodified, which is how machine 3 was analysed at all."))
story.append(P(
    "One cross-cutting measurement was separated out here as the quantitative "
    "form of the pseudorandomness heuristic, on the strength of its recurring "
    "independently in two workstreams: each machine&rsquo;s average backward "
    "branching has a rigorous ceiling &mdash; the sum of 1/A over branches, "
    "each branch contributing one residue class &mdash; and both machines sat "
    "<i>on</i> it, the Needle measuring 0.5452 against a ceiling of 0.5453 and "
    "machine 3 measuring 0.8080 against 0.8081. <b>That reading was wrong, and "
    "Section 2.4 replaces it.</b> The agreement is forced by a three-line "
    "argument, so it is evidence of nothing; the quantity that is not forced "
    "&mdash; branching along the backward tree &mdash; turns out to sit some "
    "20% <i>below</i> the ceiling on both machines, which is a real "
    "observation and points the other way."))
story.append(P(
    "<b>What follows from this, for the next phase.</b> Pushing any of the "
    "three methods harder now buys constants rather than structure: another "
    "SAT state is a day of compute and then a week, another backward depth "
    "multiplies the bound by a logarithm, another congruence rung does not "
    "exist. The reorientation the stock-take suggests has three items, in "
    "order. <b>First, WS4, whose content has changed.</b> It was planned as an "
    "assembly of known results; it should now be written around our own three "
    "impossibility theorems with their measured resource growth, because "
    "&ldquo;here are three certificate families, each exact within its bound "
    "(the phenomenon is catalogued as pattern P9 in Section 7), "
    "each silent beyond it, with the growth constant of the bound in each "
    "case&rdquo; is a sharper account of decider-resistance than anything in "
    "the literature and is the natural G3 deliverable. <b>Second, the one "
    "genuinely unexplored direction with a two-sided payoff: MSB-first "
    "automatic invariants.</b> Every WS1 bound above is on LSB-first state "
    "count, and an MSB automaton for the same set can be exponentially "
    "smaller, so &ldquo;no certificate at &le; 11 LSB states&rdquo; says "
    "almost nothing about small MSB certificates &mdash; this is the only "
    "place a <i>positive</i> WS1 result could still be hiding. The work is a "
    "new encoding, since the branch relation is not MSB-synchronous; "
    "everything else is reused. <b>Third, WS5&rsquo;s census.</b> It is now "
    "unblocked in a way it was not when the plan was written: the entire "
    "pipeline is branch-table-generic, as the sweep and the base-q SAT search "
    "demonstrated, so it can be run automatically over an enumeration of small "
    "guarded-affine machines. It is also the only item on the list that "
    "changes the <i>supply</i> of results rather than pushing one machine "
    "further, which is the right move when three methods have just hit their "
    "ceilings on the same two machines. WS6 follows these, and it now has a "
    "specific target it did not have before: Matthews&ndash;Watts Haar "
    "ergodicity is the natural home for the tree-branching deficit of "
    "Section 2.4, which replaced the coincidence this section originally "
    "reported."))

story.append(P("2.4&nbsp;&nbsp;Correction: the branching ceiling is forced, and "
               "the tree is thinner than it", H2))
story.append(P(
    "The measurement recorded above &mdash; average backward branching sitting "
    "on its rigorous ceiling on both machines &mdash; was presented as the "
    "quantitative form of the pseudorandomness heuristic, and WS6 was pointed "
    "at explaining it. It explains nothing, because the agreement cannot fail. "
    "<b>Lemma (proved).</b> For the Needle, a preimage of y under branch v "
    "satisfies b&middot;A<sub>v</sub> = 2<super>v+1</super>y + "
    "2<super>v</super>(3 &minus; 2v) with A<sub>v</sub> = 2<super>v+1</super> "
    "+ 3 &#8801; 3 (mod 2<super>v+1</super>), so 3b &#8801; 2<super>v</super>"
    "(3 &minus; 2v) (mod 2<super>v+1</super>). The factor 3 &minus; 2v is odd, "
    "so the right-hand side has 2-adic valuation exactly v, and 3 is "
    "invertible; hence v<sub>2</sub>(b) = v <i>always</i>. The side condition "
    "that could have cost density is free, so the density of y admitting a "
    "branch-v preimage is exactly 1/A<sub>v</sub>, and summing over v gives "
    "the ceiling by equidistribution modulo A<sub>v</sub> over an interval. "
    "That is arithmetic, not pseudorandomness. (Machine-verified: zero "
    "violations of v<sub>2</sub>(b) = v over v &le; 20 with 5,000 preimages "
    "each; per-branch interval densities match 1/A<sub>v</sub> to five "
    "decimals. Machine 3 behaves identically &mdash; its side conditions "
    "survive 79,990 of 79,990 congruence hits over j &le; 9.) The tell was "
    "always in the code: the measurement in "
    "<font face=\"Courier\">density/density.py</font> sums over the interval "
    "y &#8712; [3, 200000), and its own docstring states that the branch-v "
    "preimage exists only for y in one residue class. It was measuring its "
    "own hypothesis."))
story.append(P(
    "The quantity that is <i>not</i> forced is branching along the backward "
    "tree, where y ranges over the nodes of the tree of H &mdash; a sparse, "
    "self-similar set with no reason to equidistribute modulo A<sub>v</sub>. "
    "That is also the only version of the quantity a density theorem could "
    "use. Measuring it is exact rather than statistical: F expands, so every "
    "preimage is strictly smaller than its image and the tree below any cap is "
    "finite and complete, and each node has exactly one parent, so no "
    "deduplication is involved. Pooled over the whole tree (equivalently, "
    "1 &minus; seeds/nodes, the total-progeny estimator for a subcritical "
    "process):"))
story.append(tab([
    ["Needle (base 2)", "0.5453", "0.4503<br/>(199 / 362)",
     "0.4309<br/>(799 / 1,404)", "0.4332<br/>(3,196 / 5,639)",
     "&minus;20.6%"],
    ["machine 3 (base 3)", "0.8081", "0.5976<br/>(66 / 164)",
     "0.5682<br/>(133 / 308)", "0.5632<br/>(266 / 609)", "&minus;30.3%"],
], ("machine", "interval<br/>ceiling", "tree, small cap<br/>(seeds / nodes)",
    "tree, medium cap", "tree, largest cap", "deficit"),
   (1.15 * inch, 0.85 * inch, 1.25 * inch, 1.2 * inch, 1.3 * inch,
    0.75 * inch)))
story.append(P(
    "Caps are 10<super>60</super>, 10<super>240</super>, 10<super>960</super> "
    "for the Needle and 3<super>200</super>, 3<super>400</super>, "
    "3<super>800</super> for machine 3. Both figures settle rather than drift "
    "&mdash; the Needle at about 0.433, machine 3 at about 0.563 &mdash; so "
    "the deficit is a limit and not a small-sample artefact.", FIGCAP))
story.append(P(
    "So the tree carries about 21% less branching than the independence model "
    "predicts on the Needle, and about 30% less on machine 3 &mdash; in "
    "the direction that <i>helps</i> an upper bound on halting density, since "
    "a thinner tree means fewer halting seeds. That was written as the honest "
    "replacement for the discarded coincidence: not evidence that the machines "
    "behave randomly, but a measured, unexplained departure from randomness in "
    "the one place where the departure would matter, and the target WS6 "
    "deserved. <b>It did not survive either.</b> The deficit is as forced as "
    "the agreement it replaced, and for a closely related reason: the interval "
    "ceiling is a statement about uniform y, while the tree contains no "
    "uniform y at any depth. Section 2.7 carries the resolution and the "
    "control experiment that settles it; the numbers in the table above stand, "
    "and only their interpretation changes."))

story.append(P("2.5&nbsp;&nbsp;Stock-take: the Phase 3 opening, and the "
               "exchange rate", H2))
story.append(P(
    "The three items executed on July 27 (Section 2.2) were meant to test "
    "three different things, and between them they changed what the whole of "
    "WS1 is worth. Taken in order of how much they moved: "
    "<b>the impossibility results were certified non-vacuous.</b> Every one of "
    "them is a completed UNSAT, which no amount of solver slowness can "
    "undermine &mdash; but an encoding that was accidentally over-constrained "
    "would report UNSAT for machines that <i>do</i> have certificates, and "
    "every theorem built on it would be empty. That risk had never been "
    "tested: the only calibration on record was a control machine whose "
    "certificate has two states, which shows the search is not blind and "
    "nothing more. Both encodings are now shown, by direct construction of the "
    "satisfying assignment rather than by search, to admit certificates at 3, "
    "5, 7, 11, 13, 17, 19 and 23 states &mdash; covering every size at which "
    "this program claims an impossibility. That is retrospective insurance on "
    "all of WS1, and it is what lets WS4 quote the bounds."))
story.append(P(
    "<b>The MSB-first gap closed, and it was never the gap it looked like.</b> "
    "The plan had ranked MSB second and called it blocked, because the branch "
    "relation is not MSB-synchronous. It is synchronous &mdash; for every "
    "machine in the family, by an elimination that takes one line (Section "
    "2.2) &mdash; and the resulting encoding is O(n<super>2</super>) where the "
    "LSB one is O(n<super>3</super>). So the item ranked second as the "
    "program&rsquo;s best remaining two-sided bet turned out to be cheap, and "
    "it produced the same answer as everything else: no certificate, now on a "
    "size measure the earlier bounds did not constrain. The honest reading is "
    "that the report had been describing an obstacle it had not examined."))
story.append(P(
    "<b>And a prediction failed, which is where the round&rsquo;s one real "
    "advance came from.</b> Feeding the solver the halting basin &mdash; the "
    "obstruction WS1 itself identified, enumerated exactly by WS2 &mdash; was "
    "predicted here to move the wall several states. It moved it by an eighth "
    "of a state. Setting that beside the MSB result, which won a factor of 42, "
    "gives the exchange rate that Section 7 now "
    "records as the sharpened form of P9: with cost per state growing "
    "geometrically at rate g, a constant-factor improvement C buys "
    "log<sub>g</sub>(C) states. Both outcomes are what that formula predicts, "
    "and it was fitted to neither. It converts the question &ldquo;should we "
    "optimise the search?&rdquo; into arithmetic with a discouraging answer: "
    "three more states needs a 588-fold improvement, five needs 41,300-fold. "
    "<i>Written while the MSB search was still at 11 states, this section "
    "predicted the rewrite was worth about two.</i> The n = 12 refutation has "
    "since completed, putting MSB&rsquo;s reach at 12 against the LSB "
    "search&rsquo;s 10 at a matched budget of 1,874 s &mdash; a gain of 2 on a "
    "measurement the formula could not have been fitted to, though at the "
    "larger budget the LSB search has since spent the gain reads 1 "
    "(Section 2.7). The same datapoint "
    "also refuted the formula&rsquo;s own premise that g is constant &mdash; it "
    "rises, in all three encodings &mdash; which makes the inverse figures "
    "above optimistic; Section 7 carries the correction."))
story.append(P(
    "<b>Against the goals.</b> <b>G1</b> gained the tree-branching deficit of "
    "Section 2.4 &mdash; and lost a false observation, which is worth "
    "recording as progress in the same column. <b>G2 did not move, for the "
    "third stock-take running</b>, and there is now a structural reason to "
    "expect it will not move by this route: refuting at size n costs minutes "
    "while <i>finding</i> a certificate that exists at n costs hours (36 "
    "seconds to refute 10 states against 213 to 2,803 seconds to find one at "
    "11), so this machinery produces negative answers cheaply and positive "
    "ones barely at all. That asymmetry is a property of the evidence the "
    "method generates, not of the machines, and it should be stated whenever "
    "the accumulated negatives are presented as if they were a weight of "
    "evidence. <b>G3</b> is again where the yield is: P9 went from a pattern "
    "to a formula that predicts. <b>G4</b> gained two transferable pieces "
    "&mdash; the MSB-synchronous elimination, which holds for every "
    "branch-affine machine in any base, and the adequacy check, which any "
    "future search-based impossibility claim in this program should carry."))
story.append(P(
    "<b>What follows, for what remains.</b> The exchange rate settles one "
    "question outright: no more states, in any encoding or convention. That "
    "was already on the &ldquo;will not pursue&rdquo; list on general grounds; "
    "it is now there with a number attached. Three things remain worth doing, "
    "and the ranking has changed. <b>First, WS4</b>, unchanged in position but "
    "materially better supplied: it can now say that three certificate "
    "families each failed within a measured resource, that the bounds are "
    "certified non-vacuous, that the cost of extending any of them obeys a "
    "measured exchange rate, and that the method is biased toward producing "
    "exactly the kind of result it produced. <b>Second, the tree-branching "
    "deficit</b> (Section 2.4), promoted above the census: it is the only open "
    "<i>positive</i> empirical question the program currently holds, the trees "
    "are small enough to interrogate directly, and any proved bound c &lt; the "
    "interval ceiling feeds straight into WS2&rsquo;s counting. The first step "
    "is to find out what the deficit is made of &mdash; whether it is a "
    "boundary effect of the powers-of-2 seeds or persists in the interior of "
    "the tree. <i>(That step was taken and it closed the item rather than "
    "advancing it &mdash; the deficit is an artefact of the seeds and there is "
    "no phenomenon to bound. Section 2.7. The question named here was the "
    "right one; the expectation that it had a positive answer was not.)</i> "
    "<b>Third, WS1&rsquo;s unbounded question as a proof target "
    "rather than a search target</b>: is there an automatic invariant of "
    "<i>any</i> size? Search cannot reach it and the exchange rate says buying "
    "reach is futile, but WS1 produced the lever itself &mdash; a certificate "
    "must avoid the entire halting basin, not merely H &mdash; and that is a "
    "structural statement, not a bounded one. Then the census (WS5), which is "
    "unchanged in rationale and now inherits both the cheaper MSB encoding and "
    "the adequacy check as automatic quality control."))

story.append(P("2.6&nbsp;&nbsp;Stock-take: the rate itself was not a law", H2))
story.append(P(
    "Two refutations completed after Section 2.5 was written, and between them "
    "they confirmed that section&rsquo;s central formula and refuted its "
    "central assumption. <b>What arrived.</b> The MSB search refuted n = 12 in "
    "1,679 s, moving that bound from 11 to <b>12 states</b>; and machine 3 "
    "refuted n = 7 in 12,018 s against 73.2 million clauses, moving its bound "
    "from 6 to <b>7 states</b>. The second matters out of proportion to its "
    "size: it is a different map in a different base, so the certificate "
    "program&rsquo;s negative results now rest on two machines rather than one, "
    "and the branch-affine interface (Section 2.3) carried the whole apparatus "
    "across without modification."))
story.append(P(
    "<b>The prediction held, prospectively.</b> Section 2.5 was written while "
    "the MSB search stood at 11 states and predicted, from C = 42.32 and a "
    "mean g, that the rewrite was worth about two states. The n = 12 result "
    "arrived afterwards and put MSB&rsquo;s reach at 12 against the LSB "
    "search&rsquo;s 10 on a matched cumulative budget of 1,874 s: a gain of 2, "
    "on a measurement the formula could not have been fitted to. That is the "
    "only "
    "<i>prospectively confirmed</i> quantitative claim in this program, which "
    "is worth something precisely because so little else here predicts "
    "anything &mdash; but it ranks below the results that are simply proved "
    "(the density theorem of Section 2.2, the forcing lemma of Section 2.4), "
    "and a confirmed empirical prediction should not be mistaken for the "
    "stronger thing. It comes with one qualification, recorded before the "
    "fact: a reach gap is a function of the budget one fixes. The gap is 2 at "
    "the matched budget of about 1,900 s; if the LSB n = 11 instance now "
    "running completes, LSB reaches 11 at a budget near 14,000 s and the gap "
    "reads 1. The two readings <i>bracket</i> the formula&rsquo;s 1.61 to 2.09 "
    "rather than pinning it."))
story.append(P(
    "<b>And it refuted its own premise &mdash; a premise this document had "
    "already discarded once.</b> The exchange rate treats the per-state cost "
    "factor g as constant, which is what licenses quoting one g per encoding "
    "and then inverting it. Both new datapoints are the largest factor yet "
    "seen in their series &mdash; MSB 10.18&times; at n = 11 to 12, machine 3 "
    "<b>53.20&times;</b> at n = 6 to 7 &mdash; and across all four independent "
    "series, spanning two machines and three conventions, the last step is the "
    "largest every time. Consequently the inverse prices in Section 7 "
    "(588-fold for three more states, 41,300-fold for five) understate the "
    "true cost &mdash; <i>conditional on the rise continuing</i>, which is an "
    "extrapolation from four bounded series and not a proved property of the "
    "search. Were the factor to plateau at its current slope those prices "
    "would be roughly right rather than optimistic; nothing observed rules "
    "that out, and the honest statement is that the error runs in the safe "
    "direction under any continuation consistent with the data. <i>The novelty "
    "here is also reach, not the "
    "fact.</i> Section 2.3 &mdash; written before Section 2.5 &mdash; already "
    "recorded that the factor was rising, and drew the sharper conclusion "
    "without any formula: that the wall is &ldquo;not merely far away but "
    "accelerating away, and no constant-factor engineering reaches the sizes "
    "at which the question would become interesting.&rdquo; That is Section "
    "2.5&rsquo;s conclusion, reached earlier and without its false premise. So "
    "the correct account is not that new data revealed a rising g; it is that "
    "<b>Section 2.5 regressed against Section 2.3</b>, assuming away precisely "
    "the fact an earlier section had flagged as the one that mattered. What "
    "the new datapoints genuinely add is scope &mdash; four series across two "
    "machines and three conventions, where there had been one &mdash; and the "
    "quantified direction of the error."))
story.append(P(
    "<b>The pattern worth naming: twice within a day, a quantity summarised "
    "over the range examined was relied on outside it.</b> In Section 2.4 the "
    "backward branching ratio was found sitting on its rigorous ceiling on two "
    "machines and written up as the quantitative form of the pseudorandomness "
    "heuristic; the agreement turned out to be forced by an arithmetic "
    "identity, so the measurement could not have come out any other way. In "
    "Section 2.5 the per-state factor was summarised as one number per "
    "encoding and then <i>inverted</i> to price all future work; the number "
    "was a geometric mean over a window, and the underlying quantity drifts. "
    "The two are not quite the same error. The first was a fresh misreading of "
    "what a measurement could show. The second is worse in one specific way: "
    "<b>the caveat was already on record two sections earlier</b>, so this was "
    "not a fact the program lacked but one it had written down and then "
    "assumed away. Both are cheap to defend against, and Section 11 now "
    "carries the umbrella trap: before quoting a measured regularity, ask what "
    "would have to be true for it to come out differently; if it is to be "
    "extrapolated or inverted, check which way it drifts at the edge of the "
    "data; and grep the document for what it already says about the quantity "
    "before treating it as new."))
story.append(P(
    "<b>Against the goals.</b> <b>G1</b> gained no new fact about the "
    "machines. The rising factor is a fact about our instruments, and saying "
    "otherwise would be the third instance of the error just named. <b>G2 did "
    "not move, for the fourth stock-take running.</b> <b>G3</b> is again the "
    "yield, and this time narrowly &mdash; and less than the previous "
    "paragraph would suggest, since the decaying rate restores an observation "
    "Section 2.3 already held rather than adding one. What is genuinely new is "
    "its scope: measured now on four series across two machines, where the "
    "original was a single series on one. One <i>weakly</i> "
    "suggestive observation belonged here and has since been withdrawn "
    "&mdash; that after the best encoding change available to us the wall "
    "re-formed with an essentially unchanged gradient (10.18&times; against "
    "10.24&times;), which is what one expects if the wall belongs to the "
    "problem and not to the encoding. It compared a single step against a "
    "single step, and the LSB search has since taken one more: it pays "
    "15.89&times;, not 10.24&times;, so the gradients are <i>not</i> equal "
    "and MSB remains the cheaper encoding per state (Section 7). The "
    "withdrawn version rested on timings carrying perhaps "
    "&plusmn;30% from concurrent load; it is a straw in the wind, not a "
    "result. <b>G4</b> gained the projection instrument: each series&rsquo; "
    "own last factor now gives a lower bound on what its next state costs."))
story.append(P(
    "<b>What follows.</b> The ranking of Section 2.5 is unchanged &mdash; WS4, "
    "then the tree-branching deficit, then WS1&rsquo;s unbounded question as a "
    "proof target, then the census &mdash; and the projections harden the one "
    "negative decision behind it. Priced from each series&rsquo; own last "
    "measured factor, the cheapest unclaimed state in the program costs about "
    "4.7 hours (MSB n = 13); the next two cost <b>63 hours</b> (0-invariant "
    "n = 14) and <b>178 hours</b> (machine 3 n = 8) &mdash; each computed by "
    "applying that series&rsquo; own last measured factor once more, so each "
    "is a lower bound if the rise continues and roughly accurate if it "
    "plateaus. Nothing in the ranked plan depends on any "
    "of them. The instruction that follows is not &ldquo;wait&rdquo; but "
    "&ldquo;stop&rdquo;: the two multi-day jobs should be abandoned rather "
    "than left to run, since their results would change no claim in this "
    "document."))

story.append(P("2.7&nbsp;&nbsp;The tree-branching deficit was the wrong null "
               "model", H2))
story.append(P(
    "Section 2.4 retracted a measured <i>agreement</i> as forced arithmetic and "
    "put a measured <i>disagreement</i> in its place: backward branching along "
    "the tree of H runs about 21% below its interval ceiling on the Needle and "
    "about 30% below on machine 3. Section 2.5 promoted that deficit above the "
    "census, called it the only open positive empirical question the program "
    "held, and named its first step &mdash; find out whether the deficit is a "
    "boundary effect of the powers-of-2 seeds or persists in the interior of "
    "the tree. That step has now been taken, and the answer is <b>both, and "
    "for one reason</b>: it is entirely an effect of the seeds, and it persists "
    "into the interior because the seeds&rsquo; arithmetic is inherited by "
    "every descendant. There is no dynamical phenomenon here. The deficit "
    "measures the distance between a statistic and a null model that never "
    "applied to it."))
story.append(P(
    "<b>The criterion (proved).</b> Reading the backward formula of Section 2.4 "
    "modulo A<sub>v</sub> = 2<super>v+1</super> + 3 and using "
    "2<super>v+1</super> &#8801; &minus;3, the condition for y to have a "
    "preimage of valuation v collapses to a single congruence, "
    "3y &#8801; 2<super>v</super>(3 &minus; 2v), that is"))
story.append(P("y &#8801; 2<super>v</super> + v &nbsp;&nbsp;(mod "
               "2<super>v+1</super> + 3),", MATHC))
story.append(P(
    "one class per branch, which is where the ceiling "
    "&#8721;<sub>v</sub> 1/A<sub>v</sub> = 0.5453 comes from. (Machine-verified "
    "against the explicit backward map for 3 &le; y &lt; 60,000: zero "
    "disagreements.) The ceiling is a statement about a <i>uniform</i> y. The "
    "roots of the tree are not uniform &mdash; they are H itself, the powers "
    "of 2, and a power of 2 does not meet the residue classes modulo "
    "A<sub>v</sub> uniformly. It meets the cyclic subgroup generated by 2. So "
    "the density of M for which 2<super>M</super> admits branch v is "
    "1/ord<sub>A<sub>v</sub></sub>(2) when 2<super>v</super> + v lies in that "
    "subgroup, and <b>zero</b> when it does not &mdash; never 1/A<sub>v</sub>."))
story.append(tab([
    ["0", "5", "1", "4", "1/4 = 0.2500", "0.2000"],
    ["1", "7", "3", "3", "<b>0</b>", "0.1429"],
    ["2", "11", "6", "10", "1/10 = 0.1000", "0.0909"],
    ["3", "19", "11", "18", "1/18 = 0.0556", "0.0526"],
    ["4", "35", "20", "12", "<b>0</b>", "0.0286"],
    ["5", "67", "37", "66", "1/66 = 0.0152", "0.0149"],
], ("v", "A<sub>v</sub>", "2<super>v</super>+v<br/>mod A<sub>v</sub>",
    "ord(2)", "density off a<br/>power of 2", "interval<br/>model 1/A<sub>v</sub>"),
   (0.4 * inch, 0.6 * inch, 0.85 * inch, 0.6 * inch, 1.35 * inch, 1.05 * inch)))
story.append(P(
    "Branch 1 is impossible because 2<super>M</super> &#8801; 3 (mod 7) has no "
    "solution &mdash; the subgroup is {1, 2, 4}. Branch 4 is impossible because "
    "2<super>M</super> &#8801; 20 (mod 35) would need a non-unit. Nine of the "
    "first twenty valuations are impossible outright (v = 1, 4, 7, 9, 10, 12, "
    "13, 18, 19), and the survivors are re-weighted. Summing the exact "
    "densities over v &lt; 20 predicts a root branching of <b>0.4336</b>; "
    "evaluating d(2<super>M</super>) directly for M &lt; 3,200 gives "
    "<b>0.4344</b>; and the tree&rsquo;s own depth-0 row measures "
    "<b>0.4339</b>, against a pooled figure over the whole tree of 0.4337. The "
    "deficit is present in full at the root, and it is predicted from "
    "multiplicative orders to three decimals.", FIGCAP))
story.append(P(
    "<b>Machine 3 states it more sharply.</b> The same argument in base 3, with "
    "H the powers of 27, kills almost everything: of the 28 branches (j, r) "
    "with j &le; 13, <i>exactly two survive</i> &mdash; j = 1 with r = 1 and "
    "r = 2, each at density 1/4, because ord<sub>10</sub>(27) = 4. Predicted "
    "root branching <b>0.5000</b> against an interval ceiling of 0.8081; "
    "measured root branching <b>0.5000</b>, exactly, 133 children from 266 "
    "roots. The content of that is an impossibility theorem in the WS3 family, "
    "reached from an entirely different direction: <b>every preimage of a power "
    "of 27 has 3-adic valuation exactly 1</b> (verified for j &le; 13 by exact "
    "order computation; no larger j contributed to any of the 266 roots "
    "measured). It lands precisely where WS1 said the difficulty lives &mdash; "
    "on the structure of the halting basin a certificate has to avoid."))
story.append(P(
    "<b>The control, which is what decides it.</b> Rebuild the identical "
    "backward trees on generic roots of the same size. If the deficit belongs "
    "to the map or to the tree, it must survive; if it belongs to the roots, "
    "it must vanish."))
story.append(tab([
    ["halting set (powers of 2)", "0.4337", "0.4339", "0.4335"],
    ["generic, 800-bit roots", "0.5262", "0.5325", "0.5205"],
    ["generic, 1600-bit roots", "0.5330", "0.5281", "0.5372"],
    ["generic, 3200-bit roots", "0.5518", "0.5563", "0.5482"],
], ("roots (1,600 each; 3,190 for H)", "pooled", "depth 0", "depth &ge; 1"),
   (2.3 * inch, 0.9 * inch, 0.9 * inch, 0.95 * inch)))
story.append(P(
    "Generic roots sit on the ceiling of 0.5453 at every depth. The halting "
    "tree sits 20% below it at every depth. The backward operator is unbiased; "
    "only the roots are special.", FIGCAP))
story.append(P(
    "<b>Why the skew survives the descent.</b> The backward map is affine in "
    "its argument, so by induction every node at depth j is "
    "(&alpha;&middot;2<super>M</super> + &beta;)/&gamma; with coefficients "
    "fixed by the branch word alone. A descendant of a power of 2 is never a "
    "generic integer, at any depth &mdash; its residues stay inside images of "
    "the multiplicative orbit of 2, which is why the interval model fails all "
    "the way down rather than only at the root. This is visible without any "
    "theory: node residues modulo 7 in the halting tree are supported on "
    "{1, 2, 4} at depth 0 (0.334, 0.333, 0.333, and exactly zero on the other "
    "four classes) and are still violently skewed at depth 1, where two classes "
    "carry 0.012 and 0.007 against a uniform 0.143; the control is flat to "
    "within sampling at every depth."))
story.append(P(
    "<b>What it costs, and the pattern it completes.</b> The cost is that WS6&rsquo;s "
    "retargeted question dissolves and G1 gives back an observation: the "
    "&ldquo;only open positive empirical question&rdquo; was not a question. "
    "The gain is two impossibility results and a corrected model. But the "
    "reason this section matters more than either is that <b>it is the second "
    "retraction of the same kind, in the same place</b>. Section 2.4 threw out "
    "a measured <i>agreement</i> with the independence model because the "
    "agreement was forced; Section 2.7 throws out the measured "
    "<i>disagreement</i> that replaced it, because the disagreement is forced "
    "too. Both times an aggregate statistic was read as evidence about the "
    "dynamics while the null model it was compared against did not apply to "
    "the sample actually drawn &mdash; and both times the diagnosis cost "
    "minutes, because the fix is the same: <i>run the statistic on a control "
    "whose answer you already know</i>. That test now belongs in Section 11 "
    "beside the others, and it is the one this program has needed twice."))

story.append(P("2.8&nbsp;&nbsp;WS4: three bounds in three units, and what "
               "happened when they were converted", H2))
story.append(P(
    "WS4 was the top item of the revised ranking, and its brief was to build an "
    "account of decider-resistance out of <i>our own</i> three impossibility "
    "results and their measured growth rates. The account exists "
    "(<font face='Courier'>formal/ws4/</font>, with its own report). Two of its "
    "premises did not survive being executed, and the first of those changes "
    "how the program should read its own results."))
story.append(P(
    "<b>The three bounds were never comparable.</b> They are quoted in three "
    "units &mdash; DFA states, congruence modulus, backward depth &mdash; which "
    "invites ranking them by size. Two of them convert into each other exactly. "
    "A congruence certificate is a union of residue classes mod m, and the "
    "canonical residue trackers take <b>m</b> states reading most-significant-"
    "digit first (c &rarr; 2c + d) but <b>m &middot; ord<sub>m</sub>(2)</b> "
    "states reading least-significant-digit first. So an n-state impossibility "
    "rules out exactly those moduli whose tracker fits in n states:"))
story.append(tab([
    ["direct congruence sweep", "~30 seconds",
     "<b>every m &le; 20,000</b>, with any threshold", "19,999"],
    ["MSB automatic, &le; 13 states", "~3.2 hours cumulative",
     "moduli 2..13", "12"],
    ["LSB automatic, &le; 11 states", "~5 hours cumulative",
     "moduli 2, 3, 4", "<b>3</b>"],
], ["certificate family", "compute spent", "moduli ruled out", "count"],
    [1.6 * inch, 1.35 * inch, 1.9 * inch, 0.65 * inch]))
story.append(P(
    "<b>The headline of this program for two days is the weakest of the three "
    "on this axis, by roughly 1,500&times;.</b> That is not an argument that "
    "WS1 was wasted, and the reading that matters is the other one: WS1&rsquo;s "
    "value was never the state count. What it established is the <i>shape</i> "
    "of the obstruction &mdash; that a certificate must avoid the entire "
    "halting basin and not merely H &mdash; and that survives the conversion "
    "untouched. What does not survive is the habit of quoting &ldquo;&le; 11 "
    "states&rdquo; as though the number measured something. A union of residue "
    "classes is a vanishing fraction of the automatic sets of any size, so the "
    "two families genuinely do not contain one another; the point is that "
    "neither number tells you which is stronger until you convert."))
story.append(P(
    "<b>What the cheap sweep actually buys.</b> In one variable, "
    "Presburger-definable means ultimately periodic, which means congruence "
    "plus threshold &mdash; so the single sweep refutes linear-arithmetic "
    "non-termination certificates, the affine sieve, and <i>every bbchallenge "
    "regular decider</i> at once, the last because a regular language over "
    "unary-coded counters is ultimately periodic. The wiki records that "
    "cryptids resist these deciders as an empirical fact; this is the "
    "structural reason. The m = 1 case needs no sweep at all: the Needle&rsquo;s "
    "orbit is strictly increasing, so a certificate that is a finite union of "
    "intervals must contain a ray, and every ray contains a power of two."))
story.append(P(
    "<b>A soundness bug, and a fix that strengthened the theorem.</b> The first "
    "version of the sweep collided the orbit against every residue that "
    "2<super>e</super> takes mod m. That is unsound for a threshold claim: "
    "2<super>e</super> mod m is only <i>eventually</i> periodic, and a residue "
    "in the pre-period is taken by finitely many powers of two, so a large "
    "enough threshold defeats a collision there. Restricting to the eventual "
    "cycle makes every witness an infinite family of halting values, and the "
    "refutation then holds for <i>every</i> threshold rather than for "
    "thresholds below a cutoff. The search became harder and the conclusion "
    "became better &mdash; worth recording, because the failure mode is silent: "
    "the sweep reported success either way."))
story.append(P(
    "<b>The last survivor was worth an hour.</b> One modulus held out, "
    "2&middot;3<super>8</super> = 13,122 for machine 3, whose single "
    "threshold-proof residue demands v<sub>3</sub>(a) &ge; 8 together with an "
    "odd 3-free part; all eight orbit values with v<sub>3</sub> &ge; 8 in the "
    "first 60,500 had an even one. A genuine survivor would have been a "
    "<i>proof</i> that machine 3 never halts, so it was diagnosed rather than "
    "swept away with a wider window &mdash; and the diagnosis produced a "
    "theorem:"))
story.append(P("G(a) &#8801; v<sub>3</sub>(a) &nbsp;(mod 2)", MATHC))
story.append(P(
    "since G(a) = (3<super>j+1</super>+1)m + (r&middot;3<super>j</super> + j + "
    "c<sub>r</sub>) has an even leading coefficient, 3<super>j</super> is odd, "
    "and r + c<sub>r</sub> is odd for both r. So the 3-free part of an orbit "
    "value is odd about a quarter of the time rather than half, eight even ones "
    "in a row has probability 0.10 rather than 1/256, and the survivor was "
    "luck; extending the orbit killed it at index 105,033. <b>The lemma is the "
    "durable output, and it exists only because a null result was checked "
    "instead of accepted.</b>"))
story.append(P(
    "<b>The size frontier does not separate our machines, and the plan said it "
    "did.</b> WS4.1 delivered what it promised &mdash; a verified compiler from "
    "register machines into one-counter guarded-affine form at no more than 2I "
    "rules, step for step, and Conway&rsquo;s PRIMEGAME re-run here as a "
    "14-rule instance checked to emit the primes rather than quoted as doing "
    "so. But the plan&rsquo;s conclusion, that our cryptids &ldquo;sit strictly "
    "below&rdquo; the universal machines, does not follow. Valuation branching "
    "unfolds a single rule schema into infinitely many affine pieces, so "
    "smaller on the page is not smaller in power, and nothing known "
    "lower-bounds a one-schema valuation machine. <b>The frontier is an upper "
    "bound on where universality begins, and that is all it is.</b>"))
story.append(P(
    "What replaces it is a better question, and the only two-sided bet the "
    "program currently holds: <i>is the one-schema valuation class "
    "Turing-complete?</i> If it is, the frontier is vacuous for our machines "
    "and their resistance has a structural cause. If instead the class is "
    "decidable, <b>the decision procedure decides our cryptids</b>. Both "
    "outcomes are consequential, which is the property worth selecting for."))
story.append(P(
    "<b>And a measurement lesson that invalidates a number in Section 2.6.</b> "
    "Every growth constant this program has quoted came from runs executed "
    "concurrently on one box at varying load. A completed UNSAT survives that; "
    "the constant that <i>prices</i> it does not. Re-measured under a single "
    "load condition &mdash; one process, strictly sequential, load sampled at "
    "every instance &mdash; the contamination is about threefold (MSB at n = 10 "
    "costs 7.9 s clean against 24.6 s loaded), and <i>both</i> series come out "
    "strictly monotone: MSB at 2.73, 4.10, 6.91, 11.23, 13.12 and LSB at 4.30, "
    "4.35, 5.55, 9.46. Every reversal in the loaded series was load. The "
    "reading that the factor had fallen back at n = 13, which arrived just as "
    "two competing multi-day jobs were killed, is withdrawn &mdash; measured "
    "cleanly that step is the <i>largest</i> in its series. What the clean "
    "numbers do confirm is the qualitative claim they were quoted for: the "
    "per-state cost rises, and the MSB advantage compounds (18.98, 38.62, "
    "89.23 at n = 8, 9, 10) rather than being a fixed discount."))

story.append(P("2.9&nbsp;&nbsp;WS5: the census, and the first time the "
               "program&rsquo;s own tools decided anything", H2))
story.append(P(
    "The census was promoted on the grounds that it is the only item that "
    "changes the <i>supply</i> of results rather than pushing one machine "
    "further. WS4 then handed it a target: the one-schema valuation class, "
    "whose Turing-completeness is the open question and which is also where "
    "both flagship machines live. Code and report in "
    "<font face='Courier'>census/</font>."))
story.append(P(
    "A member of the family is five integers: with x = 2<super>v</super>m, m "
    "odd, the machine halts at m = 1 and otherwise sends "
    "x = 2<super>v+1</super>k + 2<super>v</super> to A<sub>v</sub>k + "
    "B<sub>v</sub>, where A<sub>v</sub> = &alpha;2<super>v+1</super> + &beta; "
    "and B<sub>v</sub> = &gamma;2<super>v</super> + &delta;v + &epsilon;. The "
    "Space Needle is (1, 3, 1, 1, 0), checked against its own step function. "
    "1,080 machines were enumerated, 3 are not well defined, and the remaining "
    "1,077 were put through the whole pipeline in 220 seconds."))
story.append(P(
    "<b>318 of them &mdash; 29.5% &mdash; are decided outright</b>, proved "
    "never to halt, by an exact congruence test. The test is complete for its "
    "class, unlike the necessary condition Section 2.8 had to settle for: on "
    "branch v the source-target pair mod m traces one affine map, and "
    "A<sub>v</sub>, B<sub>v</sub> mod m depend on v only through "
    "(2<super>v</super> mod m, v mod m), a state space of size "
    "m<super>2</super>, so iterating until that state repeats enumerates every "
    "branch. Two further machines are proved never to halt after their <i>first "
    "step</i>. <b>All 318 certificates were re-audited by brute force without "
    "reusing the machinery that produced them: zero failures.</b> A false proof "
    "of non-halting is the worst thing this program could emit."))
story.append(P(
    "<b>So G2 moves, for the first time in four stock-takes &mdash; and the "
    "honest size of the move is this.</b> The machines decided are new and "
    "easier ones; a machine with a separating congruence is by definition not a "
    "cryptid, and none of the seven case-file machines was touched. What the "
    "census delivers is the partition: which members are easy, why, and a pool "
    "of 120 hard ones. Worth noting what it cost, though. 220 seconds decided "
    "318 machines; two days of SAT search bought two states."))
story.append(P(
    "<b>Three theorems came out, and one of them is about the Needle.</b> The "
    "closed form for the cheapest certificate of all is exact on every machine "
    "in the census: a member is decided at modulus 3 if and only if"))
story.append(P("&delta; &#8801; 0,&nbsp;&nbsp;&gamma; &#8801; &alpha;,"
               "&nbsp;&nbsp;&beta; + &epsilon; &#8801; 0&nbsp;&nbsp;(mod 3)",
               MATHC))
story.append(P(
    "because mod 3 the powers of two occupy every nonzero class, so a "
    "separating class must be {0}, and 3 | x forces k &#8801; 1, leaving "
    "F(x) &#8801; (&minus;1)<super>v</super>(&gamma;&minus;&alpha;) + &beta; + "
    "&delta;v + &epsilon;. Checked: 41 predicted, 41 decided, no discrepancies "
    "in 1,077 machines. <b>The corollary is the sharpest statement the program "
    "has about why its own flagship resists: the v-linear term blocks the "
    "cheapest certificate there is, and the Needle has &delta; = 1.</b> That "
    "term injects unbounded valuation information into the value, and no "
    "modulus can follow it."))
story.append(P(
    "<b>And the Needle is not special in anything measured globally.</b> Drift "
    "and the backward branching ceiling turn out to be functions of (&alpha;, "
    "&beta;) alone &mdash; 24 classes, none carrying two values &mdash; so 45 "
    "machines share its drift 0.9411 and ceiling 0.54528 exactly. Both of the "
    "statistics this program spent weeks computing are blind to 44 siblings. "
    "What separates them is the sieve, which reads (&gamma;, &delta;, "
    "&epsilon;): across those twins the forbidden mass runs 0.0000 to 0.7988, "
    "with the Needle at 0.2852 &mdash; an independent reproduction of WS3&rsquo;s "
    "28.7%. And &beta; parity is what makes a member hard at all: even &beta; is "
    "decided 68% of the time, odd &beta; 5%, and 108 of the 120 cryptid "
    "candidates have odd &beta;. An odd A<sub>v</sub> is exactly the classic "
    "Collatz situation &mdash; no 2-adic structure to exploit."))
story.append(P(
    "Seven undecided machines have <i>every</i> branch forbidden out to v = 200. "
    "Two of them yielded uniform arguments and became the two "
    "any-start theorems. <b>The other five are not claimed</b>: forbidden to "
    "v = 200 is not forbidden for all v, and that gap is the kind this program "
    "does not paper over. They are the best open leads the census produced "
    "&mdash; Section 2.10 closes three of the five the next day, and Section 2.11 closes the other two and finishes the method, using "
    "nothing the census had not already computed."))

story.append(P("2.10&nbsp;&nbsp;Status board: every workstream, and what each "
               "goal actually got", H2))
story.append(P(
    "The plan of July 25 had six workstreams and this document has recorded "
    "them across nine subsections written as the work happened, which is the "
    "right order to <i>do</i> the work and the wrong order to <i>read</i> it. This "
    "section is the consolidated board, so that the state of the program can be "
    "read off in one place instead of reconstructed. It says three things a "
    "single stock-take could not: the plan is close to exhausted, the one goal "
    "that had never moved was moved by the one workstream that changed the "
    "supply of machines rather than the depth on two of them, and the remaining "
    "items are no longer ranked the way the plan ranked them."))
story.append(Spacer(1, 4))
story.append(tab([
    ("WS1 &mdash; automatic invariants", "executed; closed at its bound",
     "No q-automatic non-halting certificate exists at the sizes searched, and "
     "the encodings were proved adequate by construction rather than by "
     "sampling, so the UNSATs are not vacuous",
     "DFA states: Needle 13 MSB-first, 11 LSB minimal-word, 13 LSB "
     "0-invariant; machine 3, 7 states in base 3", "G3"),
    ("WS2 &mdash; halting density", "executed",
     "Depth-graded polylogarithmic density theorem, with the completeness "
     "cutoff lemma that turns enumeration into a count",
     "Exact complete counts at every fixed backward depth, run to "
     "x = 10<super>192</super>", "G1"),
    ("WS3 &mdash; forbidden valuations", "executed; saturated",
     "Unconditional exclusion of halting steps &mdash; the collection&rsquo;s "
     "first statements about the actual orbit at infinite time &mdash; and the "
     "sieve proved machine-independent",
     "Needle 28.7% of steps; machine 3 95.06% of consecutive pairs; the ladder "
     "has exactly one rung", "G1, G3"),
    ("WS4 &mdash; hardness frontier", "executed",
     "The three impossibility bounds converted to a common currency; "
     "one-variable semilinear certificates refuted wholesale; the slope theorem; "
     "a verified register-machine compiler",
     "Every modulus m &le; 20,000 with any threshold, on both machines, in "
     "about 30 seconds", "G3"),
    ("WS5a &mdash; Fenrir", "executed",
     "The first FRACTRAN cryptid entered as machine 7, with an exact halting "
     "criterion", "Complete", "G1"),
    ("WS5b &mdash; the census", "executed",
     "318 machines decided outright and independently audited; T1, T2 and &mdash; "
     "in the follow-up below &mdash; T4&ndash;T6, all non-halting after their "
     "first step; T3, the closed form for the cheapest certificate",
     "The whole (&alpha;, &beta;, &gamma;, &delta;, &epsilon;) box &mdash; "
     "1,077 machines, moduli to 64, in 220 seconds", "G2, G1, G3"),
    ("WS5c &mdash; Lean, community", "not started", "&mdash;",
     "&mdash;", "G4"),
    ("WS6 &mdash; stochastic backbone", "not started; target vacated twice",
     "&mdash;",
     "Both anomalies it was pointed at &mdash; the ceiling coincidence and the "
     "tree deficit &mdash; turned out to be forced (Sections 2.4 and 2.7)",
     "G1"),
], ("workstream", "status", "what it delivered", "reach attained", "goals"),
   (1.15 * inch, 0.8 * inch, 2.15 * inch, 1.75 * inch, 0.5 * inch)))
story.append(P(
    "<b>Table.</b> Every workstream in the July 25 plan. Five of six are "
    "executed; what remains of the plan is one durability chore and one "
    "workstream whose target dissolved under examination.", FIGCAP))
story.append(P(
    "<b>Against the four goals, scored honestly.</b> The scoring matters more "
    "than the list, because three of the four verdicts have changed at least "
    "once and one of them changed direction."))
story.append(Spacer(1, 4))
story.append(tab([
    ("G1 &mdash; new observations", "The program&rsquo;s main yield, "
     "consistently",
     "The density theorem and its cutoff lemma; the forbidden-valuation "
     "theorem; machine 3 pinned to a single valuation for the last two steps "
     "before any halt; Fenrir&rsquo;s criterion; the thin-H law; the slope "
     "theorem; T1, T2, T3; and the fact that drift and the branching ceiling "
     "depend on (&alpha;, &beta;) alone"),
    ("G2 &mdash; decide halting", "Moved once, and only on easier machines",
     "318 of 1,077 census members decided, plus five proved never to halt after "
     "their <i>first step</i> (T1, T2, T4&ndash;T6) &mdash; against zero of the seven "
     "case-file machines, "
     "in either direction. A machine with a separating congruence is by "
     "definition not a cryptid, so the move is real but it is not the move "
     "the goal was written for"),
    ("G3 &mdash; explain the hardness", "The surprise: a list became an account",
     "Four mechanisms, each measured rather than asserted: a certificate must "
     "avoid the whole halting <i>basin</i>, not the halting set; the "
     "sieve&rsquo;s strength is governed by how thin H is as a set of values; "
     "every method is exact inside a bounded resource and silent beyond it, "
     "with the growth constant measured in each case (pattern P9); and the "
     "v-linear term &delta;v blocks the cheapest certificate there is"),
    ("G4 &mdash; a toolkit that transfers", "Settled, and now generative",
     "The branch-affine interface F(x) = A<sub>p</sub>m + B<sub>p</sub> on "
     "x = q<super>|p|</super>m + val(p) carries the sieve, the base-q SAT "
     "search and the density counting unmodified. The census went further and "
     "made the toolkit produce machines instead of consuming them &mdash; the "
     "only thing built here that scales with compute rather than with "
     "attention"),
], ("goal", "verdict", "what supports it"),
   (1.35 * inch, 1.5 * inch, 3.9 * inch)))
story.append(P(
    "<b>Table.</b> The four goals, scored against the executed work. G2&rsquo;s "
    "verdict is the one to read twice.", FIGCAP))
story.append(P(
    "<b>What the board shows that the individual stock-takes did not.</b> "
    "First, the plan is nearly spent: five of the six workstreams are executed, "
    "the sixth has had its target dissolve twice, and the only unexecuted piece "
    "of the other five is WS5&rsquo;s Lean-and-community limb, which is "
    "engineering rather than research. The next move therefore has to be "
    "<i>derived</i> rather than picked off the list. Second, the ratio between "
    "effort and yield now points in an uncomfortable direction. Two days of SAT "
    "search bought two automaton states; 220 seconds of census decided 318 "
    "machines. That is not an argument that the census is the better science "
    "&mdash; the machines it decided are the ones nobody was stuck on &mdash; "
    "but it is an argument about where the next result is likely to come from, "
    "and it points away from depth on the flagship and toward breadth around "
    "it. Third, and least comfortable: <b>every one of the program&rsquo;s "
    "positive results is about the machines that are not hard, and every result "
    "about the hard ones is negative.</b> That is a coherent research position "
    "&mdash; it is what G3 is for, and the account is genuinely sharper than "
    "anything in the literature &mdash; but it should be stated rather than "
    "left to be inferred from nine subsections of progress."))
story.append(P(
    "<b>Building the board turned one of its own open leads into three "
    "theorems.</b> The census left five machines whose every branch is sieved "
    "out to v = 200, recorded as leads and deliberately not claimed. Checking "
    "them against each other rather than one at a time shows they are not five "
    "problems: <b>four of them have A<sub>v</sub> = 2<super>v+2</super> "
    "&minus; 1 identically</b> &mdash; the whole &alpha; = 2, &beta; = &minus;1 "
    "corner &mdash; which is exactly T2&rsquo;s modulus, where ord(2) = v + 2 "
    "makes the powers of two the listable set {1, 2, &hellip;, "
    "2<super>v+1</super>}. Writing branch v&rsquo;s halting condition as "
    "2<super>e</super> &#8801; S<sub>v</sub> (mod A<sub>v</sub>), the fixed "
    "point gives P<sub>0</sub> = (2B<sub>v</sub> &minus; A<sub>v</sub>)"
    "2<super>v</super> and Q<sub>0</sub> = 1 &minus; 2<super>v+1</super>; and "
    "since 2<super>v+2</super> &#8801; 1 forces 2<super>v+1</super> &#8801; "
    "2<super>&minus;1</super>, we get Q<sub>0</sub> &#8801; "
    "2<super>&minus;1</super> and the whole expression collapses.", BODY))
story.append(P("<b>Lemma.</b>&nbsp;&nbsp;For &alpha; = 2, &beta; = &minus;1:"
               "&nbsp;&nbsp;S<sub>v</sub> &#8801; 2B<sub>v</sub> "
               "(mod A<sub>v</sub>)", MATHC))
story.append(P(
    "<i>Verified: 45 machines, 18,045 branches, v = 0 to 400, no mismatches.</i> "
    "A power of two mod A<sub>v</sub> is 1 or even, so <b>S<sub>v</sub> odd and "
    "greater than 1 already forbids the branch</b>, as does S<sub>v</sub> = 0. "
    "That closes three of the four in a line each: (2, &minus;1, 2, 2, 1) has "
    "S<sub>v</sub> &#8801; 4v + 3; (2, &minus;1, 3, 0, 0) has "
    "2<super>v+1</super> + 1; (2, &minus;1, 3, 1, 0) has 2<super>v+1</super> + "
    "2v + 1 &mdash; each odd, greater than 1 and less than A<sub>v</sub> for "
    "v &ge; 2, with the boundary branches landing on S<sub>v</sub> = 0. (The "
    "fourth is T2 itself, recovered as S<sub>v</sub> &#8801; 2v + 3.) <b>So "
    "T4, T5 and T6: three more machines that never halt after their first step, "
    "proved "
    "rather than range-checked</b> (<font face='Courier'>census/leads.py</font>). "
    "The remaining two leads do not transfer and stay open: (2, 1, 1, 2, "
    "&minus;1) has A<sub>v</sub> = 2<super>v+2</super> + 1 with "
    "ord(2) = 2(v + 2), twice as many powers to exclude, and (3, 3, 2, 0, 1) "
    "has a v-dependent order (4, 18, 8, 30, 12, 42) and so no listable set at "
    "all."))
story.append(P(
    "<b>The lesson is about the board, not the machines.</b> These four had "
    "been sitting in the same list for a day, described one at a time, each "
    "looking like its own research problem. Nothing new was computed to crack "
    "them &mdash; the collapse came from putting them in a row and noticing "
    "they shared a modulus. <b>Consolidating a status report is not clerical "
    "work; it is the cheapest search this program has run.</b> It is recorded "
    "as a trap in Section 11."))
story.append(P(
    "<b>Superseded the same evening &mdash; see Section 2.11.</b> The ranking "
    "below is kept because it is what the board actually said, and because "
    "what happened to it is the point: item (2) was closed within hours, "
    "and closing it exposed that item (1) had been aimed at the wrong "
    "pool. The board was right that the leads were the cheapest thing on "
    "the table; it was wrong about how cheap.", BODY))
story.append(P(
    "<b>Where the board said the program goes next.</b> (1) <i>Promote one census "
    "candidate to a full case file.</i> T3 says where to look &mdash; odd "
    "&beta;, &delta; &ne; 0 &mdash; and the 120 candidates are currently "
    "candidates on the strength of an undecided orbit alone, which is not the "
    "standard the seven case files were held to. (2) <i>The two leads that did "
    "not transfer.</i> (2, 1, 1, 2, &minus;1) is the more promising: ord(2) = "
    "2(v + 2) is still listable, just twice as long, so the question is whether "
    "S<sub>v</sub> avoids a set of size 2v + 4 rather than v + 2 &mdash; the "
    "same argument with a weaker margin, not a new idea. (3) <i>The VAL(q) "
    "universality question</i> (Section 12), still the only two-sided bet: "
    "universal makes the resistance structural, decidable decides our cryptids. "
    "(4) <i>Lean and the community contribution</i> &mdash; durability rather "
    "than discovery, and the only item here that does not depend on a research "
    "outcome. <b>WS6 is demoted, and the reason is on the record twice.</b> It "
    "was pointed at the ceiling coincidence, which Section 2.4 proved forced, "
    "and then at the tree deficit, which Section 2.7 proved forced as well. A "
    "workstream whose motivating anomaly has evaporated twice should be taken "
    "up again only when a third, genuinely unexplained measurement appears "
    "&mdash; not on the strength of its position in a plan written before "
    "either correction."))

story.append(P("2.11&nbsp;&nbsp;The lemma was universal, and the method is "
               "finished: ten machine theorems and a completeness proof", H2))
story.append(P(
    "The board in Section 2.10 ranked &ldquo;the two leads that did not "
    "transfer&rdquo; second and called the first follow-up&rsquo;s algebra "
    "routine. Both judgements were wrong in the same direction, and the "
    "correction is a single observation: <b>the derivation of "
    "S<sub>v</sub> &#8801; 2B<sub>v</sub> never used &alpha; = 2 or "
    "&beta; = &minus;1.</b> On branch v the sieve forbids a halt unless "
    "Q<sub>0</sub>&middot;2<super>e</super> &#8801; P<sub>0</sub> "
    "(mod A<sub>v</sub>) with P<sub>0</sub> = (2B<sub>v</sub> &minus; "
    "A<sub>v</sub>)2<super>v</super> and Q<sub>0</sub> = 2<super>v+1</super> "
    "&minus; A<sub>v</sub>. Reducing mod A<sub>v</sub> deletes the "
    "A<sub>v</sub> terms outright: Q<sub>0</sub> &#8801; 2<super>v+1</super>, "
    "P<sub>0</sub> &#8801; B<sub>v</sub>2<super>v+1</super>, so "
    "P<sub>0</sub>Q<sub>0</sub><super>&minus;1</super> &#8801; B<sub>v</sub>."))
story.append(P("<b>Universal sieve lemma.</b>&nbsp;&nbsp;For every machine with "
               "&beta; odd:&nbsp;&nbsp;S<sub>v</sub> &#8801; 2B<sub>v</sub> "
               "(mod A<sub>v</sub>)", MATHC))
story.append(P(
    "&mdash; equivalently, <b>branch v can immediately precede a halt if and "
    "only if B<sub>v</sub> lies in &#9001;2&#9002; mod A<sub>v</sub></b>, the "
    "group generated by 2. <i>Machine-verified: 672 machines &mdash; the whole "
    "odd-&beta; box &mdash; 51,030 branches, v = 0 to 80, no mismatches</i> "
    "(<font face='Courier'>census/universal.py</font>). And since "
    "&alpha;2<super>v+1</super> &#8801; &minus;&beta; (mod A<sub>v</sub>), "
    "multiplying by &alpha; removes the exponential from the target:"))
story.append(P("<b>Linear corollary.</b>&nbsp;&nbsp;&alpha;S<sub>v</sub> "
               "&#8801; 2&alpha;&delta;v + 2&alpha;&epsilon; &minus; "
               "&beta;&gamma; &nbsp;(mod A<sub>v</sub>)", MATHC))
story.append(P(
    "<b>The exponential is not in the target; it is only in the modulus.</b> "
    "That is the shape of the whole difficulty in one line: what must be "
    "decided is whether an affine function of v lands in the group generated "
    "by 2, modulo a number that doubles with v. Whether that is hard depends "
    "entirely on how big the group is &mdash; four (&alpha;,&beta;) classes are "
    "<b>listable</b> (ord(2) linear in v, so the powers of two are a short "
    "explicit list), and the rest are <b>thin</b> (ord exponential on average, "
    "no elementary handle)."))
story.append(P(
    "<b>Ten machine theorems &mdash; and the two &ldquo;open&rdquo; leads were not open.</b> "
    "The lemma closes both immediately &mdash; (2,1,1,2,&minus;1) because "
    "S<sub>v</sub> = 2&middot;odd cannot meet a signed power of two, and "
    "(3,3,2,0,1) because S<sub>v</sub> &#8801; 0 modulo a divisor of "
    "A<sub>v</sub> where every power of two is a unit &mdash; and a sweep of "
    "the box turns up three more machines the earlier hunt had never seen. "
    "<b>T7 to T11: five more machines that never halt after their first step</b>, "
    "each on an exact integer identity for S<sub>v</sub> confirmed on a second, "
    "independent code path (v &le; 4,000) and brute-forced (0 halts, all "
    "non-power-of-two starts below 20,000). The three strays were hidden not by "
    "a weaker test but by a <b>pool filter</b>: the leads had been drawn from "
    "undecided <i>growers</i>, and two of the three were already "
    "congruence-decided while the third is a machine with a genuine cycle "
    "(F(3) = 3). For the congruence-decided pair this is a real upgrade, from "
    "&ldquo;never halts from x<sub>0</sub> = 3&rdquo; to &ldquo;no orbit from "
    "any start reaches a power of two after a step&rdquo;."))
story.append(P(
    "<b>And then it stops &mdash; provably.</b> For every other machine in the "
    "odd-&beta; box the sweep returns an <b>explicit surviving branch</b>: a "
    "v &le; 22 and the exponent e witnessing 2<super>e</super> &#8801; "
    "S<sub>v</sub> (mod A<sub>v</sub>). <i>672 swept: 10 all-forbidden, 620 "
    "with a surviving-branch certificate, 42 sieve-silent.</i> A surviving "
    "branch is a positive certificate, not a failure to find one, so this is "
    "<b>completeness, not exhaustion</b> &mdash; the first time this program "
    "has closed a method with a completeness statement instead of a budget "
    "(contrast P9 and Section 2.5, where every bound is a spent resource). What "
    "is not claimed: a surviving branch does not make a machine halt; it means "
    "only that this method cannot decide it."))
story.append(P("<b>The frontier map.</b> Of the 636 odd-&beta; machines no "
               "congruence decides:"))
story.append(tab([
    ("1 &mdash; mechanical", "8", "all branches forbidden with a pattern proof "
     "&mdash; the ten, less those decided another way"),
    ("2 &mdash; <b>S-unit</b>", "<b>399</b>", "thin group; the sieve bites but "
     "does not close. <b>The Space Needle is here</b>, with 120 machines "
     "sharing its group"),
    ("3a &mdash; sieve-closed", "164", "listable, but a branch certifiably "
     "survives: the route is provably shut"),
    ("3b &mdash; sieve-void", "24", "thin, forbidden mass 0"),
    ("3c &mdash; sieve-silent", "41", "the (1,&minus;1) class: no expanding "
     "branch at all"),
], ("tier", "count", "what it means"),
   (1.3 * inch, 0.55 * inch, 4.05 * inch)))
story.append(P(
    "<b>The Needle&rsquo;s open problem, in one line.</b> A<sub>v</sub> = "
    "2<super>v+1</super> + 3 forces 2<super>v+1</super> &#8801; &minus;3, so "
    "&#9001;2&#9002; = {&plusmn;3<super>a</super>&middot;2<super>i</super>} and "
    "the condition on branch v is:"))
story.append(P("2v &minus; 3 &nbsp;&#8712;&nbsp; "
               "{&plusmn;3<super>a</super>&middot;2<super>i</super>} "
               "&nbsp;(mod 2<super>v+1</super> + 3)", MATHC))
story.append(P(
    "<i>Verified: exact for v &le; 200; weighted forbidden mass 0.2868, an "
    "independent reproduction of WS3&rsquo;s 28.7%; 19 of the first 35 "
    "valuations forbidden, matching WS3 exactly.</i> <b>It does not close.</b> "
    "The surviving branches to v = 40 are 0, 2, 3, 5, 6, 8, 11, 14, 15, 16, 17, "
    "20, 27, 29, 30, 34, 37, 38 &mdash; 18 of 41, and not thinning. There is no "
    "asymptotic all-branches-forbidden theorem here; the last-step sieve "
    "saturates near 28.7% of weight forever, and whatever decides the Needle "
    "comes from elsewhere. Recorded so the next reader does not repeat the "
    "search."))
story.append(P(
    "<b>Where this leaves the difficulty, and it is a sharper place than "
    "before.</b> The question is now a <b>2,3-S-unit membership problem</b>, "
    "and that is a named object with a literature rather than a private "
    "obstacle. Two placements matter. First, the ten machine theorems are explicit "
    "instances of <b>Skolem&rsquo;s conjecture</b> &mdash; that an unsolvable "
    "exponential Diophantine equation is already unsolvable modulo some witness "
    "&mdash; which means this program&rsquo;s certificate searches have been "
    "Skolem-witness searches all along, and the Bertók&ndash;Hajdu "
    "modulus-construction algorithm is a tool built for exactly this. Second, "
    "the Needle&rsquo;s lifted halting equation is a linear-exponential "
    "Diophantine system of the shape Dong&ndash;Shafrir and "
    "Chistikov&ndash;Mansutti&ndash;Starchak prove decidable &mdash; <i>except</i> "
    "for a single product of a free variable with an exponential, and a modulus "
    "that is not a power of two. <b>The machine sits one syntactic step beyond "
    "the 2026 decidability frontier</b>, which is the most precise answer G3 "
    "has ever had."))
story.append(P(
    "<b>The methodological point, which is the same one as Section 2.10 and "
    "should not have needed repeating.</b> Yesterday&rsquo;s lesson was that "
    "consolidating the open items <i>is</i> a search. Today&rsquo;s is its "
    "sharper form: <b>the leads were closed not by new computation but by "
    "deleting a hypothesis nobody had tested</b>. &ldquo;For &alpha; = 2, "
    "&beta; = &minus;1&rdquo; was written into the lemma because that is where "
    "it was found, not because the proof needed it, and that phrase alone kept "
    "two theorems out of reach for a day and three more out of sight entirely. "
    "The generalisation cost one reading of our own derivation. It is recorded "
    "as a trap in Section 11."))

story.append(P("2.12&nbsp;&nbsp;Two theorems from a zoom-out, and the "
               "refutation of a whole genre of argument", H2))
story.append(P(
    "Section 2.11 left the difficulty stated as a 2,3-S-unit membership "
    "question and the hardness placed one syntactic step beyond the 2026 "
    "decidability frontier. Two follow-ups were commissioned against that "
    "picture: import the Skolem-conjecture machinery that constructs witness "
    "moduli, and prove a counting barrier showing VAL(2) too poor to be "
    "universal. <b>Both failed, and each failure produced something better than "
    "its assignment would have.</b>"))

story.append(P("<b>T12 &mdash; the &delta;-saturation theorem (proved).</b> "
               "WS4 swept every modulus m &le; 20,000 and found no separating "
               "congruence for the Needle &mdash; a bounded resource, and P9 "
               "warns that such results are silent past their budget. An "
               "infinite slice of that sweep is now a proof.", BODY))
story.append(P("Let M be <b>odd</b> with gcd(&delta;, M) = 1 and "
               "gcd(ord<sub>M</sub>(2), M) = 1. Then for <i>every</i> residue c "
               "the one-step image {&phi;<sub>v</sub>(c) : v &ge; 0} is "
               "<b>all of Z<sub>M</sub></b>.", MATHC))
story.append(P(
    "<i>Proof.</i> M odd makes 2<super>v+1</super> invertible, so branch v is a "
    "single affine map &phi;<sub>v</sub>(c) = &mu;<sub>v</sub>c + "
    "a<sub>v</sub>. Restrict to v &#8801; v<sub>0</sub> (mod "
    "ord<sub>M</sub>(2)): there 2<super>v</super> is constant, hence so are "
    "A<sub>v</sub> mod M, &mu;<sub>v</sub> and &gamma;2<super>v</super>. The "
    "only surviving v-dependence is the term &delta;v, so a<sub>v</sub> "
    "&minus; a<sub>v<sub>0</sub></sub> &#8801; &delta;(v &minus; "
    "v<sub>0</sub>). As v runs over v<sub>0</sub> + ord<sub>M</sub>(2)&middot;Z "
    "that difference sweeps the subgroup generated by gcd(ord<sub>M</sub>(2), M) "
    "= 1, i.e. all of Z<sub>M</sub>, and gcd(&delta;, M) = 1 keeps it so. "
    "<b>QED</b>"))
story.append(P(
    "<b>Corollary: no odd prime modulus can ever separate the Space "
    "Needle.</b> &delta; = 1, and ord<sub>p</sub>(2) divides p &minus; 1 makes "
    "the second hypothesis automatic for primes. Not &ldquo;none below the "
    "search bound&rdquo; &mdash; none, unconditionally; and since already the "
    "one-step image from any residue is everything, no branch can even be "
    "excluded. <i>Machine-verified: the proof&rsquo;s steps on 4,000 (machine, "
    "odd M) pairs meeting the hypotheses, 0 violations; end-to-end image = "
    "Z<sub>M</sub> in 265 cases with M &lt; 62 and on the 45 primes below 200, "
    "0 failures; all 549 odd primes below 4,000 satisfy the hypotheses</i> "
    "(<font face='Courier'>census/saturation.py</font>)."))
story.append(P(
    "<b>This sharpens T3&rsquo;s corollary from a remark into a mechanism.</b> "
    "T3 said the v-linear term blocks the <i>cheapest</i> certificate, m = 3. "
    "T12 says &delta; blocks <b>every prime certificate totally, in a single "
    "step</b>, for reasons that have nothing to do with the size of the prime. "
    "A falsifier was run, because a theorem this strong deserves attack: each "
    "of the 318 separating certificates must violate a hypothesis or T12 is "
    "false &mdash; 274 have an even modulus, 44 fail a gcd condition, and "
    "<b>0 would refute</b>. The honest boundary is exactly there: <b>even M is "
    "not covered</b>, 2 is not invertible, and 274 of the 318 certificates live "
    "at even moduli. If a certificate for a hard machine exists at all, that is "
    "where it has to be."))
story.append(P(
    "<b>The congruence criteria at m = 4, 6, 8 (proved).</b> T3 gave a closed "
    "form at m = 3 and nothing was known at the moduli deciding more machines. "
    "Since separation at m depends on the parameters only through their "
    "residues mod m, each criterion is a finite object on (Z<sub>m</sub>)"
    "<super>5</super> and was checked <i>completely</i> rather than sampled: "
    "<b>C4</b> is &ldquo;&beta; even and 2&alpha;+&beta;+&gamma;+&epsilon; "
    "&#8801; 3 (mod 4)&rdquo;; <b>C6</b> is a four-case disjunction one of "
    "whose cases is T3 itself; <b>C8</b> reduces to the forward orbit of 3 "
    "under an explicit four-node map. <i>C4 on all 1,024 tuples mod 4 and C6 on "
    "all 7,776 mod 6: 0 mismatches. Against the census, all 1,077 machines: 41, "
    "105 and 68 predicted and decided, 0 discrepancies in either direction.</i> "
    "A by-product of getting this exact: the deciding-modulus list in the "
    "census results had <b>omitted m = 7</b> and its three machines, which is "
    "why its counts never reconciled."))
story.append(P(
    "<b>Why the Skolem import failed, and why the failure was worth it.</b> "
    "Bert&oacute;k&ndash;Hajdu&rsquo;s class admits only <i>exponents</i> as "
    "unknowns. Our halting equation A<sub>v</sub>k + B<sub>v</sub> = "
    "2<super>E</super> carries k linearly and every open machine carries v "
    "linearly through &delta;v; reducing mod A<sub>v</sub> eliminates k and is "
    "an <i>equivalence</i>, so our local-to-global step is a theorem with a "
    "<b>forced</b> modulus rather than a conjecture with a searched one. Run on "
    "16 known-forbidden branches their algorithm returns a power of two every "
    "time and never A<sub>v</sub>: it certifies &ldquo;B<sub>v</sub> is not a "
    "power of two&rdquo; where we need &ldquo;not a power of two <i>mod "
    "A<sub>v</sub></i>&rdquo;. Skolem stays a good orienting remark and is not "
    "a tool. But asking <i>why no witness modulus exists</i> instead of "
    "<i>which one works</i> is what produced T12."))

story.append(P("<b>The barrier, and the far more useful thing that replaced "
               "it.</b> <b>Theorem R (proved):</b> branch v sends every "
               "non-halting input to the same valuation iff "
               "v<sub>2</sub>(B<sub>v</sub>) &lt; v<sub>2</sub>(A<sub>v</sub>), "
               "and then that valuation is v<sub>2</sub>(B<sub>v</sub>). "
               "<b>T13 (proved):</b> if that holds at every v, the branch "
               "sequence is fixed <i>independently of the state</i>, so the "
               "orbit is a periodic composition of affine maps with closed form "
               "x<sub>n</sub> = c&lambda;<super>n</super> + d &mdash; such a "
               "machine does no state-dependent branching and cannot carry a "
               "computation. <i>Machine-verified: 2,351 of 19,092 machines, "
               "12.31%, all with &beta; even</i> "
               "(<font face='Courier'>formal/ws4/rigidity.py</font>).", BODY))
story.append(P(
    "<b>The counting barrier itself is refuted.</b> The plan was: (A<sub>v</sub>,"
    " B<sub>v</sub>) mod M depends on v only through (2<super>v</super> mod M, "
    "v mod M), so the branch table is eventually periodic in v &mdash; while a "
    "Conway reduction mod M needs M independent affine pieces. The periodicity "
    "is true; the conclusion is false. Measured <i>bandwidth</i>, the number of "
    "distinct (A<sub>v</sub>, B<sub>v</sub>) mod M actually achieved, is at "
    "least M for every modulus tested: 100 at M = 23, 412 at M = 101, 1,036 at "
    "M = 257. VAL(2) supplies at least as many branch behaviours as such a "
    "reduction consumes."))
story.append(P("<b>Universality is a property of a single point, not of a "
               "family.</b>", MATHC))
story.append(P(
    "That sentence retires the entire genre. A 5-parameter family of dimension "
    "5 inside a 2V-dimensional space of branch tables can still contain a "
    "universal machine, because a universal machine is a <b>0-parameter "
    "object</b>. Every argument of the form <i>too few degrees of freedom</i>, "
    "<i>rank at most 5</i>, <i>density M<super>5&minus;2V</super></i>, "
    "<i>bandwidth too small</i> is answering a question nobody asked &mdash; "
    "including the composite-step version, where the dimension bound survives "
    "at 5 for every step count and is equally useless. A real barrier needs a "
    "property shared by <i>every point</i>. Two exist: Theorem R, which holds "
    "only on the &beta;-even slice; and the slope spectrum s<sub>v</sub> = "
    "&alpha; + &beta;2<super>&minus;(v+1)</super>, giving at most "
    "floor(log<sub>2</sub>(|&beta;|/&rho;)) branches pairwise "
    "&rho;-separated &mdash; so k separated branches cost |&beta;| &ge; "
    "&rho;2<super>k&minus;1</super>. That is an <b>exponential compression "
    "bound, not an impossibility</b>, and saying so is the honest end of the "
    "line."))
story.append(P(
    "<b>Where universality now stands.</b> Q1 &mdash; does some single member "
    "have an undecidable halting set &mdash; is <b>untouched</b>; the 12.31% "
    "slice is decided <i>because</i> it is trivial. Q2, the parametrized "
    "problem, is <b>narrowed three ways and not settled</b>: the rigid slice is "
    "computation-free, branch-index-preserving one-step simulation of "
    "FRACTRAN/RES is impossible (the forced &alpha;, &beta; come out "
    "non-integral for PRIMEGAME and for both WS4-compiled machines), and "
    "confinement to v &#8712; {0,1}, wherever it can be certified, collapses "
    "the machine <i>below</i> the 3x+1 shape onto a closed-form recurrence "
    "instead of onto it. Untouched: the <b>&beta;-odd half</b>, where both "
    "flagship machines live and the control graph on valuations is complete. "
    "Every negative here is one-step and branch-index-preserving, so the live "
    "direction is multi-step / return-map simulation on that half."))
story.append(P(
    "<b>The pattern is now three for three, and it is the finding.</b> "
    "Consolidating the board closed three leads (Section 2.10); deleting an "
    "untested hypothesis closed five more and finished a method (Section 2.11); "
    "and here, two commissioned imports both failed while their failures "
    "produced a theorem and a genre-level refutation. <b>In none of the three "
    "cases did new computation produce the result.</b> What produced it each "
    "time was re-reading what the program already had, with the specific "
    "question &ldquo;what does this actually depend on?&rdquo;. Recorded as a "
    "trap in Section 11."))

story.append(P("2.13&nbsp;&nbsp;The even half: what an even modulus actually "
               "buys, and why &beta; odd cannot buy it", H2))
story.append(P(
    "T12&rsquo;s falsifier located its own gap in one line: <b>274 of the 318 "
    "separating certificates live at even moduli</b>, so if a certificate for a "
    "hard machine exists at all, that is where it has to be. Closing that half "
    "turned out to need one observation about what evenness is <i>for</i>."))
story.append(P(
    "Write M = 2<super>s</super>M&rsquo; with M&rsquo; odd. A source residue c "
    "mod M with v<sub>2</sub>(c) = v &lt; s <b>pins the branch index v "
    "exactly</b> &mdash; the low bits of the value <i>are</i> the valuation. "
    "That is precisely the information Section 2.12 proves an odd modulus can "
    "never have, and it is the whole of what an even modulus is spending. For "
    "v &ge; s the source is 0 mod 2<super>s</super>, every branch v &ge; s "
    "becomes available at once, and the odd part is back in T12&rsquo;s "
    "situation. Which immediately says where the escape hatch is: on such a "
    "source the multiplier k is <b>free</b> mod 2<super>s</super> (it is pinned "
    "only mod M&rsquo;), and since v &ge; s,"))
story.append(P("target = A<sub>v</sub>k + B<sub>v</sub> &#8801; &beta;k + "
               "&delta;v + &epsilon; &nbsp;(mod 2<super>s</super>)", MATHC))
story.append(P(
    "<b>&beta; odd makes &beta;k sweep all of Z<sub>2<super>s</super></sub>, and "
    "the 2-adic information is destroyed in a single step. &beta; even leaves "
    "only the subgroup generated by gcd(&beta;, 2<super>s</super>) &mdash; the "
    "hatch stays open.</b> So the census&rsquo;s oldest empirical fact, that "
    "&beta; parity is what makes a member hard, is not a statistical tendency: "
    "it is this mechanism."))
story.append(P("<b>T14 &mdash; even-modulus saturation (proved).</b> Let "
               "M = 2<super>s</super>M&rsquo; with M&rsquo; odd, and suppose "
               "(i) &beta; odd; (ii) gcd(&delta;, M&rsquo;) = 1; (iii) "
               "gcd(ord<sub>M&rsquo;</sub>(2), M&rsquo;) = 1; (iv) the closure "
               "of x<sub>0</sub> contains some c<sub>0</sub> &#8801; 0 (mod "
               "2<super>s</super>). Then that closure is <b>all of "
               "Z<sub>M</sub></b> &mdash; no separation, and no branch can be "
               "excluded either.", BODY))
story.append(P(
    "<i>Proof.</i> Splitting the source congruence by CRT: mod 2<super>s</super> "
    "it holds identically, so k is unconstrained there; mod M&rsquo; the factor "
    "2<super>v+1</super> is invertible, so k is determined. Since v + 1 &gt; s, "
    "A<sub>v</sub> &#8801; &beta; and B<sub>v</sub> &#8801; &delta;v + "
    "&epsilon;, and &beta; is a unit &mdash; so the 2-adic component of the "
    "targets sweeps everything while the M&rsquo;-component sits at "
    "&mu;<sub>v</sub>c<sub>0</sub>&rsquo; + a<sub>v</sub>. Taking the union over "
    "v &ge; s, those components run over T12&rsquo;s set restricted to v &ge; s, "
    "which costs nothing because each class mod ord<sub>M&rsquo;</sub>(2) still "
    "contains infinitely many such v. <b>QED</b> <i>Machine-verified: the "
    "mechanism on 502 residues (s = 1 to 8); the three proof steps on 3,000 "
    "instances, 0 failures each; the conclusion on 7,840 (&beta;-odd machine, "
    "even modulus) pairs, closure not all of Z<sub>M</sub> in 0</i> "
    "(<font face='Courier'>census/even_saturation.py</font>)."))
story.append(P(
    "<b>The falsifier is the most persuasive part, because the census confirms "
    "the mechanism without being asked.</b> Every even-modulus certificate must "
    "break a hypothesis or T14 is false: <b>267 have &beta; even</b> &mdash; "
    "they are buying exactly the hatch &mdash; <b>7 have &delta; = 0</b> and so "
    "fail (ii) outright, and <b>0 would refute</b>."))
story.append(P(
    "<b>T14&rsquo; &mdash; the sharp form, and it is an equivalence.</b> "
    "Hypothesis (iii) is far from necessary, and the exact condition is cheap "
    "once two simplifications are made. Mod M&rsquo;, "
    "&mu;<sub>v</sub>2<super>v</super> = A<sub>v</sub>/2, so a<sub>v</sub> = "
    "B<sub>v</sub> &minus; A<sub>v</sub>/2 = (&gamma;&minus;&alpha;)"
    "2<super>v</super> + &delta;v + (&epsilon; &minus; &beta;/2) and "
    "&mu;<sub>v</sub> = &alpha; + &beta;/2<super>v+1</super> &mdash; no hidden "
    "v-dependence at all. Writing v = v<sub>0</sub> + j&middot;ord, everything "
    "but &delta;v is constant on the class, so &phi;<sub>v</sub>(c) = "
    "&phi;<sub>v<sub>0</sub></sub>(c) + &delta;&middot;ord&middot;j, which sweeps "
    "the subgroup generated by g := gcd(ord, M&rsquo;). The reachable set is "
    "therefore a union of at most ord cosets of that subgroup, and "
    "Z<sub>M&rsquo;</sub> has exactly g of them:"))
story.append(P("the closure is all of Z<sub>M&rsquo;</sub> &nbsp;<b>iff</b>&nbsp; "
               "the ord base points cover all g cosets", MATHC))
story.append(P(
    "&mdash; decidable per (machine, modulus) in O(ord) work, with (iii) exactly "
    "its trivial case g = 1. <i>Verified: both simplifications and the "
    "equivalence on 4,000 (machine, M&rsquo;) instances, 0 violations and 0 "
    "mismatches; and it accounts for all 6,720 &beta;-odd cases at moduli (iii) "
    "does not reach.</i>"))
story.append(P(
    "<b>What is now proved, and what is only reduced &mdash; the distinction "
    "matters here more than usual.</b> &beta; = 3 is odd and &delta; = 1, so (i) "
    "and (ii) hold for the Needle at every modulus. With T12 that gives: <b>no "
    "modulus whose odd part satisfies gcd(ord<sub>M&rsquo;</sub>(2), M&rsquo;) = "
    "1 can separate the Space Needle, odd or even, with no upper bound on "
    "M</b> &mdash; <b>12,916 of the 19,999 moduli below 20,000, 64.58%</b>, by a "
    "one-line gcd test where WS4 had only a computation. The remaining third is "
    "covered by T14&rsquo; in every case tested, but T14&rsquo; is a "
    "<i>per-modulus test rather than a closed form</i> in the parameters. So "
    "&ldquo;no modulus whatever separates the Needle&rdquo; is now <b>reduced to "
    "a coset-covering statement, not proved</b>. A descent is visible &mdash; "
    "g<sub>1</sub> := gcd(ord<sub>g</sub>(2), g) is strictly smaller than g "
    "whenever g &gt; 1, so the condition recurses on a smaller modulus &mdash; "
    "but making that a proof needs the base points controlled at every level, "
    "and that is not done. The gap is named rather than papered over."))
story.append(P(
    "<b>What this changes about the program&rsquo;s own position.</b> The "
    "uncomfortable summary in Section 2.10 was that every positive result is "
    "about machines that are not hard and every result about the hard ones is "
    "negative. T12 and T14 do not overturn it &mdash; but they change the "
    "<i>kind</i> of negative available, from a spent budget to an unconditional "
    "theorem covering infinitely many moduli. That is the first time the "
    "program has said something with no upper bound about the flagship machine "
    "itself, and it is what G3 was written to want."))

story.append(P("2.14&nbsp;&nbsp;The descent closes: no modulus separates the "
               "Space Needle", H2))
story.append(P(
    "Sections 2.12 and 2.13 both carried the hypothesis "
    "gcd(ord<sub>M&rsquo;</sub>(2), M&rsquo;) = 1, which covered 64.58% of the "
    "moduli below 20,000 and was known to be conservative. <b>It was never "
    "needed.</b> What exposed that is worth stating, because it is a "
    "methodological point as much as a mathematical one: the proof used a "
    "<i>single</i> step from c<sub>0</sub>, but the object being bounded is a "
    "<b>closure</b>, so composition is free. Testing two composed steps on the "
    "uncovered moduli returned something better than expected &mdash; the "
    "<i>one-step</i> image was already all of Z<sub>M&rsquo;</sub> in every one "
    "of 6,336 cases. The coset analysis had simply been too pessimistic."))
story.append(P("<b>Descent lemma.</b>&nbsp;&nbsp;M odd with gcd(&delta;, M) = 1 "
               "&nbsp;&#8658;&nbsp; the one-step image {&phi;<sub>v</sub>(c) : "
               "v &ge; 0} is all of Z<sub>M</sub>, with no condition on "
               "ord<sub>M</sub>(2)", MATHC))
story.append(P(
    "<i>Proof.</i> Put g<sub>0</sub> = M and g<sub>j+1</sub> = "
    "gcd(ord<sub>g<sub>j</sub></sub>(2), g<sub>j</sub>), and let I<sub>j</sub> be "
    "the image in Z<sub>g<sub>j</sub></sub>. <b>(1)</b> For odd g &ge; 3, "
    "ord<sub>g</sub>(2) &le; &lambda;(g) &lt; g, so g<sub>j+1</sub> &lt; "
    "g<sub>j</sub> strictly and the chain reaches 1. <b>(2)</b> Mod g<sub>j</sub> "
    "with h = ord<sub>g<sub>j</sub></sub>(2): on a class v &#8801; w (mod h) the "
    "quantity 2<super>v</super> is constant, so &mu;<sub>v</sub> and the "
    "(&gamma;&minus;&alpha;)2<super>v</super> term are constant and the only "
    "surviving v-dependence is &delta;v &mdash; and since v runs over an "
    "<i>infinite</i> progression w + hZ, that term sweeps the <b>full</b> "
    "subgroup &#9001;g<sub>j+1</sub>&#9002;. So I<sub>j</sub> is a union of h "
    "cosets of &#9001;g<sub>j+1</sub>&#9002;, and reducing the whole image mod "
    "g<sub>j+1</sub> annihilates those shifts and leaves exactly the base "
    "points: <b>I<sub>j</sub> = Z<sub>g<sub>j</sub></sub> if and only if "
    "I<sub>j+1</sub> = Z<sub>g<sub>j+1</sub></sub></b>. <b>(3)</b> At the last "
    "level g<sub>k</sub> = 1 and I<sub>k</sub> is trivially full; walking the "
    "equivalences back up gives I<sub>0</sub> = Z<sub>M</sub>. <b>QED</b>"))
story.append(P(
    "<b>The point the first attempt missed</b> is that the shifts sweep a "
    "<i>full</i> subgroup precisely because v ranges over infinitely many "
    "integers. Restricting v to one period &mdash; which is what a finite search "
    "does, and what the conservative hypothesis silently assumed &mdash; loses "
    "exactly that. <i>Machine-verified: 2,500 (machine, odd M, c) instances with "
    "gcd(&delta;,M) = 1, of which <b>708 have gcd(ord<sub>M</sub>(2), M) &gt; "
    "1</b> &mdash; precisely the cases the hypothesis excluded &mdash; and the "
    "one-step image failed to be all of Z<sub>M</sub> in <b>0</b>; the chain "
    "descends strictly for every odd g &lt; 6,000, longest chain 7</i> "
    "(<font face='Courier'>census/descent.py</font>)."))
story.append(P(
    "<b>So both theorems lose the hypothesis, and the corollary is the one the "
    "program has been trying to reach for weeks.</b> T12 becomes: M odd with "
    "gcd(&delta;, M) = 1 gives no separation. T14 becomes: M = 2<super>s</super>"
    "M&rsquo; with &beta; odd, gcd(&delta;, M&rsquo;) = 1 and 2-adic reach gives "
    "no separation. And since the Space Needle has &beta; = 3 odd and "
    "&delta; = 1, so that gcd(&delta;, M&rsquo;) = 1 at <i>every</i> modulus:"))
story.append(P("<b>No modulus separates the Space Needle</b> &mdash; odd or "
               "even, with no upper bound and no arithmetic side condition",
               MATHC))
story.append(P(
    "<i>Machine-verified: every modulus 2 to 400, closure is all of "
    "Z<sub>M</sub> in every case and 0 separate. Falsifier: of the 318 "
    "certificates, 267 fail &ldquo;&beta; odd&rdquo;, 51 fail the gcd condition, "
    "0 fail 2-adic reach, and <b>0 are explained by the dropped hypothesis "
    "alone</b>.</i>"))
story.append(P(
    "<b>What is still a hypothesis, stated plainly.</b> 2-adic reach &mdash; "
    "that the closure contains some residue &#8801; 0 (mod 2<super>s</super>) "
    "&mdash; is <i>verified, not proved</i> (8,512 &beta;-odd &times; "
    "even-modulus cases, 0 failures). It is a condition on the closure rather "
    "than on the parameters, so it is decidable per (machine, modulus); but "
    "&ldquo;decidable for each M&rdquo; is not &ldquo;true for all M&rdquo;, and "
    "that is exactly the distinction this program does not paper over. <b>The "
    "honest summary: the arithmetic side is closed; one reachability hypothesis "
    "remains.</b>"))
story.append(P(
    "<b>What this settles.</b> The congruence-certificate question for the "
    "flagship &mdash; open since WS4&rsquo;s sweep, and answered until now only "
    "by &ldquo;nothing below 20,000&rdquo; &mdash; is now answered by a theorem. "
    "Section 2.13 observed that T12 and T14 changed the <i>kind</i> of negative "
    "available, from a spent budget to an unconditional statement; this "
    "completes that change on the arithmetic side. The Needle&rsquo;s "
    "resistance to congruences is no longer an experimental fact about a search "
    "range. It is a consequence of &delta; &ne; 0, and the mechanism is exactly "
    "the one T3 pointed at in a single line months earlier."))

story.append(P("2.15&nbsp;&nbsp;The reach lemma: the last hypothesis falls",
               H2))
story.append(P(
    "Section 2.14 ended with one verified-but-unproved hypothesis: <b>2-adic "
    "reach</b>, that the closure contains a residue divisible by "
    "2<super>s</super>. It is now proved, from &beta; odd alone, and in a "
    "stronger form: not just some closure element but <b>the actual orbit of a "
    "suitably chosen lift</b>."))
story.append(P("<b>Reach lemma.</b>&nbsp;&nbsp;&beta; odd, A<sub>v</sub> &gt; 0: "
               "for every residue c mod M = 2<super>s</super>M&rsquo; there is "
               "a lift x &#8801; c whose F-orbit reaches a value &#8801; 0 "
               "(mod 2<super>s</super>) within s + 1 steps", MATHC))
story.append(P(
    "<i>Proof idea &mdash; the exponent ledger.</i> Choose x = c + "
    "2<super>s</super>M&rsquo;T with T a free integer and iterate F "
    "<i>exactly</i>. The T-dependence stays affine, y<sub>n</sub> = "
    "p<sub>n</sub> + q<sub>n</sub>T, and each step spends v<sub>n</sub> + 1 "
    "bits of the coefficient&rsquo;s 2-adic valuation: e<sub>n+1</sub> = "
    "e<sub>n</sub> &minus; (v<sub>n</sub> + 1) &mdash; the same precision "
    "accounting that the confinement analysis of Section 2.12 met from the "
    "other side. Two events are exhaustive: either some p<sub>n</sub> is "
    "divisible by 2<super>e<sub>n</sub></super>, and solving one congruence "
    "for T lands y<sub>n</sub> on 0 mod 2<super>s</super>; or the ledger "
    "reaches zero, the multiplier k becomes a <i>unit times T</i>, and "
    "&beta; odd (A<sub>v</sub> odd) makes the next value sweep every residue. "
    "While neither has fired, v<sub>n</sub> &lt; e<sub>n</sub> keeps the "
    "branch sequence T-independent, and the ledger strictly decreases from "
    "s &minus; 1, so the process ends within s + 1 steps. &beta; odd is used "
    "exactly twice: the A&rsquo;s never feed the ledger, and the final free "
    "multiplier is a unit. <i>Machine-verified constructively: 4,000 (machine, "
    "modulus, residue) instances &mdash; the recipe&rsquo;s witness lift was "
    "built and its orbit run, reaching 0 mod 2<super>s</super> every time, "
    "deepest hit 9 steps; the ledger bookkeeping checked in isolation on "
    "3,000 chains, 0 violations</i> "
    "(<font face='Courier'>census/reach.py</font>)."))
story.append(P(
    "<b>T15 &mdash; the no-certificate theorem, final form.</b> &beta; odd, "
    "A<sub>v</sub> &gt; 0, gcd(&delta;, M&rsquo;) = 1 &#8658; the closure of "
    "<i>every</i> residue is <i>all</i> of Z<sub>M</sub>: no modulus "
    "separates, no branch can be excluded. Assembly: odd M is the descent "
    "lemma alone; even M is reach + the T14 argument. <i>Verified: 7,616 "
    "(machine, modulus) pairs, closure short of Z<sub>M</sub> in 0; falsifier "
    "&mdash; &beta;-even machines with even-modulus certificates are exactly "
    "where reach fails, confirming the hypothesis is load-bearing.</i>"))
story.append(P(
    "<b>Corollary. No modulus separates the Space Needle &mdash; and there "
    "are no hypotheses left.</b> &beta; = 3 odd, &delta; = 1, A<sub>v</sub> = "
    "2<super>v+1</super> + 3 &gt; 0. The question &ldquo;is there a "
    "congruence certificate for the Needle?&rdquo;, open since WS4 swept "
    "m &le; 20,000, is closed: <b>there is none</b>, and the reason is "
    "&delta; = 1 and &beta; odd &mdash; exactly the two parameters T3 flagged "
    "on the census&rsquo;s first day. What began as &ldquo;the v-linear term "
    "blocks the cheapest certificate&rdquo; is now, five theorems later, "
    "&ldquo;the v-linear term blocks every certificate, and here is the "
    "mechanism at every modulus&rdquo;."))

story.append(P("2.16&nbsp;&nbsp;The transfer back to base q: machine 3 "
               "joins, and the sibling split is explained", H2))
story.append(P(
    "Every theorem of Sections 2.11 to 2.15 was proved on the base-2 census "
    "family, and none of the proofs used base 2 in any essential way &mdash; "
    "which was a claim until July 30 and is now a verified fact. The transfer "
    "target is <b>machine 3</b>, the base-3 flagship: its return map is the "
    "base-3 member of the (&alpha;,&beta;) = (1,1) class, with branch table "
    "A<sub>j</sub> = 3<super>j+1</super> + 1, B<sub>(j,r)</sub> = "
    "r&middot;3<super>j</super> + j + c<sub>r</sub> &mdash; in census "
    "coordinates &gamma; = r (the leading digit), <b>&delta; = 1</b> (the "
    "divide-chain length enters the value), &epsilon;<sub>r</sub> = r + 2 "
    "&mdash; and halting set {27<super>k</super>}. <i>Verified against the raw "
    "two-variable rules: 59,988 non-spine values, 0 mismatches; spine "
    "behaviour (halt iff 3 | j) exact</i> "
    "(<font face='Courier'>machine3/m3_nocert.py</font>, an independent "
    "re-derivation of the transfer analysis)."))
story.append(P(
    "<b>The base-q universal sieve lemma.</b> For machine 3 the fixed-point "
    "reduction is even cleaner than in base 2: Q<sub>0</sub> = "
    "3<super>j+1</super> &minus; A<sub>j</sub> = &minus;1 exactly, and "
    "3<super>j+1</super> &#8801; &minus;1 (mod A<sub>j</sub>) collapses the "
    "sieve to <b>h &#8801; B<sub>(j,r)</sub> (mod A<sub>j</sub>) for some "
    "h &#8712; {27<super>k</super>}</b> &mdash; the invariant content of the "
    "base-2 form S<sub>v</sub> &#8801; 2B<sub>v</sub> was always "
    "&ldquo;target &#8801; B&rdquo;, with the 2 a normalization artifact. The "
    "class relation makes &#9001;3&#9002; = {&plusmn;3<super>i</super>} a "
    "short list, and the gap argument closes every branch except j = 1. "
    "<i>Verified: lemma verdict against the project&rsquo;s own "
    "geometric_solver on 50 branches, 0 mismatches; survivors exactly (1,1) "
    "and (1,2), with genuine halting witnesses 21 &rarr; 27 and 478293 &rarr; "
    "27<super>4</super> run on the raw rules.</i>"))
story.append(P(
    "<b>M3-N1 &mdash; no modulus separates machine 3 (proved).</b> The whole "
    "chain &mdash; &delta;-saturation, descent, reach, assembly &mdash; "
    "transfers with 2 &rarr; 3, &ldquo;odd M&rdquo; &rarr; &ldquo;M coprime "
    "to 3&rdquo;, &ldquo;&beta; odd&rdquo; &rarr; &ldquo;&beta; coprime to "
    "3&rdquo;, ledger bits &rarr; trits: machine 3 has &delta; = 1 and "
    "&beta; = 1, so for every modulus M the closure of every residue is all "
    "of Z<sub>M</sub>. WS4&rsquo;s bounded sweeps for machine 3 become an "
    "unconditional statement. <i>Verified independently: every modulus "
    "M = 2..250, three start residues each &mdash; closure short of "
    "Z<sub>M</sub> in 0 cases.</i> A correction rides along: explorations "
    "Finding 3&rsquo;s informal argument (&ldquo;the valuation is invisible "
    "mod M, hence no congruence certificate&rdquo;) proves too much &mdash; "
    "44 of the census&rsquo;s 318 certificates live at odd moduli where the "
    "valuation is equally invisible. The true mechanism is relational "
    "saturation, which genuinely needs &delta; and &beta;."))
story.append(P(
    "<b>M3-N2 &mdash; the last two steps before any halt have v<sub>3</sub> "
    "= 1, for every j (proved).</b> Previously machine-verified to j &le; "
    "500; now closed by the same gap pattern one level deeper (a parity lemma "
    "kills even j; for odd j &ge; 5 the depth-2 targets sit strictly inside "
    "the gaps of {&plusmn;3<super>i</super>}; small j checked exactly). The "
    "excluded-pair frequency is now exact: 1 &minus; (2/9)<super>2</super> = "
    "77/81 = 95.0617%. Machine 3&rsquo;s sieve pipeline is <b>complete at "
    "depths 1 and 2</b>: every branch either carries an all-j exclusion "
    "theorem or an explicit halting witness."))
story.append(P(
    "<b>Why machine 3 is on the theorem side and the Needle is not &mdash; "
    "the split is one class parameter.</b> Both have &delta; = 1 and &beta; "
    "coprime to the base, so both get the no-certificate theorem. The "
    "difference is the <b>rank of the sieve group</b>: machine 3&rsquo;s "
    "(1,1) class has q<super>j+1</super> &#8801; &minus;1, ord = 2(j+1), "
    "&#9001;q&#9002; = {&plusmn;q<super>i</super>} &mdash; listable, rank 1, "
    "and the gap argument closes everything it meets. The Needle&rsquo;s "
    "(1,3) class has &#9001;2&#9002; = {&plusmn;3<super>a</super>"
    "2<super>i</super>} &mdash; thin, rank 2, the S-unit frontier. <b>A class "
    "property, not a machine accident</b> &mdash; and the sharpest form yet "
    "of the program&rsquo;s oldest observation, that the two flagships behave "
    "differently under every congruence-flavoured tool."))
story.append(P(
    "<b>Fenrir and the Hydra family do not take the transfer, and the "
    "obstruction is structural</b>: their branch modulus is constant (A = 5, "
    "A = 3), there is no valuation-indexed branch family for the "
    "&delta;-sweep to sweep, and halting is a <i>path-counter</i> condition, "
    "not a value condition &mdash; so the sieve lemma has no object to apply "
    "to. Their no-congruence conclusion was already delivered by the q-adic "
    "branch-memory theorem (Section 5.4) through an entirely different "
    "mechanism. Recorded as an obstruction, not a failure: the interface "
    "boundary of the week&rsquo;s toolkit is now mapped exactly &mdash; "
    "valuation-indexed branch families with a value-condition halting set, "
    "any base."))

story.append(P("2.17&nbsp;&nbsp;Leaving the Needle: a second wild cryptid, "
               "and three corrections", H2))
story.append(P(
    "By July 30 the program had become a study of one machine. Every theorem "
    "of Sections 2.11&ndash;2.16 was aimed at the Space Needle, and the "
    "paper&rsquo;s own threats-to-validity section said so. July 31 was spent "
    "on machines that are not the Needle. Three machines were taken up, and "
    "all three gave new theorems (the sheep machine, machine 1, machine 4). "
    "Three "
    "statements this document previously asserted turned out to be wrong: "
    "the mod-16 theorem for machine 1, the taxonomy row for machine 4, and "
    "the claim in Section 6 that the halting-risk sum converges for every "
    "machine in the collection."))
story.append(P(
    "<b>The sheep machine &mdash; the second cryptid inside the interface.</b> "
    "<font face='Courier'>1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE</font>, a "
    "BB(6) machine found by <i>sheep</i> on 7 April 2026 and listed as a "
    "bbchallenge Cryptid, has a published one-variable reduction "
    "f(n) = HALT if oddPart(n) = 1; n + v<sub>2</sub>(n) + 3 if oddPart(n) = "
    "3; n + v<sub>2</sub>(n) + (oddPart(n)&minus;1)/2 otherwise, from n = 5. "
    "Its generic branch <b>is census member (1,1,1,1,0)</b> &mdash; the "
    "Needle&rsquo;s reduction is (1,3,1,1,0), so the two machines differ in "
    "&beta; alone, which is exactly the parameter Section 2.16 says should "
    "decide whether the last-step sieve closes. <i>Verified: 15,920 "
    "systematic and 200,000 random (v,k) pairs to v &lt; 200, k &lt; "
    "10<super>30</super>, 0 mismatches; f differs from the census member on "
    "exactly the values with oddPart = 3 and nowhere else.</i>"))
story.append(P(
    "<b>It closes, and the prediction was on the record first.</b> Reducing "
    "the halting condition modulo A<sub>v</sub> = 2<super>v+1</super> + 1 "
    "(where 2<super>v+1</super> &#8801; &minus;1 and 2<super>&minus;1</super> "
    "&#8801; 2<super>v</super> + 1) turns the sieve into "
    "<b>2<super>t+1</super> &#8801; 2v &minus; 1 (mod 2<super>v+1</super> + "
    "1)</b>, and &#9001;2&#9002; is contained in the list "
    "{2<super>i</super>} &#8746; {A<sub>v</sub> &minus; 2<super>i</super>}, "
    "i &le; v. Two lines of gap argument then give: <b>only v = 0 and v = 1 "
    "can immediately precede a halt; every v &ge; 2 is forbidden (proved).</b> "
    "The wiki states this as a lemma with the threshold &ldquo;a &ge; 2&rdquo; "
    "assumed; here the threshold is the conclusion and the two survivors are "
    "located at the same time. The exceptional oddPart = 3 branch is closed "
    "too (3&middot;2<super>a</super> + a + 3 lies strictly between "
    "3&middot;2<super>a</super> and 2<super>a+2</super> for a &ge; 3). "
    "Together these give the halting set in <b>closed form</b>: H = "
    "{2<super>i</super>} &#8746; {(2<super>2j+1</super>+1)/3} &#8746; "
    "{2(2<super>4j</super>&minus;1)/5}, matched exactly against brute force "
    "below 300,000. <b>The Needle has no such closed form</b> &mdash; its "
    "surviving branch set is infinite and only sieved to density 0.71."))
story.append(P(
    "So the sheep machine is a cryptid whose <b>last-step analysis is closed "
    "and whose orbit question is open</b>; the Needle is one where both are "
    "open. That is the rank-of-sieve-group dichotomy of Section 2.16 "
    "confirmed on a machine this program did not construct, in the direction "
    "predicted before anyone looked. T15 still applies (&beta; = 1 odd, "
    "&delta; = 1), so no modulus separates it either &mdash; <i>verified for "
    "every M &le; 200</i>. And one small finding with a large moral: census "
    "member (1,1,1,1,0) <b>halts</b>, at 3 &rarr; 4, and the sheep "
    "machine&rsquo;s exceptional branch intercepts exactly that value. <b>One "
    "extra branch on one odd part converts a halting census member into an "
    "open problem</b> &mdash; the sharpest available answer to what a "
    "manufactured census misses about machines found in the wild."))
story.append(P(
    "<b>Machine 1: the congruence question, closed &mdash; and an erratum.</b> "
    "The oldest case file was revisited with the census machinery. "
    "<b>T16 (proved)</b>, a machine-independent saturation lemma: if "
    "gcd(&delta;,M) = gcd(&rho;,M) = 1 then the closure of any residue under "
    "c &rarr; Ac + &delta;n + &epsilon; + &kappa;&rho;<super>n</super> is all "
    "of Z<sub>M</sub> &mdash; no hypothesis on A, none on &kappa;. This is "
    "the descent of Section 2.14 stripped of the VAL(2) branch schema "
    "entirely. <b>M1-D (proved)</b>: the dominant branch word&rsquo;s closed "
    "form F(D) = 16D &minus; 240&middot;2<super>n</super> + 32n + 169 "
    "<i>and its exact domain</i> 16&middot;2<super>n</super> &minus; 2n "
    "&minus; 10 &le; D &le; 20&middot;2<super>n</super> &minus; 2n &minus; 13, "
    "both derived rather than fitted. Since that interval has length "
    "4&middot;2<super>n</super> &minus; 2 it contains a complete residue "
    "system mod M as soon as 2<super>n</super> &ge; (M+2)/4, so the true "
    "edge relation contains T16&rsquo;s: <b>M1-N1 &mdash; no odd modulus "
    "separates machine 1 (proved)</b>, already from the single dominant "
    "branch. <i>Verified for every odd M &le; 401 plus 25 random odd M &lt; "
    "1200.</i>"))
story.append(P(
    "With the 2-adic side this closes the question completely: the odd "
    "direction carries <b>no</b> congruence information and the 2-adic "
    "direction carries <b>exactly one class, 9 (mod 16)</b> &mdash; the "
    "dominant branch alone pins the closure to 25 (mod 32) for every "
    "e &ge; 5, and the other branches restore the second lift, so no "
    "2<super>e</super> says more than mod 16 does. Machine 1 is the first "
    "case-file machine on the <b>&beta;-even</b> side of the parity "
    "dichotomy. <b>Erratum.</b> The mod-16 note&rsquo;s universal claim "
    "&mdash; &ldquo;for every non-halting D, F(D) &#8801; 9 (mod 16)&rdquo; "
    "&mdash; is <b>false</b>: F(5) = 17. A trace of the anchor map finds "
    "<b>four</b> producers of a b = 1 anchor, not two; the closed forms force "
    "9 (mod 16) for only two of them, and both others do fire (the flat pump "
    "once, at D = 5; the &ldquo;two&rdquo; exit six times, all compliant but "
    "only forced into 1 mod 4) over 2 &le; D &lt; 400,000. The <i>orbit</i> "
    "corollary is untouched, since 5 is not on the orbit of 17."))
story.append(P(
    "<b>Machine 4: a 2-adic theorem, and a genre correction that this "
    "document needs.</b> Rewriting the rules with a = 2k+1 substituted out "
    "makes two confinements visible. <b>Every interior state has a &#8801; 3 "
    "(mod 4) (proved)</b>; and <b>every interior state with a &#8801; 7 "
    "(mod 8) has b odd (proved)</b>, because only the two small-b rules can "
    "produce a &#8801; 7 (mod 8) and both emit an odd b. Since a return is "
    "produced by five configurations whose outputs are 2a&plusmn;1, 2a+3, "
    "2a+5, and three of the five need an even b, the parity lock removes them "
    "when a &#8801; 7 (mod 8). Hence <b>the return map&rsquo;s image avoids "
    "13 and 15 (mod 16) (proved)</b>, and since the primary halting family "
    "16&middot;2<super>j</super> &minus; j &minus; 12 (j odd) sits at "
    "4 &minus; j (mod 16), <b>exactly a quarter of it &mdash; j &#8801; 5, 7 "
    "(mod 16) &mdash; is unreachable from any start after the first return "
    "(proved)</b>. <i>Verified on 362,327,921 interior states and 450,000 "
    "random transitions to 10<super>12</super>.</i>"))
story.append(P(
    "<b>The correction is bigger than the theorem.</b> This document has "
    "classified machine 4 as &ldquo;sparse coincidence, linear growth&rdquo; "
    "(Sections 5.4 and 6). Both halves are wrong. Measured: the probability "
    "that an excursion from the section halts before returning stays in the "
    "band 0.035&ndash;0.240 across a &#8712; [2<super>6</super>, "
    "2<super>23</super>) &mdash; noisy, but with <b>no decay over nine "
    "octaves</b> (pooled 0.109 over 2,350 excursions). Meanwhile the true "
    "orbit visits the section only <b>19 times in 6&times;10<super>7</super> "
    "base steps</b>, at exponentially spaced times. So a + b does grow "
    "linearly per base step, but the quantity that governs halting "
    "opportunities &mdash; the section value &mdash; grows geometrically, and "
    "the coincidence it has to hit is not sparse. <b>Expected halts over N "
    "section visits is 0.109N, which diverges: machine 4&rsquo;s own "
    "pseudorandom heuristic predicts that it HALTS.</b> It is the "
    "collection&rsquo;s only probviously-halting machine, and its open "
    "question should be read as <i>find the halt</i>, not <i>prove "
    "non-halting</i>. Observing 19 visits with no halt is unremarkable: "
    "(1 &minus; p)<super>19</super> = 0.111."))
story.append(P(
    "<b>The methodological reading.</b> Three of this round&rsquo;s five "
    "results are corrections to statements this program had already written "
    "down and believed: the mod-16 theorem (false as stated), machine "
    "4&rsquo;s genre (inverted), and the Borel&ndash;Cantelli paragraph of "
    "Section 6 (which silently read &ldquo;supercritical return values&rdquo; "
    "as &ldquo;thin halting target&rdquo;). All three were found by "
    "<i>applying new machinery to old files</i> rather than by new "
    "computation &mdash; the same pattern Section 11 records for the "
    "consolidation rounds, now with a fourth instance and a sharper rule: "
    "<b>when a toolkit is finished, re-run it over everything that predates "
    "it.</b>"))

story.append(P("2.18&nbsp;&nbsp;The sieve saturates: depth is not a "
               "resource", H2))
story.append(P(
    "Asked whether the sheep machine&rsquo;s proof could be finished, the "
    "program ran its own last-step sieve one step deeper and then all the way "
    "up. <b>SHEEP-D2 (proved): no branch v &ge; 6 can be the SECOND-to-last "
    "step; the depth-2 survivor set is exactly {0,1,2,3,5}.</b> The proof is "
    "the same shape as the depth-1 one. Because 3N = 2<super>2j+1</super> + 1 "
    "and 5N = 2<super>4j+1</super> &minus; 2 identically, clearing "
    "denominators turns &ldquo;N &#8801; B<sub>v</sub> (mod A<sub>v</sub>)"
    "&rdquo; into 2<super>2j+1</super> &#8801; 3B<sub>v</sub> &minus; 1 "
    "(mod 3A<sub>v</sub>) and 2<super>4j+1</super> &#8801; 5B<sub>v</sub> + 2 "
    "(mod 5A<sub>v</sub>) &mdash; the larger modulus is not optional, since "
    "3 divides A<sub>v</sub> for every even v. Reducing mod A<sub>v</sub> "
    "gives targets 2<super>v</super> + 3v &minus; 2 and 2<super>v</super> + "
    "5v, each of which must be &plusmn;2<super>i</super>, and four gap "
    "inequalities finish it. One is a near miss worth recording: "
    "2<super>5</super> &minus; 25 + 1 = 8 is a genuine power of two, which is "
    "why v = 5 survives and v = 4 does not."))
story.append(P(
    "<b>The ladder can then be climbed exactly.</b> Call N(i) = "
    "(2<super>&alpha;+ei</super> + b)/c with c odd a <i>geometric family</i>. "
    "The halting set is one such family, and the shape is CLOSED under "
    "preimages: f(x) = N(i) for x = 2<super>v</super>(2k+1) reduces to "
    "2<super>&alpha;+ei</super> &#8801; cB<sub>v</sub> &minus; b (mod "
    "cA<sub>v</sub>), whose solutions are a residue class i &#8801; "
    "i<sub>0</sub> (mod P), and substituting back gives another family with "
    "e&prime; = eP and c&prime; = cA<sub>v</sub>. So every depth is computed "
    "in closed form with no search over x. (The leading coefficient stays a "
    "pure power of two &mdash; storing the exponent rather than the integer "
    "is what makes deep levels feasible; it cut depth 4 from 47 s to 1 s.)"))
story.append(Spacer(1, 4))
story.append(tab([
    ("1", "{0, 1}", "2", "0.250000", "0.750000"),
    ("2", "{0, 1, 2, 3, 5}", "7", "0.046875", "0.714844"),
    ("3", "{0, ..., 6}", "23", "0.007812", "0.709259"),
    ("4", "{0, ..., 6, 9}", "90", "0.006836", "0.704411"),
    ("5", "{0, ..., 10, 13}", "346", "0.000427", "0.704110"),
    ("6", "{0, ..., 13}", "1421", "0.000061", "0.704067"),
], ("depth", "surviving branches", "families", "forbidden branch mass",
    "admissible word mass"),
   (0.55*inch, 1.75*inch, 0.8*inch, 1.5*inch, 1.5*inch)))
story.append(Spacer(1, 4))
story.append(P(
    "<b>And it saturates.</b> The forbidden mass per depth collapses "
    "geometrically (0.250, 0.047, 0.0078, 0.0068, 0.00043, 0.000061) while "
    "the family count grows by a factor of about 3.8 per depth, so the "
    "admissible word mass is a <b>convergent product, not a vanishing "
    "one</b>: 0.704067 by depth six, extrapolating to about 0.70406. The "
    "depth-5 data alone extrapolated to 0.704045 and depth 6 then measured "
    "0.704067, so the extrapolation was right to five decimals before the "
    "check existed. (Depth 7 was not run: each depth costs about 15 times "
    "the last &mdash; 1 s, 80 s, 6.4 h &mdash; so depth 7 is about four days "
    "with a linear order-scan; reaching depth 8 or 9 needs the order from a "
    "factorisation of the modulus, which is always a product of "
    "A<sub>v</sub> = 2<super>v+1</super> + 1, plus Pohlig-Hellman.) <b>The "
    "last-step sieve, at "
    "any depth whatsoever, can never forbid more than about 29.6% of branch "
    "words.</b> The mechanism is legible: the depth-d target is a union of "
    "F<sub>d</sub> families, so a branch survives if ANY of them is "
    "reachable; each is reachable with probability about "
    "ord(2)/A<sub>v</sub> = O(v)/2<super>v</super>, so branches survive up to "
    "v &#8776; log<sub>2</sub>F<sub>d</sub>, which grows linearly in d. "
    "Survivor sets grow, forbidden mass decays geometrically, the product "
    "converges. <i>Ground truth agrees at every depth checked: brute force to "
    "3&times;10<super>6</super> gives valuations {0,1,2,3}, {0,1,2,3} and "
    "{0,1,2,5} for halts in two, three and four steps, each inside the "
    "predicted set &mdash; and the v = 5 survivor the sieve predicted at "
    "depth 2 does show up in real data.</i>"))
story.append(P(
    "<b>This is the most useful negative result the program has produced, and "
    "it should change how depth is budgeted everywhere in the collection.</b> "
    "Until now &ldquo;go one step deeper&rdquo; was treated as a resource "
    "that could be spent for more exclusion &mdash; WS3&rsquo;s 28.7%, "
    "M3-N2&rsquo;s 95.06% at depth 2. The sheep computation shows the "
    "resource is bounded: the product of per-depth survival rates converges "
    "because the target set grows as fast as the sieve tightens. Together "
    "with T15 (no congruence certificate at any modulus, which applies to the "
    "sheep verbatim) <b>both congruence-flavoured lanes are now closed on "
    "this machine with numbers attached</b>, leaving exactly one untried: "
    "automatic invariants. There the sheep is a better target than the "
    "Needle, because its halting set is a <b>tiny regular language</b> "
    "&mdash; in binary H<sub>0</sub> = (10)*11, H<sub>1</sub> = (1100)*110, "
    "and the powers of two are 10*. The obstruction is the map, not the "
    "target: f(n) = n + (n &gt;&gt; (v+1)) + v adds a copy of itself shifted "
    "by a <i>variable</i> amount, so f is not 2-automatic, which is exactly "
    "why the WS1 searches stall at small DFA sizes."))

story.append(P("3. The domain in one page", H1))
story.append(P(
    "A <b>Collatz-like problem</b> asks whether the orbit of an explicit "
    "piecewise-affine map on the integers ever meets an explicit target. The "
    "original (3n + 1, open since 1937) is the template; Conway (1972) showed "
    "the general class simulates arbitrary computation, so no algorithm "
    "decides it &mdash; any particular instance can only fall to an "
    "instance-specific insight. Tao (2019) proved the strongest known "
    "statistical result for Collatz itself, and it is representative of the "
    "whole field&rsquo;s limit: it speaks about <i>almost every</i> orbit and "
    "says nothing about any <i>single</i> one."))
story.append(P(
    "A <b>cryptid</b> (the term is from the Busy Beaver community, e.g. the "
    "bbchallenge machine Antihydra) is a small, fully explicit machine whose "
    "halting is provably equivalent to an open problem of exactly that type. "
    "Three structural features make an instance hard, and every machine in "
    "this collection exhibits all three:"))
story.append(tab([
    ("piecewise-affine dynamics",
     "finitely many affine branches selected by guards; exactly solvable "
     "locally, opaque globally"),
    ("expansion",
     "the orbit grows, so it never settles into a checkable finite region"),
    ("digit consumption",
     "each branch choice reads ever-deeper digits of the state, so the branch "
     "stream is pseudorandom and no bounded-state invariant tracks it"),
], ("feature", "why it blocks proofs"), (1.7 * inch, 5.0 * inch)))
story.append(Spacer(1, 4))
story.append(P(
    "The honest endpoint, in every case so far: all structure short of the "
    "halting question itself can be proved, the halting question reduces to "
    "one exact coincidence along one orbit, and there it stops &mdash; the "
    "<b>single-orbit versus almost-everywhere gap</b>, identical to what keeps "
    "Collatz open. Section 4 unpacks this landscape in detail, with "
    "references; this page is the map."))

# ================= 3. case files =================
# ================= 3. related work =================
story.append(P("4. Related work", H1))
story.append(P(
    "What follows situates the program in three bodies of work: the Collatz "
    "conjecture itself, the undecidability theory of the class, and the Busy "
    "Beaver community&rsquo;s cryptid catalogue and decision methods "
    "(bbchallenge wiki, accessed July 2026). Citations [n] refer to the "
    "references at the end."))

story.append(P("4.1&nbsp;&nbsp;The Collatz conjecture itself", H2))
story.append(P(
    "The conjecture &mdash; every positive integer reaches 1 under n &rarr; "
    "n/2 (even), 3n + 1 (odd) &mdash; has been verified for all "
    "n &lt; 2<super>71</super> &#8776; 2.4 &times; 10<super>21</super> "
    "(Barina&rsquo;s distributed GPU computation [9]). The strongest "
    "structural results are statistical: Terras and Everett [6] showed the "
    "set of n whose orbit drops below n has density 1 &mdash; and, crucially, "
    "that initial parity vectors of orbits are equidistributed, the "
    "&ldquo;coin-flip&rdquo; theorem behind every heuristic since; "
    "Krasikov&ndash;Lagarias [7] proved at least x<super>0.84</super> of the "
    "integers up to x reach 1; and Tao [3] proved that <i>almost all</i> "
    "orbits (logarithmic density) attain values below any function tending "
    "to infinity &mdash; almost all orbits fall almost to the bottom. None "
    "of these constrains a single given orbit, and Tao&rsquo;s method "
    "provably loses control exactly at the bottom of the orbit."))
story.append(P(
    "Cycles are excluded by a completely different tool: Baker-type lower "
    "bounds for linear forms in logarithms plus continued-fraction analysis "
    "of log 3 / log 2 &mdash; Steiner ruled out 1-cycles (1977), "
    "Simons&ndash;de Weger m-cycles for m &le; 76, and Hercher [8] recently "
    "m &le; 91, which with the verified range forces any nontrivial cycle to "
    "have length above 2 &times; 10<super>11</super>. This is the one corner "
    "of the field where an <i>infinite family of hypothetical behaviors</i> "
    "is excluded unconditionally &mdash; and Section 8 (Finding 6) turns the "
    "same tool on a cryptid&rsquo;s <i>halting</i> family for the first time; "
    "it is also a model for what our machine-level "
    "cycle exclusions (potentials, expansion margins) accomplish by more "
    "elementary means."))
story.append(P(
    "The ergodic viewpoint explains both the confidence and the obstruction. "
    "The Collatz map extends continuously to the 2-adic integers, where it "
    "preserves Haar measure and is conjugate to the full one-sided shift "
    "(Lagarias [1], Akin); for generalized maps this is Matthews&ndash;Watts "
    "theory [11]. But the integers sit inside Z<sub>2</sub> as a set of "
    "<i>measure zero</i>, so the ergodic theorem says nothing about them. "
    "Lagarias&rsquo;s summary is the epigraph for this whole subject: the "
    "pseudorandomness that supports the conjecture &ldquo;at the same time "
    "deprives us of any obvious mechanism to prove it, since mathematical "
    "arguments exploit the existence of structure, rather than its "
    "absence&rdquo; [2]."))
story.append(P(
    "The stochastic models built on the coin-flip "
    "property (Lagarias&ndash;Weiss branching random walks; "
    "Kontorovich&ndash;Lagarias [10]) predict the empirical constants "
    "with startling accuracy (e.g. maximal-excursion exponent 2, "
    "total-stopping-time constant &#8776; 41.68) &mdash; rigorous about "
    "themselves, heuristic about Collatz. Our per-machine risk accounting "
    "is a transplant of exactly this modeling style, and inherits exactly "
    "its epistemic status."))
story.append(P(
    "Two relatives calibrate how little is provable here. For 5x + 1, "
    "believed divergent for almost all starts, <i>it is open to prove that "
    "even one orbit escapes to infinity</i> [2, 10] &mdash; sobering for "
    "every &ldquo;probviously non-halting&rdquo; claim, ours included. And "
    "Mahler&rsquo;s 3/2 problem (Z-numbers) [12] ties Collatz-adjacent "
    "iterations to the equidistribution of fractional parts of "
    "(3/2)<super>n</super> &mdash; the same circle of questions our "
    "machine 1 mantissa result touches, and the wiki links it directly to "
    "Antihydra&rsquo;s parity stream."))

story.append(P("4.2&nbsp;&nbsp;The class is as hard as it can be", H2))
story.append(P(
    "Conway [4] proved in 1972 that generalized Collatz functions simulate "
    "arbitrary computation &mdash; packaged later as FRACTRAN &mdash; making "
    "their halting problem undecidable; his 2013 sequel exhibits a 24-line "
    "instance he argues is <i>unsettleable</i> (true but unprovable in any "
    "reasonable system), and his &ldquo;amusical permutation&rdquo; carries "
    "his simplest candidate for a true-but-unsettleable concrete claim. "
    "Kurtz and Simon [5] sharpened the classification: for functions defined "
    "by residues mod p with affine branches (exactly our machines&rsquo; "
    "class), the totality question &mdash; does <i>every</i> start reach 1 "
    "&mdash; is &Pi;<super>0</super><sub>2</sub>-complete, as hard as it can "
    "syntactically be. Conway&rsquo;s construction only controlled orbits of "
    "specially encoded starts; Kurtz&ndash;Simon control all of them."))
story.append(P(
    "Consequences for this program: there is no uniform method, so every "
    "settled instance must fall to instance-specific structure; and no "
    "meta-theorem forbids any particular machine from being settled &mdash; "
    "the class being &Pi;<super>0</super><sub>2</sub>-complete coexists with "
    "most instances being easy. Whether 3n + 1 itself is undecidable is "
    "open; Lagarias notes Conway&rsquo;s result &ldquo;indicates that the "
    "3x+1 problem could be close to the unsolvability threshold&rdquo; [2]."))
story.append(P(
    "One clarification this program adds, summarized in Section 9 and "
    "developed in full in the companion <i>Collatz-equivalence</i> report "
    "(collatz/formal/): the "
    "&Pi;<super>0</super><sub>2</sub>-completeness is a property of the "
    "<i>class</i>. Each of our machines, and each single-orbit cryptid like "
    "Antihydra, is a &Pi;<super>0</super><sub>1</sub> statement &mdash; one "
    "universal quantifier over a single orbit, <i>one level below</i> the "
    "&Pi;<super>0</super><sub>2</sub> Collatz conjecture. So &ldquo;as hard as "
    "Collatz&rdquo; names the shared pseudorandom-orbit obstruction, not a "
    "shared logical complexity; the honest same-level comparison is a single "
    "cryptid orbit against a single Collatz orbit. That report also gives an "
    "explicit hardness ordering of the collection (equal at the core; a "
    "partial order on the shell, with the multiplicative machines the only "
    "ones <i>proven</i> beyond congruences)."))

story.append(P("4.3&nbsp;&nbsp;The cryptid bestiary", H2))
story.append(P(
    "The Busy Beaver community coined <b>cryptid</b> (Ligocki, Oct 2023) for "
    "machines whose blank-tape behavior is completely described by a simple "
    "rule that lands in an open, presumed-hard problem [13, 15]. The BB(5) "
    "proof [13] decided all 181,385,789 five-state machines &mdash; "
    "&ldquo;in hindsight, it is surprising (and lucky!) that there are no "
    "5-state Cryptids&rdquo; &mdash; but BB(6) is now provably "
    "&ldquo;Hard&rdquo;: Antihydra&rsquo;s halting is an open Collatz-like "
    "problem, so BB(6) cannot be resolved without solving one. The current "
    "BB(6) champion exceeds 2^^^5 (pentation); roughly 1,100 six-state "
    "machines remain undecided. The wiki catalogues ~21 cryptids under "
    "three verdicts &mdash; <i>undecided</i>, <i>probviously non-halting</i>, "
    "<i>probviously halting</i> (&ldquo;probviously&rdquo; = probabilistic + "
    "obvious, a coinage the wiki attributes to Conway). The named ones:"))
story.append(Spacer(1, 4))
story.append(tab([
    ("Bigfoot", "BB(3,3)",
     "3-var system, value &times;4/3 keyed on b mod 6; counter a random-walks "
     "(+1 w.p. 2/3)", "a = 0 at b &#8801; 2 (mod 6)", "undecided"),
    ("Hydra", "BB(2,5)",
     "H(n) = floor(3n/2) from n = 3; counter walks +2 on odd, &minus;1 on even",
     "#even exceeds 2&middot;#odd", "undecided"),
    ("Antihydra", "BB(6)",
     "H(n) = floor(3n/2) from n = 8 &mdash; same map, mirrored condition",
     "#odd exceeds 2&middot;#even", "undecided"),
    ("Bonus cryptid", "BB(2,5)",
     "a &rarr; (4/3)a with a fuel counter b; b drifts up w.p. 2/3",
     "b = 0 with a &#8801; 0 (mod 3)", "probv. non-halting"),
    ("Lucy's Moonlight", "BB(6)",
     "epoch resets c<sub>0</sub> = 14, c<sub>1</sub> = 11292, c<sub>2</sub> "
     "&#8776; 10<super>2902</super>; fixed halt chance per epoch",
     "hit C(1, 3k+1)", "probv. halting"),
    ("Space Needle", "BB(6)",
     "b &rarr; b + v(b) + (3/2)(b/2<super>v(b)</super> &minus; 1), v = 2-adic "
     "valuation, from b = 6", "b is an exact power of 2", "probv. non-halting"),
    ("Fenrir", "FRACTRAN-22",
     "3 programs; 2/5-parity walk S(x, y), y &times;&#8776;5/2 per step",
     "x = 0 at even y", "probv. non-halting"),
], ("name", "domain", "map (one line)", "halts when", "status"),
   (0.85 * inch, 0.75 * inch, 2.55 * inch, 1.45 * inch, 1.0 * inch)))
story.append(Spacer(1, 4))
story.append(P(
    "Constructed cryptids place famous conjectures at explicit sizes "
    "(Goldbach at BB(25), Riemann at BB(744), consistency of ZF at BB(432)) "
    "[15]; the catalogued ones above were found <i>in the wild</i>. Our "
    "machines are all cryptids by the wiki&rsquo;s criteria. Machine 1 has the "
    "geometric-growth profile (dodging targets at every scale, like Bonus "
    "cryptid); and machine 4&rsquo;s section structure is the shape of "
    "Lucy&rsquo;s Moonlight&rsquo;s epochs &mdash; both probviously "
    "halting, for a reason Section 7 (P8) makes precise."))

story.append(P("4.4&nbsp;&nbsp;How instances actually get decided", H2))
story.append(P(
    "The BB(5) proof [13] is the largest corpus of settled guarded-rule "
    "machines and its pipeline is a de facto hierarchy of hardness: loop "
    "detection settles the overwhelming majority (~95% of non-halters are "
    "cyclers or translated cyclers); regular-language closed-set invariants "
    "(n-gram CPS, repeated word lists, finite-automata reduction &mdash; "
    "found by direct search or SAT) settle millions more; weighted automata "
    "add counting power for a thin tier; and 13 &ldquo;sporadic&rdquo; "
    "machines needed bespoke inductive proofs [13, 14]. Two sporadics are "
    "instructive. <b>Skelet #17</b> hid an obfuscated Gray-code counter; its "
    "invariant took a number-theoretic proof and ~7,000 lines of Coq [14]. "
    "<b>Skelet #1</b> looked chaotic but is a translated cycler with "
    "preperiod &#8776; 5.4 &times; 10<super>51</super> steps &mdash; visible "
    "only through multi-level exact acceleration. The lesson for us is "
    "sharp: apparent pseudorandomness can mask eventual periodicity at "
    "depths no simulation reaches, which is precisely why our no-cycle "
    "theorems (potentials, expansion margins) matter &mdash; they are what "
    "licenses calling a machine a cryptid rather than a Skelet #1."))
story.append(P(
    "Instances of Collatz-like <i>functions</i> have been settled too: "
    "Farkas&rsquo;s variant falls to induction, and Yolcu&ndash;Aaronson&ndash;"
    "Heule [16] even found automated termination proofs (SAT-searched matrix "
    "interpretations &mdash; machine-found ranking functions) for weakened "
    "Collatz systems; the polynomial analogue over GF(2)[x] is a theorem "
    "because degree is monotone &mdash; in our language, a potential exists "
    "and the digit/carry interaction that blocks the integer case is absent "
    "[17]. The existence proofs matter: instances do fall, always to "
    "instance-specific structure of kinds we recognize. The correspondence "
    "between the community&rsquo;s deciders and this program&rsquo;s toolkit "
    "is essentially exact:"))
story.append(Spacer(1, 4))
story.append(tab([
    ("backward reasoning from the halt state",
     "halt-route closure theorems; the last-step valuation sieve"),
    ("CTL / FAR: regular-language invariants",
     "separating-congruence search (a residue class is a finite-automaton "
     "invariant on digits)"),
    ("weighted automata (WFAR): counting invariants",
     "affine potentials (&Phi; = 2b + d, machine 1)"),
    ("shift rules, macro machines, inductive rule provers",
     "acceleration levels L1&ndash;L4: batched loops and geometric cascades"),
    ("accelerated simulation with certified checkpoints",
     "step-exact deep runs (10<super>150,514</super>; 5 &times; "
     "10<super>11</super>) verified against the base rules"),
    ("sporadic machines: bespoke inductive proofs",
     "the theorem-per-machine style of the machine reports"),
], ("bbchallenge decider", "this program's tool"),
   (3.2 * inch, 3.5 * inch)))
story.append(Spacer(1, 4))
story.append(P(
    "Their practices worth importing directly: proof by reflection (soundness "
    "of a decider proved once, then run over millions of instances), "
    "small independently-checkable certificates, and formalization as a bug "
    "hunt &mdash; the Coq check of Skelet #1 caught transcription errors in "
    "the informal proof, just as our step-exact checks caught two real "
    "acceleration bugs (Section 11)."))

story.append(P("5. Case files", H1))

story.append(P("5.1&nbsp;&nbsp;Machine 1 &mdash; NextConfig(a, b, c, d) from "
               "(0, 0, 0, 0)", H2))
story.append(P(
    "Thirteen guarded rules over four counters. A four-level exact "
    "acceleration (eliminate the transfer buffer; batch unary loops; batch "
    "geometric cascades; first-return map on the section b = 1) reduces the "
    "machine to iteration of a single integer map D &rarr; F(D) from "
    "D<sub>0</sub> = 17 &mdash; piecewise affine with countably many "
    "digit-indexed branch words, dominant word F(D) = 16D &minus; "
    "240&middot;2<super>n</super> + 32n + 169. Halting &hArr; the F-orbit "
    "meets an infinite halting set H (explicit affine families such as "
    "15&middot;2<super>i</super> &minus; 2i &minus; 12). Proved along the "
    "way: the halting criterion (&phi; = d &minus; b &minus; a = 2 with a "
    "side congruence), <b>mod-16 confinement</b> (F(D) &#8801; 9 mod 16, "
    "pruning H to a thin subfamily), an exact <b>expansion margin</b> on the "
    "dominant word (F(D) &minus; D &ge; 2n + 19; the guard fails 11 units "
    "before contraction would begin), and an <b>obstruction theorem</b>: F "
    "has no continuous extension to the 2-adic integers, so the route behind "
    "Collatz&rsquo;s ergodic backbone is provably closed. And &mdash; added "
    "July 2026 &mdash; a "
    "<b>monotone potential</b>: &Phi; = 2b + d rises by at least 2 at every "
    "anchor step, so the machine provably cannot cycle. Verified: no halt "
    "in the first 10<super>150,514</super> base steps; growth &times;2.4 per "
    "cycle. Heuristic residual risk below 10<super>&minus;75,000</super>. "
    "<b>Status: open (geometric growth); halts or escapes &mdash; "
    "periodicity excluded by proof.</b>"))
story.append(P(
    "<b>Nearest relatives in the bestiary.</b> Machine 1 combines "
    "sparse-coincidence halting with geometric growth &mdash; the "
    "combination <b>Space Needle</b> exhibits: both orbits must land "
    "<i>exactly</i> in a set that thins as they grow (an affine "
    "(2<super>i</super>, i)-family here; exact powers of 2 there), and both "
    "are probviously non-halting precisely because the coincidence "
    "probability decays with the orbit. Its growth-and-verification profile "
    "&mdash; &times;2.4 per cycle, no halt in 10<super>150,514</super> steps "
    "&mdash; matches <b>Bonus cryptid</b>, driven to comparable depths "
    "(values above 10<super>12,000,000</super>). And its branch words, "
    "consuming ~log<sub>2</sub> D bits per cycle, are the machine-level "
    "incarnation of the Terras&ndash;Everett coin flips (Section 4.1)."))
story.append(P(
    "<b>What Section 4 says to try next.</b> (i) <i>Done (July 2026):</i> "
    "the missing monotone potential was found &mdash; &Phi; = 2b + d, "
    "increment &ge; 2, resting on a conservation lemma A* + &Delta;* = "
    "A + &Delta; + 3n for the sweep cascades (machine 1 report, &sect;9.6d). "
    "The Skelet #1 scenario is now excluded by proof rather than by measured "
    "expansion, exactly as this list called for. (ii) <i>Attempted (Section "
    "8, Finding 6):</i> Baker&rsquo;s linear forms in logarithms &mdash; the "
    "tool that eliminated every Collatz m-cycle with m &le; 91 &mdash; were "
    "pointed at the halting family (a first for a cryptid&rsquo;s <i>halting</i> "
    "problem); they reach each fixed branch word but not the unbounded "
    "sequence, giving one unconditional partial result. (iii) <i>Done (Section "
    "8, Finding 2):</i> the mantissa density is located &mdash; a two-branch "
    "circle map with breakpoint log<sub>2</sub>(5/4), strongly mixing; its "
    "non-uniformity connects to the (3/2)<super>n</super>-equidistribution "
    "circle of Mahler&rsquo;s problem, the same one the wiki links to "
    "Antihydra. (iv) Still open: a SAT-driven weighted-automaton "
    "search (Section 4.4) would mechanize the separation hunt "
    "that stopped by hand at m &le; 256."))

story.append(P("5.2&nbsp;&nbsp;Machine 3 &mdash; A(a, b) from (1, 1), the "
               "multiplicative cryptid", H2))
story.append(P(
    "Six rules over two counters; halting is a genuinely new type for the "
    "collection. b resets to 1 whenever a is not &#8801; 0 (mod 3), and a divides by "
    "3 (pumping b) when a &#8801; 0 (mod 3), so a reaches 1 &mdash; the only "
    "gateway to halting &mdash; <b>only when it hits an exact power of 3</b>. "
    "<b>Theorem 1:</b> the machine halts iff the a-orbit lands on "
    "{3<super>j</super> : j &#8801; 0 (mod 3)} = {27, 729, 19683, &hellip;} = "
    "{27<super>m</super>}. This is the <b>multiplicative-coincidence</b> type "
    "&mdash; the bbchallenge Space Needle&rsquo;s power-of-2 target, here a "
    "power of 3 with an exponent congruence (a Theorem-7-like refinement "
    "selecting one third of the powers). The divide chains have a closed form "
    "(Theorem 2); the potential &Phi; = a + b (b cancelling in the reset "
    "rules) proves no cycles (Theorem 3) &mdash; the third machine to yield an "
    "affine potential by the same recipe; and the divide depth is the 3-adic "
    "valuation, Geom law P(j) = (2/3)(1/3)<super>j&minus;1</super> to three "
    "decimals. Verified: no halt in 3,000,000 composite steps (a past 700,000 "
    "bits, 2.25M resets, never a power of 3). Grows geometrically. "
    "<b>Status: open (geometric growth, multiplicative-coincidence); periodicity "
    "excluded by proof.</b> Nearest relative: <b>Space Needle</b>, now itself analyzed (Section 5.5)."))

story.append(P("5.3&nbsp;&nbsp;Machine 4 &mdash; A(a, b) from (1, 1), the "
               "recovery-potential cryptid", H2))
story.append(P(
    "Ten rules over two counters, a second sparse-coincidence machine. "
    "<b>Theorem 1:</b> a stays odd forever (every odd-a rule outputs odd a), "
    "so the even-a rules never fire. <b>Theorem 2:</b> halting is exactly the "
    "line <b>b = a + 3</b> (a odd). The dominant rule cascades in closed form "
    "(Theorem 3). Its distinctive result is <b>Theorem 4</b>: no affine "
    "combination p&middot;a + q&middot;b is monotone (the small-b rules "
    "shrink a; b = a+1 lowers a + b by 1), so the plain P6 recipe fails "
    "&mdash; the first machine where it does &mdash; but a + b is a "
    "<b>potential with recovery</b> (every non-increasing step is isolated, "
    "lands on b = 1, and is followed by a +4 step), and that proves no "
    "cycles. Growth is linear; the orbit came within distance 1 of the halt "
    "line; no halt in 3,000,000 steps. <b>Status (revised July 31): open, and "
    "the heuristic predicts it HALTS.</b> Periodicity is still excluded by "
    "proof (recovery potential), but the &ldquo;sparse coincidence&rdquo; "
    "label was wrong &mdash; see Section 2.17 for the measurement and for two "
    "new 2-adic theorems (the return map&rsquo;s image avoids 13 and 15 mod "
    "16; a quarter of the primary halting family is unreachable from any "
    "start). Nearest relatives: Lucy&rsquo;s Moonlight (the other "
    "probviously-halting machine)."))

story.append(P("5.4&nbsp;&nbsp;The Hydra family &mdash; catalogued relatives "
               "(program step 1)", H2))
story.append(P(
    "Applying the toolkit to the closest bbchallenge cryptids: <b>Hydra</b> "
    "(BB(2,5)) and <b>Antihydra</b> (BB(6)) iterate H(n) = floor(3n/2) with "
    "mirrored count conditions, and <b>Fenrir</b> (three FRACTRAN-22 holdouts) "
    "is the same machine in base 5. All are <i>walk-absorption</i> type. "
    "Results (see the hydra/ report): implementations verified against every "
    "wiki trajectory, including two conjugacies the wiki leaves unstated; the "
    "family cannot cycle (the value is its own potential); the golden-ratio "
    "absorption model q = (&radic;5&minus;1)/2 is made exact; and the branch "
    "statistic is Geom(1/2) to three decimals. The headline is a "
    "<b>q-adic branch-memory theorem</b>: n mod 3<super>k</super> depends only "
    "on the last k parities, so no congruence invariant of the value can track "
    "the cumulative count that decides halting &mdash; upgrading &ldquo;no "
    "separating modulus&rdquo; from a search result (machine 1) to a "
    "two-line theorem, and giving the collection its sharpest structural "
    "account of why regular-invariant deciders fail on these machines. Deep "
    "runs reproduce the wiki drifts (Hydra 2M steps, counter 1,003,573). "
    "<b>Status: unchanged &mdash; open; proofs added beneath the "
    "community&rsquo;s simulations.</b>"))

story.append(P("5.5&nbsp;&nbsp;The Space Needle &mdash; machine 3&rsquo;s "
               "archetype, analyzed", H2))
story.append(P(
    "Machine 3 was built to mirror a specific catalogued cryptid: the BB(6) "
    "<b>Space Needle</b> (mxdys, January 2025), which halts iff its "
    "one-variable orbit (Doucette&rsquo;s form, from b = 6) hits an exact "
    "power of 2. Running the toolkit over it (needle/ report) both "
    "characterizes it and, more valuably, <b>validates the tools against a "
    "genuine catalogued cryptid we did not design</b>. Every check passes: "
    "the implementation reproduces the wiki&rsquo;s published sequence 6, 10, "
    "17, 41, 101, 251, 626, 1095, 2736, 2995 exactly; b is strictly "
    "increasing, so the machine cannot cycle (the state is its own potential, "
    "as for the Hydra family); the branch is the 2-adic valuation with the "
    "geometric law P(v = k) = 2<super>&minus;(k+1)</super> to three decimals; "
    "and the sharpest test &mdash; the measured per-step log-growth is "
    "<b>0.6515 against the wiki&rsquo;s independently derived 0.652355</b> "
    "(b &#8776; 1.918<super>n</super> vs their 1.92006). It is a "
    "geometric-growth machine of exactly machine 3&rsquo;s shape, with powers "
    "of 2 for powers of 3 and no exponent congruence (every power of 2 halts). "
    "That machine-built tools reproduce the community&rsquo;s growth constant "
    "to three decimals is the strongest single piece of evidence in this "
    "collection that its methods and the bbchallenge analyses are the same "
    "analysis in different notation. <b>Status: unchanged &mdash; open "
    "(geometric growth, multiplicative-coincidence).</b>"))

story.append(P("5.6&nbsp;&nbsp;The sheep machine &mdash; the second wild "
               "cryptid inside the interface", H2))
story.append(P(
    "<font face='Courier'>1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE</font>, "
    "BB(6), found by <i>sheep</i> on 7 April 2026 and listed as a "
    "bbchallenge Cryptid. Published reduction: f(n) = HALT if oddPart(n) = 1; "
    "n + v<sub>2</sub>(n) + 3 if oddPart(n) = 3; n + v<sub>2</sub>(n) + "
    "(oddPart(n) &minus; 1)/2 if oddPart(n) &gt; 3; start at 5. Its generic "
    "branch is <b>census member (1,1,1,1,0)</b>, the Space Needle&rsquo;s "
    "reduction (1,3,1,1,0) with &beta; changed from 3 to 1 &mdash; so the "
    "collection now holds <b>two</b> wild machines inside the branch-affine "
    "interface, not one. Everything the toolkit has applies, and for the "
    "first time the last-step sieve <b>closes completely</b>: only "
    "v &#8712; {0,1} can precede a halt, the oddPart = 3 branch never can, "
    "and the halting set has a closed form in three geometric families "
    "(Section 2.17). No modulus separates it (T15). <b>Status: open &mdash; "
    "arithmetic settled, single-orbit avoidance open</b>; 30,000 steps run "
    "with no halt, drift 0.4014 measured against 0.401524 predicted by the "
    "census member. Nearest relative: the <b>Space Needle</b>, of which it is "
    "the &beta; = 1 sibling &mdash; and the pair is the sharpest instance of "
    "the rank-of-sieve-group dichotomy the program has."))

story.append(P("5.7&nbsp;&nbsp;Each machine and its nearest catalogued "
               "relative", H2))
story.append(tab([
    ("machine 1", "Space Needle",
     "growing orbit must land exactly in a thinning sparse set; probviously "
     "non-halting for the same reason",
     "target affine in (2<super>i</super>, i) vs exact powers of 2"),
    ("machine 1", "Bonus cryptid",
     "geometric growth, verified to astronomical depths",
     "Bonus halts by walk absorption (fuel hits 0)"),
    ("machine 3", "Space Needle",
     "the exact type-twin: growing orbit must hit an exact power",
     "powers of 3 (ours) vs powers of 2 &mdash; same multiplicative type"),
    ("machine 4", "Lucy's Moonlight",
     "dense per-epoch halting chance, so the expected hit count diverges",
     "both are probviously HALTING; machine 4 needs the recovery potential "
     "for no-cycle (revised, Section 2.17)"),
    ("sheep", "Space Needle",
     "same census schema, same halting set (powers of 2), &beta; = 1 vs 3",
     "sheep&rsquo;s sieve group is listable, so its last-step analysis "
     "closes; the Needle&rsquo;s is thin and does not"),
], ("machine", "nearest relative", "shared structure", "key difference"),
   (0.85 * inch, 1.2 * inch, 2.7 * inch, 2.0 * inch)))
story.append(Spacer(1, 8))

# ================= 4. side by side =================
story.append(P("6. The machines side by side", H1))
story.append(P(
    "The case files in prose; here all three of our machines, attribute by "
    "attribute (the catalogued Hydra family is summarized in Section 5.4):"))
story.append(tab([
    ("rules / counters", "13 / 4", "6 / 2", "10 / 2"),
    ("start", "(0,0,0,0)", "(1, 1)", "(1, 1)"),
    ("halting type", "sparse coincidence",
     "multiplicative", "sparse coincidence"),
    ("halting condition", "&phi; = d&minus;b&minus;a = 2",
     "a = 3<super>j</super>, j &#8801; 0 (mod 3)", "b = a + 3 (a odd)"),
    ("halting target",
     "family 15&middot;2<super>i</super>&minus;2i&minus;12",
     "powers {27<super>m</super>}", "line b = a + 3"),
    ("growth", "geometric, &times;2.4",
     "geometric", "linear, &#8776;2.34"),
    ("reduction / accel.", "F on {b = 1}",
     "divide-chains batched", "dominant-rule cascade"),
    ("key invariant", "orbit &#8801; 9 (mod 16)",
     "exponent &#8801; 0 (mod 3)", "a stays odd"),
    ("no-cycle proof", "&Phi; = 2b + d", "&Phi; = a + b",
     "a + b, w/ recovery"),
    ("branch statistic", "~log<sub>2</sub> D bits",
     "3-adic val.", "digit-driven"),
    ("verified horizon", "10<super>150,514</super> steps",
     "3&times;10<super>6</super> comp.", "3&times;10<super>6</super> steps"),
    ("per-step growth / returns", "geom. / frequent",
     "geom. / frequent", "linear / thinning"),
    ("halting risk &Sigma;1/C", "converges", "converges",
     "converges"),
    ("status", "open", "open", "open"),
], ("", "machine 1", "machine 3", "machine 4"),
   (1.30*inch, 1.60*inch, 1.55*inch, 1.55*inch)))
story.append(Spacer(1, 4))
story.append(P(
    "The machines split by <b>per-step growth rate</b>, and it is worth being "
    "precise about what that split does and does not mean (the explorations "
    "report has the measurements). Machines 1 and 3 grow geometrically per "
    "step because their orbits return to the section at a constant rate; "
    "machine 4 grows only linearly because its returns thin out "
    "exponentially. That is a real structural difference. It is <b>not</b> a "
    "difference in the halting mechanism <i>except for machine 4</i>: the "
    "first-return maps of all of them &mdash; and of the Space Needle &mdash; "
    "are supercritical (return values grow geometrically, mean log-ratio "
    "0.33&ndash;0.99), so the halting-risk sum &Sigma; 1/C<sub>n</sub> "
    "converges, by the same Borel&ndash;Cantelli argument (Pattern P8). "
    "<b>Machine 4 breaks this and the July 31 measurement is the reason "
    "(Section 2.17): its per-return risk is not 1/C<sub>n</sub> at all.</b> "
    "The halting set is dense in its section &mdash; an excursion halts with "
    "probability 0.035&ndash;0.240 regardless of scale &mdash; so the "
    "per-return risk does not decay, the sum diverges, and Borel&ndash;"
    "Cantelli points the other way. That is a defect in the old paragraph, "
    "not in machine 4: &ldquo;supercritical return values&rdquo; was silently "
    "being read as &ldquo;thin halting target&rdquo;, and for machine 4 the "
    "two come apart. The large residual-risk "
    "figures in the case files &mdash; 10<super>&minus;75,000</super> for "
    "machine 1, far larger elsewhere &mdash; are therefore "
    "<b>verified-depth artifacts</b> (machine 1&rsquo;s orbit was simply "
    "pushed to far larger return values), not two kinds of cryptid. All are "
    "the same open problem: a supercritical orbit threading a geometrically "
    "sparse target, probviously but never provably forever. The labels "
    "&ldquo;geometric / frequent returns&rdquo; and &ldquo;linear / thinning "
    "returns&rdquo; are the honest form of the old "
    "divergent/convergent contrast."))
story.append(P("6.1&nbsp;&nbsp;The whole collection at a glance", H2))
story.append(P(
    "The table above compares our three machines attribute by attribute; the "
    "scannable summary below adds the catalogued Hydra family, so all four "
    "objects &mdash; spanning all three halting-condition types (Section 7.1) "
    "&mdash; sit in one view:"))
story.append(Spacer(1, 4))
story.append(tab([
    ("machine 1", "sparse coincidence", "geometric &times;2.4",
     "affine family 15&middot;2<super>i</super>&minus;2i&minus;12",
     "proved (&Phi;=2b+d)", "open"),
    ("machine 3", "multiplicative", "geometric",
     "exact powers {27<super>m</super>}", "proved (&Phi;=a+b)", "open"),
    ("machine 4", "DENSE coincidence*", "linear a+b, geometric section",
     "line b = a+3 (a odd)", "proved (a+b w/ recovery)",
     "open &mdash; probviously HALTS*"),
    ("Hydra family", "walk absorption", "geometric &times;3/2",
     "cumulative count boundary", "proved (value is potential)",
     "open (3 machines)"),
    ("Space Needle", "multiplicative", "geometric &times;1.92",
     "exact powers {2<super>i</super>}", "proved (b increasing)", "open"),
    ("sheep", "multiplicative", "geometric &times;1.32",
     "{2<super>i</super>} &#8746; two explicit families",
     "proved (value increasing)", "open (arithmetic settled)"),
], ("machine", "halt type", "growth", "halting target", "no-cycle", "status"),
   (1.05*inch, 1.25*inch, 0.95*inch, 1.55*inch, 1.2*inch, 1.05*inch)))
story.append(Spacer(1, 4))
story.append(P(
    "* <b>Corrected July 31 (Section 2.17).</b> Machine 4 was listed here as "
    "&ldquo;sparse coincidence / linear growth&rdquo;. Measurement says "
    "otherwise: its per-excursion halt probability sits in 0.035&ndash;0.240 "
    "with no decay over nine octaves, while its section is visited only "
    "logarithmically often, so the expected number of halts <i>diverges</i> "
    "and its own heuristic predicts a halt. a + b does grow linearly per base "
    "step, but the section values &mdash; the ones that govern halting "
    "opportunities &mdash; grow geometrically.",
    ParagraphStyle("TabFoot", parent=BODY, fontSize=9,
                   textColor=colors.HexColor("#555555"))))
story.append(P(
    "One reading stands out that the two-machine version could not show. "
    "<b>No-cycle is now proved for every machine</b> &mdash; three by a plain "
    "affine potential, machine 4 by the recovery extension (Section 7, P6), "
    "the Hydra family for free &mdash; so across the whole collection "
    "&ldquo;halts or escapes&rdquo; is universal and the Skelet #1 "
    "long-transient scenario is everywhere excluded. And the growth-rate "
    "split of the previous paragraph is a spanned pattern &mdash; two "
    "geometric machines, two linear &mdash; while the halting risk is uniform "
    "across all of them (supercritical returns, convergent &Sigma; "
    "1/C<sub>n</sub>); the two axes are independent, and decidability is "
    "untouched by either."))

# ================= 5. patterns =================
story.append(P("7. What generalizes: patterns across the machines", H1))
story.append(P(
    "Each pattern below first appeared in machine 1 and has since been "
    "checked against machines 3 and 4 and the Hydra family; the illustrative "
    "text keeps the original two-machine examples, with the wider evidence "
    "noted inline. On the next machine these are predictions to test, not "
    "merely observations. Section 7.1 then confronts them with the catalogued "
    "cryptids of Section 4.3 &mdash; most survive, one is refined, and an "
    "eighth pattern emerges."))

pats = [
    ("P1 &mdash; The orbit lives on a section",
     "Machines 1&ndash;3 collapse to the iteration of one integer on a "
     "first-return section (anchors b = 1; resets a = 1 or a = 3<super>j</super>); "
     "the Hydra family is one-variable outright; machine 4 keeps two counters "
     "but pins one by an invariant (a odd). The reduction is what makes the "
     "halting question sayable. "
     "<i>Next machine: hunt the revisited section before anything else; pin "
     "coordinates until one integer remains.</i>"),
    ("P2 &mdash; Halting sets are affine in (2<super>j</super>, j)",
     "Machine 1: families like 15&middot;2<super>i</super> &minus; 2i "
     "&minus; 12. Machine 4: 16&middot;2<super>j</super> &minus; j &minus; "
     "12. Reason: a halt is a batched geometric cascade landing exactly on a "
     "line, and equating a cascade&rsquo;s closed form to a constant yields "
     "&alpha;&middot;2<super>j</super> + &beta;j + &gamma;. <i>Next machine: "
     "write the cascade closed form, set it equal to the halting line, and "
     "read off H directly.</i> (The catalogue shows this is the signature of "
     "one halting-condition type among three &mdash; refined in 6.1.)"),
    ("P3 &mdash; Congruences confine but never separate",
     "Machine 1: the orbit is provably pinned to 9 (mod 16). Machine 4: "
     "the return map&rsquo;s image avoids 13 and 15 (mod 16), erasing a "
     "quarter of the primary halting family. In both, "
     "2-power congruence structure prunes the target set by a constant "
     "fraction &mdash; and in both, an exhaustive search finds no modulus "
     "that fully separates orbit from targets (none &le; 256, none &le; "
     "628). July 2026 turned this into proof: for machine 1 the entire "
     "congruence content is the single class 9 (mod 16), and for the Space "
     "Needle and the sheep machine T15 shows <i>no</i> modulus separates, "
     "with no hypotheses left. <i>Next machine: compute the "
     "2-adic structure of both orbit and "
     "H; expect a confinement theorem; budget no hope for a separation.</i>"),
    ("P4 &mdash; The branch stream mimics Collatz's valuation",
     "Machine 1 consumes ~log<sub>2</sub> D leading bits per cycle (branch "
     "words); the Space Needle&rsquo;s branch obeys P(v) = "
     "2<super>&minus;(v+1)</super> &mdash; precisely the geometric law of the 2-adic "
     "valuation of 3n + 1 that the Collatz heuristic assumes. <i>Next "
     "machine: measure the branch statistic early; it calibrates every "
     "risk estimate and explains the growth rate quantitatively.</i> "
     "Confirmed in every machine of the collection and at three bases: 2-adic "
     "(Hydra, Space Needle, the sheep machine), 3-adic (machine 3&rsquo;s divide depth, Geom law "
     "(2/3)(1/3)<super>j&minus;1</super>), and 5-adic (Fenrir) &mdash; always "
     "the valuation law the Collatz heuristic assumes."),
    ("P5 &mdash; Expansion holds by exact, small margins",
     "Machine 1's dominant word cannot contract &mdash; and misses doing so "
     "by exactly 11 guard units (F(D) &minus; D &ge; 2n + 19). Machine 4&rsquo;s "
     "a + b dips by at most 1 before recovering +4. The guards sit just barely on "
     "the expanding side, which is also why measured minimum growth ratios "
     "crowd 1 (1.0002 and 1.0048). A further instance appeared in July 2026: "
     "machine 1&rsquo;s exit guard is <i>exactly</i> the positivity "
     "condition of its newly found potential, with margin 9. Three "
     "independent instances suggest a survivorship reading: the machines "
     "that run long are precisely those whose guards just barely preserve "
     "monotone growth &mdash; anything less would have halted or cycled "
     "early. <i>Next machine: derive the margin "
     "exactly; expect it to be tight, and expect uniform geometric growth to "
     "be unprovable even when average growth is obvious.</i>"),
    ("P6 &mdash; A conserved or monotone quantity closes the cycle route",
     "Machine 1 has a proved potential, &Phi; = 2b + "
     "d (an affine quantity, a "
     "minimum increment, a conservation lemma under cascades), so it "
     "provably cannot cycle. Machines 3 (&Phi; = a + b) and 4 "
     "extend the count: all machines of the collection provably cannot "
     "cycle. Machine 4 needed a twist worth keeping &mdash; no affine "
     "quantity is monotone there, but a + b is a <b>potential with "
     "recovery</b> (it dips by at most 1 and is restored +4 the next step), "
     "which still forbids cycles. <i>Next "
     "machine: look for an affine potential with a provable minimum "
     "increment; if none is monotone, check whether the decreases are "
     "isolated and self-correcting &mdash; the recovery form still works.</i>"),
    ("P7 &mdash; Everything closes except one exact coincidence",
     "In every machine of the collection every halt route but one is closed "
     "by proof, and the "
     "last is an equality (reach exactly one line; land exactly on one "
     "family member) that the orbit must satisfy once. That equality is the "
     "cryptid core, and no tool in the kit &mdash; congruences, potentials, "
     "statistics &mdash; addresses a single orbit. <i>Next machine: drive "
     "the analysis until only an exact coincidence remains, then say so and "
     "stop claiming.</i>"),
]
for title, body in pats:
    story.append(P(f"<b>{title}.</b> {body}"))

story.append(P("7.1&nbsp;&nbsp;The patterns tested against the catalogue", H2))
story.append(P(
    "With the bbchallenge bestiary in hand (Section 4.3), each pattern now "
    "has an external verdict. <b>P1 holds everywhere</b>: every catalogued "
    "cryptid&rsquo;s analysis passes through a 1&ndash;2 variable rule "
    "system, usually with an explicit one-variable form (the Hydra function; "
    "Space Needle&rsquo;s valuation form). <b>P4 is not just confirmed but "
    "rooted</b>: the coin-flip behavior we measured is, for Collatz on the "
    "2-adics, the Terras&ndash;Everett theorem, and Space Needle&rsquo;s "
    "analysis rests on the same uniform-low-bits assumption we tested. "
    "<b>P3 turns out to be a special case</b> of the community&rsquo;s "
    "central boundary: a congruence class is a finite-automaton invariant on "
    "digits, so our separating-modulus searches are the arithmetic shadow of "
    "CTL/FAR &mdash; and the community&rsquo;s experience matches ours "
    "exactly (invariants prune, cryptids are where none separates). The "
    "Hydra family then supplies P3&rsquo;s strongest form: its q-adic "
    "branch-memory theorem (Section 5.4) turns &ldquo;no separating modulus "
    "found&rdquo; from a search outcome into a <i>proof</i> that no congruence "
    "invariant of the value can decide halting &mdash; the empirical wall of "
    "machine 1 shown to be a real one, at least for the value alone; "
    "the same theorem holds for the multiplicative machines (Section 8, "
    "Finding 3), whose valuation branch is orthogonal to every modulus coprime "
    "to the base. "
    "<b>P6 acquires its sharpest motivation</b> from Skelet #1: a "
    "5.4 &times; 10<super>51</super>-step transient before periodicity means "
    "&ldquo;looks pseudorandom&rdquo; is worthless testimony; only no-cycle "
    "theorems separate cryptids from long-transient cyclers."))
story.append(P(
    "<b>P2 must be refined</b> &mdash; the catalogue shows our machines "
    "occupy one branch of a three-way taxonomy of halting conditions:"))
story.append(Spacer(1, 4))
story.append(tab([
    ("sparse coincidence",
     "land exactly on a member of a thin explicit set, affine in "
     "(2<super>j</super>, j)", "machines 1 and 4 (two of ours)"),
    ("walk absorption",
     "a counter&rsquo;s running total hits a boundary (an absorbing state of "
     "a random walk)", "Hydra, Antihydra, Bigfoot, Bonus, Fenrir"),
    ("multiplicative coincidence",
     "the value itself hits a multiplicative target (an exact power)",
     "Space Needle; machine 3 (powers of 3)"),
], ("halting-condition type", "the halting event", "instances"),
   (1.5 * inch, 3.2 * inch, 2.0 * inch)))
story.append(Spacer(1, 4))
story.append(P(
    "As of the machine 3 and 4 analyses, <b>our own machines now instantiate "
    "all three types</b> &mdash; sparse coincidence (1, 4), multiplicative "
    "(3), and, through the analyzed Hydra family, walk absorption &mdash; so "
    "the taxonomy is no longer a claim about the catalogue alone but a "
    "spanned classification we can build in and test tools against at will."))
story.append(P(
    "The affine-in-(2<super>j</super>, j) form of P2 is the signature of "
    "type-1 machines specifically &mdash; it comes from equating a cascade "
    "closed form to a halting line. Walk-absorption machines need no such "
    "set: their halting event is cumulative, not positional. Whether a given "
    "guarded system is type 1 or type 2 is visible early (does the halt "
    "guard read the current state only, or a running balance?) and should "
    "be the first classification made."))
story.append(P(
    "<b>P8 &mdash; the Borel&ndash;Cantelli dichotomy (new, and it is the "
    "<i>right</i> dichotomy &mdash; the one the growth-rate contrast of "
    "Section 6 is not).</b> Every cryptid presents a stream of halting "
    "opportunities with per-opportunity probabilities p<sub>n</sub>; the "
    "wiki&rsquo;s two probvious verdicts are exactly the two halves of "
    "Borel&ndash;Cantelli. This is the split that matters, and all four of "
    "our machines fall on the same side of it (&Sigma;p<sub>n</sub> "
    "converges &mdash; the explorations report confirms their return maps "
    "are all supercritical); geometric-vs-linear growth is a separate, "
    "risk-neutral axis. &Sigma;p<sub>n</sub> "
    "divergent &rarr; probviously halting: Lucy&rsquo;s Moonlight&rsquo;s "
    "epochs carry a <i>constant</i> halt chance each. &Sigma;p<sub>n</sub> "
    "convergent &rarr; probviously non-halting: "
    "Antihydra&rsquo;s chances shrink like a golden-ratio "
    "power of its walk height, machine 1&rsquo;s like the density of a "
    "geometrically-thinning family."))
story.append(P(
    "<b>P9 &mdash; the bounded-resource wall (new; the shape every negative "
    "result in this program has turned out to share).</b> Each decision method "
    "the program has built is exact up to a bound on one resource and "
    "<i>provably silent</i> beyond it, and the resource is different every "
    "time: automaton size for automatic-invariant certificates (Section "
    "2.2), backward depth for the halting-density count, and the number of "
    "composed steps for the congruence sieve. What makes this a pattern rather "
    "than three disappointments is that the price of one more unit of resource "
    "is measurable, and in each case it was measured: solver time rises by a "
    "factor of 5.5 to 10.2 per automaton state and the factor is itself "
    "growing; the density bound gains a factor of (log x) per unit of depth; "
    "and the sieve&rsquo;s position bound grows like q<sub>b</sub><super>n"
    "&minus;1</super> per rung, which is why that ladder stops after one rung "
    "(two on machine 3) instead of climbing. A method whose cost per unit of "
    "reach grows geometrically does not fail at a size &mdash; it fails at a "
    "<i>rate</i>, and the rate is the honest content of the negative result. "
    "This is also what separates these bounds from the no-congruence theorems "
    "of P3: those are unconditional impossibilities, whereas P9 bounds are "
    "exhaustion statements, and conflating the two would overclaim. <i>Next "
    "machine: before running any bounded search, identify which resource "
    "bounds it and measure the cost per unit; report the growth rate alongside "
    "the reach, because the rate is what tells the reader whether the wall is "
    "worth pushing.</i>"))
story.append(P(
    "<b>P9 sharpened: the exchange rate.</b> Because the cost per unit is "
    "geometric with ratio g, an engineering improvement worth a constant "
    "factor C buys exactly log<sub>g</sub>(C) units of reach &mdash; and the "
    "measured g are 8.38 per state for the LSB search, 4.01 for MSB, 13.37 for "
    "the 0-invariant convention. This converts speculation about optimisation "
    "into arithmetic, and it has now been tested twice, prospectively. Handing "
    "the solver the halting basin was worth a factor of about 1.3, i.e. "
    "log<sub>8.38</sub>(1.3) = <b>0.12 states</b>; the prediction beforehand "
    "was &ldquo;several states&rdquo;, and the measured outcome was an eighth "
    "of one. Rewriting the whole search MSB-first was worth a factor of 42 at "
    "n = 10, i.e. <b>2.1 states</b>. That second prediction was settled by "
    "datapoints that arrived after the formula was fixed, and so test it "
    "rather than feed it &mdash; but they settled it at a range, not a "
    "number: n = 12 refuted in 1,679 s gives MSB a reach of 12 against the "
    "LSB search&rsquo;s 10 at a matched budget of 1,874 s, <b>a gain of 2</b>; "
    "the LSB search then completed n = 11 in 16,538 s, and at that budget of "
    "17,703 s the same comparison <b>reads 1</b> (Section 2.7). Inverted, the "
    "rate says what any future proposal must deliver: 3 more states needs a "
    "588-fold improvement, 5 needs 41,300-fold, 10 needs a factor of "
    "1.7&times;10<super>9</super>. "
    "<i>The triage question for anything proposed in this line is therefore "
    "not &ldquo;is it faster?&rdquo; but &ldquo;does it change g, or only win "
    "a constant?&rdquo;</i> Of the two improvements tried, the basin won a "
    "constant outright; the MSB rewrite looked like a constant and on closer "
    "reading bought a slightly smaller g over the range it covered, which is "
    "why it paid at all &mdash; see the next paragraph, where that reading is "
    "set against the fact that g is itself rising. A "
    "method that changed g would have to change the shape of the search "
    "&mdash; compositional or abstraction-refinement construction rather than "
    "a flat sweep over structures &mdash; and none of the certificate machinery "
    "in this program does that."))
story.append(P(
    "<b>The correction the confirming datapoint also forced: g is not a "
    "constant, it rises.</b> The exchange rate above treats the per-unit cost "
    "factor as fixed, which is how a single g can be quoted per encoding. The "
    "measured factors say otherwise &mdash; MSB pays 3.00, 4.33, 3.46, 5.47, "
    "6.70, 10.18 as n climbs; the LSB general search 7.00, 6.57, 5.53, 10.24, "
    "15.89; the 0-invariant convention 9.64 then 18.55; and machine 3, in "
    "base 3, "
    "3.38, 12.62, then <b>53.20</b> &mdash; the steepest step measured anywhere "
    "in this program, 226 s at n = 6 against 12,018 s at n = 7. <i>In all four "
    "independent series the largest factor is the last one.</i> (Machine 3 is a "
    "different map with a far larger encoding, 73.2 million clauses at n = 7, "
    "so its absolute rate is not comparable to the Needle&rsquo;s; what "
    "transfers is the direction.) Two consequences, in "
    "opposite directions. In MSB&rsquo;s favour, its advantage was never a "
    "flat constant: the LSB-to-MSB ratio at matched n runs 4.00, 9.33, 14.15, "
    "22.60, 42.32, 100.29 for n = 6 to 11, so it compounds, and MSB "
    "genuinely does carry the smaller per-state factor &mdash; the good kind "
    "of win by this section&rsquo;s own test, and it has not stopped "
    "compounding. <b>A second input was not constant either.</b> The formula "
    "takes a constant improvement C and returns log<sub>g</sub>(C) states, "
    "but C is measured at a particular n and is itself growing &mdash; from "
    "42 at n = 10 to 100 at n = 11 &mdash; so both of its arguments drift. "
    "Two encodings with different growth rates do not differ by a constant "
    "factor at all, and a reach gap between them is not a fixed number of "
    "states. <i>The qualification recorded in advance, now activated:</i> a "
    "reach gap is a function of the budget one fixes. It is 2 at the matched "
    "cumulative budget of 1,874 s, where MSB stands at 12 and LSB at 10; the "
    "LSB n = 11 instance, then still running, has since completed in "
    "16,538 s, and at that budget of 17,703 s LSB reaches 11 while MSB is "
    "still at 12, so the gap <b>reads 1</b>. The two readings bracket the "
    "formula rather than pinning it: 1.99 states from C = 100 against "
    "MSB&rsquo;s current slope, 1.67 against the LSB slope, 3.32 against "
    "MSB&rsquo;s mean g. What is confirmed is the order of the answer &mdash; "
    "the best available encoding change is worth one or two states, not an "
    "order of magnitude &mdash; and that was the claim that mattered. What is "
    "not confirmed is any particular number, and the withdrawn "
    "&ldquo;unchanged gradient&rdquo; reading went with it: LSB pays "
    "15.89&times; at its newest step against MSB&rsquo;s 10.18&times;, so the "
    "two gradients are not equal and MSB is still the cheaper encoding. The "
    "arithmetic consequence is that "
    "log<sub>g</sub>"
    "(C) computed from a <i>mean</i> g overstates what a constant buys, and "
    "increasingly so with n, which makes the inverse figures just quoted "
    "&mdash; 588-fold for 3 states, 41,300-fold for 5 &mdash; <b>optimistic "
    "lower bounds on the true price</b>. The conclusion they support, that no "
    "further states are worth buying, is strengthened rather than weakened. "
    "<i>Caveat carried openly:</i> these runs were made concurrently on one "
    "10-core machine at varying load, so cross-run absolute times carry "
    "perhaps &plusmn;30%. A factor of 42 is far outside that noise; a single "
    "step&rsquo;s 6.70 against 10.18 is not. What survives the noise is the "
    "qualitative claim, and it survives because it repeats in four "
    "independent series, across two machines and three conventions."))
story.append(P(
    "The comparison of machine 4 with "
    "Lucy&rsquo;s Moonlight is the clean controlled experiment: <i>the same "
    "section/epoch architecture and the same probviously-halting verdict, "
    "differing only in how fast the opportunities thin out</i>. On any new machine, computing the "
    "opportunity stream and testing &Sigma;p<sub>n</sub> is the fastest "
    "route to the expected verdict &mdash; and the honest statement of what "
    "remains open is always the same: Borel&ndash;Cantelli needs "
    "independence-like structure that no one can prove for a single "
    "deterministic orbit."))

# ================= 6. traps =================
story.append(P("8. Cross-machine structure: what zooming out revealed", H1))
story.append(P(
    "Stepping back from the individual machines to try ideas from the "
    "generalized-Collatz literature turned up six cross-cutting findings "
    "(full detail and verification in the explorations report). One is a "
    "correction, already folded into Section 6; the others locate or pin down "
    "structure that the per-machine reports had left open or vague."))
story.append(tab([
    ("1. Drift dichotomy (correction)",
     "All five return maps are supercritical (drift 0.33&ndash;0.99), so "
     "&Sigma;1/C<sub>n</sub> converges for every machine by the same "
     "mechanism &mdash; the divergent/convergent split is per-step growth "
     "(frequent vs thinning returns), not halting risk (Section 6)."),
    ("2. The mantissa backbone, located",
     "Machine 1&rsquo;s mantissa (its open &ldquo;missing backbone&rdquo;) "
     "evolves by an explicit two-branch circle map with breakpoint exactly "
     "log<sub>2</sub>(5/4); its transfer operator has spectral gap 0.77 "
     "(strongly mixing), density 1.12&times; below the breakpoint and "
     "0.94&times; above, with a jump there."),
    ("3. No congruence decides the multiplicative machines",
     "Machine 3 and the Space Needle branch on the q-adic valuation, which is "
     "independent of residues mod any M coprime to q &mdash; so no congruence "
     "closure exists. &ldquo;No separating modulus&rdquo; is now a theorem, "
     "not a search outcome (the multiplicative analogue of the Hydra q-adic "
     "result, P3)."),
    ("4. A self-similarity relation",
     "The Space Needle obeys step(2b) = step(b) + b + 1 exactly; machine "
     "3&rsquo;s divide-chain lemma is its &times;3 analogue. Exact "
     "renormalization structure, linking halt targets across scales."),
    ("5. The halting set, computed backward",
     "Enumerating the Space Needle&rsquo;s halting set backward from the "
     "powers of 2 gives only ~16 seeds below 2&times;10<super>6</super> "
     "(~log-many below N, density decaying geometrically); the start is "
     "provably not among them &mdash; non-halting corroborated from the "
     "target side."),
    ("6. Baker reaches the runs, not the orbit",
     "The orbit is not an S-unit sequence, so Baker cannot touch it directly; "
     "but per geometric run, halting is an S-unit equation, and "
     "lifting-the-exponent forces any halt to sit at a run boundary, never "
     "in the interior of an ascent (run length &le; ~1 + "
     "log<sub>5</sub>log<sub>2</sub>B). First time linear-forms-in-logs is "
     "aimed at a cryptid&rsquo;s halting family."),
], ("finding", "what it says"), (2.05 * inch, 4.6 * inch)))
story.append(Spacer(1, 4))
story.append(P(
    "The findings converge on one picture, and it sharpens the program&rsquo;s "
    "third aim &mdash; the account of what makes the hard ones hard, the "
    "regular-invariant boundary of Section 4.4 &mdash; into something exact: "
    "<b>every tool stops at the same "
    "place &mdash; the branch word is orbit-determined and grows without "
    "bound.</b> Congruences cannot read it (3), Baker decides each fixed word "
    "but not their unbounded sequence (6), and the valuation process "
    "generating it is mixing with a positive spectral gap (2): structured "
    "enough to model precisely, random enough to defeat every finite "
    "invariant. The honest end state of the whole program is not a decision "
    "but a complete map of why one is out of reach, drawn tool by tool &mdash; "
    "together with the genuinely new structure above and the one unconditional "
    "partial result (no halt in the interior of a geometric run)."))

story.append(P("9. Collatz-equivalence and the hardness ordering", H1))
story.append(P(
    "A recurring question &mdash; what does it formally mean that these "
    "machines are &ldquo;Collatz-like,&rdquo; and are they equally hard? "
    "&mdash; is treated in full in the companion report (collatz/formal/). The "
    "summary: the slogan runs together three formally distinct questions."))
story.append(tab([
    ("(i) Is any machine the Collatz map?",
     "<b>No.</b> The maps are distinct; none is conjugate to n &rarr; n/2, "
     "3n + 1. Two internal equivalences do hold: Hydra &#8801; Antihydra (one "
     "map, floor(3n/2), two boundary conditions) and machine 3 &#8776; Space "
     "Needle (multiplicative, base 3 vs 2)."),
    ("(ii) Are they &ldquo;Collatz-like&rdquo; formally?",
     "<b>Yes.</b> All are generalized Collatz functions (Conway; "
     "Kurtz&ndash;Simon), the class whose totality is "
     "&Pi;<super>0</super><sub>2</sub>-complete &mdash; that membership is the "
     "precise content of the informal term. Hydra is a strict "
     "(finite-residue) member; the reduced return maps branch on q-adic "
     "valuations or digit words, a broader family the acceleration exposes."),
    ("(iii) As hard as the Collatz conjecture?",
     "<b>Not in logical level.</b> Each machine&rsquo;s non-halting is "
     "&Pi;<super>0</super><sub>1</sub> &mdash; one universal quantifier over a "
     "<i>single</i> orbit (like Antihydra) &mdash; one level <i>below</i> the "
     "&Pi;<super>0</super><sub>2</sub> Collatz conjecture. &ldquo;As hard as "
     "Collatz&rdquo; names the shared single-orbit pseudorandom obstruction, "
     "not the complexity; the honest same-level comparison is a single cryptid "
     "orbit against a single Collatz orbit."),
], ("question", "answer"), (2.15 * inch, 4.5 * inch)))
story.append(Spacer(1, 4))
story.append(P(
    "<b>The ranking.</b> Because a single fixed instance is one decidable bit, "
    "reductions only compare parametrized families; there is no established "
    "ordering among specific Collatz-like problems, so the following is ours "
    "to propose. On the primary axis &mdash; logical level and the "
    "pseudorandom obstruction &mdash; <b>all the machines tie</b> (and all sit "
    "below the conjecture). A partial order appears on secondary structure:"))
story.append(tab([
    ("Axis A: certified vs candidate",
     "For the multiplicative machines (3, Space Needle) it is a <b>theorem</b> "
     "that no congruence can decide halting (Section 8, Finding 3); for the "
     "sparse machines (1 and 4) that is only empirical. So certified "
     "(3, Needle) &gt; candidate (1, 4) in certainty of being a true "
     "cryptid."),
    ("Axis B: distance to a named problem",
     "Hydra/Antihydra and machine 1 (via its mantissa) sit in the "
     "(3/2)<super>n</super>-equidistribution circle of Mahler&rsquo;s "
     "Z-number problem &mdash; by analogy, not proven equivalence; the "
     "multiplicative machines are perfect-powers (Baker) territory; machine "
     "4 is freestanding."),
], ("axis", "ordering"), (1.7 * inch, 4.95 * inch)))
story.append(Spacer(1, 4))
story.append(P(
    "So the answer to &ldquo;equally hard, or ranked?&rdquo; is <b>both: equal "
    "at the core, ordered on the shell.</b> Hardness here is genuinely "
    "multi-dimensional and the deepest axis is flat; what distinguishes the "
    "machines is how much is <i>proven</i> around the irreducible core &mdash; "
    "and there the multiplicative pair stands out as the only members proven "
    "beyond elementary methods."))

story.append(P("10. The standard workflow for the next machine", H1))
story.append(P(
    "Distilled from the analyses; across the collection stages 1&ndash;6 have "
    "terminated with proofs every time, and stage 7 is where the open core is "
    "reached."))
story.append(Spacer(1, 6))
story.append(pipeline_diagram())
story.append(P(
    "<b>Figure 1.</b> The pipeline the machines followed. Every stage "
    "before the last has closed with theorems in every case; the last stage "
    "is where the single-orbit gap lives. One amendment from Section 7.1: "
    "the halting-condition type (coincidence / absorption / multiplicative) "
    "is visible in the raw guards and should be read off at stage 1.", FIGCAP))

# ================= 8. open =================
story.append(P("11. Methodological lessons (learned the hard way)", H1))
story.append(tab([
    ("consolidate the open items before working them",
     "five machines sat in a list of &ldquo;best open leads&rdquo; for a day, "
     "each described on its own and each looking like a separate research "
     "problem. Put side by side they were not: four shared a modulus "
     "identically, and one lemma closed three of them. Nothing was computed "
     "that had not been computable the day before. Writing the status board "
     "was the search that found it &mdash; so consolidate <i>before</i> deciding "
     "what to work on, not after."),
    ("delete the hypothesis you never tested",
     "the lemma that closed those three was written &ldquo;for &alpha; = 2, "
     "&beta; = &minus;1&rdquo; because that is the corner it was found in "
     "&mdash; not because the derivation used either value, which it does not "
     "(Section 2.11). That unexamined phrase kept two theorems classified as "
     "open leads needing new ideas, and three more machines out of sight "
     "entirely. When a result is stated over the special case that produced "
     "it, re-read the proof and ask what it actually consumed; the "
     "generalisation is often free."),
    ("prefer the question the negative result answers",
     "two imports were commissioned and both failed: Skolem&rsquo;s witness "
     "machinery does not fit our equations, and the counting barrier is "
     "refuted by measured bandwidth. Each failure was worth more than its "
     "assignment &mdash; asking <i>why no witness modulus exists</i> produced "
     "T12, and asking <i>why counting cannot work</i> produced the observation "
     "that universality is a property of a single point, which retires the "
     "genre. When an import fails, extract the question it was answering "
     "before discarding it (Section 2.12)."),
    ("a filter chosen for one purpose bounds every later use of the list",
     "the all-branches-forbidden leads were drawn from undecided <i>growers</i>, "
     "which was right for the census's own question. Three machines with the "
     "same property were therefore never seen &mdash; two already decided by a "
     "weaker certificate, one with a cycle &mdash; and two of them turned out "
     "to be strict upgrades. Re-derive a candidate list from the property you "
     "now care about instead of reusing the one you have."),
    ("small-sample congruence artifacts",
     "with N samples, a residue class mod m is missed by chance with "
     "probability (1 &minus; 1/m)<super>N</super> &mdash; 12% already at "
     "m = 15, N = 31. Both machines produced spurious &ldquo;separating "
     "moduli&rdquo; this way; all vanished under proper sampling. Never "
     "report a separation without a sample-size argument."),
    ("accelerations must be verified step-exact",
     "machine 1's level-3 seed rule was wrong at exactly one input (b = 1) "
     "and survived until cross-verification against the anchor map caught "
     "it. Every level must reproduce the base machine on random states, "
     "and every deep run must reproduce earlier checkpoints."),
    ("vacuous tests pass silently",
     "a check over randomly sampled states that never hits the guarded "
     "case (0 cases, &ldquo;0 violations&rdquo;) proves nothing; construct "
     "the guarded case explicitly and count it."),
    ("later results invalidate earlier prose",
     "successive review rounds of the case-file reports each found claims made "
     "true-at-the-time and falsified by later theorems (e.g. &ldquo;a "
     "geometrically convergent sum&rdquo; after non-uniformity was proved). "
     "After any new theorem, sweep the whole document for now-stale claims."),
    ("a measurement that cannot fail is not evidence",
     "backward branching was measured against its rigorous ceiling on two "
     "machines, agreed to four decimals both times, and was written up as the "
     "quantitative form of the pseudorandomness heuristic. The agreement is "
     "forced &mdash; the side condition v<sub>2</sub>(b) = v is automatic, so "
     "the interval density <i>is</i> the ceiling by construction "
     "(Section 2.4). Before reporting an agreement as confirmation, ask what "
     "the measurement would have shown had the hypothesis been false; if the "
     "answer is &ldquo;the same thing&rdquo;, it is a consistency check, not "
     "evidence. Two machines agreeing does not help: both were forced."),
    ("run the statistic on a control whose answer you already know",
     "the same place caught the program twice. Section 2.4 discarded a "
     "measured <i>agreement</i> with the independence model as forced; the "
     "<i>disagreement</i> installed in its place &mdash; a 21% and 30% "
     "branching deficit along the backward tree &mdash; was forced too, by "
     "the arithmetic of the powers-of-q roots (Section 2.7). Both times the "
     "error was identical and invisible from inside the number: a statistic "
     "was compared against a null model that did not apply to the sample "
     "actually drawn. Asking what would have made it come out differently is "
     "necessary but was not sufficient here, because the answer looked like "
     "&ldquo;a different dynamics&rdquo;. What settled it in minutes was "
     "cheaper: <i>recompute the same statistic on a control sample whose "
     "answer is known</i> &mdash; generic roots instead of the halting set "
     "&mdash; and see whether the effect survives. It did not. Budget a "
     "control for every aggregate statistic that is about to be interpreted."),
    ("ask what would have made the measurement come out differently",
     "the umbrella over the two traps that follow, and the program made both "
     "within one day &mdash; the second while writing up the correction to the "
     "first. A branching ratio agreed with its ceiling because the agreement "
     "was forced (Section 2.4); a cost factor was quoted as one number per "
     "encoding because the window examined happened to be flat (Section 2.6). "
     "Each time a quantity stable across the range examined was reported as a "
     "property of the object rather than of the range. Two questions before "
     "quoting any measured regularity: what would have to be true for this to "
     "come out differently, and &mdash; if it is to be extrapolated or "
     "inverted &mdash; which way does it drift at the edge of the data? A "
     "third question earned the hard way: <i>grep the document for what it "
     "already says about the quantity.</i> The rising cost factor was recorded "
     "in Section 2.3, with the right conclusion drawn from it, before Section "
     "2.5 assumed it constant. A later section silently regressing against an "
     "earlier one is the same failure as a stale plan contradicting a fresh "
     "result, and it is caught the same way."),
    ("a growth rate fitted over a window is not a constant of the method",
     "the exchange rate log<sub>g</sub>(C) was derived treating the per-state "
     "cost factor g as fixed, and a single g was quoted per encoding from a "
     "geometric mean. The factors rise with n &mdash; the last step is the "
     "largest in all four independent series, and MSB&rsquo;s quoted g moved "
     "from 4.84 to 5.99 on the arrival of one further datapoint (Section 7). "
     "A mean over a window is a summary of that window, not a law; when it is "
     "then inverted to price future work, say which direction the drift "
     "biases the answer. Here it makes the prices quoted optimistic, which "
     "happens to strengthen the conclusion drawn &mdash; but that was luck, "
     "and the check is owed either way."),
    ("convert bounds into a common currency before ranking them",
     "three impossibility results were carried for weeks in three units "
     "&mdash; DFA states, congruence modulus, backward depth &mdash; which "
     "invites ranking them by the size of the number. Converted (Section 2.8), "
     "the one being quoted as the headline covered three moduli against a "
     "thirty-second script&rsquo;s twenty thousand. The conversion was twenty "
     "lines and should have been the first thing written, not the last."),
    ("when a sweep leaves survivors, diagnose them &mdash; do not widen the "
     "window until they vanish",
     "one modulus resisted the congruence sweep, and a genuine survivor would "
     "have been a <i>proof</i> of non-halting. Chasing it produced a new lemma "
     "(G(a) &#8801; v<sub>3</sub>(a) mod 2) and the correct probability model "
     "for its resistance. Widening the window alone would have produced a "
     "bigger number and no understanding."),
    ("&ldquo;arbitrarily large&rdquo; needs the residues taken infinitely "
     "often, not the residues taken",
     "an argument that a certificate cannot use a threshold has to collide the "
     "orbit against halting values <i>above</i> that threshold. Powers of q are "
     "only eventually periodic mod m, and the pre-period residues are taken "
     "finitely often &mdash; colliding against those is unsound, and the code "
     "reports success either way. Restricting to the eventual cycle fixed it "
     "and strengthened the theorem (Section 2.8)."),
    ("do not measure a growth constant under variable load",
     "a completed UNSAT survives a noisy box; the constant that prices it does "
     "not. Every per-state factor here came from concurrent runs, and "
     "re-measuring one process at a time moved them by about threefold and "
     "turned a non-monotone series monotone. Budget one clean sequential pass "
     "before quoting any ratio of running times."),
    ("keep proved / verified / heuristic distinct",
     "10<super>150,514</super> verified steps is not a proof; an "
     "average-case risk figure is not a bound. Both reports state, next to "
     "every claim, which of the three it is &mdash; this discipline is what "
     "made the honest endpoints clear."),
], ("trap", "the lesson"), (1.8 * inch, 4.9 * inch)))

# ================= 7. workflow =================
story.append(P("12. Open problems across the collection", H1))
story.append(P(
    "<b>Status in one line:</b> every machine is fully reduced and "
    "provably non-cycling; each halting question is settled down to a single "
    "&Pi;<super>0</super><sub>1</sub> orbit-avoidance statement (Section 9), "
    "and there &mdash; and only there &mdash; each remains open, for the same "
    "reason Collatz is. The concrete open questions, and what is known toward "
    "each, are the natural entry points for continuing the work:"))
story.append(tab([
    ("machine 1", "does the F-orbit of 17 avoid H forever?",
     "equivalent to the machine's non-halting; open"),
    ("machine 1", "the exact stationary density of the mantissa "
     "frac(log<sub>2</sub> D<sub>k</sub>)",
     "<b>located</b> (Section 8, Finding 2): a two-branch circle map, "
     "breakpoint log<sub>2</sub>(5/4), spectral gap 0.77. A closed form for "
     "the density (Perron&ndash;Frobenius) is the remaining step"),
    ("machine 3", "does the a-orbit of A(1,1) ever hit a power 27<super>m</super>?",
     "equivalent to non-halting; the multiplicative target has never been "
     "hit in 3&times;10<super>6</super> steps. Newly unconditional (Section "
     "2.16): <b>no modulus separates machine 3</b> (M3-N1), and the last two "
     "steps before any halt have v<sub>3</sub> = 1 for every j (M3-N2, "
     "95.06% of pairs excluded, now exact)"),
    ("machine 4", "does the orbit ever land on b = a + 3 (a odd)?",
     "equivalent to non-halting; closest approach so far is distance 1, "
     "never 0"),
    ("Hydra family", "does H(n) from n = 8 keep #odd &le; 2&middot;#even "
     "forever (Antihydra)?", "the family&rsquo;s open cores; tied to "
     "(3/2)<super>n</super> equidistribution / Mahler&rsquo;s problem"),
    ("all", "any bounded-state invariant separating orbit from target",
     "none found (m &le; 256 / m &le; 628); and now a <b>theorem</b> that no "
     "congruence invariant of the value can decide halting &mdash; for the "
     "Hydra family (q-adic branch memory, Section 5.4) and for the "
     "multiplicative machines 3 and Space Needle (Section 8, Finding 3). "
     "Widened from congruences to <i>automatic</i> sets, still none: no "
     "certificate at &le; 11 LSB states for the Needle, &le; 7 for machine 3 "
     "(Section 2.2). Conway&rsquo;s undecidability says only "
     "instance-specific structure could do it. Sharpened in the congruence "
     "direction to <b>every m &le; 20,000 with any threshold</b>, which also "
     "disposes of the whole one-variable semilinear class and every "
     "bbchallenge regular decider (Section 2.8). The branch sieve is now "
     "<b>complete</b> on the census family &mdash; it decides exactly ten "
     "machines and every other member carries an explicit surviving-branch "
     "certificate (Section 2.11), so this route is closed with a proof rather "
     "than a budget"),
    ("the syntax itself",
     "is the one-schema valuation class (VAL(q), a single affine-in-"
     "q<super>v</super> rule) Turing-complete?",
     "<b>open, and the only two-sided bet the program holds.</b> Universality "
     "would make the size frontier vacuous for our machines and give their "
     "resistance a structural cause; a decision procedure for the class would "
     "<i>decide our cryptids</i>. Known: the residue-branched sibling RES(d) is "
     "Turing-complete (verified compiler, &le; 2I rules, Section 2.8), and "
     "nothing lower-bounds VAL(q)"),
    ("Needle, machine 3",
     "is there an automatic non-halting certificate of <i>any</i> size?",
     "<b>open, and the sharpest new question the program has produced.</b> "
     "Conjecture: every nonempty 2-automatic F-invariant meets H. The bounded "
     "searches are exhaustion, not impossibility (P9), so they do not bear on "
     "it. The sub-question that had a real chance of a <i>positive</i> answer "
     "&mdash; all bounds are on LSB-first state count, and an MSB-first "
     "automaton for the same set can be exponentially smaller &mdash; has "
     "since been closed negatively to 13 states (Section 2.2). Because the "
     "exchange rate of Section 2.5 makes further search worthless, this "
     "question is now a <i>proof</i> target, and the lever is WS1&rsquo;s own "
     "finding: a certificate must avoid the whole halting basin, not just H"),
    ("Needle, machine 3", "unbounded-depth halting density",
     "open. #{starts &le; x halting within L steps} is polylogarithmic and "
     "exactly counted for each fixed L (Section 2.2); removing the dependence "
     "on L would assert that all but O(x<super>c</super>) starts never halt, a "
     "single-orbit claim of Collatz strength. What the theorem needs is a "
     "bound on branching <i>along the backward tree</i>. Measured there it is "
     "0.433 on the Needle and 0.500 on machine 3, against interval ceilings "
     "of 0.5453 and 0.8081; the gap is now explained &mdash; it is the "
     "arithmetic of the powers-of-q roots, not a departure from randomness "
     "(Section 2.7), and the root row is predicted exactly. Proving any bound "
     "c &lt; 1 <i>uniformly along the tree</i>, not merely at the root or on "
     "average, is the open step"),
    ("Needle", "is 2v &minus; 3 in "
     "{&plusmn;3<super>a</super>2<super>i</super>} mod 2<super>v+1</super>+3, "
     "for infinitely many v?",
     "<b>open &mdash; and this is now the sharpest statement of the "
     "Needle&rsquo;s difficulty the program has.</b> By the universal sieve "
     "lemma (Section 2.11) a branch can precede a halt exactly when this "
     "2,3-S-unit membership holds. Measured: 18 of the first 41 branches "
     "satisfy it and the set does <i>not</i> thin out, so the sieve saturates "
     "near 28.7% of weight and no asymptotic exclusion is available this way. "
     "120 census machines share the same group. Nothing in the literature "
     "decides membership of a linear form in {&plusmn;3<super>a</super>"
     "2<super>i</super>} modulo a shifted power of two"),
    ("the syntax itself",
     "does every one-schema VAL(2) machine with a non-halting orbit have a "
     "<i>local</i> certificate?",
     "<b>open, and newly nameable: this is Skolem&rsquo;s conjecture for our "
     "family.</b> T1&ndash;T11 are exactly explicit local witnesses, and the "
     "program&rsquo;s certificate searches have been Skolem-witness searches "
     "without saying so. The conjecture predicts a witness exists whenever "
     "non-halting is true; for the Needle we now know the answer exactly: "
     "<b>no congruence witness exists at any modulus</b> (T15, Section 2.15), "
     "so if the Needle does not halt and Skolem-type completeness is to hold "
     "for this family, the witness must come from a richer certificate class "
     "than congruences &mdash; which is what the automatic-invariant "
     "conjecture asks"),
    ("machine 3", "does the orbit hit an exact power of q?",
     "open; not an S-unit sequence, so Baker applies per-run but not globally "
     "&mdash; halts (if any) sit at run boundaries, never mid-ascent "
     "(Section 8, Finding 6). Unconditionally narrowed since: no halt can "
     "follow a step of 19 of the first 35 valuations on the Needle (28.7% of "
     "steps), and machine 3&rsquo;s last two steps before any halt must both "
     "have v<sub>3</sub> = 1 (95.06% of pairs) &mdash; Section 2.2"),
], ("machine", "problem", "state"),
   (0.8 * inch, 2.9 * inch, 3.0 * inch)))

story.append(P("References", H1))
refs = [
 "J. C. Lagarias, The 3x+1 problem and its generalizations, Amer. Math. "
 "Monthly 92 (1985) 3&ndash;23.",
 "J. C. Lagarias, The 3x+1 problem: an overview, arXiv:2111.02635 (2021); "
 "and (ed.) The Ultimate Challenge: The 3x+1 Problem, AMS, 2010.",
 "T. Tao, Almost all orbits of the Collatz map attain almost bounded "
 "values, Forum of Mathematics, Pi 10 (2022) e12; arXiv:1909.03562.",
 "J. H. Conway, Unpredictable iterations, Proc. 1972 Number Theory Conf., "
 "Boulder (1972) 49&ndash;52; FRACTRAN, in Open Problems in Communication "
 "and Computation, Springer (1987); On unsettleable arithmetical problems, "
 "Amer. Math. Monthly 120 (2013) 192&ndash;198.",
 "S. A. Kurtz, J. Simon, The undecidability of the generalized Collatz "
 "problem, TAMC 2007, LNCS 4484, 542&ndash;553.",
 "R. Terras, A stopping time problem on the positive integers, Acta Arith. "
 "30 (1976) 241&ndash;252; C. J. Everett, Adv. Math. 25 (1977) 42&ndash;45.",
 "I. Krasikov, J. C. Lagarias, Bounds for the 3x+1 problem using "
 "difference inequalities, Acta Arith. 109 (2003) 237&ndash;258.",
 "C. Hercher, There are no Collatz m-cycles with m &le; 91, J. Integer "
 "Sequences 26 (2023) 23.3.5.",
 "D. Barina, Improved verification limit for the convergence of the "
 "Collatz conjecture, J. Supercomputing 81 (2025) 810; earlier 77 (2021) "
 "2681&ndash;2688.",
 "A. V. Kontorovich, J. C. Lagarias, Stochastic models for the 3x+1 and "
 "5x+1 problems, in The Ultimate Challenge, AMS (2010) 131&ndash;188; "
 "J. C. Lagarias, A. Weiss, Ann. Appl. Probab. 2 (1992) 229&ndash;261.",
 "K. R. Matthews, A. M. Watts, A generalization of Hasse's generalization "
 "of the Syracuse algorithm, Acta Arith. 43 (1984) 167&ndash;175.",
 "K. Mahler, An unsolved problem on the powers of 3/2, J. Austral. Math. "
 "Soc. 8 (1968) 313&ndash;321.",
 "The bbchallenge Collaboration, Determination of the fifth Busy Beaver "
 "value, arXiv:2509.12337 (2025); also Turing machines deciders, part I, "
 "arXiv:2504.20563 (2025).",
 "C. Xu, Skelet #17 and the fifth Busy Beaver number, arXiv:2407.02426 "
 "(2024); S. Ligocki, blog analyses of Bigfoot, Hydra, Skelet #1 "
 "(sligocki.com, 2023&ndash;2024).",
 "BusyBeaverWiki, pages: Cryptids, Antihydra, Hydra, Bigfoot, Bonus "
 "cryptid, Lucy's Moonlight, Space Needle, Fenrir, Hydra function, BB(6), "
 "Probviously (wiki.bbchallenge.org, accessed July 2026).",
 "E. Yolcu, S. Aaronson, M. J. H. Heule, An automated approach to the "
 "Collatz conjecture, CADE-28 (2021); J. Automated Reasoning 67 (2023).",
 "K. Hicks, G. L. Mullen, J. L. Yucas, R. Zavislak, A polynomial analogue "
 "of the 3n+1 problem, Amer. Math. Monthly 115 (2008) 615&ndash;622.",
]
REFSTYLE = ParagraphStyle("Refx", parent=BODY, fontSize=8.8, leading=11.5,
                          spaceAfter=3, leftIndent=18, firstLineIndent=-18)
for i, r in enumerate(refs, 1):
    story.append(P(f"[{i}]&nbsp;&nbsp;{r}", REFSTYLE))

story.append(Spacer(1, 10))
story.append(HRFlowable(width="100%", thickness=0.8, color=BLUE))
story.append(Spacer(1, 4))
story.append(P(
    "<i>This document is meant to stay current: when a new machine is "
    "analyzed, add a case file in Section 5, a column-worth of rows in "
    "Section 6, and test every pattern in Section 7 against it &mdash; "
    "promoting patterns that hold, demoting ones that break.</i>",
    ParagraphStyle("Foot", parent=BODY, fontSize=9.5,
                   textColor=colors.HexColor("#555555"))))

class TOCDoc(BaseDocTemplate):
    """Doc template that feeds top-level (H1x) headings to the TableOfContents."""
    def afterFlowable(self, flowable):
        if flowable.__class__.__name__ == "Paragraph" and \
                getattr(flowable.style, "name", "") == "H1x":
            self.notify("TOCEntry", (0, flowable.getPlainText(), self.page))


doc = TOCDoc(OUT, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
             topMargin=0.8 * inch, bottomMargin=0.8 * inch,
             title="Collatz-Like Machines and Cryptids: Field Notes")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame])])
doc.multiBuild(story)
print("wrote", OUT)
