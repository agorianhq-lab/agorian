import json,base64,io,os
from PIL import Image
D=json.load(open('sources.json'))
def du(name,w=900,q=70):
    im=Image.open('../img/%s.jpg'%name).convert('RGB'); im.thumbnail((w,w)); b=io.BytesIO(); im.save(b,'JPEG',quality=q,optimize=True)
    return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
for s in D['sources']:
    if s.get('img'): s['src']=du(s['img'])
js=json.dumps(D,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
CSS=r"""
:root{--bg:#F1EEE7;--surface:#FBFAF7;--ink:#1E2436;--muted:#636A7A;--line:#DAD5CB;--navy:#243A6B;--accent:#C7431F;--gold:#CF9A3A;--gold-ink:#9A6616;--sage:#4F7F6B;--teal:#2A7A86;--eu:#7A2E2B;--jp:#1F3A5F;--display:"Fraunces",Georgia,serif;--body:"Atkinson Hyperlegible",system-ui,sans-serif}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#151A26;--surface:#1E2434;--ink:#EDEAE3;--muted:#A4A9B6;--line:#343B4E;--navy:#4A5F9E;--accent:#E8694A;--gold:#E2B45C;--gold-ink:#E2B45C;--sage:#6FA58D;--teal:#5FB3BF;--eu:#C9736C;--jp:#7FA0D1}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);line-height:1.45}
.wrap{max-width:1100px;margin:0 auto;padding:24px 16px 60px}
h1{font-family:var(--display);font-size:30px;color:var(--navy);margin:0 0 4px}h1 em{color:var(--teal);font-style:italic}
.sub{color:var(--muted);max-width:72ch;margin:0 0 16px}
.tipbox{background:var(--surface);border:2px solid var(--navy);border-left:8px solid var(--gold);border-radius:10px;padding:10px 14px;font-size:14px;margin:0 0 18px}
.tipbox ol{margin:6px 0 0;padding-left:20px}.tipbox li{margin:2px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.st{background:var(--surface);border:2px solid var(--navy);border-radius:12px;padding:0;overflow:hidden;text-align:left;cursor:pointer;font:inherit;color:var(--ink);display:flex;flex-direction:column;transition:transform .12s}
.st:hover{transform:translateY(-2px)}.st .th{height:120px;background:var(--line);display:grid;place-items:center;overflow:hidden}.st .th img{width:100%;height:100%;object-fit:cover}
.st .th.txt{font-family:var(--display);font-size:15px;font-style:italic;color:var(--muted);padding:12px;text-align:center;background:color-mix(in srgb,var(--navy) 8%,var(--bg))}
.st .body{padding:10px 12px}.st .eyebrow{font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:var(--muted)}
.st.eu .eyebrow{color:var(--eu)}.st.jp .eyebrow{color:var(--jp)}.st b{font-size:14px;display:block;margin-top:2px}.st .done{font-size:12px;color:var(--sage);font-weight:700;margin-top:4px;display:block}
.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.btn{font:inherit;font-weight:700;padding:9px 14px;border-radius:10px;border:2px solid var(--navy);background:var(--surface);color:var(--ink);cursor:pointer}
.btn.primary{background:var(--navy);color:#fff}.btn.quiet{border-color:var(--line);color:var(--muted)}.btn[disabled]{opacity:.5;cursor:default}
.src{background:var(--surface);border:2px solid var(--navy);border-radius:12px;padding:14px;margin-top:12px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px}
@media(max-width:800px){.src{grid-template-columns:1fr}}
.src img{width:100%;border-radius:8px;border:1px solid var(--line)}
.src blockquote{margin:0;font-family:var(--display);font-size:17px;line-height:1.5;padding:12px 16px;border-left:6px solid var(--gold);background:color-mix(in srgb,var(--gold) 10%,transparent);border-radius:0 8px 8px 0}
.cap{font-size:13.5px;color:var(--muted)}.cap b{color:var(--ink)}
.qq{background:var(--surface);border:2px solid var(--navy);border-radius:12px;padding:14px;margin-top:12px}
.qq h3{margin:0 0 8px;font-family:var(--display);font-size:16px}
.opts{display:grid;gap:6px}.opt{text-align:left;font:inherit;padding:9px 12px;border-radius:9px;border:2px solid var(--line);background:var(--bg);color:var(--ink);cursor:pointer}
.opt:hover{border-color:var(--navy)}.opt.ok{border-color:var(--sage);background:color-mix(in srgb,var(--sage) 14%,var(--bg))}.opt.no{border-color:var(--accent);background:color-mix(in srgb,var(--accent) 12%,var(--bg))}
.opt[disabled]{cursor:default}.x{display:none;margin-top:8px;font-size:13.5px;color:var(--muted);border-top:1px dashed var(--line);padding-top:8px}.x.show{display:block}
.wr{display:none;margin-top:16px}.wr.show{display:block}
.wr .q{font-family:var(--display);font-size:19px;margin:0 0 6px;color:var(--navy)}
.timer{font-family:var(--display);font-weight:700;font-size:22px;color:var(--navy);min-width:70px}.timer.low{color:var(--accent)}
textarea{width:100%;min-height:130px;font:inherit;font-size:15px;padding:10px;border:2px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);margin-top:8px}
.chk{display:grid;gap:4px;margin:8px 0 0;padding:0;list-style:none;font-size:13.5px;color:var(--muted)}.chk li::before{content:"\2610  ";}
.model{display:none;margin-top:12px;background:var(--surface);border:2px solid var(--sage);border-radius:12px;padding:12px 14px}.model.show{display:block}
.model h4{margin:0 0 6px;font-family:var(--display)}.model ol{margin:8px 0 0;padding-left:20px;font-size:13.5px;color:var(--muted)}
.self{margin-top:10px}.self select{font:inherit;padding:6px 8px;border-radius:8px;border:2px solid var(--line);background:var(--bg);color:var(--ink)}
.foot{font-size:12px;color:var(--muted);margin-top:24px}
"""
JS=r"""
const D=__DATA__;const app=document.getElementById('app');
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
let done={};try{done=JSON.parse(localStorage.getItem('srcdrill')||'{}')}catch(e){}
function save(){try{localStorage.setItem('srcdrill',JSON.stringify(done))}catch(e){}}
let tick=null;
function list(){
 clearInterval(tick);
 app.innerHTML=`<h1>Unseen <em>sources</em></h1><p class="sub">${D.intro}</p>
 <div class="tipbox"><b>The 3-mark checklist</b><ol>${D.checklist.map(c=>`<li>${c}</li>`).join('')}</ol></div>
 <div class="grid">${D.sources.map(s=>`<button class="st ${s.unit==='Medieval Europe'?'eu':'jp'}" data-id="${s.id}"><div class="th ${s.img?'':'txt'}">${s.img?`<img src="${s.src}" alt="">`:'&ldquo;'+esc(s.text.slice(0,70))+'&hellip;&rdquo;'}</div><div class="body"><span class="eyebrow">${s.unit} &middot; ${s.img?'visual':'written'}</span><b>${esc(s.caption.split(',')[0])}</b>${done[s.id]?`<span class="done">&#10003; ${done[s.id].mc}/4 quick &middot; self-mark ${done[s.id].self??'–'}/3</span>`:''}</div></button>`).join('')}</div>
 <p class="foot">Sources are public domain, from Wikimedia Commons. Written extracts are adapted and shortened, as they would be in an exam.</p>`;
 app.querySelectorAll('.st').forEach(b=>b.onclick=()=>one(D.sources.find(s=>s.id===b.dataset.id)));
 window.scrollTo(0,0);
}
function one(s){
 clearInterval(tick); let mc=0, answered=0;
 app.innerHTML=`<div class="row" style="justify-content:space-between"><button class="btn quiet" id="back">&larr; All sources</button><span style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:var(--muted)">${s.unit} &middot; ${s.img?'visual source':'written source'}</span></div>
 <div class="src">${s.img?`<div><img src="${s.src}" alt=""></div>`:`<blockquote>${esc(s.text)}</blockquote>`}<div><p class="cap"><b>Source.</b> ${esc(s.caption)}</p><p class="cap" style="margin-top:10px">Read the caption first. It tells you the type, who made it, where and when. Then answer the four quick questions, then write.</p></div></div>
 ${s.qs.map((q,i)=>`<div class="qq" data-i="${i}"><h3>${i+1}. ${esc(q.q)}</h3><div class="opts">${shuffle(q.o.map((o,k)=>({o,k}))).map(({o,k})=>`<button class="opt" data-k="${k}">${esc(o)}</button>`).join('')}</div><div class="x">${esc(q.x)}</div></div>`).join('')}
 <div class="wr" id="wr"><p class="q">${esc(s.write)} <span style="color:var(--muted);font-size:14px">(3 marks)</span></p>
  <div class="row"><button class="btn primary" id="start">Start writing (2 min 15 s)</button><span class="timer" id="td">2:15</span><span class="sub" style="margin:0;font-size:13px">45 seconds a mark, like the exam.</span></div>
  <ul class="chk">${D.checklist.map(c=>`<li>${c}</li>`).join('')}</ul>
  <textarea id="ta" placeholder="Start with the source: 'The source shows…' or 'The writer says…', then 'which suggests…'" disabled></textarea>
  <div class="row" style="margin-top:8px"><button class="btn" id="reveal" disabled>Reveal a full-marks answer</button></div>
  <div class="model" id="model"><h4>A 3-mark answer</h4><p style="margin:0">${esc(s.model)}</p><ol>${s.mark.map(m=>`<li>${esc(m)}</li>`).join('')}</ol>
   <div class="self"><label>Mark yourself honestly: <select id="self"><option value="">–</option><option>0</option><option>1</option><option>2</option><option>3</option></select> / 3</label></div></div>
  <div class="row" style="margin-top:16px"><button class="btn" id="next">Next source</button><button class="btn quiet" id="back2">All sources</button></div>
 </div>`;
 const $=q=>app.querySelector(q);
 $('#back').onclick=list;
 app.querySelectorAll('.qq').forEach(box=>{const i=+box.dataset.i; box.querySelectorAll('.opt').forEach(b=>b.onclick=()=>{
  const k=+b.dataset.k, ok=k===s.qs[i].a; if(ok) mc++; answered++;
  box.querySelectorAll('.opt').forEach(o=>{o.disabled=true; if(+o.dataset.k===s.qs[i].a) o.classList.add('ok')}); if(!ok) b.classList.add('no');
  box.querySelector('.x').classList.add('show');
  if(answered===s.qs.length){ $('#wr').classList.add('show'); $('#wr').scrollIntoView({behavior:'smooth',block:'start'}); }
 })});
 $('#start').onclick=()=>{ $('#start').disabled=true; $('#ta').disabled=false; $('#ta').focus(); $('#reveal').disabled=false; let t=135; const td=$('#td');
  tick=setInterval(()=>{t--; td.textContent=Math.floor(t/60)+':'+String(t%60).padStart(2,'0'); if(t<=20) td.classList.add('low'); if(t<=0){clearInterval(tick); $('#ta').disabled=true; td.textContent='Pens down'; }},1000) };
 $('#reveal').onclick=()=>{ clearInterval(tick); $('#ta').disabled=true; $('#model').classList.add('show'); $('#reveal').disabled=true; done[s.id]={mc,self:null,text:$('#ta').value}; save(); $('#model').scrollIntoView({behavior:'smooth',block:'center'}) };
 $('#self').onchange=e=>{ done[s.id]=Object.assign(done[s.id]||{mc},{self:e.target.value}); save() };
 $('#next').onclick=()=>{const i=D.sources.indexOf(s); one(D.sources[(i+1)%D.sources.length])}; $('#back2').onclick=list;
 window.scrollTo(0,0);
}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
list();
"""
html=f"""<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Unseen sources</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap" id="app"></div><script>{JS.replace('__DATA__',js)}</script></body></html>"""
open('sources.html','w').write(html); print('built sources.html',len(html)//1024,'KB')
