"""Build Agorian.
  python3 build.py            -> docs/index.html with images as separate files (for hosting)
  python3 build.py --inline   -> docs/index.html with images embedded (for the Claude preview)
"""
import json,base64,glob,os,sys,shutil
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'tools'))
import chrono
inline='--inline' in sys.argv
s=open('src/index.html').read()
b=json.load(open('data/bank.json'))
for q in b['questions']: q.pop('srcId',None); q.pop('source',None)
sq=json.load(open('data/shortq.json'))
b['shortq']=sq
b['marker']=json.load(open('data/marker.json'))
b['sources']=json.load(open('data/sources.json'))
js=json.dumps(b,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
os.makedirs('docs/img',exist_ok=True)
img={}
for f in sorted(glob.glob('img/*.jpg')):
    k=os.path.basename(f)[:-4]
    if k.startswith('p-'): continue  # raw band sources, used only by the sandbox
    if inline: img[k]='data:image/jpeg;base64,'+base64.b64encode(open(f,'rb').read()).decode()
    else: img[k]='img/'+os.path.basename(f); shutil.copy(f,'docs/img/')
ccss,chtml,_=chrono.render(img)
# Fonts are served by the site itself (no Google Fonts dependency). Numerals in the display face come from
# Atkinson Hyperlegible Next (variable weight): Fraunces draws its 8 with the large bowl on top, which reads as upside down.
# Every face in the composite family must carry the same weight descriptor (100 900) or Chromium will not fall through between them.
os.makedirs('docs/fonts',exist_ok=True)
def fsrc(name):
    if inline: return 'data:font/woff2;base64,'+base64.b64encode(open('fonts/'+name,'rb').read()).decode()
    shutil.copy('fonts/'+name,'docs/fonts/'); return 'fonts/'+name
DIG='U+0030-0039'; NODIG='U+0000-002F,U+003A-FFFF'
fonts=(f'@font-face{{font-family:"Fraunces";src:url({fsrc("fraunces.woff2")}) format("woff2");font-weight:100 900;font-style:normal;font-display:swap;unicode-range:{NODIG}}}'
 f'@font-face{{font-family:"Fraunces";src:url({fsrc("atkinson-next-digits.woff2")}) format("woff2");font-weight:100 900;font-style:normal;font-display:swap;unicode-range:{DIG}}}'
 f'@font-face{{font-family:"Atkinson Hyperlegible";src:url({fsrc("atkinson-400.woff2")}) format("woff2");font-weight:400;font-style:normal;font-display:swap}}'
 f'@font-face{{font-family:"Atkinson Hyperlegible";src:url({fsrc("atkinson-700.woff2")}) format("woff2");font-weight:700;font-style:normal;font-display:swap}}'
 f'@font-face{{font-family:"Atkinson Hyperlegible";src:url({fsrc("atkinson-400i.woff2")}) format("woff2");font-weight:400;font-style:italic;font-display:swap}}')
out=s.replace('/*__FONTS__*/',fonts).replace('__BANK__',js).replace('__IMG__',json.dumps(img)).replace('/*__CHRONO_CSS__*/',ccss).replace('__CHRONO__',json.dumps(chtml,ensure_ascii=False).replace('</','<\\/'))
if not inline:
    # hosted page needs the document skeleton the preview adds for us
    import re
    title=re.search(r'<title>.*?</title>',out); out=out.replace(title.group(0),'') if title else out
    out='<!doctype html><html lang="en-AU"><head><meta charset="utf-8">'+(title.group(0) if title else '<title>Agorian</title>')+'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="description" content="Agorian. Year 8 Humanities revision for Medieval Europe and Shogunate Japan. Challenge what you know."><link rel="icon" href="favicon.svg" type="image/svg+xml"><meta property="og:type" content="website"><meta property="og:site_name" content="Agorian"><meta property="og:title" content="Agorian. Challenge what you know."><meta property="og:description" content="Year 8 History revision for Medieval Europe and Shogunate Japan. Quick questions with explanations, timed challenges, a timeline game, flashcards and paragraph practice."><meta property="og:url" content="https://agorian.au/"><meta property="og:image" content="https://agorian.au/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#243A6B"><style>[hidden]{display:none!important}img{max-width:100%}</style></head><body>'+out+'</body></html>'
open('docs/index.html','w').write(out)
print('built', 'inline' if inline else 'hosted', len(out)//1024,'KB')
