"""Crop every booktabs table out of the compiled paper.

Two signals do the work:
  * pdftotext -bbox gives the caption's y position, which says WHICH table on the page.
  * the raster's long horizontal dark runs are the \\toprule/\\bottomrule, which give the
    table's exact vertical AND horizontal extent - so the crop excludes the submission
    line numbers in the margins without hardcoding a margin width.
"""
import subprocess, re, os, sys, html, json
from PIL import Image

PDF = None   # set by --pdf
DPI = 300

def bbox_pages():
    xml = subprocess.run(["pdftotext", "-bbox", PDF, "-"],
                         capture_output=True, text=True).stdout
    pages = []
    for pm in re.finditer(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', xml, re.S):
        w, h, body = float(pm.group(1)), float(pm.group(2)), pm.group(3)
        words = [(float(a), float(b), float(c), float(d), html.unescape(t))
                 for a, b, c, d, t in re.findall(
                     r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', body)]
        pages.append({"w": w, "h": h, "words": words})
    return pages

def find_caption(pages, phrase):
    """Return (page_index, yMin_in_points) for the first run of words matching phrase."""
    toks = phrase.split()
    for pi, p in enumerate(pages):
        ws = p["words"]
        for i in range(len(ws) - len(toks) + 1):
            if all(ws[i + k][4] == toks[k] for k in range(len(toks))):
                return pi, ws[i][1], ws[i][0]
    return None, None, None

def rule_rows(im, min_span=0.30):
    g = im.convert("L"); w, h = g.size; px = g.load()
    hits = []
    for y in range(h):
        run = best = beststart = 0; start = None
        for x in range(w):
            if px[x, y] < 160:
                if start is None: start = x
                run += 1
                if run > best: best = run; beststart = start
            else:
                run = 0; start = None
        if best / w >= min_span:
            hits.append((y, beststart, beststart + best))
    return hits

def group(hits):
    if not hits: return []
    gs = [[hits[0]]]
    for hrow in hits[1:]:
        if hrow[0] - gs[-1][-1][0] <= 3: gs[-1].append(hrow)
        else: gs.append([hrow])
    return gs

def crop_table(pages, phrase, out, keep_caption=True):
    pi, cap_y, cap_x = find_caption(pages, phrase)
    if pi is None:
        print("  MISS  caption not found:", phrase); return False
    page = pi + 1
    prefix = out[:-4]
    subprocess.run(["pdftoppm", "-r", str(DPI), "-f", str(page), "-l", str(page),
                    "-png", "-singlefile", PDF, prefix + "__p"], check=True)
    png = prefix + "__p.png"
    im = Image.open(png)
    scale = im.size[1] / pages[pi]["h"]
    cap_py = cap_y * scale
    gs = [g for g in group(rule_rows(im)) if g[0][0] >= cap_py - 6]
    if not gs:
        print("  MISS  no rules under caption on page", page, "-", phrase)
        os.remove(png); return False
    # The boundary is the NEXT caption on the page, not a gap width: a tall table
    # (projections) puts a whole page-quarter between its midrule and bottomrule,
    # so a gap heuristic truncates it right after the header row.
    limit = im.size[1]
    # Only a caption in the SAME column bounds this table. On a two-column page a
    # caption in the other column sits at a smaller y and would truncate to nothing.
    colw = pages[pi]["w"] * 0.15
    for _, other in TABLES:
        if other == phrase: continue
        opi, oy, ox = find_caption(pages, other)
        if opi == pi and abs(ox - cap_x) < colw and oy * scale > cap_py + 6:
            limit = min(limit, oy * scale)
    kept = [g for g in gs if g[0][0] < limit]
    if not kept:
        print("  MISS  no rules before the next caption -", phrase)
        os.remove(png); return False
    top = kept[0][0][0]; bot = kept[-1][-1][0]
    x0 = min(h[1] for g in kept for h in g); x1 = max(h[2] for g in kept for h in g)
    if keep_caption: top = int(cap_py) - 10
    pad = 14
    box = (max(0, x0 - pad), max(0, top - pad),
           min(im.size[0], x1 + pad), min(im.size[1], bot + pad))
    im.crop(box).save(out)
    os.remove(png)
    print("  ok    %-38s p%-3d %sx%s" % (os.path.basename(out), page, *Image.open(out).size))
    return True

TABLES = [
 ("tab-participants",             "Formative study participant backgrounds."),
 ("tab-projections",              "The six projections available"),
 ("tab-extended-run-phases",      "The five phases of each Extended Run cycle."),
 ("tab-research-goals",           "Submitted and transformed research goals"),
 ("tab-tasks",                    "The six prompts participants worked through"),
 ("tab-run-artifacts",            "Artifact counts for the 28 controlled-study runs"),
 ("tab-run-runtime",              "Recorded runtime of the controlled-study runs,"),
 ("tab-trajectory-statistics",    "Structural characteristics of the 28 research trajectories."),
 ("tab-construct-map",            "Post-task scales, and what each one measures."),
 ("tab-post-task-items",          "Post-task survey items."),
 ("tab-final-survey-comparison",  "Post-study comparative survey questions."),
 ("tab-final-survey-compact",     "Comparative survey questions."),
 ("tab-extended-run-prompts",     "Extended Run orchestration. Each cycle runs"),
]

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", required=True, help="the compiled paper")
    ap.add_argument("--tables", help='JSON: [[name, "caption prefix"], ...]; omit for the built-in list')
    ap.add_argument("-o", "--out", default="tables")
    _a = ap.parse_args()
    PDF = _a.pdf
    if _a.tables:
        TABLES = [tuple(x) for x in json.load(open(_a.tables))]
    outdir = _a.out
    os.makedirs(outdir, exist_ok=True)
    pages = bbox_pages()
    print("paper:", len(pages), "pages")
    ok = 0
    for name, phrase in TABLES:
        if crop_table(pages, phrase, os.path.join(outdir, name + ".png")): ok += 1
    print(ok, "of", len(TABLES), "cropped")
