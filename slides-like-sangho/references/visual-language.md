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
(box-filtered, mean absolute RGB difference), **computed here** — and, since this review round,
generated into [`tools/slide-audit.md`](../../tools/slide-audit.md)'s header too, so the evidence
base this document cites carries the same caveat this document opens with. The audit's union-find
over the same test puts the corpus at **170 distinct designs, not 365 slides**:

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
ad hoc. A 4- or 5-step scale is therefore an **imposition** — but it is one Sangho asked for
(*"yes, please derive a scale"*, 2026-09-13, in answer to whether a skill should derive one or
match sizes case by case from the nearest archetype). The derived scale is below, under
"A derived type scale"; read it as a working default, not as a description of these four decks.

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

## A derived type scale

The section above says these decks contain no scale. This section imposes one anyway, because a
skill has to put a number on a hero question and cannot ask. **Sangho chose this**
(*"yes, please derive a scale"*) over the alternative of matching sizes case by case from the
nearest archetype. What follows is therefore a derived default with its own error bars, not a
finding about how he sets type.

### Method, and what was excluded (computed here)

Every one of the **1,147 spans** in the corpus was given a **role** — by reading the slide it sits
on, not by its size — from: hero, section, deck title, slide title, quote, body, band label,
figure label, caption/credit, slide number. Sizes were then measured per role. All 365 slides were
read for this (31 contact sheets at 620 px per cell, plus individual slides at full resolution
where a call was close).

**147 spans (13%) were excluded before any of it**, on 55 slides and 18 distinct designs:

- **Text inside a pasted screenshot — 104 spans.** 21.0 pt (58 spans: the ChatGPT response bodies
  and prompt fields), 24.0 pt UI chrome (45 spans: the `SA` avatar chip, `Regenerate`, `Explore`,
  `1. 2. 3.`, `> <`), and 25.0 pt (1 span, the story text inside a drawn page on Luminate 51).
- **Code specimens set inside his own figures — 43 spans**, at 15.0, 19.0, 27.0, 29.0, 33.0, 41.0,
  53.0 and 73.0 pt (the `while (dormammu_refuses)` listings on KAIST 88–95 / job talk 106–113, and
  the `x = 10 / if x == 10:` listing on KAIST 100–110 / job talk 118–128). These are his, but they
  are code specimens, not slide type, and their size tracks how much code had to fit.

Both exclusions were already flagged as traps in earlier rounds: the 21.0 pt band is a screenshot,
and the 24.0 pt band is 55 slide numbers plus 1,204 words of figure text. **The 24.0 pt band is
not excluded wholesale** — 22 of its spans are his own greyed-back ladder column labels (KAIST
88–95, job talk 106–113) and the `… … … …` ellipsis row on Sensecape 16/17 and its twins, and
those are kept as figure labels.

That leaves **1,000 authored spans on 345 of the 365 slides**, and **475 distinct
(design, size) pairs** once the 170-design deduplication from the top of this document is applied.

### Role → size, measured

Design counts use the same MAE < 3 grouping as everywhere else in this document, which merges
**build steps of one figure** as well as cross-deck twins — so "designs" here means distinct
pictures, not distinct slides.

| Role | Spans | Slides | Designs | Distinct sizes | Median pt | Where it actually sits |
|---|---:|---:|---:|---:|---:|---|
| Slide number | 173 | 173 | 97 | **2** | 22 | 22 pt everywhere except Luminate, which uses 24 |
| Slide title | 74 | 74 | 39 | 14 | 84 | **84 pt** — 52 of 74 spans, 20 designs |
| Section / chapter name | 35 | 35 | 20 | 6 | 100 | **bimodal**: 112 pt (Luminate) vs 74 pt (KAIST + job talk) |
| Hero (the slide's one line) | 53 | 52 | 25 | 15 | 84 | 66 – 137, clustered 78 – 112 |
| Band label on an image | 43 | 29 | 23 | 12 | 75 | 45 – 128, plus a 244 pt drop cap |
| Quote | 39 | 35 | 22 | **20** | 79 | 38 – 119 — very nearly one size per quote |
| Body line | 39 | 26 | 21 | 16 | 53 | 30 – 78 |
| Figure label | 440 | 197 | 84 | **35** | 45 | 24 – 159, modes at 30 / 36 / 45 / 50 / 51 / 80 |
| Caption / credit | 93 | 33 | 25 | 15 | 47.5 | 31.7 and 47.5 are the title-card apparatus (31 spans each) |
| Deck / paper title | 11 | 11 | 9 | 6 | 79 | 59.8 – 98, one per title card |

**Two roles have a real size and the rest do not.** The slide number is 22 pt (or 24 in Luminate)
and nothing else. The slide title is **84 pt** in three decks of four — Sensecape 2/2, KAIST 23/28,
job talk 27/35 — and **0 of Luminate's 9 title spans are at 84**; Luminate titles are 59, 60, 72.8,
75, 86 and 103 pt, one size each. That is the sharpest caveat on the scale below.

### The scale

Five steps. The point values are the observed modes, not a ratio series — the ratios between them
are 1.50, 1.39, 1.68, 1.33, and the two geometric ladders I tested fitted the corpus no better
(a ×4/3 ladder from 84 pt scored 47.9% at ±8% against this one's 50.6%; a ×1.5 ladder, 39.6%).

| Step | pt | What it sets | Two real examples |
|---|---:|---|---|
| **Display** | **112** | a section's name; the contribution's name; a question that is the whole slide | `Evaluation` (Luminate 33, 34, 35, 40, 41); `Luminate` (Luminate 22, KAIST 40, job talk 53) |
| **Title** | **84** | the slide's title; a claim card's single line | `Changing Levels of Abstraction for Learning` (KAIST 85–91, job talk 103–109); `How Do We Make Connections Clear?` (KAIST 106–110, job talk 124–128) |
| **Support** | **50** | a body line; the larger labels in a diagram; a study fact | `Design Space` + the six `idea` dots (Luminate 6, KAIST 23, job talk 36); `Single-Output` / `Multi-Output` (Luminate 16, 17, 19; KAIST 34, 35, 37) |
| **Label** | **36** | labels inside a dense diagram; affiliations on a title card | `Thinkable Territory` (KAIST 11, 12, 13, 14, 15); `Knowledge Territory / Problem Territory / Solution Territory` (KAIST 120–124, job talk 146–150) |
| **Caption** | **24** | the slide number; a venue tag; a source URL | the slide number on 173 slides; `https://huntington.org/verso/…` at 23 pt (KAIST 6, job talk 14) |

**How much of the corpus this actually covers** (computed here):

| | ±8% of a step | ±15% of a step |
|---|---:|---:|
| Authored spans (n = 1,000) | **51%** | **87%** |
| Distinct (design, size) pairs (n = 475) | **52%** | **85%** |

Per step, at ±15%, and what lands there:

| Step | Spans | Designs | Exactly on the step | Observed sizes it absorbs | Roles |
|---|---:|---:|---|---|---|
| 24 | 200 | 99 | 77 spans / 58 designs | 22, 23, 24, 27 | slide number 173, figure 22, caption 5 |
| 36 | 158 | 42 | 54 / 17 | 31.7 – 41 | figure 118, caption 34, body 3, title 2, quote 1 |
| 50 | 253 | 85 | 58 / 22 | 43 – 57 | figure 168, caption 46, body 22, band 13, quote 4 |
| 84 | 202 | 79 | 64 / 23 | 72.8 – 96 | title 59, figure 45, hero 35, band 20, quote 16, section 14, deck-title 7 |
| 112 | 54 | 34 | 17 / 13 | 98 – 128 | section 21, hero 12, title 7, quote 7, figure 4, band 2 |

Per deck, at ±15%: **Luminate 77%** (137/178 authored spans), Sensecape 97% (60/62), KAIST 87%
(283/326), job talk 89% (387/434). Luminate is the worst fit and the reason is the one named
above — it has no 84 pt title.

### What the scale cannot cover

**13% of authored spans (133 spans, 56 designs) sit more than ±15% from every step**, and the
misses are not noise:

- **The 30 pt figure-label band — 37 spans on 19 designs**, the largest off-scale cluster. Counting
  every role at 30 pt it is 22 designs, which makes it the joint-fourth most-used authored size in
  the corpus, level with 50 pt and behind only the two slide-number sizes (24 pt, 58 designs;
  22 pt, 49) and the title size (84 pt, 23). It is the small annotation inside
  a drawn figure: `prompt` (Luminate 14, 15, 19; KAIST 32, 33, 37; job talk 45, 46, 50),
  `prompt #1 prompt #2 …` (Luminate 16; KAIST 34; job talk 47), `. . .` (Luminate 10; KAIST 28;
  job talk 41). A sixth step at 30 pt would take ±15% coverage from 87% to 91% (and ±8% from 51%
  to 60%); it is left
  out because four steps plus a caption size is already the most a skill should be handed, and
  because this band is exactly where sizing is driven by fit rather than by role.
- **One-off display sizes**: the 244.1 pt drop-cap `M` of `Most-visited public observatory`
  (KAIST 4, 8; job talk 12, 16) and the 159 pt drawn `?` glyphs (KAIST 101, 102, 108; job talk 119,
  120, 126, 138). These are drawn elements, not type set to a step.
- **The 60 pt band** (18 spans, 14 designs), which serves four different roles at once — figure
  label, body line, a quote, and the `Try Luminate luminate-research.github.io` contact line
  (Luminate 53, 54).

**Two roles are genuinely sizeless and a skill should not pretend otherwise.**

- **Quotes.** 39 quote spans carry **20 distinct sizes** over 22 designs — very nearly one size per
  quote, from 38 pt (KAIST 45) to 119 pt (KAIST 113, job talk 131). The size is set by how long the
  quote is. Set a quote to fill its slide and let the size fall where it falls; the *emphasis*
  pattern (context set back, phrase pushed forward) is the portable part, not the size.
- **Figure labels.** 440 spans across **35 distinct sizes**, with real modes at 30, 36, 45, 50/51
  and 80 pt, and hardly a gap anywhere between 30 and 51. A figure's labels are sized to the figure.

**So the rule a skill should carry is: use the scale for the roles that have one — the slide
number, the title, the section name — and size quotes and figure labels to fit.** Deviating is not
a defect; on this corpus it is what he does 13% of the time by span and, in Luminate, 23%.

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

**Prior work is credited by venue tag, not by reference.** Other people's systems appear as
screenshots with the venue lettered beneath (Luminate 3, 18; KAIST 20, 36, 81; job talk 6, 33, 49,
99). **(observed)**

**An earlier draft said "there is no textual citation anywhere in the corpus's slide copy". That
is false**, and it is the same failure as the statistics claim above: an absence asserted from a
search that could not see the counter-examples. Re-measured (**computed here**), slide copy
carries **venue tags on 4 slides** — Luminate 3 (`CHI'22 UIST'23 VIS'23 DIS'23 IUI'23`),
Luminate 18 / KAIST 36 / job talk 49 (`Promptify (UIST'23)`, `PromptMagician (VIS'23)`) — and a
**source URL on 2** — KAIST 6 / job talk 14, the Mount Wilson photograph, lettered along the
bottom edge. A system name plus a parenthesised venue *is* a citation.

**What is genuinely absent is the academic apparatus**: searching slide copy for `Author et al.`,
`Author (2023)` and bracketed numbered references `[12]` returns **0 of 365** (**computed here**).
So the rule is *"no author–year and no numbered reference"* — he credits by venue tag and by URL,
in the smallest type on the slide, and never by a reference list. **(observed + computed here)**

**There is not one chart of his own results in 365 slides.** No bar chart, no line graph, no
scatter, no table of statistics — **(observed)**, across five studies. And **no inferential
statistic**: the pattern below, run case-insensitively over slide copy, returns **0 of 365**, as
does the `%` character (**computed here**).

```
\bp\s*[<=>]\s*0?\.\d|\bSD\b|\bM\s*=|\bCI\b|\bt\s*\(|\bF\s*\(|χ|\bANOVA\b|\bsignifican|\beffect size\b|\bstd\b|±
```

**The word boundaries are load-bearing and an earlier draft of this sentence dropped them when it
paraphrased the pattern in prose.** Written without them, `SD` matches inside "San Diego", `CI`
inside "San Francisco", and `t(` inside `print("true")` — 85 slides rather than 0. The pattern as
written above is the one that was run; `\bt\s*\(` alone matches 0 slides, because the character
before the `t` in `print(` is a word character and so there is no boundary there.

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

**The band label is the substitute for a title on an image slide — in three decks of four.**
A solid grey / near-black rectangle carrying white text, dropped wherever the image is empty:
Luminate 3, 9, 13, 20, 22–32; KAIST 4, 6, 7, 8; job talk 5, 12–14, 59–60, 91–93, 140–141. In
KAIST and the job talk it is often translucent over a photograph rather than opaque.
**(observed)**

**Sensecape inverts it, and the inversion is the finding.** I checked all 32 of its slides for a
solid dark rectangle carrying light type and found none — its one white-on-dark slide (9) sets the
type straight onto the dimmed screenshot with no rectangle behind it. Where it labels an image
slide it uses the opposite polarity — **black text in a white rounded box with a black border**.
It is the node box it draws on its own diagram slides (Sensecape 14, 15, 16), carried over and
laid on top of the capture on 18. So the *job* (name the beat without claiming the top of the
slide) is in all four decks and the *rendering* is not: three decks put light type on a dark
field, Sensecape puts dark type on a light one. A template that treats the dark band as universal
will apply it to an austere white-ground deck, which is the one place in this corpus it never
appears. **(observed)**

**One caution on provenance, and it is why the citation list above is short.** Sensecape also
carries a soft-shadowed white pill with **no** border — slide 19's only chip, and slide 20's —
which is the **interface's own breadcrumb** inside the screenshot, not a label Sangho added. The
bordered boxes and that pill are different objects and I count only the bordered ones. (An earlier
draft of this sentence cited 20 and 21 as well: 20 is a near-empty canvas whose only label is that
unbordered breadcrumb, and 21 carries plain unbordered canvas captions. Both were written from the
shape of the finding rather than from re-opening the slides, which in a passage about raising the
evidentiary bar would have handed a reader a false counter-example against the claim. Each of
14, 15, 16 and 18 was re-opened and checked before this list was cut to them.)

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

- **21 slides of 365 (5.8%) account for 96.9% of all slate-bin pixels in the corpus** — and the
  18 largest of those 21 carry **96.0%** on their own. Only 66 slides carry any at all.
- On the 18 largest the slate covers **22 – 95% of the whole slide** — the signature of a
  full-bleed or half-bleed screenshot, not of an accent. The remaining three (Sensecape 12,
  KAIST 58, job talk 73) carry it at 2.7% each: the same window, shown small.
- At true colour (1/8 nearest-neighbour subsample, so no resampling blur invents values) the
  bins resolve to **two flat fills**, `#343441` and `#444554` (with `#333441`, a one-step variant
  of the first, in the anthology decks). Those account for **99.6% of Luminate's, 94.5% of
  Sensecape's, 92.9% of KAIST's and 91.7% of the job talk's** slate pixels. Two or three flat
  values over enormous areas is a UI fill, not drawn artwork.
- Visually: all 21 are Luminate 14, 15, 48, 49, 50; Sensecape 6, 8, 10, 12; KAIST 32, 33, 52,
  54, 56, 58; job talk 45, 46, 67, 69, 71, 73 — every one of them a capture of the same dark
  ChatGPT-style window. And they are only **7 distinct designs** (**computed here**, grouping the
  21 at MAE < 3): three of them appear in three decks each, one in four decks and two variants
  (Sensecape 6/8 ≡ KAIST 52/54 ≡ job talk 67/69), one pair inside Luminate (48 ≡ 50), and
  Luminate 49 alone. (An earlier draft said "18 slides" in the sentence above and then named 21 —
  the 18 was the top-18 cumulative figure — and put the design count at six by eye rather than
  measuring it. Both are corrected.)

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
