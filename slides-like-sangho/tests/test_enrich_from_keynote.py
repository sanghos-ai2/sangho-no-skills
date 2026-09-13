import importlib.util
import json
import pathlib

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
