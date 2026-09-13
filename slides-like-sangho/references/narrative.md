# Narrative — first pass

**Evidence base: one deck.** Luminate @ CHI'24, 55 slides. This is the best-evidenced of the four
documents, because 35 of the 55 slides carry a presenter note and those notes are a **timed
script**, not reminders. It is still one talk, and a conference talk is the most constrained
speaking format there is — a job talk or an invited talk may have a completely different arc.

Audit figures cite [`tools/slide-audit.md`](../../tools/slide-audit.md) (1 deck). Figures marked
`controller-findings` come from `controller-findings.md`. Anything else is **my count** over the
55 manifest entries.

---

## The source, and what it is

**Notes: 35 of 55 slides, median 23 words, maximum 47** (audit, "Presenter notes", 1 deck).

They are a script with a clock in it. The first reads:

> `00:00 - 00:20 (20 s)` — Hi, my name is Sangho. I will present Luminate on behalf of my
> co-authors…

**Timing markers appear on 20 of the 55 Luminate slides** (`controller-findings`), and
`controller-findings` is explicit that this is a per-deck convention: **21/126 on KAIST, 0/32 on
Sensecape, 0/152 on the job talk.** Do not carry the habit to other decks.

**The clock is the strongest single finding here.** Of the notes that start with a cue, the
duration is almost always **10 s or 15 s**, occasionally 20 s (my reading of the 22 cue-bearing
notes). He is budgeting per slide, at roughly a slide every twelve seconds through the setup —
which is why the setup can spend eleven slides on one diagram without feeling slow.

**A note belongs to a beat, not to a slide.** Slides 26, 27 and 28 carry the *same note, word for
word* — three slides of one semantic-zoom build, narrated once. Slides 53 and 54 do the same. Where
a slide is a build step or a return to something already narrated, the note is absent or repeated
rather than rewritten. This is the mechanism behind everything in the next section.

---

## How much lives in his mouth

Reading notes-word count as "how much is spoken here" against what is on the slide:

**Where the notes are densest, the slides are emptiest.** The five highest note counts are slides
2 (47 words), 4 (45), 5 (42), 32 (36) and 36 (36). Slide 4 is *one sentence on a black field*.
Slide 5 is a quotation and a photograph. The setup slides 6–13 carry a wordless diagram and notes
of 12–32 words each. The argument is spoken; the slide holds the picture he is speaking over.

**Where the notes disappear, the slide is doing one of three things** (all 20 note-free slides
account for):

| Job | Slides | Count |
|---|---|---:|
| **Build step** — the previous beat continuing, already narrated | 23, 24, 25, 29, 30, 46, 47, 48, 49, 50 | 10 |
| **Return / re-orientation** — a card the audience has already seen | 35, 40, 41, 37, 43, 44 | 6 |
| **Structural** — divider or blackout, nothing to say | 1, 33, 45, 55 | 4 |

That third of the deck is the part he *shows* rather than *says*. Note the 43/44 entry: the two
deployment-study quote slides carry no note at all, which means he intends the audience to **read
the quote** while he is silent or improvising over it. The user-study quote slides (38, 39) do
carry notes — and their notes paraphrase the quote rather than adding to it.

**The demo is where speech drops out hardest.** Slides 23–32 are ten slides; they carry 4 distinct
notes between them (26/27/28 share one). He narrates the *capability* once and then lets the
interface play.

---

## The arc

| Slides | Beat | Move |
|---|---|---|
| 1–2 | **Open** | Blackout, then the paper's own title card. Names co-authors and where the work was done, in twenty seconds. No preamble, no outline slide. |
| 3 | **The world now** | Other people's systems, as pictures, venue-tagged. Establishes that the area is live without claiming anything. |
| 4 | **Turn 1 — the challenge** | Black slide, one question: *"But are we using the creative potential of generative AI to its fullest?"* He tells you the answer is no in the note, not on the slide. |
| 5 | **Borrowed authority** | Pauling: have lots of ideas, throw the bad ones away. The talk's whole principle arrives in someone else's words before any of Sangho's. |
| 6–8 | **The principle, drawn** | The design-space plane. Then fixation. Then design-space thinking replacing it, staged as a strike-through. |
| 9–12 | **The opportunity** | The *same* drawing, now with LLMs attached, built up across four slides at 12–20 words of narration each. |
| 13 | **The gap** | Same drawing again, with two large X marks and a band title: current paradigms do not support this. |
| 14–18 | **The gap, concretely** | Real ChatGPT, real prior systems. Single-output, then multi-output, then the two papers that did multi-output — and the verdict: *help converge, not diverge*. |
| 19 | **Turn 2 — the research question** | The evidence he just built is dimmed to grey and the question is laid across it on a black band. The question is literally placed *on top of* what motivated it. |
| 20–21 | **Contribution named** | The framework gets a name and a one-line gloss, then one dense worked example. |
| 22 | **System named** | Luminate, centred, alone. |
| 23–32 | **System shown** | Ten full-bleed captures, annotated. Four notes total. |
| 33 | **Divider** | "Evaluation." |
| 34–35 | **Roadmap** | All three research questions in a box; then the same box narrowed to Study I. |
| 36–39 | **Study I** | Who (14 writers, cartoon faces), what (task counts), then two slides of findings *entirely in participant quotes*. |
| 40–41 | **Roadmap, returned to** | The same box again — Study I closed, Study II opened. No note on either: the card does the work. |
| 42–44 | **Study II** | Who (8 writers), then two quote slides, both note-free. |
| 45 | **Divider** | "Implications & Future Work." |
| 46–47 | **Widen** | Divergent/convergent thinking — the talk's specific result placed inside a general theory of creativity. |
| 48–50 | **Speculate** | What an ordinary chat interface would look like with an "Explore" button. Note-free: he is showing a possible future, not arguing for one. |
| 51 | **Next** | Design space ⊕ creative writing, and the implied ⊕ everything else. |
| 52 | **Turn 3 — the closing questions** | The future-work slide dimmed, two questions laid over it in *handwriting*. The talk ends on questions, not on claims. |
| 53–54 | **Close** | QR, URL, "Demo & Code", team, contact, "Questions?". |
| 55 | **Blackout** | |

---

## What the shape is

**Three questions, three hinges.** Slides 4, 19 and 52 are the only slides that stop the argument
to ask something, and they sit at almost exactly the three joints of the talk: motivation→principle,
evidence→contribution, results→future. Each is staged the same way — the stage is blanked or dimmed
so nothing competes with the question.

**The principle is borrowed before it is asserted.** Slide 5 puts a Nobel laureate's sentence on
screen before Sangho makes any claim of his own. The rest of the setup (6–13) is that sentence
turned into a drawing.

**The contribution is named twice, in two registers.** First the framework (20 — an abstraction),
then the system (22 — a thing you can run). They are separate slides with separate names, and the
system slide is deliberately quiet: a logo and two lines.

**Results are testimony, not measurement.** Both studies report through participant quotes and
cartoon faces, and both the evaluation roadmap slides carry a grey line in the corner —
"* Please read our paper for detailed results". The talk delegates the numbers to the paper
on purpose and says so.

**There is no summary.** No conclusion slide, no takeaways, no recap of contributions. The last
content slide is two open questions in handwriting. **This is the most falsifiable claim in this
document**: if the other three decks all end in a takeaways slide, it is a CHI-format artifact,
not taste.

**The audience is re-oriented by returning to an unchanged card, not by a progress bar.** Slides
34, 35, 40, 41 are the same rough-bordered box, shown four times with different amounts of it
live. That device carries all the structural signalling in the second half.

---

## What I could not get from this source

- **Whether the script was followed.** These are authored notes; the talk as delivered is not in
  the corpus. `watch-recording` over the CHI recording would settle how much he improvises —
  particularly over the note-free quote slides (43, 44), where the current reading assumes he
  lets the audience read.
- **Whether the clock is normal for him.** `controller-findings` already shows it is not: two of
  the four canon decks carry no timing markers at all. The *habit of budgeting* may still be
  there and just not written down.
- **Why 18 slides are skipped in the file** (`controller-findings`). Cut material is kept rather
  than deleted, which is itself a working-method fact, but the cut slides are not in the render
  and I could not read what he chose to drop. That is probably the single most informative thing
  still unextracted.
