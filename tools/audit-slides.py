#!/usr/bin/env python3
"""Measure Sangho's slide corpus, so slides-like-sangho can cite evidence.

    uv run --with pillow python tools/audit-slides.py

Every figure quoted in slides-like-sangho/references/ comes from this script and
is labelled with the number of decks behind it. A one-deck measurement must never
be mistaken for a corpus-wide one: during wave 1 the corpus is Luminate alone.
"""
from __future__ import annotations

import collections
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from tools.slide_canon import CORPUS_ROOT  # noqa: E402

REPORT = pathlib.Path(__file__).resolve().parent / "slide-audit.md"


def load_manifests(corpus_root: pathlib.Path | None = None) -> list[dict]:
    root = corpus_root or CORPUS_ROOT
    manifests = []
    for path in sorted(root.glob("*/manifest.json")):
        manifests.append(json.loads(path.read_text(encoding="utf-8")))
    return manifests


def _word_counts(manifests: list[dict]) -> list[int]:
    return [
        len(slide["text"].split())
        for manifest in manifests
        for slide in manifest["slides"]
    ]


def word_stats(manifests: list[dict]) -> dict:
    counts = _word_counts(manifests)
    if not counts:
        return {
            "decks": len(manifests),
            "slides": 0,
            "median": 0.0,
            "p25": 0.0,
            "p75": 0.0,
            "max": 0,
            "share_under_four": 0.0,
        }
    ordered = sorted(counts)
    quartiles = statistics.quantiles(ordered, n=4) if len(ordered) > 1 else [
        ordered[0],
        ordered[0],
        ordered[0],
    ]
    return {
        "decks": len(manifests),
        "slides": len(counts),
        "median": statistics.median(ordered),
        "p25": quartiles[0],
        "p75": quartiles[2],
        "max": max(counts),
        "share_under_four": sum(1 for c in counts if c < 4) / len(counts),
    }


def size_histogram(manifests: list[dict]) -> list[tuple[float, int]]:
    """Total words per font size across every slide, descending by word count.

    Reads `slides[].spans` (Task 2's per-run-of-size text, sizes rounded to 1
    decimal). A manifest whose slides carry no `spans` key — a synthetic test
    manifest, or one ingested before spans were captured — contributes nothing
    rather than raising.

    This deliberately does NOT classify a size as slide-copy / narration /
    figure-text. That split is per-deck (see Ruling A / the module docstring
    in build-slide-corpus.py): the timing-marker convention that puts speaker
    narration at 12.8pt on Luminate does not hold across the whole canon, and
    wave 1 is one deck. The histogram exists so that call can be made later,
    over all four decks, by someone looking at the actual slides — not baked
    in here from a single data point.
    """
    tally: dict[float, int] = collections.defaultdict(int)
    for manifest in manifests:
        for slide in manifest.get("slides", []):
            for span in slide.get("spans", []):
                tally[span["size"]] += len(span["text"].split())
    return sorted(tally.items(), key=lambda kv: kv[1], reverse=True)


def _notes_word_counts(manifests: list[dict]) -> list[int]:
    """Word counts of every slide carrying a non-null `notes` field.

    `notes` is optional (Task 4's IWA enrichment); most manifests won't have
    it yet, and that is recorded, not hidden.
    """
    counts = []
    for manifest in manifests:
        for slide in manifest.get("slides", []):
            notes = slide.get("notes")
            if notes is not None:
                counts.append(len(notes.split()))
    return counts


def _normalize_ws(text: str) -> str:
    return " ".join(text.split())


# Fix round 1 (Task 6 review), Critical: a bare containment check
# (`a in b or b in a`) matches a short heading against a long free-form note
# with no regard for how much of either string actually overlaps -- median
# note length is 22.5 words, so a 2-3 word title has ample room to appear
# inside one by chance. Below this many words, containment does not count;
# exact equality always counts regardless of length, since a short note can
# legitimately be reproduced verbatim in full.
NOTES_CONTAINMENT_MIN_WORDS = 8


def _verbatim_match(norm_span: str, norm_note: str) -> bool:
    """Whether a slide's own text-layer span, at one font size, agrees with
    its presenter note -- exact equality always counts (a short note can be
    reproduced in full), containment counts only when the CONTAINED string
    clears `NOTES_CONTAINMENT_MIN_WORDS` (see that constant's docstring)."""
    if norm_span == norm_note:
        return True
    if norm_span and norm_span in norm_note:
        return len(norm_span.split()) >= NOTES_CONTAINMENT_MIN_WORDS
    if norm_note and norm_note in norm_span:
        return len(norm_note.split()) >= NOTES_CONTAINMENT_MIN_WORDS
    return False


def notes_span_agreement(manifests: list[dict]) -> dict:
    """Measure whether a slide's presenter note also appears in its own PDF
    text layer, and if so, at which font size(s).

    A one-deck controller measurement found the deck's 12.8pt span band to be
    exactly the presenter note text on every notes-bearing Luminate slide.
    That is a fact about ONE deck's text layer, not a mechanism (visible on
    the slide? exported by Keynote? pasted into a text box?), and not a size
    that necessarily holds on wave 2 — so it is computed here, from whatever
    manifests are handed in, rather than hard-coded. If a future deck breaks
    the pattern, the numbers this returns move on their own.

    For each slide carrying a non-null `notes`, spans are grouped by their
    (already-rounded) `size` and each size's span text is compared, after
    whitespace normalization, against the normalized note via
    `_verbatim_match` (see `NOTES_CONTAINMENT_MIN_WORDS`). A slide contributes
    at most one match, at the first size found to agree with its note.

    Returns `{"slides_with_notes": int, "slides_matching": int,
    "size_breakdown": list[(float, int)]}` -- `size_breakdown` is every size
    that produced at least one match, sorted by match count descending (ties
    broken by size ascending, for a reproducible order), never collapsed to
    a single plurality size: a single dominant size and a scattering of
    single-slide matches across many sizes are different findings, and a
    "modal size" sentence cannot tell a reader which one it is looking at.
    Empty when nothing matched (or no slide had notes to compare at all).
    """
    slides_with_notes = 0
    slides_matching = 0
    match_size_tally: collections.Counter = collections.Counter()

    for manifest in manifests:
        for slide in manifest.get("slides", []):
            notes = slide.get("notes")
            if notes is None:
                continue
            slides_with_notes += 1
            norm_note = _normalize_ws(notes)
            if not norm_note:
                continue

            spans_by_size: dict[float, list[str]] = collections.defaultdict(list)
            for span in slide.get("spans", []):
                spans_by_size[span["size"]].append(span["text"])

            for size, texts in spans_by_size.items():
                norm_span = _normalize_ws(" ".join(texts))
                if not norm_span:
                    continue
                if _verbatim_match(norm_span, norm_note):
                    slides_matching += 1
                    match_size_tally[size] += 1
                    break

    size_breakdown = sorted(
        match_size_tally.items(), key=lambda kv: (-kv[1], kv[0])
    )
    return {
        "slides_with_notes": slides_with_notes,
        "slides_matching": slides_matching,
        "size_breakdown": size_breakdown,
    }


# Fix round 1 (Task 6 review), Important: the "Words per slide" caveat used
# to state, as a standing fact, that presenter-note text is one of three
# things page.get_text() sums onto a slide. That was true of the stale
# notes-layout export (100% of notes-bearing slides duplicated their note at
# print size) and is not true of the clean export (a small, likely-spurious
# share even before the Critical fix above is applied). The threshold below
# decides, from the MEASURED agreement, whether the notes category still
# belongs in that sentence -- so the sentence can't outlive the data twice.
NOTES_CAVEAT_MATERIAL_SHARE = 0.10  # of notes-bearing slides


def page_chrome_spans(manifests: list[dict]) -> int:
    """Spans that are a bare integer equal to their own slide's index.

    `_extract_spans` (build-slide-corpus.py) names four things `get_text()`
    conflates -- slide copy, speaker narration, figure-embedded text and PAGE
    CHROME. On the branch where presenter-note text is immaterial the caveat
    below used to name only two of those four (slide copy and figure-embedded
    text), which made it disagree with the ingest module about its own data.
    This counts the chrome instead of asserting it.
    """
    import re

    return sum(
        1
        for manifest in manifests
        for slide in manifest["slides"]
        for span in slide.get("spans", [])
        if re.fullmatch(r"\d{1,3}", span["text"].strip())
        and int(span["text"].strip()) == slide["index"]
    )


def word_count_caveat_lines(agreement: dict, chrome_spans: int = 0) -> list[str]:
    """The explanatory paragraph under 'Words per slide', built from
    `notes_span_agreement`'s measured result rather than stated as a standing
    fact. When presenter-note text materially appears in the text layer
    (`slides_matching / slides_with_notes >= NOTES_CAVEAT_MATERIAL_SHARE`),
    the notes category stays in the list, with its measured figure. When it
    is negligible -- or there is no notes data to measure at all -- the
    category is dropped from the list entirely and the paragraph says so
    plainly, rather than instructing the reader to cross-reference a figure
    that would contradict it.
    """
    with_notes = agreement["slides_with_notes"]
    matching = agreement["slides_matching"]
    material = with_notes > 0 and matching / with_notes >= NOTES_CAVEAT_MATERIAL_SHARE

    if material:
        return [
            "**This is an upper bound, not slide copy.** These counts come from",
            "`page.get_text()`, which sums three unrelated things onto one slide:",
            "the actual slide copy, text identical to the deck's presenter notes",
            f"(matched on {matching} of {with_notes} notes-bearing slides — see",
            "\"Notes in the text layer\" under Presenter notes for the per-size",
            "breakdown), and text baked inside embedded figures. See \"Words by",
            "font size\" below for the breakdown a threshold would need — this",
            "script does not pick one.",
        ]

    if with_notes > 0:
        detail = (
            f"measured at {matching} of {with_notes} notes-bearing slides, "
            f"below the {NOTES_CAVEAT_MATERIAL_SHARE:.0%} materiality bar this "
            "script uses"
        )
    else:
        detail = "no presenter notes have been extracted for this corpus yet"

    chrome = (
        f",\nand the deck's own page chrome ({chrome_spans} spans in this corpus"
        "\nare a bare integer equal to their own slide's index)"
        if chrome_spans
        else ""
    )
    return [
        "**This is an upper bound, not slide copy.** These counts come from",
        "`page.get_text()`, which sums onto one slide the actual slide copy,",
        f"text baked inside embedded figures{chrome}. Presenter-note",  # noqa: E501
        "text does not appear in the slide text layer in this corpus",
        f"({detail} — see \"Notes in the text layer\" under Presenter notes).",
        "See \"Words by font size\" below for the breakdown a threshold would",
        "need — this script does not pick one.",
    ]


REUSE_MAE_CUTOFF = 3.0
REUSE_THUMB = (64, 36)


def reuse_stats(
    manifests: list[dict], corpus_root: pathlib.Path | None = None
) -> dict:
    """How much of the corpus is the same slide appearing twice.

    Every other figure in this report is a count of SLIDES. When one deck
    carries another deck's slides, a slide count stops being a count of
    decisions, and a reader who treats 365 slides as 365 independent
    observations will over-credit whatever those reused slides happen to do.
    This measures that directly so the header can say it, rather than leaving
    every consumer of this file to discover it.

    Two slides are "the same" when their 64x36 box-filtered renders differ by
    less than REUSE_MAE_CUTOFF in mean absolute RGB. That is deliberately
    strict enough to ignore ordinary visual similarity and loose enough to
    survive re-export: on this corpus it separates pixel-identical reuse from
    a redrawn version of the same figure.

    Returns per-deck twin counts plus a corpus-wide distinct-design count.
    Degrades to an empty dict when no renders are on disk, so the report can
    omit the frame rather than print a zero that looks like a finding.
    """
    from PIL import Image

    root = corpus_root or CORPUS_ROOT
    vectors: dict[tuple[str, int], list[tuple[int, int, int]]] = {}
    for manifest in manifests:
        for slide in manifest["slides"]:
            path = root / manifest["slug"] / slide["image"]
            if not path.is_file():
                continue
            with Image.open(path) as img:
                thumb = img.convert("RGB").resize(REUSE_THUMB, Image.BOX)
            vectors[(manifest["slug"], slide["index"])] = list(thumb.getdata())
    if not vectors:
        return {}

    keys = sorted(vectors)
    parent = {k: k for k in keys}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    px = REUSE_THUMB[0] * REUSE_THUMB[1] * 3
    for i, a in enumerate(keys):
        va = vectors[a]
        for b in keys[i + 1 :]:
            vb = vectors[b]
            total = 0
            for (r1, g1, b1), (r2, g2, b2) in zip(va, vb):
                total += abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)
            if total / px < REUSE_MAE_CUTOFF:
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[ra] = rb

    groups: dict = collections.defaultdict(list)
    for k in keys:
        groups[find(k)].append(k)

    cross = [g for g in groups.values() if len({x[0] for x in g}) > 1]
    twins: collections.Counter = collections.Counter()
    for g in cross:
        for slug, _ in g:
            twins[slug] += 1
    return {
        "slides": len(keys),
        "distinct": len(groups),
        "per_deck": {
            m["slug"]: {
                "slides": sum(1 for k in keys if k[0] == m["slug"]),
                "twinned": twins[m["slug"]],
            }
            for m in manifests
        },
    }


NEUTRAL_SAT_CUTOFF = 0.15
NEUTRAL_MAX_CHANNEL_CUTOFF = 40
ACCENT_BIN_LEVELS = 16


def palette(
    manifests: list[dict],
    corpus_root: pathlib.Path | None = None,
    top: int = 8,
) -> dict:
    """Split rendered-slide pixels into neutral vs chromatic, and rank the
    chromatic "accent" colours.

    Tallying exact RGB values (the original design) reported six imperceptibly
    different whites in the top 8 rows on a real deck — "the slides are white,
    and also slightly different whites" — which cannot inform a design
    language's colour choices. This instead classifies every sampled pixel as
    neutral or chromatic and only bins + tallies the chromatic ones, so the
    accent table reports colour that is actually there rather than
    antialiasing noise around white.

    Classification, per pixel (mx = max(r,g,b), mn = min(r,g,b)):
    - sat = 0 if mx == 0 else (mx - mn) / mx
    - neutral when sat < NEUTRAL_SAT_CUTOFF or mx < NEUTRAL_MAX_CHANNEL_CUTOFF;
      otherwise chromatic
    Chromatic pixels are binned to ACCENT_BIN_LEVELS (16) levels per channel
    before tallying, so close accent hues group into one row instead of
    fragmenting into near-duplicates.

    Returns `{"neutral_share": float, "chromatic_share": float,
    "accents": list[(hex, share_of_chromatic_pixels)]}`.

    `neutral_share` and `chromatic_share` are fractions of ALL sampled pixels
    (they sum to 1.0, when any pixels were sampled at all) — they are the
    bridge between the two denominators in this return value. `accents`
    shares are fractions of CHROMATIC pixels only: dividing by all pixels
    (the first cut of this fix) reintroduced the exact failure this rewrite
    exists to close — with ~98% of pixels typically neutral, every accent's
    share of *all* pixels rounds to 0.0% at one decimal, which is as
    uninformative as the near-identical whites this function replaced.
    Re-denominating to chromatic pixels answers the question a design
    language actually asks: when colour is spent, on what?

    No accent colour is named or interpreted here; that is left to whoever
    looks at the actual slides.
    """
    from PIL import Image

    root = corpus_root or CORPUS_ROOT
    neutral = 0
    chromatic = 0
    accent_tally: collections.Counter = collections.Counter()
    # Per-colour, per-slide tallies, so the report can say how CONCENTRATED a
    # colour is. A bin spread thinly over many slides behaves like an accent; a
    # bin whose mass sits on a handful of slides is far more likely to be one
    # flat fill inside a screenshot, which is not a design choice at all. The
    # report prints the concentration beside each share rather than asserting
    # either reading.
    by_slide: dict[tuple[int, int, int], collections.Counter] = (
        collections.defaultdict(collections.Counter)
    )
    slides_sampled = 0
    for manifest in manifests:
        for slide in manifest["slides"]:
            path = root / manifest["slug"] / slide["image"]
            if not path.is_file():
                continue
            key = (manifest["slug"], slide["index"])
            slides_sampled += 1
            with Image.open(path) as img:
                small = img.convert("RGB").resize((64, 48))
                for count, (r, g, b) in small.getcolors(maxcolors=64 * 48):
                    mx = max(r, g, b)
                    mn = min(r, g, b)
                    sat = 0 if mx == 0 else (mx - mn) / mx
                    if sat < NEUTRAL_SAT_CUTOFF or mx < NEUTRAL_MAX_CHANNEL_CUTOFF:
                        neutral += count
                    else:
                        chromatic += count
                        binned = (
                            r // ACCENT_BIN_LEVELS * ACCENT_BIN_LEVELS,
                            g // ACCENT_BIN_LEVELS * ACCENT_BIN_LEVELS,
                            b // ACCENT_BIN_LEVELS * ACCENT_BIN_LEVELS,
                        )
                        accent_tally[binned] += count
                        by_slide[binned][key] += count

    total = neutral + chromatic
    if total == 0:
        return {"neutral_share": 0.0, "chromatic_share": 0.0, "accents": []}
    # Explicit guard, not incidental: when nothing was classified chromatic,
    # accent_tally is empty anyway, but stating the zero-division avoidance
    # here (rather than relying on that coincidence) is what makes it a
    # guard rather than a lucky accident of the tallying logic above.
    def _concentration(rgb: tuple[int, int, int]) -> tuple[int, int]:
        """(slides carrying 90% of this bin's pixels, slides carrying any).

        Reported, not interpreted: a low first number against a large corpus
        means the colour is not spread across the deck.
        """
        counts = sorted(by_slide[rgb].values(), reverse=True)
        target = 0.9 * sum(counts)
        running = 0
        for taken, c in enumerate(counts, start=1):
            running += c
            if running >= target:
                return taken, len(counts)
        return len(counts), len(counts)

    ranked = accent_tally.most_common(top) if chromatic > 0 else []
    accents = [
        {
            "hex": "#%02x%02x%02x" % rgb,
            "share": count / chromatic,
            "slides_for_90pc": _concentration(rgb)[0],
            "slides_any": _concentration(rgb)[1],
        }
        for rgb, count in ranked
    ]
    return {
        "neutral_share": neutral / total,
        "chromatic_share": chromatic / total,
        "accents": accents,
        # What share of chromatic pixels the printed rows actually account for.
        # Without this the table looks exhaustive when it is not.
        "listed_share": (
            sum(count for _, count in ranked) / chromatic if chromatic > 0 else 0.0
        ),
        "distinct_bins": len(accent_tally),
        "slides_sampled": slides_sampled,
    }


def _palette_has_data(palette_data) -> bool:
    """True when `palette_data` is a real reading from `palette()` (some
    pixels were sampled), false for the legacy empty-list sentinel some
    callers still pass for "no palette data available" and for a dict where
    literally zero pixels were sampled (no matching rendered slides on disk)."""
    if not palette_data:
        return False
    return bool(
        palette_data.get("neutral_share")
        or palette_data.get("chromatic_share")
        or palette_data.get("accents")
    )


def render_report(
    manifests: list[dict],
    palette_data: dict | list,
    reuse: dict | None = None,
) -> str:
    stats = word_stats(manifests)
    decks = stats["decks"]
    label = f"{decks} deck" + ("" if decks == 1 else "s")
    geometries = sorted({tuple(m["geometry_pt"]) for m in manifests})
    agreement = notes_span_agreement(manifests)

    reuse = reuse or {}

    lines = [
        "# Slide audit",
        "",
        f"Measured over **{label}**, {stats['slides']} slides.",
        "",
    ]
    if reuse:
        lines += [
            f"**Those {reuse['slides']} slides are not {reuse['slides']}",
            "independent observations.** Grouping every slide against every",
            f"other at {REUSE_THUMB[0]} x {REUSE_THUMB[1]} px (box-filtered, mean",
            f"absolute RGB difference < {REUSE_MAE_CUTOFF}) leaves",
            f"**{reuse['distinct']} distinct designs** — decks in this corpus reuse",
            "each other's slides. Every other figure in this file is a count of",
            "SLIDES, so a shape that recurs may be one slide carried forward rather",
            "than a habit. The per-deck column below gives the share of each deck",
            "that has a near-identical twin in another deck.",
            "",
        ]
        lines += [
            "| Deck | Slides | Geometry (pt) | Aspect | Twinned in another deck |",
            "|---|---|---|---|---|",
        ]
        for m in manifests:
            w, h = m["geometry_pt"]
            d = reuse["per_deck"].get(m["slug"], {"slides": 0, "twinned": 0})
            share = d["twinned"] / d["slides"] if d["slides"] else 0.0
            lines.append(
                f"| {m['title']} | {m['pages']} | {w:.0f} x {h:.0f} | {m['aspect']} "
                f"| {d['twinned']} ({share:.0%}) |"
            )
    else:
        lines += [
            "| Deck | Slides | Geometry (pt) | Aspect |",
            "|---|---|---|---|",
        ]
        for m in manifests:
            w, h = m["geometry_pt"]
            lines.append(
                f"| {m['title']} | {m['pages']} | {w:.0f} x {h:.0f} | {m['aspect']} |"
            )

    lines += [
        "",
        "## Words per slide",
        "",
        f"Measured over {label}. Slides with no text count as zero, not as missing —",
        "a full-bleed figure slide is a real measurement.",
        "",
        f"- median **{stats['median']:.1f}**",
        f"- interquartile range {stats['p25']:.1f} - {stats['p75']:.1f}",
        f"- maximum {stats['max']}",
        f"- share under four words: **{stats['share_under_four']:.0%}**",
        "",
    ] + word_count_caveat_lines(agreement, page_chrome_spans(manifests))

    hist = size_histogram(manifests)
    lines += [
        "",
        "## Words by font size",
        "",
        f"Measured over {label}: total words at each font size, across every",
        "slide. Slide copy, speaker narration, and figure-embedded text land at",
        "different sizes on a given deck, but the convention is per-deck, not",
        "universal — so this table is left unclassified rather than guessing a",
        "threshold from a single deck.",
        "",
    ]
    if hist:
        lines += ["| Size (pt) | Words |", "|---|---|"]
        lines += [f"| {size:.1f} | {words} |" for size, words in hist]
    else:
        lines.append("_No per-size span data recorded._")

    notes_counts = _notes_word_counts(manifests)
    lines += [
        "",
        "## Presenter notes",
        "",
    ]
    if notes_counts:
        lines += [
            f"Measured over {label}: {len(notes_counts)} of {stats['slides']} slides",
            "carry presenter notes.",
            "",
            f"- median **{statistics.median(notes_counts):.1f}** words",
            f"- maximum {max(notes_counts)} words",
        ]
    else:
        lines.append("_No presenter notes extracted._")

    lines += [
        "",
        "### Notes in the text layer",
        "",
    ]
    if agreement["slides_with_notes"] == 0:
        lines.append("_No presenter notes to compare against the text layer._")
    elif not agreement["size_breakdown"]:
        lines.append(
            f"_None of the {agreement['slides_with_notes']} notes-bearing "
            "slides' text matches any font size._"
        )
    else:
        lines.append(
            f"Measured over {label}: {agreement['slides_matching']} of "
            f"{agreement['slides_with_notes']} notes-bearing slides have "
            "text matching their note in the text layer, by size (a "
            f"containment match counts only when the contained text is "
            f"{NOTES_CONTAINMENT_MIN_WORDS}+ words; exact matches always count):"
        )
        lines.append("")
        lines += [
            f"- **{size:.1f}pt**: {count}"
            for size, count in agreement["size_breakdown"]
        ]

    lines += [
        "",
        "## Geometry",
        "",
        f"Measured over {label}: "
        + ", ".join(f"{w:.0f} x {h:.0f} pt" for w, h in geometries)
        + ". Archetypes take their dimensions from this table; a hard-coded",
        "aspect ratio is a defect.",
        "",
        "## Palette",
        "",
    ]
    if _palette_has_data(palette_data):
        lines += [
            f"Measured over {label}, by share of all sampled pixels. A pixel is",
            f"**neutral** when saturation < {NEUTRAL_SAT_CUTOFF} or its brightest",
            f"channel < {NEUTRAL_MAX_CHANNEL_CUTOFF}; otherwise **chromatic**.",
            f"Chromatic colours are binned to {ACCENT_BIN_LEVELS} levels per",
            "channel before tallying, so close accent hues group into one row",
            "instead of fragmenting into near-duplicates. Colours are reported,",
            "not named or interpreted.",
            "",
            f"- neutral: **{palette_data['neutral_share']:.1%}**",
            f"- chromatic: **{palette_data['chromatic_share']:.1%}**",
            "",
        ]
        accents = palette_data["accents"]
        if accents:
            listed = palette_data.get("listed_share", 0.0)
            bins = palette_data.get("distinct_bins", 0)
            sampled = palette_data.get("slides_sampled", 0)
            lines += [
                "### Chromatic colours, ranked",
                "",
                f"The table below divides that **{palette_data['chromatic_share']:.1%}**",
                "chromatic share up further, by colour — each row is a share of",
                "chromatic pixels only, not of the whole slide.",
                "",
                f"**These are the {len(accents)} largest of {bins} bins and cover",
                f"{listed:.1%} of chromatic pixels; the remaining",
                f"{1 - listed:.1%} is not listed.** The heading says *chromatic*,",
                "not *accent*, on purpose: a large bin is not necessarily a design",
                "choice. The last column is how many slides carry 90% of that",
                f"colour's pixels — against {sampled} sampled slides, a single-digit",
                "figure means the colour is one flat fill in a handful of images (a",
                "screenshot, say) rather than an ink spent across the deck.",
                "Reported, not interpreted.",
                "",
                "| Colour | Share of chromatic pixels | Slides carrying 90% of it |",
                "|---|---|---|",
            ]
            lines += [
                f"| `{a['hex']}` | {a['share']:.1%} | "
                f"{a['slides_for_90pc']} of {a['slides_any']} |"
                for a in accents
            ]
        else:
            lines.append("_No chromatic pixels sampled._")
    else:
        lines += [
            f"Most-used colours over {label}, by share of rendered pixels.",
            "",
            "_No rendered slides available._",
        ]

    return "\n".join(lines) + "\n"


def main() -> int:
    manifests = load_manifests()
    if not manifests:
        print(f"no manifests under {CORPUS_ROOT}; run build-slide-corpus.py first")
        return 1
    REPORT.write_text(
        render_report(manifests, palette(manifests), reuse_stats(manifests)),
        encoding="utf-8",
    )
    print(f"wrote {REPORT} over {len(manifests)} deck(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
