import json, re, difflib
from collections import Counter

raw = json.load(open('raw.json'))

def clean(s):
    return re.sub(r'\s+', ' ', (s or '')).strip()

def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', clean(s).lower())

# ---------- topic inference for untagged Socrative questions ----------
TOPIC_RULES = [
    ('Shogunate Japan', 'Meiji Restoration', r'meiji|perry|1853|1854|1868|modernis|western technology|conscript|prefecture|constitution|turn(ed)? against the shogun'),
    ('Shogunate Japan', 'Tokugawa Shogunate', r'tokugawa|sakoku|sankin|ieyasu|sekigahara|edict|christianity|merchants grew|four classes|rank farmers|isolation'),
    ('Shogunate Japan', 'Feudalism and samurai', r'samurai|daimyo|bushido|shogun|genpei|japan|emperor|1192'),
    ('Medieval Europe', 'The Black Death', r'black death|plague|flagellant|1347'),
    ('Medieval Europe', 'The Crusades', r'crusade|jerusalem|1099|holy|first crusade'),
    ('Medieval Europe', 'Catholic Church', r'church|pope|tithe|excommunicat|monk|clergy|priest|bishop'),
    ('Medieval Europe', 'Law and order', r'punish|crime|trial|ordeal|treason|stocks|pillory'),
    ('Medieval Europe', 'Castles and knights', r'castle|knight|chivalry|motte|concentric'),
    ('Medieval Europe', 'Feudalism and hierarchy', r'feudal|vassal|serf|lord|fief|peasant|hierarchy|manor'),
    ('Skills and concepts', 'Source analysis', r'source|caption|manuscript|origin'),
    ('Skills and concepts', 'Chronology', r'happened first|in order|century'),
]
def infer_topic(qtext, opts):
    t = qtext.lower()
    if re.search(r'both medieval europe and|european feudal role|japanese equivalent|hastings or the genpei|happened first', t):
        return ('Skills and concepts', 'Comparing the two societies')
    if re.search(r'source is captioned|which century', t):
        return ('Skills and concepts', 'Source analysis')
    for unit, topic, pat in TOPIC_RULES:
        if re.search(pat, t):
            return (unit, topic)
    o = ' '.join(opts).lower()
    for unit, topic, pat in TOPIC_RULES:
        if re.search(pat, o):
            return (unit, topic)
    return ('Skills and concepts', 'Historical concepts')

bank = []
nid = 0
def add(q):
    global nid
    nid += 1
    q['id'] = nid
    bank.append(q)

# ---------- EP bank ----------
for r in raw['ep']:
    typ = r['EP question type']
    base = dict(unit=r['Unit'], topic=r['Topic'], skill=clean(r['Exam skill or knowledge tested']),
                stimulus=clean(r['Stimulus (text to paste as text stimulus)']) or None,
                explanation=clean(r['Feedback shown to students']), source='EP', srcId=r['ID'])
    opts = [clean(r[k]) for k in ('Option A','Option B','Option C','Option D') if r[k]]
    correct = clean(r['Correct answer'])
    qtext = clean(r['Question'])
    if typ == 'Multiple choice':
        add(dict(base, type='mc', question=qtext, options=opts, answer=['ABCD'.index(correct)]))
    elif typ == 'True/False':
        add(dict(base, type='mc', question=qtext, options=['True','False'], answer=[0 if correct.lower()=='true' else 1]))
    elif typ == 'Multiple select':
        add(dict(base, type='ms', question=qtext, options=opts, answer=['ABCD'.index(c.strip()) for c in correct.split(',')]))
    elif typ == 'Textbox (exact answer)':
        add(dict(base, type='text', question=qtext, answer=[correct.lower()]))
    elif typ == 'Fill the gaps (dropdown)':
        full = r['Question'] or ''
        blanks = re.findall(r'\[([^\]]+)\]', full)
        optA = r['Option A'] or ''
        # option lists
        if 'Each blank offers' in optA:
            m = re.search(r'offers[^:]*:?\s*(.*)', optA)
            pool = [o.strip() for o in re.split(r'\s/\s|/', m.group(1))] if m else blanks
            if 'all six events' in optA or 'all four punishments' in optA:
                pool = blanks
            choices = [pool for _ in blanks]
        else:
            choices = []
            for k in ('Option A','Option B','Option C','Option D'):
                if r[k] and 'options:' in r[k]:
                    choices.append([o.strip() for o in r[k].split('options:')[1].split('/')])
        # split passage into segments around blanks
        intro, _, passage = full.partition('\n') if '\n' in full else ('', '', full)
        segs = re.split(r'\[[^\]]+\]', passage)
        add(dict(base, type='gaps', question=clean(intro) or 'Complete the passage.',
                 segments=[clean(s) for s in segs], blanks=blanks, choices=choices))
    elif typ == 'Highlight':
        stim = base['stimulus'] or ''
        quote = re.search(r'"(.*)"', stim)
        body = quote.group(1) if quote else stim
        caption = stim.split('"')[0].strip()
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', body) if s.strip()]
        targets = [c.strip().lower() for c in correct.split(';')]
        ans = [i for i,s in enumerate(sents) if any(t in s.lower() for t in targets)]
        q = qtext.replace('Highlight', 'Select').replace('phrases', 'sentences').replace('phrase', 'sentence').replace('the rule', 'the sentence with the rule')
        add(dict(base, stimulus=caption, type='ms' if len(ans)>1 else 'mc', question=q, options=sents, answer=ans))
    elif typ == 'Extended Response':
        add(dict(base, type='extended', question=qtext, guidance=base['explanation']))

# ---------- Socrative ----------
seen = [norm(q['question']) for q in bank]
def is_dup(text):
    n = norm(text)
    for s in seen:
        if difflib.SequenceMatcher(None, n, s).ratio() > 0.82:
            return True
    return False

for key in ('soc_exam','soc_warm','soc_me'):
    for r in raw[key]:
        qtext = clean(r['q'])
        if is_dup(qtext):
            continue
        unit, topic = infer_topic(qtext, r['opts'])
        base = dict(unit=unit, topic=topic, skill='', stimulus=None, explanation=clean(r['expl']), source='Socrative', srcId=key)
        if r['type'] == 'Multiple choice':
            ans = ['ABCDE'.index(c) for c in r['correct']]
            typ = 'ms' if len(ans) > 1 else 'mc'
            q = qtext
            if typ == 'mc' and q.lower().startswith('select all'):
                typ = 'ms'
            add(dict(base, type=typ, question=q, options=r['opts'], answer=ans))
        else:
            add(dict(base, type='short', question=qtext, model=clean(r['expl'])))
        seen.append(norm(qtext))

terms = [dict(term=clean(t['term']), definition=clean(t['def'])) for t in raw['terms']]

json.dump(dict(questions=bank, terms=terms), open('bank.json','w'), indent=1, ensure_ascii=False)
print('questions', len(bank))
print(Counter(q['type'] for q in bank))
print(Counter((q['unit'], q['topic']) for q in bank))
for q in bank:
    if q['source']=='Socrative': print(' ', q['unit'][:8], '|', q['topic'][:22].ljust(22), '|', q['question'][:80])
