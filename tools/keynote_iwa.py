"""Shared low-level reader for Keynote `.key` IWA archives.

Two callers need to walk a `.key`'s `Index/*.iwa` protobuf archives and merge
their objects into one id-keyed lookup table: `enrich-from-keynote.py` (reads
the whole bundle for presenter notes + master-slide vocabulary) and
`build-slide-corpus.py` (reads just `Index/Document.iwa` for the deck's true
slide size, as a cross-check against the exported PDF's page size). This
module owns that primitive so the two callers can't drift into two slightly
different IWA readers, per the module docstrings' own instruction not to
duplicate the parsing logic.

`keynote_parser` is imported lazily, inside the functions that actually need
it, so importing this module never requires the optional dependency -- only
calling into it does. That laziness is load-bearing for
`build-slide-corpus.py`'s layout guard, which must degrade rather than fail
when `keynote_parser` is not installed (see that module's `_check_layout`).
"""
from __future__ import annotations

import pathlib


def merge_objects_by_id(data: dict, into: dict[str, list[dict]]) -> None:
    """Merge one parsed IWA file's archives into an id -> objects lookup,
    extending any id already present rather than overwriting it. An archive
    id can be split across a shared `Index/Slide.iwa` and per-slide
    `Index/Slide-<id>.iwa` files, so a caller merging several files must
    accumulate objects under an id, not replace them.
    """
    for chunk in data.get("chunks", []):
        for archive in chunk.get("archives", []):
            hid = archive["header"]["identifier"]
            into.setdefault(hid, []).extend(archive.get("objects") or [])


def find_show_archive(doc_map: dict[str, list[dict]]) -> dict | None:
    """The single `KN.ShowArchive` object in a `Document.iwa`-derived lookup
    table, or `None` if none is present. Carries `size` (the deck's true
    slide dimensions) and `slideTree` (presentation order)."""
    for objs in doc_map.values():
        for obj in objs:
            if obj.get("_pbtype") == "KN.ShowArchive":
                return obj
    return None


def read_document_show(key_path: pathlib.Path) -> dict | None:
    """Read only `Index/Document.iwa` out of a `.key` and return its
    `KN.ShowArchive` object, or `None` if that archive holds no such object.

    Reads a single small member of the bundle rather than the whole
    thing: a `.key`'s per-slide `Index/Slide-<id>.iwa` files can run to
    hundreds of megabytes each, and the slide-size cross-check this backs
    (`build-slide-corpus.py`'s layout guard) needs none of that -- only the
    document-level `KN.ShowArchive`. `zip_file_reader` yields members in
    filename-sorted order, and "Document" sorts before "Slide"/
    "TemplateSlide", so this stops as soon as it is found rather than
    scanning the rest of the archive's member list.
    """
    from keynote_parser.codec import IWAFile
    from keynote_parser.file_utils import file_reader

    doc_map: dict[str, list[dict]] = {}
    for filename, handle in file_reader(str(key_path), progress=False):
        if filename != "Index/Document.iwa":
            continue
        data = IWAFile.from_buffer(handle.read(), filename).to_dict()
        merge_objects_by_id(data, doc_map)
        break

    return find_show_archive(doc_map)


def read_slide_size(key_path: pathlib.Path) -> tuple[float, float] | None:
    """The deck's true slide dimensions `(width, height)` in points, read
    from `KN.ShowArchive.size` -- the size Keynote actually authored the
    slide at, independent of whatever page size a PDF export boxed it into.

    Returns `None` when the archive carries no size at all (unexpected, but
    not this function's job to raise over -- see the caller's degrade
    policy). Any failure to read or parse the `.key` itself (a corrupt
    bundle, a format `keynote_parser` cannot decode, the dependency not
    being installed) is left to propagate; callers that must degrade rather
    than fail catch around this call themselves.
    """
    show = read_document_show(key_path)
    if show is None:
        return None
    size = show.get("size")
    if not size:
        return None
    return (size["width"], size["height"])
