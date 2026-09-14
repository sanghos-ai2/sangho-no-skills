#!/usr/bin/env python3
"""Build an interactive storyboard editor from a deck payload.

    build_storyboard.py payload.json  [-o editor.html]

The payload is the talk; the template is the skill. Publish the result as a Claude
artifact with `capabilities: {db: {}}` so edits persist and Claude can read them back.

Payload shape:
  {
    "title":    "Atlas - Ai2 team talk",
    "subtitle": "Ai2 team - ~8 min - brand: Ai2 Strata",
    "beats":    [ {id, n, t, m, a, v, sub, ty, b, note, k, lines?, at?, under?,
                   boxes?, band?, g?, o?}, ... ],
    "figures":  [ {f: "figure.png", u: true, c: "caption"}, ... ],
    "tables":   [ {id, n, label, page, crop, units, px, full, cols, rows, trim}, ... ]
  }

`k` picks the renderer: blackout titlecard question capture statement naming build
pipeline dimmed quote takeaway open ladder space montage chapter.
"""
import argparse, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "editor-template.html")
BLOCK = re.compile(
    r'(<script id="deck-payload" type="application/json">\n).*?(\n</script>)', re.S)

REQUIRED = ("title", "beats")

def build(payload, template_path=TEMPLATE):
    for k in REQUIRED:
        if k not in payload:
            raise SystemExit("payload is missing %r" % k)
    seen = set()
    for i, b in enumerate(payload["beats"]):
        if "id" not in b:
            raise SystemExit("beat %d has no id; ids are the storage key" % i)
        if b["id"] in seen:
            raise SystemExit("duplicate beat id %r - edits would collide" % b["id"])
        seen.add(b["id"])
    payload.setdefault("subtitle", "")
    payload.setdefault("figures", [])
    payload.setdefault("tables", [])
    html = io.open(template_path, encoding="utf-8").read()
    if not BLOCK.search(html):
        raise SystemExit("template has no deck-payload block")
    # json.dumps escapes nothing that can close a <script>, except a literal "</"
    blob = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    return BLOCK.sub(lambda m: m.group(1) + blob + m.group(2), html, count=1)

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("payload")
    ap.add_argument("-o", "--out", default="storyboard-editor.html")
    ap.add_argument("--template", default=TEMPLATE)
    a = ap.parse_args()
    payload = json.load(io.open(a.payload, encoding="utf-8"))
    html = build(payload, a.template)
    io.open(a.out, "w", encoding="utf-8").write(html)
    print("%s - %d beats, %d figures, %d tables, %.0f KB"
          % (a.out, len(payload["beats"]), len(payload["figures"]),
             len(payload["tables"]), len(html) / 1024))

if __name__ == "__main__":
    main()
