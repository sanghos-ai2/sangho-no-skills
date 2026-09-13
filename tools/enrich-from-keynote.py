#!/usr/bin/env python3
"""Enrich corpus manifests with presenter notes and master-slide vocabulary,
read straight out of the IWA payload inside each canon `.key` file.

    uv run --with keynote-parser python tools/enrich-from-keynote.py --wave 1
    uv run --with keynote-parser python tools/enrich-from-keynote.py --all

This is the one enrichment pass that needs the `.key` itself rather than the
exported PDF: presenter notes and Keynote master-slide names never reach the
PDF at all. It is also the one pass allowed to fail per-deck without failing
the corpus. `extract()` is wrapped in `try/except Exception` and degrades to
`({}, [])` on any error — an unreadable/unsupported `.key` leaves the
manifest exactly as Tasks 1-3 left it (`masters: []`, no `notes` key on any
slide) rather than raising and blocking every other deck's enrichment.

Verified shape (keynote-parser 1.14.5.0, against the real Luminate .key,
Keynote format T13.1):

  - `Index/Document.iwa` holds one `KN.ShowArchive` object with
    `slideTree.slides`: the ordered list of `KN.SlideNodeArchive` ids as they
    appear in the show (this is the presentation order the PDF export also
    walks). Each `KN.SlideNodeArchive` carries `isSkipped` (a slide hidden
    from the show, and so absent from the exported PDF too) and
    `slide.identifier`, the id of that slide's own `KN.SlideArchive`.
  - A `KN.SlideArchive`'s real content is split across `Index/Slide-<id>.iwa`
    (one file per frequently-edited slide) *and* one shared `Index/Slide.iwa`
    that batches the rest — an archive id can land in either, so both must be
    merged into one lookup table before resolving anything by id.
  - A `KN.SlideArchive` optionally carries `note: {identifier: ...}`, pointing
    at a `KN.NoteArchive` (same slide-family lookup table) whose
    `containedStorage.identifier` points at a `TSWP.StorageArchive` (kind
    `NOTE`) carrying the actual presenter-note paragraphs in `text: [str]`.
    No `note` key, or an empty `text`, means the slide has no presenter note
    at all -- a real `None`, not a failure.
  - Each `KN.SlideArchive` also carries `templateSlide: {identifier: ...}`,
    which names which `Index/TemplateSlide-<id>.iwa` file supplied its
    master. Each such file's root `KN.SlideArchive` object has a plain `name`
    field (e.g. "Title & Bullets") -- the master vocabulary is just every
    distinct name across a deck's `TemplateSlide-*` files, in ascending id
    order, deduplicated (the Luminate deck has 13 such files but only 12
    distinct names -- "Title" appears twice).
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import traceback

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from tools.slide_canon import (  # noqa: E402
    CANON,
    CORPUS_ROOT,
    CanonError,
    Deck,
    resolve_key,
)


def merge_extraction(
    manifest: dict,
    notes_by_index: dict[int, str | None],
    masters: list[str],
) -> dict:
    """Pure merge: stamp `masters` and any known-index `notes` onto a manifest.

    An index absent from `notes_by_index` gets no `notes` key at all -- that
    is what keeps a total extraction failure (`notes_by_index == {}`) from
    reading as "every slide has no notes" instead of "we never looked".
    """
    manifest["masters"] = list(masters)
    for slide in manifest["slides"]:
        if slide["index"] in notes_by_index:
            slide["notes"] = notes_by_index[slide["index"]]
    return manifest


def _merge_objects_by_id(data: dict, into: dict[str, list[dict]]) -> None:
    for chunk in data.get("chunks", []):
        for archive in chunk.get("archives", []):
            hid = archive["header"]["identifier"]
            into.setdefault(hid, []).extend(archive.get("objects") or [])


def _find(objs_by_id: dict[str, list[dict]], oid: str, pbtype: str) -> dict | None:
    for obj in objs_by_id.get(oid, []):
        if obj.get("_pbtype") == pbtype:
            return obj
    return None


def _note_text(slide_map: dict[str, list[dict]], slide_root: dict) -> str | None:
    note_ref = slide_root.get("note")
    if not note_ref:
        return None
    note_arch = _find(slide_map, note_ref["identifier"], "KN.NoteArchive")
    if not note_arch:
        return None
    storage_ref = note_arch.get("containedStorage")
    if not storage_ref:
        return None
    storage = _find(slide_map, storage_ref["identifier"], "TSWP.StorageArchive")
    if not storage:
        return None
    text = "".join(t for t in (storage.get("text") or []) if isinstance(t, str))
    return text.strip() or None


def extract(key_path: pathlib.Path) -> tuple[dict[int, str | None], list[str]]:
    """Read presenter notes + master-slide names straight out of a `.key`.

    Returns `(notes_by_index, masters)`. `notes_by_index` covers every
    slide actually shown in the presentation (`isSkipped: false`), 1-based
    in show order, mapping to the note text or `None` when that slide
    genuinely carries no presenter note. `masters` is the deck's distinct
    TemplateSlide names, in ascending template-id order.
    """
    from keynote_parser.codec import IWAFile
    from keynote_parser.file_utils import file_reader

    doc_map: dict[str, list[dict]] = {}
    slide_map: dict[str, list[dict]] = {}
    master_names: dict[int, str] = {}

    for filename, handle in file_reader(str(key_path), progress=False):
        if not (filename.startswith("Index/") and filename.endswith(".iwa")):
            continue
        base = filename[len("Index/") : -len(".iwa")]
        data = IWAFile.from_buffer(handle.read(), filename).to_dict()

        if base == "Document":
            _merge_objects_by_id(data, doc_map)
        elif base == "Slide" or base.startswith("Slide-"):
            _merge_objects_by_id(data, slide_map)
        elif base.startswith("TemplateSlide-"):
            tid = int(base.split("-", 1)[1])
            objs_by_id: dict[str, list[dict]] = {}
            _merge_objects_by_id(data, objs_by_id)
            for objs in objs_by_id.values():
                for obj in objs:
                    if obj.get("_pbtype") == "KN.SlideArchive" and obj.get("name"):
                        master_names[tid] = obj["name"]

    show = None
    for objs in doc_map.values():
        for obj in objs:
            if obj.get("_pbtype") == "KN.ShowArchive":
                show = obj
                break
        if show is not None:
            break
    if show is None:
        raise ValueError("no KN.ShowArchive found in Index/Document.iwa")

    node_ids = [s["identifier"] for s in show["slideTree"]["slides"]]

    notes_by_index: dict[int, str | None] = {}
    index = 0
    for node_id in node_ids:
        node = _find(doc_map, node_id, "KN.SlideNodeArchive")
        if node is None or node.get("isSkipped"):
            continue
        index += 1
        slide_ref = node.get("slide")
        slide_root = (
            _find(slide_map, slide_ref["identifier"], "KN.SlideArchive")
            if slide_ref
            else None
        )
        notes_by_index[index] = (
            _note_text(slide_map, slide_root) if slide_root else None
        )

    masters = list(dict.fromkeys(master_names[k] for k in sorted(master_names)))
    return notes_by_index, masters


def enrich_manifest(
    deck: Deck,
    *,
    key_root: pathlib.Path | None = None,
    corpus_root: pathlib.Path | None = None,
) -> dict:
    manifest_path = (corpus_root or CORPUS_ROOT) / deck.slug / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    try:
        key_path = resolve_key(deck, key_root)
        notes_by_index, masters = extract(key_path)
    except Exception:
        print(f"{deck.slug}: IWA extraction unavailable:", file=sys.stderr)
        traceback.print_exc()
        notes_by_index, masters = {}, []

    merged = merge_extraction(manifest, notes_by_index, masters)
    manifest_path.write_text(
        json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return merged


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--wave", type=int, help="enrich one phasing wave (1 or 2)")
    group.add_argument("--all", action="store_true", help="enrich every canon deck")
    args = parser.parse_args(argv)

    decks = CANON if args.all else [d for d in CANON if d.wave == args.wave]
    if not decks:
        parser.error(f"no decks in wave {args.wave}")

    for deck in decks:
        try:
            merged = enrich_manifest(deck)
        except (CanonError, FileNotFoundError) as exc:
            print(f"{deck.slug}: skipped ({exc})")
            continue
        notes_count = sum(1 for s in merged["slides"] if s.get("notes"))
        print(
            f"{deck.slug}: {len(merged['masters'])} masters, "
            f"{notes_count}/{len(merged['slides'])} slides carry presenter notes"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
