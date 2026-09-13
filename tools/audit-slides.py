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
    for manifest in manifests:
        for slide in manifest["slides"]:
            path = root / manifest["slug"] / slide["image"]
            if not path.is_file():
                continue
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

    total = neutral + chromatic
    if total == 0:
        return {"neutral_share": 0.0, "chromatic_share": 0.0, "accents": []}
    # Explicit guard, not incidental: when nothing was classified chromatic,
    # accent_tally is empty anyway, but stating the zero-division avoidance
    # here (rather than relying on that coincidence) is what makes it a
    # guard rather than a lucky accident of the tallying logic above.
    accents = (
        [
            ("#%02x%02x%02x" % rgb, count / chromatic)
            for rgb, count in accent_tally.most_common(top)
        ]
        if chromatic > 0
        else []
    )
    return {
        "neutral_share": neutral / total,
        "chromatic_share": chromatic / total,
        "accents": accents,
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
    manifests: list[dict], palette_data: dict | list
) -> str:
    stats = word_stats(manifests)
    decks = stats["decks"]
    label = f"{decks} deck" + ("" if decks == 1 else "s")
    geometries = sorted({tuple(m["geometry_pt"]) for m in manifests})

    lines = [
        "# Slide audit",
        "",
        f"Measured over **{label}**, {stats['slides']} slides.",
        "",
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
        "**This is an upper bound, not slide copy.** These counts come from",
        "`page.get_text()`, which sums three unrelated things onto one slide:",
        "the actual slide copy, speaker narration Sangho sometimes renders onto",
        "the slide itself, and text baked inside embedded figures. See",
        "\"Words by font size\" below for the breakdown a threshold would need —",
        "this script does not pick one.",
    ]

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
            lines += [
                "### Accent colours",
                "",
                f"The table below divides that **{palette_data['chromatic_share']:.1%}**",
                "chromatic share up further, by colour — each row is a share of",
                "chromatic pixels only, not of the whole slide.",
                "",
                "| Colour | Share of chromatic pixels |",
                "|---|---|",
            ]
            lines += [f"| `{hexcode}` | {share:.1%} |" for hexcode, share in accents]
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
    REPORT.write_text(render_report(manifests, palette(manifests)), encoding="utf-8")
    print(f"wrote {REPORT} over {len(manifests)} deck(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
