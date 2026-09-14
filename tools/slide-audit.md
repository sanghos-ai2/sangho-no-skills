# Slide audit

Measured over **4 decks**, 365 slides.

**Those 365 slides are not 365
independent observations.** Grouping every slide against every
other at 64 x 36 px (box-filtered, mean
absolute RGB difference < 3.0) leaves
**170 distinct designs** — decks in this corpus reuse
each other's slides. Every other figure in this file is a count of
SLIDES, so a shape that recurs may be one slide carried forward rather
than a habit. The per-deck column below gives the share of each deck
that has a near-identical twin in another deck.

| Deck | Slides | Geometry (pt) | Aspect | Twinned in another deck |
|---|---|---|---|---|
| Job talk 2024 | 152 | 1920 x 1080 | 1.7778 | 109 (72%) |
| KAIST invited talk | 126 | 1920 x 1080 | 1.7778 | 108 (86%) |
| Luminate @ CHI'24 | 55 | 1920 x 1080 | 1.7778 | 10 (18%) |
| Sensecape @ UIST'23 | 32 | 1920 x 1080 | 1.7778 | 27 (84%) |

## Words per slide

Measured over 4 decks. Slides with no text count as zero, not as missing —
a full-bleed figure slide is a real measurement.

- median **12.0**
- interquartile range 5.0 - 25.0
- maximum 297
- share under four words: **18%**

**This is an upper bound, not slide copy.** These counts come from
`page.get_text()`, which sums onto one slide the actual slide copy,
text baked inside embedded figures,
and the deck's own page chrome (173 spans in this corpus
are a bare integer equal to their own slide's index). Presenter-note
text does not appear in the slide text layer in this corpus
(measured at 0 of 180 notes-bearing slides, below the 10% materiality bar this script uses — see "Notes in the text layer" under Presenter notes).
See "Words by font size" below for the breakdown a threshold would
need — this script does not pick one.

## Words by font size

Measured over 4 decks: total words at each font size, across every
slide. Slide copy, speaker narration, and figure-embedded text land at
different sizes on a given deck, but the convention is per-deck, not
universal — so this table is left unclassified rather than guessing a
threshold from a single deck.

| Size (pt) | Words |
|---|---|
| 21.0 | 3534 |
| 24.0 | 1259 |
| 50.0 | 360 |
| 30.0 | 255 |
| 84.0 | 242 |
| 53.0 | 224 |
| 31.7 | 180 |
| 60.0 | 167 |
| 36.0 | 159 |
| 32.0 | 159 |
| 85.0 | 126 |
| 22.0 | 118 |
| 42.0 | 116 |
| 90.0 | 113 |
| 15.0 | 112 |
| 74.0 | 111 |
| 66.0 | 111 |
| 80.0 | 108 |
| 70.0 | 103 |
| 89.0 | 103 |
| 86.0 | 96 |
| 49.0 | 93 |
| 48.0 | 92 |
| 43.0 | 92 |
| 51.0 | 85 |
| 78.7 | 82 |
| 96.0 | 82 |
| 33.0 | 78 |
| 19.0 | 78 |
| 62.0 | 70 |
| 45.0 | 67 |
| 44.0 | 63 |
| 47.5 | 62 |
| 41.0 | 60 |
| 75.0 | 57 |
| 38.0 | 55 |
| 98.0 | 54 |
| 78.0 | 51 |
| 112.0 | 47 |
| 46.0 | 47 |
| 57.0 | 45 |
| 119.0 | 44 |
| 63.0 | 42 |
| 58.0 | 42 |
| 92.0 | 41 |
| 79.3 | 40 |
| 40.0 | 37 |
| 59.0 | 37 |
| 102.0 | 34 |
| 25.0 | 33 |
| 111.0 | 30 |
| 120.0 | 29 |
| 73.8 | 28 |
| 67.6 | 28 |
| 81.0 | 26 |
| 73.0 | 24 |
| 59.6 | 23 |
| 74.9 | 22 |
| 39.0 | 22 |
| 29.0 | 22 |
| 108.0 | 22 |
| 27.0 | 21 |
| 54.0 | 18 |
| 37.0 | 18 |
| 55.0 | 17 |
| 83.0 | 16 |
| 59.8 | 15 |
| 65.0 | 15 |
| 100.0 | 13 |
| 110.0 | 12 |
| 72.8 | 12 |
| 47.0 | 11 |
| 46.6 | 10 |
| 98.6 | 10 |
| 159.0 | 10 |
| 82.0 | 10 |
| 78.3 | 8 |
| 76.0 | 8 |
| 68.0 | 6 |
| 94.0 | 6 |
| 128.0 | 6 |
| 103.0 | 6 |
| 71.0 | 6 |
| 244.1 | 4 |
| 35.0 | 4 |
| 56.0 | 4 |
| 38.3 | 4 |
| 23.0 | 2 |
| 116.0 | 2 |
| 113.0 | 2 |
| 76.4 | 2 |
| 124.0 | 1 |
| 43.5 | 1 |
| 137.0 | 1 |

## Presenter notes

Measured over 4 decks: 180 of 365 slides
carry presenter notes.

- median **22.5** words
- maximum 155 words

### Notes in the text layer

_None of the 180 notes-bearing slides' text matches any font size._

## Geometry

Measured over 4 decks: 1920 x 1080 pt. Archetypes take their dimensions from this table; a hard-coded
aspect ratio is a defect.

## Palette

Measured over 4 decks, by share of all sampled pixels. A pixel is
**neutral** when saturation < 0.15 or its brightest
channel < 40; otherwise **chromatic**.
Chromatic colours are binned to 16 levels per
channel before tallying, so close accent hues group into one row
instead of fragmenting into near-duplicates. Colours are reported,
not named or interpreted.

- neutral: **91.3%**
- chromatic: **8.7%**

### Chromatic colours, ranked

The table below divides that **8.7%**
chromatic share up further, by colour — each row is a share of
chromatic pixels only, not of the whole slide.

**These are the 8 largest of 1466 bins and cover
36.9% of chromatic pixels; the remaining
63.1% is not listed.** The heading says *chromatic*,
not *accent*, on purpose: a large bin is not necessarily a design
choice. The last column is how many slides carry 90% of that
colour's pixels — against 365 sampled slides, a single-digit
figure means the colour is one flat fill in a handful of images (a
screenshot, say) rather than an ink spent across the deck.
Reported, not interpreted.

| Colour | Share of chromatic pixels | Slides carrying 90% of it |
|---|---|---|
| `#303040` | 14.5% | 13 of 55 |
| `#404050` | 14.4% | 11 of 49 |
| `#505060` | 1.8% | 17 of 43 |
| `#304050` | 1.5% | 11 of 40 |
| `#f0f090` | 1.3% | 6 of 14 |
| `#d0d0a0` | 1.2% | 8 of 22 |
| `#c0e0f0` | 1.2% | 9 of 70 |
| `#203040` | 1.1% | 10 of 23 |
