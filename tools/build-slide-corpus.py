#!/usr/bin/env python3
"""Ingest Sangho's exported talk PDFs into the slide corpus.

    uv run --with pymupdf python tools/build-slide-corpus.py --wave 1
    uv run --with pymupdf python tools/build-slide-corpus.py --all

There is no export step. Apple Keynote is not installed on this machine, and
`tell application "Keynote"` resolves to a third-party app that declares Apple's
bundle identifier, so a scripted export would have driven the wrong application
without erroring. PDFs are exported by hand and dropped in PDF_INBOX.

Writes only into CORPUS_ROOT, which is outside every git working tree.

A "Slides With Notes" or handout export boxes the 16:9 slide into the top of
a taller page and prints the presenter note below it -- every measured figure
downstream (geometry, palette, words-per-slide, font sizes) then silently
describes the PAGE, not the slide, with no error raised. `ingest_deck` guards
against this by cross-checking the exported PDF's page aspect against the
deck's real Keynote slide aspect, read straight out of `Index/Document.iwa`
(`tools.keynote_iwa.read_slide_size`, shared with `enrich-from-keynote.py` so
the two tools can't grow two different IWA readers). That check is
opportunistic, not a corpus-integrity gate: `keynote_parser` is an optional
dependency and the `.key` may be a future format `keynote_parser` cannot
read, so when the slide size cannot be determined for ANY reason -- no
`.key` resolvable, an unreadable/unsupported IWA payload, the dependency
missing -- the check degrades to a warning rather than blocking ingestion. A
deck we cannot check is not the same as a deck that fails the check.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import fitz  # PyMuPDF

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from tools.keynote_iwa import read_slide_size  # noqa: E402
from tools.slide_canon import (  # noqa: E402
    CANON,
    CORPUS_ROOT,
    CanonError,
    Deck,
    resolve_key,
    resolve_pdf,
)

# Tolerance on the |pdf_aspect - slide_aspect| difference before the layout
# guard raises. Not a percentage of either aspect -- a flat tolerance on the
# ratio itself, per the controller ruling.
LAYOUT_ASPECT_TOLERANCE = 0.02


def _extract_spans(page: fitz.Page) -> list[dict]:
    """Per-slide text with font sizes preserved, so downstream work can
    partition speaker narration / figure-embedded text / slide copy / page
    chrome by size — a partition `page.get_text()`'s flat string cannot
    support, since it conflates all of them into one string.

    Consecutive runs at the same (rounded) size are merged into one entry so
    the list stays short; this deliberately does not classify or threshold
    sizes — that split is per-deck (see CanonError docstring in this module's
    caller) and belongs downstream, over the whole corpus, not at ingest time.
    """
    spans: list[dict] = []
    for block in page.get_text("dict").get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span.get("text", "").strip()
                if not text:
                    continue
                size = round(span.get("size", 0.0), 1)
                if spans and spans[-1]["size"] == size:
                    spans[-1]["text"] = f'{spans[-1]["text"]} {text}'
                else:
                    spans.append({"size": size, "text": text})
    return spans


def _check_layout(
    deck: Deck,
    pdf_aspect: float,
    key_root: pathlib.Path | None,
    allow_layout_mismatch: bool,
) -> bool | None:
    """Cross-check `pdf_aspect` (the exported PDF's page aspect) against the
    deck's real Keynote slide aspect.

    Returns `True` (checked, matches), `False` (checked, mismatched, accepted
    via `allow_layout_mismatch`), or `None` (could not be determined -- no
    resolvable `.key`, an unreadable/unsupported IWA payload, or
    `keynote_parser` not installed). `None` is deliberately not a failure:
    this check is opportunistic. The corpus's actual canon-integrity gate is
    `resolve_key`'s byte-size check, enforced (and allowed to raise) in
    `enrich-from-keynote.py` -- see that module's docstring. Here, ANY
    failure to obtain a slide size -- including `resolve_key` finding no
    `.key`, or finding the wrong one -- means the check is simply unavailable
    for this ingest, not that the deck fails it.
    """
    try:
        key_path = resolve_key(deck, key_root)
        slide_size = read_slide_size(key_path)
        if slide_size is None:
            raise CanonError(f"{deck.slug}: .key carries no KN.ShowArchive size")
    except Exception as exc:
        print(
            f"{deck.slug}: could not verify slide layout ({exc}); "
            f"proceeding without a layout check.",
            file=sys.stderr,
        )
        return None

    width, height = slide_size
    slide_aspect = round(width / height, 4)
    if abs(pdf_aspect - slide_aspect) <= LAYOUT_ASPECT_TOLERANCE:
        return True

    if not allow_layout_mismatch:
        raise CanonError(
            f"{deck.slug}: PDF page aspect {pdf_aspect} does not match the "
            f"deck's slide aspect {slide_aspect} ({width:.0f}x{height:.0f} pt). "
            f"This PDF is probably a \"Slides With Notes\" or handout export "
            f"-- it boxes the slide above a printed presenter note instead of "
            f"filling the page, which silently changes what every measured "
            f"figure (geometry, palette, words-per-slide, font sizes) "
            f"describes. Re-export from Keynote with Layout set to Slides, "
            f"or pass --allow-layout-mismatch to accept this export anyway."
        )
    return False


def ingest_deck(
    deck: Deck,
    *,
    dpi: int = 150,
    inbox: pathlib.Path | None = None,
    corpus_root: pathlib.Path | None = None,
    key_root: pathlib.Path | None = None,
    allow_page_drift: bool = False,
    allow_layout_mismatch: bool = False,
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
        pdf_aspect = round(rect.width / rect.height, 4)
        layout_verified = _check_layout(
            deck, pdf_aspect, key_root, allow_layout_mismatch
        )

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
                    "spans": _extract_spans(page),
                }
            )

        manifest = {
            "slug": deck.slug,
            "title": deck.title,
            "pages": doc.page_count,
            "geometry_pt": [rect.width, rect.height],
            "aspect": pdf_aspect,
            "dpi": dpi,
            "layout_verified": layout_verified,
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
    parser.add_argument("--allow-layout-mismatch", action="store_true")
    args = parser.parse_args(argv)

    decks = CANON if args.all else [d for d in CANON if d.wave == args.wave]
    if not decks:
        parser.error(f"no decks in wave {args.wave}")

    layout_note = {
        True: "layout verified",
        False: "layout NOT verified (--allow-layout-mismatch)",
        None: "layout unchecked",
    }
    for deck in decks:
        manifest = ingest_deck(
            deck,
            dpi=args.dpi,
            allow_page_drift=args.allow_page_drift,
            allow_layout_mismatch=args.allow_layout_mismatch,
        )
        print(
            f"{deck.slug}: {manifest['pages']} slides, "
            f"{manifest['geometry_pt'][0]:.0f}x{manifest['geometry_pt'][1]:.0f} pt "
            f"(aspect {manifest['aspect']}) -- {layout_note[manifest['layout_verified']]}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
