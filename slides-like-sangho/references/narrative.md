# Narrative

**Evidence base: four decks, 365 slides, 180 of them carrying a presenter note**
([`tools/slide-audit.md`](../../tools/slide-audit.md), "Presenter notes").

Figures marked **(computed here)** are mine, over the `notes` field of each manifest, with the
method stated. Slide-level readings are marked **(observed)**.

---

## Read this first: the job talk has no script, and that is not what it looks like

The brief for this pass reported note coverage as Sensecape 91% / KAIST 67% / Luminate 64% /
job talk 21%, and read the spread as "conference talks are scripted, the job talk is improvised."
The coverage numbers are right. The reading is wrong, and in an interesting way.

**30 of the job talk's 32 notes contain Korean, and 29 of 32 are glossary-shaped** — lines of the
form `term - term`, e.g. *"Broader picture - 큰 그림 / Detail - 세부적인 / Levels of abstraction -
추상화 레벨/계층"* (slide 1). **(computed here**: Hangul codepoint search, plus a line-shape test
requiring ≥60% of a note's non-empty lines to match `<phrase> - <phrase>`.) The remaining three
are not narration either: slides 22 and 23 are **media attributions** (author, title, YouTube
link for the telescope and microscope footage) and slide 93 is the **generated-image record**
("Here is the image depicting a group of researchers…").

So the honest figure is: **0 of 152 job-talk slides carry a line of narration.** Its notes field
is being used for three completely different jobs — an English→Korean vocabulary crib, a media
credits ledger, and a provenance record for generated imagery. Whether that means the talk was
improvised, rehearsed from memory, or prepared for delivery in Korean is **not** something the
file can tell you, and I have not asserted one.

By contrast the other three decks' notes are unambiguously spoken narration:

> **Luminate 2** — `00:00 - 00:20 (20 s)` · "Hi, my name is Sangho. I will present Luminate on
> behalf of my co-authors, Meng Chen, Bryan Min, Toby Li, and Haijun Xia…"
>
> **KAIST 79** — `0:15 - 0:45 (30 s)` · "So, here is a photo of two kids looking at a laptop
> screen. Does anyone find anything weird about this picture? (Pause) I think it's weird that
> they are looking at this Java code and are smiling…"

---

## The source, per deck

**(computed here**, over the manifests' `notes` fields.)

| Deck | Notes | Coverage | Median words | Max | What the notes are |
|---|---:|---:|---:|---:|---|
| Sensecape | 29 | **91%** | 33 | 76 | narration |
| KAIST | 84 | 67% | 23 | 155 | narration |
| Luminate | 35 | 64% | 23 | 47 | narration, timed |
| Job talk | 32 | 21% | 12 | 78 | **not narration** — see above |

**Timing markers are a per-deck convention and the corrected numbers differ from what
`controller-findings.md` records** (which was measured on the bad export):

| Deck | Notes with a duration `(N s)` | Notes with a wall clock `mm:ss` |
|---|---:|---:|
| Luminate | 20 of 35 | 2 |
| Sensecape | 0 of 29 | 2 |
| KAIST | 28 of 84 | **33** |
| Job talk | 0 of 32 | 0 |

KAIST's clocks are not spread across the deck — they cluster on slides 78–106, the CodeToon
segment, which is also where its notes are longest (median 33 words over slides 51–75). That is
the section he timed most carefully. **(computed here)**

**A note belongs to a beat, not to a slide** — in the three decks that have narration.
Verbatim-identical notes are repeated across *consecutive* slides. The lists are **complete**, so
the slide counts add up to the percentages: Luminate 26/27/28 and 53/54 (5 slides); Sensecape
3/4/5, 13/14/15, 19/20/21/22 and 28/29/30 (13); KAIST 9/10, 49/50/51, 59/60/61, 65/66/67/68 and
71/72/73 (15). That is **14% of Luminate's notes-bearing slides, 45% of Sensecape's and 18% of
KAIST's** (5/35, 13/29, 15/84) — where a slide is a
build step or a return to something already said, the note is repeated or omitted rather than
rewritten. **(computed here)**

**The job talk is deliberately excluded from that figure.** Its notes repeat too (14 of 32 slides
under any-duplicate matching, 9 under consecutive-only), but a repeated Korean glossary block is
not a beat narrated once — it is the same vocabulary list pasted onto adjacent slides. Counting it
here would use the glossary as evidence of a narration habit the deck does not have. The three
narration decks give identical figures under both matching rules; only the job talk diverges
(44% vs 28%), which is itself a sign it is a different kind of artefact. **(computed here)**

**Presenter notes do not appear in the slide text layer** — 0 of the 180 notes-bearing slides
(audit, "Notes in the text layer"). The previous pass's claim that a 12.8 pt band *was* the note
came from the bad export and is dead.

---

## How much lives in his mouth, and where

Notes coverage by position in the deck **(computed here**, quintiles by slide index):

| Deck | 1st fifth | 2nd | 3rd | 4th | 5th |
|---|---:|---:|---:|---:|---:|
| Luminate | 91% | 100% | 45% | 45% | 36% |
| Sensecape | 83% | 100% | 100% | 100% | 71% |
| KAIST | 32% | 76% | 92% | 80% | 54% |
| Job talk | 57%* | 20%* | 3%* | 10%* | 16%* |

\* job-talk cells count the Korean glossary, not narration.

Three genre shapes fall straight out of this.

**Luminate — scripted front, shown back.** The setup is written out sentence by sentence with a
per-slide clock; by the demo and the results it drops to under half, and the two deployment-study
quote slides (43, 44) carry no note at all. He narrates the *capability* once over ten
screenshots (23–32 carry four distinct notes between them) and then lets the interface play.
**The densest notes sit on the emptiest slides** — slide 4 is one sentence on black with a 45-word
note; slide 5 is a quotation and a photograph with 42. **(observed + computed here)**

**Sensecape — scripted throughout.** 91% coverage, the highest in the corpus, and the longest
median note (33 words). It is also the shortest deck and the emptiest — 22% of its slides carry
no copy at all. The talk is almost entirely in his mouth and the slides are almost entirely
picture. **(computed here)**

**KAIST — scripted where it is new.** Coverage climbs from 32% in the opening frame to 92% in the
middle, and the clocks concentrate in the CodeToon section. The frame — telescopes, observatories,
the thinkable-territory metaphor — is the part he can say without notes; the paper segments are
the part he times. **(computed here)**

**Job talk — no script anywhere.** See above.

---

## The arcs

### Luminate (CHI'24, 55 slides) — the conference arc

| Slides | Beat | Move |
|---|---|---|
| 1–2 | Open | Blackout, then the paper's own title card. Co-authors named in twenty seconds. No outline slide. |
| 3 | The world now | Other people's systems, as pictures, venue-tagged. |
| 4 | **Turn 1 — the challenge** | Black slide, one question. The answer is in the note, not on the slide. |
| 5 | Borrowed authority | Pauling: have lots of ideas and throw the bad ones away. The talk's whole principle arrives in somebody else's words before any of Sangho's. |
| 6–13 | The principle, drawn | The design-space plane; fixation; design-space thinking staged as a strike-through; then the same drawing with LLMs attached; then two ✗ marks. Eight slides, one picture. |
| 14–18 | The gap, concretely | Real ChatGPT, real prior systems, and the verdict: *help converge, not diverge*. |
| 19 | **Turn 2 — the research question** | The evidence just built is dimmed and the question is laid on top of it. |
| 20–22 | Contribution named twice | The framework (an abstraction), then one worked example, then the system (a thing you can run). |
| 23–32 | System shown | Ten full-bleed captures, four notes between them. |
| 33–44 | Evaluation | Divider; the question box; who; then findings **entirely in participant quotes**. The box returns unchanged at 40/41 to close Study I and open Study II. |
| 45–51 | Widen and speculate | Divergent/convergent thinking; a chat interface with an "Explore" button; design space ⊕ creative writing. |
| 52 | **Turn 3 — the closing questions** | The future-work slide dimmed, two questions laid over it in handwriting. |
| 53–55 | Close | QR, URL, team, "Questions?", blackout. |

### Sensecape (UIST'23, 32 slides) — the same arc, compressed and barer

Blackout → title card → **a scenario acted out in screenshots** (3–6: a search box, a results
page, a ChatGPT answer) → the question on white (7) → the limitation stated over a dimmed
screenshot (9) → simple-vs-complex comparison (10) → the axis built over six slides (11–16) →
the system named over the dimmed axis (17) → the system shown (18–22) → two quote cards (23, 24)
→ "Takeaway & Future Work" (25) → three widening statements (26–31) → **the title card again**
(32).

Two differences from Luminate that are worth a skill knowing: **the scenario comes before the
argument** (you watch somebody fail at a task before you are told what is wrong), and **the deck
ends where it began**, on its own title card, with no QR and no "Questions?".

### KAIST (126 slides) and the job talk (152) — the anthology arc

Both are a **frame** into which whole conference talks are dropped. The frame is measurable: a
cream right-edge strip carrying the icon rail appears on **24 KAIST slides** — 1, 4, 5, 6, 9–17,
46, 47, 76, 77, 118–124 — and **30 job-talk slides** — 5, 12, 13, 14, 17, 18, 20–30, 61, 62, 94,
95, 142–150. That is the opening, the joins between papers, and the close, and none of the
embedded segments (**computed here**; same measurement as `visual-language.md`). Note what is
*not* in those lists: KAIST 2 (the blackout), 3 (the title card) and 7 (a full-bleed photograph)
carry no rail — their right strip is 100%, 94% and 100% dark respectively.

**The frame's arc, shared by both:**

1. **Who I am, in photographs.** Two lab photos with band labels (KAIST 1; job talk 5).
2. **Blackout.** (KAIST 2; job talk 10.)
3. **Talk title card** — serif, on black, beside a generated image, with only his name.
4. **An extended physical metaphor, told as a visit.** Griffith Observatory, Mount Wilson, a
   founder's quote, a timeline from 1650 BC to today (KAIST 4–8; job talk 12–19). The talk's
   thesis — *optical instruments extend the range and depth of perception; AI tools should do the
   same for thought* — is established entirely through other people's things before any of his
   work appears.
5. **The question, twice** (KAIST 9, 10; job talk 20, 21), then the abstraction built as one
   drawing over five to seven slides.
6. **Three chapters**, each announced by the chapter card and each containing a whole paper talk:
   Design Space (Luminate), Information Space (Sensecape), Representation Space (CodeToon).
7. **Looking ahead** — an open-question card naming the spaces he has *not* entered
   (KAIST 119; job talk 143–145), then the metaphor drawn one last time.
8. **Contact card, blackout.**

**The job talk differs from KAIST in three ways**, all of them additive: it opens with four
diagram slides *before* the lab photos (see `archetypes.md`, boundary 5 — I cannot tell whether
that is a cold open or leftovers); it inserts seven **AI-image + band question** slides
(59, 60, 91, 92, 93, 140, 141) that widen each chapter from "writers" to "the general public" and
"scientists"; and it carries a research-agenda slide (139, the Artshine partnership) that KAIST
does not.

---

## What the shape is, across four decks

**The talk turns on questions, and the question is laid over the evidence that produced it.**
15 dimmed-stage questions and 13 full-stop questions across the corpus, in all four decks. The
dimmed form is the signature: Luminate 19 and 52, Sensecape 9, KAIST 19/22/94/95, job talk
7/9/32/35/112/113 all fade the argument to grey and put the question on top of it, so the
question is literally placed on what motivated it. **(observed)**

**The principle is borrowed before it is asserted.** Ten borrowed-authority quotes: Pauling
(Luminate 5), Griffith J. Griffith (KAIST 7, job talk 15), Bill Buxton (job talk 8), Bret Victor
(KAIST 74, job talk 89), Donald Knuth (KAIST 84, job talk 102). In every case the borrowed
sentence arrives *before* Sangho's own claim on the same subject, and the next several slides are
that sentence turned into a drawing. **(observed)**

**Results are testimony, not measurement.** 17 participant-quote cards across four decks, and
**no result is ever plotted, tabulated or given an inferential statistic** — 0 charts and 0
inferential tokens in 365 slides (**computed here**; see `never-list.md` entry 3 for the searches
and for the descriptive study quantities that *are* on slides, such as `14 Professional Writers`
and `Average: 7.3 years`). Luminate says so out loud: "* Please read our paper for detailed results"
(34, 35). This was the previous pass's most Luminate-suspect finding and it holds across five
studies in four decks.

**The contribution is named twice, at two levels of abstraction** — framework first, system
second, on separate slides (Luminate 20 then 22; KAIST 38 then 40; job talk 51 then 53).
**(observed)**

**Re-orientation is done by returning to an unchanged card**, not by a progress bar — but the card
differs between decks. Luminate returns to the same rough-bordered research-question box four
times (34, 35, 40, 41). KAIST and the job talk instead return to the three-spaces chapter card
with a different one blackened (KAIST 17/46/47/76/77/118; job talk 30/61/62/94/95/142). Same job,
two implementations. **(observed)**

**A note on vocabulary, for readers arriving from the other three documents.** Those group the
decks into a "conference register" (Luminate) and a "talk register" (KAIST, the job talk), with
Sensecape straddling. **That grouping is a hypothesis about *why* the four decks differ, not a
grade of evidence, and it is not settled** — both conference talks land on opposite sides of it,
and the decks do not order chronologically (Sensecape is UIST'23, Luminate CHI'24, so the sequence
runs clean → rough → clean). See `visual-language.md`, "Two registers" and item 1 of its
uncertainty list. **This document therefore names decks rather than registers**, and the words
"conference register" and "talk register" appear nowhere in it outside this paragraph.

**"There is no summary" was wrong.** The previous pass called this its most falsifiable claim and
it is false: **Takeaway cards exist** — KAIST 44, 45, 114 and job talk 57, 58, 132, 133, plus
Sensecape's "Takeaway & Future Work" divider (25). Three of the four decks summarise. What is
true, and worth keeping, is the narrower claim: **no deck in the corpus *ends* on a takeaways
slide.** All four end on a contact card or the title card, and two of them on a blackout. The
takeaway lands mid-talk, at the close of each paper segment, not at the end of the talk.

---

## What I could not get from this source

- **Whether any script was followed.** These are authored notes; no recording is in the corpus.
  `watch-recording` over the CHI'24 or the KAIST recording would settle how much he improvises,
  and is the single most informative thing still unextracted.
- **Why the job talk's notes are a Korean glossary.** Three readings fit the file equally well
  (delivery in Korean, rehearsal aid, personal vocabulary practice) and nothing in the corpus
  separates them.
- **Whether job-talk slides 1–4 are a cold open or leftovers.** See `archetypes.md`.
- **What was cut.** `controller-findings.md` records that Luminate's `.key` holds 73 slides of
  which 18 are skipped — cut material is kept rather than deleted. The cut slides are not in any
  render, so what he chose to drop is still invisible.
