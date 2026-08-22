#!/usr/bin/env python3
"""Build the write-like-sangho voice corpus from published PDFs.

Turns each paper into `write-like-sangho/examples/<section>/<corpus_id>.md`, holding
only prose Sangho wrote: running heads, figure/table text, references, acknowledgments
and appendices are dropped, hyphenation from line wrapping is repaired, and paragraphs
are reflowed out of the PDF's line-by-line layout.

    uv run --with pymupdf tools/build-corpus.py --dry-run   # review the section mapping
    uv run --with pymupdf tools/build-corpus.py             # write the corpus

The corpus itself is gitignored. This script is what ships, so the corpus can be
rebuilt from source whenever the paper set changes.
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

import pymupdf

PAPERS_DIR = pathlib.Path("~/Github/sanghosuh.github.io/papers").expanduser()
OUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "write-like-sangho" / "examples"

# corpus_id is filled in by tools/resolve-corpus-ids.py; `key` is the fallback filename.
PAPERS = [
    {"file": "storyensemble_uist.pdf", "key": "storyensemble", "venue": "UIST", "year": 2025},
    {"file": "luminate_chi.pdf",       "key": "luminate",      "venue": "CHI",  "year": 2024},
    {"file": "sensecape_uist.pdf",     "key": "sensecape",     "venue": "UIST", "year": 2023},
    {"file": "codetoon_uist.pdf",      "key": "codetoon",      "venue": "UIST", "year": 2022},
    {"file": "privacytoon.pdf",        "key": "privacytoon",   "venue": "DIS",  "year": 2022},
    {"file": "comics_sigcse.pdf",      "key": "comics-cs1",    "venue": "SIGCSE", "year": 2021},
    {"file": "codingstrip_vlhcc.pdf",  "key": "codingstrip",   "venue": "VL/HCC", "year": 2020},
    {"file": "concreteness_idc.pdf",   "key": "concreteness",  "venue": "IDC",  "year": 2020},
]

# Heading text -> corpus folder. First match wins; checked against the uppercased
# heading with any numbering prefix stripped.
SECTION_RULES = [
    (r"^ABSTRACT$",                                  "abstract"),
    (r"^INTRODUCTION$",                              "introduction"),
    (r"^(RELATED WORK|BACKGROUND)",                  "related-work"),
    (r"^FORMATIVE STUD",                             "formative-study"),
    (r"^DESIGN (GOALS|OBJECTIVES)",                  "design-goals"),
    (r"(EXAMPLE|MOTIVATING|USAGE) (SCENARIO|WORKFLOW)", "example-user-scenario"),
    (r"^(USER STUDY|USER EVALUATION|EVALUATION|METHODS?)$", "study-method"),
    (r"^RESULTS?$",                                  "rq-results"),
    (r"^(DISCUSSION|LIMITATIONS)",                   "discussion"),
    (r"^CONCLUSION",                                 "conclusion"),
    (r"^METHODOLOGY$",                               "survey-method"),
    (r"^(PRACTICAL IMPLICATIONS|IMPLICATIONS)",      "practical-implications"),
    (r"(FRAMEWORK|DESIGN DIMENSIONS|TAXONOMY|^OVERVIEW$)", "framework"),
    # Subsection headings, matched before falling back to the parent section.
    (r"^RQ\s*\d",                                    "rq-results"),
    (r"^(PARTICIPANTS|PROCEDURE|STUDY PROCEDURE|MEASURES|TASKS|CONDITIONS|APPARATUS)$",
                                                     "study-method"),
    (r"^(USER )?INTERFACE|^SYSTEM DESIGN|^IMPLEMENTATION|^FEATURES",
                                                     "system-design"),
    (r"^(SUMMARY|FUTURE WORK|DESIGN IMPLICATIONS)",  "discussion"),
]

# Headings a rule can't reach: system sections are named after the system, and two
# papers use a generic heading for a section type that is specific to them.
PAPER_OVERRIDES = {
    "storyensemble": {"STORYENSEMBLE": "system-design"},
    "luminate":      {"LUMINATE": "system-design",
                      "PROMPTING FOR DESIGN SPACE: A FRAMEWORK FOR DESIGN SPACE THINKING IN HUMAN-AI CO-CREATION": "framework"},
    "sensecape":     {"SENSECAPE": "system-design"},
    "codetoon":      {"CODETOON": "system-design", "CODE-DRIVEN STORYTELLING": "system-design"},
    "privacytoon":   {"DESIGN OF PRIVACYTOON": "system-design"},
    "codingstrip":   {"CODING STRIP: EXAMPLE": "example-user-scenario",
                      "CODING STRIP: DESIGN PROCESS & TOOLS": "system-design",
                      "DESIGN WORKSHOPS": "study-method"},
    # A classroom deployment, not a lab study: its method and findings are their own type.
    "comics-cs1":    {"METHODS": "classroom-study", "RESULTS": "classroom-study",
                      "COURSE & STUDENT INFORMATION": "classroom-study",
                      "USE CASES": "classroom-study", "SURVEY": "classroom-study",
                      "DEMOGRAPHICS": "classroom-study",
                      "ANALYSIS OF EACH USE CASE": "classroom-study",
                      "ANALYSIS OF OVERALL EXPERIENCE": "classroom-study",
                      "ANALYSIS OF DEMOGRAPHICS": "classroom-study"},
}

# Sections that are never voice, dropped whole.
DROP_HEADINGS = re.compile(
    r"^(CCS CONCEPTS?|KEYWORDS?|ACM REFERENCE FORMAT|ACKNOWLEDGE?MENTS?|"
    r"REFERENCES?|APPENDI(X|CES)|BIBLIOGRAPHY)", re.I)

CAPTION_START = re.compile(r"^\s*(Figure|Fig\.|Table|Listing|Algorithm)\s*\d+[.:]", re.I)
NUM_PREFIX = re.compile(r"^\s*(?:[IVXLC]+\.|\d+(?:\.\d+)*\.?|[A-Z]\.)\s+")
ROMAN_HEAD = re.compile(r"^\s*[IVXLC]+\.\s+[A-Z][A-Z \-&:,'()]{2,}$")
LETTER_HEAD = re.compile(r"^\s*[A-Z]\.\s+[A-Z]")
# Section and subsection headings share a font size in the ACM template; the depth of
# the numbering is what separates them.
DEPTH2 = re.compile(r"^\s*(?:\d+\.\d+|[A-Z]\.\d*)\s+\S")
DEPTH1 = re.compile(r"^\s*(?:\d+|[IVXLC]+\.)\s+\S")
# The template often lays the number out as its own line, so `3` / `CODETOON` and
# `3.1` / `Design Goals` arrive separately. A bare number is a level marker for the
# heading that follows it, not a heading of its own.
NUM_TOKEN = re.compile(r"^\s*(\d+(?:\.\d+)*|[IVXLC]+|[A-Z])\.?\s*$")
UNNUMBERED = re.compile(r"^(ABSTRACT|CCS CONCEPTS?|KEYWORDS?)$")
# Everything from here on is bibliography or appendix, never voice.
TERMINAL = re.compile(r"^(REFERENCES?|BIBLIOGRAPHY|APPENDI(X|CES)|ACKNOWLEDGE?MENTS?)\b", re.I)


def modal_body_size(doc) -> float:
    """Modal glyph size over the first 70% of pages.

    References are set small and run long; in an 8-page paper they can outweigh the
    body and make the whole document look like 7pt text.
    """
    vol = collections.Counter()
    cutoff = max(1, int(doc.page_count * 0.7))
    for page in doc:
        if page.number >= cutoff:
            continue
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    vol[round(span["size"], 1)] += len(span["text"])
    return vol.most_common(1)[0][0]


# Some PDFs encode ligatures as single glyphs; left in place they break tokenisation
# ("confidence" arrives as "con" + a ligature + "dence") and corrupt the word counts.
LIGATURES = str.maketrans({
    "\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl",
    "\ufb05": "st", "\ufb06": "st", "\u00a0": " ",
})


def line_text(line) -> str:
    return "".join(s["text"] for s in line["spans"]).translate(LIGATURES).strip()


def is_bold(line) -> bool:
    return any("Bold" in s["font"] or s["font"].endswith("B") or "Semibold" in s["font"]
               for s in line["spans"])


def collect_lines(doc, body: float):
    """Yield (page_no, y, text, size, bold, all_bold) for body-sized-or-larger lines.

    Anything below the modal body size is caption, table cell, footnote or running
    head — a different register that would skew the frequency audit.
    """
    out = []
    for page in doc:
        height = page.rect.height
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                text = line_text(line)
                if not text:
                    continue
                size = max(s["size"] for s in line["spans"])
                if size < body - 0.4:
                    continue
                y = line["bbox"][1]
                # running heads and folios
                if y < height * 0.06 or y > height * 0.94:
                    continue
                all_bold = all("Bold" in sp["font"] or sp["font"].endswith("B")
                               or "Semibold" in sp["font"]
                               for sp in line["spans"] if sp["text"].strip())
                out.append((page.number, y, text, size, is_bold(line), all_bold))
    return out


def find_heading_size(lines, body: float) -> float | None:
    """The section-heading size: the largest bold size that recurs.

    The title is bold and bigger than any heading, but appears once or twice; a
    section heading appears many times. Requiring recurrence separates them.
    """
    counts = collections.Counter(
        sz for _, _, _, sz, bold, _ in lines if bold and sz >= body + 0.5)
    recurring = [sz for sz, n in counts.items() if n >= 3]
    return max(recurring) if recurring else None


def classify(lines, body: float):
    """Tag each line as ('h1'|'h2'|'body', text). Handles ACM and IEEE templates."""
    tier = find_heading_size(lines, body)
    tagged = []
    for _, _, text, size, bold, all_bold in lines:
        # A caption is bold and short and would otherwise read as a heading.
        if CAPTION_START.match(text):
            tagged.append(("body", text, False))
            continue

        heading = False
        if not re.match(r"[A-Z0-9(]", text):
            # Figure captions wrap onto bold lines that begin lowercase; a heading
            # never does.
            tagged.append(("body", text, False))
            continue
        if tier is not None:
            if abs(size - tier) < 0.2 and bold and len(text) < 120:
                heading = True
            elif (all_bold and body - 0.2 <= size < tier - 0.4
                  and len(text) < 75 and not text.endswith(".")):
                # ACM subsection heads sit at body size; only being bold for the whole
                # line separates them from bold emphasis inside a sentence.
                heading = True
        elif ROMAN_HEAD.match(text) or (LETTER_HEAD.match(text) and len(text) < 70):
            # IEEE: headings share the body font and size; only numbering marks them.
            heading = True
        if re.fullmatch(r"(ABSTRACT|CCS CONCEPTS?|KEYWORDS?)", text.upper()):
            heading = True

        if not heading:
            tagged.append(("body", text, False))
            continue
        top = tier is not None and abs(size - tier) < 0.2
        tagged.append(("head", text, top))
    return assign_levels(tagged)


def depth_of(token: str) -> int:
    """Heading level implied by a numbering token: `3` -> 1, `3.1` -> 2, `A.` -> 2."""
    token = token.strip().rstrip(".")
    if re.fullmatch(r"[IVXLC]+", token):
        return 1
    if re.fullmatch(r"[A-Z]", token):
        return 2
    return min(2, token.count(".") + 1)


def assign_levels(tagged):
    """Merge wrapped heading lines and resolve each heading to h1 or h2.

    Numbering depth wins over typography, because the ACM template sets a section and
    its subsections at the same size. A bare number line supplies the depth for the
    heading text that follows it.
    """
    out = []
    pending = None  # a numbering token awaiting its heading text
    for kind, text, top in tagged:
        if kind != "head":
            pending = None
            out.append(("body", text))
            continue
        if NUM_TOKEN.match(text):
            pending = NUM_TOKEN.match(text).group(1)
            continue

        level = None
        if ROMAN_HEAD.match(text):
            # `I. INTRODUCTION` — a single-letter numeral would otherwise be read as
            # an `A.`-style subsection. Requiring all caps separates the two.
            out.append(("h1", text))
            pending = None
            continue
        if pending is not None:
            # Restore the period so the numbering strips cleanly later on.
            level, text, pending = depth_of(pending), f"{pending}. {text}", None
        elif DEPTH2.match(text):
            level = 2
        elif DEPTH1.match(text):
            level = 1
        if level is None:
            # Every real section heading here is numbered or is one of the few
            # unnumbered front-matter heads, so an unnumbered line straight after a
            # heading is that heading wrapping onto a second line.
            if (out and out[-1][0] in ("h1", "h2")
                    and not UNNUMBERED.match(text.strip().upper())):
                out[-1] = (out[-1][0], out[-1][1] + " " + text)
                continue
            level = 1 if top else 2
        out.append((f"h{level}", text))
    return out


def dehyphenate_and_reflow(lines: list[str]) -> str:
    """Join PDF lines into paragraphs, repairing words split across a line break."""
    buf = ""
    for raw in lines:
        text = raw.strip()
        if not text:
            continue
        if buf.endswith("-") and not buf.endswith("--"):
            # `turn-` + `ing` -> `turning`; keep the hyphen if the next word is capitalised
            # (a real compound such as `Human-AI` wrapped at the hyphen).
            buf = buf[:-1] + text if text[:1].islower() else buf + text
        elif buf:
            buf += " " + text
        else:
            buf = text
    # sentence-ending followed by a capital starts a new paragraph
    buf = re.sub(r"\s+", " ", buf).strip()
    return buf


def segment(tagged):
    """[(h1, h2|None, [body lines])] in document order."""
    out, h1, h2, body = [], None, None, []

    def flush():
        if h1 and body:
            out.append((h1, h2, list(body)))
        body.clear()

    for kind, text in tagged:
        if kind in ("h1", "h2") and TERMINAL.match(norm_heading(text)):
            break  # bibliography and appendix follow; neither is voice
        if kind == "h1":
            flush()
            h1, h2 = text, None
        elif kind == "h2":
            flush()
            h2 = text
        else:
            if CAPTION_START.match(text):
                continue
            body.append(text)
    flush()
    return out


def norm_heading(text: str) -> str:
    return NUM_PREFIX.sub("", text).strip().rstrip(".").upper()


# Front matter is only ever a top-level heading. Bold labels inside a figure ("Abstract",
# "Concrete") would otherwise be read as subsections and pull body text into abstract/.
H1_ONLY = {"abstract"}


def map_section(h1: str, h2: str | None, overrides: dict) -> str | None:
    """Subsection wins when it names a section type of its own; else inherit the parent."""
    for level, heading in ((2, h2), (1, h1)) if h2 else ((1, h1),):
        if heading is None:
            continue
        key = norm_heading(heading)
        if DROP_HEADINGS.match(key):
            return None
        if key in overrides:
            return overrides[key]
        for pattern, folder in SECTION_RULES:
            if folder in H1_ONLY and level != 1:
                continue
            if re.search(pattern, key):
                return folder
    return None


def build(paper, dry_run: bool):
    path = PAPERS_DIR / paper["file"]
    doc = pymupdf.open(path)
    body_size = modal_body_size(doc)
    lines = collect_lines(doc, body_size)
    tagged = classify(lines, body_size)
    sections = segment(tagged)
    overrides = PAPER_OVERRIDES.get(paper["key"], {})

    buckets: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
    unmapped = []
    for h1, h2, body in sections:
        folder = map_section(h1, h2, overrides)
        prose = dehyphenate_and_reflow(body)
        if not folder:
            if not DROP_HEADINGS.match(norm_heading(h2 or h1)) and len(prose) > 400:
                unmapped.append((h1, h2, len(prose.split())))
            continue
        if len(prose.split()) < 40:
            continue
        buckets[folder].append((h2 or h1, prose))

    name = paper.get("corpus_id") or paper["key"]
    total = 0
    for folder, chunks in sorted(buckets.items()):
        words = sum(len(p.split()) for _, p in chunks)
        total += words
        if dry_run:
            print(f"    {folder:24s} {words:6,d}w  <- {', '.join(h for h, _ in chunks)[:88]}")
        else:
            dest = OUT_DIR / folder
            dest.mkdir(parents=True, exist_ok=True)
            header = f"# {paper['key']} ({paper['venue']} {paper['year']}) — {folder}\n\n"
            text = header + "\n\n".join(f"## {h}\n\n{p}" for h, p in chunks) + "\n"
            (dest / f"{name}.md").write_text(text)
    if dry_run and unmapped:
        for h1, h2, w in unmapped:
            print(f"    {'UNMAPPED':24s} {w:6,d}w  <- {h2 or h1!r} (under {h1!r})")
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="print the section mapping without writing files")
    args = ap.parse_args()

    ids_file = pathlib.Path(__file__).resolve().parent / "corpus-ids.json"
    if ids_file.exists():
        ids = json.loads(ids_file.read_text())
        for p in PAPERS:
            if p["key"] in ids:
                p["corpus_id"] = str(ids[p["key"]])

    grand = 0
    for paper in PAPERS:
        if not (PAPERS_DIR / paper["file"]).exists():
            print(f"!! missing: {paper['file']}", file=sys.stderr)
            continue
        print(f"\n=== {paper['key']} ({paper['venue']} {paper['year']}) ===")
        grand += build(paper, args.dry_run)
    print(f"\nTotal corpus: {grand:,} words")
    if not args.dry_run:
        print(f"Written to {OUT_DIR}")


if __name__ == "__main__":
    main()
