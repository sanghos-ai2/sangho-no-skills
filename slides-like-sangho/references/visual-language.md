# Visual language

**Evidence base: four decks, 365 slides** — Luminate @ CHI'24 (55), Sensecape @ UIST'23 (32),
KAIST invited talk (126), job talk 2024 (152). All 1920 × 1080, 16:9
([`tools/slide-audit.md`](../../tools/slide-audit.md), "Geometry").

Quantitative claims cite the audit, or are marked **(computed here)** with the method stated.
Claims that come from looking at the slides are marked **(observed)** and carry slide numbers so
Sangho can refute them with one counter-example.

---

## Read this first: the four decks are not four independent samples

This is the thing most likely to mislead in everything below, and it was not known when the
previous pass was written.

**The decks share slides, heavily.** Comparing every slide against every other at 64 × 36 px
(box-filtered, mean absolute RGB difference), **computed here**:

| Deck | Slides with a near-identical twin in another deck (MAE < 3) | Strict (MAE < 1.5, low-detail slides excluded) |
|---|---:|---:|
| Luminate | 10 / 55 (18%) | 3 |
| Sensecape | 27 / 32 (84%) | 9 |
| KAIST | 108 / 126 (86%) | 67 |
| Job talk | 109 / 152 (72%) | 68 |

The two long decks are **anthologies**. KAIST and the job talk each drop the Sensecape and
CodeToon talks in more or less whole, plus a redrawn version of Luminate, inside a new frame.
So a shape that appears "in three decks" may be one slide he made once. **Every per-deck count
in `archetypes.md` should be read with that in mind**, and a device that appears independently
in Luminate *and* Sensecape is much better evidence than one that appears in KAIST and the job
talk, which are near-siblings.

**The frame is measurable, and it is where his own composition lives.** A cream right-edge strip
(`#f0eade`) carrying a five-icon rail appears on 24 / 126 KAIST slides and 30 / 152 job-talk
slides, and on **zero** slides of the two conference decks (**computed here**: the modal colour of
the right 4.5% of the slide is cream-ish *and* that strip contains dark pixels).
Those rail slides are exactly the frame — KAIST 1, 4–6, 9–17, 46–47, 76–77, 118–124; job talk 5,
12–14, 17–18, 20–30, 61–62, 94–95, 142–150 — and never the embedded paper segments. The rail
switches off the moment a reused conference talk begins.

---

## Two registers, not one style

**"Register" is my word for a bundle of surface choices — ground colour, stroke quality, type
families, whether people are drawn or photographed — that move together across a deck. It is a
description, not an explanation, and the two groupings below are a hypothesis about what causes
them, not a grade of evidence.** Wherever a later section needs to say how well-evidenced a shape
is, it names the decks, not the register. Read §"What I am least sure of", item 1, before using
the vocabulary for anything.

Reading all 365 slides, there are two clearly separated bundles, and the previous pass
described only the first because it only had Luminate.

**The conference register** — Luminate, and only Luminate. Flat white ground. A rough,
hand-drawn stroke on every figure edge. An informal handwriting face for anything that is not
the author's formal argument. Black-and-white cartoon faces for people. Highlighter-marker
underlines. Red / blue as the argument's two colours.

**The talk register** — KAIST and the job talk. Cream or white ground. Clean vector strokes, no
roughness. A serif display face on the title card. Real photographs and AI-generated imagery. A
blue→magenta gradient (KAIST) or orange/teal (job talk) on the load-bearing words. Line icons used
as nouns. A persistent icon rail.

**Sensecape belongs to neither cleanly, and that is useful.** It has the talk register's clean
vector strokes, grotesque-only type and line icons, with none of Luminate's roughness,
handwriting or cartoons — and at the same time it has the conference register's flat white ground,
no cream, no rail, no photographs, and almost no colour at all (1.2% chromatic once its four
screenshots are removed). It is the austere case: the same compositional moves with the decoration
taken out.

**The same argument was re-drawn between the two.** Luminate's design-space figure (rough
parallelogram, cartoon boy, amber gradient cone — Luminate 7, 11, 12) is redrawn for KAIST 24–30
and job-talk 37–43 as a crisp vector parallelogram with a line-art head and a flat yellow cone.
The roughness and the cartoon were **dropped on purpose**, not lost — the composition is
identical and everything else was kept. That is the strongest evidence in the corpus that the
rough/hand-made look is a *choice per talk*, not a fixed house style. **(observed)**

---

## Type

**Sizes are now real.** The pages are 1920 × 1080, so the audit's size table is in true slide
points for the first time — the previous pass's warning that "on-slide type is roughly twice the
listed value" is dead and should not be carried forward.

**Distinct sizes per deck (computed here, from `spans[].size`):**

| Deck | Distinct sizes | Range |
|---|---:|---|
| Luminate | 41 | 21 – 137 pt |
| Sensecape | 19 | 21 – 120 pt |
| KAIST | 75 | 15 – 244 pt |
| Job talk | 80 | 15 – 244 pt |

**There is still no type scale**, and this now holds over four decks, not one. Sensecape is the
tightest at 19 sizes over 32 slides and is the closest thing to a ramp; the two long decks are
ad hoc. A template that imposes a 4- or 5-step scale imposes something no deck in this corpus has.

**Two of the audit's biggest word buckets are not slide type at all** (**computed here**, by
grouping every span by size and counting the slides each size lands on):

- **21.0 pt — 3,534 words but only 18 slides**, median 64 words per span. That is text baked
  inside the embedded ChatGPT screenshots (Luminate 14, 15, 48–50; and their twins). It is the
  single largest row in the audit's size table and says nothing about how he sets type.
- **22.0 pt — 118 words in 118 spans, every one of them the slide number.** Nothing else is set
  at this size anywhere in the corpus.
- **24.0 pt — 1,259 words in 122 spans, of which only 55 spans (55 words) are the slide number.**
  The other 67 spans carry **1,204 words and are entirely figure text**: enumerated on their full
  text, they are **12 distinct strings** — the ChatGPT avatar chip `SA` (x17), `1. 2. 3.` (x9),
  the CodeToon abstraction table in two lengths (an 18-word variant x8 and a 49-word variant x8),
  `... ... ... ...` (x6), `Regenerate` (x4), `SA Regenerate` (x4), `> <` (x3), `Explore` (x1),
  `Regenerate Explore` (x1), and two ChatGPT prompts — 28 words (x3) and 165 words (x3, on
  Sensecape 10, KAIST 56, job talk 71). **The bucket's median span of one word comes from the
  numbers; its mass does not**, and an earlier draft of this document called the whole bucket
  "the slide number", which is wrong about 96% of its words. (An earlier count of this
  enumeration said 11 distinct strings; it compared truncated text and so merged the CodeToon
  table's two length variants.)

**The slide number itself is 173 spans** — 55 at 24 pt plus 118 at 22 pt — and **zero spans in the
corpus are a bare integer that is *not* that slide's own index**: Luminate 42/55, Sensecape 8/32,
KAIST 56/126, job talk 67/152.

**Real slide copy is about 9 words** (**computed here**: every span, minus the 21.0 pt and
24.0 pt bands — verified above to contain only figure text plus the 55 slide numbers — and minus
any bare-index span at any size):

| Deck | Median copy words | IQR | Max (slide) | ≤ 3 words | 0 words |
|---|---:|---|---|---:|---:|
| Luminate | 9 | 4 – 23 | 69 (#39) | 20% | 9% |
| Sensecape | 4 | 0 – 13 | 44 (#30) | 44% | 28% |
| KAIST | 9 | 4 – 20 | 83 (#44) | 24% | 13% |
| Job talk | 11 | 4 – 19 | 77 (#58) | 20% | 11% |
| **All four** | **9** | **4 – 19** | **83** | **24%** | **13%** |

Each maximum is now a real slide: #39 and #30 are participant-quote cards, #44 and #58 are
Takeaway cards. **An earlier draft of this table reported a maximum of 195 for three of the four
decks** — that was Sensecape 10 / KAIST 56 / job talk 71, one reused slide whose 165-word ChatGPT
prompt sits at 24 pt and therefore survived a filter aimed at 21 pt. The median, IQR and
short-slide columns barely moved when it was removed (corpus median 10 -> 9); the maximum was the
only figure it distorted, and it distorted it by a factor of two.

The audit's raw median of **12.0** words/slide is the upper bound including all figure text; **9**
is the same measure with the two figure bands removed. Either way, **a slide is a phrase, not a
paragraph.** Nearly one slide in four is three words or fewer.

**Emphasis is inverted, in every deck, in two different type families.** This was the previous
pass's strongest single finding and it survives intact — and generalises. In a quote slide the
*context* is set back and the *load-bearing phrase* is pushed forward, rather than the reverse:

- Luminate 38, 39, 43, 44 — handwriting face, grey for context, black + coloured marker underline
  for the phrase.
- Sensecape 23, 24, 30; KAIST 73, 112, 113; job talk 84, 85, 88, 130, 131 — grotesque italic,
  grey regular for context, **bold black** for the phrase.

Same device, two completely different type systems. **(observed)** It is the most portable thing
in this corpus.

**Headline colour is a gradient on the words that matter** (KAIST, job talk). `Changing Levels of
Abstraction for Learning` (job talk 103–109), `How Do We Make Connections Clear?` (124–128),
`Takeaways` (132), `amplify our mind` (KAIST 9, 10) all carry a blue→magenta ramp across the
line, and inside body copy the same ramp marks the two or three terms being defined
(job talk 112, 130, 131). The job talk uses orange/teal in the frame sections and the
blue→magenta ramp inside the CodeToon segment. **(observed)**

---

## Space

**The ground is white, with a second cream ground for the frame** (**computed here**: modal
colour of an 80 × 45 box-filtered slide, classified white when its brightest channel is ≥ 245 and
near-neutral, cream when warm and in the 225–248 range, black when its brightest channel is < 40,
and "dark" otherwise below 110):

| Deck | White | Cream `#f0eade` / `#f0eae0` | Black | Dark (UI capture or dimmed stage) | Other |
|---|---:|---:|---:|---:|---:|
| Luminate | 46 | 0 | 5 | 4 | 0 |
| Sensecape | 28 | 0 | 2 | 2 | 0 |
| KAIST | 93 | 25 | 5 | 2 | 1 |
| Job talk | 96 | 36 | 11 | 6 | 3 |
| **All four** | **263** | **61** | **23** | **14** | **4** |

**Dark-dominant slides (mean luminance < 110): 8 / 55, 4 / 32, 8 / 126, 16 / 152 — 36 of 365,
10%** (**computed here**). Darkness is a device, not an accident: it is the blackout bookends,
the dark-UI screenshots, and the dimmed stage.

**Empty space is used at full strength.** Sensecape is the extreme: 22% of its slides carry no
copy at all and a third carry three words or fewer, and slides 19 and 20 are a nearly blank
canvas carrying one small chip in a corner. Luminate 45 is four words on three lines in an
otherwise empty field; KAIST 38 and job talk 51 are four words centred on white. **(observed)**

**There is no grid.** No repeating column structure, no consistent left margin, no baseline grid
detectable across the 365. Where a diagram and its text share a slide, either can be on either
side (Luminate 7 vs 36; job talk 37 vs 40). Band labels on screenshots land wherever the
screenshot is empty and move between adjacent slides. **(observed)**

**Screenshots are full-bleed or half-bleed, never framed.** Interface captures run to the slide
edges (Luminate 23–32, 48–50; Sensecape 18–22; job talk 79–83, 122–123) or occupy one clean half
against the diagram (Luminate 14–15; KAIST 32–33; job talk 45–46). No device frame, no rounded
card, no inset-with-caption. **(observed)**

---

## Figures

**The deck advances by editing the picture, not replacing it.** This is the single strongest
cross-deck compositional finding. **Computed here**: mean absolute difference between each pair
of consecutive slides at 64 × 36 px.

| Deck | Consecutive pairs that are edits of the slide before (MAE < 25) | Longest run |
|---|---:|---|
| Luminate | 30 / 54 (56%) | 11 slides (25–35) |
| Sensecape | 17 / 31 (55%) | 11 slides (12–22) |
| KAIST | 83 / 125 (66%) | 19 slides (85–103) |
| Job talk | 92 / 151 (61%) | 19 slides (103–121) |

At the stricter MAE < 10 the shares are 17% / 26% / 36% / 34%. Either threshold says the same
thing: **more than half of every deck is one picture being changed.** The previous pass found
this in Luminate's design-space plane (eleven slides) and it turns out to be the governing habit
of the whole corpus — job talk 103–113 builds the abstraction ladder over eleven slides;
Sensecape 11–16 builds the simple↔complex axis over six.

**The accompanying device is greying back, not adding.** When the picture gains a part, the parts
already explained fade to light grey and only the new one is black: Sensecape 12–16 (the four
representations along the axis, one black at a time), KAIST 46/47/76/77/118 and job talk
61/62/94/95/142 (the three "spaces", one black at a time), job talk 105–111 (the abstraction
ladder's columns). The current thing is the only thing at full contrast. **(observed)**

**The rough stroke is Luminate's, not the corpus's.** Noisy, hand-drawn plane edges, arrows, box
borders and cartoon faces are everywhere in Luminate (6–13, 16–17, 34–35, 40–41, 47, 51) and
appear nowhere in Sensecape, and in KAIST/job talk only on the redrawn Luminate segment's own
`Thinkable Territory` parallelogram outline (KAIST 11–15, 120–124). **(observed)** The previous
pass could not tell whether the roughness was his or an asset pack's; the redraw settles that it
is a per-talk decision, but not who drew it.

**People are drawn in the conference register and photographed in the talk register.** Luminate's
study populations and quoted participants are hand-drawn black-and-white cartoon faces (36, 37,
38, 39, 42, 43, 44). The same studies in KAIST 43 and job talk 56 are re-presented with **flat
stock-style vector people icons** (orange and slate). **(observed)**

**AI-generated imagery is a real element of the job talk and is credited.** Job talk 11, 59, 60,
91, 92, 93, 140, 141 and KAIST 3 carry generated illustrations, used full-bleed as a backdrop
under a dark translucent band carrying the question. Job talk slide 93's presenter note is the
generation's own description text ("Here is the image depicting a group of researchers…"), which
is how we know. **(observed / notes)**

**Prior work is shown, not cited.** Other people's systems appear as screenshots with a venue
lettered beneath (Luminate 3, 18; KAIST 20, 36, 81; job talk 6, 33, 49, 99). There is no
textual citation anywhere in the corpus's slide copy. **(observed)**

**There is not one chart of his own results in 365 slides.** No bar chart, no line graph, no
scatter, no table of statistics — **(observed)**, across five studies. And **no inferential
statistic**: searching slide copy for `p </=/>`, `SD`, `M =`, `CI`, `t(`, `F(`, the chi symbol,
`ANOVA`, `significan*`, "effect size" and the plus-minus sign returns **0 of 365**, as does the
`%` character (**computed here**).

**Descriptive study quantities are a different matter, and they are present** — `14 Professional
Writers`, `8 Professional Writers`, `Creative Writing (Average: 7.3 years)`, a task breakdown and
a study duration, on 7 slides across 3 decks. They are always set as type on a study-setup card,
never plotted. `never-list.md` entry 3 has the full enumeration and the searches. *Results*
themselves are carried entirely by participant quotes; Luminate says so in the corner of 34 and
35: "* Please read our paper for detailed results".

---

## Titles and band labels

**Most slides carry no title.** In Luminate at least 25 of 55 have no title element of any kind;
across the corpus the pattern holds wherever a figure or a screenshot is doing the work.
**(observed)**

**Where a title exists it is centred, bold, black, at the top** (Luminate 9, 13, 34–44, 46–47;
Sensecape 23, 24, 30; KAIST 44, 45; job talk 57, 58, 132). Not left-aligned, not in a coloured
bar. **(observed)**

**The band label is the substitute for a title on any image slide**, and it is in all four decks:
a solid grey / near-black rectangle carrying white text, dropped wherever the image is empty.
Luminate 3, 9, 13, 20, 22–32; KAIST 4, 6, 7, 8; job talk 5, 12–14, 59–60, 91–93, 140–141. In the
talk register it is often translucent over a photograph rather than opaque. **(observed)**

**The chapter card is the talk register's replacement for a section divider.** Luminate and
Sensecape use a bare centred word on white (Luminate 33, 45; Sensecape 25). KAIST and the job
talk instead show the three "spaces" with the current one black and the others greyed, under a
boxed label — `Interaction`, `Interface & Interaction`, `Interface Design`, `Design Concept`
(KAIST 17, 46, 47, 76, 77, 118; job talk 30, 61, 62, 94, 95, 142). **(observed)**

---

## Colour

**Where colour is spent, in one sentence: almost nowhere, and mostly on borrowed pixels.**
The audit gives **neutral 91.3% / chromatic 8.7%** over four decks. Per deck (**computed here**,
running the audit's own classifier deck by deck): Luminate 90.8 / 9.2, Sensecape 92.6 / 7.4,
KAIST 92.8 / 7.2, job talk 89.9 / 10.1.

### The dark slate is borrowed UI chrome. It is not his accent.

The audit's top two rows — `#303040` at 14.5% and `#404050` at 14.4% of all chromatic pixels —
are the flat fills of a dark chat interface inside screenshots, and they are extraordinarily
concentrated. **Computed here**, tallying pixels falling in those two bins:

- **18 slides of 365 (4.9%) account for 96% of all slate-bin pixels in the corpus.** Only 66
  slides carry any at all.
- On those 18, the slate covers **22 – 95% of the whole slide** — the signature of a full-bleed
  or half-bleed screenshot, not of an accent.
- At true colour (1/8 nearest-neighbour subsample, so no resampling blur invents values) the
  bins resolve to **two flat fills**, `#343441` and `#444554` (with `#333441`, a one-step variant
  of the first, in the anthology decks). Those account for **99.6% of Luminate's, 94.5% of
  Sensecape's, 92.9% of KAIST's and 91.7% of the job talk's** slate pixels. Two or three flat
  values over enormous areas is a UI fill, not drawn artwork.
- Visually: those 18 slides are Luminate 14, 15, 48, 49, 50; Sensecape 6, 8, 10, 12;
  KAIST 32, 33, 52, 54, 56, 58; job talk 45, 46, 67, 69, 71, 73 — every one of them a capture of
  the same dark ChatGPT-style window. And they are only **six distinct designs**, repeated across
  the anthology decks.

**Remove those slides and the colour table inverts** (**computed here**, same classifier):

| Deck | Top chromatic colour, all slides | Top chromatic colour, minus the dark-UI slides | Chromatic share after |
|---|---|---|---:|
| Luminate | `#303040` 49.7% | `#d0d0a0` 16.4% (warm amber family) | 4.5% |
| Sensecape | `#404050` 57.5% | `#c0d0e0` 2.5% (the canvas blue) | **1.2%** |
| KAIST | `#404050` 16.8% | `#f0f090` 3.1% (the yellow cone) | 5.4% |
| Job talk | `#404050` 10.1% | `#304050` 3.3% (the dark band over photos) | 8.7% |

Sensecape's chromatic share collapses from 7.4% to **1.2%** on removing four slides. That deck is
effectively black and white; what colour the audit saw was somebody else's product.

**Verdict: the dark slate is contamination, and the previous pass was right.** The objection that
four independent talks would not share one tool's chrome does not hold, because **the four talks
are not independent** — KAIST and the job talk contain the Sensecape and Luminate slides
themselves. Six screenshots, reused, produce both of the audit's top rows.

**A caution that is not contamination.** `#304050` / `#203040` survive the removal in the job
talk at 3.3% / 2.5%. Those are his own **dark translucent bands** laid over photographs and
generated images (job talk 59, 60, 91, 92, 93, 140, 141; KAIST 4–8). Do not sweep them out with
the screenshots — they are a real, deliberate device.

### What the accent colours actually are

- **Luminate: one warm amber/cream family** (`#d0d0a0`, `#f0e0b0`, `#f0f0b0`, `#e0d0a0`,
  `#e0e0a0` — 16.4 / 5.8 / 5.5 / 3.4 / 2.8% of chromatic pixels with the screenshots removed).
  It is the cone of attention, the filled design-space plane, and the Luminate mark
  (7, 8, 11, 12, 22, 53, 54). **(computed here + observed)**
- **Luminate: red and blue as the argument's two words.** Red marks the problem (`Fixation` —
  7, 9, 11, 12, 13, 34, 35, 38, 40); blue marks the good thing (`Design Space Thinking` — 8, 9,
  12, 13, 34, 35, 39, 40, 52). Once a term has a colour it keeps it, and on slide 8 the switch is
  staged as a strike-through of the red word replaced by the blue one. They never reach the top
  of the audit's table, which is the point: they are spent a word at a time. **(observed)**
- **KAIST: the yellow cone** (`#f0f090`, 3.1%) plus the blue→magenta headline ramp.
- **Job talk: dark translucent bands, a pale blue** (`#c0e0f0`, 2.5% — the `range` / `depth`
  highlight chips on 24–28, 146–150) **and orange/coral** on the load-bearing term (20, 21).
- **Sensecape: essentially none.** Black, white, one blue for a marked word (`Complex Systems`,
  29, 30), and the blue→magenta wordmark (17).

**The wordmark gradient is a repeated device**, not a one-off: Sensecape's logotype (17), the same
logotype re-used in KAIST 63 and job talk 78, and KAIST's `amplify our mind` (9, 10). Gradients
as *illustration and type fill* are allowed; gradients as *background* appear nowhere.
**(observed)**

---

## The emphasis vocabulary

Per-deck presence, **(observed)**:

| Device | Lum | Sen | KAIST | Job |
|---|:--:|:--:|:--:|:--:|
| Greying back what has already been explained | ✓ | ✓ | ✓ | ✓ |
| Dimming the whole previous slide and laying a question over it | ✓ | ✓ | ✓ | ✓ |
| Inverted emphasis in a quote (context set back, phrase pushed forward) | ✓ | ✓ | ✓ | ✓ |
| Solid band behind white text, dropped on an image | ✓ | – | ✓ | ✓ |
| A large ✗ drawn onto the diagram instead of written | ✓ | – | ✓ | ✓ |
| Colour on two or three words of a set line | ✓ | ✓ | ✓ | ✓ |
| Marker/highlighter underline | ✓ | – | – | ✓ (143) |
| Rough-bordered box around the thing being returned to | ✓ | – | – | – |
| Strike-through replacement of one concept by another | ✓ | – | – | – |
| Hand-drawn arrow with a handwritten label | ✓ | – | – | ✓ (7, 23) |

**Four devices are in all four decks** — greying back, dimming the stage under a question,
inverted emphasis in a quote, and colour on two or three words of a set line. Two more are in
three of four (the band label and the large ✗, both absent from Sensecape). The rough-bordered
box and the strike-through replacement are Luminate's alone, and the handwriting survives into
exactly two job-talk slides (7 and 23, where 23 also carries Korean annotations in highlight
chips).

---

## Persistent chrome

The previous pass recorded "never put persistent chrome on every slide". That is false for the
talk register:

- **The icon rail** — five line icons down the right edge, current one boxed — on 24 / 126 KAIST
  and 30 / 152 job-talk slides, and on zero Luminate or Sensecape slides. It appears only on the
  frame. **(computed here)**
- **A slide number** on 173 / 365 slides, corpus-wide. **(computed here)**

So it is not that he refuses chrome; it is that chrome belongs to the talk's own frame and is
switched off inside the material the frame is carrying.

---

## What I am least sure of

1. **Whether "two registers" is a real distinction at all.** This is the most load-bearing
   uncertainty in the set, and two facts make it worse rather than better.

   **The genre reading does not hold.** Luminate and Sensecape are *both* 15-minute conference
   paper talks, and they land on opposite sides of the split — Luminate rough, hand-drawn,
   cartooned; Sensecape clean, grotesque-only, line-iconed. So "conference paper talk vs. long
   first-person talk" cannot be what separates them.

   **The chronological reading does not hold either.** Sensecape is UIST'23 and Luminate is
   CHI'24, so the order runs clean (Sensecape) → rough (Luminate) → clean (KAIST, job talk). That
   is not monotonic, so "his taste changed over time" does not order the decks either.

   What is left is that the Luminate look may be a one-deck experiment, or may be reserved for
   some property of the material I cannot see from the files. **One sentence from Sangho settles
   it**, and until he supplies it, treat "register" as a label for what I observed and never as a
   reason to believe a shape generalises.
2. **My archetype boundaries in the anthology decks.** KAIST and the job talk contain reused
   material, and I classified reused slides in the deck they appear in, so a per-deck count
   partly measures *how much was reused*, not *what he chooses*. See `archetypes.md`.
3. **The `#304050` / `#203040` reading as "his own dark bands".** I am confident they are not the
   ChatGPT screenshots, because they survive removing those slides; I am reading them as the
   translucent bands over photographs from looking at the slides, and I have not measured that
   directly.
4. **The handwriting face's identity**, still. It is Luminate-wide and reaches exactly two
   job-talk slides. It cannot be named from raster.
5. **Whether the rough stroke was drawn or bought.** The redraw for KAIST/job talk proves the
   roughness is a per-talk choice; it does not say who made the rough version.
