#!/usr/bin/env python3
"""Audit a reportlab-generated PDF for the failures that don't raise exceptions.

Checks, from the RENDERED text (what actually printed, not the source):
  - page count
  - missing-glyph boxes (U+25A0 '#') with the lines they appear on
  - the section / subsection headings present
  - cross-reference resolution: every "Section X" / "Section X.Y" mention
    checked against headings that actually exist
  - presence of any --expect strings you name (key numbers, theorem names)

Usage:
    python3 audit_pdf.py report.pdf
    python3 audit_pdf.py report.pdf --expect "Theorem (mod-16" "10^150,514"
    python3 audit_pdf.py report.pdf --require-crossrefs   # nonzero exit if any dangle

Requires: pypdf  (pip install pypdf)
"""
import argparse
import re
import sys

BOX = "■"  # the missing-glyph square reportlab prints for absent glyphs


def extract(path):
    from pypdf import PdfReader
    r = PdfReader(path)
    pages = [p.extract_text() for p in r.pages]
    return pages, "\n".join(pages)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--expect", nargs="*", default=[],
                    help="strings that MUST appear in the rendered text")
    ap.add_argument("--require-crossrefs", action="store_true",
                    help="exit nonzero if any Section reference is dangling")
    args = ap.parse_args()

    pages, full = extract(args.pdf)
    flat = full.replace("\n", " ")
    problems = 0

    print(f"pages: {len(pages)}")

    # 1) missing-glyph boxes
    box_lines = [ln for ln in full.splitlines() if BOX in ln]
    nboxes = full.count(BOX)
    print(f"missing-glyph boxes ({BOX}): {nboxes}")
    if nboxes:
        problems += 1
        for ln in box_lines[:12]:
            print(f"    {ln.strip()[:90]}")

    # 2) headings
    heads = re.findall(r"^\d+\.(?:\d+)?\s+.*$", full, re.M)
    top = [h for h in re.findall(r"^\d+\.\s+[A-Z].*$", full, re.M)]
    print(f"top-level sections: {len(top)}")
    for h in top:
        print(f"    {h[:60]}")

    # 3) cross-reference resolution
    secs = set(re.findall(r"^(\d+)\.\s", full, re.M)) | \
        set(re.findall(r"^(\d+\.\d+)\s\s", full, re.M))
    refs = sorted(set(re.findall(r"Section\s+(\d+(?:\.\d+)?)", full)))
    dangling = [r for r in refs if r not in secs]
    print(f"cross-references: {len(refs)} distinct; "
          f"dangling: {dangling if dangling else 'none'}")
    if dangling:
        problems += 1

    # 4) expected strings
    for s in args.expect:
        ok = s in flat
        print(f"expect {s!r}: {'OK' if ok else 'MISSING'}")
        if not ok:
            problems += 1

    print("\nRESULT:", "clean" if problems == 0 else f"{problems} problem(s)")
    if problems and (args.require_crossrefs or nboxes or
                     any(s not in flat for s in args.expect)):
        sys.exit(1)


if __name__ == "__main__":
    main()
