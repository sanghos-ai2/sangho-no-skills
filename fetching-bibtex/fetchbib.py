#!/usr/bin/env python3
"""fetchbib.py - resolve citation queries to publisher-quality BibTeX.

Sources, tried in order per query (first confident hit wins):
  1. DBLP     - CS/HCI venues (ACM, IEEE). Publisher-deposited, best for
                proceedings. Uses ?param=1 for the FULL booktitle + DOI that
                ACM-Reference-Format needs (param=0 gives only "{{UIST}}").
  2. Crossref - journals, most non-CS work. Title search -> DOI content
                negotiation.
  3. OpenAlex - broadest coverage; the only one of the three that reliably
                has BOOKS (Weick, Hutchins, Suchman ...).

Input : a file of "citekey<TAB>query" lines (blank / #-comment lines skipped).
Output: --bib writes BibTeX; the report goes to stdout.

Every entry is stamped OK or REVIEW. REVIEW means the matched record did not
agree with the query on author surname and/or year -- a wrong-but-plausible
citation is worse than an unresolved one, so these are never presented as done.

Usage:
    python3 fetchbib.py --file queries.tsv --bib out.bib
    python3 fetchbib.py --query "Sensecape multilevel sensemaking"
"""
import argparse, json, re, subprocess, sys, time, urllib.parse

UA = 'fetchbib/1.0 (mailto:sanghos@allenai.org)'


def get(url, accept=None, tries=4):
    """curl-based fetch. urllib is blocked in some sandboxes; curl is not.
    DBLP and Crossref both emit sporadic 5xx, so every call retries."""
    cmd = ['curl', '-sSL', '--max-time', '30', '-A', UA, '-w', '\n%{http_code}']
    if accept:
        cmd += ['-H', f'Accept: {accept}']
    last = '?'
    for attempt in range(tries):
        r = subprocess.run(cmd + [url], capture_output=True, text=True)
        body, _, code = r.stdout.rpartition('\n')
        if code.strip() == '200':
            return body
        last = code.strip()
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f'HTTP {last} after {tries} tries')


# ---------------------------------------------------------------- confidence

def surnames(q):
    """Capitalised tokens in the query that look like surnames."""
    stop = {'The', 'A', 'An', 'And', 'Of', 'In', 'On', 'For', 'With', 'UIST',
            'CHI', 'ACM', 'IEEE', 'Proceedings', 'Conference', 'Journal'}
    return {w for w in re.findall(r'\b[A-Z][a-z]{2,}\b', q) if w not in stop}


def year_of(q):
    m = re.search(r'\b(19|20)\d{2}\b', q)
    return m.group(0) if m else None


REVIEW_PAT = re.compile(
    r'\bby\s+[A-Z]\w+\s+[A-Z]|\bbook\s+review\b|\breview\s+essay\b'
    r'|\d+\s*pages|\bhardback\b|\bpaperback\b|£|\bedited\s+by\b', re.I)


def rank(query):
    """Sort key for candidate records. Two failure modes this exists to fix:

    1. A REVIEW of a book outranks the book. Reviews appear a year later, so
       newest-first picks the review -- observed on Weick 1995 (got a 1996
       French review) and Suchman 1987 (got a 1988 review). Penalise titles
       that read like reviews, and prefer an exact year match over a newer one.
    2. The arXiv preprint outranks the published version."""
    want = year_of(query)

    def key(info):
        y = str(info.get('year') or info.get('publication_year') or '')
        title = str(info.get('title') or '')
        return (
            REVIEW_PAT.search(title) is not None,   # reviews last
            info.get('venue') == 'CoRR',            # preprints after venues
            bool(want) and y != want,               # exact year first
            -int(y or 0),                           # then newest
        )
    return key


def judge(query, bib):
    """Return (ok, why). Requires the year to match and, when the query names
    a surname, that surname to appear in the record."""
    probs = []
    y = year_of(query)
    if y:
        got = re.findall(r'year\s*=\s*[{"]?\s*((?:19|20)\d{2})', bib)
        if got and y not in got:
            probs.append(f'year mismatch: query {y}, record {got[0]}')
    if REVIEW_PAT.search(bib):
        probs.append('record looks like a REVIEW OF the work, not the work')
    want = surnames(query)
    if want:
        blob = bib.lower()
        if not any(s.lower() in blob for s in want):
            probs.append(f'no query surname {sorted(want)} in record')
    return (not probs), '; '.join(probs)


# ------------------------------------------------------------------- sources

def dblp(query):
    u = 'https://dblp.org/search/publ/api?' + urllib.parse.urlencode(
        {'q': query, 'format': 'json', 'h': 5})
    hits = json.loads(get(u))['result']['hits'].get('hit', [])
    infos = [h['info'] for h in hits]
    if not infos:
        return None
    # a real venue beats the CoRR/arXiv preprint of the same paper
    infos.sort(key=rank(query))
    top = infos[0]
    return {
        'bib': get(f"https://dblp.org/rec/{top['key']}.bib?param=1").strip(),
        'source': 'dblp',
        'chose': f"[{top.get('venue')} {top.get('year')}] {top.get('title')}",
        'alts': [f"[{i.get('venue')} {i.get('year')}] {str(i.get('title'))[:50]}"
                 for i in infos[1:4]],
    }


def crossref(query):
    u = 'https://api.crossref.org/works?' + urllib.parse.urlencode(
        {'query.bibliographic': query, 'rows': 4,
         'select': 'DOI,title,container-title,issued,type'})
    items = json.loads(get(u))['message']['items']
    if not items:
        return None
    for it in items:  # normalise for rank(): flat title + year
        it['title'] = (it.get('title') or [''])[0]
        it['year'] = ((it.get('issued', {}).get('date-parts') or [[None]])[0] or [None])[0]
    items.sort(key=rank(query))
    top = items[0]
    return {
        'bib': get(f"https://doi.org/{top['DOI']}",
                   accept='application/x-bibtex').strip(),
        'source': 'crossref',
        'chose': f"[{(top.get('container-title') or [''])[0]} "
                 f"{top.get('year')}] {top.get('title')}",
        'alts': [f"[{(i.get('container-title') or [''])[0]} {i.get('year')}] "
                 f"{str(i.get('title'))[:50]}" for i in items[1:4]],
    }


def openalex(query):
    u = 'https://api.openalex.org/works?' + urllib.parse.urlencode(
        {'search': query, 'per-page': 4, 'mailto': 'sanghos@allenai.org'})
    res = json.loads(get(u))['results']
    if not res:
        return None
    top = res[0]
    doi = (top.get('doi') or '').replace('https://doi.org/', '')
    if doi:
        bib = get(f'https://doi.org/{doi}', accept='application/x-bibtex').strip()
    else:
        # hand-build: OpenAlex has no BibTeX endpoint, and books often lack a DOI
        auth = ' and '.join(a['author']['display_name']
                            for a in top.get('authorships', [])[:12])
        loc = ((top.get('primary_location') or {}).get('source') or {})
        key = re.sub(r'\W', '', (auth.split(' and ')[0].split()[-1]
                                 if auth else 'anon')) + str(top.get('publication_year', ''))
        typ = 'book' if top.get('type') == 'book' else 'article'
        bib = (f'@{typ}{{{key},\n  author = {{{auth}}},\n'
               f'  title = {{{top.get("title")}}},\n'
               f'  year = {{{top.get("publication_year")}}},\n'
               + (f'  journal = {{{loc.get("display_name")}}},\n'
                  if loc.get('display_name') else '')
               + (f'  publisher = {{{loc.get("host_organization_name")}}},\n'
                  if loc.get('host_organization_name') else '')
               + '}')
    return {
        'bib': bib, 'source': 'openalex',
        'chose': f"[{top.get('type')} {top.get('publication_year')}] {top.get('title')}",
        'alts': [f"[{r.get('publication_year')}] {str(r.get('title'))[:50]}"
                 for r in res[1:4]],
    }


def resolve(query):
    """First source that returns a confident match wins; otherwise report the
    best REVIEW candidate so a human can judge rather than getting nothing."""
    fallback = None
    for fn in (dblp, crossref, openalex):
        try:
            r = fn(query)
        except Exception as e:
            continue
        if not r:
            continue
        ok, why = judge(query, r['bib'])
        r['ok'], r['why'] = ok, why
        if ok:
            return r
        fallback = fallback or r
    return fallback


MONTHS = {'jan':'jan','feb':'feb','mar':'mar','apr':'apr','may':'may','june':'jun',
          'jun':'jun','july':'jul','jul':'jul','aug':'aug','sept':'sep','sep':'sep',
          'oct':'oct','nov':'nov','dec':'dec'}


def fix_months(bib):
    """Crossref emits `month=Sept` / `month=June`. BibTeX's built-in month macros
    are 3-letter lowercase, so anything else raises
    `Warning--string name "sept" is undefined`."""
    return re.sub(r'month\s*=\s*([A-Za-z]+)',
                  lambda m: 'month=' + MONTHS.get(m.group(1).lower(), m.group(1).lower()),
                  bib)


def rekey(bib, citekey):
    """Force our own stable citekey; DBLP emits DBLP:conf/... which is ugly in
    prose and collides with nothing we control."""
    return fix_months(
        re.sub(r'^(@\w+\s*\{)[^,]*,', r'\g<1>' + citekey + ',', bib.strip(), count=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--file'); ap.add_argument('--query'); ap.add_argument('--bib')
    a = ap.parse_args()

    if a.query:
        pairs = [('tmpkey', a.query)]
    else:
        pairs = []
        for ln in open(a.file):
            ln = ln.strip()
            if not ln or ln.startswith('#'):
                continue
            k, _, q = ln.partition('\t')
            pairs.append((k.strip(), q.strip() or k.strip()))

    out, ok_n, rev_n, miss = [], 0, 0, []
    for key, q in pairs:
        r = resolve(q)
        if not r:
            miss.append(key)
            print(f'MISS    {key:28} no hit in dblp/crossref/openalex   <- {q}')
            sys.stdout.flush()
            continue
        tag = 'OK' if r['ok'] else 'REVIEW'
        ok_n, rev_n = ok_n + r['ok'], rev_n + (not r['ok'])
        print(f"{tag:7} {key:28} {r['source']:9} {r['chose'][:72]}")
        if not r['ok']:
            print(f"        {'':28} ^ {r['why']}")
        for alt in r['alts']:
            print(f"        {'':28} alt: {alt}")
        sys.stdout.flush()
        out.append(f"% {tag} via {r['source']} | query: {q}\n"
                   f"% chose: {r['chose']}\n"
                   + (f"% WHY REVIEW: {r['why']}\n" if not r['ok'] else '')
                   + rekey(r['bib'], key))

    print(f"\n{'='*70}\nOK {ok_n}   REVIEW {rev_n}   MISS {len(miss)}")
    if miss:
        print('missing: ' + ', '.join(miss))
    if a.bib and out:
        open(a.bib, 'w').write('\n\n'.join(out) + '\n')
        print(f'wrote {a.bib}')


if __name__ == '__main__':
    main()
