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


def _no_key_root(tmp_path: pathlib.Path) -> pathlib.Path:
    """A `key_root` that resolves to no `.key` file for any canon deck.

    Every pre-existing test in this file predates the layout guard and
    fabricates 4:3 fixture PDFs that do not (and should not have to) match
    any deck's real Keynote slide aspect. Passing this keeps those tests off
    the guard's default `key_root` (the real `~/Desktop/presentation/previous`
    on this machine, per the global "tests never touch the real corpus or
    real `.key` files" rule) and lands them on the guard's degrade path
    (`layout_verified: None`) instead of a spurious mismatch.
    """
    return tmp_path / "no-such-key-root"


def test_ingest_writes_manifest_and_one_png_per_page(tmp_path):
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1024, height=768)

    out = tmp_path / "corpus"
    manifest = bsc.ingest_deck(
        deck, dpi=36, inbox=inbox, corpus_root=out, key_root=_no_key_root(tmp_path)
    )

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
        deck,
        dpi=36,
        inbox=inbox,
        corpus_root=tmp_path / "corpus",
        key_root=_no_key_root(tmp_path),
    )

    assert manifest["geometry_pt"] == [1024.0, 768.0]
    assert manifest["aspect"] == pytest.approx(4 / 3, abs=1e-3)


def test_ingest_extracts_per_slide_text(tmp_path):
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1024, height=768)

    manifest = bsc.ingest_deck(
        deck,
        dpi=36,
        inbox=inbox,
        corpus_root=tmp_path / "corpus",
        key_root=_no_key_root(tmp_path),
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
        bsc.ingest_deck(
            deck,
            dpi=36,
            inbox=inbox,
            corpus_root=tmp_path / "corpus",
            key_root=_no_key_root(tmp_path),
        )


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
        key_root=_no_key_root(tmp_path),
        allow_page_drift=True,
    )
    assert manifest["pages"] == deck.pages + 7


def test_filenames_are_zero_padded_to_sort_lexically(tmp_path):
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1024, height=768)

    bsc.ingest_deck(
        deck,
        dpi=36,
        inbox=inbox,
        corpus_root=tmp_path / "corpus",
        key_root=_no_key_root(tmp_path),
    )

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
        deck,
        dpi=36,
        inbox=inbox,
        corpus_root=tmp_path / "corpus",
        key_root=_no_key_root(tmp_path),
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
        deck,
        dpi=36,
        inbox=inbox,
        corpus_root=tmp_path / "corpus",
        key_root=_no_key_root(tmp_path),
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
        deck,
        dpi=36,
        inbox=inbox,
        corpus_root=tmp_path / "corpus",
        key_root=_no_key_root(tmp_path),
    )

    # Two separate text runs at the identical size collapse into one span
    # entry rather than staying two — this is the assertion that actually
    # pins the merging rule (as opposed to merely not-splitting).
    assert manifest["slides"][0]["spans"] == [
        {"size": 20.0, "text": "First line Second line"}
    ]


def test_a_size_that_recurs_after_another_size_is_not_merged_back(tmp_path):
    # The discriminator between "merge consecutive runs" (correct) and
    # "group every run by size" (wrong, and reading-order-destroying): a size
    # that RETURNS after an intervening different size must stay a separate,
    # later entry rather than being folded back into its earlier occurrence.
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf_with_first_page_runs(
        inbox / deck.pdf_name,
        pages=deck.pages,
        width=1024,
        height=768,
        runs=[
            ((72, 144), "First at forty four", 44),
            ((72, 300), "Middle at twelve", 12),
            ((72, 450), "Third at forty four again", 44),
        ],
    )

    manifest = bsc.ingest_deck(
        deck,
        dpi=36,
        inbox=inbox,
        corpus_root=tmp_path / "corpus",
        key_root=_no_key_root(tmp_path),
    )

    assert manifest["slides"][0]["spans"] == [
        {"size": 44.0, "text": "First at forty four"},
        {"size": 12.0, "text": "Middle at twelve"},
        {"size": 44.0, "text": "Third at forty four again"},
    ]


# --- Task 6 / Part A: layout guard ------------------------------------------


def test_layout_guard_accepts_a_matching_aspect(tmp_path, monkeypatch):
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    # A correctly-exported 16:9 PDF, matching the (mocked) deck slide size.
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1920, height=1080)

    monkeypatch.setattr(bsc, "resolve_key", lambda deck_, root: tmp_path / "fake.key")
    monkeypatch.setattr(bsc, "read_slide_size", lambda path: (1920.0, 1080.0))

    manifest = bsc.ingest_deck(
        deck, dpi=36, inbox=inbox, corpus_root=tmp_path / "corpus"
    )
    assert manifest["layout_verified"] is True


def test_layout_guard_rejects_a_slides_with_notes_export(tmp_path, monkeypatch):
    # The actual failure this guard exists for: a "Slides With Notes"/handout
    # export boxes the real 16:9 slide inside a 4:3 (or letter) page.
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1024, height=768)

    monkeypatch.setattr(bsc, "resolve_key", lambda deck_, root: tmp_path / "fake.key")
    monkeypatch.setattr(bsc, "read_slide_size", lambda path: (1920.0, 1080.0))

    with pytest.raises(CanonError) as excinfo:
        bsc.ingest_deck(deck, dpi=36, inbox=inbox, corpus_root=tmp_path / "corpus")

    message = str(excinfo.value)
    assert "1.3333" in message  # the PDF's (wrong) page aspect
    assert "1.7778" in message  # the deck's real slide aspect
    assert "Slides" in message  # re-export guidance names the fix


def test_layout_mismatch_is_overridable_and_records_false(tmp_path, monkeypatch):
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1024, height=768)

    monkeypatch.setattr(bsc, "resolve_key", lambda deck_, root: tmp_path / "fake.key")
    monkeypatch.setattr(bsc, "read_slide_size", lambda path: (1920.0, 1080.0))

    manifest = bsc.ingest_deck(
        deck,
        dpi=36,
        inbox=inbox,
        corpus_root=tmp_path / "corpus",
        allow_layout_mismatch=True,
    )
    assert manifest["layout_verified"] is False


def test_layout_guard_within_tolerance_is_accepted(tmp_path, monkeypatch):
    # 1280x720 has the identical 16:9 ratio to 1920x1080 -- a real deck
    # re-sized at export time, not a layout mistake -- and must not raise.
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1280, height=720)

    monkeypatch.setattr(bsc, "resolve_key", lambda deck_, root: tmp_path / "fake.key")
    monkeypatch.setattr(bsc, "read_slide_size", lambda path: (1920.0, 1080.0))

    manifest = bsc.ingest_deck(
        deck, dpi=36, inbox=inbox, corpus_root=tmp_path / "corpus"
    )
    assert manifest["layout_verified"] is True


def test_layout_guard_degrades_when_no_key_is_resolvable(tmp_path):
    # No monkeypatch at all: the default key_root (pointed at a directory
    # with nothing in it) makes resolve_key raise "no .key at path" -- this
    # must degrade to `None`, not raise, and ingestion must still complete.
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1024, height=768)

    manifest = bsc.ingest_deck(
        deck,
        dpi=36,
        inbox=inbox,
        corpus_root=tmp_path / "corpus",
        key_root=_no_key_root(tmp_path),
    )
    assert manifest["layout_verified"] is None
    assert manifest["pages"] == deck.pages  # ingestion proceeded


def test_layout_guard_degrades_when_show_archive_has_no_size(tmp_path, monkeypatch):
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1024, height=768)

    monkeypatch.setattr(bsc, "resolve_key", lambda deck_, root: tmp_path / "fake.key")
    monkeypatch.setattr(bsc, "read_slide_size", lambda path: None)

    manifest = bsc.ingest_deck(
        deck, dpi=36, inbox=inbox, corpus_root=tmp_path / "corpus"
    )
    assert manifest["layout_verified"] is None


def test_layout_guard_degrades_when_iwa_is_unreadable(tmp_path, monkeypatch):
    # keynote_parser missing, or a future/unsupported .key format -- either
    # way, "IWA unreadable" must degrade rather than block ingestion.
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1024, height=768)

    monkeypatch.setattr(bsc, "resolve_key", lambda deck_, root: tmp_path / "fake.key")

    def _boom(path):
        raise ImportError("keynote_parser is not installed")

    monkeypatch.setattr(bsc, "read_slide_size", _boom)

    manifest = bsc.ingest_deck(
        deck, dpi=36, inbox=inbox, corpus_root=tmp_path / "corpus"
    )
    assert manifest["layout_verified"] is None


def test_layout_guard_runs_before_any_rasterizing(tmp_path, monkeypatch):
    # The guard must reject a bad export before spending time/disk rasterizing
    # pages that will just be deleted. No PNGs should land on disk when the
    # mismatch raises.
    deck = by_slug("luminate")
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    _fake_pdf(inbox / deck.pdf_name, pages=deck.pages, width=1024, height=768)

    monkeypatch.setattr(bsc, "resolve_key", lambda deck_, root: tmp_path / "fake.key")
    monkeypatch.setattr(bsc, "read_slide_size", lambda path: (1920.0, 1080.0))

    out = tmp_path / "corpus"
    with pytest.raises(CanonError):
        bsc.ingest_deck(deck, dpi=36, inbox=inbox, corpus_root=out)

    assert not list((out / deck.slug / "slides").glob("*.png"))
