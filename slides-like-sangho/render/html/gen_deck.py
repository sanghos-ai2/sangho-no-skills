# -*- coding: utf-8 -*-
"""Render a deck.json into a 1920x1080 HTML deck in Sangho's measured design language.

    gen_deck.py deck.json [-a assets.json] [-o deck.html]

Sizing is FIT-TO-BOX on his measured ladder, never a word count: for each candidate
size the wrapped height is estimated from per-character advance widths, and the
largest size that fits both axes wins. See ../html.md for the rules and for the
failures that are silent if you change them.
"""
import argparse, json, io, re, html, os, sys, math

_ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
_ap.add_argument("deck", nargs="?", default="deck.json")
_ap.add_argument("-a", "--assets", default="assets.json")
_ap.add_argument("-o", "--out", default="deck.html")
ARGS = _ap.parse_args()

D = json.load(io.open(ARGS.deck, encoding="utf-8"))
deck, TABLES = D["deck"], D["tables"]
for i, s in enumerate(deck, 1): s["n"] = i
ASSETS = json.load(io.open(ARGS.assets)) if os.path.exists(ARGS.assets) else {}

def e(x): return html.escape(x or "", quote=True)
def lines_of(s):
    raw = [l.strip() for l in (s.get("words") or "").split("\n") if l.strip()]
    # Prose pasted from a document carries hard newlines where it happened to wrap.
    # Those are not line breaks he chose, and rendering them as separate lines puts a
    # paragraph gap mid-sentence. Rejoin a LONG line that ends unfinished with a
    # following line that starts lower-case; a deliberate short stack ("GOAL - ...",
    # "TRAJECTORY TREE - ...") is left exactly as written.
    out = []
    for l in raw:
        if (out and len(out[-1]) >= 60
                and not re.search(r'[.!?:;"\u201d\u2014]$', out[-1])
                and l[:1].islower()):
            out[-1] = out[-1] + " " + l
        else:
            out.append(l)
    return out
def wc(ls): return sum(len(l.split()) for l in ls)

# his measured scale on a 1920-unit page, expressed in cqw
PT = lambda p: "%.2fcqw" % (p / 1920 * 100)

# Manrope 600 advance widths, in em. Counting characters by class beats one flat
# factor: "WWW" and "ill" differ by 3x, and a word count sees neither.
_W = {}
for _c in "iljI.,:;'!|()[]": _W[_c] = 0.30
for _c in "ftr-": _W[_c] = 0.38
for _c in "mw": _W[_c] = 0.85
for _c in "MW": _W[_c] = 0.95
def em_width(t):
    return sum(_W.get(c, 0.68 if c.isupper() else 0.52) for c in t)

AVAIL_W = 86.0                                   # 100cqw minus the 7cqw side pads
def avail_h(s, has_under=False):
    h = 56.25 - (15.0 if s.get("header") else 8.0) - 7.0
    return h - (3.2 if has_under else 0.0)

def fit(lines, box_w, box_h, ladder, lh=1.16, gap=0.5):
    """Largest size on the ladder whose wrapped text fits the box in BOTH axes."""
    lines = [l for l in lines if l is not None]
    if not lines: return ladder[-1]
    for pt in ladder:
        F = pt / 1920.0 * 100.0                  # cqw
        vis = 0; ok = True
        for l in lines:
            if not l.strip(): vis += 1; continue
            if max(em_width(w) for w in l.split()) * F > box_w:
                ok = False; break                # one unbreakable word already too wide
            vis += max(1, math.ceil(em_width(l) * F / box_w))
        if not ok: continue
        if vis * F * lh + (len(lines) - 1) * F * gap <= box_h: return pt
    return ladder[-1]

# 112 is his display size and the corpus reserves it for naming slides, so it is
# offered only to a single short line; everything else starts at the 84 title size.
STACK_LADDER = [84, 50, 36, 30, 26, 22]
def stack_size(ls, s):
    lad = ([112] + STACK_LADDER) if (len(ls) == 1 and len(ls[0].split()) <= 3) else STACK_LADDER
    return fit(ls, AVAIL_W, avail_h(s, bool((s.get("under") or s.get("sub") or "").strip())), lad)

def quote_size(ls, s):
    return fit(ls, AVAIL_W, avail_h(s, True), [84, 60, 50, 44, 36, 30], gap=0.45)

def img(fname, cls="", alt=""):
    url = ASSETS.get(fname)
    if url: return '<img class="%s" src="%s" alt="%s">' % (cls, e(url), e(alt))
    return ('<div class="pending %s"><span>%s</span><em>asset not uploaded yet</em></div>'
            % (cls, e(fname)))

# Four bins, not a continuous curve. A formula gave 18 distinct sizes across the deck,
# so two headers of near-equal length got visibly different boxes. Binning means a whole
# range of lengths shares one size, and the box keeps one height across that range.
HEADER_BINS = [74, 58, 46, 36]
HEADER_TEXT_W = 85.4                     # 88cqw max-width less the box's own padding
def header_size(txt):
    for pt in HEADER_BINS:
        if em_width(txt) * (pt / 1920.0 * 100.0) <= HEADER_TEXT_W:
            return pt                     # largest bin this still fits on ONE line
    return HEADER_BINS[-1]

def header_el(s):
    h = (s.get("header") or "").strip()
    if not h: return ""
    return '<div class="sechdr" style="font-size:%s">%s</div>' % (PT(header_size(h)), e(h))

def num_el(s, kind):
    if kind in ("black", "title"): return ""
    return '<span class="num">%d</span>' % s["n"]

def under_el(s):
    # HIS edit wins over the authored default, always. This was inverted once and it
    # silently printed a "[CO-AUTHOR LINE - PLACEHOLDER]" over a byline he had written.
    u = (s.get("sub") or "").strip() or (s.get("under") or "").strip()
    return '<div class="under">%s</div>' % e(u) if u else ""

def table_fit(nrows, box_h=41.0):
    """Size the cell so nrows + the table's own header row fit the room actually left."""
    per = box_h / (nrows + 1.6)         # +1.6 buys the header row and its rule
    return max(1.15, min(2.08, per / 1.9)), max(0.22, min(0.70, per / 5.5))

def numeric_cols(t):
    """A column is numeric when most of its filled cells read as a number."""
    out = []
    for i in range(len(t["cols"])):
        vals = [r[i] for r in t["rows"] if i < len(r) and r[i].strip()]
        hits = sum(1 for v in vals if re.match(r"^[-+\u2212]?[\d.]", v.strip()))
        out.append(bool(vals) and hits >= max(1, int(len(vals) * 0.6)))
    return out

def table_html(t, box_h=41.0):
    nums = numeric_cols(t)
    head = "".join('<th%s>%s</th>' % (' class="num"' if nums[i] else "", e(c))
                   for i, c in enumerate(t["cols"]))
    rows = ""
    for r in t["rows"]:
        cells = "".join('<td%s>%s</td>' % (' class="num"' if i < len(nums) and nums[i] else "", e(c))
                        for i, c in enumerate(r))
        rows += "<tr>%s</tr>" % cells
    cell, pad = table_fit(len(t["rows"]), box_h)
    return ('<div class="tabwrap"><table class="ptab%s" style="--cell:%.2fcqw;--rowpad:%.2fcqw">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            % (" c2" if len(t["cols"]) == 2 else "", cell, pad, head, rows))

def classify(s):
    if s["k"] == "blackout": return "black"
    if s["table"]:
        t = TABLES.get(s["table"])
        if t and t.get("rows") and s["tableTreat"] == "recreate": return "table"
        return "tablecrop"
    if s["figure"]: return "figure"
    if s["k"] == "titlecard": return "title"
    ls = lines_of(s)
    if s["k"] == "quote" or (ls and re.match(r'^[“"‘\']', ls[0])): return "quote"
    if s["k"] == "pipeline" and s.get("boxes"): return "pipeline"
    return "stack"

def body_for(s, kind):
    ls = lines_of(s)
    if kind == "black": return ""
    if kind == "title":
        big = "".join('<div class="l">%s</div>' % e(l) for l in ls) or '<div class="l">Atlas</div>'
        return '<div class="pad ctr"><div class="titlelines">%s</div>%s</div>' % (big, under_el(s))
    if kind == "quote":
        sz = quote_size(ls, s)
        q = "".join('<p class="ql" style="font-size:%s">%s</p>' % (PT(sz), e(l)) for l in ls)
        return '<div class="pad"><div class="quote">%s%s</div></div>' % (q, under_el(s))
    if kind == "pipeline":
        bx = "".join('<div class="box">%s</div>' % "<br>".join(e(x) for x in b.split("\n"))
                     for b in s["boxes"])
        return '<div class="pad ctr"><div class="strip">%s</div></div>' % bx
    if kind == "table":
        t = TABLES[s["table"]]
        cap = (ls[0] if ls else t["label"])
        rest = "".join('<div class="l">%s</div>' % e(l) for l in ls[1:])
        csz = fit([cap], AVAIL_W, avail_h(s) * 0.22, [50, 36, 30, 26])
        # what the table actually gets: the slide's room, less the caption and its gap
        box = avail_h(s) - (csz / 1920.0 * 100.0) * 1.25 - 1.8
        return ('<div class="pad"><div class="tcap" style="font-size:%s">%s</div>%s%s</div>'
                % (PT(csz), e(cap), table_html(t, box), rest))
    if kind == "tablecrop":
        t = TABLES[s["table"]]
        if not ls and not s.get("header"):
            return '<div class="bleed">%s</div>' % img(t["crop"], "full", t["label"])
        cap = ls[0] if ls else t["label"]
        csz = fit([cap], AVAIL_W, avail_h(s) * 0.22, [50, 36, 30, 26])
        return ('<div class="pad"><div class="tcap" style="font-size:%s">%s</div>'
                '<div class="figwrap">%s</div></div>' % (PT(csz), e(cap), img(t["crop"], "fig", t["label"])))
    if kind == "figure":
        band = (s.get("band") or "").strip()
        if not ls and not s.get("header"):          # nothing to say: let the artwork carry the slide
            return ('<div class="bleed">%s%s</div>'
                    % (img(s["figure"], "full", s["title"]),
                       '<div class="band">%s</div>' % e(band) if band else ""))
        sz = fit(ls, AVAIL_W, avail_h(s) * 0.34, [84, 50, 36, 30, 26])
        txt = "".join('<div class="l">%s</div>' % e(l) for l in ls)
        lead = '<div class="figlead" style="font-size:%s">%s</div>' % (PT(sz), txt) if ls else ""
        return ('<div class="pad">%s<div class="figwrap">%s</div></div>'
                % (lead, img(s["figure"], "fig", s["title"])))
    sz = stack_size(ls, s)
    txt = "".join('<div class="l">%s</div>' % e(l) for l in ls)
    cls = "pad ctr"
    return '<div class="%s"><div class="stack" style="font-size:%s">%s</div>%s</div>' % (cls, PT(sz), txt, under_el(s))

def slide_html(s):
    kind = classify(s)
    g = s.get("ground") or ("g-black" if kind == "black" else "")
    note = (s.get("note") or "").strip()
    msg = (s.get("message") or "").strip()
    hdr = " hashdr" if s.get("header") else ""
    return ('<section class="slide %s %s%s" data-n="%d" data-kind="%s">%s%s%s'
            '<div class="notes"><b>%s</b>%s%s</div></section>'
            % (g, "k-" + kind, hdr, s["n"], kind, header_el(s), body_for(s, kind), num_el(s, kind),
               e(s["title"]),
               '<i>%s</i>' % e(msg) if msg else "",
               '<p>%s</p>' % e(note) if note else ""))

CSS = """
:root{
  --ground:#faf2e9; --ink:#0a3235; --rev:#032629; --grey:#9cb2af;
  --pink:#f0529c; --green:#0fcb8c; --rule:#105257;
  --face:'Manrope','Helvetica Neue',Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
body{margin:0;background:#1b1f21;font-family:var(--face);color:var(--ink)}
#stage{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;padding:2vmin}
.slide{
  position:relative;width:min(96vw,calc(96vh*16/9));aspect-ratio:16/9;
  container-type:inline-size;background:var(--ground);color:var(--ink);
  overflow:hidden;box-shadow:0 2px 40px rgba(0,0,0,.45);display:none;
}
.slide.on{display:block}
.slide.g-rev{background:var(--rev);color:var(--ground)}
.slide.g-black{background:#000;color:var(--ground)}
.pad{position:absolute;inset:8cqw 7cqw 7cqw;display:flex;flex-direction:column;justify-content:center}
.pad.ctr{align-items:flex-start;text-align:left}
.l{line-height:1.16;margin:0 0 .5em}
.l:last-child{margin-bottom:0}
.stack{font-weight:600;letter-spacing:-.012em}
.titlelines{font-size:4.38cqw;font-weight:700;letter-spacing:-.02em;line-height:1.12}
.under{margin-top:2.4cqw;font-size:1.88cqw;font-weight:400;color:var(--grey)}
.slide.g-rev .under{color:#7fa3a1}
.quote .ql{margin:0 0 .45em;font-weight:600;line-height:1.2;letter-spacing:-.01em}
.quote .ql:last-of-type{margin-bottom:0}
.strip{display:flex;gap:2.4cqw;align-items:stretch;width:100%}
.box{flex:1;border:.16cqw solid currentColor;padding:2cqw 1.6cqw;font-size:1.88cqw;
  font-weight:600;line-height:1.3;display:flex;align-items:center}
.slide.hashdr .pad{top:15cqw}
.sechdr{position:absolute;left:6cqw;top:4.4cqw;right:6cqw;width:max-content;max-width:88cqw;
  z-index:3;border:.16cqw solid currentColor;padding:.55cqw 1.3cqw;
  font-weight:600;letter-spacing:-.01em;line-height:1.15}
.num{position:absolute;right:3.4cqw;bottom:2.6cqw;font-size:1.25cqw;color:var(--grey)}
.bleed{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:var(--ground)}
.bleed .full{width:100%;height:100%;object-fit:contain}
.band{position:absolute;left:0;right:0;bottom:0;background:var(--rev);color:var(--ground);
  padding:1.4cqw 3.4cqw;font-size:1.88cqw;font-weight:600}
.figwrap{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;margin-top:1.8cqw}
.figwrap .fig{max-width:100%;max-height:100%;object-fit:contain}
.figlead{font-weight:600;line-height:1.2;flex:none}
.tcap{font-weight:600;line-height:1.2;flex:none}
.tabwrap{flex:1;min-height:0;overflow:hidden;display:flex;align-items:flex-start}
.ptab{width:100%;border-collapse:collapse;margin-top:1.8cqw}
.ptab th,.ptab td{text-align:left;padding:var(--rowpad,.7cqw) 1.4cqw var(--rowpad,.7cqw) 0;
  font-size:var(--cell,2.08cqw);line-height:1.2}
.ptab thead th{font-weight:700;border-bottom:.16cqw solid currentColor;padding-bottom:.9cqw}
.ptab tbody tr+tr td{border-top:.06cqw solid var(--grey)}
.ptab th,.ptab td{text-align:left}
.ptab th.num,.ptab td.num{text-align:right;position:static;
  font-variant-numeric:tabular-nums;font-size:var(--cell,2.08cqw);color:inherit}
/* a two-column table reads better with the key column held narrow than with it
   stretched by the browser's auto layout */
.ptab.c2 th:first-child,.ptab.c2 td:first-child{width:26%}
.pending{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1cqw;
  width:100%;height:100%;min-height:24cqw;border:.2cqw dashed var(--grey);color:var(--grey);
  font-size:1.6cqw}
.pending em{font-style:normal;font-size:1.25cqw;opacity:.8}
.notes{display:none}
#hud{position:fixed;left:0;right:0;bottom:0;display:flex;gap:18px;align-items:center;
  padding:8px 14px;background:#12161800;color:#8ea3a1;font-size:12px;
  font-family:ui-monospace,SFMono-Regular,Menlo,monospace;pointer-events:none}
#hud b{color:#cfe0de;font-weight:500}
#pane{position:fixed;right:0;top:0;bottom:0;width:min(420px,34vw);background:#0f1416;color:#cfe0de;
  padding:22px 20px;overflow:auto;font-size:14px;line-height:1.55;display:none;
  border-left:1px solid #223033}
#pane.on{display:block}
#pane h3{margin:0 0 10px;font-size:15px;color:#fff}
#pane i{display:block;color:#8ea3a1;font-style:normal;margin-bottom:10px}
@media print{
  body{background:#fff}
  #stage{position:static;display:block;padding:0}
  #hud,#pane{display:none!important}
  .slide{display:block!important;width:100%;box-shadow:none;break-after:page;page-break-after:always}
  @page{size:1920px 1080px;margin:0}
}
"""

JS = """
const S=[...document.querySelectorAll('.slide')];let i=0;
function show(n){i=Math.max(0,Math.min(S.length-1,n));
  S.forEach((s,k)=>s.classList.toggle('on',k===i));
  document.getElementById('pos').textContent=(i+1)+' / '+S.length;
  const nd=S[i].querySelector('.notes');
  document.getElementById('pane').innerHTML='<h3>'+(nd?nd.querySelector('b').textContent:'')+'</h3>'
    +(nd?nd.innerHTML.replace(/^<b>.*?<\\/b>/,''):'');
  location.hash=(i+1);}
addEventListener('keydown',ev=>{
  if(ev.key==='ArrowRight'||ev.key===' '||ev.key==='PageDown'){ev.preventDefault();show(i+1);}
  else if(ev.key==='ArrowLeft'||ev.key==='PageUp'){ev.preventDefault();show(i-1);}
  else if(ev.key==='Home'){show(0);} else if(ev.key==='End'){show(S.length-1);}
  else if(ev.key==='n'||ev.key==='N'){document.getElementById('pane').classList.toggle('on');}
});
addEventListener('click',ev=>{if(ev.target.closest('#pane'))return;
  show(i+(ev.clientX<innerWidth*0.28?-1:1));});
show(Math.max(0,(parseInt(location.hash.slice(1),10)||1)-1));
// a pasted or hand-edited #N should move the deck, not just sit in the address bar
addEventListener('hashchange',()=>{const n=parseInt(location.hash.slice(1),10);
  if(n&&n-1!==i)show(n-1);});
"""

buf = io.StringIO()
out = buf
out.write('<title>Atlas — Ai2 team talk</title>\n')
out.write('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
          'family=Manrope:wght@400;500;600;700;800&display=swap">\n')
out.write("<style>%s</style>\n" % CSS)
out.write('<div id="stage">%s</div>\n' % "".join(slide_html(s) for s in deck))
out.write('<aside id="pane"></aside>\n')
out.write('<div id="hud"><b id="pos"></b><span>&larr; &rarr; move</span>'
          '<span>N speaker notes</span><span>&#8984;P to PDF</span></div>\n')
out.write("<script>%s</script>\n" % JS)
io.open(ARGS.out,"wb").write(buf.getvalue().encode("ascii","xmlcharrefreplace"))
print("%s - %d slides, %d assets wired" % (ARGS.out, len(deck), len(ASSETS)))
from collections import Counter
print("  " + ", ".join("%s x%d"%(k,v) for k,v in Counter(classify(s) for s in deck).most_common()))
