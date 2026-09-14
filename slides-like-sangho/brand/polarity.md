# Polarity: what a dark ground does to each archetype

Decided once so it is not re-guessed per deck. Read it whenever a brand pack's
`colors.background` is dark — Asta's `extra-dark-teal #032629` under `cream #faf2e9` text is the
case this was worked through against. Strata and any other light system need the palette swap and
nothing here.

**Why this document exists.** Several archetypes are not defined by what they contain but by a
*contrast direction*. Flipping the ground does not repaint them; it reverses or deletes them, and
it does so quietly — the slide still renders, the tokens are all correct, and the device has simply
stopped doing its job. Working through all twenty-three found a further pattern nobody warned
about: **light-ground artwork he does not control** (the paper's own figures, other people's
screenshots, cut-out portraits) collides with a dark ground harder than any of his own devices do.

**The rule, and its exception, in one line each.**

> **A device whose meaning is a CONTRAST inverts with the ground.** A dark band means something only
> against light paper; greying-back means recession only relative to a ground; inverted quote
> emphasis is a comparison between two values. Flip the ground and all three flip with it.
>
> **A device whose meaning is ABSENCE does not invert.** It is not saying "different from the
> surface", it is saying "nothing here", and nothing is nothing at any polarity.

**The blackout is the exception, and Sangho confirmed it** (§3): a blackout on a dark ground is
still black, not the ground's bright inverse. Applying the inversion rule to it produces a
confident, wrong answer that still looks like a design decision — which is exactly the failure this
document exists to prevent, arriving through the document's own rule.

**It is the only absence-defined archetype in the set.** Sorting all thirteen re-specifications by
*why* they need re-specifying:

| Why | Count | Which |
|---|---:|---|
| **Contrast** — the rule above applies | 6 | Conceptual diagram, Participant-quote card, Dimmed-stage question, Chapter card, Study-setup card, Talk title card |
| **Asset provenance** (§6) — the artwork's own ground, which is not yours to flip | 6 | Interface capture, Prior-work montage, Borrowed-authority quote, Paper title card, Interface ↔ concept split, Annotated paper figure |
| **Machine readability** (§8) — a scanner, not a viewer, is the reader | 1 | Closing contact card |
| **Absence** — the rule above does *not* apply | 0 re-specified; 1 unchanged | Blackout (§3) |

So the inversion rule governs **six** of the twenty-three, not all of them. Seven more are
re-specified for reasons that have nothing to do with polarity, and exactly one is
absence-defined — the blackout, which is why it is the one the rule gets wrong.

A future archetype added to this file should be sorted the same way **before** the inversion rule is
applied to it: contrast, absence, or neither.

The archetype list is `references/archetypes.md`. Counts there are his; the verdicts here are mine.

---

## First: this document is the cost of choosing Asta, not the cost of branding with Ai2

The inversion does not come from Ai2. It comes from **one product system inside it**:

| System | `colors.background` | `colors.text` | Ground |
|---|---|---|---|
| **Strata** (the base system) | `{colors.cream}` | `{colors.dark-teal}` | **light** |
| **Asta** | `{colors.extra-dark-teal}` | `{colors.cream}` | **dark** |

Strata is the foundation both products are composed from, and it is a **cream ground with dark-teal
ink** — which is his own corpus's polarity almost exactly (263 of 365 slides white, 61 cream).
**Under Strata the inversion mostly does not arise**: the greying-back family fades toward a light
ground as it already does, the dimmed-stage question dims toward dark as it already does, and the
dark band label keeps working. What is left is a palette-and-typeface swap, and the §6 artwork
problem all but disappears because light-ground artwork meets a light ground. (The blackout is
unchanged either way — see §3; it is not one of the things Strata buys you.)

Asta is dark, and **everything below follows from that one choice.** Thirteen of the twenty-three
archetypes have to be re-specified — and one, the blackout, notably does **not** (§3, confirmed by
Sangho), which is the document's own rule failing in its one absence-defined case.

**The default stays Asta.** Sangho chose it and that stands; this is not an argument for switching.
It is so the cost is legible when the choice is made, and so the light-ground alternative has a
name. If a deck does not specifically need Asta's identity — an internal talk, a submission draft,
anything where "Ai2" is the brand rather than "Asta" — `strata/DESIGN.md` gives the Ai2 palette and
typeface at his own polarity, and this document becomes almost entirely unnecessary.

Check `background` / `text` on whatever DESIGN.md you are handed before assuming which case you are
in. A third system may be either.

---

## All 23, at a glance

| Archetype | On a dark ground |
|---|---|
| Conceptual diagram (build step) | **re-specified** — greying-back reverses |
| Interface capture | **re-specified** — pasted light artwork |
| Participant-quote card | **re-specified** — the inverted emphasis reverses |
| Statement card | unchanged (ink flips) |
| Dimmed-stage question | **re-specified** — dimming toward black is invisible |
| Full-stop question | unchanged (ink flips) |
| Prior-work montage | **re-specified** — pasted light artwork |
| Borrowed-authority quote | **re-specified** — cut-out portraits |
| Photo + band label | unchanged, with one constraint |
| Chapter card | **re-specified** — greying-back reverses |
| Paper title card | **re-specified** — pasted light artwork (forbidden under `brand: none`) |
| Study-setup card | **re-specified** — icons must be restroked |
| Blackout | **unchanged — it stays black. Confirmed by Sangho** (the one entry the inversion rule gets wrong) |
| Naming slide | unchanged (ink flips) |
| AI-image + band question | unchanged, same constraint as Photo + band label |
| Takeaway card | unchanged (ink flips) |
| Interface ↔ concept split | **re-specified** — the seam is the problem |
| Question roadmap | unchanged (border ink flips) |
| Annotated paper figure | **re-specified** — pasted light artwork |
| Open-question card | unchanged (ink flips) |
| Closing contact card | **re-specified** — the QR (forbidden under `brand: none`) |
| Section divider | unchanged (ink flips) |
| Talk title card | **re-specified** — it loses its distinction (forbidden under `brand: none`) |

**Thirteen re-specified, ten unchanged** — of those ten, seven are a plain ink flip, two carry one
constraint, and one (Blackout) is confirmed unchanged by Sangho. "Unchanged (ink flips)" means
exactly that: black type on white becomes `text` on `background` and nothing else about the slide
changes.

*(An earlier version of this line read "twelve / nine / two". The rows summed to 23 but the
categories did not match them — a tally error in my own verdicts, corrected here along with
Blackout's move out of the re-specified column.)*

---

## 1. The greying-back family — the direction reverses

**Affects: Conceptual diagram (build step), Chapter card**, and the greying-back device wherever
else it appears. This is the corpus's single strongest compositional finding — more than half of
every deck is one picture being edited, and what makes the edit legible is that *explained parts
fade and only the new part is at full contrast*.

On white, "faded" means **lighter** — toward the ground. On a dark ground, lighter moves *away*
from the ground and a faded part becomes the loudest thing on the slide. Fading has to move toward
the ground in both cases, so on dark it means **dimmer**.

**Re-spec:** the current part is `text` at full value. Explained parts drop to roughly `cream-40`
to `cream-30` (Asta names these). Not-yet-introduced parts, where the figure shows them at all, go
to `cream-20`.

Keep the *contrast ratio* his greys achieve, not the grey. A light-grey on white is a small
step down from black; three levels of `cream-*` alpha on `extra-dark-teal` is the equivalent
ladder. Check that the dimmest level is still readable at the back of a room — on a dark ground it
is easy to fade something into genuine invisibility, which is a different move (it reads as removed
rather than as set aside) and reverses what the build is saying.

## 2. Dimmed-stage question — dim by lowering, not by darkening

**Affects: Dimmed-stage question** (15 slides, all four decks; the signature move of the corpus's
question habit — the question is laid *on* the evidence that produced it).

The move is: take the slide that just made the argument, dim it, lay a question across it. On white
he dims toward grey or black. **On a dark ground there is nowhere darker to go** — the argument is
already sitting on near-black, and dimming it toward black makes it vanish, which destroys the
whole point. The question would then be a full-stop question on a blank stage, which is a
*different archetype he also uses*, so the failure is invisible: the slide looks like a deliberate
choice.

**Re-spec:** dim the argument by dropping its ink to `cream-30` and keep it there — still legible
as a shape, no longer readable as a claim. Lay the question over it at full `text`. If the argument
beneath is a photograph or a screenshot rather than line work, drop its opacity to ~35% against the
ground instead, and keep the question off the image's busiest region.

**Do not add a scrim.** A translucent dark scrim over a dark ground buys almost no separation and
costs the ability to see the argument at all.

## 3. Blackout — it stays black. **Confirmed by Sangho**

**Affects: Blackout** (7 slides; at both ends of Luminate, both ends of KAIST and the job talk, and
the head of Sensecape — the placement evidence is why it was promoted to a real archetype).

**Sangho Suh, 2026-09-13.** Asked what a blackout should be on a dark ground, he answered:
*"I think the blackout slide under a dark ground can just be a black slide."*

> **Re-spec: there is none. A blackout is black, `#000000`, empty.** Nothing on it — no mark, no
> number — exactly as in the corpus. This archetype **does not invert**, and it is the one place in
> this document where the general rule is wrong.

**Why, because the reasoning matters more than the verdict.** Every other entry here inverts because
its meaning is **relational**: a dark band means something only against light paper, greying-back
means recession only relative to a ground, inverted quote emphasis is a comparison between two
values. Flip the ground and a relational device flips with it.

**A blackout is not relational. Its meaning is absence — the screen goes away.** Black on
`extra-dark-teal` is still a step down and still removes the surface, so the gesture survives at a
smaller contrast step. It does not need to be the *most* different value on offer; it needs to be
nothing.

**The rejected reading, kept on the record.** This entry previously specified a full-bleed **cream**
slide (`background-reversed`), reasoning that the archetype's job is "a hard interval maximally
different from its neighbours" and that on a dark deck the maximally different value is the ground's
inverse. That is what the general inversion rule produces, and it is wrong twice over: cream in a
dark room is a **flash**, which is the opposite gesture to lights-out, and it makes a talk that
opens and closes on two blackouts open and close on the brightest slides in the deck. The rejected
reading is why the confirmation is load-bearing rather than decorative — the rule that correctly
governs every contrast-driven entry in this file would have broken this one, and it would have
broken it in a way that still looked like a deliberate design decision.

## 4. Band label — Sensecape's inversion becomes the default

**Affects: Photo + band label, AI-image + band question**, and the band label wherever it
substitutes for a title.

Three decks put **light type on a dark rectangle**; Sensecape does the opposite — **black text in a
white rounded box with a black border**. `references/visual-language.md` records that the *job*
(name the beat without claiming the top of the slide) is in all four decks and the *rendering* is
not.

On a dark ground the majority rendering stops working and **Sensecape's minority rendering becomes
the correct default**: a light box carrying dark type is now the high-contrast move, and a dark
band is now the low-contrast one.

**Re-spec:** a `background-reversed` box with `text-reversed` type, at the same placement rule —
dropped wherever the image is empty, never centred, never at the top by default.

**The one constraint on Photo + band label and AI-image + band question:** the dark translucent
band survives *only* where it sits entirely over the image. A full-bleed photograph is the brightest
thing on a dark slide, so a `extra-dark-teal-70` band over it works exactly as it does in the
corpus. The moment the image is half-bleed and the band crosses onto the ground, the band and the
ground merge and the type appears to float. Keep the band inside the image's bounds, or bleed the
image.

## 5. Participant-quote card — the inverted emphasis reverses

**Affects: Participant-quote card** (17 cards across four decks, and the device survives being
re-set in two completely different type families, which makes it the most portable thing in the
corpus).

The device is *inverted*: the context is set **back** and the load-bearing phrase is pushed
**forward**. On white, "set back" is grey and "pushed forward" is bold black.

On a dark ground, forward is toward `cream` at full value and back is toward the ground. So the
grey does not become a lighter grey — it becomes `cream-50`, and the phrase becomes full `cream`
plus the weight step he already uses.

**Re-spec:** context `cream-50` regular (or italic, per the deck's type system); phrase `text` at
full value, bold. If the deck marks the phrase with a coloured underline rather than weight, take
the accent from the brand's `link` or `interactive-primary` alias and check it against the dark
ground — several brand accents are tuned for a light surface and lose most of their chroma on a
dark one.

## 6. Light-ground artwork he does not control

**Affects: Paper title card, Annotated paper figure, Interface capture, Prior-work montage,
Interface ↔ concept split, Borrowed-authority quote.** This family was not on the warning list and
is the largest group here.

Every one of these archetypes places artwork **he did not draw for this deck**: the paper's own
title graphic, the paper's own method figure, other people's interface screenshots, portraits. All
of it is on a white ground, because papers and interfaces are.

Pasted onto `#032629`, a white-ground figure is a glowing rectangle — and a rectangle is exactly
what never-list entry 6 (`visual`) says a capture must not become. On a white deck the capture's
own ground merges with the slide's and the edge disappears; on a dark deck there is no such thing
as an unframed light capture.

**Re-spec, in preference order:**

1. **Bleed it.** A capture that runs to the slide edges has no floating edge to read as a frame.
   This is what he does with most captures anyway (`Interface capture`: full bleed or one clean
   half), so it costs nothing.
2. **Give it a full-width band of its own** when it cannot bleed — the image sits in a light band
   that runs edge to edge, so the seam is horizontal and deliberate rather than a card outline.
3. **Re-draw it** when it is line work and you have the source. His own redraw of the Luminate
   figure for KAIST/job talk is the precedent, and a figure redrawn in the brand's ink is the only
   version of this that is genuinely clean.
4. **Invert it** only for pure black-on-white line art with no photographic content, and check the
   result — inverted line art reads as a negative, which is a strong effect and rarely what you
   want on more than one slide.

**Portraits** (Borrowed-authority quote) are their own case: a cut-out on white leaves a halo on a
dark ground. Either use a rectangular crop bled to an edge, or a cut-out made against the dark
ground with no matte. **Archival photographs keep their source URL lettered along the bottom edge**
(KAIST 6 / job talk 14) — that type flips to `cream` and stays the smallest thing on the slide.

**Interface ↔ concept split** is the worst case in the family, because the capture and the drawn
abstraction sit side by side: a light half against a dark half with an arrow crossing between them.
Prefer redrawing the abstraction onto the light half's ground so the whole slide is the light band
(option 2), rather than splitting the ground down the middle.

**Paper title card** is a pasted image by definition — the paper's own title graphic with headshots
and institution marks. Under `brand: none` it is forbidden outright; under a brand pack, set the
title, authors and marks as type and assets instead of pasting the graphic.

## 7. Study-setup card — restroke the icons

**Affects: Study-setup card**, and every other slide carrying line icons (the icon rail, the
`Opportunities` grid, the process strips).

Line icons in the corpus are black strokes. On a dark ground they disappear. Restroke them to
`text`, at the brand's stroke weight if it names one.

**The flat orange-and-slate stock people** (KAIST 43 / job talk 56) are the harder half: the slate
is a mid-dark value that was chosen to sit on white and goes nearly invisible on `extra-dark-teal`.
Re-value the dark parts of any flat illustration rather than re-tinting the whole thing, or replace
the illustration with line icons in `text`, which is what the same card does in the other decks.

## 8. Closing contact card — the QR

**Affects: Closing contact card.** Forbidden under `brand: none`; under a brand pack the QR is the
problem. Many scanners handle an inverted QR (light modules on dark) poorly or not at all, and a QR
that does not scan is worse than no QR because the audience finds out by failing.

**Re-spec:** keep the QR dark-on-light and set it in its own light patch with the full quiet zone
intact. Do not invert it, and do not trust that a given scanner copes.

## 9. Talk title card — it loses its distinction

**Affects: Talk title card.** It is a serif title on black beside a generated image, and it is the
one archetype that is *already* at a dark deck's polarity. Nothing about it breaks — it simply
stops being distinct, because the whole deck is now that value.

**Re-spec:** keep it, and let the distinction come from the serif face, the image and the amount of
empty space rather than from the ground. If the deck needs the title card to feel like an arrival,
the cheapest move is **not** the neighbouring slide. An earlier version of this entry sent you
there — he places a blackout immediately before the title card in both long decks, and while §3
still specified a cream blackout that neighbour restored the contrast step for free. §3 is now
settled the other way, so the preceding slide is black on near-black: a real step down, but a small
one, and not enough on its own to make the title card feel like an arrival. Buy the arrival inside
the slide instead — the amount of empty space around the title is the lever, and it costs nothing. Forbidden under `brand: none`.

---

## What this document does not settle

- ~~**Whether the cream blackout is right at all.**~~ **Settled — and settled against this
  document's own reasoning.** Sangho answered on 2026-09-13: the blackout stays black. See §3, where
  the rejected cream reading is kept on the record. The general lesson is at the top: an
  absence-defined device does not invert.
- **Whether a dark deck should carry his cream `#f0eade` frame ground.** The corpus's second ground
  is a warm cream used for the talk's own frame. On Asta, `cream` is the *text* colour, so reusing
  it as a frame ground collides. Left open: either the frame drops its second ground entirely, or
  it uses `dark-teal #0a3235` as a one-step-lighter frame value. Raise it in the storyboard.
- **Nothing here is measured.** Every verdict is derived from the archetype's stated job in
  `references/archetypes.md` plus one design system's tokens. One sentence from Sangho overrides
  any of it.
