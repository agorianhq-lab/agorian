"""Build Agorian.
  python3 build.py                        -> docs/index.html for the History course (hosting)
  python3 build.py --course civics        -> docs/civics/index.html for the Civics course
  python3 build.py --inline [--course X]  -> preview/<course>.html, one file with images and fonts embedded

Each course is described by courses/<id>.json: its units, modes, copy and data files. The page reads that
description at run time (COURSE), so one src/index.html serves every course.
"""
import json,base64,glob,os,sys,shutil,re
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'tools'))
import validate
if validate.main()!=0: sys.exit('build stopped: fix the problems above')
inline='--inline' in sys.argv
course_id=sys.argv[sys.argv.index('--course')+1] if '--course' in sys.argv else 'history'
C=json.load(open(f'courses/{course_id}.json',encoding='utf-8'))
s=open('src/index.html',encoding='utf-8').read()
b=json.load(open(C['data']['bank'],encoding='utf-8'))
for q in b['questions']: q.pop('srcId',None); q.pop('source',None)
b['shortq']=json.load(open(C['data']['shortq'],encoding='utf-8')) if C['data'].get('shortq') else []
b['sources']=json.load(open(C['data']['sources'],encoding='utf-8')) if C['data'].get('sources') else {'sources':[],'checklist':[]}
b['mythfact']=json.load(open(C['data']['mythfact'],encoding='utf-8')) if C['data'].get('mythfact') else []
esc=lambda j: json.dumps(j,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
js=esc(b)
out_dir='preview' if inline else C['out']
os.makedirs(out_dir,exist_ok=True)
# images: the History page refers to its artwork by name throughout, so it takes every file; other courses take only what they name
want=None if course_id=='history' else json.dumps(C)+json.dumps(b)
img={}
for f in sorted(glob.glob('img/*.jpg')):
    k=os.path.basename(f)[:-4]
    if k.startswith('p-'): continue  # raw band sources, used only by the sandbox
    if want is not None and f'"{k}"' not in want: continue
    if inline: img[k]='data:image/jpeg;base64,'+base64.b64encode(open(f,'rb').read()).decode()
    else: os.makedirs(f'{out_dir}/img',exist_ok=True); img[k]='img/'+os.path.basename(f); shutil.copy(f,f'{out_dir}/img/')
has_timeline=any(m['id']=='timeline' for m in C['modes'])
if has_timeline:
    import chrono
    ccss,chtml,_=chrono.render(img)
else: ccss,chtml='',''
# Fonts are served by the site itself (no Google Fonts dependency). Numerals in the display face come from
# Atkinson Hyperlegible Next (variable weight): Fraunces draws its 8 with the large bowl on top, which reads as upside down.
# Every face in the composite family must carry the same weight descriptor (100 900) or Chromium will not fall through between them.
def fsrc(name):
    if inline: return 'data:font/woff2;base64,'+base64.b64encode(open('fonts/'+name,'rb').read()).decode()
    os.makedirs(f'{out_dir}/fonts',exist_ok=True); shutil.copy('fonts/'+name,f'{out_dir}/fonts/'); return 'fonts/'+name
DIG='U+0030-0039'; NODIG='U+0000-002F,U+003A-FFFF'
fonts=(f'@font-face{{font-family:"Fraunces";src:url({fsrc("fraunces.woff2")}) format("woff2");font-weight:100 900;font-style:normal;font-display:swap;unicode-range:{NODIG}}}'
 f'@font-face{{font-family:"Fraunces";src:url({fsrc("atkinson-next-digits.woff2")}) format("woff2");font-weight:100 900;font-style:normal;font-display:swap;unicode-range:{DIG}}}'
 f'@font-face{{font-family:"Atkinson Hyperlegible";src:url({fsrc("atkinson-400.woff2")}) format("woff2");font-weight:400;font-style:normal;font-display:swap}}'
 f'@font-face{{font-family:"Atkinson Hyperlegible";src:url({fsrc("atkinson-700.woff2")}) format("woff2");font-weight:700;font-style:normal;font-display:swap}}'
 f'@font-face{{font-family:"Atkinson Hyperlegible";src:url({fsrc("atkinson-400i.woff2")}) format("woff2");font-weight:400;font-style:italic;font-display:swap}}')
# per-course colours for the three unit slots (eu, jp, sk), light and dark
ccol=''
if C.get('colours'):
    light=''.join(f'--{k}:{v};' for k,v in C['colours']['light'].items()); dark=''.join(f'--{k}:{v};' for k,v in C['colours'].get('dark',{}).items())
    ccol=f':root{{{light}}}' + (f'@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{{dark}}}}}:root[data-theme="dark"]{{{dark}}}' if dark else '')
out=(s.replace('/*__FONTS__*/',fonts).replace('__BANK__',js).replace('__IMG__',json.dumps(img)).replace('/*__CHRONO_CSS__*/',ccss)
      .replace('__CHRONO__',json.dumps(chtml,ensure_ascii=False).replace('</','<\\/')).replace('__COURSE__',esc(C)).replace('/*__COURSE_CSS__*/',ccol))
if inline:
    path=f'{out_dir}/{course_id}.html'
else:
    # hosted page needs the document skeleton the preview adds for us
    title=re.search(r'<title>.*?</title>',out); out=out.replace(title.group(0),'') if title else out
    out=('<!doctype html><html lang="en-AU"><head><meta charset="utf-8">'+(title.group(0) if title else '<title>Agorian</title>')+'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
         f'<meta name="description" content="{C["description"]}"><link rel="icon" href="{"../" if "/" in C["out"] else ""}favicon.svg" type="image/svg+xml"><meta property="og:type" content="website"><meta property="og:site_name" content="Agorian"><meta property="og:title" content="Agorian. Challenge what you know."><meta property="og:description" content="{C["ogDescription"]}"><meta property="og:url" content="https://agorian.au/{"" if C["out"]=="docs" else C["out"].split("/",1)[1]+"/"}"><meta property="og:image" content="https://agorian.au/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#243A6B"><style>[hidden]{{display:none!important}}img{{max-width:100%}}</style></head><body>'+out+'</body></html>')
    path=f'{out_dir}/index.html'
open(path,'w',encoding='utf-8').write(out)
print('built', course_id, 'inline' if inline else 'hosted', path, len(out)//1024,'KB')
