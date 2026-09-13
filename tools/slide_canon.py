#!/usr/bin/env python3
"""The canon of Sangho's talks, resolved by explicit path.

Never resolve a canon deck by glob or filename search. Two distinct decks share
the name "uist2023 - sensecape (10-30-2023).key": 271 MB (Oct 27) at the corpus
root and 681 MB (Oct 30) in conferences/. UIST'23 ran Oct 29 - Nov 1, so the
larger, later file is talk day. Byte size is therefore verified, and a mismatch
is a loud failure rather than a fallback.
"""
from __future__ import annotations

import dataclasses
import pathlib

CORPUS_ROOT = pathlib.Path.home() / ".cache" / "slides-like-sangho" / "corpus"
PDF_INBOX = pathlib.Path.home() / "Desktop" / "slides-like-sangho"
KEY_ROOT = pathlib.Path.home() / "Desktop" / "presentation" / "previous"


class CanonError(RuntimeError):
    """A canon deck could not be resolved, or resolved to the wrong bytes."""


@dataclasses.dataclass(frozen=True)
class Deck:
    slug: str
    title: str
    pdf_name: str
    key_relpath: str
    key_bytes: int
    pages: int
    wave: int


# NOTE: "2024 job-talk /" ends in a space. That is the real directory name.
CANON: tuple[Deck, ...] = (
    Deck(
        slug="luminate",
        title="Luminate @ CHI'24",
        pdf_name="chi2024-luminate-presentation.pdf",
        key_relpath="2024-05-14 Luminate @ CHI/chi2024-luminate-presentation.key",
        key_bytes=151209601,
        pages=55,
        wave=1,
    ),
    Deck(
        slug="sensecape",
        title="Sensecape @ UIST'23",
        pdf_name="uist2023 - sensecape (10-30-2023).pdf",
        key_relpath="conferences/uist2023 - sensecape (10-30-2023).key",
        key_bytes=681436109,
        pages=32,
        wave=2,
    ),
    Deck(
        slug="kaist",
        title="KAIST invited talk",
        pdf_name="kaist-talk-v2.pdf",
        key_relpath="2023-12-09 talk @ kaist - Dec, 2023/kaist-talk-v2.key",
        key_bytes=630342815,
        pages=126,
        wave=2,
    ),
    Deck(
        slug="job-talk",
        title="Job talk 2024",
        pdf_name="job-talk-uninhabited-space-of-intelligence.pdf",
        key_relpath="2024 job-talk /job-talk-uninhabited-space-of-intelligence.key",
        key_bytes=901159834,
        pages=152,
        wave=2,
    ),
)


def by_slug(slug: str) -> Deck:
    for deck in CANON:
        if deck.slug == slug:
            return deck
    known = ", ".join(d.slug for d in CANON)
    raise CanonError(f"unknown deck {slug!r}; canon is: {known}")


def resolve_pdf(deck: Deck, inbox: pathlib.Path | None = None) -> pathlib.Path:
    path = (inbox or PDF_INBOX) / deck.pdf_name
    if not path.is_file():
        raise CanonError(
            f"{deck.slug}: no exported PDF at {path}. Export from Keynote with "
            f"Layout=Slides, Image Quality=Best, builds off."
        )
    return path


def resolve_key(
    deck: Deck,
    root: pathlib.Path | None = None,
    *,
    verify_size: bool = True,
) -> pathlib.Path:
    path = (root or KEY_ROOT) / deck.key_relpath
    if not path.is_file():
        raise CanonError(f"{deck.slug}: no .key at {path}")
    if verify_size:
        actual = path.stat().st_size
        if actual != deck.key_bytes:
            raise CanonError(
                f"{deck.slug}: expected {deck.key_bytes} bytes at {path}, found "
                f"{actual}. Refusing: filenames are not unique in this corpus."
            )
    return path
