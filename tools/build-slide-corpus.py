#!/usr/bin/env python3
"""Ingest Sangho's exported talk PDFs into the slide corpus.

    uv run --with pymupdf python tools/build-slide-corpus.py --wave 1
    uv run --with pymupdf python tools/build-slide-corpus.py --all

There is no export step. Apple Keynote is not installed on this machine, and
`tell application "Keynote"` resolves to a third-party app that declares Apple's
bundle identifier, so a scripted export would have driven the wrong application
without erroring. PDFs are exported by hand and dropped in PDF_INBOX.

Writes only into CORPUS_ROOT, which is outside every git working tree.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import fitz  # PyMuPDF

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from tools.slide_canon import (  # noqa: E402
    CANON,
    CORPUS_ROOT,
    CanonError,
    Deck,
    resolve_pdf,
)


def ingest_deck(
    deck: Deck,
    *,
    dpi: int = 150,
    inbox: pathlib.Path | None = None,
    corpus_root: pathlib.Path | None = None,
    allow_page_drift: bool = False,
) -> dict:
    pdf_path = resolve_pdf(deck, inbox)
    out_dir = (corpus_root or CORPUS_ROOT) / deck.slug
    slides_dir = out_dir / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    try:
        if doc.page_count != deck.pages and not allow_page_drift:
            raise CanonError(
                f"{deck.slug}: expected {deck.pages} pages, found {doc.page_count}. "
                f"A build-stages export changes what 'a slide' means for every "
                f"measured figure. Re-export with builds off, or pass "
                f"--allow-page-drift and update Deck.pages."
            )

        rect = doc[0].rect
        pad = len(str(doc.page_count))
        slides = []
        for index, page in enumerate(doc, start=1):
            name = f"{index:0{pad}d}.png"
            page.get_pixmap(dpi=dpi).save(slides_dir / name)
            slides.append(
                {
                    "index": index,
                    "image": f"slides/{name}",
                    "text": page.get_text().strip(),
                }
            )

        manifest = {
            "slug": deck.slug,
            "title": deck.title,
            "pages": doc.page_count,
            "geometry_pt": [rect.width, rect.height],
            "aspect": round(rect.width / rect.height, 4),
            "dpi": dpi,
            "slides": slides,
        }
    finally:
        doc.close()

    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--wave", type=int, help="ingest one phasing wave (1 or 2)")
    group.add_argument("--all", action="store_true", help="ingest every canon deck")
    parser.add_argument("--dpi", type=int, default=150)
    parser.add_argument("--allow-page-drift", action="store_true")
    args = parser.parse_args(argv)

    decks = CANON if args.all else [d for d in CANON if d.wave == args.wave]
    if not decks:
        parser.error(f"no decks in wave {args.wave}")

    for deck in decks:
        manifest = ingest_deck(
            deck, dpi=args.dpi, allow_page_drift=args.allow_page_drift
        )
        print(
            f"{deck.slug}: {manifest['pages']} slides, "
            f"{manifest['geometry_pt'][0]:.0f}x{manifest['geometry_pt'][1]:.0f} pt "
            f"(aspect {manifest['aspect']})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
