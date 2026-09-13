# Never list — first pass

**One entry here is confirmed. Every other entry is a hypothesis.**

The confirmed entry came from Sangho. The rest are *inferred from absence* over a single deck
(Luminate @ CHI'24, 55 slides), which is the weakest kind of evidence there is: a pattern absent
from one talk may be absent because the talk did not need it. Each candidate states exactly what
I checked and against how many slides, so Sangho can reject it on one counter-example.

**Only Sangho can promote an entry.** Nothing marked `UNCONFIRMED` should reach the skill as a
rule.

---

## Confirmed

### 1. Never use the design skill's default aesthetic.

*— Sangho Suh, 2026-09-13.*

> Recorded wording in `controller-findings.md` is *"I would never try to utilize the default
> Claude design."* Both are here because they are not identical and the difference may matter:
> the first is a rule about a skill's output, the second is about a house style. Sangho should
> keep whichever he meant.

---

## Candidates — inferred from absence (all `UNCONFIRMED`)

### 2. Never use bullet lists as body text. `UNCONFIRMED`

**What I checked.** All 55 slides, both visually and by searching every text span in the manifest
for `•  ‣  ▪  ◦  ·  –  —  ›` used as a list marker, after excluding the printed-presenter-note
spans.

**Result.** **0 of 55.** The only `*` characters in slide copy are the co-first-author marker
(slide 2) and a footnote asterisk (34, 35). Where a list genuinely exists it is set as a bare
stack of lines with no marker — slide 37 ("4 copywriting / 4 short story / 2 email / …"), slide 36
(bold label, grey detail line beneath). Structured questions are numbered by *content*
("**Q1.** …", "**Q2.** …"), not by a glyph.

**Why this could still be wrong.** The Keynote White theme's masters include "Title & Bullets",
"Bullets", and "Title, Bullets & Photo" (`controller-findings`). He started from a theme built
around bullets and used none. That is suggestive, but it is one talk.

---

### 3. Never put a title on a slide that does not need one. `UNCONFIRMED`

**What I checked.** All 55 slides for a title element of any kind.

**Result.** **At least 25 of 55 carry no title at all** (1, 6, 7, 8, 10, 11, 12, 14, 15, 16, 17,
23–32, 48, 49, 50, 55), plus several cards (2, 3, 5, 18, 53, 54). On image slides the substitute
is a solid band label dropped wherever the screenshot is empty — it names the beat without
claiming the top of the slide.

**Note the inversion.** This is not "never use titles" — where a title exists it is centred, bold,
black and at the top (9, 13, 34–44, 46, 47, 51). The rule is against the *default*: a title applied
because the template has a slot for one.

---

### 4. Never use clip art or a stock icon set. `UNCONFIRMED`

**What I checked.** All 55 slides for flat multicolour vector icons (gear, lightbulb, rocket,
checkmark) used as decoration or as a stand-in for a noun.

**Result.** **0 of 55 used decoratively.** All illustration in the deck belongs to one consistent
black-and-white hand-drawn cartoon family (the person watching the design space, 7/8/11/12; the
study populations, 36/37/42; the participant portraits, 38/39/43/44) plus one drawn speech-bubble
glyph for "LLMs" (9–13).

**Weakly evidenced — read this before promoting it.** Slide 3 carries two small illustrations (a
figure and a lightbulb/monitor) among the reproduced prior-work screenshots. I believe they are
part of a reproduced figure rather than decoration Sangho added, but I cannot prove that from the
raster. If they are his, this candidate is wrong as stated and should be narrowed to "never use an
icon as a substitute for a noun you could draw."

---

### 5. Never use a gradient as a background. `UNCONFIRMED`

**What I checked.** All 55 slides.

**Result.** **0 of 55 backgrounds are gradients.** Backgrounds are flat white (47 of 55) or flat
black (8 of 55).

**Important correction to the seeded hypothesis.** "Never use gradients" is **false** for this
deck. Gradients are used, three times, always as *illustration*: the cone of attention on 4, the
filled design-space plane on 8, the Luminate mark on 22/53/54. The absence is specifically of
gradients as chrome.

---

### 6. Never use a drop shadow to make a flat card look raised. `UNCONFIRMED` — **weak, likely wrong as stated**

**What I checked.** All 55 slides.

**Result.** Drop shadows **are present**: the design-space parallelogram carries a soft shadow on
7, 8, 9, 11, 12, 16, 17. What is absent is a shadow on a *screenshot* — interface captures are
full-bleed with no frame, no rounded corner, no lift (23–32, 48–50).

I am recording this rather than deleting it because the narrower form — "never frame a screenshot
as a floating card" — held on all 13 interface slides. The broad form does not hold and should not
be promoted.

---

### 7. Never lay out a three-column feature grid. `UNCONFIRMED`

**What I checked.** All 55 slides for a division into three (or more) equal labelled columns —
the "three benefits / three features" shape.

**Result.** **0 of 55.** Where two things are compared they are given two halves and an explicit
connector (14, 15, 51). Where many things are shown they are placed by meaning, not by grid (3,
18, 21).

---

### 8. Never put a results chart in the talk. `UNCONFIRMED` — **most likely to be Luminate-specific**

**What I checked.** All 55 slides for any bar chart, line graph, scatter of results, or table of
statistics.

**Result.** **0 of 55**, across a 14-participant user study *and* an 8-participant deployment
study. Findings are carried entirely by participant quotes (38, 39, 43, 44), and the deck says so:
a grey line in the corner of 34 and 35 reads "* Please read our paper for detailed results."

**Why this may not be taste.** Both studies are qualitative; there may have been nothing worth
plotting. Check against the job talk before believing it.

---

### 9. Never end on a summary or takeaways slide. `UNCONFIRMED`

**What I checked.** All 55 slides for a conclusion, contributions recap, or takeaways slide.

**Result.** **0 of 55.** The last content slide (52) is two open questions in handwriting, laid
over the dimmed future-work slide. After it: a QR/contact card, "Questions?", and a blackout.

**Why this may not be taste.** CHI talk format pushes hard toward ending on the QR code. Very
likely to differ in the job talk, which has a different job.

---

### 10. Never put persistent chrome on every slide. `UNCONFIRMED`

**What I checked.** All 55 slides for a repeated logo, footer, progress bar, section indicator,
or running header.

**Result.** **0 of 55** carry any of those. Institution and venue marks appear on exactly three
slides (2, 53, 54). The only repeating element is a small grey page number. Structural
re-orientation is done instead by *returning to an unchanged card* — the same rough-bordered
research-question box shown four times (34, 35, 40, 41).

---

### 11. Never use stock photography. `UNCONFIRMED`

**What I checked.** All 55 slides for photographic imagery.

**Result.** Photographs appear on **3 of 55**, and all three are specific people: Linus Pauling
(5) and the team's own headshots (53, 54). No generic photography of any kind — no people at
laptops, no abstract textures, no landscape.

---

### 12. Never let a colour mean two things. `UNCONFIRMED`

**What I checked.** Every appearance of red and blue across the 55 slides.

**Result.** Red marks the problem — "Fixation" — on 7, 9, 11, 12, 13, 34, 35, 38, 40. Blue marks
the good thing — "Design Space Thinking" — on 8, 9, 12, 13, 34, 35, 39, 40, 52, and "creative" on
4. I found **no slide where either colour is used for anything else**. On slide 8 the switch
between the two is staged as a strike-through of the red word and its replacement by the blue one.

This is a "never" phrased from a positive habit, so it is the shakiest kind of inference here —
but it held across the whole deck and it is easy for Sangho to refute in one sentence.

---

## Things I expected to find as nevers and did not

Recorded so the next pass does not re-derive them:

- **"Never use dark slides."** False. 8 of 55 are dark-dominant, and the black stage is a deliberate
  device on 4 and 19.
- **"Never use more than two colours."** Roughly true of the deck's system, but green and salmon
  appear as a local pair on 46/47 and green/amber marker underlines on 44. Local palettes are
  allowed.
- **"Never use a dense slide."** False. Slide 21 reproduces the paper's method figure at full width
  and is the densest thing in the deck by a wide margin. The audit's maximum of **321 words on one
  slide** (1 deck) is consistent with a deck that permits one very dense slide when it is earning
  its place.
