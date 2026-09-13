import importlib.util
import json
import pathlib

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "audit_slides",
    pathlib.Path(__file__).resolve().parents[2] / "tools" / "audit-slides.py",
)
audit = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(audit)


def _manifest(slug, texts, root):
    d = root / slug
    (d / "slides").mkdir(parents=True)
    m = {
        "slug": slug,
        "title": slug.title(),
        "pages": len(texts),
        "geometry_pt": [1024.0, 768.0],
        "aspect": 1.3333,
        "dpi": 36,
        "slides": [
            {"index": i, "image": f"slides/{i:02d}.png", "text": t}
            for i, t in enumerate(texts, start=1)
        ],
    }
    (d / "manifest.json").write_text(json.dumps(m), encoding="utf-8")
    return m


def _manifest_with_spans(slug, spans_per_slide, root):
    """Like `_manifest`, but each slide carries a `spans` list instead of a
    bare `text` string — the shape `size_histogram` reads."""
    d = root / slug
    (d / "slides").mkdir(parents=True)
    m = {
        "slug": slug,
        "title": slug.title(),
        "pages": len(spans_per_slide),
        "geometry_pt": [1024.0, 768.0],
        "aspect": 1.3333,
        "dpi": 36,
        "slides": [
            {
                "index": i,
                "image": f"slides/{i:02d}.png",
                "text": " ".join(s["text"] for s in spans),
                "spans": spans,
            }
            for i, spans in enumerate(spans_per_slide, start=1)
        ],
    }
    (d / "manifest.json").write_text(json.dumps(m), encoding="utf-8")
    return m


def test_word_stats_reports_distribution_not_just_a_mean(tmp_path):
    _manifest("luminate", ["a b c", "a", "a b c d e f g", "a b"], tmp_path)
    stats = audit.word_stats(audit.load_manifests(tmp_path))

    assert stats["slides"] == 4
    assert stats["decks"] == 1
    assert stats["max"] == 7
    assert stats["median"] == pytest.approx(2.5)
    assert stats["share_under_four"] == pytest.approx(0.75)


def test_empty_slides_count_as_zero_words_not_as_missing(tmp_path):
    # A full-bleed figure slide has no text. That is a measurement, not a gap:
    # dropping it would inflate every words-per-slide figure.
    _manifest("luminate", ["", "", "a b c d"], tmp_path)
    stats = audit.word_stats(audit.load_manifests(tmp_path))
    assert stats["slides"] == 3
    assert stats["median"] == pytest.approx(0.0)


def test_report_labels_every_figure_with_its_deck_count(tmp_path):
    _manifest("luminate", ["a b"], tmp_path)
    report = audit.render_report(audit.load_manifests(tmp_path), [])
    assert "1 deck" in report
    assert "4 decks" not in report


def test_report_names_the_measured_aspect_ratio(tmp_path):
    _manifest("luminate", ["a b"], tmp_path)
    report = audit.render_report(audit.load_manifests(tmp_path), [])
    assert "1024" in report and "768" in report


def test_load_manifests_is_sorted_and_skips_incomplete_decks(tmp_path):
    _manifest("sensecape", ["a"], tmp_path)
    _manifest("luminate", ["a"], tmp_path)
    (tmp_path / "halfbuilt" / "slides").mkdir(parents=True)  # no manifest.json
    assert [m["slug"] for m in audit.load_manifests(tmp_path)] == [
        "luminate",
        "sensecape",
    ]


# --- Controller ruling A: words-by-font-size histogram ---------------------


def test_size_histogram_sums_words_per_size_across_slides_and_decks(tmp_path):
    _manifest_with_spans(
        "luminate",
        [
            [
                {"size": 21.0, "text": "a b c"},
                {"size": 12.8, "text": "d e"},
            ],
            [
                {"size": 21.0, "text": "f"},
            ],
        ],
        tmp_path,
    )
    _manifest_with_spans(
        "sensecape",
        [[{"size": 12.8, "text": "g h i j"}]],
        tmp_path,
    )

    hist = audit.size_histogram(audit.load_manifests(tmp_path))

    assert dict(hist) == {21.0: 4, 12.8: 6}
    # descending by word count
    assert hist[0] == (12.8, 6)
    assert hist[1] == (21.0, 4)


def test_size_histogram_skips_manifests_with_no_spans_key(tmp_path):
    # A manifest ingested before spans were captured (or a synthetic test
    # manifest using the plain `text`-only shape) must not raise.
    _manifest("luminate", ["a b c", "d e"], tmp_path)
    hist = audit.size_histogram(audit.load_manifests(tmp_path))
    assert hist == []


def test_size_histogram_section_carries_its_deck_count_label(tmp_path):
    _manifest_with_spans(
        "luminate", [[{"size": 21.0, "text": "a b c"}]], tmp_path
    )
    report = audit.render_report(audit.load_manifests(tmp_path), [])
    assert "## Words by font size" in report
    assert "1 deck" in report
    assert "4 decks" not in report


def test_report_states_raw_word_count_is_an_upper_bound(tmp_path):
    _manifest("luminate", ["a b"], tmp_path)
    report = audit.render_report(audit.load_manifests(tmp_path), [])
    assert "upper bound" in report.lower()


# --- Controller ruling B: presenter-notes density ---------------------------


def test_notes_section_reports_none_extracted_when_no_slide_has_notes(tmp_path):
    _manifest("luminate", ["a b", "c d e"], tmp_path)
    report = audit.render_report(audit.load_manifests(tmp_path), [])
    assert "_No presenter notes extracted._" in report


def test_notes_section_reports_counts_when_some_slides_have_notes(tmp_path):
    _manifest("luminate", ["a b", "c d e", "f"], tmp_path)
    manifest_path = tmp_path / "luminate" / "manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["slides"][0]["notes"] = "one two three four"
    data["slides"][1]["notes"] = None
    # slide 3 carries no "notes" key at all — never extracted for that slide
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    report = audit.render_report(audit.load_manifests(tmp_path), [])

    assert "_No presenter notes extracted._" not in report
    assert "## Presenter notes" in report
    assert "1 of 3" in report
    assert "1 deck" in report
