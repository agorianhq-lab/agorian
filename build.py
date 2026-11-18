"""Build Agorian.
  python3 build.py                        -> docs/history/index.html for the History course (hosting)
  python3 build.py --course civics        -> docs/index.html for the Civics course, the site's front page
  python3 build.py --inline [--course X]  -> preview/<course>.html, one file with images and fonts embedded
  python3 build.py --inline --course X --variants
                                          -> the preview with a theme switcher, one theme per entry in courses/X.variants.json

Each course is described by courses/<id>.json: its units, modes, copy and data files. The page reads that
description at run time (COURSE), so one src/index.html serves every course.
"""
import json,base64,glob,os,sys,shutil,re
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'tools'))
import validate
if validate.main()!=0: sys.exit('build stopped: fix the problems above')
inline='--inline' in sys.argv
variants='--variants' in sys.argv
course_id=sys.argv[sys.argv.index('--course')+1] if '--course' in sys.argv else 'history'
C=json.load(open(f'courses/{course_id}.json',encoding='utf-8'))
V={}
if variants:
    if not inline: sys.exit('--variants is for --inline previews only')
    V=json.load(open(f'courses/{course_id}.variants.json',encoding='utf-8'))
    for k,v in V.items():  # a variant may inherit another's tokens
        base=V.get(v.get('inherits'))
        if base:
            for side in ('light','dark'): v[side]={**base.get(side,{}),**v.get(side,{})}
            v['fonts']=base.get('fonts',[])+v.get('fonts',[]); v['css']=base.get('css','')+v.get('css','')
s=open('src/index.html',encoding='utf-8').read()
b=json.load(open(C['data']['bank'],encoding='utf-8'))
for q in b['questions']: q.pop('srcId',None); q.pop('source',None)
b['shortq']=json.load(open(C['data']['shortq'],encoding='utf-8')) if C['data'].get('shortq') else []
b['sources']=json.load(open(C['data']['sources'],encoding='utf-8')) if C['data'].get('sources') else {'sources':[],'checklist':[]}
b['mythfact']=json.load(open(C['data']['mythfact'],encoding='utf-8')) if C['data'].get('mythfact') else []
b['play']=json.load(open(C['data']['play'],encoding='utf-8')) if C['data'].get('play') else {'items':[]}
b['errors']=json.load(open(C['data']['errors'],encoding='utf-8')) if C['data'].get('errors') else {'items':[]}
b['explain']=json.load(open(C['data']['explain'],encoding='utf-8')) if C['data'].get('explain') else {'items':[]}
esc=lambda j: json.dumps(j,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
js=esc(b)
out_dir='preview' if inline else C['out']
os.makedirs(out_dir,exist_ok=True)
# images: img/ holds the shared artwork and img/<course>/ anything only that course uses. The History page refers to its artwork
# by name throughout, so it takes every shared file; other courses take only what they name
want=None if course_id=='history' else json.dumps(C)+json.dumps(b)
img={}
for f in sorted(glob.glob('img/*.jpg')+glob.glob('img/*.svg')+glob.glob(f'img/{course_id}/*.jpg')+glob.glob(f'img/{course_id}/*.svg')):
    k=os.path.basename(f).rsplit('.',1)[0]
    if k.startswith('p-'): continue  # raw band sources, used only by the sandbox
    if want is not None and f'"{k}"' not in want: continue
    mime='image/svg+xml' if f.endswith('.svg') else 'image/jpeg'
    if inline: img[k]=f'data:{mime};base64,'+base64.b64encode(open(f,'rb').read()).decode()
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
extra_fonts=list(C.get('fonts',[]))+[f for v in V.values() for f in v.get('fonts',[])]
seen=set(); xf=''
for f in extra_fonts:
    if f['file'] in seen: continue
    seen.add(f['file']); xf+=f'@font-face{{font-family:"{f["family"]}";src:url({fsrc(f["file"])}) format("woff2");font-weight:{f.get("weight","400")};font-style:{f.get("style","normal")};font-display:swap}}'
fonts=xf+(f'@font-face{{font-family:"Fraunces";src:url({fsrc("fraunces.woff2")}) format("woff2");font-weight:100 900;font-style:normal;font-display:swap;unicode-range:{NODIG}}}'
 f'@font-face{{font-family:"Fraunces";src:url({fsrc("atkinson-next-digits.woff2")}) format("woff2");font-weight:100 900;font-style:normal;font-display:swap;unicode-range:{DIG}}}'
 f'@font-face{{font-family:"Atkinson Hyperlegible";src:url({fsrc("atkinson-400.woff2")}) format("woff2");font-weight:400;font-style:normal;font-display:swap}}'
 f'@font-face{{font-family:"Atkinson Hyperlegible";src:url({fsrc("atkinson-700.woff2")}) format("woff2");font-weight:700;font-style:normal;font-display:swap}}'
 f'@font-face{{font-family:"Atkinson Hyperlegible";src:url({fsrc("atkinson-400i.woff2")}) format("woff2");font-weight:400;font-style:italic;font-display:swap}}')
# per-course design tokens (unit slots eu, jp, sk; or any other --token), light and dark
def tokens(scope, light, dark):
    l=''.join(f'--{k}:{v};' for k,v in light.items()); d=''.join(f'--{k}:{v};' for k,v in dark.items())
    return (f'{scope}{{{l}}}' if l else '') + (f'@media (prefers-color-scheme: dark){{{scope}:not([data-theme="light"]){{{d}}}}}{scope}[data-theme="dark"]{{{d}}}' if d else '')
ccol=tokens(':root', C.get('colours',{}).get('light',{}), C.get('colours',{}).get('dark',{})) if C.get('colours') else ''
def prefix_css(css, pre):
    out=[]
    for rule in css.split('}'):
        if '{' not in rule: continue
        sel,body=rule.split('{',1); out.append(','.join(f'{pre} {x.strip()}' for x in sel.split(','))+'{'+body+'}')
    return ''.join(out)
vbar=''
if V:
    for name,v in V.items():
        scope=f':root[data-variant="{name}"]'
        ccol+=tokens(scope, v.get('light',{}), v.get('dark',{}))+prefix_css(v.get('css',''), scope)
    btns=''.join(f'<button type="button" data-v="{n}">{v["label"]}</button>' for n,v in V.items())
    vbar=('<div id="variantbar" style="position:fixed;left:12px;bottom:12px;z-index:50;display:flex;gap:6px;align-items:center;flex-wrap:wrap;padding:8px 10px;border-radius:12px;background:rgba(20,24,30,.92);color:#fff;font:600 12px/1 system-ui,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.3)"><span style="opacity:.75;margin-right:4px">Theme</span>'+btns+'</div>'
          '<style>#variantbar button{font:inherit;color:#fff;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);border-radius:8px;padding:6px 9px;cursor:pointer}#variantbar button.on{background:#E2B45C;color:#1B1F26;border-color:#E2B45C}</style>'
          '<script>(function(){var k="agorian:variant";var cur="";try{cur=localStorage.getItem(k)||""}catch(e){}var bs=document.querySelectorAll("#variantbar button");function set(v){cur=v;if(v&&v!=="'+list(V.keys())[0]+'")document.documentElement.setAttribute("data-variant",v);else document.documentElement.removeAttribute("data-variant");try{localStorage.setItem(k,v)}catch(e){}bs.forEach(function(b){b.classList.toggle("on",b.dataset.v===(v||"'+list(V.keys())[0]+'"))})}bs.forEach(function(b){b.onclick=function(){set(b.dataset.v)}});set(cur)})();</script>')
out=(s.replace('/*__FONTS__*/',fonts).replace('__BANK__',js).replace('__IMG__',json.dumps(img)).replace('/*__CHRONO_CSS__*/',ccss)
      .replace('__CHRONO__',json.dumps(chtml,ensure_ascii=False).replace('</','<\\/')).replace('__COURSE__',esc(C)).replace('/*__COURSE_CSS__*/',ccol))
if inline:
    path=f'{out_dir}/{course_id}{"-variants" if V else ""}.html'; out+=vbar
else:
    # hosted page needs the document skeleton the preview adds for us
    title=re.search(r'<title>.*?</title>',out); out=out.replace(title.group(0),'') if title else out
    out=('<!doctype html><html lang="en-AU"><head><meta charset="utf-8">'+(title.group(0) if title else '<title>Agorian</title>')+'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
         f'<meta name="description" content="{C["description"]}"><link rel="icon" href="{"../" if "/" in C["out"] else ""}favicon.svg" type="image/svg+xml"><meta property="og:type" content="website"><meta property="og:site_name" content="Agorian"><meta property="og:title" content="Agorian. Challenge what you know."><meta property="og:description" content="{C["ogDescription"]}"><meta property="og:url" content="https://agorian.au/{"" if C["out"]=="docs" else C["out"].split("/",1)[1]+"/"}"><meta property="og:image" content="https://agorian.au/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#243A6B"><style>[hidden]{{display:none!important}}img{{max-width:100%}}</style></head><body>'+out+'</body></html>')
    path=f'{out_dir}/index.html'
open(path,'w',encoding='utf-8').write(out)
print('built', course_id, 'inline' if inline else 'hosted', path, len(out)//1024,'KB')
