#!/usr/bin/env python3
"""Merge a deck payload with the edits saved in the storyboard artifact's database.

    build_deck_json.py payload.json storyboard-db/ [-o deck.json]

Read the database first with the Artifact tool:
    action: read_db, db_op: get,  collection: meta,  doc_id: order, out_dir: storyboard-db/
    action: read_db, db_op: list, collection: beats,                out_dir: storyboard-db/

THE PRECEDENCE RULE: a saved edit always beats the authored default. Never the other
way round. Inverting it once printed a "[CO-AUTHOR LINE - PLACEHOLDER]" over a byline
that was sitting in the database the whole time, and nothing errored - a placeholder is
still text, so the slide rendered fine and looked deliberate.
"""
import argparse, glob, io, json, os, re

FALLBACK = ("words", "message", "visual", "sub", "build", "note")   # edit wins, authored is the floor

def derived_title(s, tables):
    for k in ("words", "header", "message"):
        v = (s.get(k) or "").strip()
        if v:
            one = re.sub(r"\s+", " ", v.split("\n")[0]).strip()
            return one if len(one) <= 46 else re.sub(r"\s+\S*$", "", one[:45]) + "…"
    # a slide whose only content is its artwork is NAMED for that artwork
    if s.get("table") and tables.get(s["table"]):
        return tables[s["table"]]["label"]
    if s.get("figure"):
        return re.sub(r"[-_]+", " ", s["figure"].rsplit(".", 1)[0]).strip().capitalize()
    return s.get("slideType") or ("" if s.get("isNew") else s.get("t")) or "New slide"

def build(payload, dbdir):
    ORIG = {b["id"]: b for b in payload.get("beats", [])}
    TABLES = {t["id"]: t for t in payload.get("tables", [])}
    FIGS = {f["f"]: f for f in payload.get("figures", [])}

    od_path = os.path.join(dbdir, "meta", "order.json")
    if os.path.exists(od_path):
        od = json.load(io.open(od_path, encoding="utf-8"))
        order = od.get("data", od)["order"]
    else:                                        # never edited: the payload's own sequence
        order = [b["id"] for b in payload.get("beats", [])]

    docs = {}
    for f in glob.glob(os.path.join(dbdir, "beats", "*.json")):
        d = json.load(io.open(f, encoding="utf-8"))
        docs[d["id"]] = d.get("data", d)

    deck = []
    for n, bid in enumerate(order, 1):
        b = dict(ORIG.get(bid, {})); e = docs.get(bid, {})
        s = {"n": n, "id": bid, "isNew": bid not in ORIG}
        # `words` is the one field whose authored form lives under another name
        s["words"] = e["words"] if e.get("words") is not None else \
                     (b.get("words") or "\n".join(b.get("lines") or []))
        for k, src in (("message", "m"), ("visual", "v"), ("sub", "sub"),
                       ("build", "b"), ("note", "note")):
            s[k] = e[k] if e.get(k) is not None else b.get(src, "")
        s["header"] = e.get("header") or ""
        s["slideType"] = e.get("slideType") or ""
        s["ground"] = e.get("ground") or ""
        s["figure"] = e.get("figure") or ""
        s["figureNote"] = e.get("figureNote") or ""
        s["table"] = e.get("table") or ""
        s["tableTreat"] = e.get("tableTreat") or "recreate"
        s["status"] = e.get("status") or ""
        s["feedback"] = e.get("feedback") or ""
        s["k"] = b.get("k") or "statement"
        s["under"] = b.get("under") or ""
        s["boxes"] = b.get("boxes") or []
        s["band"] = b.get("band") or ""
        s["at"] = b.get("at") or []
        s["title"] = (e.get("name") or "").strip() or \
                     (b.get("t") if bid in ORIG else "") or derived_title(s, TABLES)
        deck.append(s)
    return {"deck": deck, "tables": TABLES, "figs": FIGS}

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("payload"); ap.add_argument("dbdir")
    ap.add_argument("-o", "--out", default="deck.json")
    a = ap.parse_args()
    out = build(json.load(io.open(a.payload, encoding="utf-8")), a.dbdir)
    io.open(a.out, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
    print("%s - %d slides" % (a.out, len(out["deck"])))

if __name__ == "__main__":
    main()
