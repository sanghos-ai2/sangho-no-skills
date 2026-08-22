---
name: fetching-bibtex
description: Use when a LaTeX paper has unresolved citation placeholders (\needcite, [CITE], TODO cite, "cite me") or a references.bib is missing entries, and the BibTeX must come from publisher-quality sources rather than being written by hand or pulled from a model's memory.
---

# Fetching BibTeX

## Overview

Filling a `references.bib` from memory fabricates plausible-looking entries:
right title, invented pages, wrong venue, hallucinated DOI. Reviewers catch
these. **Every entry must come from a publisher-deposited record**, and every
entry must be auditable back to the query that found it.

Core principle: **a wrong-but-plausible citation is worse than a visible
unresolved placeholder.** Never swap a placeholder for a `\cite{}` you have not
verified.

## When to Use

- A `.tex` file has `\needcite{}`, `[CITE]`, `\todo{cite}`, or bare `[?]` marks
- `references.bib` is thin or empty but the prose cites many works
- BibTeX exists but lacks the DOI / full booktitle / pages that
  `ACM-Reference-Format` or `IEEEtran` requires
- Migrating a draft (Markdown, Google Docs, Word) into LaTeX

**Do NOT use** to invent a citation for a claim that has no source, or to guess
which paper a bare name like "the AI Scientist" refers to. Ask the author.

## Source Selection

| Source | Best for | Gets you | Gap |
|---|---|---|---|
| **DBLP** | CS/HCI proceedings (ACM, IEEE) | full booktitle, pages, DOI, editors, correct `@inproceedings` | CS only |
| **Crossref** | journals, most non-CS | DOI-negotiated BibTeX | poor book coverage |
| **OpenAlex** | books, theses, grey lit | broadest index | no BibTeX endpoint; must hand-build when no DOI |
| **Semantic Scholar** | last resort | `--fields citationStyles` | see below |

**Semantic Scholar's BibTeX is generated from its own extracted metadata**, so
PDF-extraction noise leaks into it. Observed on the GPT-3 paper: `@Article` for
a NeurIPS paper, initials instead of first names (`J. Kaplan`), a hyphenation
artifact (`Ma-teusz Litwin`), both `booktitle` AND `journal = {ArXiv}`, and no
DOI/pages/publisher. Usable to identify a paper; not to cite it. Reach for it
only when the other three miss. Via asta: `asta papers get <ID> --fields
title,year,citationStyles` (undocumented in `--help`, but the flag is an S2 API
passthrough).

## Quick Reference

```bash
# one query
python3 fetchbib.py --query "Sensecape multilevel sensemaking Suh 2023"

# batch: TSV of  citekey <TAB> query
python3 fetchbib.py --file queries.tsv --bib references-new.bib
```

Each result is stamped:

| Stamp | Meaning | Action |
|---|---|---|
| `OK` | matched record agrees with query on surname AND year | safe to use |
| `REVIEW` | year or surname disagreed | read it before using |
| `MISS` | no hit in any source | find it by hand |

## Writing Good Queries

Author + year alone is not enough — it returns the author's most-cited paper,
not the one you meant. **Include distinguishing title terms.**

```
# ✗ returns whatever Kang is most cited for
kang2022threddy    Kang 2022
# ✓
kang2022threddy    Threddy interactive threading scholarly literature Kang 2022
```

## Gotchas That Cost Real Time

- **DBLP's default `?param=0` is not enough.** It collapses the booktitle to
  `{{UIST}}` and omits the DOI. `ACM-Reference-Format` needs the full
  proceedings title — always `?param=1`.
- **DBLP indexes both the proceedings paper and its arXiv preprint.** Citing the
  CoRR version of a published paper is a real error; prefer the venue. The
  script sorts `venue == 'CoRR'` last.
- **DBLP returns sporadic HTTP 500s.** A bare `q=Sensecape` failed twice while a
  longer query succeeded seconds later. Any client needs retry-with-backoff, or
  you will read a transient 500 as "paper not indexed".
- **`urllib` is blocked in some sandboxes while `curl` is not.** The script
  shells out to `curl` for this reason. If you rewrite it with `requests`,
  expect SSL failures that look like network outages.
- **Books mostly aren't in Crossref.** Weick 1995, Hutchins 1995, Suchman 1987
  resolve via OpenAlex, often with no DOI, so the entry is hand-built from
  OpenAlex fields and always deserves a read.
- **Rekey the entries.** DBLP emits `DBLP:conf/uist/SuhMPX23`. Fine as a key,
  awful to type in prose. The script rewrites it to your chosen citekey.

## Workflow

1. **Extract** placeholders from the `.tex`, with counts, by brace-matching
   (not a naive regex — nested braces are common).
2. **Split** into resolvable (has author + year) vs bare (`[CITE]`, a bare
   system name). Bare ones go back to the author; do not guess.
3. **Write** `queries.tsv` — one line per unique work, citekey + distinguishing
   terms.
4. **Run** `fetchbib.py --file ... --bib ...`.
5. **Read every `REVIEW` and every hand-built entry.** This is the step that
   makes the difference; do not skip it.
6. **Only then** swap `\needcite{X}` → `\cite{key}`, and recompile. BibTeX
   warns on undefined keys — a clean `*.blg` is the check that you got them all.

## Common Mistakes

| Mistake | Consequence |
|---|---|
| Writing BibTeX from model memory | fabricated pages/DOIs; reviewers notice |
| Auto-swapping every placeholder | silently wrong citations, no trace of which |
| Trusting a first hit on author+year | cites the author's *other* paper |
| Treating a 500 as "not found" | re-typing an entry that was one retry away |
| Using S2 BibTeX for camera-ready | wrong entry type, initials, no DOI |
