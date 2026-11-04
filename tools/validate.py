#!/usr/bin/env python3
"""Validate Agorian's content files. Run from the repository root:

    python3 tools/validate.py          # exit 1 and list every problem if anything is wrong

Checks data/bank.json (questions and terms), data/shortq.json, data/sources.json, and that every
image key referenced by the data, the page or the timeline exists in img/. build.py runs this first
and refuses to build on errors, and the GitHub workflow runs it on every push.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS = {'Medieval Europe', 'Shogunate Japan', 'Skills and concepts'}
TYPES = {'mc', 'ms', 'gaps', 'text', 'short', 'extended'}
errors = []
SOURCE_IMGS = set()

def err(where, msg): errors.append(f'{where}: {msg}')
def nonempty(s): return isinstance(s, str) and s.strip() != ''
def load(rel):
    path = os.path.join(ROOT, rel)
    try:
        with open(path, encoding='utf-8') as f: return json.load(f)
    except Exception as e:
        err(rel, f'cannot parse: {e}'); return None

def images():
    return {f[:-4] for f in os.listdir(os.path.join(ROOT, 'img')) if f.endswith('.jpg')}

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

def check_bank(imgs):
    b = load('data/bank.json')
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
    print(f'bank.json: {len(qs)} questions, {len(terms)} terms')

def check_shortq(imgs):
    d = load('data/shortq.json')
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
    print(f'shortq.json: {len(d)} questions')

def check_sources(imgs):
    d = load('data/sources.json')
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
        for k in ('write', 'model'):
            if not nonempty(s.get(k)): err(w, f'{k} is blank')
        if not isinstance(s.get('mark'), list) or not s['mark']: err(w, 'mark points must be a non-empty list')
    print(f'sources.json: {len(srcs)} sources')

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
    check_bank(imgs); check_shortq(imgs); check_sources(imgs); check_images(imgs)
    if errors:
        print(f'\n{len(errors)} problem(s):'); [print(' -', e) for e in errors]; return 1
    print('all checks passed'); return 0

if __name__ == '__main__':
    sys.exit(main())
