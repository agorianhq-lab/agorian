import json
D=json.load(open('marker.json'))
js=json.dumps(D,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
CSS=r"""
:root{--bg:#F1EEE7;--surface:#FBFAF7;--ink:#1E2436;--muted:#636A7A;--line:#DAD5CB;--navy:#243A6B;--accent:#C7431F;--gold:#CF9A3A;--gold-ink:#9A6616;--sage:#4F7F6B;--plum:#6B3F7A;--eu:#7A2E2B;--jp:#1F3A5F;--display:"Fraunces",Georgia,serif;--body:"Atkinson Hyperlegible",system-ui,sans-serif}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#151A26;--surface:#1E2434;--ink:#EDEAE3;--muted:#A4A9B6;--line:#343B4E;--navy:#4A5F9E;--accent:#E8694A;--gold:#E2B45C;--gold-ink:#E2B45C;--sage:#6FA58D;--plum:#B58AC4;--eu:#C9736C;--jp:#7FA0D1}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);line-height:1.45}
.wrap{max-width:1100px;margin:0 auto;padding:24px 16px 60px}
h1{font-family:var(--display);font-size:30px;color:var(--navy);margin:0 0 4px}h1 em{color:var(--plum);font-style:italic}
.sub{color:var(--muted);max-width:70ch;margin:0 0 16px}
.tipbox{background:var(--surface);border:2px solid var(--navy);border-left:8px solid var(--gold);border-radius:10px;padding:10px 14px;font-size:14px;margin:0 0 18px}
.tipbox ol{margin:6px 0 0;padding-left:20px}.tipbox li{margin:2px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}
.qt{background:var(--surface);border:2px solid var(--navy);border-radius:12px;padding:14px;text-align:left;cursor:pointer;font:inherit;color:var(--ink);display:flex;flex-direction:column;gap:6px;transition:transform .12s}
.qt:hover{transform:translateY(-2px)}.qt .eyebrow{font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:var(--muted)}
.qt.eu{border-left:8px solid var(--eu)}.qt.jp{border-left:8px solid var(--jp)}.qt b{font-size:15.5px;font-family:var(--display)}
.qt .done{font-size:12px;color:var(--sage);font-weight:700}
.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.btn{font:inherit;font-weight:700;padding:9px 14px;border-radius:10px;border:2px solid var(--navy);background:var(--surface);color:var(--ink);cursor:pointer}
.btn.primary{background:var(--navy);color:#fff}.btn.quiet{border-color:var(--line);color:var(--muted)}.btn[disabled]{opacity:.5;cursor:default}
.q{font-family:var(--display);font-size:21px;margin:14px 0 4px;color:var(--navy)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:12px}@media(max-width:800px){.two{grid-template-columns:1fr}}
.ans{background:var(--surface);border:2px solid var(--navy);border-radius:12px;padding:14px;position:relative}
.ans h3{margin:0 0 8px;font-family:var(--display);font-size:17px;display:flex;justify-content:space-between;align-items:center}
.ans .mk{display:none;background:var(--gold);color:#1C2333;font-weight:800;border-radius:999px;padding:3px 10px;font-size:14px}
.ans p{margin:0;font-size:15px;white-space:pre-line}
.ans.chosen{outline:3px solid var(--gold);outline-offset:2px}
.ans .pick{margin-top:12px;width:100%}
mark{background:none;color:inherit;border-bottom:0}
.revealed mark{background:color-mix(in srgb,var(--gold) 28%,transparent);border-bottom:2px solid var(--gold-ink);cursor:help;padding:0 1px}
.revealed mark::after{content:attr(data-n);font-size:10px;font-weight:800;color:var(--gold-ink);vertical-align:super;margin-left:1px}
.revealed .ans .mk{display:inline-block}
.notes{display:none;margin:12px 0 0;padding:0;list-style:none;font-size:13px;color:var(--muted)}
.revealed .notes{display:block}.notes li{margin:5px 0;padding-left:24px;position:relative}.notes li b{position:absolute;left:0;top:0;width:18px;height:18px;border-radius:50%;background:var(--gold);color:#1C2333;font-size:11px;display:grid;place-items:center}
.why{display:none;margin-top:12px;padding:10px 12px;border-radius:10px;font-size:14px;border:2px dashed var(--line)}
.revealed .why{display:block}.why b{display:block;margin-bottom:3px}
.reason{margin-top:14px;background:var(--surface);border:2px solid var(--navy);border-radius:12px;padding:14px;display:none}
.reason.show{display:block}.reason label{display:block;font-weight:700;margin-bottom:6px}
textarea{width:100%;min-height:70px;font:inherit;font-size:15px;padding:10px;border:2px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink)}
.verdict{display:none;margin-top:14px;padding:12px 14px;border-radius:12px;border:2px solid var(--navy);background:var(--surface);font-size:15px}
.revealed .verdict{display:block}.verdict.ok{border-color:var(--sage)}.verdict.no{border-color:var(--accent)}.verdict b{font-family:var(--display);font-size:17px}
.check{display:none;margin-top:14px;background:var(--surface);border:2px solid var(--navy);border-radius:12px;padding:12px 14px;font-size:14px}
.revealed .check{display:block}.check ol{margin:6px 0 0;padding-left:20px}.check li{margin:3px 0}
.mine{font-style:italic;color:var(--muted);margin-top:8px;font-size:14px}
.foot{font-size:12px;color:var(--muted);margin-top:24px}
"""
JS=r"""
const D=__DATA__;const app=document.getElementById('app');
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
let done={};try{done=JSON.parse(localStorage.getItem('marker')||'{}')}catch(e){}
function save(){try{localStorage.setItem('marker',JSON.stringify(done))}catch(e){}}
function render(t){ let n=0; const notes=[]; const html=t.replace(/\[\[(.+?)\|\|(.+?)\]\]/g,(m,a,b)=>{n++;notes.push(b);return `<mark data-n="${n}" title="${esc(b).replace(/"/g,'&quot;')}">${esc(a)}</mark>`}); return {html, notes}; }
function list(){
 app.innerHTML=`<h1>Be the <em>marker</em></h1><p class="sub">${D.intro}</p>
 <div class="tipbox"><b>What a marker looks for in a Section C answer</b><ol>${D.checklist.map(c=>`<li>${c}</li>`).join('')}</ol></div>
 <div class="grid">${D.pairs.map(p=>`<button class="qt ${p.unit==='Medieval Europe'?'eu':'jp'}" data-id="${p.id}"><span class="eyebrow">${p.unit}</span><b>${esc(p.q)}</b>${done[p.id]?`<span class="done">&#10003; Marked${done[p.id].right?' correctly':''}</span>`:'<span class="eyebrow" style="color:var(--gold-ink)">8 marks &middot; two answers</span>'}</button>`).join('')}</div>
 <p class="foot">Answers are written for this activity. Neither is a real student's work. Marks follow the Section C criteria: structure, historical concepts, knowledge, evidence, expression.</p>`;
 app.querySelectorAll('.qt').forEach(b=>b.onclick=()=>pair(D.pairs.find(p=>p.id===b.dataset.id)));
 window.scrollTo(0,0);
}
function pair(p){
 const flip=Math.random()<.5; const A=flip?p.strong:p.weak, B=flip?p.weak:p.strong; const strongIs=flip?'A':'B';
 const ra=render(A.text), rb=render(B.text); let picked=null;
 app.innerHTML=`<div class="row" style="justify-content:space-between"><button class="btn quiet" id="back">&larr; All questions</button><span class="eyebrow" style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:var(--muted)">${p.unit} &middot; Section C &middot; 8 marks</span></div>
 <p class="q">${esc(p.q)}</p><p class="sub">Read both. One scored 4, the other 7. Pick the stronger one, then say why before the marks appear.</p>
 <div class="two" id="two">
  ${[['A',A,ra],['B',B,rb]].map(([k,x,r])=>`<div class="ans" data-k="${k}"><h3>Answer ${k} <span class="mk">${x.marks} / 8</span></h3><p>${r.html}</p><ol class="notes">${r.notes.map((n,i)=>`<li><b>${i+1}</b>${esc(n)}</li>`).join('')}</ol><div class="why"><b>Why ${x.marks}, not ${x.marks+1}</b>${esc(x.why)}</div><button class="btn pick" data-k="${k}">Answer ${k} is stronger</button></div>`).join('')}
 </div>
 <div class="reason" id="reason"><label for="rt">Why? Name one thing the answer you chose does that the other does not.</label><textarea id="rt" placeholder="For example: it says which impact mattered most in the first sentence."></textarea><div class="row" style="margin-top:10px"><button class="btn primary" id="reveal" disabled>Reveal the marks</button><span class="sub" style="margin:0;font-size:13px">A few words is enough.</span></div></div>
 <div class="verdict" id="verdict"></div>
 <div class="check"><b>Now check the 7 against the list. Can you find all five?</b><ol>${D.checklist.map(c=>`<li>${c}</li>`).join('')}</ol><p class="mine" id="mine"></p></div>
 <div class="row" style="margin-top:16px"><button class="btn" id="next" style="display:none">Next question</button><button class="btn quiet" id="back2" style="display:none">All questions</button></div>`;
 const $=s=>app.querySelector(s);
 $('#back').onclick=list;
 app.querySelectorAll('.pick').forEach(b=>b.onclick=()=>{picked=b.dataset.k; app.querySelectorAll('.ans').forEach(a=>a.classList.toggle('chosen',a.dataset.k===picked)); $('#reason').classList.add('show'); $('#reveal').disabled=false; $('#rt').focus()});
 $('#reveal').onclick=()=>{
  const right=picked===strongIs; const txt=$('#rt').value.trim();
  app.classList.add('revealed'); app.querySelectorAll('.pick').forEach(b=>b.disabled=true);
  const v=$('#verdict'); v.className='verdict '+(right?'ok':'no');
  v.innerHTML=right?`<b>Yes. Answer ${strongIs} scored 7.</b> Now look at the numbered notes: the gold phrases are where the marks were earned, and the dashed box under each answer says what separates 4 from 5 and 7 from 8.`
   :`<b>Answer ${strongIs} is the 7.</b> Answer ${picked} reads well and has plenty of correct knowledge, which is what usually draws people to it. But a marker reads for a contention, dated evidence with a because, who was affected, and a judgement. Look at the numbered notes on both answers to see where the marks were earned and lost.`;
  $('#mine').textContent=txt?`Your reason: "${txt}"`:'';
  done[p.id]={right,reason:txt}; save();
  $('#next').style.display=''; $('#back2').style.display='';
  $('#next').onclick=()=>{const i=D.pairs.indexOf(p); app.classList.remove('revealed'); pair(D.pairs[(i+1)%D.pairs.length])}; $('#back2').onclick=()=>{app.classList.remove('revealed'); list()};
  $('#verdict').scrollIntoView({behavior:'smooth',block:'center'});
 };
 window.scrollTo(0,0);
}
list();
"""
html=f"""<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Be the marker</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap" id="app"></div><script>{JS.replace('__DATA__',js)}</script></body></html>"""
open('marker.html','w').write(html); print('built marker.html',len(html)//1024,'KB')
