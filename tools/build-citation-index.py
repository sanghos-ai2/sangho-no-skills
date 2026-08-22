#!/usr/bin/env python3
"""Index the references Sangho has already cited, for write-like-sangho.

The skill distinguishes a citation Sangho has used before (reuse it freely) from a
new one (surface it for vetting). This builds the first list, by parsing the
reference sections of the corpus papers.

    uv run --with pymupdf python tools/build-citation-index.py

Writes write-like-sangho/examples/prior-citations.md, which is gitignored along with
the rest of the corpus. Reads the PDFs directly rather than an API, so it stays
runnable offline and is not subject to rate limits.
"""
from __future__ import annotations

import collections
import pathlib
import re

import pymupdf

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "build_corpus", pathlib.Path(__file__).resolve().parent / "build-corpus.py")
_bc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bc)

OUT = _bc.OUT_DIR / "prior-citations.md"

ENTRY_SPLIT = re.compile(r"\n?\[\s*(\d{1,3})\s*\]\s+")
# ACM: `Authors. 2013. Title. In Venue...`   IEEE: `Authors, "Title," venue, 2011.`
ACM_TITLE = re.compile(r"\.\s*(?:19|20)\d{2}[a-z]?\.\s*(.+?)\.\s+(?:In\b|Proceedings\b|[A-Z]|$)",
                       re.S)
IEEE_TITLE = re.compile(r"[“\"]\s*(.+?)\s*[,.]?\s*[”\"]", re.S)
# A bare 4-digit match also hits page ranges ("pp. 2057-2063"), so years are bounded
# and the ACM `Authors. 2013. Title.` position is preferred when present.
YEAR = re.compile(r"\b(19[4-9]\d|20[0-2]\d)\b")
ACM_YEAR = re.compile(r"\.\s*((?:19|20)\d{2})[a-z]?\.\s")


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("-\n", "").translate(_bc.LIGATURES)).strip()


def references_text(doc) -> str:
    full = "\n".join(page.get_text() for page in doc)
    match = None
    for m in re.finditer(r"\n\s*(?:[IVXLC]+\.\s*)?R\s?EFERENCES?\s*\n", full, re.I):
        match = m
    if not match:
        return ""
    tail = full[match.end():]
    # Stop at an appendix, which follows the references in several of these papers.
    stop = re.search(r"\n\s*(?:[A-Z]\s+)?APPENDI(?:X|CES)\b", tail)
    return tail[: stop.start()] if stop else tail


def parse_entries(text: str) -> list[tuple[str, str]]:
    """[(title, year)] for each numbered reference entry."""
    parts = ENTRY_SPLIT.split(text)
    out = []
    # parts = [preamble, num, body, num, body, ...]
    for body in parts[2::2]:
        body = clean(body)
        if len(body) < 25:
            continue
        title = None
        if m := IEEE_TITLE.search(body):
            title = m.group(1)
        elif m := ACM_TITLE.search(body):
            title = m.group(1)
        if not title:
            continue
        title = title.strip(" .,")
        if not (8 < len(title) < 300):
            continue
        if title.lower() in {"update later", "forthcoming", "in press", "to appear"}:
            continue
        if m := ACM_YEAR.search(body):
            year = m.group(1)
        else:
            years = YEAR.findall(body)
            year = years[-1] if years else "?"
        out.append((title, year))
    return out


def norm(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", title.lower())


def main() -> None:
    seen: dict[str, dict] = {}
    per_paper = {}
    for paper in _bc.PAPERS:
        path = _bc.PAPERS_DIR / paper["file"]
        if not path.exists():
            continue
        entries = parse_entries(references_text(pymupdf.open(path)))
        per_paper[paper["key"]] = len(entries)
        for title, year in entries:
            key = norm(title)
            if not key:
                continue
            rec = seen.setdefault(key, {"title": title, "year": year, "papers": []})
            if paper["key"] not in rec["papers"]:
                rec["papers"].append(paper["key"])
            # Keep the longest rendering of the title; PDFs truncate inconsistently.
            if len(title) > len(rec["title"]):
                rec["title"] = title

    records = sorted(seen.values(), key=lambda r: (-len(r["papers"]), r["title"].lower()))
    multi = [r for r in records if len(r["papers"]) > 1]

    lines = [
        "# Prior citations",
        "",
        f"{len(records)} unique references across {len(per_paper)} first-author papers, parsed "
        "from their reference sections. Anything here is a citation Sangho has used before: reuse "
        "it freely where it genuinely supports the text, and note it under bib-keeping the first "
        "time it enters a draft. Anything *not* here is a new citation and must be surfaced for "
        "vetting.",
        "",
        "Entries cited by more than one paper come first — that is the core literature.",
        "",
        f"Per paper: {', '.join(f'{k} ({n})' for k, n in per_paper.items())}",
        "",
        f"## Cited by more than one paper ({len(multi)})",
        "",
    ]
    for r in multi:
        lines.append(f"- **{r['title']}** ({r['year']}) — {', '.join(sorted(r['papers']))}")
    lines += ["", f"## Cited once ({len(records) - len(multi)})", ""]
    for r in records:
        if len(r["papers"]) == 1:
            lines.append(f"- {r['title']} ({r['year']}) — {r['papers'][0]}")

    OUT.write_text("\n".join(lines) + "\n")
    print(f"{len(records)} unique references ({len(multi)} cited more than once) -> {OUT}")
    for k, n in per_paper.items():
        print(f"  {k:16s} {n:3d} parsed")


if __name__ == "__main__":
    main()
