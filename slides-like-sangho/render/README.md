# Render paths

Four of them. Pick one **after** the storyboard is approved, and say which you picked and why
before you start — the choice determines what Sangho can do with the deck afterwards, which is
usually the thing he actually cares about.

| Path | Pick it when | He can then |
|---|---|---|
| [Claude Design canvas](canvas.md) *(needs the bundled `design` skill)* | it is available AND he wants click-to-edit | see every slide on one pan/zoom canvas, click any element and edit it, export PNG/PDF |
| [PPTX → Google Slides](pptx-google-slides.md) | he wants to edit in a browser, or to hand the deck to a co-author | edit natively in Google Slides, present from it, share a link |
| [Standalone HTML](html.md) **(the default)** | published as a Claude artifact — his stated preference, and the only path here with a generator | present from the browser, speaker notes on `N`, print to PDF, share a link; you can screenshot-verify it |
| [Keynote via AppleScript](keynote.md) | he asks for Keynote — **and see the gate; it does not work on this machine** | finish by hand in Keynote |

**Every path consumes `deck.json`.** `render/html/build_deck_json.py` merges his storyboard edits
over the payload once and emits a renderer-neutral file — one entry per slide with `words`,
`header`, `figure`, `table`, `tableTreat`, `ground`, `title`, `note`, plus the resolved `tables`
registry. A new output path is a new consumer of that file. Never write a second merge: the
precedence rule (a saved edit beats an authored default) would then exist in two places and drift.

Everything renders at **1920 × 1080 (16:9)**, matching the corpus. Type sizes from
`references/visual-language.md` are in points at that size, so at 1920 × 1080 a point is a pixel
and the numbers transfer directly.

## What every path owes the storyboard

- **One artboard / slide / file per storyboard beat**, in beat order, including build steps. A
  build of eleven slides is eleven slides, not one slide with eleven animations. More than half of
  every deck in the corpus is one picture being edited — that *is* the slide count.
- **The speaker note travels with the slide** wherever the format has a notes field. Canvas and
  HTML do not; put those notes in `notes.md` beside the output, numbered to the slides.
- **Nothing is invented at render time.** If a beat's visual was flagged as a guess in the
  storyboard and Sangho did not resolve it, render the flag — a visible `[GUESS: …]` block on the
  slide — rather than quietly deciding. The same rule the sibling skill's placeholders follow.

## Verify before handing over

Screenshot the render and look at it. Two failures are common enough to check for by name:

- **Type too small.** Measure one Display and one Title against 112 pt / 84 pt. This is the failure
  mode a brand pack causes silently (`brand/README.md`, Finding 1).
- **A slide that went blank — but check the storyboard before calling it.** On a dark ground the
  usual cause is a black-ink asset that was never restroked; on a light ground, white-on-white.
  **An all-black slide with nothing on it is not a failure if the beat is a blackout** — that is the
  correct output at any polarity (`brand/polarity.md` §3, confirmed by Sangho). The error worth
  flagging is the inverse: **a blackout beat that came out light.**

The HTML path is the one you can verify most cheaply — if you need certainty about a tricky figure,
render it there first even when the deliverable is something else.
