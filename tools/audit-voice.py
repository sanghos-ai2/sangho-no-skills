#!/usr/bin/env python3
"""Measure Sangho's published voice, so write-like-sangho can cite evidence.

Every frequency claim in write-like-sangho/SKILL.md comes from this script. Run it
after rebuilding the corpus; it writes tools/voice-audit.md, and those numbers are
what the skill quotes.

    uv run python tools/audit-voice.py

Counts are reported both raw and per 100k words, so a threshold stays comparable
when the paper set changes size.
"""
from __future__ import annotations

import collections
import dataclasses
import pathlib
import re

CORPUS = pathlib.Path(__file__).resolve().parent.parent / "write-like-sangho" / "examples"
REPORT = pathlib.Path(__file__).resolve().parent / "voice-audit.md"

# Words commonly banned as "LLM tells". Which of these Sangho actually uses is the
# question the audit answers; the list itself is only the set of candidates to check.
CANDIDATES = """
delve pivotal vital effortless effortlessly realm tapestry journey landscape foster
empower unlock harness underscore underscores multifaceted myriad plethora
transformative groundbreaking cutting-edge synergy boasts intricate intricacies
meticulous meticulously interplay garner testament bolster showcase showcasing
vibrant versatile enduring profound albeit leverage leverages leveraging novel
comprehensive crucial nuanced seamless seamlessly holistic utilize utilizes utilizing
interestingly importantly emerge emerged emerging robust
""".split()

# Plain alternatives, to build the "what Sangho writes instead" table.
ALTERNATIVES = {
    "importance": "important key core central critical significant",
    "inquiry": "explore explored exploring investigate investigated examine examined",
    "use": "use using used utilize based build builds building",
    "enablement": "support supports supporting help helps helping allow allows allowing enable enables enabling",
    "prior art": "prior previous existing",
    "connectives": "however furthermore moreover additionally specifically instead finally similarly",
}

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z“(])")
WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")
QUOTE_SPAN = re.compile(r"[“‘\"][^”’\"]{15,}[”’\"]")


@dataclasses.dataclass
class Block:
    """One paragraph of corpus prose, with the context needed to judge it."""
    section: str          # corpus folder, e.g. "rq-results"
    paper: str            # e.g. "sensecape"
    heading: str          # the section heading it sits under
    text: str             # the paragraph itself
    words: int            # word count
    quote_fraction: float # share of words inside quotation marks (participant speech)


# ---------------------------------------------------------------------------
# TODO(sangho): decide what counts as your voice.
#
# Every number this script produces is measured over the blocks this returns True
# for, so this predicate defines what the skill's rules are evidence *of*.
#
# The trade-offs, using the corpus as it actually is:
#   - `study-method` is 8,279 words (11%). It's your densest, most formulaic prose
#     ("We recruited 12 participants..."). Keeping it makes the counts describe how
#     you write papers; dropping it makes them describe how you argue.
#   - `rq-results` is 15,113 words (21%) and is where participant quotes live. A
#     block's `quote_fraction` tells you how much of it is someone else's words.
#     Excluding quote-heavy blocks keeps the counts yours, but loses how you frame
#     a quote, which is itself a voice marker.
#   - `abstract` is 1,049 words of maximally compressed prose. Small enough not to
#     move the totals much, distinctive enough that you may want it in.
#
# Return True to count the block. The default below counts everything, which is a
# defensible choice but not an examined one.
# ---------------------------------------------------------------------------
def should_count_block(block: Block) -> bool:
    return True


def load_blocks() -> list[Block]:
    blocks = []
    for path in sorted(CORPUS.rglob("*.md")):
        section, paper = path.parent.name, path.stem
        heading = ""
        for chunk in path.read_text().split("\n\n"):
            chunk = chunk.strip()
            if not chunk or chunk.startswith("# "):
                continue
            if chunk.startswith("## "):
                heading = chunk[3:].strip()
                continue
            words = len(WORD.findall(chunk))
            if not words:
                continue
            quoted = sum(len(WORD.findall(m.group())) for m in QUOTE_SPAN.finditer(chunk))
            blocks.append(Block(section, paper, heading, chunk, words, quoted / words))
    return blocks


def rate(n: int, total: int) -> float:
    return n / total * 100_000 if total else 0.0


def main() -> None:
    every = load_blocks()
    counted = [b for b in every if should_count_block(b)]
    text = "\n".join(b.text for b in counted)
    words = WORD.findall(text)
    total = len(words)
    freq = collections.Counter(w.lower() for w in words)

    kept_w = sum(b.words for b in counted)
    all_w = sum(b.words for b in every)
    lines = [
        "# Voice audit",
        "",
        f"Corpus: {len(every)} blocks / {all_w:,} words. "
        f"Counted: {len(counted)} blocks / {kept_w:,} words "
        f"({kept_w / all_w * 100:.0f}%).",
        "",
        "Rates are per 100,000 words.",
        "",
    ]

    by_section = collections.Counter()
    for b in counted:
        by_section[b.section] += b.words
    lines += ["## Counted by section", "", "| section | words |", "|---|---|"]
    lines += [f"| {s} | {w:,} |" for s, w in sorted(by_section.items())]
    lines.append("")

    lines += ["## Candidate LLM words", "", "| word | count | per 100k |", "|---|---|---|"]
    for w in sorted(CANDIDATES, key=lambda w: (-freq[w], w)):
        lines.append(f"| {w} | {freq[w]} | {rate(freq[w], total):.1f} |")
    lines.append("")

    lines += ["## Words used instead", "", "| group | counts |", "|---|---|"]
    for group, ws in ALTERNATIVES.items():
        parts = [f"{w} ({freq[w]})" for w in ws.split() if freq[w]]
        lines.append(f"| {group} | {' · '.join(parts)} |")
    lines.append("")

    em, en = text.count("—"), text.count("–")
    lines += [
        "## Punctuation",
        "",
        f"- em-dash (U+2014): {em} ({rate(em, total):.1f} per 100k)",
        f"- en-dash (U+2013): {en} ({rate(en, total):.1f} per 100k)",
        "",
    ]

    sents = [s.strip() for s in SENT_SPLIT.split(text) if len(WORD.findall(s)) >= 3]
    openers = collections.Counter()
    solo = {"however", "finally", "specifically", "additionally", "furthermore",
            "moreover", "similarly", "instead", "overall", "notably", "importantly",
            "interestingly"}
    for s in sents:
        toks = WORD.findall(s)[:2]
        if not toks:
            continue
        openers[toks[0] if toks[0].lower() in solo else " ".join(toks[:2])] += 1
    lines += ["## Sentence openers (top 25)", "", "| opener | count |", "|---|---|"]
    lines += [f"| {o} | {n} |" for o, n in openers.most_common(25)]
    lines.append("")

    lengths = [len(WORD.findall(s)) for s in sents]
    mean = sum(lengths) / len(lengths)
    var = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    short = sum(1 for x in lengths if x <= 12) / len(lengths)
    lon = sum(1 for x in lengths if x >= 35) / len(lengths)
    lines += [
        "## Cadence",
        "",
        f"- sentences: {len(sents):,}",
        f"- mean length: {mean:.1f} words (sd {var ** 0.5:.1f})",
        f"- short (<=12 words): {short * 100:.0f}%",
        f"- long (>=35 words): {lon * 100:.0f}%",
        "",
    ]

    REPORT.write_text("\n".join(lines) + "\n")
    print(f"{kept_w:,} of {all_w:,} words counted -> {REPORT}")
    print(f"em-dash {em} ({rate(em, total):.0f}/100k) · sentences {len(sents):,} "
          f"· mean {mean:.1f}w sd {var ** 0.5:.1f}")


if __name__ == "__main__":
    main()
