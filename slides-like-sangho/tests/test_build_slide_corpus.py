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
