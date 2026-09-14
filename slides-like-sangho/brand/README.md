# Brand modes

A deck is built in one of two modes. **Anonymous is the default** and you do not ask for
permission to use it — you ask before leaving it.

| Mode | What it means |
|---|---|
| `brand: none` *(default)* | His measured palette and scale. No brand marks, and **no identity text of any kind**. Safe to submit double-blind. |
| `brand: <path to a DESIGN.md>` | A named design system supplies the palette, the ground polarity and the typeface. Logo and wordmark are placed from its `assets:` key. |

When branded, the **default system is `asta/DESIGN.md`** from Ai2's design repo.

---

## `brand: none` — what "anonymous" covers

Strip **both** halves. Stripping only the visuals is the failure this mode exists to prevent,
because it fails silently: the deck looks anonymised, the reviewer reads an acknowledgement on
slide 51, and you find out at desk reject.

**Visual identity** — no brand palette, no logo, no wordmark, no institutional colour.

**Identity text** — no author names, no co-author list, no affiliation, no lab name, no
acknowledgements slide, no funder, and **no institution-revealing URL** (a project page on a
university domain, a lab GitHub org, a personal site, a QR code that resolves to any of them).

Three archetypes are **forbidden outright** in this mode, because their content *is* identity:

- **Paper title card** — it is the paper's own title graphic with author headshots and institution
  marks pasted in as one image. Under `brand: none` set the title as type instead.
- **Closing contact card** — QR, URL, headshots, handle. Replace it with the talk's closing
  question, which is what three of the four decks actually end on anyway.
- **Talk title card** — it carries "Sangho Suh" and nothing else. Set the talk's title alone.

Two more need care rather than removal: a **borrowed-authority quote** keeps the quoted person's
name (that is someone else's identity and it is the point of the archetype), and a **lab photo**
under a band label is a photograph of the authors — cut it.

Sangho chose the strict scope. Do not narrow it on the grounds that a particular venue's policy is
looser; say what you stripped in the handback and let him add anything back.

---

## `brand: <DESIGN.md>` — what a brand pack may and may not override

This table is the whole feature. Read the tag column of `references/never-list.md` alongside it.

| Layer | `brand: none` | `brand: <DESIGN.md>` |
|---|---|---|
| Palette, ground polarity | measured (91.3% neutral, white ground) | **overridden** |
| Typeface | as measured | **overridden** |
| **Absolute type sizes** | 112 / 84 / 50 / 36 / 24 pt | **KEPT — the brand supplies ratios only** |
| Density (9-word median) | kept | **kept** — behavioural, not visual |
| Archetypes, narrative arc | kept | **kept** |
| Never-list — `structural` entries | enforced | **enforced** |
| Never-list — `visual` entries | enforced | **the brand may overrule** |
| Logo, wordmark, affiliation | omitted | placed from `assets:` |

Two consequences worth stating out loud, because both read as over-caution until you hit them:

- A brand pack cannot license a results chart, a template title on a slide that does not need
  one, decorative stock photography, a colour that means two things, or ending on a takeaways
  slide. Those are `structural`.
- A brand pack *can* license a gradient ground and a framed, shadowed screenshot card. Those are
  the two `visual` entries, and a design system is entitled to its own opinion about them.

---

## Finding 1 — the Ai2 type scale cannot be transplanted

Ai2's scale is a **screen** scale. `display` is `3rem` and `heading-xl` is `2.5rem`, in PP
Telegraf. At a 16 px root that is **48 pt and 40 pt**, against his measured Display of **112 pt**
and Title of **84 pt** — 43% and 48% of the sizes he actually presents at.

Apply the brand's absolute sizes and the deck comes out less than half size, **and it looks like a
faithful brand application the whole way down**: every token is correct, every name is correct, the
type is simply too small to read from the back of a room. There is no error to notice.

**So: take the typeface, the weights and the line heights. Do not take the point sizes.** Keep
112 / 84 / 50 / 36 / 24. If you need a step the derived scale does not name, take the *ratio* from
the brand and scale it so the top of the ladder lands on 112 pt — Asta's own ladder, rescaled that
way, is 112 / 93 / 75 / 56 / 47, which is not his scale and should not replace it.

Two things carry over unchanged from `visual-language.md` and do not become brand decisions:
hard-code a size only for the **slide number** and the **slide title**, and set everything else to
fit. Quotes and figure labels are genuinely sizeless — 20 distinct sizes across 39 quote spans.

---

## Finding 2 — branding can invert the ground, and contrast-defined archetypes do not survive the flip

His corpus is a near-white ground with black ink: 263 of 365 slides white, 61 cream, and colour on
8.7% of pixels. **Asta is dark mode** — ground `extra-dark-teal #032629`, text `cream #faf2e9`.

That is not a repaint. Several archetypes are *defined by* a contrast direction, and flipping the
ground reverses them: the dark band label vanishes into a dark ground and has to become a light one,
and greying-back has to grey *up* instead of down.

**But the rule's reach is narrower than it looks, and assuming otherwise is how it breaks things.**
Of the twenty-three archetypes, the inversion rule governs **six**. Sorting every re-specification
in [`polarity.md`](polarity.md) by *why* it needs one: 6 turn on a contrast, 6 are an
asset-provenance problem (light-ground artwork he did not draw — paper figures, other people's
screenshots, cut-out portraits), and 1 is machine readability (the QR on the contact card). Only the
first six are a polarity question at all.

**And one archetype is defined by absence rather than contrast, so it does not invert: the
blackout.** A blackout on a dark ground is still black — confirmed by Sangho, 2026-09-13. The
general rule would have made it a bright slide, which is the opposite gesture. The reasoning and the
rejected alternative are in [`polarity.md`](polarity.md) §3; do not re-derive them here.

**The mapping is worked through once, per archetype, in [`polarity.md`](polarity.md).** Read it
before rendering any branded deck on a dark ground. Do not re-derive it per deck.

**Note that the inversion is Asta's, not Ai2's.** Strata — the base system both products are
composed from — is **light**: `background: cream`, `text: dark-teal`. So `strata/DESIGN.md` needs
the palette swap and nothing from `polarity.md`, while `asta/DESIGN.md` needs both. Check the
`background` / `text` semantic aliases of whatever DESIGN.md you are handed before assuming which
case you are in; a third system may be either.

---

## Fetching a DESIGN.md

**Do not vendor these files into this repo.** They are Ai2's, they are versioned there, and a copy
here drifts silently — the failure would be a deck built to a palette Ai2 retired.

```bash
git clone --depth 1 https://github.com/allenai/design /tmp/ai2design
```

Then read `/tmp/ai2design/asta/DESIGN.md` (or `strata/`, `olmo-earth/`). Each product file is
**fully resolved** — no inheritance to follow, no build step — so one file is the whole system.

DESIGN.md is [an open format from Google](https://github.com/google-labs-code/design.md): YAML
token frontmatter (`colors`, `typography`, `spacing`, `rounded`, `components`, `assets`) plus
markdown prose explaining why the values exist. Read the prose as well as the tokens; it is where a
system says which of its own colours are load-bearing.

What to pull out of it, in order:

1. `colors.background` and `colors.text` — this is the polarity check above.
2. The **two or three** accent colours, from the `interactive-*` / `link` aliases. Not the whole
   primitive palette. He spends colour a word at a time; a brand pack is a source of hues, not a
   licence to use more of them.
3. `typography.*.fontFamily` and `fontWeight` — the faces. **Not `fontSize`.**
4. `assets.logo` / `assets.wordmark` — relative to the DESIGN.md, so grab the `assets/` folder
   beside it. Place them on the title card and the closing card only; his own chrome habit is that
   marks belong to the talk's frame and switch off inside the material the frame carries.

If the brand supplies a font you cannot embed in the render path, say so and fall back to the
nearest available face rather than silently substituting one — a wrong face is the most visible
half of a brand and the easiest to spot.
