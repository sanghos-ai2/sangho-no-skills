# slides-like-sangho — design

**Status:** approved design, pending implementation plan
**Date:** 2026-09-13

## Problem

`write-like-sangho` captures Sangho's *prose* taste by grounding a model in a corpus of their
published sections plus a measured blocklist of LLM tells. There is no equivalent for slides.
Asking a model for "a CHI talk" today produces a deck in the model's default register — generic
type, templated layouts, decorative icons — which is precisely the thing Sangho would never ship.

The goal is the visual sibling of that skill: a deck that a colleague who has seen Sangho talk
would not suspect a model built.

## Non-goals

- Not a general-purpose presentation generator. It makes decks in one person's taste.
- Not a Keynote automation product. The Keynote path produces a scaffold, not a finished deck.
- Not a replacement for the design skill. It *constrains* that skill rather than competing with it.

## The gate: `.i-am-sangho`

Same gate as `write-like-sangho`, for the same reason and one additional one.

The reason it shares: the skill imitates a real, named person, and this repo is public
(`github.com/sanghos-ai2/sangho-no-skills`). Before doing anything, read `<repo-root>/.i-am-sangho`.
If absent, say the skill is gated, explain that `touch .i-am-sangho` opts a repo in, and help with
the slide task in a normal unimitated register.

The additional one, specific to this skill: `references/` is committed while `corpus/` is
gitignored. A stranger who installs this plugin therefore receives the *derived characterization*
of Sangho's visual language even though they receive none of the source slides — so the skill would
work for them. The gate, not the gitignore, is what prevents that.

## Canon

Four as-presented talks. Chosen with Sangho, 2026-09-13.

| Talk | File (under `~/Desktop/presentation/previous/`) | Size | Why |
|---|---|---|---|
| Luminate @ CHI'24 | `2024-05-14 Luminate @ CHI/chi2024-luminate-presentation.key` | 151 MB | de facto template; later talks start from it |
| Sensecape @ UIST'23 | `conferences/uist2023 - sensecape (10-30-2023).key` | 681 MB | flagship conference talk, talk-day version |
| Job talk 2024 | `2024 job-talk /job-talk-uninhabited-space-of-intelligence.key` (note trailing space in dir name) | 901 MB | long-form arc |
| KAIST invited talk | `2023-12-09 talk @ kaist - Dec, 2023/kaist-talk-v2.key` | 630 MB | different genre, different room |

Narrative source: `2024-05-02 Luminate CHI Practice Talk @ DGP/luminate-presentation-video.mp4`
(115 MB) — a recording of a canon talk, processed with the `watch-recording` skill.

Explicitly excluded, with reasons, so they are not re-proposed later:

- `2026-09-11-atlas-CHI27/chi2024-luminate-presentation.key` — work in progress, not representative.
- `KnowledgeTrail.key` — excluded by Sangho.
- `uist2023 - sensecape @ msr (08-09-2023).pdf` — a pre-existing PDF export, and therefore tempting
  to use because it costs nothing to extract, but it is an earlier talk than the conference version.
- All `v1` / earlier-dated siblings of canon decks — drafts already revised past.

### Extraction rule: as-presented beats latest-modified, and filename means nothing

Two distinct decks share the name `uist2023 - sensecape (10-30-2023).key`: 271 MB (Oct 27) at the
corpus root and 681 MB (Oct 30) in `conferences/`. UIST'23 ran Oct 29 – Nov 1, so the Oct 30 file is
talk day. Selecting by filename, or by first match, silently yields the wrong deck.

The tool resolves canon by **explicit path**, never by glob or name search, and verifies the
expected byte size before extracting. A mismatch is a loud failure, not a fallback.

Two path hazards in this corpus, both of which fail silently rather than loudly:

- The job-talk directory is named `2024 job-talk ` — with a **trailing space**. Any code that
  strips or normalizes path components resolves it to a directory that does not exist.
- Canon paths contain spaces, apostrophes, `@`, and commas throughout. Paths are passed as argument
  vectors, never interpolated into shell strings.

## Architecture

### Corpus pipeline (`tools/build-slide-corpus.py`)

Run once; re-runnable when the canon changes. Writes only into `slides-like-sangho/corpus/`.

1. **Export** — AppleScript drives Keynote per deck: slides to PDF, presenter notes to per-slide
   plain text, build order where the format exposes it.
2. **Rasterize** — `pdftoppm` produces per-slide PNGs at presentation resolution plus a downsampled
   reading set.
3. **Theme internals** — read fonts, master-slide names, and color swatches out of the `.key`
   bundle where they are reachable without parsing IWA protobuf.
4. **Narrative** — `watch-recording` over the Luminate practice recording, yielding a transcript
   aligned to slide boundaries.

Cost is real: ~2.4 GB of Keynote, and Keynote export on the 901 MB job talk is measured in minutes.
The pipeline is therefore resumable per deck and skips completed stages.

### Measurement (`tools/audit-slides.py`)

Every claim in `references/` quotes a measured number, following `audit-voice.py`'s precedent. When
the canon changes, the audit is re-run and the numbers updated rather than re-guessed.

Measured: words per slide (distribution, not mean); share of slides with a title; share full-bleed
figure vs. framed; palette histogram over rendered pixels; type sizes in use; notes-words per slide
(the "how much lives in his mouth" proxy); slides per minute of talk time; figure-to-text ratio.

### What ships

```
slides-like-sangho/
  SKILL.md                    trigger, gate, workflow, never-list
  references/
    visual-language.md        type scale, palette, density — measured
    archetypes.md             recurring slide shapes, one entry each
    narrative.md              openings, tension, landing a contribution, closing
    build-rhythm.md           reveal patterns, carried into storyboards as notes
  archetypes/*.dc.html        runnable artboard templates
  corpus/                     GITIGNORED — slides, notes, transcripts
tools/
  build-slide-corpus.py
  audit-slides.py
```

`references/` is interpretation; `archetypes/` is execution. Prose covers the one-off slide every
talk has; templates stop the recurring majority from drifting between decks.

`corpus/` is added to `.gitignore` alongside the existing `write-like-sangho/examples/` entry, with
the same rationale comment.

## Runtime workflow

1. **Mode detect.** A source document (paper, spec, draft) means draft directly from it. A topic
   alone means a short interview first: audience, the one sentence they must remember, what is
   demoable, time budget.
2. **Arc.** Select a narrative shape from `references/narrative.md`, sized to the time budget.
3. **Storyboard.** One block per beat — message, archetype, visual, build steps, speaker note —
   with guesses flagged. **This is the review gate.** The arc is corrected here, before pixels.
4. **Render.** Default is `.dc.html` artboards composed from `archetypes/`. On request: reveal.js,
   or Keynote.
5. **Sweep.** Check the deck against the never-list before handing it over, mirroring the prose
   skill's blocklist sweep.

## Render paths

All three render from the same storyboard and token set, so they cannot drift apart.

- **Claude Design canvas** (default) — multi-artboard `.dc.html`, refined visually, exported PNG/PDF.
- **reveal.js** — a web deck, and the path that can be screenshot-verified with Playwright.
- **Keynote** (AppleScript) — produces a scaffold to finish by hand. AppleScript's control of
  Keynote layout is coarse; the skill says so rather than over-promising, because a scaffold
  presented as a finished deck wastes more time than no deck.

## The never-list

The counterpart to `write-like-sangho`'s blocklist, and the part expected to do the most work.

**Seeded by Sangho, 2026-09-13:**

> Never use the design skill's default aesthetic.

This is load-bearing rather than a stylistic note. It means archetypes are **fully self-styled** —
type, spacing, and color are set explicitly and never inherited from the canvas's defaults. A
default leaking through is a failure condition checked in step 5, not a neutral starting point.

**The rest is derived, then corrected.** Taste is not introspectable on demand, but absence is
measurable against a baseline: if zero of ~300 canon slides carry a bullet list, a stock icon row,
or a title on every slide, that is an inferred "never" worth putting in front of Sangho to accept or
reject. The never-list therefore ships as a draft the corpus writes and Sangho edits, and it grows
as decks are made and rejected.

## Phasing

The corpus pass precedes skill authoring. Nothing truthful can be written about Sangho's visual
language before the slides have been looked at, so:

1. **Extraction** — build the corpus, run the audit.
2. **Derivation** — write `references/` and the draft never-list; **present to Sangho for
   correction**. This gate decides whether the skill feels like him.
3. **Authoring** — `SKILL.md`, archetypes, the three render paths.

## Risks

- **Keynote AppleScript export may not expose build order** on newer file formats. Build rhythm then
  degrades to what is visible across slide images plus presenter-note cues. Acceptable: the layer
  lands as storyboard notes regardless, since the canvas is static.
- **The design skill is harness-provided**, so its artboard contract is observed rather than read
  from source. The `.dc.html` archetypes are validated by rendering, not by reading a schema.
- **A four-deck canon may under-represent patterns** used often but not in these four. Mitigated by
  the audit being re-runnable: adding a deck is a re-run, not a rewrite.
- **Derived taste can be wrong in ways that look right.** Mitigated by the step-2 correction gate
  and by every reference claim quoting a number that can be checked against the corpus.
