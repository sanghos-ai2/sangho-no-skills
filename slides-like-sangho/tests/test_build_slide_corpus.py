import importlib.util
import json
import pathlib

import fitz  # PyMuPDF
import pytest

from tools.slide_canon import CanonError, by_slug

_SPEC = importlib.util.spec_from_file_location(
    "build_slide_corpus",
    pathlib.Path(__file__).resolve().parents[2] / "tools" / "build-slide-corpus.py",
)
bsc = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(bsc)


def _fake_pdf(path: pathlib.Path, pages: int, width: float, height: float) -> None:
    """A synthetic deck. Tests never touch the real corpus — it lives outside
    the repo and is not distributed."""
    doc = fitz.open()
    for i in range(pages):
        page = doc.new_page(width=width, height=height)
        page.insert_text((72, 144), f"Slide {i + 1} headline", fontsize=44)
    doc.save(path)
    doc.close()


def test_ingest_writes_manifest_and_one_png_per_page(tmp_path):
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1024, height=768)

    out = tmp_path / "corpus"
    manifest = bsc.ingest_deck(deck, dpi=36, inbox=inbox, corpus_root=out)

    assert manifest["pages"] == deck.pages
    assert len(manifest["slides"]) == deck.pages
    assert len(list((out / deck.slug / "slides").glob("*.png"))) == deck.pages
    assert json.loads((out / deck.slug / "manifest.json").read_text()) == manifest


def test_ingest_measures_geometry_rather_than_assuming_sixteen_by_nine(tmp_path):
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1024, height=768)

    manifest = bsc.ingest_deck(
        deck, dpi=36, inbox=inbox, corpus_root=tmp_path / "corpus"
    )

    assert manifest["geometry_pt"] == [1024.0, 768.0]
    assert manifest["aspect"] == pytest.approx(4 / 3, abs=1e-3)


def test_ingest_extracts_per_slide_text(tmp_path):
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1024, height=768)

    manifest = bsc.ingest_deck(
        deck, dpi=36, inbox=inbox, corpus_root=tmp_path / "corpus"
    )

    assert manifest["slides"][0]["text"] == "Slide 1 headline"


def test_page_count_drift_fails_loudly(tmp_path):
    # A re-export with "print each stage of builds" on inflates the page count,
    # which silently changes what "a slide" means for every measured figure.
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages + 7, width=1024, height=768)

    with pytest.raises(CanonError, match="expected 55"):
        bsc.ingest_deck(deck, dpi=36, inbox=inbox, corpus_root=tmp_path / "corpus")


def test_page_count_drift_is_overridable(tmp_path):
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages + 7, width=1024, height=768)

    manifest = bsc.ingest_deck(
        deck,
        dpi=36,
        inbox=inbox,
        corpus_root=tmp_path / "corpus",
        allow_page_drift=True,
    )
    assert manifest["pages"] == deck.pages + 7


def test_filenames_are_zero_padded_to_sort_lexically(tmp_path):
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1024, height=768)

    bsc.ingest_deck(deck, dpi=36, inbox=inbox, corpus_root=tmp_path / "corpus")

    names = sorted(p.name for p in (tmp_path / "corpus" / deck.slug / "slides").glob("*.png"))
    assert names[0] == "01.png"
    assert names[-1] == "55.png"


def _fake_pdf_with_first_page_runs(
    path: pathlib.Path,
    pages: int,
    width: float,
    height: float,
    runs: list[tuple[tuple[float, float], str, float]],
) -> None:
    """Like `_fake_pdf`, but the first page's text runs are given explicitly as
    (position, text, fontsize) tuples, so span size + merging can be pinned.
    Remaining pages get `_fake_pdf`'s placeholder text so the page count still
    matches the deck (no page-count-drift noise in these tests)."""
    doc = fitz.open()
    for i in range(pages):
        page = doc.new_page(width=width, height=height)
        if i == 0:
            for pos, text, fontsize in runs:
                page.insert_text(pos, text, fontsize=fontsize)
        else:
            page.insert_text((72, 144), f"Slide {i + 1} headline", fontsize=44)
    doc.save(path)
    doc.close()


def test_ingest_preserves_span_font_size_for_a_single_run(tmp_path):
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf_with_first_page_runs(
        inbox / deck.pdf_name,
        pages=deck.pages,
        width=1024,
        height=768,
        runs=[((72, 144), "Slide 1 headline", 44)],
    )

    manifest = bsc.ingest_deck(
        deck, dpi=36, inbox=inbox, corpus_root=tmp_path / "corpus"
    )

    slide = manifest["slides"][0]
    assert slide["spans"] == [{"size": 44.0, "text": "Slide 1 headline"}]
    # A single-run slide's merged span text matches the flat `text` field
    # exactly — merging must not add or drop anything the flat extraction has.
    assert slide["spans"][0]["text"] == slide["text"]


def test_ingest_captures_two_different_font_sizes_in_reading_order(tmp_path):
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf_with_first_page_runs(
        inbox / deck.pdf_name,
        pages=deck.pages,
        width=1024,
        height=768,
        runs=[
            ((72, 144), "Big Title", 44),
            ((72, 300), "small caption text", 12),
        ],
    )

    manifest = bsc.ingest_deck(
        deck, dpi=36, inbox=inbox, corpus_root=tmp_path / "corpus"
    )

    assert manifest["slides"][0]["spans"] == [
        {"size": 44.0, "text": "Big Title"},
        {"size": 12.0, "text": "small caption text"},
    ]


def test_ingest_merges_consecutive_same_size_spans(tmp_path):
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf_with_first_page_runs(
        inbox / deck.pdf_name,
        pages=deck.pages,
        width=1024,
        height=768,
        runs=[
            ((72, 144), "First line", 20),
            ((72, 200), "Second line", 20),
        ],
    )

    manifest = bsc.ingest_deck(
        deck, dpi=36, inbox=inbox, corpus_root=tmp_path / "corpus"
    )

    # Two separate text runs at the identical size collapse into one span
    # entry rather than staying two — this is the assertion that actually
    # pins the merging rule (as opposed to merely not-splitting).
    assert manifest["slides"][0]["spans"] == [
        {"size": 20.0, "text": "First line Second line"}
    ]
