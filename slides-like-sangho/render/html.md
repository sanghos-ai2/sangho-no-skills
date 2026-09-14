# Render path: standalone HTML

A single self-contained `.html` file: one `<section>` per slide at 1920 × 1080, arrow keys to
advance. Pick it when Sangho wants a web deck, or when you need to **look at your own output**
before handing it over — this is the cheapest path to verify, because you can drive it with
Playwright and screenshot every slide.

## Structure

`render/html/gen_deck.py` builds it. One `<section class="slide">` per slide, each a
`container-type: inline-size` box at `aspect-ratio: 16/9`, with **every length in `cqw`**.

```css
.slide { width: min(96vw, calc(96vh*16/9)); aspect-ratio: 16/9;
         container-type: inline-size; }
.t-title { font-size: 4.38cqw; }        /* 84pt of a 1920 page */
```

This is the same commitment the earlier draft of this file made with a JS-driven
`transform: scale()` — **scale the whole slide, never reflow it** — reached without the
JS. `1cqw` is 1% of the slide's own width, so a size written as `84/1920*100 = 4.38cqw`
IS 84pt at every window size, and the browser maintains it with no resize handler and no
flash before the first measurement. Everything placed inside stays in the same relation
at any scale, which is what the corpus requires: there is no grid across the 365 slides,
so every composition is placed, not laid out.

Consequences that follow:

- **Keyboard**: `->` / `Space` / `PageDown` forward, `<-` / `PageUp` back, `Home` / `End`.
  The index rides the URL hash, and a `hashchange` listener means a pasted `#31` moves the
  deck rather than only changing the address bar.
- **Speaker notes** are a hidden `.notes` block per slide, surfaced in a side panel on `N`.
  There is no notes field in HTML; this is the substitute.
- **Print** is the PDF path: `@page { size: 1920px 1080px }` plus `break-after: page`, so
  Cmd-P gives one landscape page per slide.
- **Images** go in the artifact's asset store (`upload_asset`), referenced by the returned
  `/_blob/<id>` url verbatim. Do NOT inline them as data URIs: base64 inflates by a third
  and the rendered page is capped at 16MB, which a handful of paper figures will breach.
  Downscale to 3840 wide first - beyond 2x a 1920 slide buys nothing.
- **Write the file as pure ASCII** (`encode("ascii", "xmlcharrefreplace")`). The page cannot
  then depend on a charset header being right, which is exactly what produced `researchersa\u20ac\u2122`
  in a local preview once.

## Sizing: fit the box, never count the words

**The single most important rule in this path.** The corpus says he fixes only two sizes —
the slide number and the title — and sizes everything else to fit. So:

For each candidate size on his ladder (112 / 84 / 50 / 36 and below only when forced),
estimate the wrapped height from per-character advance widths, reject any size at which a
single unbreakable word is wider than the column, and take the largest that fits in BOTH
axes. `gen_deck.py:fit()`.

- **Per-character widths, not a flat factor.** In Manrope `W` is 0.95em and `i` is 0.30em;
  a flat 0.5 is wrong by 3x at the extremes, and a word count sees neither.
- **112 is offered only to a single line of three words or fewer.** It is his display size
  and the corpus reserves it for naming slides. Without that guard the fitter happily sets
  a 10-word line at 112 and wraps it to three lines, which "fits" and is still wrong.
- **A word-count heuristic was tried first and was visibly wrong** — it produced a deck
  whose commonest size was the 30pt fallback. Fitting moved 84pt to the commonest size and
  raised the floor of the whole deck to 50pt.

**Reflow pasted prose before sizing.** Text pasted from a document carries hard newlines
where it happened to wrap. Those are not line breaks he chose, and rendering them as lines
puts a paragraph gap mid-sentence. Rejoin a line of 60+ characters that ends unfinished
with a following line that starts lower-case; leave a deliberate short stack alone.

## Section headers: bin the size, keep it on one line

Boxed chapter labels are 74pt in the corpus on SHORT text. When they carry a real title,
size them from **four bins** (74 / 58 / 46 / 36), picking the largest at which the text
still fits on ONE line. A continuous formula produced 18 distinct sizes across 29 headers,
so two headers of near-equal length got visibly different boxes. Single-line is the half
that actually holds the box height steady: a wrapped header doubles its height at any size.

A slide carrying a header box must also push its body down (`.slide.hashdr .pad{top:15cqw}`)
or the content renders behind the box — silently, because both are legible on their own.

## Tables

Recreate them in type rather than pasting a screenshot. Measured: **0 of 365 slides in the
corpus carry a table of statistics** (`references/never-list.md` entry 3), and a crop of a
paper table lands its body type at 18-36 units on a 1920 slide. `render/html/crop_paper_tables.py`
generates faithful crops from the compiled PDF when the paper's own layout is the point -
it finds each table's extent from the booktabs rules in the raster, which also excludes
submission line numbers without hardcoding a margin.

- **Alignment comes from a column's CONTENT, never its position.** A column is numeric when
  most of its filled cells begin with a digit or sign, and that one verdict drives the header
  AND the cells so they cannot disagree. Keying off position right-aligns a text column's
  heading over left-aligned cells.
- **Size the cell to the room actually left** — the slide's height less the header box and
  the caption — not to a constant. A 7-row table on a captioned, headed slide overflows by a
  row otherwise, and the clipped row is below the fold where you will not see it.

## Notes

There is no notes field. Write `notes.md` beside the deck, numbered to the slides, or — if he wants
them in the file — a hidden `<aside>` per section toggled by `N`, which also gives him a crude
presenter view on a second window.

## Verifying, which is the point of this path

```bash
# serve, then screenshot every slide
python3 -m http.server 8765 --directory <output dir>
```

Drive it with Playwright at a 1920 × 1080 viewport, step with `ArrowRight`, screenshot each slide,
and **look at the images**. Check, by name:

- **Type size.** Measure one Display and one Title against 112 pt / 84 pt. A brand pack's screen
  scale halving the deck is invisible in code and obvious in a screenshot (`brand/README.md`).
- **Blank or near-blank slides — against the storyboard, not on sight.** Black ink on a dark
  ground, white on white, a figure whose stroke colour did not get restroked
  (`brand/polarity.md`). **An empty black slide at a blackout beat is correct**, at any polarity
  (`brand/polarity.md` §3, confirmed by Sangho) — it is the single most plausible correct output to
  mistake for a render failure, and the corpus puts one at both ends of most decks. What to flag is
  **a blackout beat that rendered light**, and any *other* empty slide the storyboard did not ask
  for.
- **Text overflowing its slide.** Quotes have no fixed size in the corpus — 20 distinct sizes across
  39 quote spans — because each is set to fill its slide. A quote set at a step will overflow.
- **Word count.** The corpus median is 9 words of real slide copy. A slide running to 40 is not
  automatically wrong (the Takeaway and quote cards reach 77–83) but it is worth a second look.

Screenshot verification is the reason to reach for this path even when the deliverable is a canvas
or a PPTX: render the tricky figures here first, look at them, then build the real thing.
