"""Build the WS1 report: automatic non-halting certificates for the Space Needle."""
import re

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.colors import HexColor

OUT = "/Users/tomzahavy/Documents/Claude/collatz/automatic/ws1_report.pdf"
HERE = "/Users/tomzahavy/Documents/Claude/collatz/automatic/"

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=styles["Heading1"], spaceBefore=16, spaceAfter=7,
                    fontSize=14)
H2 = ParagraphStyle("H2x", parent=styles["Heading2"], spaceBefore=12, spaceAfter=5,
                    fontSize=11.5)
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
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#e8eef7")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, HexColor("#f6f8fb")])]))
    return t


def scan_log(path):
    """Parse 'n= 7  structures=256,182,290  REFUTED ...' lines from a run log."""
    out = {}
    try:
        for line in open(path):
            m = re.match(r"\s*n=\s*(\d+)\s+structures=\s*([\d,]+)\s+(.*?)\s{2,}"
                         r"([\d.]+)s", line)
            if m:
                out[int(m.group(1))] = (m.group(2), m.group(3).strip(),
                                        m.group(4))
    except FileNotFoundError:
        pass
    return out


started = scan_log(HERE + "n1_6.log")
started.update(scan_log(HERE + "n7.log"))
free = scan_log(HERE + "anystart_n6.log")
KNOWN = {1: "1", 2: "12", 3: "216", 4: "5,248", 5: "160,675", 6: "5,931,540",
         7: "256,182,290"}
NMAX_START = max(started) if started else 6
NMAX_FREE = max(free) if free else 5

story = []
story.append(P("Automatic non-halting certificates for the Space Needle", TITLE))
story.append(P("WS1, first execution &mdash; an impossibility theorem at "
               "bounded size, with audited witnesses &mdash; July 26, 2026", SUB))
story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=12))

# ---------------------------------------------------------------- 1 result --
story.append(P("1. What was asked, and what came out", H1))
story.append(P(
    "The plan&rsquo;s top-priority workstream asks whether the Space "
    "Needle&rsquo;s non-halting can be certified by an <b>automatic set</b>: a "
    "set I of positive integers, recognised by a finite automaton reading "
    "binary digits, with"))
story.append(P("6 &isin; I,&nbsp;&nbsp;&nbsp; F(I) &sube; I,"
               "&nbsp;&nbsp;&nbsp; I &cap; H = &empty;", MATHC))
story.append(P(
    "where F is the one-variable Space Needle map and H = {1, 2, 4, 8, &hellip;} "
    "is its halting set. Any such I is a complete, finite, machine-checkable "
    "proof that the orbit of 6 never halts. This is the one certificate class "
    "that the collection&rsquo;s no-congruence theorems do not already "
    "exclude, and nobody has pointed it at an arithmetic Collatz-like map "
    "before."))
story.append(P(
    f"<b>Result (machine-verified).</b> There is no such I with at most "
    f"<b>{NMAX_START} states</b>. The search is exhaustive over all "
    f"{KNOWN.get(NMAX_START, '?')} transition structures of that size (every "
    f"isomorphism class exactly once) and exact for each: given a structure, "
    f"whether ANY acceptance labelling works is decided by Horn propagation, "
    f"not sampled. A stronger, start-free statement also holds: there is no "
    f"nonempty automatic I with F(I) &sube; I and I &cap; H = &empty; at all "
    f"with at most <b>{NMAX_FREE} states</b> &mdash; so at these sizes "
    f"automatic certificates cannot decide <i>any</i> start of this map, not "
    f"only 6."))
story.append(P(
    "<b>And the obstruction is dynamical, not a failure to see.</b> The "
    "natural worry about a bounded search like this is that small automata "
    "simply cannot tell the orbit apart from the powers of 2, in which case "
    "the theorem would be about digit complexity rather than about the map. "
    "That is measured in Section 6 and it is not what happens: at 3, 4 and 5 "
    "states there are 4, 100 and 2,887 structures that <i>do</i> separate the "
    "orbit from H, and closure destroys every one of them &mdash; each with an "
    "explicit witness, audited by direct simulation."))

# ------------------------------------------------------------------ 2 map ---
story.append(P("2. The identity that makes this computable", H1))
story.append(P(
    "Write x = 2<super>v</super>(2k + 1) with v = v<sub>2</sub>(x), so the "
    "LSB-first word of x is 0<super>v</super>1&middot;w(k). The published map "
    "x &rarr; x + v + (3/2)(x/2<super>v</super> &minus; 1) is then"))
story.append(P("F(x) = x + 3&middot;(x &gt;&gt; (v+1)) + v = "
               "(2<super>v+1</super> + 3)&middot;k + (2<super>v</super> + v)",
               MATHC))
story.append(P(
    "(verified against needle.step1 for every non-power-of-2 x &lt; 300,000). "
    "Each valuation branch is therefore an <b>affine map in k</b>. That is the "
    "whole enabling step: multiply-and-add in base 2 is a finite carry "
    "automaton, so for a fixed DFA the set of state pairs (state on x, state "
    "on F(x)) realised inside branch v is computed <i>exactly</i> by a product "
    "of three finite components &mdash; DFA-state on x, carry, DFA-state on y "
    "&mdash; with carries bounded by max(a<sub>v</sub>, b<sub>v</sub>). Branch "
    "v = 0 is the odd branch x &rarr; (5x &minus; 3)/2, i.e. "
    "(a, b) = (5, 1); then (7, 3), (11, 6), (19, 11), (35, 20), &hellip;"))
story.append(P("2.1 A local-action lemma (new, and useful beyond WS1)", H2))
story.append(P(
    "Because F(x) = x + 3k + v, if 3k + v &lt; 2<super>v</super> the three "
    "pieces of the sum occupy disjoint bit ranges, so the LSB-first word of "
    "F(x) is"))
story.append(P("(v + 3k) in v bits&nbsp;&middot;&nbsp;1&nbsp;&middot;&nbsp;w(k)",
               MATHC))
story.append(P(
    "&mdash; the high part k is carried through untouched and only the low "
    "block of zeros is rewritten; and then "
    "v<sub>2</sub>(F(x)) = v<sub>2</sub>(3k + v). Proof is the disjointness of "
    "the ranges; checked on 29,414 (v, k) pairs as well. It says the map acts "
    "<i>locally on the low digits</i> whenever the valuation is large "
    "relative to the tail, which is also the regime the density workstream "
    "(WS2) has to count."))

# -------------------------------------------------------------- 3 method ----
story.append(P("3. Why the search is a decision procedure, not a sampling", H1))
story.append(tab([
    ("Search space",
     "Canonical initially-connected DFAs by BFS numbering: each isomorphism "
     "class of transition structures appears exactly once. Counts produced by "
     "the generator are 1, 12, 216, 5,248, 160,675, 5,931,540, 256,182,290, "
     "matching the known initially-connected-DFA counts for a two-letter "
     "alphabet &mdash; an independent check that the enumeration is complete "
     "and non-redundant. Structures with unreachable states are covered by "
     "the smaller sizes."),
    ("Labelling",
     "For a fixed structure, each realised pair (p, q) is an implication "
     "acc(p) &rArr; acc(q); orbit elements are TRUE units; states of powers "
     "of 2 are FALSE units. That is a Horn system, so propagating TRUE from "
     "the units gives the least model: the structure admits a certificate iff "
     "propagation forces no FALSE unit. Exact, not heuristic."),
    ("Convention",
     "I is decided on <i>minimal</i> LSB words &mdash; the general meaning of "
     "&ldquo;2-automatic&rdquo;, with no normalisation. (Demanding a "
     "trailing-zero-invariant DFA instead is a special case and would make "
     "the theorem weaker.) The product therefore also tracks the y-state just "
     "after the last emitted 1, which is where y&rsquo;s minimal word ends."),
    ("Partial branch budget",
     "Only branches v &le; V are imposed. Those conditions are a subset of "
     "full closure, so refutation stays sound: an unsatisfiable subsystem "
     "means no certificate exists. (A survivor would be only a candidate, "
     "owing the branches v &gt; V.) Diagnostics: the branches v &le; 1 "
     "already suffice at every size tested."),
    ("Exactness of the pair sets",
     "branch_pairs and branch_pairs_min are tested against brute-force "
     "enumeration of the actual (v, k) instances &mdash; equality of sets, "
     "not containment, for k &lt; 20,000 and several structures &mdash; so "
     "the product neither invents pairs (which could refute wrongly) nor "
     "misses them."),
], ("component", "why it is sound"), (1.25 * inch, 5.05 * inch)))

# ------------------------------------------------------------- 4 results ----
story.append(P("4. Results", H1))
rows = []
for n in sorted(set(list(started) + list(free) + list(range(1, 8)))):
    if n > max(NMAX_START, NMAX_FREE):
        continue
    a = started.get(n)
    b = free.get(n)
    rows.append((str(n), KNOWN.get(n, "?"),
                 ("no certificate" if a and "REFUTED" in a[1] else
                  (a[1] if a else "&mdash;")),
                 ("no invariant" if b and "NONE" in b[1] else
                  (b[1] if b else "&mdash;")),
                 (a[2] + " s" if a else "&mdash;")))
story.append(tab(rows, ("states n", "structures searched",
                        "certificate for the orbit of 6", "any nonempty "
                        "F-invariant avoiding H", "runtime"),
                 (0.6 * inch, 1.25 * inch, 1.65 * inch, 1.7 * inch, 0.7 * inch)))
story.append(P(
    "Both columns are exhaustive at their size. The start-free column is the "
    "stronger claim and was run with the cheaper branch budget v &le; 4; the "
    "orbit column used v &le; 6. Every entry is a complete search, so the "
    "table reads as a single theorem: <b>no automatic certificate for this "
    "map exists below the stated sizes</b>.", BODY))

# ---------------------------------------------------------- 5 calibration ---
story.append(P("5. Calibration: the search finds certificates when they exist", H1))
story.append(P(
    "An impossibility result from a search is worth exactly as much as the "
    "search&rsquo;s ability to succeed. The same code was run on a control "
    "machine with the same halting set and the same branch format &mdash; "
    "C(x) = 4x, written as a<sub>v</sub> = 2<super>v+3</super>, "
    "b<sub>v</sub> = 2<super>v+2</super> &mdash; whose orbit from 6 is "
    "6, 24, 96, 384, &hellip; It finds a certificate at <b>2 states</b>: "
    "I = {x : x has an even number of 1 bits}, which contains 6, is preserved "
    "by x &rarr; 4x (a shift), and misses every power of 2 (one 1 bit). The "
    "certificate is then re-verified by brute force against the actual map "
    "over x &lt; 200,000, not merely accepted from the search. So the "
    "machinery does produce certificates; the Needle simply has none at these "
    "sizes."))

# ------------------------------------------------------------- 6 anatomy ---
story.append(P("6. Anatomy of the impossibility: separation versus closure", H1))
story.append(P(
    "Two quite different things could kill a structure. Either it cannot "
    "<b>separate</b> the orbit from H at all &mdash; some orbit element and "
    "some power of 2 reach the same state, a statement about digit complexity "
    "with no dynamics in it &mdash; or it separates them and then "
    "<b>closure</b> drags a power of 2 in. Only the second is about the map. "
    "The split, measured exhaustively:"))
story.append(tab([
    ("3", "216", "4", "0", "4"),
    ("4", "5,248", "100", "0", "100"),
    ("5", "160,675", "2,887", "0", "2,887"),
], ("states", "structures", "separate the orbit from H",
    "survive closure too", "killed by closure"),
    (0.7 * inch, 1.0 * inch, 1.7 * inch, 1.2 * inch, 1.1 * inch)))
story.append(P(
    "Every separating structure dies, and dies at the <i>first</i> closure "
    "step: in all 504 audited cases the witness chain has length one. The "
    "mechanism is concrete and always the same shape. Membership depends only "
    "on the state a number&rsquo;s word reaches, so if some x sits in the same "
    "state as an orbit element, then x &isin; I, hence F(x) &isin; I &mdash; "
    "and F(x) turns out to be (or to share a state with) a power of 2. A "
    "worked witness, for the 4-state structure "
    "&delta; = [[0,1],[1,2],[1,3],[1,2]]:"))
story.append(P(
    "orbit element 101 &isin; I reaches state 3&nbsp;&nbsp;|&nbsp;&nbsp; "
    "7 also reaches state 3, so 7 &isin; I&nbsp;&nbsp;|&nbsp;&nbsp; "
    "F(7) = 16 &isin; I&nbsp;&nbsp;|&nbsp;&nbsp; 16 = 2<super>4</super> "
    "&isin; H &mdash; contradiction.", CODE))
story.append(P(
    "Each witness is audited independently of the automaton machinery: the "
    "integers are re-run through needle.step1 and the words re-run through the "
    "DFA. 1,620 witnesses were audited with no failures &mdash; 504 on "
    "separating structures (all 4 at size 3, all 100 at size 4, 400 of the "
    "2,887 at size 5) and 1,116 on structures drawn without regard to "
    "separation (all 216 at size 3, samples of 300 at sizes 4, 5 and 6)."))

# ------------------------------------------------------ 7 interpretation ----
story.append(P("7. What the result means", H1))
story.append(P(
    "<b>The real requirement is avoiding the halting basin, not the halting "
    "set.</b> A certificate must contain the orbit and be closed, so it must "
    "avoid H<super>*</super> = &cup;<sub>j</sub> "
    "F<super>&minus;j</super>(H) &mdash; every number whose orbit ever halts, "
    "not merely the powers of 2 themselves. That is what the witnesses "
    "expose: the length-one chains are exactly first-layer basin elements "
    "(halting seeds) sitting in the same automaton state as an orbit element. "
    "So the theorem should be read as: <b>at these sizes no finite-state "
    "partition of the integers separates the orbit of 6 from the halting "
    "basin</b>."))
story.append(P(
    "<b>It is the automatic generalisation of our no-congruence theorems.</b> "
    "A congruence class is the degenerate automatic set &mdash; the "
    "1-state-per-residue case. The collection already proved no congruence "
    "separates the orbit from H. This replaces &ldquo;congruence&rdquo; by "
    "&ldquo;any finite automaton on binary digits&rdquo;, which is a strictly "
    "richer class (it can express digit patterns, not just residues), and the "
    "separation still fails. That is the first structural explanation the "
    "program has for why regular deciders bounce off cryptids &mdash; and it "
    "is a different statement from the community&rsquo;s FAR experience, "
    "whose automata run on unary-coded tape languages and collapse to "
    "congruence-plus-threshold expressiveness."))
story.append(P(
    "<b>The negative half of the two-sided bet has landed; the positive half "
    "is still open.</b> The plan predicted exactly this fork. What we have is "
    "the bounded impossibility theorem plus the machinery to keep pushing; "
    "what we do not have is any evidence that a larger automaton would "
    "succeed."))

# ------------------------------------------------------------- 8 next ------
story.append(P("8. Where this goes next", H1))
story.append(tab([
    ("Push the size bound",
     "Exhaustive enumeration ends around 8 states (12.7 billion structures). "
     "Beyond that, either a SAT encoding (none of pysat/z3/minisat is "
     "installed here) or an incremental DFS that assigns transitions lazily "
     "and prunes as soon as a constraint&rsquo;s words are determined. The "
     "separating structures are a tiny fraction (2,887 of 160,675 at n = 5), "
     "so building only separating structures should pay for itself."),
    ("The MSB convention",
     "2-automatic is encoding-independent as a class, but the state count is "
     "not: an MSB-first automaton can be exponentially smaller. Reversal "
     "bounds only give MSB &le; 2 states from the present result. A direct "
     "MSB search needs the multiply-add relation read most-significant-first, "
     "which is rational but nondeterministic &mdash; worth doing, and "
     "honestly a gap until it is."),
    ("Weighted certificates (the WFAR analogue)",
     "Add an integer weight per transition and accept on an interval. This is "
     "how bbchallenge&rsquo;s WFAR strictly extends FAR, it subsumes both "
     "automatic sets and the collection&rsquo;s affine potentials, and the "
     "Horn structure survives if the weights are fixed by search."),
    ("Other machines, other bases",
     "The construction only needs branches affine in the tail: machine 3 in "
     "base 3 (halting set = powers of 27), the Hydra family in base q, and "
     "Fenrir once its case file exists. Cross-machine comparison of the "
     "smallest refuted size would be a genuine new hardness measure."),
    ("The general conjecture",
     "Every nonempty 2-automatic F-invariant meets H. A proof would explain "
     "cryptid decider-resistance outright. The witness structure suggests the "
     "route: show the halting basin is unavoidable in the automatic topology "
     "&mdash; i.e. every finite-index digit partition mixes basin elements "
     "with orbit elements. Note this cannot follow from counting alone: the "
     "basin is thin (about one halting seed per octave), so the argument must "
     "be about digit patterns, not density."),
], ("direction", "content"), (1.45 * inch, 4.85 * inch)))

# --------------------------------------------------------------- 9 ledger --
story.append(P("9. Verification ledger", H1))
story.append(tab([
    ("F(x) = x + 3(x &gt;&gt; (v+1)) + v and the branch form",
     "PROVED (algebra) and machine-verified against needle.step1 for all "
     "non-powers-of-2 below 300,000."),
    ("Local-action lemma (Section 2)",
     "PROVED (disjoint bit ranges); also checked on 29,414 (v, k) pairs."),
    ("Branch pair sets are exact",
     "MACHINE-VERIFIED: equality against brute-force enumeration of instances, "
     "several structures, k &lt; 20,000, v &le; 4, both conventions."),
    ("Enumeration is complete and non-redundant",
     "MACHINE-VERIFIED: generator counts match the known "
     "initially-connected-DFA counts through 7 states."),
    ("Horn propagation decides a structure exactly",
     "PROVED (least model of a Horn system) &mdash; given the pair sets and "
     "the units."),
    (f"No certificate at &le; {NMAX_START} states; no nonempty invariant at "
     f"&le; {NMAX_FREE}",
     "MACHINE-VERIFIED by exhaustive search, sound because the imposed branch "
     "conditions are a subset of full closure. Not a statement about larger "
     "automata."),
    ("Witnesses",
     "MACHINE-VERIFIED independently: integers re-run through needle.step1, "
     "words re-run through the DFA; 1,620 audited, zero failures."),
    ("Anything about certificates of unbounded size",
     "OPEN. Nothing here bounds the general question, and no heuristic in "
     "this report should be read as evidence either way."),
], ("claim", "status"), (2.3 * inch, 4.0 * inch)))
story.append(Spacer(1, 10))
story.append(P(
    "Code: dfa_invariant.py (machinery and tests), search.py (orbit "
    "certificate search), anystart.py (start-free search), witness.py "
    "(witness extraction and audit), strength.py (separation versus closure), "
    "verify.py (calibration). Every script is runnable standalone and prints "
    "its own checks.", CODE))

doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.85 * inch,
                        rightMargin=0.85 * inch, topMargin=0.8 * inch,
                        bottomMargin=0.8 * inch,
                        title="WS1: automatic certificates for the Space Needle")
doc.build(story)
print(f"wrote {OUT}")
print(f"  start-specific sizes covered: {sorted(started)}")
print(f"  start-free sizes covered:     {sorted(free)}")
