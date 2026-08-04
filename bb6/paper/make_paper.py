"""Build the BB(6) port report.

Every number here is copied from a recorded measurement in
`bb6/RESULTS.md`, which in turn comes from the scripts in `bb6/`.  No
figure is rounded from memory.  Rebuild with

    python3 make_paper.py && python3 audit_pdf.py bb6_report.pdf

Glyph discipline: reportlab's base-14 fonts are Latin-1 only, so no
Unicode sub/superscripts anywhere -- use <sub>/<super> markup and HTML
entities, and plain ASCII inside graphics Strings.
"""
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle,
                                KeepTogether)

ACCENT = colors.HexColor("#1a4d7a")
GREY = colors.HexColor("#555555")
LIGHT = colors.HexColor("#eef2f6")

ss = getSampleStyleSheet()
body = ParagraphStyle("body", parent=ss["BodyText"], fontName="Times-Roman",
                      fontSize=10, leading=14.2, alignment=TA_JUSTIFY,
                      spaceAfter=7)
mono = ParagraphStyle("mono", parent=body, fontName="Courier", fontSize=8,
                      leading=11, alignment=0, leftIndent=14, spaceAfter=8,
                      textColor=colors.HexColor("#333333"))
h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Times-Bold",
                    fontSize=14, leading=17, textColor=ACCENT,
                    spaceBefore=15, spaceAfter=7)
h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Times-Bold",
                    fontSize=11.2, leading=14, textColor=colors.black,
                    spaceBefore=11, spaceAfter=5)
title = ParagraphStyle("title", parent=body, fontName="Times-Bold",
                       fontSize=19, leading=23, alignment=1, spaceAfter=5)
sub = ParagraphStyle("sub", parent=body, fontName="Times-Italic",
                     fontSize=11, leading=14, alignment=1,
                     textColor=GREY, spaceAfter=16)
cell = ParagraphStyle("cell", parent=body, fontSize=8.4, leading=10.8,
                      alignment=0, spaceAfter=0)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Times-Bold")
cellm = ParagraphStyle("cellm", parent=cell, fontName="Courier", fontSize=7.2,
                       leading=9.4)
cap = ParagraphStyle("cap", parent=body, fontSize=8.6, leading=11.4,
                     textColor=GREY, alignment=0, spaceBefore=3,
                     spaceAfter=10)


def P(t, s=body):
    return Paragraph(t, s)


def tbl(rows, widths, head=True, mono_cols=()):
    data = []
    for i, r in enumerate(rows):
        row = []
        for j, c in enumerate(r):
            st = cellb if (head and i == 0) else (
                cellm if j in mono_cols else cell)
            row.append(P(str(c), st))
        data.append(row)
    t = Table(data, colWidths=widths, hAlign="LEFT")
    style = [("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 3),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
             ("LEFTPADDING", (0, 0), (-1, -1), 5),
             ("RIGHTPADDING", (0, 0), (-1, -1), 5),
             ("LINEBELOW", (0, 0), (-1, 0), 0.7, ACCENT),
             ("LINEBELOW", (0, 1), (-1, -2), 0.25, colors.HexColor("#cccccc")),
             ("BACKGROUND", (0, 0), (-1, 0), LIGHT)]
    t.setStyle(TableStyle(style))
    return t


story = []
A = story.append

A(P("Porting a rigid-certificate method to BB(6)", title))
A(P("Two censuses of the 1,064-machine holdout list, a negative result "
    "about what boundary rigidity buys, three cryptid candidates, and a "
    "Lean formalisation of the machinery", sub))

# ---------------------------------------------------------------- summary
A(P("Summary", h1))
A(P("A method that decided nine FRACTRAN holdouts was ported to the BB(6) "
    "Turing-machine holdout list. This report records what transferred, "
    "what did not, and why. Four results are worth stating up front.", body))
A(P("<b>1. A negative that transfers.</b> Rigid phase boundaries do not "
    "imply a rigid phase word. In the FRACTRAN setting the two came "
    "together and fitting the boundary was the hard part; on Turing "
    "machines they come apart completely. Four machines were found whose "
    "boundary families are exactly affine and confirmed at a hundred times "
    "the fitting budget, and none of them is decidable by the method, "
    "because the word between boundaries never compresses at any block "
    "size. A rigidity census therefore over-counts what a certificate "
    "method can decide.", body))
A(P("<b>2. Three cryptid candidates.</b> Of 1,064 machines, five have a "
    "two-level structure whose outer map meets the cryptid criteria; three "
    "survive deeper runs. Their halting questions reduce to orbit "
    "avoidance for explicit expanding integer maps with multiple branches "
    "and no periodic branch pattern over the observed range.", body))
A(P("<b>3. An acceleration of about 158 orders of magnitude.</b> "
    "Recognising the machines' induction rule at run time takes the "
    "reachable horizon from roughly 10<super>7</super> base steps to "
    "roughly 10<super>165</super> in 45 seconds, and the observable outer "
    "orbits from 10&ndash;12 steps to 289&ndash;294.", body))
A(P("<b>4. The halting criterion, and a Lean formalisation of the "
    "machinery.</b> All three candidates halt if and only if a two-state "
    "scanning gadget meets two adjacent zeros. The Turing-machine "
    "semantics, the chain lemma, the block-crossing table and the halting "
    "criterion are formalised in Lean 4, mathlib-free, with no "
    "<font face='Courier'>sorry</font> and no added axioms.", body))
A(P("Nothing here decides whether any of the three machines halts. That is "
    "the open problem they exist to pose, and no claim is made against "
    "it.", body))

# ------------------------------------------------------------------ setup
A(P("1. Setting", h1))
A(P("The Busy Beaver challenge maintains lists of small Turing machines "
    "whose halting is undecided by any deployed decider. The BB(6) list "
    "used here has 1,064 machines up to equivalence (mxdys, 28 July 2026). "
    "These machines have survived Cyclers, Translated Cyclers, Backward "
    "Reasoning, Closed Tape Language, n-gram CPS, WFAR and RepWL, so any "
    "method that reports a large fraction of them as easy is reporting a "
    "bug.", body))
A(P("That observation is used throughout as a calibration test. The first "
    "version of the rigidity detector classified about 15% of the list as "
    "having polynomial phase structure, which is impossible; the cause was "
    "a missing filter, described in section 3.", body))
A(P("A <i>cryptid</i>, in this community's usage, is a small explicit "
    "machine whose halting is provably equivalent to an open "
    "Collatz-type orbit-avoidance problem. Three structural features make "
    "such problems hard, and they are what section 5 measures: the "
    "dynamics are piecewise affine, the map expands on average, and the "
    "branch taken depends on ever deeper digits of the argument.", body))

# ------------------------------------------------------------ simulators
A(P("2. Acceleration is the whole game", h1))
A(P("A cell-at-a-time simulator run for two million steps on one of these "
    "machines sees the head visit about fifty new cells. Fifty. Whatever "
    "structure they have lives at a scale a raw simulator does not reach, "
    "so every later section depends on compressing the simulation "
    "exactly.", body))
A(P("Three layers were built, each cross-checked step-for-step against the "
    "one below it. Correctness here is load-bearing: a plausible "
    "acceleration with a wrong step count corrupts every downstream "
    "number.", body))
A(tbl([["layer", "what it does", "verification"],
       ["tm.py", "cell at a time",
        "all four Busy Beaver champions exact; BB(5) at 47,176,870 steps "
        "and 4,098 ones"],
       ["blocktape.py", "chain steps",
        "step-exact against tm.py on 3,000 random machines and 60 "
        "holdouts, tapes identical"],
       ["macro.py", "macro machines, block sizes 1 to 6",
        "3,454 machine/block-size pairs cross-checked"]],
      [3.0 * cm, 4.4 * cm, 8.2 * cm], mono_cols=(0,)))
A(P("Figure 1. The simulator stack. Each layer is checked against an "
    "independent, simpler implementation rather than against itself.", cap))
A(P("<b>A measured negative worth recording.</b> Chain steps alone &mdash; "
    "crossing a run of identical cells when a state re-enters itself in "
    "the same direction &mdash; give a speed-up of about 1.2 times on this "
    "list. These machines have almost no base-level self-loops; they "
    "bounce. Grouping cells into blocks of size b and treating each block "
    "as one symbol (Marxen&ndash;Buntrock macro machines) creates the "
    "self-loops that do not exist at cell level, and the speed-up on BB(5) "
    "becomes about 1,900 times.", body))
A(P("Two decisions come free from simulating inside a block. If the head "
    "never leaves the block within the pigeonhole bound "
    "|Q| &times; b &times; 2<super>b</super>, a configuration must repeat "
    "and the machine never halts; if it halts inside, the machine halts. "
    "Both are proofs, not heuristics.", body))

# ---------------------------------------------------------------- census 1
A(P("3. First census: single-level rigidity", h1))
A(P("A machine is <i>rigid</i> when some sub-sequence of its configurations "
    "&mdash; its phase boundaries &mdash; has coordinates given by "
    "formulas in EXP = {a + bn + c&middot;q<super>n</super>}, with the same "
    "word of machine steps between consecutive boundaries. A Turing "
    "machine has no coordinate vector until the tape is run-length "
    "encoded, at which point block lengths are the coordinates and the "
    "definition transfers unchanged.", body))
A(tbl([["class", "count", "share"],
       ["NONRIGID", "626", "58.8%"],
       ["FEWPHASE", "431", "40.5%"],
       ["GEO", "4", "0.4%"],
       ["UNCONFIRMED", "3", "0.3%"]],
      [4.0 * cm, 2.4 * cm, 2.4 * cm]))
A(P("Figure 2. All 1,064 machines, 3,191 seconds.", cap))
A(P("Two filters are what make these numbers mean anything.", body))
A(P("<b>Eventual positivity.</b> A fitted counter with a negative trend "
    "describes a transient, not a phase family. One real example from the "
    "sweep: a counter fitted as 381 &minus; 4n, exact over all 96 phases it "
    "was fitted on, and then the family simply ends because the counter "
    "reaches zero. The longer the transient, the more convincing the fit "
    "looks. Without this filter the detector reported the impossible 15% "
    "POLY rate.", body))
A(P("<b>Confirmation.</b> Every fit is determined by three phases and then "
    "re-tested on phases it never saw. Fits that fail are counted "
    "separately as UNCONFIRMED rather than silently dropped.", body))

# -------------------------------------------------------------- the negative
A(P("4. Rigid boundaries do not imply a rigid phase word", h1))
A(P("The four GEO machines (lines 360, 833, 852, 1005) have genuinely "
    "rigid boundaries. Re-run at a 20M macro budget, a hundred times the "
    "budget their formulas were fitted at, each reproduced seven or eight "
    "unseen phases with zero mismatches. For line 360 the boundary is", body))
A(P("B(n) = 1^(6+2n) 0 1^23 0 1^12, head at far left facing left, state D<br/>"
    "steps between boundaries = 72140 &minus; 6n + 96 &middot; 2^n", mono))
A(P("&mdash; a linear tape with an exponential clock. But a certificate "
    "needs the word <i>between</i> boundaries to be a fixed list of "
    "stages, and it is not.", body))
A(tbl([["block size", "phase-word lengths", "stages", "max run"],
       ["1", "15, 30, 60, 120, 240", "same as length", "1"],
       ["2", "11, 19, 39, 78, 156", "same as length", "1"],
       ["4", "29, 141, 568, 2180, 8708", "same as length", "1"]],
      [2.4 * cm, 6.2 * cm, 3.4 * cm, 2.2 * cm]))
A(P("Figure 3. The phase word never compresses: every run-length count is "
    "1, at every block size tried.", cap))
A(P("There is real structure, uniform across all four machines and every "
    "level: |W(n+1)| = 2|W(n)| exactly, and the words agree on a common "
    "prefix of exactly |W(n)| &minus; 6 symbols &mdash; the same constant 6 "
    "for all four, including the machine whose base word is 17 rather than "
    "15. The obvious recursion this suggests, W(n+1) = W(n)[:&minus;6] + X "
    "+ W(n) with X the constant divergence block, is false at every level; "
    "it was tested. The divergence from &ldquo;W(n) repeated twice&rdquo; "
    "grows proportionally (13, 22, 44, 88 symbols), so it is not a "
    "bounded-edit substitution either.", body))
A(P("<b>The conceptual point.</b> For the nine FRACTRAN holdouts, boundary "
    "rigidity and phase-word rigidity came together, and fitting the "
    "boundary was the hard part. On Turing machines they come apart: the "
    "boundary family can be exactly affine while the word between "
    "boundaries is exponentially complex and incompressible. The boundary "
    "fit is necessary and nowhere near sufficient. Here four candidates "
    "yielded zero decisions.", body))
A(P("Deciding those four needs a decider for the reachable <i>set</i> "
    "&mdash; a closed-tape-language argument &mdash; not a certificate for "
    "a single orbit. That is a different tool, and one the community "
    "already has stronger versions of.", body))

# ---------------------------------------------------------------- census 2
A(P("5. Second census: cryptid-shaped outer maps", h1))
A(P("A two-level machine has an inner loop that iterates an affine map "
    "and an outer map that carries one reservoir value to the next. The "
    "outer map is the object the cryptid criteria apply to. The detector "
    "was calibrated on the BB(6) machine decided in April 2026 via "
    "Baker&ndash;W&uuml;stholz, whose inner recurrence it recovers as "
    "x &rarr; 3x + 4 and which it classifies as cryptid-shaped.", body))
A(tbl([["class", "count", "share"],
       ["no two-level structure", "1,033", "97.1%"],
       ["INSUFFICIENT", "22", "2.1%"],
       ["CRYPTID-SHAPED", "5", "0.5%"],
       ["NOT-EXPANDING", "3", "0.3%"],
       ["PREDICTABLE-BRANCHES", "1", "0.1%"]],
      [5.6 * cm, 2.4 * cm, 2.4 * cm]))
A(P("Figure 4. All 1,064 machines, 523 seconds.", cap))
A(P("<b>One criterion runs the opposite way to intuition.</b> Piecewise "
    "affineness is not something to look for: the outer map of a two-level "
    "machine is affine on each branch by construction, since it is built "
    "from macro rules that are themselves affine. What must be tested is "
    "whether a <i>single</i> affine branch explains the whole orbit. If "
    "one does, the orbit has a closed form and the machine is tractable "
    "&mdash; which is what a cryptid is not. A failed global affine fit is "
    "evidence of several branches, hence evidence <i>for</i> the cryptid "
    "shape. Getting this backwards initially made the "
    "Baker&ndash;W&uuml;stholz machine read as having no closed form "
    "rather than as cryptid-shaped.", body))
A(P("Cryptid-shaped does not mean undecided. The "
    "Baker&ndash;W&uuml;stholz machine is cryptid-shaped and was decided, "
    "with heavy machinery. The label says where the difficulty lives.", body))

A(P("5.1 Two corrections found by running deeper", h2))
A(P("<b>The last outer step is systematically truncated.</b> The "
    "simulation stops at a fixed macro budget, which lands in the middle "
    "of the final inner loop, so that loop's length is an undercount. "
    "Raising the budget from 8M to 40M changed one machine's last branch "
    "index from 9 to 10 and flipped its verdict. A criterion that depends "
    "on the final delta is reading the budget, not the machine; the last "
    "step is now dropped.", body))
A(P("<b>A periodic branch pattern is as predictable as a constant one.</b> "
    "The delta sequence 1, 2, 3, 1, 2, 3 is generated by a three-state "
    "automaton, so a bounded invariant does track the branch sequence. "
    "Testing only for constant deltas let one machine through as "
    "cryptid-shaped.", body))
A(P("Both corrections removed candidates. The surviving three:", body))
A(tbl([["line", "inner", "outer steps", "branch deltas", "growth", "verdict"],
       ["336", "2x+4", "10", "2,0,2,2,2,2,2,1,1", "2.94", "CRYPTID-SHAPED"],
       ["555", "2x+5", "12", "1,1,1,0,2,1,1,2,2,1,2", "2.56",
        "CRYPTID-SHAPED"],
       ["1002", "2x+4", "10", "2,2,1,1,1,1,2,2,2", "2.93", "CRYPTID-SHAPED"],
       ["106", "2x+3", "6", "1,1,1,1,1 (period 1)", "2.06", "predictable"],
       ["990", "2x+2", "7", "1,2,3,1,2,3 (period 3)", "4.48",
        "predictable"]],
      [1.5 * cm, 1.7 * cm, 2.0 * cm, 5.0 * cm, 1.8 * cm, 3.6 * cm],
      mono_cols=(1, 3)))
A(P("Figure 5. All inner recurrences are base 2, where the "
    "Baker&ndash;W&uuml;stholz machine is base 3 &mdash; a different "
    "family.", cap))
A(P("The three machines, in the standard format:", body))
A(P("336&nbsp;&nbsp;1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE<br/>"
    "555&nbsp;&nbsp;1RB1RE_1LC0RA_1RD0LB_1LB1RC_1LF0RD_---0LE<br/>"
    "1002&nbsp;1RB1LC_1RC0LD_1LA0RB_1LB1LE_1RF0LA_---0RE", mono))

# ------------------------------------------------------------- unit lemma
A(P("6. The unit lemma", h1))
A(P("The inner loop of each machine is a fixed unit of five macro steps. "
    "Observed first as an empirical regularity, it was then derived "
    "symbolically, and the two routes agree.", body))
A(P("<b>The symbolic route needed one correction.</b> A symbolic macro "
    "simulator, carrying block counts as expressions rather than integers, "
    "stalls after five to seven steps: it refuses to consume a single cell "
    "from a symbolic block, because for some values of the parameter the "
    "block survives and is read again and for others it vanishes and the "
    "next block is read. Those are different runs, and an engine that "
    "picks one is simulating a branch rather than the machine. The stall "
    "is sound and was mistaken for a wall. What the lemma wants is the "
    "guard carried forward, not the run stopped &mdash; but only if the "
    "block being lifted is the one the unit actually sweeps. Lifting the "
    "wrong block, a constant-length one, fragments the tape into a "
    "configuration the machine never reaches; the first attempt did "
    "exactly that.", body))
A(tbl([["line", "one unit", "cost"],
       ["336", "(1, c1, x, c3) &rarr; (1, c1&minus;1, x+2, c3&minus;1)",
        "4x + 12"],
       ["555", "(x, c1, 1, c3) &rarr; (x+2, c1&minus;1, 1, c3&minus;1)",
        "4x + 4"],
       ["1002", "(1, c1, x, c3) &rarr; (1, c1&minus;1, x+2, c3&minus;1)",
        "4x + 12"]],
      [1.6 * cm, 9.0 * cm, 2.6 * cm], mono_cols=(1, 2)))
A(P("Figure 6. The unit, crossed symbolically with the correct block "
    "lifted.", cap))
A(P("The derivation reproduces the measured cost law from an independent "
    "route. At unit j the swept block has x = x<sub>0</sub> + 2j, so "
    "4x + 12 = 8j + (4x<sub>0</sub> + 12), which at x<sub>0</sub> = 1 is "
    "8j + 16 &mdash; exactly the law measured empirically over 151 and 156 "
    "consecutive units. Checked additionally at x = 1, 2, 3, 7, 11, 20, "
    "53, 100, 301 and 1000: ten out of ten exact on all three machines.", body))
A(P("Stated at cell level for line 336, and verified on 54 independent "
    "instances (54 out of 54 exact, with arbitrary surrounding tape):", body))
A(P("for all x, a, b and arbitrary Lr, Rr:<br/><br/>"
    "&nbsp;&nbsp;[11] (10)^(a+1) Lr | (10)^x (11)^(b+1) Rr&nbsp;&nbsp;"
    "state A, facing left<br/>"
    "&nbsp;&nbsp;&nbsp;&nbsp;-- 4x + 12 steps --&gt;<br/>"
    "&nbsp;&nbsp;[11] (10)^a Lr&nbsp;&nbsp;&nbsp;&nbsp; | (10)^(x+2) "
    "(11)^b Rr&nbsp;&nbsp;state A, facing left", mono))
A(P("Traced at x = 3 and x = 5, the run decomposes into four pieces, two "
    "of them chains:", body))
A(tbl([["piece", "steps", "x=3", "x=5"],
       ["prologue, fixed", "4", "4", "4"],
       ["chain right: x+2 crossings of 01 &rarr; 10", "2x+4", "10", "14"],
       ["turnaround, fixed", "2", "2", "2"],
       ["chain left: x+1 crossings of 10 &rarr; 01", "2x+2", "8", "12"],
       ["total", "4x+12", "24", "32"]],
      [7.6 * cm, 2.4 * cm, 1.6 * cm, 1.6 * cm]))
A(P("Figure 7. Both chains are instances of block crossings already proved "
    "in Lean, so the remaining proof is composition.", cap))

# ----------------------------------------------------------- acceleration
A(P("7. Rule-based acceleration", h1))
A(P("A simulator that recognises the unit at run time need not walk it. "
    "At each macro step the accelerator looks ahead for a return to the "
    "same skeleton, state and direction; if the counters move by the same "
    "fixed vector on two consecutive repetitions and the per-repetition "
    "cost is constant or grows by a constant, it computes how many "
    "repetitions fit before a guard would fail and jumps the whole way. "
    "The number of repetitions is chosen one short of any guard failing, "
    "so a jump never crosses a branch. That jump is the composition of "
    "prologue, n units and epilogue &mdash; the closed form, applied.", body))
A(P("Verified against the unaccelerated simulator at 5.0, 6.3 and "
    "5.1 &times; 10<super>7</super> base steps for the three machines: "
    "identical skeleton, identical counters, identical base-step count, "
    "with 63, 90 and 79 jumps skipping 12,409, 15,215 and 14,956 units. "
    "Beyond that range the detector still self-checks, observing two full "
    "repetitions with matching deltas before every jump, but that is a "
    "safeguard rather than a proof.", body))
A(tbl([["line", "outer steps", "growth per step", "branch index range",
        "delta period", "halted"],
       ["336", "289", "2.4648", "3 to 378", "none", "no"],
       ["555", "294", "2.4166", "3 to 374", "none", "no"],
       ["1002", "290", "2.4936", "3 to 384", "none", "no"]],
      [1.5 * cm, 2.4 * cm, 3.0 * cm, 3.8 * cm, 2.4 * cm, 2.0 * cm]))
A(P("Figure 8. Reach goes from about 10<super>7</super> base steps to "
    "about 10<super>165</super> in 45 seconds, roughly 158 orders of "
    "magnitude, and outer orbits from 10&ndash;12 steps to 289&ndash;294. "
    "No halt occurs anywhere in that range.", cap))
A(P("At about 290 outer steps the absence of a periodic branch pattern is "
    "on much firmer ground than it was at ten, and the growth rate is "
    "stable rather than a small-sample artefact.", body))

# --------------------------------------------------------------- halting
A(P("8. The halting criterion", h1))
A(P("All three machines have exactly one undefined transition, state F on "
    "symbol 0, and in all three F is entered from exactly one place: state "
    "E reading 0. E and F therefore form a scanning pair. From E on a 0 "
    "the machine writes 1, steps one cell in the scan direction and lands "
    "in F; F on a 1 writes 0, steps again and returns to E; F on a 0 "
    "halts; E on a 1 leaves the scan entirely.", body))
A(P("HALT if and only if, at some moment, the machine is in state E "
    "reading 0 with the next cell in the scan direction also 0.", mono))
A(P("Equivalently the pair consumes the word 01 (mirrored to 10 for line "
    "555) repeatedly, and halts on 00. Over 6 &times; 10<super>6</super> "
    "base steps per machine there are 3,005, 4,130 and 4,904 such scans "
    "and not one carries a 00; every one reads 01 and continues.", body))
A(P("This is the reduction the whole exercise was for. Halting is now a "
    "condition on the tape word at a specific, identifiable moment rather "
    "than a statement about the machine's entire future.", body))

# ------------------------------------------------------------------ lean
A(P("9. Lean formalisation", h1))
A(P("591 lines, Lean 4.32.2, mathlib-free, no "
    "<font face='Courier'>sorry</font>, no "
    "<font face='Courier'>native_decide</font>, no added axioms &mdash; "
    "results depend on <font face='Courier'>propext</font> and "
    "<font face='Courier'>Quot.sound</font> only. Thirty-six "
    "<font face='Courier'>#guard</font> checks are evaluated at compile "
    "time.", body))
A(P("<b>The representation is the proof strategy.</b> The first version "
    "put the head on a cell and proved a sweep lemma for a state "
    "re-entering itself in the same direction. It compiled, and it was "
    "useless: none of the three machines has such a transition at cell "
    "level &mdash; which is exactly why the Python side needed macro "
    "machines in the first place. The right primitive is a block "
    "crossing, and with the head <i>between</i> cells a block crossing is "
    "literal list concatenation, so the induction goes through with no "
    "index arithmetic. With the head on a cell it does not.", body))
A(tbl([["result", "content"],
       ["Steps.trans", "runs compose, step counts add; depends on no "
        "axioms at all"],
       ["crossR_rep, crossL_rep", "the chain lemma: n copies of a block "
        "are crossed in n&middot;k steps, arbitrary machine, arbitrary "
        "block"],
       ["steps_of_runFor", "bridge from the executable runner to Steps, "
        "so the kernel computes intermediate configurations"],
       ["24 crossings", "the chain-step table, generated from the same "
        "code the measurements used, each with an executable check"],
       ["m336/m555/m1002_halt_iff", "each machine halts iff state F reads "
        "0 &mdash; the E/F gadget, formal"]],
      [4.6 * cm, 10.8 * cm], mono_cols=(0,)))
A(P("Figure 9. What is proved.", cap))
A(P("The semantics are pinned against ground truth at compile time: "
    "<font face='Courier'>#guard</font> evaluates BB(2), BB(3) and BB(4) "
    "to 6, 21 and 107 steps with 4, 5 and 13 ones. A drift in the step "
    "convention &mdash; which cell is written, whether the halting "
    "transition counts, what unwritten tape reads &mdash; breaks the "
    "build. Further guards check that none of the three candidates halts "
    "within 20,000 steps, which would catch a transcription slip in the "
    "transition tables.", body))
A(P("One subtlety is load-bearing. The halt lemmas carry a hypothesis "
    "that the state index is below 6, because the table lookup also "
    "returns nothing for an out-of-range state; without it the statement "
    "is false. Reachable states are always in range, but that is a fact "
    "to be carried rather than assumed.", body))

# ---------------------------------------------------------------- status
A(P("10. What is and is not established", h1))
A(P("<b>Established.</b> Both censuses, on the full list, with the "
    "calibration and confirmation filters described. The negative result "
    "of section 4, from direct measurement at every block size tried. The "
    "unit lemma of section 6, derived symbolically and agreeing with an "
    "independent empirical measurement to the constant. The acceleration "
    "of section 7, cross-checked exactly against the unaccelerated "
    "simulator over the range where that is feasible. The halting "
    "criterion of section 8, read from the transition tables and "
    "confirmed over millions of steps. The Lean development of "
    "section 9.", body))
A(P("<b>Not established.</b> Whether any of the three machines halts. "
    "That is the open problem, and these results sharpen its statement "
    "without touching it.", body))
A(P("The equivalence itself &mdash; a machine-checked proof that a given "
    "machine follows a given map, and halts if and only if that map's "
    "orbit meets an explicit set &mdash; is not finished. Its remaining "
    "obligations are: composing the four fragments of Figure 7 into the "
    "unit lemma in Lean, iterating it, composing to obtain the outer map, "
    "and expressing the section-8 condition in terms of the section "
    "counters. Every one of those is assembly on results already stated "
    "and verified; none is open. That distinction is the honest "
    "characterisation of where this stands.", body))
A(P("Two limits are worth naming precisely. The absence of a periodic "
    "branch pattern is measured over 289 to 294 outer steps, not proved; "
    "a longer period could hide beyond that range. And the cost wall is "
    "real: growth is 2.5 to 2.9 per outer step with work scaling in the "
    "reservoir value, so each further outer step costs roughly three "
    "times the last, and reaching twenty more is a factor of about "
    "3<super>20</super>.", body))

# --------------------------------------------------------- reproducibility
A(P("11. Reproducing this", h1))
A(P("All code, logs and the Lean development are at "
    "github.com/TomZahavy/collatz-cryptids, under "
    "<font face='Courier'>collatz/bb6/</font>. The censuses are "
    "<font face='Courier'>sweep.py</font> and "
    "<font face='Courier'>sweep_cryptid.py</font> over "
    "<font face='Courier'>bbf/bb6_holdouts_1064.txt</font>; every "
    "simulator has a self-test that runs its own cross-checks; "
    "<font face='Courier'>lake build</font> in "
    "<font face='Courier'>bb6/lean</font> reproduces the formalisation in "
    "a few seconds. Detailed measurements, including the failed "
    "hypotheses, are in <font face='Courier'>bb6/RESULTS.md</font>.", body))
A(P("The failed hypotheses are recorded deliberately. Three of the "
    "corrections in this report &mdash; the missing positivity filter, the "
    "truncated final outer step, and the periodic-branch blind spot "
    "&mdash; were mistakes that produced confident wrong answers before "
    "they were caught, and each was caught by a check that could have been "
    "run earlier.", body))


def footer(canv, doc):
    canv.saveState()
    canv.setFont("Times-Roman", 8)
    canv.setFillColor(GREY)
    canv.drawCentredString(A4[0] / 2.0, 1.05 * cm, str(doc.page))
    canv.restoreState()


doc = BaseDocTemplate("bb6_report.pdf", pagesize=A4,
                      leftMargin=2.4 * cm, rightMargin=2.4 * cm,
                      topMargin=2.1 * cm, bottomMargin=2.1 * cm,
                      title="Porting a rigid-certificate method to BB(6)")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
              id="n")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])
doc.build(story)
print("wrote bb6_report.pdf")
