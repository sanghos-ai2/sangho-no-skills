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

The additional one, specific to this skill: `references/` is committed while the corpus lives
outside the repo entirely (see Corpus containment). A stranger who installs this plugin therefore receives the *derived characterization*
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

Run once; re-runnable when the canon changes. Writes only into `~/.cache/slides-like-sangho/corpus/`,
outside any git working tree (see Corpus containment).

1. **Ingest** — PDFs exported by Sangho from Keynote (Slides layout, Best quality, builds off) are
   copied into the corpus. **There is no AppleScript export step**; see Why extraction is not
   scripted.
2. **Rasterize** — `pdftoppm` produces per-slide PNGs at presentation resolution plus a downsampled
   reading set.
3. **Structure** — parse `Index/*.iwa` out of the `.key` zip for exact per-slide text, presenter
   notes, and the master-slide vocabulary. The files are modern snappy-framed IWA (verified:
   `Document.iwa` begins `00 50 29 00`; `Metadata/BuildVersionHistory.plist` reports Keynote T13.1),
   so `keynote-parser` applies. Media assets are readable directly from `Data/`.
4. **Narrative** — `watch-recording` over the Luminate practice recording, yielding a transcript
   aligned to slide boundaries.

Structure and pixels answer different questions, and the split is deliberate: parsed IWA text gives
**exact** counts where image analysis would only estimate, while the PDF gives composition, which no
parse can recover. Neither substitutes for the other.

### Why extraction is not scripted

Apple Keynote is not installed on the target machine, and the obvious probe says otherwise.
`osascript -e 'id of app "Keynote"'` answers `com.apple.Keynote`, but
`path to application "Keynote"` resolves to `/Applications/Keynote Creator Studio.app/`, whose
Info.plist declares `CFBundleIdentifier = com.apple.Keynote` and `CFBundleName = Keynote` under
`TeamIdentifier = JCRTNEU7GK` — not Apple's. A third-party app holds the name and bundle ID that
`tell application "Keynote"` resolves to.

An AppleScript export would therefore have succeeded against the wrong application, silently, and
produced a corpus with no error to attribute it to. Export stays a manual step performed by Sangho
in real Keynote. This is recorded rather than merely fixed, so it is not "simplified" back into an
AppleScript step by a later reader who re-runs the same misleading probe.

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
  archetypes/*.dc.html        runnable artboard templates — placeholder content only
tools/
  build-slide-corpus.py
  audit-slides.py
```

`references/` is interpretation; `archetypes/` is execution. Prose covers the one-off slide every
talk has; templates stop the recurring majority from drifting between decks.

### Corpus containment

The corpus lives at `~/.cache/slides-like-sangho/corpus/` — **outside every git working tree** —
not at `slides-like-sangho/corpus/` behind a `.gitignore` rule.

Nothing reads the corpus at runtime; only the derivation pass touches it. Co-locating it therefore
buys nothing, while costing a standing obligation to remember a gitignore rule forever. This repo
has already failed that obligation once, as its own `.gitignore` records: the thematic-analysis
copyright rule was *"missed when the skill was vendored on 2026-09-02, which left a dropped PDF
stageable and pushable."* There are also no active git hooks here, so `.gitignore` is the only
barrier — and it is defeated by `git add -f`, by a path-scoped `git commit -- <path>`, and by any
parallel session or subagent running a broad `git add`, all of which are recurring patterns in this
workspace. A 900 MB deck swept into a commit is not merely a leak; it is an unpushable repo.

Outside the working tree, none of those paths reach it. A `slides-like-sangho/corpus/` entry is
still added to `.gitignore` as a second layer, in case a future refactor moves the directory back.

### Committed artifacts carry no slide content

Archetype geometry is **measured, never assumed.** All four canon decks are **1920 × 1080 pt —
16:9**. Archetypes take slide dimensions from the audited canon (`tools/slide-audit.md`,
"Geometry"), and any hard-coded aspect ratio is a defect.

> **Correction, 2026-09-13.** This paragraph previously read *"All four canon decks export at
> 1024 × 768 pt — 4:3, not the 16:9 a modern deck is assumed to be."* That figure came from a
> Keynote **"Slides With Notes"** export: each PDF page was a 1024 × 768 sheet carrying a 16:9
> slide in its upper portion with the presenter note printed below, so every page-derived number
> described the page and not the slide. It was caught by an agent re-cropping the renders to read
> the handwriting and finding the slide's non-white bounding box byte-identical on all 55 pages of
> one deck at aspect 1.775. The corpus was re-exported cleanly and rebuilt. Recorded rather than
> silently overwritten, because the same paragraph calls a hard-coded aspect ratio a defect — and
> a spec that quietly changes a number teaches nothing about how the number went wrong. Other
> figures from that export moved a long way too: median words/slide 27 → 12, neutral pixel share
> 98.4% → 91.3%. **The 1024 × 768 values in the test fixtures are correct and deliberate** — they
> are synthetic, and their job is to prove no code hard-codes the canon's real geometry.

`archetypes/*.dc.html` **is** committed, which makes it the likeliest leak: an archetype traced from
a real slide can quietly embed that slide's text or a cropped screenshot.

Archetypes therefore ship with synthetic placeholder text and no real slide imagery. The committed
artifact encodes layout — grid, type scale, figure treatment, spacing — never content. The same rule
applies to `references/`: it describes and measures, and quotes real slide text only where a phrase
is necessary to name a pattern.

The canon is four publicly delivered talks, so this is defense in depth rather than the primary
concern — but it is the rule that keeps the committed half of the skill safe to distribute no matter
what the canon grows to include later.

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
  **Untestable on the current machine**, and worse than untestable: per Why extraction is not
  scripted, `tell application "Keynote"` here resolves to a third-party app. This path is gated on
  Apple Keynote resolving to an Apple-signed bundle, checked at runtime by comparing
  `codesign` TeamIdentifier rather than by bundle ID, and refuses to run otherwise. It ships
  unverified and labelled unverified.

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

**Luminate first, then the rest.** Sangho delivered PDFs for all four decks on 2026-09-13
(`~/Desktop/slides-like-sangho/`: Luminate 55 pp, Sensecape 32 pp, KAIST 126 pp, job talk 152 pp —
365 slides total), so the original cost argument for phasing is gone. The epistemic one is not: a
design language derived from a wrong first reading is confidently and unfalsifiably wrong, and
reading 365 slides before anyone checks the method spends the review gate's value. Waves stay.

1. **Derive from Luminate alone** (55 slides, the de facto template) and run the audit against it.
2. **Derive a first-pass design language** from that one deck — `references/` plus the draft
   never-list — and **present it to Sangho for correction**. This gate decides whether the approach
   reads as him at all. A wrong reading is cheap to discover here and expensive to discover after
   the 901 MB job talk.
3. **Extract the remaining three** (Sensecape, job talk, KAIST), re-run the audit, and update every
   measured number. Single-deck claims are revised or dropped, never silently kept.
4. **Author** — `SKILL.md`, archetypes, the three render paths.

One consequence to hold onto: **numbers derived from one deck are provisional.** Until step 3, every
figure in `references/` is labelled with the deck count behind it, so a one-deck measurement is never
mistaken for a corpus-wide one.

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
