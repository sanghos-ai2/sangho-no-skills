---
name: slides-like-sangho
description: Make presentation slides in Sangho Suh's design language, grounded in four of his talks. Use this WHENEVER the task is slides or a talk — a conference presentation, a job talk, an invited talk, a lab meeting, a defense, a demo deck, a poster session pitch — including turning a paper, spec or draft into slides, revising an existing deck, designing one figure or build for a talk, or deciding a deck's structure. If the output is something someone will present from, load this first. Gated per repo — it only designs in this language when a `.i-am-sangho` marker file exists at the repo root (see The gate).
---

# Slides Like Sangho

`references/` holds the design language, measured over four of Sangho's talks. **It is not
repeated here, and this file is not a summary of it** — read the four documents and work from them
directly. They carry their own evidence and their own error bars, which is exactly what a summary
would strip.

**What this file is for is the process**, because the design language is the half that transfers on
its own and the process is the half that does not. A baseline run of this task — two agents, no
skill — produced good-looking decks in Sangho's idiom and still failed four ways: neither checked
the gate, neither stopped for his approval before rendering 26 finished slides, both wrote output
into a public repo, and both improvised a render path. Those four are what the rest of this file
closes.

## The gate: `.i-am-sangho`

This skill imitates a real, named person. That is only acceptable in Sangho's own projects, so it
is gated per repo: **before doing anything else, read `<repo-root>/.i-am-sangho`.** If the file does
not exist, the repo has not opted in — do NOT design in Sangho's language, even if this skill was
explicitly invoked. Say the skill is gated and that it can be enabled by creating an empty
`.i-am-sangho` file at the repo root (`touch .i-am-sangho`), then help with the slide task in a
normal, unimitated register. An empty file counts as opted in; its content, if any, is irrelevant.

The baseline agents both wrote in his design language in a repo with no marker file, having found
`references/` on their own. Finding the references is not permission.

## Workflow

### 1. Detect the mode

- **A source document** — a paper, a spec, a draft, an existing deck. Draft from it. Read it fully
  before proposing an arc; a talk is a re-argument of the document, not a compression of it.
- **A topic alone.** Interview first, four questions, then stop: *Who is the audience? What is the
  one sentence they must remember? What can you show live or as a capture? How long do you have?*
  Do not proceed on guesses — every one of the four changes the arc, and the time budget changes
  the slide count outright.

### 2. Arc

From `references/narrative.md`, sized to the time budget. That document carries three real arcs at
three lengths; pick the one whose length matches, and say which you took and where you departed.

### 3. Storyboard — **and stop**

> **This is a hard stop. Do not render anything until Sangho has responded.**

The baseline's failure here was not laziness — both agents produced decent decks. They produced
them before anyone could redirect the arc, which makes every later fix a rebuild instead of an
edit. One block per beat, in order:

```
BEAT n — <short name>
  Message    the one thing this beat says, in a sentence
  Archetype  from references/archetypes.md, by name
  Visual     what is actually on the slide
  Type       which roles are present and at which step (references/visual-language.md)
  Build      1 step, or N: <what changes between them>
  Note       what he says over it
  ?          [GUESS: <what you assumed and why>] — one line per guess, or omit
```

Rules for the block:

- **Every build step is a beat.** More than half of every deck in the corpus is one picture being
  edited; an eleven-slide build is eleven blocks, not one block saying "builds over 11".
- **Flag guesses inline with `[GUESS: …]`,** and repeat them as a list at the end of the storyboard.
  A guess you did not flag is a decision you made for him.
- **Name what you could not source** — a figure that needs a screenshot he has not given you, a
  quote you do not have, a study number you invented. Say it rather than filling it in.
- **End with the count and the running time** at his own rate, and with the four questions from
  step 1 restated as you answered them, so a wrong premise is visible in one line.

Then hand it over and wait. If he responds with changes, restate the changed beats and stop again
— the second stop is cheap and a second rebuild is not.

### 4. Render — only after approval

`render/README.md` picks the path. Default is the Claude Design canvas; PPTX → Google Slides when
he wants to edit in a browser; standalone HTML when you need to verify by screenshot; Keynote is
gated and currently unusable on this machine (see `render/keynote.md`).

### 5. Sweep

Before handing over, check the deck against `references/never-list.md`, entry by entry. It is eight
live entries and takes a minute. Report which entries you checked and anything you deliberately
let stand, with the reason — several entries are `UNCONFIRMED` hypotheses and a deliberate
departure is legitimate; a silent one is not.

Then look at the render. `render/README.md` lists the two failures worth checking by name.

## Where output goes

**Never inside a git repo unless he names a path.** Default:

```
~/Desktop/slides-like-sangho/out/<YYYY-MM-DD>-<slug>/
```

Both baseline agents wrote a finished deck into `talks/` in a public plugin repo, untracked. They
also collided on the same path and one silently overwrote the other — hence the date and slug, and
hence checking whether the directory already exists before writing into it.

If the path he names **is** inside a repo, say so once — one sentence, naming the repo and whether
it is public — and then use it. It is his call; silence is how `talks/` happened.

## Brand modes

Two, and **anonymous is the default**. Full rules in `brand/README.md`; the polarity mapping a dark
brand forces is decided once in `brand/polarity.md`.

- **`brand: none`** *(default)* — his measured palette and scale, safe for double-blind submission.
  Strips brand visuals **and all identity text**: no author names, affiliation, acknowledgements,
  or institution-revealing URLs. Sangho chose the strict scope, because the failure is silent — you
  find out at desk reject.
- **`brand: <path to a DESIGN.md>`** — a named design system supplies palette, ground polarity and
  typeface. Default system when branded is Ai2's `asta/DESIGN.md`.

Ask which mode before storyboarding, in the same breath as the four questions. The mode changes
which archetypes are available, so it is an arc decision, not a rendering one.

**Two things a brand pack may never override**, because both are behavioural rather than visual:
the density (a 9-word median slide) and the `structural` entries in `references/never-list.md`.
**And it never supplies the absolute type sizes** — Ai2's `display` is `3rem`, which is 48 pt
against his measured 112, so applying a brand's sizes halves the deck while looking like a faithful
brand application the whole way down. Take the faces; keep the sizes.

## The references

Read all four before storyboarding. In this order:

| File | What it settles |
|---|---|
| `references/narrative.md` | the arc, and how much of the talk lives in his mouth rather than on the slide |
| `references/archetypes.md` | the 23 slide shapes, by the job each does in a talk |
| `references/visual-language.md` | type, space, figures, colour, emphasis — and the derived type scale |
| `references/never-list.md` | one confirmed rule, seven hypotheses, four refuted candidates |

Three things about them that a reader routinely gets wrong:

- **365 slides are 170 distinct designs.** The four decks are not four independent samples — the
  two long talks are anthologies that carry the two short ones inside them. A shape in Luminate
  *and* Sensecape is much better evidence than one in KAIST and the job talk. Every per-deck count
  should be read that way.
- **Exactly one never-list entry is confirmed by Sangho.** The other seven are inferred from
  absence, which is the weakest evidence there is. Treat them as strong defaults he can overturn in
  a sentence, and never as rules that beat something he has said.
- **The derived type scale is an imposition, and it says so.** These decks contain no scale; he
  asked for one anyway. Hard-code it only for the slide number and the slide title, and size
  everything else to fit — quotes and figure labels are genuinely sizeless in the corpus.

Every claim you repeat back to him should carry its scope. "He never uses charts" is a claim about
365 slides across five studies; "he grids the frame with an icon rail" is a claim about two decks
that share most of their slides. The difference is the whole value of the reference set.
