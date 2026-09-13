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


def _solid_deck(slug, colors, root):
    """A deck of one slide per RGB colour in `colors`, each a full 64x48 PNG
    (the exact size `palette()` resizes to, so the resize is a no-op and every
    sampled pixel is exactly the requested colour — no antialiasing to worry
    about when asserting an exact split)."""
    from PIL import Image

    d = root / slug
    slides_dir = d / "slides"
    slides_dir.mkdir(parents=True)
    slides = []
    for i, rgb in enumerate(colors, start=1):
        name = f"{i:02d}.png"
        Image.new("RGB", (64, 48), rgb).save(slides_dir / name)
        slides.append({"index": i, "image": f"slides/{name}", "text": ""})
    m = {
        "slug": slug,
        "title": slug.title(),
        "pages": len(colors),
        "geometry_pt": [1024.0, 768.0],
        "aspect": 1.3333,
        "dpi": 36,
        "slides": slides,
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


# --- Controller ruling (fix round 1): neutral/chromatic palette split ------


def test_palette_all_white_deck_is_fully_neutral(tmp_path):
    _solid_deck("luminate", [(255, 255, 255)], tmp_path)
    result = audit.palette(audit.load_manifests(tmp_path), tmp_path)

    assert result["neutral_share"] == 1.0
    assert result["chromatic_share"] == 0.0
    assert result["accents"] == []


def test_palette_half_white_half_red_splits_and_ranks_red_first(tmp_path):
    _solid_deck("luminate", [(255, 255, 255), (255, 0, 0)], tmp_path)
    result = audit.palette(audit.load_manifests(tmp_path), tmp_path)

    assert result["neutral_share"] == pytest.approx(0.5, abs=0.01)
    assert result["chromatic_share"] == pytest.approx(0.5, abs=0.01)
    assert result["accents"]
    top_hex, top_share = result["accents"][0]
    assert top_hex == "#f00000"  # 255 binned to 16 levels/channel -> 240 = 0xf0
    assert top_share == pytest.approx(0.5, abs=0.01)


def test_mid_grey_counts_as_neutral_via_saturation_arm(tmp_path):
    # sat = 0 (mx == mn == 128), and mx=128 is well above the darkness cutoff —
    # this pins the `sat < 0.15` arm specifically.
    _solid_deck("luminate", [(128, 128, 128)], tmp_path)
    result = audit.palette(audit.load_manifests(tmp_path), tmp_path)

    assert result["neutral_share"] == 1.0
    assert result["accents"] == []


def test_dark_saturated_pixel_counts_as_neutral_via_darkness_arm(tmp_path):
    # sat = (30-0)/30 = 1.0 (maximally saturated) but mx=30 < 40 — this would
    # be wrongly classified chromatic if only the saturation arm existed.
    _solid_deck("luminate", [(30, 0, 0)], tmp_path)
    result = audit.palette(audit.load_manifests(tmp_path), tmp_path)

    assert result["neutral_share"] == 1.0
    assert result["accents"] == []


def test_report_palette_section_states_cutoffs_and_deck_count(tmp_path):
    _solid_deck("luminate", [(255, 0, 0)], tmp_path)
    manifests = audit.load_manifests(tmp_path)
    report = audit.render_report(manifests, audit.palette(manifests, tmp_path))

    assert "## Palette" in report
    assert "0.15" in report
    assert "40" in report
    assert "1 deck" in report
    assert "4 decks" not in report


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
