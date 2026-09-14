# Render paths

Four of them. Pick one **after** the storyboard is approved, and say which you picked and why
before you start — the choice determines what Sangho can do with the deck afterwards, which is
usually the thing he actually cares about.

| Path | Pick it when | He can then |
|---|---|---|
| [Claude Design canvas](canvas.md) *(default)* | he has not said otherwise | see every slide on one pan/zoom canvas, click any element and edit it, export PNG/PDF |
| [PPTX → Google Slides](pptx-google-slides.md) | he wants to edit in a browser, or to hand the deck to a co-author | edit natively in Google Slides, present from it, share a link |
| [Standalone HTML](html.md) | he wants a web deck, or you need to screenshot-verify the render | open it, present from a browser, and you can check your own output |
| [Keynote via AppleScript](keynote.md) | he asks for Keynote — **and see the gate; it does not work on this machine** | finish by hand in Keynote |

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
- **A slide that went blank.** On a dark ground this is usually a black-ink asset on a dark ground
  or an inverted blackout (`brand/polarity.md`). On a light ground it is usually white-on-white.

The HTML path is the one you can verify most cheaply — if you need certainty about a tricky figure,
render it there first even when the deliverable is something else.
