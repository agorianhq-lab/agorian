#!/usr/bin/env python3
"""Validate Agorian's content files. Run from the repository root:

    python3 tools/validate.py          # exit 1 and list every problem if anything is wrong

Checks every course in courses/: its bank (questions and terms), short answers, sources or scenarios and
Myth or fact statements, and that every image key referenced by the data, the page or the timeline exists
in img/. build.py runs this first and refuses to build on errors, and the GitHub workflow runs it on every push.
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS = set()
TYPES = {'mc', 'ms', 'gaps', 'text', 'short', 'extended'}
errors = []
SOURCE_IMGS = set()  # images named by course files and data; counted as used

def err(where, msg): errors.append(f'{where}: {msg}')
def nonempty(s): return isinstance(s, str) and s.strip() != ''
def load(rel):
    path = os.path.join(ROOT, rel)
    try:
        with open(path, encoding='utf-8') as f: return json.load(f)
    except Exception as e:
        err(rel, f'cannot parse: {e}'); return None

def images():
    # shared artwork in img/ plus each course's own folder, img/<course>/
    out = set()
    for d, _, files in os.walk(os.path.join(ROOT, 'img')):
        out |= {f.rsplit('.', 1)[0] for f in files if f.endswith(('.jpg', '.svg'))}
    return out

def check_question(q, imgs):
    w = f"bank.json question {q.get('id', '?')}"
    if not isinstance(q.get('id'), int): err(w, 'id must be an integer')
    if q.get('unit') not in UNITS: err(w, f"unit {q.get('unit')!r} not in {sorted(UNITS)}")
    for k in ('topic', 'skill', 'question'):
        if not nonempty(q.get(k)): err(w, f'{k} is blank')
    t = q.get('type')
    if t not in TYPES: err(w, f'type {t!r} not in {sorted(TYPES)}'); return
    if q.get('stimulus') is not None and not nonempty(q.get('stimulus')): err(w, 'stimulus must be null or text')
    if t in ('mc', 'ms', 'gaps', 'text') and not nonempty(q.get('explanation')): err(w, 'explanation is blank')
    if t == 'short' and not nonempty(q.get('explanation')): err(w, 'short answer needs an explanation (the model answer)')
    if t in ('mc', 'ms'):
        opts = q.get('options'); ans = q.get('answer')
        if not isinstance(opts, list) or not 2 <= len(opts) <= 8 or not all(nonempty(o) for o in opts): err(w, 'options must be 2 to 8 non-empty strings')
        elif len(set(opts)) != len(opts): err(w, 'duplicate options')
        if not isinstance(ans, list) or not ans or not all(isinstance(a, int) for a in ans): err(w, 'answer must be a list of option indices')
        elif opts:
            if any(a < 0 or a >= len(opts) for a in ans): err(w, f'answer index out of range (options: {len(opts)})')
            if len(set(ans)) != len(ans): err(w, 'duplicate answer indices')
            if t == 'mc' and len(ans) != 1: err(w, 'mc must have exactly one answer')
            if t == 'ms' and len(ans) >= len(opts): err(w, 'ms must leave at least one option wrong')
    elif t == 'gaps':
        seg, bl, ch = q.get('segments'), q.get('blanks'), q.get('choices')
        if not (isinstance(seg, list) and isinstance(bl, list) and isinstance(ch, list)): err(w, 'gaps need segments, blanks and choices lists'); return
        if len(seg) != len(bl) + 1: err(w, f'segments ({len(seg)}) must be one more than blanks ({len(bl)})')
        if len(ch) != len(bl): err(w, f'choices ({len(ch)}) must match blanks ({len(bl)})')
        for i, (b_, c) in enumerate(zip(bl, ch)):
            if not isinstance(c, list) or len(c) < 2: err(w, f'blank {i}: fewer than two choices')
            elif b_ not in c: err(w, f'blank {i}: answer {b_!r} is not among its choices')
    elif t == 'text':
        ans = q.get('answer')
        if not isinstance(ans, list) or not ans or not all(nonempty(a) for a in ans): err(w, 'text answer must be a non-empty list of accepted strings')
    elif t == 'extended':
        if q.get('answer') is not None: err(w, 'extended prompts carry no answer')

def check_bank(imgs, rel):
    b = load(rel)
    if b is None: return
    qs, terms = b.get('questions'), b.get('terms')
    if not isinstance(qs, list) or not isinstance(terms, list): err('bank.json', 'needs "questions" and "terms" lists'); return
    ids = [q.get('id') for q in qs]
    for i in {x for x in ids if ids.count(x) > 1}: err('bank.json', f'duplicate question id {i}')
    for q in qs: check_question(q, imgs)
    topic_units = {}
    for q in qs: topic_units.setdefault(q.get('topic'), set()).add(q.get('unit'))
    for tpc, us in topic_units.items():
        if len(us) > 1: err('bank.json', f'topic {tpc!r} appears under more than one unit: {sorted(map(str, us))}')
    names = [t.get('term') for t in terms]
    for n in {x for x in names if names.count(x) > 1}: err('bank.json', f'duplicate term {n!r}')
    for t in terms:
        if not nonempty(t.get('term')) or not nonempty(t.get('definition')): err(f"bank.json term {t.get('term', '?')!r}", 'term and definition must be non-empty')
        if t.get('unit') is not None and t['unit'] not in UNITS: err(f"bank.json term {t.get('term')!r}", f"unit {t['unit']!r} not in {sorted(UNITS)}")
    print(f'{rel}: {len(qs)} questions, {len(terms)} terms')

def check_shortq(imgs, rel):
    d = load(rel)
    if d is None: return
    if not isinstance(d, list): err('shortq.json', 'must be a list'); return
    ids = [s.get('id') for s in d]
    for i in {x for x in ids if ids.count(x) > 1}: err('shortq.json', f'duplicate id {i}')
    for s in d:
        w = f"shortq.json {s.get('id', '?')}"
        for k in ('unit', 'topic', 'cmd', 'q'):
            if not nonempty(s.get(k)): err(w, f'{k} is blank')
        if not isinstance(s.get('marks'), int) or not 1 <= s['marks'] <= 8: err(w, 'marks must be an integer from 1 to 8')
        crit = s.get('criteria')
        if not isinstance(crit, list) or not crit or not all(nonempty(c) for c in crit): err(w, 'criteria must be a non-empty list of strings')
        full = s.get('full') or {}
        if not nonempty(full.get('text')) or not nonempty(full.get('why')): err(w, 'full answer needs text and why')
        src = s.get('source')
        if src is not None:
            if not nonempty(src.get('caption')): err(w, 'source needs a caption')
            if src.get('img'):
                SOURCE_IMGS.add(src['img'])
                if src['img'] not in imgs: err(w, f"source image {src['img']!r} missing from img/")
            elif not nonempty(src.get('text')): err(w, 'source needs img or text')
    print(f'{rel}: {len(d)} questions')

def check_sources(imgs, rel):
    d = load(rel)
    if d is None: return
    srcs = d.get('sources'); chk = d.get('checklist')
    if not isinstance(srcs, list) or not isinstance(chk, list) or not chk: err('sources.json', 'needs "sources" and a non-empty "checklist"'); return
    ids = [s.get('id') for s in srcs]
    for i in {x for x in ids if ids.count(x) > 1}: err('sources.json', f'duplicate id {i}')
    for s in srcs:
        w = f"sources.json {s.get('id', '?')}"
        if s.get('unit') not in UNITS: err(w, f"unit {s.get('unit')!r} not in {sorted(UNITS)}")
        if not nonempty(s.get('caption')): err(w, 'caption is blank')
        if s.get('img'):
            SOURCE_IMGS.add(s['img'])
            if s['img'] not in imgs: err(w, f"image {s['img']!r} missing from img/")
        elif not nonempty(s.get('text')): err(w, 'needs img or text')
        qs = s.get('qs')
        if not isinstance(qs, list) or len(qs) != 4: err(w, 'needs exactly four quick questions')
        else:
            for i, q in enumerate(qs):
                o = q.get('o'); a = q.get('a')
                if not nonempty(q.get('q')) or not nonempty(q.get('x')): err(w, f'quick question {i}: q and x must be non-empty')
                if not isinstance(o, list) or not 2 <= len(o) <= 6 or not all(nonempty(x) for x in o): err(w, f'quick question {i}: 2 to 6 non-empty options')
                elif not isinstance(a, int) or not 0 <= a < len(o): err(w, f'quick question {i}: answer index out of range')
        if any(k in s for k in ('write', 'model', 'mark')):  # a timed write is optional; if present it must be complete
            for k in ('write', 'model'):
                if not nonempty(s.get(k)): err(w, f'{k} is blank')
            if not isinstance(s.get('mark'), list) or not s['mark']: err(w, 'mark points must be a non-empty list')
    print(f'{rel}: {len(srcs)} sources')

def check_mythfact(rel):
    d = load(rel)
    if d is None: return
    if not isinstance(d, list) or not d: err(rel, 'must be a non-empty list'); return
    seen = set()
    for i, x in enumerate(d):
        w = f'{rel} item {i + 1}'
        if not (isinstance(x, list) and len(x) == 3 and nonempty(x[0]) and isinstance(x[1], bool) and nonempty(x[2])): err(w, 'must be [statement, true/false, why]'); continue
        if x[0] in seen: err(w, 'duplicate statement')
        seen.add(x[0])
        if len(x[0]) > 120: err(w, f'statement is {len(x[0])} characters; keep it under 120 so it fits the tile')
    myths = sum(1 for x in d if isinstance(x, list) and len(x) == 3 and x[1] is False)
    print(f'{rel}: {len(d)} statements, {myths} myths')

def check_play(rel):
    d = load(rel)
    if d is None: return
    items = d.get('items')
    if not isinstance(items, list) or not items: err(rel, 'needs a non-empty "items" list'); return
    ids = [p.get('id') for p in items]
    for i in {x for x in ids if ids.count(x) > 1}: err(rel, f'duplicate id {i}')
    for p in items:
        w = f"{rel} {p.get('id', '?')}"
        if not nonempty(p.get('title')) or not nonempty(p.get('blurb')): err(w, 'title and blurb must be non-empty')
        k = p.get('kind')
        if k == 'sort':
            bins = p.get('bins')
            if not isinstance(bins, list) or len(bins) != 3: err(w, 'sort needs three bins'); continue
            for it in p.get('items', []):
                if not (isinstance(it, list) and len(it) == 3 and nonempty(it[0]) and isinstance(it[1], int) and 0 <= it[1] < 3 and nonempty(it[2])): err(w, f'bad sort item {it!r}')
            if len(p.get('items', [])) < 12: err(w, 'sort needs at least 12 items')
        elif k == 'law':
            for col in p.get('columns', []):
                if not nonempty(col.get('label')) or not isinstance(col.get('options'), list) or len(col['options']) < 2: err(w, f"column {col.get('id')!r} needs a label and at least two options")
                for o in col.get('options', []):
                    if not nonempty(o.get('t')) or not nonempty(o.get('why')): err(w, f"option {o.get('t')!r} needs t and why")
        elif k not in ('referendum', 'government'): err(w, f'unknown kind {k!r}')
    print(f'{rel}: {len(items)} interactives')

def check_course(path, imgs):
    global UNITS
    c = load(os.path.relpath(path, ROOT))
    if c is None: return
    rel = os.path.relpath(path, ROOT)
    for k in ('id', 'out', 'subtitle', 'description', 'data', 'units', 'hero', 'welcome', 'breakdown', 'modes', 'verdicts'):
        if k not in c: err(rel, f'missing {k!r}')
    UNITS = {u.get('name') for u in c.get('units', [])}
    named = [u.get('img') for u in c.get('units', [])] + [m.get('img') for m in c.get('modes', [])] + [c.get('hero', {}).get('img')] + list((c.get('resultsImg') or {}).values())
    for u in c.get('units', []):
        if u.get('cls') not in ('eu', 'jp', 'sk'): err(rel, f"unit {u.get('name')!r}: cls must be eu, jp or sk (the three colour slots)")
    for k in named:
        if k: SOURCE_IMGS.add(k)
        if k and k not in imgs: err(rel, f"image {k!r} missing from img/")
    if not isinstance(c.get('verdicts'), list) or len(c.get('verdicts', [])) != 4: err(rel, 'verdicts must be four strings')
    d = c.get('data', {})
    if d.get('bank'): check_bank(imgs, d['bank'])
    else: err(rel, 'data.bank is required')
    if d.get('shortq'): check_shortq(imgs, d['shortq'])
    if d.get('sources'): check_sources(imgs, d['sources'])
    if d.get('mythfact'): check_mythfact(d['mythfact'])
    if d.get('play'): check_play(d['play'])
    if c.get('tile') == 'mythfact' and not d.get('mythfact'): err(rel, 'tile is mythfact but data.mythfact is not set')

def check_images(imgs):
    page = open(os.path.join(ROOT, 'src', 'index.html'), encoding='utf-8').read()
    chrono = open(os.path.join(ROOT, 'tools', 'chrono.py'), encoding='utf-8').read()
    keys = set(re.findall(r"IMG\['([a-z0-9-]+)'\]", page)) | set(re.findall(r"'(f-[a-z0-9]+)'", page)) | set(re.findall(r"'(eu-[a-z0-9]+|jp-[a-z0-9]+)'", page))
    keys |= set(re.findall(r"return '([a-z0-9-]+)'", page[page.find('function stimImg'):page.find('function stimImg') + 600]))
    # timeline: every period band expects a background image; event thumbnails are optional
    sys.path.insert(0, os.path.join(ROOT, 'tools'))
    import chrono
    for a, b, name, k in chrono.EUP + chrono.JPP:
        if k: keys.add(f'tlb-{k}')
    thumbs = sum(1 for yr, *_ in chrono.EU + chrono.JP if f'tl-{yr}' in imgs)
    for k in sorted(keys):
        if k not in imgs: err('images', f'{k!r} is referenced but img/{k}.jpg does not exist')
    unused = sorted(k for k in imgs if k not in keys and not k.startswith('tl-') and k not in SOURCE_IMGS)
    print(f'images: {len(keys)} keys referenced by the page and timeline, {thumbs} timeline thumbnails' + (f'; unused: {", ".join(unused)}' if unused else ''))

def main():
    imgs = images()
    for path in sorted(glob.glob(os.path.join(ROOT, 'courses', '*.json'))):
        if not path.endswith('.variants.json'): check_course(path, imgs)
    check_images(imgs)
    if errors:
        print(f'\n{len(errors)} problem(s):'); [print(' -', e) for e in errors]; return 1
    print('all checks passed'); return 0

if __name__ == '__main__':
    sys.exit(main())
