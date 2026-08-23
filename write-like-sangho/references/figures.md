# Figures — what Sangho's papers actually do

Derived by reading the figures in **Sensecape** (UIST 2023, 14 figures / 18pp),
**Luminate** (CHI 2024, 12 / 26pp), and **StoryEnsemble** (UIST 2025, 20 / 36pp),
plus caption inventories from the rest of the corpus. Read this before planning a
figure set or capturing a screenshot, the same way `SKILL.md` is read before
writing a sentence.

The headline number first, because it reframes most figure discussions: **these
papers carry 12–20 figures.** A systems paper with two or three is not a thinner
version of this corpus, it is a different kind of paper. Figures here are load
bearing, not decoration.

## The eight figure types, in the order they appear

| # | Type | Span | Badges | Example |
|---|---|---|---|---|
| 1 | **Teaser** — the contribution as a diagram | full width, above the abstract | letters | StoryEnsemble Fig 1 |
| 2 | **Framework / approach** — the conceptual claim, usually comparative | full width | letters | Luminate Fig 1 (A & B prior paradigms, C ours) |
| 3 | **Interface overview** — the whole UI, once | full width | letters | Luminate Fig 3 (A–K) |
| 4 | **Workflow** — one scene walked through in order | full width | **numbers** | Sensecape Fig 3 (1–6) |
| 5 | **Feature close-up** — one mechanism, tight crop | single column | numbers | Sensecape Figs 5–7 |
| 6 | **Baseline / condition** — what the study compared against | either | letters | Sensecape Fig 8 |
| 7 | **Evaluation chart** — Likert or per-feature ratings | either | none | Luminate Fig 12 |
| 8 | **Participant artifacts** — real workspaces from the study | full width | numbers | Sensecape Figs 12–14, StoryEnsemble 16–19 |

Types 1–4 are the spine. A systems paper missing an interface overview or a
workflow figure is missing something reviewers expect.

## The teaser is an argument, not a screenshot

StoryEnsemble Fig 1 is the clearest case: three diverge/converge diamonds, one
per design stage, with forward propagation drawn in blue and backward in grey,
and a *single* storyboard screenshot embedded at the bottom as the concrete
payoff. The diagram carries the paper's mechanism; the screenshot proves it
exists.

Sensecape Fig 1 does the lighter version — two UI states side by side with a
double-headed arrow between them, because the contribution *is* the movement
between those states.

So: a teaser that is just a screenshot of the system is a missed teaser. Ask what
claim the figure has to make, draw that, and let a screenshot sit inside it.

## Badges: letters for anatomy, numbers for sequence

This distinction is consistent across all three papers and it is the single most
useful convention here.

- **Letters** label the *parts* of a thing that exists all at once. Luminate Fig 3
  tags eleven regions of one static interface A–K.
- **Numbers** label *steps* that happen in order. Sensecape Fig 3 walks one canvas
  through six actions, with dashed grey arrows between them showing the flow.

Badges are **black filled circles with a white glyph**, placed *on* the artifact
at the thing they name — not in a margin, not in a legend. If a badge cannot sit
on the thing, the crop is wrong.

## Captions do argumentative work

Captions are long, and they narrate every badge in order. Luminate Fig 3's caption
is six sentences that read A through K as a tour: *"(A) text editor and (F)
exploration view. Users can (B) type and use various (C) text styles… They have
the option to (D) input a prompt… and view (E) one of the generated responses."*

Sensecape Fig 3's caption is one continuous sequence: *"A user asks Sensecape to
(1) generate a list of questions… Sensecape (2) updates the canvas topic… the
user (3) highlights 'Transportation' to create a node and (4) groups it…"*

A caption reading "The Atlas interface" is not a caption in this corpus. Write the
tour.

## Referencing from prose

The prose form is **`Fig. 3D`** — figure number and badge concatenated, no
parentheses around the badge: *"On the right side of the interface (Fig. 3B) is
the exploration view."* For numbered workflow figures it is `Fig. 3 (2)`.

Prose references individual badges constantly. Luminate §4.1 cites Fig. 3A, 3B,
3D, 3E, 3G, 3J within two paragraphs. If a figure has badges the prose never
names, either the prose is under-written or the badges are.

## Screenshot hygiene

Every screenshot in the corpus follows all of these:

- **No browser chrome, no OS window frame, no cursor.** The figure shows the
  application, not a computer.
- **Light UI on white.** Nothing in the corpus is a dark-theme screenshot. A dark
  figure prints heavy and fights the page.
- **Cropped tight to the meaningful region**, zoomed far enough that body text in
  the UI is legible at print size. Sensecape Fig 1 shows a handful of nodes, not a
  whole workspace at true scale.
- **Real content, never lorem ipsum.** Sensecape's screenshots carry an actual San
  Francisco relocation inquiry; Luminate's carry a real poem. The scenario is
  illustrative but the content is coherent and specific.
- **Citable objects must be real.** A screenshot showing paper titles is showing
  citations. Invented titles in a figure are fabricated references — capture real
  ones.

## Color

Near-greyscale by default; the UI's own light greys and one accent. Color enters
when it *encodes* something: StoryEnsemble gives each design stage its own hue and
draws the two propagation directions in different colors, because direction is the
contribution. Color for liveliness alone does not appear.

## Each figure answers a named challenge

Sangho's addition to this guide, and the one that should drive the plan: when the
paper names its challenges, the figure set should map onto them, so a reader can
see which picture answers which problem. Sensecape does this implicitly — its
subsection headings carry `[C2-4, C6]` tags and the figures sit beside them — but
state it explicitly when planning.

Worked example, from the Atlas paper:

| Challenge | The figure that answers it |
|---|---|
| Representational cost | one artifact set shown in four layouts, side by side |
| Decision opacity | the decision-tree walkthrough, with ruled-out paths visible |

A challenge with no figure is a claim the reader has to take on trust. A figure
answering no challenge is decoration.

## Vary the content types across the figure set

Also Sangho's, and it does not generalize from the older papers because their
content was homogeneous — Sensecape's nodes are all text, Luminate's are all
generated responses. When the system's content is **typed**, the figure set has a
second job beyond explaining the interface: it demonstrates range.

So do not show the same artifact type in every figure. If the interface overview
shows a paper set, the multi-layout figure should show hypotheses or findings, and
at least one figure should show a **heterogeneous set the user composed
themselves** — mixed types in one view. A figure set that shows papers six times
implies the system handles papers, which understates it.

Check the plan as a set, not figure by figure: list the artifact types appearing
in each, and if one type appears everywhere or a supported type appears nowhere,
rebalance before capturing.

## Planning a figure set

Work backwards from the claims, not forwards from the screenshots you can take:

1. **What is the contribution?** → the teaser diagram (type 1).
2. **What is the conceptual argument?** → the framework figure (type 2), usually
   comparative so the reader sees what is new.
3. **What does the system look like?** → one interface overview (type 3), lettered.
4. **What does using it look like?** → one workflow (type 4), numbered, following
   the scenario the introduction set up.
5. **Which mechanisms need their own picture?** → feature close-ups (type 5), one
   per mechanism the prose explains in detail.
6. **What did the study compare?** → the baseline figure (type 6).
7. **What did the study find?** → the evaluation chart (type 7).
8. **What did participants actually build?** → their workspaces (type 8).

Then check the set three ways: each figure's badges are referenced in prose;
each named challenge has a figure; and the artifact types are varied rather than
one type repeated. A figure whose badges are never referenced, a claim with no
figure, and a figure set that shows one content type six times are all mismatches
to fix before submission.

## Capturing from a live system

The script that drives a capture is specific to one system's DOM and belongs in that
system's repo. The *method* is not, and it cost a full session to learn. Five rules,
each from a failure that produced a plausible-looking wrong figure:

**Suppress onboarding before the app boots.** A fresh browser profile is a
first-run profile, so tutorial pickers and welcome modals open over the whole
workspace. Set whatever flag dismisses them in an init script that runs *before*
page load; setting it afterwards is too late and the modal is already in the shot.

**Open collapsed panels, and verify by geometry.** Panels that are collapsed are
usually still in the DOM at zero width, so `querySelector` finding an element proves
nothing about whether it is visible. Check the bounding box before trusting a
screenshot.

**Assert the state you think you set.** Clicking a disabled control is frequently a
silent no-op that leaves the previous state active — so the capture succeeds, looks
reasonable, and shows the wrong thing. Read back the control's pressed/active
attribute after every click and fail if it did not change.

**An ambiguous selector is worse than a missing one.** A selector matching nothing
fails loudly. One matching the *wrong* element returns plausible data and sends you
debugging phantoms: a substring that matched both "Findings — X" and the set actually
wanted cost three wrong diagnoses in a row. Fail on multiple matches, not just zero.

**Poll for availability rather than checking once.** Controls can be transiently
disabled while background work runs — a dimension pass, a layout computation. A
single check after a fixed wait cannot tell a mid-computation blip from a structural
limit. Poll to a generous ceiling, then fail with the reason the UI gives.

And one framing rule: crop to the element you mean. A wrapper named for the workspace
often contains the whole chrome, so cropping to it silently includes panels the figure
should not carry. Park the pointer somewhere neutral before shooting, or the hover card
of whatever you last clicked sits in the middle of the figure.

**Expect to reach for a mockup anyway.** Screenshots are bound to the system's own
zoom and aspect ratio, and semantic-zoom interfaces trade legibility against how much
fits: fitting a set can drop nodes below the threshold where they render as readable
cards. When the claim needs more in frame than the system will show legibly, rebuild
the figure in a drawing tool and treat the screenshot as reference.

## When the walkthrough spans several UI states

A workflow figure normally shows *one* scene walked through by numbers, which
works when the movement happens within a single view. When the walkthrough moves
between genuinely different views — a layout switch, a different panel — the
precedent is Sensecape Fig 1: the states side by side with an arrow between them,
each badged. Combine the two: panels for the distinct states, **numbers** for the
order, arrows for the movement, and a caption that narrates the numbers as one
continuous action.
