# Render path: standalone HTML

A single self-contained `.html` file: one `<section>` per slide at 1920 × 1080, arrow keys to
advance. Pick it when Sangho wants a web deck, or when you need to **look at your own output**
before handing it over — this is the cheapest path to verify, because you can drive it with
Playwright and screenshot every slide.

## Structure

One file. Slides as absolutely-positioned 1920 × 1080 sections, scaled to the viewport with a CSS
transform so the deck fills any window without reflowing:

```css
:root { --slide-w: 1920px; --slide-h: 1080px; }
.deck  { width: var(--slide-w); height: var(--slide-h);
         transform: scale(var(--fit)); transform-origin: top left; }
```

with `--fit` set once from `min(innerWidth / 1920, innerHeight / 1080)` on load and resize.

**Scale the whole slide; never reflow it.** The corpus has no grid — no repeating columns, no
consistent left margin, no baseline grid across 365 slides — so every composition is placed, not
laid out. A responsive deck would move his elements relative to each other, which is the one thing
the composition cannot survive. Absolute positions inside a fixed 1920 × 1080 box, scaled as a
unit, keeps every relationship exact at every window size.

Everything else follows from that:

- **Type in absolute `px`**, at the derived scale — 112 / 84 / 50 / 36 / 24. Not `rem`, not `vw`.
- **Keyboard**: `→` / `Space` / `PageDown` forward, `←` / `PageUp` back, `Home` / `End` to the ends.
  Read the current index from the URL hash so a slide is linkable and a reload does not lose the
  place.
- **A build is N sections.** Same rule as every other path: copy the previous section and change
  the part that changes.
- **Inline the assets.** Fonts, images and SVG go in the file, so "self-contained" is true and he
  can mail it to somebody. Photographs at 2× (3840 wide) as base64 will make the file large; say
  how large in the handback if it passes a few MB.

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
- **Blank or near-blank slides.** Black ink on a dark ground, white on white, an inverted blackout,
  a figure whose stroke colour did not get restroked (`brand/polarity.md`).
- **Text overflowing its slide.** Quotes have no fixed size in the corpus — 20 distinct sizes across
  39 quote spans — because each is set to fill its slide. A quote set at a step will overflow.
- **Word count.** The corpus median is 9 words of real slide copy. A slide running to 40 is not
  automatically wrong (the Takeaway and quote cards reach 77–83) but it is worth a second look.

Screenshot verification is the reason to reach for this path even when the deliverable is a canvas
or a PPTX: render the tricky figures here first, look at them, then build the real thing.
