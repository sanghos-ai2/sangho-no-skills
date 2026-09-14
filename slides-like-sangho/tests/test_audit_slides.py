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

    # chromatic_share is a fraction of ALL pixels; the pair with the assertion
    # below is what pins the two denominators apart — a uniform (wrong)
    # denominator would pass one of these but not both.
    assert result["neutral_share"] == pytest.approx(0.5, abs=0.01)
    assert result["chromatic_share"] == pytest.approx(0.5, abs=0.01)
    assert result["accents"]
    top = result["accents"][0]
    assert top["hex"] == "#f00000"  # 255 binned to 16 levels/channel -> 240 = 0xf0
    # accents is a fraction of CHROMATIC pixels only: red is the only
    # chromatic colour present, so it is ~100% of the chromatic share, not
    # ~50% of all pixels.
    assert top["share"] == pytest.approx(1.0, abs=0.01)
    # Concentration: with one red slide in a one-slide deck, 90% of the red
    # sits on that one slide. This is the column that lets a reader tell a
    # colour spent across a deck from one flat fill inside a screenshot.
    assert top["slides_for_90pc"] == 1
    assert top["slides_any"] == 1
    # The printed rows must state their own coverage; red is the only bin, so
    # the listed share is the whole of it.
    assert result["listed_share"] == pytest.approx(1.0, abs=0.01)
    assert result["distinct_bins"] == 1
    assert result["slides_sampled"] == 2


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


def test_palette_reports_zero_shares_when_no_images_exist_on_disk(tmp_path):
    # `_manifest` writes manifest.json (with a `slides/` dir) but no PNGs —
    # the manifest is real, but nothing was actually rendered. This must
    # produce the real-dict zero shape distinguishable from a legitimate
    # all-neutral reading, and render_report must degrade to the same
    # "no data" message it uses for the legacy []-sentinel — never claim
    # "100% neutral" for a corpus we could not measure at all.
    _manifest("luminate", ["a b"], tmp_path)
    manifests = audit.load_manifests(tmp_path)

    result = audit.palette(manifests, tmp_path)
    assert result == {"neutral_share": 0.0, "chromatic_share": 0.0, "accents": []}

    report = audit.render_report(manifests, result)
    assert "_No rendered slides available._" in report


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


# --- Controller ruling (fix round 1): notes-in-text-layer agreement --------


def test_agreement_counts_a_match_at_the_size_whose_span_text_equals_the_note():
    manifests = [
        {
            "slides": [
                {
                    "index": 1,
                    "notes": "hello world",
                    "spans": [
                        {"size": 12.8, "text": "hello world"},
                        {"size": 21.0, "text": "Title"},
                    ],
                }
            ]
        }
    ]
    result = audit.notes_span_agreement(manifests)
    assert result["slides_with_notes"] == 1
    assert result["slides_matching"] == 1
    assert result["size_breakdown"] == [(12.8, 1)]


def test_agreement_counts_no_match_when_note_differs_from_every_size():
    manifests = [
        {
            "slides": [
                {
                    "index": 1,
                    "notes": "something totally unrelated to the slide",
                    "spans": [
                        {"size": 12.8, "text": "hello world"},
                        {"size": 21.0, "text": "Title"},
                    ],
                }
            ]
        }
    ]
    result = audit.notes_span_agreement(manifests)
    assert result["slides_with_notes"] == 1
    assert result["slides_matching"] == 0
    assert result["size_breakdown"] == []


def test_agreement_handles_a_notes_bearing_slide_with_no_spans():
    # A slide can carry a real presenter note while contributing no spans at
    # all (a synthetic manifest, or a deck ingested before spans existed).
    # This must not raise, and must not count as a match.
    manifests = [{"slides": [{"index": 1, "notes": "hello world"}]}]
    result = audit.notes_span_agreement(manifests)
    assert result["slides_with_notes"] == 1
    assert result["slides_matching"] == 0
    assert result["size_breakdown"] == []


def test_agreement_matches_despite_whitespace_differences():
    # Real presenter notes carry blank-line breaks a span run does not; a
    # naive `==` on raw strings would fail this even though the words are
    # identical. Two separate same-size span runs (the real shape a timed
    # narration produces) must also be joined before comparing. This is also
    # an EXACT match once joined and normalized -- 8 words, right at the
    # containment threshold -- so it doubles as a check that exact equality
    # is not accidentally routed through the containment branch.
    manifests = [
        {
            "slides": [
                {
                    "index": 1,
                    "notes": "(15 s)\n\nHello world, this is the note.",
                    "spans": [
                        {"size": 12.8, "text": "(15 s)"},
                        {"size": 12.8, "text": "Hello world, this is the note."},
                    ],
                }
            ]
        }
    ]
    result = audit.notes_span_agreement(manifests)
    assert result["slides_with_notes"] == 1
    assert result["slides_matching"] == 1
    assert result["size_breakdown"] == [(12.8, 1)]


# --- Controller ruling (Task 6 fix round 1), Critical: containment guard ---


def test_containment_below_the_word_threshold_does_not_match():
    # A short heading is trivially a substring of a long free-form note by
    # chance -- this is the exact false-positive shape the review flagged.
    # "Questions?" is one word, far below NOTES_CONTAINMENT_MIN_WORDS (8).
    note = (
        "So that's basically the system, thanks for listening, any "
        "Questions? feel free to ask me anything about the study design."
    )
    assert len(note.split()) >= 8
    assert not audit._verbatim_match("Questions?", note)


def test_containment_at_or_above_the_word_threshold_matches():
    span = "Hello world this is a note with eight"
    assert len(span.split()) == audit.NOTES_CONTAINMENT_MIN_WORDS
    note = f"(15 s) {span} and then some more trailing narration after it"
    assert audit._verbatim_match(span, note)


def test_containment_one_word_below_the_threshold_does_not_match():
    # The boundary itself: one word short of the minimum must not match,
    # even though it otherwise would under a naive `in` check.
    span = "Hello world this is a note seven"
    assert len(span.split()) == audit.NOTES_CONTAINMENT_MIN_WORDS - 1
    note = f"(15 s) {span} and then some more trailing narration after it"
    assert not audit._verbatim_match(span, note)


def test_exact_equality_matches_regardless_of_length():
    # A naive implementation of the length guard could easily gate BOTH
    # branches (exact and containment) on the same minimum, breaking a
    # short note reproduced verbatim in full. Equality must always count.
    assert audit._verbatim_match("ok", "ok")
    assert audit._verbatim_match("hi there", "hi there")


def test_size_breakdown_lists_multiple_sizes_in_descending_count_order():
    manifests = [
        {
            "slides": [
                {
                    "index": 1,
                    "notes": "alpha bravo charlie",
                    "spans": [{"size": 12.8, "text": "alpha bravo charlie"}],
                },
                {
                    "index": 2,
                    "notes": "delta echo foxtrot",
                    "spans": [{"size": 30.0, "text": "delta echo foxtrot"}],
                },
                {
                    "index": 3,
                    "notes": "golf hotel india",
                    "spans": [{"size": 30.0, "text": "golf hotel india"}],
                },
            ]
        }
    ]
    result = audit.notes_span_agreement(manifests)
    assert result["slides_matching"] == 3
    # 30.0pt has two matches, 12.8pt has one -- descending by count.
    assert result["size_breakdown"] == [(30.0, 2), (12.8, 1)]


def test_notes_in_text_layer_section_degrades_when_no_slide_carries_notes(tmp_path):
    _manifest("luminate", ["a b", "c d e"], tmp_path)
    report = audit.render_report(audit.load_manifests(tmp_path), [])
    assert "### Notes in the text layer" in report
    assert "_No presenter notes to compare against the text layer._" in report


def test_notes_in_text_layer_section_reports_the_measured_agreement(tmp_path):
    _manifest_with_spans(
        "luminate",
        [
            [
                {"size": 12.8, "text": "hello world"},
                {"size": 21.0, "text": "Title"},
            ]
        ],
        tmp_path,
    )
    manifest_path = tmp_path / "luminate" / "manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["slides"][0]["notes"] = "hello world"
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    report = audit.render_report(audit.load_manifests(tmp_path), [])

    assert "### Notes in the text layer" in report
    assert "1 of 1 notes-bearing slides" in report
    assert "12.8pt" in report


# --- Controller ruling (Task 6 fix round 1), Important: data-driven caveat -


def test_word_count_caveat_keeps_notes_category_when_agreement_is_material():
    agreement = {"slides_with_notes": 10, "slides_matching": 5, "size_breakdown": []}
    lines = audit.word_count_caveat_lines(agreement)
    text = " ".join(lines)
    assert "text identical to the deck's presenter notes" in text
    assert "5 of 10 notes-bearing slides" in text
    assert "sums three unrelated things" in text


def test_word_count_caveat_drops_notes_category_when_agreement_is_negligible():
    # 1 of 20 is 5%, clearly under NOTES_CAVEAT_MATERIAL_SHARE (10%).
    agreement = {"slides_with_notes": 20, "slides_matching": 1, "size_breakdown": []}
    lines = audit.word_count_caveat_lines(agreement)
    text = " ".join(lines)
    assert "does not appear in the slide text layer" in text
    assert "text identical to the deck's presenter notes" not in text
    assert "sums onto one slide the actual slide copy" in text
    assert "1 of 20 notes-bearing slides" in text
    # With no chrome measured, the caveat must not invent a page-chrome clause.
    assert "page chrome" not in text


def test_word_count_caveat_names_page_chrome_only_when_measured():
    # build-slide-corpus.py's _extract_spans names four things get_text()
    # conflates -- slide copy, narration, figure text and PAGE CHROME -- and
    # this caveat used to name only two of them. The clause is data-driven so
    # it cannot outlive the data: a corpus with no slide numbers gets no
    # clause (asserted above), one with them gets the measured count.
    agreement = {"slides_with_notes": 20, "slides_matching": 1, "size_breakdown": []}
    text = " ".join(audit.word_count_caveat_lines(agreement, 173))
    assert "page chrome" in text
    assert "173 spans" in text


def test_report_reuse_frame_is_generated_and_omitted_when_unmeasured(tmp_path):
    # Every other figure in slide-audit.md is a count of SLIDES. When decks
    # reuse each other's slides that stops being a count of decisions, and the
    # four reference documents all open with that caveat -- so the file they
    # cite has to carry it too, generated rather than hand-written. And when
    # no renders are on disk the frame must be OMITTED, not printed as a zero
    # that reads like a finding.
    _manifest("luminate", ["a b"], tmp_path)
    manifests = audit.load_manifests(tmp_path)

    framed = audit.render_report(
        manifests,
        {"neutral_share": 1.0, "chromatic_share": 0.0, "accents": []},
        {
            "slides": 365,
            "distinct": 170,
            "per_deck": {"luminate": {"slides": 55, "twinned": 10}},
        },
    )
    assert "not 365" in framed
    assert "170 distinct designs" in framed
    assert "Twinned in another deck" in framed
    assert "10 (18%)" in framed

    bare = audit.render_report(
        manifests, {"neutral_share": 1.0, "chromatic_share": 0.0, "accents": []}
    )
    assert "distinct designs" not in bare
    assert "Twinned in another deck" not in bare


def test_page_chrome_spans_counts_only_a_slide_s_own_index(tmp_path):
    manifest = {
        "slides": [
            # the slide's own number -- chrome
            {"index": 7, "spans": [{"size": 22.0, "text": "7"}]},
            # a number that is not this slide's index -- content, not chrome
            {"index": 8, "spans": [{"size": 44.0, "text": "14"}]},
            # a number inside a phrase -- content
            {"index": 9, "spans": [{"size": 44.0, "text": "14 Professional Writers"}]},
        ]
    }
    assert audit.page_chrome_spans([manifest]) == 1


def test_word_count_caveat_handles_no_notes_data_at_all():
    agreement = {"slides_with_notes": 0, "slides_matching": 0, "size_breakdown": []}
    lines = audit.word_count_caveat_lines(agreement)
    text = " ".join(lines)
    assert "does not appear in the slide text layer" in text
    assert "text identical to the deck's presenter notes" not in text
    assert "no presenter notes have been extracted" in text
