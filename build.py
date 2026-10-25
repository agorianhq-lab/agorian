"""Build Agorian.
  python3 build.py            -> docs/index.html with images as separate files (for hosting)
  python3 build.py --inline   -> docs/index.html with images embedded (for the Claude preview)
"""
import json,base64,glob,os,sys,shutil
inline='--inline' in sys.argv
s=open('src/index.html').read()
b=json.load(open('data/bank.json'))
for q in b['questions']: q.pop('srcId',None); q.pop('source',None)
sq=json.load(open('data/shortq.json'))
b['shortq']=sq
js=json.dumps(b,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
os.makedirs('docs/img',exist_ok=True)
img={}
for f in sorted(glob.glob('img/*.jpg')):
    k=os.path.basename(f)[:-4]
    if inline: img[k]='data:image/jpeg;base64,'+base64.b64encode(open(f,'rb').read()).decode()
    else: img[k]='img/'+os.path.basename(f); shutil.copy(f,'docs/img/')
out=s.replace('__BANK__',js).replace('__IMG__',json.dumps(img))
if not inline:
    # hosted page needs the document skeleton the preview adds for us
    out='<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="description" content="Agorian. Year 8 Humanities revision for Medieval Europe and Shogunate Japan. Challenge what you know."><link rel="icon" href="favicon.svg" type="image/svg+xml"><meta property="og:type" content="website"><meta property="og:site_name" content="Agorian"><meta property="og:title" content="Agorian. Challenge what you know."><meta property="og:description" content="Year 8 History revision for Medieval Europe and Shogunate Japan. Quick questions with explanations, timed challenges, a timeline game, flashcards and paragraph practice."><meta property="og:url" content="https://agorian.au/"><meta property="og:image" content="https://agorian.au/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#243A6B"><style>[hidden]{display:none!important}img{max-width:100%}</style></head><body>'+out+'</body></html>'
open('docs/index.html','w').write(out)
print('built', 'inline' if inline else 'hosted', len(out)//1024,'KB')
