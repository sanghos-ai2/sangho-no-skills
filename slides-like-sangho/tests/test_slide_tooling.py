"""The storyboard/render pipeline. Every case here is a failure that was SILENT once."""
import importlib.util, io, json, os, re, subprocess, sys
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "slides-like-sangho") if os.path.isdir(
    os.path.join(ROOT, "slides-like-sangho")) else ROOT

def _load(rel, name):
    path = os.path.join(SKILL, rel)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.argv = [name, "--help"][:1]          # argparse at import must not see pytest's argv
    spec.loader.exec_module(mod)
    return mod

bdj = _load("render/html/build_deck_json.py", "bdj")
bsb = _load("storyboard/build_storyboard.py", "bsb")

PAYLOAD = {
    "title": "T", "subtitle": "s",
    "beats": [
        {"id": "b1", "t": "Authored", "k": "statement", "m": "authored message",
         "sub": "authored byline", "lines": ["authored line one", "authored line two"]},
        {"id": "b2", "t": "Second", "k": "quote", "m": "", "sub": "", "lines": ["q"]},
    ],
    "figures": [], "tables": [
        {"id": "tt", "n": "Table 1", "label": "Demo", "page": 1, "crop": "c.png",
         "units": 40, "px": "1x1", "full": "", "cols": ["A", "B"],
         "rows": [["x", "1.0"], ["y", "2.0"]], "trim": ""}],
}

def _db(tmp_path, order, beats):
    os.makedirs(tmp_path / "meta"); os.makedirs(tmp_path / "beats")
    io.open(tmp_path / "meta" / "order.json", "w").write(
        json.dumps({"id": "order", "data": {"order": order}}))
    for b in beats:
        io.open(tmp_path / "beats" / (b["id"] + ".json"), "w").write(
            json.dumps({"id": b["id"], "data": b}))
    return str(tmp_path)

# ---------------------------------------------------------------- precedence

def test_saved_edit_beats_the_authored_default(tmp_path):
    """The byline bug: an authored placeholder must never win over a saved edit."""
    db = _db(tmp_path, ["b1"], [{"id": "b1", "sub": "HIS REAL BYLINE"}])
    s = bdj.build(PAYLOAD, db)["deck"][0]
    assert s["sub"] == "HIS REAL BYLINE"

def test_authored_default_is_the_floor_not_the_ceiling(tmp_path):
    db = _db(tmp_path, ["b1"], [{"id": "b1"}])
    s = bdj.build(PAYLOAD, db)["deck"][0]
    assert s["sub"] == "authored byline"
    assert s["message"] == "authored message"

def test_authored_lines_reach_the_deck_as_words(tmp_path):
    """`lines` is where authored text lives; the deck must render it."""
    db = _db(tmp_path, ["b1"], [{"id": "b1"}])
    assert bdj.build(PAYLOAD, db)["deck"][0]["words"] == "authored line one\nauthored line two"

def test_a_cleared_field_stays_cleared(tmp_path):
    """Empty string is an EDIT; only None means 'never touched'."""
    db = _db(tmp_path, ["b1"], [{"id": "b1", "words": ""}])
    assert bdj.build(PAYLOAD, db)["deck"][0]["words"] == ""

# ---------------------------------------------------------------- titles

def test_artwork_only_slide_is_named_for_its_artwork(tmp_path):
    """A slide HE added, cleared to just its artwork, must not read "New slide"."""
    db = _db(tmp_path, ["added1"], [{"id": "added1", "words": "", "table": "tt"}])
    assert bdj.build(PAYLOAD, db)["deck"][0]["title"] == "Demo"

def test_an_authored_slide_keeps_its_authored_name(tmp_path):
    db = _db(tmp_path, ["b2"], [{"id": "b2", "words": "", "table": "tt"}])
    assert bdj.build(PAYLOAD, db)["deck"][0]["title"] == "Second"

def test_explicit_name_wins_over_everything(tmp_path):
    db = _db(tmp_path, ["b1"], [{"id": "b1", "name": "Chosen"}])
    assert bdj.build(PAYLOAD, db)["deck"][0]["title"] == "Chosen"

def test_order_is_authoritative(tmp_path):
    db = _db(tmp_path, ["b2", "b1"], [])
    assert [s["id"] for s in bdj.build(PAYLOAD, db)["deck"]] == ["b2", "b1"]
    db2 = _db(tmp_path / "x", ["b1"], [])
    assert len(bdj.build(PAYLOAD, db2)["deck"]) == 1      # a removed slide stays removed

# ---------------------------------------------------------------- the template

def test_template_carries_no_talk(tmp_path):
    """The template is the skill; a talk arrives as a payload."""
    html = io.open(os.path.join(SKILL, "storyboard/editor-template.html"),
                   encoding="utf-8").read()
    assert "const ORIGINALS=PAYLOAD.beats" in html
    assert "const FIGS=PAYLOAD.figures" in html
    assert "const TABLES=PAYLOAD.tables" in html
    assert "Atlas" not in html.split("const TYPES=")[0]   # no prior talk leaked in

def test_template_keeps_the_corpus_derived_vocabulary():
    html = io.open(os.path.join(SKILL, "storyboard/editor-template.html"),
                   encoding="utf-8").read()
    assert "const TYPES=[" in html and "Abstraction ladder" in html
    assert "const GROUNDS=[" in html

def test_template_exposes_authored_lines_for_editing():
    """Slide 44: text the mock drew but no field held, so it could not be cleared."""
    html = io.open(os.path.join(SKILL, "storyboard/editor-template.html"),
                   encoding="utf-8").read()
    assert '(b.lines||[]).join("\\n")' in html

def test_template_refuses_to_write_a_stale_order():
    html = io.open(os.path.join(SKILL, "storyboard/editor-template.html"),
                   encoding="utf-8").read()
    assert "if(stale){" in html and "onSnapshot" in html

def test_template_save_returns_its_promise():
    html = io.open(os.path.join(SKILL, "storyboard/editor-template.html"),
                   encoding="utf-8").read()
    assert 'return db.doc("beats/"+id).set(' in html

def test_storage_key_is_stable():
    """Renaming this collection orphans every note he has written."""
    html = io.open(os.path.join(SKILL, "storyboard/editor-template.html"),
                   encoding="utf-8").read()
    assert 'db.doc("beats/"+id)' in html and 'db.collection("beats")' in html

def test_builder_rejects_duplicate_ids():
    bad = dict(PAYLOAD, beats=[{"id": "x"}, {"id": "x"}])
    with pytest.raises(SystemExit):
        bsb.build(bad)

def test_builder_embeds_the_payload():
    out = bsb.build(json.loads(json.dumps(PAYLOAD)))
    assert '"title": "T"' in out or '"title":"T"' in out
    assert "</script>" in out and "<\\/" not in PAYLOAD["title"]
