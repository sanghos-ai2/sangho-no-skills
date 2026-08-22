# Personalizing the `no-skills` fork for Sangho Suh

**Status:** approved
**Date:** 2026-08-21
**Branch:** `sangho` (GitHub default; upstream `main` untouched)
**Scope:** rebrand the fork, retarget `write-like-joseph` onto Sangho's corpus, retune tooling config.

## Context

`sangho-no-skills` is a fork of `josephcc/joseph-no-skills`: three self-contained Claude Code
skills symlinked into `~/.claude/skills/` by `install.sh`. The fork is personal; no changes go
back upstream, and no `upstream` remote is configured.

Two of the three skills are person-neutral. `codex-audit` is about a tool, `interactive-plan`
about a format. Only `write-like-joseph` encodes an identity, and it does so empirically: nearly
every rule in it cites a frequency count measured against ~102k words of Joseph Chee Chang's
published prose. Renaming it without recomputing those counts would leave a skill full of
confident numbers that are false about Sangho. That recomputation is the bulk of this work.

## Corpus

Eight first-author full papers, from `~/Github/sanghosuh.github.io/papers/`:

| Paper | Venue | Year | File |
|---|---|---|---|
| StoryEnsemble | UIST | 2025 | `storyensemble_uist.pdf` |
| Luminate | CHI | 2024 | `luminate_chi.pdf` |
| Sensecape | UIST | 2023 | `sensecape_uist.pdf` |
| CodeToon | UIST | 2022 | `codetoon_uist.pdf` |
| PrivacyToon | DIS | 2022 | `privacytoon.pdf` |
| Using Comics to Introduce and Reinforce Programming Concepts in CS1 | SIGCSE | 2021 | `comics_sigcse.pdf` |
| Coding Strip | VL/HCC | 2020 | `codingstrip_vlhcc.pdf` |
| How Do We Design for Concreteness Fading? | IDC | 2020 | `concreteness_idc.pdf` |

Excluded by decision: all co-authored papers where Sangho is not first author (they teach someone
else's prose); doctoral-consortium and short pieces; the ML papers (`lensnmf_*`, `revacnn_*`,
different section grammar); and `codetoon_iui.pdf` (5pp short paper — compressed register would
skew the counts).

`codingstrip_vlhcc.pdf` uses an IEEE template with a 10pt body, and the generic
bold-and-larger-than-modal-body heading rule finds nothing in it. It needs a per-paper heading
override rather than exclusion.

## Section taxonomy

Derived from the papers' actual headings rather than inherited from Joseph's map.

Carried over: `abstract/`, `introduction/`, `related-work/` (widened to match both `RELATED WORK`
and `BACKGROUND`, which Sangho uses at similar rates), `formative-study/`, `design-goals/`
(matches `Design Objectives` too), `example-user-scenario/`, `system-design/`, `discussion/`,
`conclusion/`.

Renamed: `lab-study/` becomes `study-method/`, matching `USER STUDY` / `USER EVALUATION` /
`METHODS`.

New:
- `rq-results/` — Sangho's findings sections are RQ-structured (`RQ1. How does Sensecape support
  exploration?`) across four papers. Joseph's map assumes prose-headed findings and has no slot
  for this.
- `framework/` — conceptual contributions (Luminate's design-space framework, the concreteness
  fading taxonomy and design dimensions). Joseph writes only system papers; Sangho does not.
- `survey-method/` — systematic literature review method, distinct from a user-study method.
- `classroom-study/` — course deployment (comics_sigcse).
- `practical-implications/` — PrivacyToon's implications-and-usage-contexts section.

Dropped: `field-deployment/` (one subsection, not a section), `quantitative-results/` (fused into
RQ results), `technical-eval/` (single instance; folded into `study-method/`).

## Components

### `tools/build-corpus.py`

PDF set to `examples/<section>/<corpus_id>.md`. Stages: extract per page (PyMuPDF, verified to
handle the two-column ACM layout in correct reading order); strip non-voice text (running
headers and footers, figure and table captions, CCS Concepts, Keywords, ACM Reference Format,
Acknowledgments, References, Appendix); de-hyphenate line-broken words and reflow paragraphs;
segment on headings; map headings to section folders.

Files are named by a short paper key (`sensecape.md`) rather than the upstream convention of a
Semantic Scholar corpus id. The naming exists so the agent can follow one paper across section
folders, and a readable key serves that better than a numeric id.

De-hyphenation is not cosmetic. Raw extraction splits `turning` into `turn-\ning`, and counting
over unrepaired text corrupts every frequency in the audit.

### `tools/audit-voice.py`

Recomputes every number in the skill: Tier 1 never-words, the Tier 2 keep-list, the substitution
table, sentence-opener ranking, and em-dash rate. Reports raw counts and per-100k rates, so
thresholds stay comparable to Joseph's 102k-word baseline instead of being silently rescaled.

Em-dashes are counted as U+2014 only. The en-dash (U+2013) appears throughout venue strings and
page ranges; conflating them would produce a bogus punctuation policy.

The `should_count_block()` predicate — which text counts as voice — is a judgment call about what
the numbers mean, and is authored by Sangho rather than defaulted.

### `write-like-sangho/SKILL.md`

Rewritten from `write-like-joseph/SKILL.md`: identity, gate marker `.i-am-sangho`, placeholder
form `[TODO(sangho): …]`, the revised section map and its loading-dependency table, and every
frequency-derived rule replaced with audited numbers.

### `examples/prior-citations.md`

Reference lists parsed from the eight papers' own reference sections by
`tools/build-citation-index.py`: title, year, which papers cited it, multiply-cited work first.
Gitignored with the rest of `examples/`.

Parsed from the PDFs rather than fetched from Semantic Scholar, so the script runs offline and is
not subject to the API rate limits that made a live lookup unreliable. Both the ACM and IEEE
reference formats are handled. Yields 379 unique references, 36 of them cited more than once.

## What ships

`examples/` stays gitignored: the prose is personal and not for distribution. The scripts and the
audited numbers in `SKILL.md` do ship. This split is inherited from upstream and is correct — the
findings about the writing travel, the writing itself does not.

## Other changes

- Tier A rebrand: `README.md`, `NOTICE`, `LICENSE` copyright, `install.sh`, `.gitignore`, skill
  directory name and frontmatter.
- `interactive-plan` editor command becomes `cursor --goto {path}:{line}:{col}`, in
  `config.json`, the fallbacks in `app/server.mjs`, and the docs that name Zed.
- `codex-audit` is kept unchanged; the README gains its install step.
- Per-repo git credential config so pushes authenticate as `sanghos-ai2` without switching the
  global `gh` account.

## Out of scope

Rewriting `interactive-plan/examples/interactive-plan-skill.plan.md`. It is the actual plan
document that built the upstream skill, Joseph's design rationale included, and it is kept as
provenance rather than rewritten as history that isn't Sangho's.
