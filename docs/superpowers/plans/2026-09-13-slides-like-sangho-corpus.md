# slides-like-sangho — Corpus & Derivation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the corpus pipeline and audit that turn Sangho's exported talk PDFs into a measured, first-pass description of his slide design language, reviewed and corrected by him.

**Architecture:** A canon registry resolves four decks by explicit path with byte-size verification. An ingest step rasterizes each PDF and extracts exact per-slide text with PyMuPDF, writing a per-deck manifest into a corpus outside any git tree. An audit reads those manifests and emits a report where every figure is labelled with the deck count behind it. An optional IWA pass enriches manifests with presenter notes and master-slide names. The plan ends at a human correction gate, not at code.

**Tech Stack:** Python 3.13, PyMuPDF (rasterize + text), Pillow (palette), pytest. Dependencies are declared inline via `uv run --with …` — this repo has no `pyproject.toml` or `requirements.txt`, matching `tools/build-corpus.py`.

**Spec:** `docs/superpowers/specs/2026-09-13-slides-like-sangho-design.md`

## Scope

**This is plan 1 of 2.** It covers spec phases 1–2 (extract, derive, correction gate). Phase 3–4 — authoring `SKILL.md`, `references/`, and `archetypes/` — is deliberately **not** planned here: those artifacts' content *is* the derived design language, so tasks for them today could only be placeholders, which this skill forbids. Plan 2 gets written once Task 5's gate passes.

## Global Constraints

- **Corpus root is `~/.cache/slides-like-sangho/corpus/`** — outside every git working tree. No corpus file is ever written inside the repo.
- **Canon decks are resolved by explicit path only.** Never by glob, filename search, or first match. Two distinct decks share the filename `uist2023 - sensecape (10-30-2023).key`.
- **`.key` resolution verifies byte size** and fails loudly on mismatch.
- **The job-talk directory name ends in a space**: `2024 job-talk ` — never strip or normalize path components.
- **Paths are passed as argument vectors**, never interpolated into shell strings. Canon paths contain spaces, apostrophes, `@`, and commas.
- **No AppleScript, and no `tell application "Keynote"`.** On this machine that name resolves to a third-party app signed `TeamIdentifier=JCRTNEU7GK` while declaring `CFBundleIdentifier=com.apple.Keynote`. See the spec's "Why extraction is not scripted".
- **Slide geometry is measured, never assumed.** All four canon decks are **1920 × 1080 pt (16:9)** — see `tools/slide-audit.md`, "Geometry". No hard-coded aspect ratio anywhere. (This line previously said 1024 × 768 pt / 4:3, which was the page size of a Keynote "Slides With Notes" export rather than the slide size; see the spec's "Committed artifacts carry no slide content" for the correction and how it was caught. The 1024 × 768 values in the test fixtures are synthetic and stay as they are.)
- **Every audited figure carries the deck count behind it.** A one-deck measurement must never render identically to a four-deck one.
- **Tests never read the real corpus.** It lives outside the repo and is not distributed; tests build synthetic fixtures.

---

### Task 1: Canon registry

**Files:**
- Create: `tools/slide_canon.py`
- Create: `slides-like-sangho/tests/test_slide_canon.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `Deck` (frozen dataclass: `slug: str`, `title: str`, `pdf_name: str`, `key_relpath: str`, `key_bytes: int`, `pages: int`, `wave: int`); `CANON: tuple[Deck, ...]`; `CanonError(RuntimeError)`; `by_slug(slug: str) -> Deck`; `resolve_pdf(deck: Deck, inbox: Path | None = None) -> Path`; `resolve_key(deck: Deck, root: Path | None = None, *, verify_size: bool = True) -> Path`; `CORPUS_ROOT: Path`; `PDF_INBOX: Path`; `KEY_ROOT: Path`.

Underscored module name, unlike the hyphenated CLI scripts beside it, because this one is imported.

- [ ] **Step 1: Write the failing test**

```python
# slides-like-sangho/tests/test_slide_canon.py
import pathlib
import pytest

from tools.slide_canon import (
    CANON, CanonError, by_slug, resolve_key, resolve_pdf,
)


def test_canon_has_four_decks_one_in_wave_one():
    assert len(CANON) == 4
    assert [d.slug for d in CANON if d.wave == 1] == ["luminate"]


def test_job_talk_key_relpath_keeps_its_trailing_space():
    # The real directory is named "2024 job-talk " — stripping it yields a
    # path that does not exist, and the failure reads as "deck not found".
    deck = by_slug("job-talk")
    assert deck.key_relpath.startswith("2024 job-talk /")


def test_resolve_key_rejects_a_size_mismatch(tmp_path):
    deck = by_slug("sensecape")
    target = tmp_path / deck.key_relpath
    target.parent.mkdir(parents=True)
    target.write_bytes(b"wrong deck, right filename")
    with pytest.raises(CanonError, match="expected"):
        resolve_key(deck, tmp_path)


def test_resolve_key_accepts_when_size_matches(tmp_path):
    deck = by_slug("sensecape")
    target = tmp_path / deck.key_relpath
    target.parent.mkdir(parents=True)
    target.write_bytes(b"x" * deck.key_bytes)
    assert resolve_key(deck, tmp_path) == target


def test_resolve_pdf_missing_names_the_deck(tmp_path):
    with pytest.raises(CanonError, match="luminate"):
        resolve_pdf(by_slug("luminate"), tmp_path)


def test_by_slug_rejects_unknown():
    with pytest.raises(CanonError):
        by_slug("nope")
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd /Users/sanghos/Github/sangho-no-skills && uv run --with pytest python -m pytest slides-like-sangho/tests/test_slide_canon.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'tools.slide_canon'`

- [ ] **Step 3: Write the implementation**

```python
#!/usr/bin/env python3
"""The canon of Sangho's talks, resolved by explicit path.

Never resolve a canon deck by glob or filename search. Two distinct decks share
the name "uist2023 - sensecape (10-30-2023).key": 271 MB (Oct 27) at the corpus
root and 681 MB (Oct 30) in conferences/. UIST'23 ran Oct 29 - Nov 1, so the
larger, later file is talk day. Byte size is therefore verified, and a mismatch
is a loud failure rather than a fallback.
"""
from __future__ import annotations

import dataclasses
import pathlib

CORPUS_ROOT = pathlib.Path.home() / ".cache" / "slides-like-sangho" / "corpus"
PDF_INBOX = pathlib.Path.home() / "Desktop" / "slides-like-sangho"
KEY_ROOT = pathlib.Path.home() / "Desktop" / "presentation" / "previous"


class CanonError(RuntimeError):
    """A canon deck could not be resolved, or resolved to the wrong bytes."""


@dataclasses.dataclass(frozen=True)
class Deck:
    slug: str
    title: str
    pdf_name: str
    key_relpath: str
    key_bytes: int
    pages: int
    wave: int


# NOTE: "2024 job-talk /" ends in a space. That is the real directory name.
CANON: tuple[Deck, ...] = (
    Deck(
        slug="luminate",
        title="Luminate @ CHI'24",
        pdf_name="chi2024-luminate-presentation.pdf",
        key_relpath="2024-05-14 Luminate @ CHI/chi2024-luminate-presentation.key",
        key_bytes=151209601,
        pages=55,
        wave=1,
    ),
    Deck(
        slug="sensecape",
        title="Sensecape @ UIST'23",
        pdf_name="uist2023 - sensecape (10-30-2023).pdf",
        key_relpath="conferences/uist2023 - sensecape (10-30-2023).key",
        key_bytes=681436109,
        pages=32,
        wave=2,
    ),
    Deck(
        slug="kaist",
        title="KAIST invited talk",
        pdf_name="kaist-talk-v2.pdf",
        key_relpath="2023-12-09 talk @ kaist - Dec, 2023/kaist-talk-v2.key",
        key_bytes=630342815,
        pages=126,
        wave=2,
    ),
    Deck(
        slug="job-talk",
        title="Job talk 2024",
        pdf_name="job-talk-uninhabited-space-of-intelligence.pdf",
        key_relpath="2024 job-talk /job-talk-uninhabited-space-of-intelligence.key",
        key_bytes=901159834,
        pages=152,
        wave=2,
    ),
)


def by_slug(slug: str) -> Deck:
    for deck in CANON:
        if deck.slug == slug:
            return deck
    known = ", ".join(d.slug for d in CANON)
    raise CanonError(f"unknown deck {slug!r}; canon is: {known}")


def resolve_pdf(deck: Deck, inbox: pathlib.Path | None = None) -> pathlib.Path:
    path = (inbox or PDF_INBOX) / deck.pdf_name
    if not path.is_file():
        raise CanonError(
            f"{deck.slug}: no exported PDF at {path}. Export from Keynote with "
            f"Layout=Slides, Image Quality=Best, builds off."
        )
    return path


def resolve_key(
    deck: Deck,
    root: pathlib.Path | None = None,
    *,
    verify_size: bool = True,
) -> pathlib.Path:
    path = (root or KEY_ROOT) / deck.key_relpath
    if not path.is_file():
        raise CanonError(f"{deck.slug}: no .key at {path}")
    if verify_size:
        actual = path.stat().st_size
        if actual != deck.key_bytes:
            raise CanonError(
                f"{deck.slug}: expected {deck.key_bytes} bytes at {path}, found "
                f"{actual}. Refusing: filenames are not unique in this corpus."
            )
    return path
```

- [ ] **Step 4: Add the package marker so `tools.slide_canon` imports**

```bash
cd /Users/sanghos/Github/sangho-no-skills
touch tools/__init__.py
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `cd /Users/sanghos/Github/sangho-no-skills && uv run --with pytest python -m pytest slides-like-sangho/tests/test_slide_canon.py -v`
Expected: PASS, 6 tests

- [ ] **Step 6: Verify against the real filesystem**

Run:
```bash
cd /Users/sanghos/Github/sangho-no-skills
uv run python -c "
from tools.slide_canon import CANON, resolve_key, resolve_pdf
for d in CANON:
    print(d.slug, resolve_pdf(d).name, resolve_key(d).stat().st_size)
"
```
Expected: four lines, no exception. A `CanonError` here means a byte size in `CANON` is wrong — fix the constant, do not disable the check.

- [ ] **Step 7: Commit**

```bash
cd /Users/sanghos/Github/sangho-no-skills
git add tools/__init__.py tools/slide_canon.py slides-like-sangho/tests/test_slide_canon.py
git commit -m "feat(slides): canon registry with explicit paths and size verification"
```

---

### Task 2: PDF ingest — rasterize, geometry, per-slide text

**Files:**
- Create: `tools/build-slide-corpus.py`
- Create: `slides-like-sangho/tests/test_build_slide_corpus.py`

**Interfaces:**
- Consumes: `tools.slide_canon` — `Deck`, `CANON`, `CanonError`, `by_slug`, `resolve_pdf`, `CORPUS_ROOT`.
- Produces: `ingest_deck(deck: Deck, *, dpi: int = 150, inbox: Path | None = None, corpus_root: Path | None = None, allow_page_drift: bool = False) -> dict` and the on-disk manifest contract below.

Manifest written to `<corpus_root>/<slug>/manifest.json`:

```json
{
  "slug": "luminate",
  "title": "Luminate @ CHI'24",
  "pages": 55,
  "geometry_pt": [1024.0, 768.0],
  "aspect": 1.3333,
  "dpi": 150,
  "slides": [{"index": 1, "image": "slides/01.png", "text": "..."}]
}
```

The module is imported by its hyphenated filename via `importlib`, which `tools/build-citation-index.py` already does in this repo; the test below shows the exact loader.

- [ ] **Step 1: Write the failing test**

```python
# slides-like-sangho/tests/test_build_slide_corpus.py
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd /Users/sanghos/Github/sangho-no-skills && uv run --with pytest --with pymupdf python -m pytest slides-like-sangho/tests/test_build_slide_corpus.py -v`
Expected: FAIL — `FileNotFoundError` on `tools/build-slide-corpus.py`

- [ ] **Step 3: Write the implementation**

```python
#!/usr/bin/env python3
"""Ingest Sangho's exported talk PDFs into the slide corpus.

    uv run --with pymupdf python tools/build-slide-corpus.py --wave 1
    uv run --with pymupdf python tools/build-slide-corpus.py --all

There is no export step. Apple Keynote is not installed on this machine, and
`tell application "Keynote"` resolves to a third-party app that declares Apple's
bundle identifier, so a scripted export would have driven the wrong application
without erroring. PDFs are exported by hand and dropped in PDF_INBOX.

Writes only into CORPUS_ROOT, which is outside every git working tree.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import fitz  # PyMuPDF

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from tools.slide_canon import (  # noqa: E402
    CANON,
    CORPUS_ROOT,
    CanonError,
    Deck,
    resolve_pdf,
)


def ingest_deck(
    deck: Deck,
    *,
    dpi: int = 150,
    inbox: pathlib.Path | None = None,
    corpus_root: pathlib.Path | None = None,
    allow_page_drift: bool = False,
) -> dict:
    pdf_path = resolve_pdf(deck, inbox)
    out_dir = (corpus_root or CORPUS_ROOT) / deck.slug
    slides_dir = out_dir / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    try:
        if doc.page_count != deck.pages and not allow_page_drift:
            raise CanonError(
                f"{deck.slug}: expected {deck.pages} pages, found {doc.page_count}. "
                f"A build-stages export changes what 'a slide' means for every "
                f"measured figure. Re-export with builds off, or pass "
                f"--allow-page-drift and update Deck.pages."
            )

        rect = doc[0].rect
        pad = len(str(doc.page_count))
        slides = []
        for index, page in enumerate(doc, start=1):
            name = f"{index:0{pad}d}.png"
            page.get_pixmap(dpi=dpi).save(slides_dir / name)
            slides.append(
                {
                    "index": index,
                    "image": f"slides/{name}",
                    "text": page.get_text().strip(),
                }
            )

        manifest = {
            "slug": deck.slug,
            "title": deck.title,
            "pages": doc.page_count,
            "geometry_pt": [rect.width, rect.height],
            "aspect": round(rect.width / rect.height, 4),
            "dpi": dpi,
            "slides": slides,
        }
    finally:
        doc.close()

    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--wave", type=int, help="ingest one phasing wave (1 or 2)")
    group.add_argument("--all", action="store_true", help="ingest every canon deck")
    parser.add_argument("--dpi", type=int, default=150)
    parser.add_argument("--allow-page-drift", action="store_true")
    args = parser.parse_args(argv)

    decks = CANON if args.all else [d for d in CANON if d.wave == args.wave]
    if not decks:
        parser.error(f"no decks in wave {args.wave}")

    for deck in decks:
        manifest = ingest_deck(
            deck, dpi=args.dpi, allow_page_drift=args.allow_page_drift
        )
        print(
            f"{deck.slug}: {manifest['pages']} slides, "
            f"{manifest['geometry_pt'][0]:.0f}x{manifest['geometry_pt'][1]:.0f} pt "
            f"(aspect {manifest['aspect']})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd /Users/sanghos/Github/sangho-no-skills && uv run --with pytest --with pymupdf python -m pytest slides-like-sangho/tests/test_build_slide_corpus.py -v`
Expected: PASS, 6 tests

- [ ] **Step 5: Ingest wave 1 for real**

Run: `cd /Users/sanghos/Github/sangho-no-skills && uv run --with pymupdf python tools/build-slide-corpus.py --wave 1`
Expected: `luminate: 55 slides, 1920x1080 pt (aspect 1.7778)`  
(This step originally recorded `1024x768 pt (aspect 1.3333)`, which was the page size of a Keynote "Slides With Notes" export, not the slide size. See the spec's "Committed artifacts carry no slide content".)

- [ ] **Step 6: Confirm nothing landed in the repo**

Run: `cd /Users/sanghos/Github/sangho-no-skills && git status --porcelain && ls ~/.cache/slides-like-sangho/corpus/luminate/slides | head -3`
Expected: `git status` shows only the two new source files (no PNGs, no manifest); the corpus listing shows `01.png 02.png 03.png`.

- [ ] **Step 7: Commit**

```bash
cd /Users/sanghos/Github/sangho-no-skills
git add tools/build-slide-corpus.py slides-like-sangho/tests/test_build_slide_corpus.py
git commit -m "feat(slides): ingest exported PDFs into corpus with measured geometry"
```

---

### Task 3: Audit — measure the canon, label every figure with its deck count

**Files:**
- Create: `tools/audit-slides.py`
- Create: `slides-like-sangho/tests/test_audit_slides.py`
- Create (generated, committed): `tools/slide-audit.md`

**Interfaces:**
- Consumes: manifests written by Task 2 (`ingest_deck`'s contract), `tools.slide_canon.CORPUS_ROOT`.
- Produces: `load_manifests(corpus_root: Path | None = None) -> list[dict]`; `word_stats(manifests: list[dict]) -> dict` with keys `decks`, `slides`, `median`, `p25`, `p75`, `max`, `share_under_four`; `palette(manifests, corpus_root, top: int = 8) -> list[tuple[str, float]]`; `render_report(manifests, palette_rows) -> str`.

`tools/slide-audit.md` is committed: it is measurement of publicly delivered talks, and it is what `references/` will quote. Slide images are not.

- [ ] **Step 1: Write the failing test**

```python
# slides-like-sangho/tests/test_audit_slides.py
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd /Users/sanghos/Github/sangho-no-skills && uv run --with pytest --with pillow python -m pytest slides-like-sangho/tests/test_audit_slides.py -v`
Expected: FAIL — `FileNotFoundError` on `tools/audit-slides.py`

- [ ] **Step 3: Write the implementation**

```python
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


def palette(
    manifests: list[dict],
    corpus_root: pathlib.Path | None = None,
    top: int = 8,
) -> list[tuple[str, float]]:
    """Most-used colours across rendered slides, as (hex, share) pairs."""
    from PIL import Image

    root = corpus_root or CORPUS_ROOT
    tally: collections.Counter = collections.Counter()
    for manifest in manifests:
        for slide in manifest["slides"]:
            path = root / manifest["slug"] / slide["image"]
            if not path.is_file():
                continue
            with Image.open(path) as img:
                small = img.convert("RGB").resize((64, 48))
                for count, rgb in small.getcolors(maxcolors=64 * 48):
                    tally[rgb] += count
    total = sum(tally.values()) or 1
    return [
        ("#%02x%02x%02x" % rgb, count / total)
        for rgb, count in tally.most_common(top)
    ]


def render_report(
    manifests: list[dict], palette_rows: list[tuple[str, float]]
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
        "## Geometry",
        "",
        f"Measured over {label}: "
        + ", ".join(f"{w:.0f} x {h:.0f} pt" for w, h in geometries)
        + ". Archetypes take their dimensions from this table; a hard-coded",
        "aspect ratio is a defect.",
        "",
        "## Palette",
        "",
        f"Most-used colours over {label}, by share of rendered pixels.",
        "",
    ]
    if palette_rows:
        lines += ["| Colour | Share |", "|---|---|"]
        lines += [f"| `{hexcode}` | {share:.1%} |" for hexcode, share in palette_rows]
    else:
        lines.append("_No rendered slides available._")

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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd /Users/sanghos/Github/sangho-no-skills && uv run --with pytest --with pillow python -m pytest slides-like-sangho/tests/test_audit_slides.py -v`
Expected: PASS, 5 tests

- [ ] **Step 5: Run the audit against real wave-1 data**

Run: `cd /Users/sanghos/Github/sangho-no-skills && uv run --with pillow python tools/audit-slides.py && cat tools/slide-audit.md`
Expected: a report saying "Measured over **1 deck**, 55 slides", geometry `1920 x 1080 pt`, and a palette table.  
(Same correction as Step 5 above; the fixture-driven tests in the previous step keep 1024 × 768 deliberately.)

- [ ] **Step 6: Commit**

```bash
cd /Users/sanghos/Github/sangho-no-skills
git add tools/audit-slides.py tools/slide-audit.md slides-like-sangho/tests/test_audit_slides.py
git commit -m "feat(slides): audit corpus, labelling every figure with its deck count"
```

---

### Task 4: IWA enrichment — presenter notes and master vocabulary

**Files:**
- Create: `tools/enrich-from-keynote.py`
- Create: `slides-like-sangho/tests/test_enrich_from_keynote.py`
- Modify: manifests in the corpus (adds optional `notes` per slide, plus top-level `masters`)

**Interfaces:**
- Consumes: `tools.slide_canon` — `Deck`, `by_slug`, `resolve_key`; manifests from Task 2.
- Produces: `enrich_manifest(deck, *, key_root=None, corpus_root=None) -> dict`, adding `slides[].notes: str | None` and `masters: list[str]`. Returns the manifest unchanged with `masters: []` when extraction is unavailable.

**This task is additive and allowed to fail.** Tasks 1–3 give words-per-slide, geometry, and palette with no IWA dependency at all. Notes and master names are the only things the PDF cannot carry. If `keynote-parser` cannot read these files, record that and move on — do not block the gate.

Its first step is a verification, not a test, because writing code against an unverified third-party API would be inventing an interface.

- [ ] **Step 1: Verify what `keynote-parser` actually yields**

Run:
```bash
cd /Users/sanghos/Github/sangho-no-skills
uv run --with keynote-parser python -c "
import pathlib, tools.slide_canon as c
deck = c.by_slug('luminate')
print('key:', c.resolve_key(deck))
import keynote_parser
print('module:', keynote_parser.__file__)
print('exports:', [n for n in dir(keynote_parser) if not n.startswith('_')])
"
uv run --with keynote-parser keynote-parser --help
```
Expected: the module imports and the CLI prints usage. Record the actual API surface in the commit message.

If the import fails, stop, write `slides-like-sangho/references/_iwa-unavailable.md` recording the exact error, and skip to Task 5 — notes and masters are then simply absent from the first pass, and `references/` says so.

- [ ] **Step 2: Unpack one real deck and inspect the shape**

Run:
```bash
cd /Users/sanghos/Github/sangho-no-skills
mkdir -p /tmp/iwa-probe
uv run --with keynote-parser keynote-parser unpack \
  "$HOME/Desktop/presentation/previous/2024-05-14 Luminate @ CHI/chi2024-luminate-presentation.key" \
  /tmp/iwa-probe/luminate
find /tmp/iwa-probe/luminate -maxdepth 2 | head -40
grep -ril "note" /tmp/iwa-probe/luminate/Index | head
```
Expected: an unpacked tree under `/tmp/iwa-probe/luminate` with `Index/` entries. Note which file holds presenter notes and which hold `TemplateSlide` names — the Luminate deck has 12 `TemplateSlide-*` entries.

- [ ] **Step 3: Write the failing test, against the shape you just observed**

```python
# slides-like-sangho/tests/test_enrich_from_keynote.py
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
```

- [ ] **Step 4: Run the test to verify it fails**

Run: `cd /Users/sanghos/Github/sangho-no-skills && uv run --with pytest python -m pytest slides-like-sangho/tests/test_enrich_from_keynote.py -v`
Expected: FAIL — `FileNotFoundError` on `tools/enrich-from-keynote.py`

- [ ] **Step 5: Implement `merge_extraction` plus the extractor you verified in Step 2**

`merge_extraction` is pure and fully specified by the tests:

```python
def merge_extraction(
    manifest: dict,
    notes_by_index: dict[int, str | None],
    masters: list[str],
) -> dict:
    manifest["masters"] = list(masters)
    for slide in manifest["slides"]:
        if slide["index"] in notes_by_index:
            slide["notes"] = notes_by_index[slide["index"]]
    return manifest
```

Then write `extract(key_path) -> tuple[dict[int, str | None], list[str]]` against the structure observed in Step 2, and a `main()` that resolves each deck with `resolve_key`, calls `extract`, merges, and rewrites `manifest.json`. Wrap `extract` in `try/except Exception` and return `({}, [])` on failure, logging the exception — the merge tests above pin that this degrades to a usable manifest.

- [ ] **Step 6: Run the tests to verify they pass**

Run: `cd /Users/sanghos/Github/sangho-no-skills && uv run --with pytest python -m pytest slides-like-sangho/tests/ -v`
Expected: PASS, all tests from Tasks 1–4

- [ ] **Step 7: Enrich wave 1 and re-audit**

Run:
```bash
cd /Users/sanghos/Github/sangho-no-skills
uv run --with keynote-parser python tools/enrich-from-keynote.py --wave 1
uv run --with pillow python tools/audit-slides.py
```
Expected: the Luminate manifest gains `masters` and per-slide `notes`; the audit still runs.

- [ ] **Step 8: Commit**

```bash
cd /Users/sanghos/Github/sangho-no-skills
git add tools/enrich-from-keynote.py slides-like-sangho/tests/test_enrich_from_keynote.py tools/slide-audit.md
git commit -m "feat(slides): enrich manifests with presenter notes and master vocabulary"
```

---

### Task 5: First-pass design language and the correction gate

**Files:**
- Create: `slides-like-sangho/references/visual-language.md`
- Create: `slides-like-sangho/references/archetypes.md`
- Create: `slides-like-sangho/references/narrative.md`
- Create: `slides-like-sangho/references/never-list.md`

**Interfaces:**
- Consumes: `tools/slide-audit.md`, the Luminate manifest, and the 55 rendered slide PNGs.
- Produces: the four reference documents, which Plan 2's `SKILL.md` will read.

This task is not test-driven. Its deliverable is a reading of the corpus, and its acceptance criterion is Sangho's correction — which is the point of the gate, not a gap in the plan.

- [ ] **Step 1: Read all 55 Luminate slides**

Read every PNG in `~/.cache/slides-like-sangho/corpus/luminate/slides/` in order. Do not sample. The archetype vocabulary is a claim about what recurs, and a sample cannot support it.

- [ ] **Step 2: Draft `visual-language.md`, quoting only audited numbers**

Every quantitative claim cites `tools/slide-audit.md` and carries its deck count. Qualitative claims — figure treatment, title placement, where colour is spent — are marked as observations from one deck. Forbidden: any number not in the audit, and any claim stated corpus-wide while the corpus is one deck.

- [ ] **Step 3: Draft `archetypes.md` as a frequency table**

One entry per recurring slide shape: name, what it is for, how many of the 55 slides use it, and two example slide indices. An archetype appearing once is not an archetype — list those under a "one-offs" heading instead of promoting them.

- [ ] **Step 4: Draft `narrative.md` from slide order and presenter notes**

Where Task 4 succeeded, use notes density per slide as the "how much lives in his mouth" signal. Where it failed, say so in the document rather than inferring narrative from slide text alone.

- [ ] **Step 5: Draft `never-list.md`**

Seed with Sangho's own entry, verbatim and attributed:

> Never use the design skill's default aesthetic.

Then add *candidate* entries inferred from absence — patterns conventional in talks that appear zero times in 55 slides (bullet lists as body, stock iconography, a title on every slide, gradients, drop shadows). Mark every inferred entry **UNCONFIRMED**. An inferred never is a hypothesis about taste; only Sangho can promote it.

- [ ] **Step 6: Present all four documents to Sangho for correction**

Lead with what is most likely wrong, not with what is most impressive. Explicitly ask about: the archetype names, any UNCONFIRMED never-list entry, and anything asserted from one deck that he expects the other three to contradict.

- [ ] **Step 7: Apply corrections and commit**

```bash
cd /Users/sanghos/Github/sangho-no-skills
git add slides-like-sangho/references/
git commit -m "docs(slides): first-pass design language from Luminate, corrected by Sangho"
```

- [ ] **Step 8: Gate decision**

If the first pass reads as him, ingest wave 2 (`--all`), re-run the audit, and revise every figure and claim to its four-deck value — single-deck claims are revised or dropped, never silently kept. Then write Plan 2 for the skill itself.

If it does not, the method is wrong and stopping here has cost 55 slides instead of 365. Reconsider before extracting further.

---

## Self-Review

**Spec coverage.** Canon and its resolution rules → Task 1. PDF ingest and rasterize → Task 2. Structure from IWA → Task 4. Measurement → Task 3. Corpus containment → Global Constraints plus Task 2 Step 6. Measured geometry → Task 2 and Task 3. Never-list as a corrected draft → Task 5 Step 5. Luminate-first phasing and the gate → Task 5 Step 8. Narrative from `watch-recording` → **deferred**: the transcript pass is not needed to decide whether the method works, and it belongs with the four-deck wave; Plan 2 carries it. Render paths, `SKILL.md`, archetype templates → Plan 2, as stated under Scope.

**Placeholder scan.** Task 4 Step 5 is the only step that does not ship complete code, and deliberately: `keynote-parser`'s API is verified in Steps 1–2 before anything is written against it. Its pure function, `merge_extraction`, is given in full and fully pinned by tests.

**Type consistency.** `Deck` fields are used identically in Tasks 1, 2, and 4. The manifest contract declared in Task 2 is what Tasks 3 and 4 read. `load_manifests`, `word_stats`, `palette`, and `render_report` keep one signature across their definition and both call sites.
