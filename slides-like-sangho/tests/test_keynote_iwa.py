from tools.keynote_iwa import find_show_archive, merge_objects_by_id, read_slide_size


def _iwa_payload(archives: list[dict]) -> dict:
    return {"chunks": [{"archives": archives}]}


def _archive(identifier: str, objects: list[dict]) -> dict:
    return {"header": {"identifier": identifier}, "objects": objects}


def test_merge_objects_by_id_accumulates_rather_than_overwrites():
    # An archive id can be split across a shared Index/Slide.iwa and a
    # per-slide Index/Slide-<id>.iwa -- merging a second file for an id
    # already present must extend, not replace.
    into: dict = {}
    merge_objects_by_id(
        _iwa_payload([_archive("7", [{"_pbtype": "A"}])]), into
    )
    merge_objects_by_id(
        _iwa_payload([_archive("7", [{"_pbtype": "B"}])]), into
    )
    assert into["7"] == [{"_pbtype": "A"}, {"_pbtype": "B"}]


def test_merge_objects_by_id_defaults_missing_objects_to_empty_list():
    into: dict = {}
    merge_objects_by_id(_iwa_payload([_archive("1", [])]), into)
    assert into["1"] == []


def test_find_show_archive_returns_the_matching_object():
    doc_map = {
        "1": [{"_pbtype": "KN.DocumentArchive"}],
        "2": [{"_pbtype": "KN.ShowArchive", "size": {"width": 1920.0, "height": 1080.0}}],
    }
    show = find_show_archive(doc_map)
    assert show is not None
    assert show["size"] == {"width": 1920.0, "height": 1080.0}


def test_find_show_archive_returns_none_when_absent():
    assert find_show_archive({"1": [{"_pbtype": "KN.DocumentArchive"}]}) is None


def test_read_slide_size_returns_none_when_show_archive_has_no_size(monkeypatch):
    import tools.keynote_iwa as keynote_iwa

    monkeypatch.setattr(
        keynote_iwa, "read_document_show", lambda key_path: {"_pbtype": "KN.ShowArchive"}
    )
    assert read_slide_size("unused") is None


def test_read_slide_size_returns_none_when_no_show_archive_found(monkeypatch):
    import tools.keynote_iwa as keynote_iwa

    monkeypatch.setattr(keynote_iwa, "read_document_show", lambda key_path: None)
    assert read_slide_size("unused") is None


def test_read_slide_size_reads_width_and_height_off_the_show_archive(monkeypatch):
    import tools.keynote_iwa as keynote_iwa

    monkeypatch.setattr(
        keynote_iwa,
        "read_document_show",
        lambda key_path: {
            "_pbtype": "KN.ShowArchive",
            "size": {"width": 1920.0, "height": 1080.0},
        },
    )
    assert read_slide_size("unused") == (1920.0, 1080.0)
