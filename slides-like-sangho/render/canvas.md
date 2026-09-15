# Render path: Claude Design canvas

**Not the default, and not always available.** Sangho's stated default is HTML published as a
Claude artifact (`html.md`), which is also the only path with a generator in this skill. Reach
for the canvas when the bundled `design` skill IS offered in the session and he wants to edit
slides directly rather than through the storyboard.

**Check before promising it.** A session can carry the `design` directory's asset files with no
manifest, in which case the skill is not invocable and the path is unreachable — confirm `design`
appears in the available-skills listing, not merely on disk.

Produces a published artifact page carrying every slide as an artboard on one
pan/zoom canvas. Where saving is enabled on the account, Sangho can click any element, edit it
visually, and Save republishes a new version; otherwise he gets a view-and-export preview with
PNG/PDF.

Why it is worth offering when it IS available: a deck is a set of slides seen *together*, and this
is the only path where he can see the whole arc at once and fix one slide himself without leaving
the view. That is the one thing the HTML path cannot give him — there, edits go through the
storyboard and through Claude.

## Status: UNVERIFIED

**This path has never been run end to end by this skill.** Every other claim in these references
is marked `(observed)` or `(computed here)`; this one is neither. It is written from the design
skill's own documented contract, not from a render anyone looked at. Treat it as a plan, and say
so when you offer it — the first time it runs, verify it the way `html.md` says to verify HTML,
and replace this block with what you actually saw.

Two things are known rather than assumed:

- The bundled `design` directory has been observed **present on disk with no manifest**, and its
  files vanished from the bundle between two turns of a single session. Check the available-skills
  listing at the moment you offer this, never the filesystem.
- `python-pptx` installs cleanly here, so **PPTX is the alternative you can actually verify today**
  if he wants something editable and the canvas is unreachable.

## Handing off

Build `deck.json` first (`render/html/build_deck_json.py`) — it is the renderer-neutral seam, and
it is where his storyboard edits are merged. Then give the `design` skill:

- **one artboard per `deck` entry, in order**, at 1920 x 1080;
- the slide's resolved `words` as the body, `header` as the boxed chapter label, `title` as the
  artboard name so the canvas is navigable;
- the ground from `ground` (`""` cream / `g-rev` dark teal / `g-black` black);
- figures and tables as placed images — upload them as artifact assets first and pass the
  `/_blob/<id>` urls, exactly as `html.md` describes;
- the type ladder from `references/visual-language.md`, and the sizing rules from `html.md`.
  **The canvas does not fit text for you.** `gen_deck.py:fit()` is the only implementation of
  that rule in this skill; a canvas path that skips it will set a 90-word slide at 84pt.

## How

**Do not hand-roll this.** Invoke the bundled `design` skill and let it do the seeding — it owns
the artboard grammar, the state block, the title and filename gates, and the pre-publish check, and
those move without notice. This file only records what a *slide deck* has to tell it.

```
Skill(skill: "design")
```

Then give it:

- **One `.dc.html` artboard per storyboard beat**, in beat order. Name them so the order is
  obvious and the entry board is first: `Main.dc.html` is the editor's entry file when present.
  A name like `03-fixation.dc.html` reads better in the file list than `Slide3.dc.html`.
- **Artboard size 1920 × 1080** on every board. Do not mix sizes; a deck is one aspect ratio.
- **A `canvas.json` laying them out in reading order**, left to right, wrapping into rows. Leave
  **at least 80 px between frames** — the editor puts a name strip and tweak chips above each one,
  and overlapping frames are flagged by its own check.
- **Images as separate files**, referenced by their own bare names. Screenshots and photographs go
  in this way rather than as data URLs.

## What to put in an artboard

Plain HTML and CSS at 1920 × 1080. The design language is `references/`; this is only the mechanics.

- **Set type in absolute `px` at the derived scale** — 112 / 84 / 50 / 36 / 24 — because the
  artboard is a fixed 1920 px wide and a point is a pixel there. Do not use `rem`: the artboard's
  root size is not yours to rely on, and a scale expressed in `rem` is exactly how a brand's screen
  sizes leak in (`brand/README.md`, Finding 1).
- **Position absolutely.** There is no grid in the corpus — no repeating columns, no consistent
  left margin, no baseline grid across 365 slides. Do not impose one by reaching for flexbox
  defaults; place each element where the composition wants it.
- **A build is N boards, not one board with states.** Copy the previous board and edit it. That is
  literally what the corpus does, and it is why the boards are cheap to make.
- **Greying back is an opacity or colour change on the parts already explained**, not a rebuild.
  Keeping the DOM identical between build steps makes the edit obvious to anyone reading the files
  later, including Sangho.

## What this path cannot do

- **No presenter notes field.** Write `notes.md` beside the output, one numbered entry per slide,
  and say in the handback that the notes are there. In the corpus the note belongs to a *beat*, not
  a slide — repeated verbatim across consecutive build steps — so numbering a note to a range
  (`12–16`) is more faithful than repeating it five times.
- **No presenting.** It is a canvas, not a presenter view. If he needs to present from it, export
  PDF, or use the PPTX path instead.
- **No animation.** Which is not a limitation for this corpus — every build in it is a slide
  change.

## Where the files go

Into the output directory (`SKILL.md`, "Where output goes"), not into any repo. The published
artifact is the deliverable; the `.dc.html` sources are how it gets rebuilt, so keep them.
