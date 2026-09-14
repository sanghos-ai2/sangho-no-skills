# Never list

**One entry here is confirmed. Every other entry is a hypothesis, and four of the previous
pass's eleven candidates are now dead.**

The confirmed entry came from Sangho. The rest are *inferred from absence*, which is the weakest
kind of evidence there is — but the evidence base is now **four decks, 365 slides** rather than
one deck of 55, and that is enough to kill several candidates outright. Each entry states what I
checked and against how many slides, so Sangho can reject it on one counter-example.

**Only Sangho can promote an entry.** Nothing marked `UNCONFIRMED` should reach the skill as a
rule.

---

## Read this first: what changed on four decks

Four candidates that survived Luminate are **false across the corpus** and have been moved to
"Dead" below: never use bullets, never use clip art or a stock icon set, never lay out a
three-column feature grid, never put persistent chrome on every slide. A fifth — never end on a
summary — is false as stated and survives only in a narrower form.

The previous pass's two **corrections** (gradients and drop shadows are used, just not as chrome)
both hold on four decks and are kept.

Entries are renumbered, because four were removed. The mapping from the previous pass is:
old 3 → new 2, old 8 → new 3, old 11 → new 4, old 5 → new 5, old 6 → new 6, old 12 → new 7,
old 9 → new 8; old 2, 4, 7 and 10 are in "Dead".

---

## Confirmed

### 1. Never use the design skill's default aesthetic.

*— Sangho Suh, 2026-09-13.*

> Recorded wording in `controller-findings.md` is *"I would never try to utilize the default
> Claude design."* Both are here because they are not identical and the difference may matter:
> the first is a rule about a skill's output, the second is about a house style. Sangho should
> keep whichever he meant.

---

## Candidates that survived four decks (all `UNCONFIRMED`)

### 2. Never put a title on a slide that does not need one. `UNCONFIRMED` — strengthened

**What I checked.** All 365 slides for a title element of any kind.

**Result.** The majority of slides in every deck carry no title. Where a figure or a screenshot
is doing the work there is no title at all — Luminate 6–8, 10–12, 14–17, 23–32, 48–50; Sensecape
3–6, 8, 11–16, 18–22; KAIST 11–16, 23–31, 85–93; job talk 24–30, 36–44, 103–110. Where a title
does exist it is centred, bold, black, at the top (Luminate 9, 13, 34–44; Sensecape 23, 24, 30;
KAIST 44, 45; job talk 57, 58, 132).

**Note the inversion.** This is not "never use titles". The rule is against the *default* — a
title applied because the template has a slot for one. On image slides the substitute is a band
label dropped wherever the image is empty, which names the beat without claiming the top of the
slide, and that device is in all four decks.

---

### 3. Never put a results chart in the talk. `UNCONFIRMED` — much stronger than before

**What I checked.** All 365 slides for a bar chart, line graph, scatter of results, or table of
statistics. Then, separately, I searched every non-figure text span in the corpus for
statistic-shaped tokens (`p <`, `p =`, `M =`, `SD =`, `n = <digit>`, `<digits>%`, "mean",
"median", "significant").

**Result.** **0 of 365 slides**, across five studies in four decks. The token search returns
**four hits, all of them the word "mean" in the sentence "What does *amplifying our mind* mean?"**
(KAIST 10; job talk 21, 22, 23). No p-value, no standard deviation, no sample-size statement, no
percentage appears anywhere in the corpus's slide copy.

Findings are carried entirely by participant quotes (17 quote cards) and by Takeaway cards that
state a claim and then quote somebody. Luminate says so out loud in the corner of 34 and 35:
"* Please read our paper for detailed results".

**This was the candidate the previous pass most expected the job talk to kill.** It did not. The
job talk is 152 slides long, covers three papers and five studies, and contains no chart.

**What could still be wrong.** Every study in this corpus is qualitative or mixed with a
qualitative headline. A deck reporting a controlled quantitative result may look completely
different, and none is in the canon.

---

### 4. Never use stock photography of generic people or places. `UNCONFIRMED` — narrowed

**What I checked.** All 365 slides for photographic imagery, and where it came from.

**Result.** Photography is common in the talk register and almost absent from the conference
register. What it is, though, is consistent: **specific, named, or personal**. His own lab groups
(KAIST 1; job talk 5), portraits of the people he is quoting (Pauling, Griffith, Buxton, Bret
Victor, Knuth), his own headshot, his own photographs of Griffith Observatory (KAIST 4, 5;
job talk 12, 13), an archival photograph of Mount Wilson with its source URL lettered along the
bottom edge (KAIST 6; job talk 14).

**Two counter-examples, and they are why this is narrowed rather than promoted.** KAIST 79 /
job talk 97 is a generic stock-looking photograph of two children at a laptop — used, notably, as
the setup for a rhetorical question about it ("Does anyone find anything weird about this
picture?", KAIST 79's note). And job talk 22/23 use found footage of a telescope and a microscope,
credited by channel and URL in the presenter notes.

**So the defensible form is narrower**: no generic photography used *decoratively*. Every
photograph in the corpus is either of a specific person or place, or is the thing being talked
about. **(observed)**

---

### 5. Never use a gradient as a background. `UNCONFIRMED` — the previous pass's correction holds

**What I checked.** All 365 slides.

**Result.** **0 of 365 backgrounds are gradients.** Grounds are flat white (263 slides), flat
cream `#f0eade` (61), flat black (23), or a flat dark fill — a dark-UI screenshot or a dimmed
stage (14); 4 slides are photo-dominant with no flat ground (**computed here**; modal colour of an
80 × 45 box-filtered slide).

**The seeded hypothesis "never use gradients" is false, and more so than the previous pass
thought.** Gradients are used as *illustration and type fill* in three of the four decks: the
Luminate mark and its cone of attention (Luminate 7, 8, 22, 53, 54); the **Sensecape wordmark**, a
blue→magenta ramp (Sensecape 17, reused at KAIST 63 and job talk 78); and the blue→magenta ramp
across headline words and defined terms throughout KAIST and the job talk (KAIST 9, 10;
job talk 103–109, 112, 124–128, 130–132). The absence is specifically of gradients as *chrome*.

---

### 6. Never frame a screenshot as a floating card. `UNCONFIRMED` — the previous pass's correction holds

**What I checked.** All interface captures in the corpus.

**Result.** **The broad form — "never use a drop shadow" — is false.** Drop shadows are used
deliberately and repeatedly on the conceptual diagrams: the design-space parallelogram carries one
in all four decks (Luminate 7, 8, 9, 11, 12, 16, 17; KAIST 26, 29, 30; job talk 39, 42, 43), and
the three-spaces icon tiles carry one on every chapter card.

**The narrow form holds.** No interface capture anywhere in the corpus is presented as a framed,
rounded, lifted card. Captures run to the slide edges or occupy a clean half — Luminate 23–32,
48–50; Sensecape 3–6, 8, 18–22; KAIST 41, 49–52, 54, 56, 64–68, 104–105, 117; job talk 45–46, 54,
64–67, 69, 71, 79–83, 122–123, 136. Only the narrow form should be promoted.

---

### 7. Never let a colour mean two things within one deck. `UNCONFIRMED` — holds, but the palette changes between decks

**What I checked.** Every appearance of the accent colours in each deck.

**Result.** Within a deck the assignment is stable. Luminate: red is always `Fixation`, blue is
always `Design Space Thinking`, across 7, 8, 9, 11, 12, 13, 34, 35, 38, 39, 40, 52 — and on slide 8
the switch between them is staged as a strike-through of the red word replaced by the blue one.
Sensecape: one blue, only ever on the marked half of a two-word phrase (29, 30). KAIST and the
job talk: a blue→magenta ramp is used only on the terms being defined.

**But the mapping resets between decks.** Luminate's red = problem / blue = good does not carry
into KAIST or the job talk, which use the same blue for a *defined term* regardless of whether it
is good or bad, and the job talk uses orange for the term in its frame sections and blue inside
CodeToon. So the rule is **within-deck consistency**, not a fixed palette semantics.

This is a "never" phrased from a positive habit, which is the shakiest kind of inference here, but
it held in four decks and it is easy for Sangho to refute in one sentence.

---

### 8. Never end the talk on a summary slide. `UNCONFIRMED` — narrowed; the broad form is dead

**What I checked.** All 365 slides for a takeaways / conclusion / contributions-recap slide, and
separately what each deck's last content slide is.

**Result, broad form: false.** Explicit summary slides exist — `Takeaway (1)` / `Takeaway (2)`
(KAIST 44, 45; job talk 57, 58), `Takeaways` (KAIST 114; job talk 132), `Limitations`
(job talk 133), and the `Takeaway & Future Work` divider (Sensecape 25). Seven Takeaway cards
across two decks. **The previous pass's "0 of 55" was a Luminate fact, not a corpus fact.**

**Result, narrow form: holds.** **No deck in the corpus ends on one.** Luminate ends on two
handwritten open questions → contact card → "Questions?" → blackout. Sensecape ends on a widening
statement → its own title card. KAIST ends on the metaphor redrawn → contact card → blackout.
Job talk ends the same way. The takeaway lands *at the close of each paper segment*, mid-talk;
the talk itself closes on a question or on contact details.

Only the narrow form should be promoted, and it should be worded as a placement rule, not an
absence rule.

---

## Dead — false across four decks

These were reasonable inferences from one deck and are now refuted. Recorded so nobody re-derives
them.

### ~~Never use bullet lists as body text.~~ — **false, barely**

Searched every text span in the corpus for `• ‣ ▪ ◦ · ● ○ – — › »` used as a list marker
(**computed here**). Result: **3 slides of 365** — KAIST 114 and job talk 132, 133, all of them
`Takeaways` / `Limitations` cards using `•`. Everything else that could have been a list is set as
a bare stack of lines with no marker (Luminate 36 and 37, KAIST 115) or numbered by content
("**Q1.** …", "**Q2.** …").

The honest statement is not a never but a **conditional**: bullets appear on 0.8% of the corpus
and only ever on a Takeaway or Limitations card. Phrase it that way or drop it.

### ~~Never use clip art or a stock icon set.~~ — **false**

Flat and line vector icons used as nouns appear throughout the talk register: the abstract-concept
icons on Sensecape 26/27; the clipboard/person process icons on KAIST 42 and job talk 55; **flat
orange-and-slate stock people** on KAIST 43 and job talk 56; the bar-chart / brain / Σ / padlock
`Opportunities` grid on KAIST 115 and job talk 134, 135; the `</>` window, book and comic icons on
job talk 98, 100, 101, 124, 129; and the five-icon rail itself on 54 slides.

What is true is the *Luminate-specific* version: in Luminate all illustration belongs to one
consistent hand-drawn black-and-white cartoon family and no stock icon appears. That is a fact
about the conference register, not a rule.

### ~~Never lay out a three-column feature grid.~~ — **false**

The `Design Space | Information Space | Representation Space` row is exactly a three-column
labelled feature grid, and it is the corpus's most-repeated single composition (KAIST 16, 17, 46,
47, 76, 77, 118; job talk 29, 30, 61, 62, 94, 95, 142). Plus 2 × 2 grids on KAIST 115 and job
talk 99, 134, 135, and a three-labelled-question row on KAIST 119 and job talk 143–145.

### ~~Never put persistent chrome on every slide.~~ — **false**

A slide number appears on **173 of 365** slides (**computed here**: a bare integer span equal to
that slide's own index; 173 matches, 0 mismatches). A five-icon rail runs down the right edge of
**24 of 126** KAIST and **30 of 152** job-talk slides (**computed here**).

The true pattern is more interesting than the rule it replaces: **chrome belongs to the talk's own
frame and is switched off inside the material the frame carries.** The rail appears on the
opening, the chapter joins and the close, and on none of the embedded conference-talk segments.

---

## Things I expected to find as nevers and did not

- **"Never use dark slides."** False. 36 of 365 slides are dark-dominant (**computed here**), and
  the blackout and the dimmed stage are deliberate devices in all four decks.
- **"Never use more than two colours."** Roughly true per deck, but local pairs are allowed —
  green/salmon on Luminate 46/47, orange/teal on job talk 7.
- **"Never use a dense slide."** False. Luminate 21, KAIST 39 and job talk 52 reproduce the
  paper's method figure at full width; job talk 110 and 111 carry a twelve-box abstraction grid.
  One very dense slide is permitted when it earns its place.
- **"Never use AI-generated imagery."** False, and the opposite of a never — the job talk uses it
  on eight slides as full-bleed backdrops (11, 59, 60, 91, 92, 93, 140, 141) plus KAIST 3. One of
  those is confirmed by the deck itself: job talk 93's presenter note is the generation's own
  description text. The other eight I am reading from style, not from a record.
- **"Never reuse a slide between talks."** Emphatically false. 72–86% of the two long decks are
  slides carried over from earlier talks (**computed here**). Reuse is the working method, not a
  lapse.
