import importlib.util
import json
import pathlib

import pytest

from tools.slide_canon import CanonError, by_slug

_SPEC = importlib.util.spec_from_file_location(
    "enrich_from_keynote",
    pathlib.Path(__file__).resolve().parents[2] / "tools" / "enrich-from-keynote.py",
)
enrich = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(enrich)


def _manifest(root, slug="luminate", pages=2):
    d = root / slug
    d.mkdir(parents=True)
    m = {
        "slug": slug,
        "title": "Luminate",
        "pages": pages,
        "geometry_pt": [1024.0, 768.0],
        "aspect": 1.3333,
        "dpi": 36,
        "slides": [
            {"index": i, "image": f"slides/{i:02d}.png", "text": ""}
            for i in range(1, pages + 1)
        ],
    }
    (d / "manifest.json").write_text(json.dumps(m), encoding="utf-8")
    return m


def test_merge_adds_notes_and_masters_without_dropping_existing_fields(tmp_path):
    _manifest(tmp_path)
    merged = enrich.merge_extraction(
        json.loads((tmp_path / "luminate" / "manifest.json").read_text()),
        notes_by_index={1: "open cold, no title", 2: None},
        masters=["Title", "Blank", "Photo"],
    )
    assert merged["slides"][0]["notes"] == "open cold, no title"
    assert merged["slides"][1]["notes"] is None
    assert merged["masters"] == ["Title", "Blank", "Photo"]
    assert merged["geometry_pt"] == [1024.0, 768.0]  # untouched
    assert merged["slides"][0]["image"] == "slides/01.png"  # untouched


def test_merge_is_a_noop_when_extraction_yielded_nothing(tmp_path):
    # IWA extraction is allowed to fail. An empty result must leave the
    # manifest usable rather than stamping every slide with a false empty note.
    original = _manifest(tmp_path)
    merged = enrich.merge_extraction(dict(original), notes_by_index={}, masters=[])
    assert merged["masters"] == []
    assert all("notes" not in s for s in merged["slides"])


def test_merge_ignores_note_indices_outside_the_deck(tmp_path):
    original = _manifest(tmp_path, pages=2)
    merged = enrich.merge_extraction(
        dict(original), notes_by_index={1: "a", 99: "stray"}, masters=[]
    )
    assert len(merged["slides"]) == 2
    assert merged["slides"][0]["notes"] == "a"


# --- Task 6 / Part B: a CanonError from resolve_key must not be swallowed --


def test_canon_error_from_resolve_key_propagates_out_of_enrich_manifest(
    tmp_path, monkeypatch
):
    # Two distinct decks in the corpus share a filename; resolve_key's
    # byte-size check is what catches that. Reporting it as "IWA extraction
    # unavailable" would hide a corpus-integrity failure behind what reads
    # as a benign degradation.
    _manifest(tmp_path)
    deck = by_slug("luminate")

    def _wrong_deck(deck_, root):
        raise CanonError(
            f"{deck_.slug}: expected {deck_.key_bytes} bytes, found 271000000. "
            f"Refusing: filenames are not unique in this corpus."
        )

    monkeypatch.setattr(enrich, "resolve_key", _wrong_deck)

    with pytest.raises(CanonError, match="Refusing"):
        enrich.enrich_manifest(deck, corpus_root=tmp_path)


def test_extract_failure_still_degrades_to_empty_after_narrowing(tmp_path, monkeypatch):
    # A parse failure *inside* extract() (an unsupported/future .key format)
    # is the case this pass is still allowed to swallow -- resolve_key having
    # already succeeded, the deck's canon identity was never in question.
    _manifest(tmp_path)
    deck = by_slug("luminate")

    monkeypatch.setattr(
        enrich, "resolve_key", lambda deck_, root: tmp_path / "fake.key"
    )

    def _unsupported_format(key_path):
        raise ValueError("unsupported Keynote format")

    monkeypatch.setattr(enrich, "extract", _unsupported_format)

    merged = enrich.enrich_manifest(deck, corpus_root=tmp_path)
    assert merged["masters"] == []
    assert all("notes" not in s for s in merged["slides"])
