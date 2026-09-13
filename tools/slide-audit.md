# Slide audit

Measured over **1 deck**, 55 slides.

| Deck | Slides | Geometry (pt) | Aspect |
|---|---|---|---|
| Luminate @ CHI'24 | 55 | 1024 x 768 | 1.3333 |

## Words per slide

Measured over 1 deck. Slides with no text count as zero, not as missing —
a full-bleed figure slide is a real measurement.

- median **27.0**
- interquartile range 17.0 - 44.0
- maximum 321
- share under four words: **5%**

**This is an upper bound, not slide copy.** These counts come from
`page.get_text()`, which sums three unrelated things onto one slide:
the actual slide copy, speaker narration Sangho sometimes renders onto
the slide itself, and text baked inside embedded figures. See
"Words by font size" below for the breakdown a threshold would need —
this script does not pick one.

## Words by font size

Measured over 1 deck: total words at each font size, across every
slide. Slide copy, speaker narration, and figure-embedded text land at
different sizes on a given deck, but the convention is per-deck, not
universal — so this table is left unclassified rather than guessing a
threshold from a single deck.

| Size (pt) | Words |
|---|---|
| 12.8 | 828 |
| 5.5 | 432 |
| 13.1 | 139 |
| 7.9 | 91 |
| 15.7 | 68 |
| 6.3 | 55 |
| 12.9 | 42 |
| 15.2 | 42 |
| 19.7 | 40 |
| 12.1 | 39 |
| 6.6 | 33 |
| 8.3 | 28 |
| 17.3 | 27 |
| 11.5 | 25 |
| 23.4 | 23 |
| 15.5 | 22 |
| 22.6 | 21 |
| 21.0 | 18 |
| 14.4 | 17 |
| 15.0 | 16 |
| 11.8 | 15 |
| 29.4 | 15 |
| 17.1 | 15 |
| 9.7 | 12 |
| 14.2 | 12 |
| 19.1 | 12 |
| 12.5 | 10 |
| 21.5 | 6 |
| 23.6 | 6 |
| 27.0 | 6 |
| 18.6 | 6 |
| 7.1 | 5 |
| 18.4 | 5 |
| 9.4 | 5 |
| 10.8 | 4 |
| 16.3 | 4 |
| 20.5 | 3 |
| 20.1 | 2 |
| 5.8 | 2 |
| 11.4 | 1 |
| 36.0 | 1 |

## Presenter notes

_No presenter notes extracted._

## Geometry

Measured over 1 deck: 1024 x 768 pt. Archetypes take their dimensions from this table; a hard-coded
aspect ratio is a defect.

## Palette

Measured over 1 deck, by share of all sampled pixels. A pixel is
**neutral** when saturation < 0.15 or its brightest
channel < 40; otherwise **chromatic**.
Chromatic colours are binned to 16 levels per
channel before tallying, so close accent hues group into one row
instead of fragmenting into near-duplicates. Colours are reported,
not named or interpreted.

- neutral: **98.4%**
- chromatic: **1.6%**

### Accent colours

| Colour | Share of all pixels |
|---|---|
| `#303040` | 0.6% |
| `#202030` | 0.1% |
| `#d0d0a0` | 0.1% |
| `#e0e0a0` | 0.1% |
| `#e0e0b0` | 0.0% |
| `#f0e0b0` | 0.0% |
| `#404050` | 0.0% |
| `#e0d0a0` | 0.0% |
