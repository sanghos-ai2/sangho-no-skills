# Visual language — first pass

**Evidence base: one deck.** Luminate @ CHI'24, 55 slides. Nothing here is a claim about
Sangho's work in general. Sensecape (UIST'23), the 2024 job talk, and the KAIST invited talk
are not yet ingested, so every sentence below should be read as *"in Luminate"*, and several
will probably turn out to be Luminate-specific rather than characteristic.

Quantitative claims cite [`tools/slide-audit.md`](../../tools/slide-audit.md) (1 deck, 55
slides) or, where noted, `controller-findings.md`. Slide counts that I produced by looking at
all 55 images are labelled **(my count)** — they are not audit figures and Sangho should treat
them as claims to check, not as measurements.

---

## Read this first: the audit's numbers do not measure the slides

This is the thing most likely to be wrong in every document in this folder, so it goes at the top.

**The rendered corpus pages are not slides.** They are Keynote's *"slide with presenter notes"*
PDF export. Each page is a white sheet carrying a 16:9 slide reproduced small in its upper
portion, with the presenter note set below it as plain text. I confirmed this on every page:
the slide's frame occupies an identical box on all 55, and the text below it is the note
verbatim.

Three audit figures inherit that framing, and each is measuring the export rather than the design:

| Audit figure | What it actually measures |
|---|---|
| Geometry **1024 × 768 pt, aspect 1.3333** (1 deck) | the export **page**. The slide inside it is **16:9**, not 4:3. `controller-findings.md`'s "all four canon decks are 1024 × 768 (4:3), not 16:9" is describing the same export artifact and is likely wrong about the slides too — worth re-checking before it reaches the skill. |
| **neutral 98.4% / chromatic 1.6%** (1 deck) | the page, which is mostly white paper margin and black note text. The direction is right — the slides *are* overwhelmingly achromatic — but the specific share is inflated by the export. |
| **median 27.0 words/slide**, max 321 (1 deck) | already flagged in the audit as an upper bound. Two of the three contributors are not slide copy: the 12.8 pt band (**828 of 2153 words, 38%** — audit, "Notes in the text layer", 35/35 notes-bearing slides) is the printed note, and the 5.5 pt band (**432 words** — audit) is text baked inside embedded screenshots. |

**Font sizes in the audit are export-page sizes, not slide sizes.** The slide is reproduced at
roughly half the page width, so on-slide type is roughly twice the listed value. Use the audit's
size table as *ratios between roles*, never as absolute point sizes. Writing a template against
"21 pt for the hero question" would produce type half the size Sangho used.

**What this costs.** Colour share, density, and geometry all need re-measuring against the slide
box before the skill quotes any of them. Archetype and narrative conclusions survive: those come
from looking at the slides, not from the page-level statistics.

---

## Type

**There is no tight type scale.** The audit's size table lists **41 distinct font sizes across
55 slides** (1 deck). That is an ad-hoc, per-slide sizing habit — text is sized to fit its job on
that slide, not drawn from a 4- or 5-step ramp. A skill that imposes a strict scale would be
imposing something the deck does not have.

Grouping the audit's sizes by the role I can see them playing (ratios, not points; roles assigned
by me from the images):

| Role | Audit sizes | Example slides |
|---|---|---|
| Closing hero | 36.0 | 54 ("Questions?") |
| Section / system name | 29.4, 27.0 | 33, 45, 22, 42 |
| Full-stop question, borrowed quote | 23.4, 22.6, 21.5, 21.0 | 4, 5, 13, 19 |
| Slide title, band label on a screenshot | 19.7, 19.1, 18.6, 17.3, 17.1 | 25, 26, 31, 32, 43 |
| Sub-title, participant id, banner subtitle | 15.7, 15.2, 15.0, 14.4, 14.2 | 20, 21, 36, 38 |
| Body, quote text, diagram labels | 13.1, 12.9, 12.1, 11.8, 11.5 | 6, 16, 38, 39 |
| Secondary grey detail | 9.7, 9.4 | 36 |
| Handwritten annotation, slide number | 8.3, 7.9, 7.1, 6.6, 6.3 | 7, 21, 34 |
| **Not slide type** | 12.8 (printed note), 5.5 (inside screenshots) | — |

**Two type families, with strictly separated jobs** (observation, 1 deck). A grotesque
(consistent with Keynote's stock White theme, which `controller-findings.md` names as the base)
carries everything the *author* says: titles, section names, framing questions, study facts. A
single informal handwriting face carries everything that is *someone else's voice or a margin
note*: participant quotes (38, 39, 43, 44), labels pointing at parts of a screenshot (23, 24,
26–30), captions under figures (51), asides ("freely (in non-controlled setting)", 34), and the
two closing questions (52). I could not identify the handwriting face from raster; it needs
naming from the Keynote internals before a template can use it.

**Weight, not size, does most of the emphasis work.** Bold-vs-regular inside one line is the
commonest device (34, 35, 41: "**Q1.** Help Avoid Fixation?"; 36: bold label over grey detail).

**Emphasis is often inverted.** In the participant-quote slides the *whole quote* is set in grey
and the load-bearing phrase is pushed up to black, rather than the reverse (38, 39, 44). The
slide de-emphasises the context instead of emphasising the point. This is the single most
distinctive typographic habit I found.

---

## Space

**Empty space is used as a full-strength element, not as a margin.** Roughly a third of the
slides leave half the canvas or more genuinely empty (10, 20, 22, 33, 41, 42, 45) — **(my count)**.
Slide 45 is three words in the middle of an otherwise blank field.

**Content is placed where the argument is, not in a grid.** There is no repeating column
structure, no consistent left margin, no baseline grid I could detect across the 55. A diagram
sits left and its text right on 7; the same relationship is reversed on 36. Band labels on
screenshots (23–32) land in whichever corner of the screenshot is empty, and move between slides.

**Screenshots are full-bleed.** Interface captures run to all four edges of the slide (23–32, 48,
49, 50) — no device frame, no rounded card, no inset with a caption underneath. The slide *becomes*
the interface, and Sangho's own marks are drawn on top of it.

**The deck is mostly white.** 47 of 55 slides are light-dominant; 8 are dark-dominant **(my count,
mean-luminance measurement over the cropped slide box)**, and those 8 split into two jobs: the two
blackout bookends plus two dark-UI screenshots (1, 55, 48, 50), and four deliberate blackouts of the
stage (4, 19, 53, 54).

---

## Figures

**One metaphor carries the whole first half.** A parallelogram — the "design space" plane — with
small circles as ideas, a cone of warm light as one person's attention, and a star as the optimal
idea. It is introduced on 6 and then rebuilt, extended, filled, doubled and dimmed on 7, 8, 9, 10,
11, 12, 13, 16, 17, and returns at 51. That is **eleven slides sharing one drawing**
**(my count)**. The argument is made by *changing the same picture*, not by presenting a sequence
of different pictures.

**Diagram strokes are deliberately rough.** Plane edges, arrows, circles and box borders all carry
a noisy, hand-drawn edge rather than a crisp vector line (6–13, 16, 17, 34, 35, 40, 41, 47, 51).
This is a consistent, chosen texture, not an artifact.

**People are drawn, not photographed.** The study population is a cluster of black-and-white
cartoon faces (36, 37, 42), and each quoted participant gets one cartoon face plus a hand-lettered
id (38: P6; 39: P2, P7; 43: P4; 44: P14). Photographs appear on exactly three slides: the Pauling
portrait (5) and the team headshots (53, 54).

**Prior work is shown, not cited.** Related systems appear as screenshots with the venue lettered
beneath (3: CHI'22, UIST'23, VIS'23, DIS'23, IUI'23; 18: Promptify UIST'23, PromptMagician VIS'23).
There is no textual citation anywhere on the 55 slides.

**There is not a single chart.** No bar chart, no line graph, no table of statistics, across two
studies and 55 slides **(my count)**. Results are carried entirely by participant quotes, and the
deck says so out loud in the corner of 34 and 35: "* Please read our paper for detailed results".

---

## Titles

**There is no title on most slides.** At least 25 of 55 carry no title element of any kind
**(my count)**: 1, 6, 7, 8, 10, 11, 12, 14, 15, 16, 17, 23–32, 48, 49, 50, 55. Several more
(2, 3, 5, 18, 53, 54) have no title either, though they are cards rather than body slides.

**Where a title exists it is centred, bold, black, at the top** (9, 13, 34–44, 46, 47, 51). Not
left-aligned, not in a coloured bar, not the theme's title placeholder as far as I can tell.

**A band label is the substitute for a title on image slides.** A solid grey or near-black
rectangle with white text, dropped onto a screenshot or diagram wherever there is room — 9, 13,
20, 21, 22, 23, 25–32, and the highlighter-coloured variants on 3 and 21. It names the beat
without claiming the top of the slide.

---

## Colour

**Colour is a scarce, semantic resource.** The audit's neutral/chromatic split (98.4 / 1.6,
1 deck) measures the export page and overstates the effect, but the direction is right: almost
everything is black, white and grey, and colour is reserved for meaning.

Two of the eight colours the audit reports are the deck's real accent, and five of the eight are
one family:

| Audit colour | Share of chromatic pixels (1 deck) | What I see it doing |
|---|---|---|
| `#303040`, `#202030`, `#404050` | 39.2%, 7.6%, 2.4% | **Not an accent.** Dark-navy UI chrome in the ChatGPT-style screenshots (14, 15, 48, 49, 50) and the blackout slides. |
| `#d0d0a0`, `#e0e0a0`, `#e0e0b0`, `#f0e0b0`, `#e0d0a0` | 4.5%, 3.2%, 3.1%, 3.0%, 2.1% | **The real accent.** One warm amber/cream family: the cone of attention and the filled design-space plane (7, 8, 11, 12), the Luminate mark (22, 53, 54), the highlighted text panel in the system (26–30). |

**Red and blue are the argument's two colours, and they never appear in the audit's top eight** —
consistent with their being spent on a few words at a time. Red marks the problem ("Fixation" —
7, 9, 11, 12, 13, 34, 35, 38, 40); blue marks the good thing ("Design Space Thinking" — 8, 9, 12,
13, 34, 35, 39, 40, 52; and "creative" on 4). The pairing is stable across the whole deck: once a
term has a colour it keeps it. On 8 the switch between them is staged as a strike-through of the
red word and its replacement by the blue one.

**Green and salmon appear once each, as a local pair** (46, 47: Diverge / Converge bands), and
green/amber marker underlines appear once (44). These are local, not part of the deck palette.

---

## The emphasis vocabulary

A short, repeatedly reused set of marks (observation, 1 deck; slide lists are **my counts**):

- **Marker underline** — a rough highlighter stroke under one term, in that term's colour
  (7, 8, 9, 11, 12, 13, 19, 34, 35, 38, 39, 40, 41, 43, 44, 52).
- **Solid band behind white text** — the label device described under Titles.
- **Strike-through replacement** — one concept crossed out and another written over it (8).
- **A large X** — negation drawn onto the diagram rather than written (13, 46, 47).
- **Rough-bordered box** — a hand-drawn rectangle around the thing being returned to
  (34, 35, 40, 41, 51).
- **Hand-drawn arrow with a handwritten label** pointing into a screenshot or figure
  (7, 21, 24, 26–30, 34, 53).
- **Dimming the stage** — the previous slide's content greyed out so a question can be laid over
  it (19, 52).

---

## What I am least sure of

1. **Everything geometric and chromatic**, because the audit measured the export page. See the
   top of this file.
2. **Whether the rough stroke is his or the illustration source's.** The parallelograms, arrows
   and boxes all carry it, and the cartoon faces do too, which is consistent with either a
   deliberate deck-wide texture or an asset pack that came that way.
3. **Whether "no chart, ever" is taste or is Luminate-specific.** A qualitative user study and a
   deployment study genuinely have little to plot. A deck with quantitative results may look
   completely different.
4. **The handwriting face's identity.** Everything about the author-voice / other-voice split
   depends on naming it, and I cannot name it from raster.
