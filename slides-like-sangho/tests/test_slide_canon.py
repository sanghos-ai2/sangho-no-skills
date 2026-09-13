import os
import pathlib
import pytest

from tools.slide_canon import (
    CANON, CanonError, by_slug, resolve_key, resolve_pdf,
)


def test_canon_has_four_decks_one_in_wave_one():
    assert len(CANON) == 4
    assert [d.slug for d in CANON if d.wave == 1] == ["luminate"]


def test_job_talk_key_relpath_keeps_its_trailing_space():
    # The real directory is named "2024 job-talk " — stripping it yields a
    # path that does not exist, and the failure reads as "deck not found".
    deck = by_slug("job-talk")
    assert deck.key_relpath.startswith("2024 job-talk /")


def test_resolve_key_rejects_a_size_mismatch(tmp_path):
    deck = by_slug("sensecape")
    target = tmp_path / deck.key_relpath
    target.parent.mkdir(parents=True)
    target.write_bytes(b"wrong deck, right filename")
    with pytest.raises(CanonError, match="expected"):
        resolve_key(deck, tmp_path)


def test_resolve_key_accepts_when_size_matches(tmp_path):
    deck = by_slug("sensecape")
    target = tmp_path / deck.key_relpath
    target.parent.mkdir(parents=True)
    # Sparse fixture: deck.key_bytes is 681,436,109 for this deck. Writing that
    # many real bytes would allocate 681 MB per test run. os.truncate sets
    # stat().st_size exactly (what resolve_key's size check reads) without
    # allocating the underlying blocks on APFS.
    target.write_bytes(b"")
    os.truncate(target, deck.key_bytes)
    assert resolve_key(deck, tmp_path) == target


def test_resolve_pdf_missing_names_the_deck(tmp_path):
    with pytest.raises(CanonError, match="luminate"):
        resolve_pdf(by_slug("luminate"), tmp_path)


def test_by_slug_rejects_unknown():
    with pytest.raises(CanonError):
        by_slug("nope")
