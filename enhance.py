p='src/index.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, ('not unique/found: '+a[:60])
    s=s.replace(a,b)

# ---------- CSS ----------
rep("footer{margin-top:40px;", r"""
/* daily banner */
.daily{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;background:var(--navy);color:var(--navy-ink);border-radius:var(--radius);padding:16px 20px;margin-top:6px}
.daily .t{font-family:var(--display);font-size:20px;font-weight:700}
.daily .n{font-size:13px;opacity:.85}
.daily .btn{background:var(--gold);border-color:var(--gold);color:#1C2333}
.daily .btn.done{background:transparent;color:var(--navy-ink);border-color:rgba(255,255,255,.4)}
.mode.timeline .k{background:var(--gold)}
/* mastery */
.badge{display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--line);flex:none}
.badge.bronze{background:#B5713C}.badge.silver{background:#9AA3B2}.badge.gold{background:var(--gold)}
/* timeline game */
.tl{display:grid;gap:8px}
.tl .ev{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:1px solid var(--line);border-radius:10px;padding:12px 14px;background:var(--bg);cursor:pointer;line-height:1.35}
.tl .ev:hover:not(:disabled){border-color:var(--navy)}
.tl .ev .yr{flex:none;min-width:58px;font-family:var(--display);font-weight:700;font-size:18px;color:var(--navy);font-variant-numeric:tabular-nums;text-align:right}
.tl .ev.placed{background:var(--ok-bg);border-color:var(--ok);order:-1;cursor:default}
.tl .ev.shake{animation:shake .3s}
@keyframes shake{25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
.tl .ev .u{margin-left:auto;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
.rail{display:flex;gap:6px;align-items:center;font-size:13px;color:var(--muted)}
.rail i{width:12px;height:12px;border-radius:50%;background:var(--line);display:inline-block}
.rail i.on{background:var(--ok)} .rail i.miss{background:var(--bad)}
/* term sprint */
.sprint .def{font-size:19px;font-weight:600;line-height:1.4}
.sprint .opts{grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}
.sprint .opt{justify-content:center;font-weight:600}
/* teacher */
table.tt{width:100%;border-collapse:collapse;font-size:14px}
.tt th,.tt td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
.tt th{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.tt td.n{font-variant-numeric:tabular-nums;white-space:nowrap;text-align:right}
.tt th.n{text-align:right}
.tt .lo{color:var(--bad);font-weight:700}
.tbl{overflow-x:auto}
canvas#fx{position:fixed;inset:0;pointer-events:none;z-index:50}
footer{margin-top:40px;""")

# ---------- state / helpers ----------
rep("let state = { mode:null };", r"""let state = { mode:null };
const today = () => new Date().toISOString().slice(0,10);
function mastery(t){ const s=topicStats(t); if(s.a<8) return null; const p=s.c/s.a; return p>=.95?'gold':p>=.8?'silver':p>=.6?'bronze':null }
const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
function confetti(){
  if(REDUCED) return;
  const c=document.createElement('canvas'); c.id='fx'; document.body.appendChild(c);
  const x=c.getContext('2d'); c.width=innerWidth; c.height=innerHeight;
  const cols=['#C8431F','#D9A441','#4F7F6B','#2B3A67'];
  const ps=Array.from({length:120},()=>({x:Math.random()*c.width,y:-20-Math.random()*c.height*.5,v:2+Math.random()*3,r:4+Math.random()*5,a:Math.random()*6,s:(Math.random()-.5)*.2,col:cols[Math.random()*4|0]}));
  let t=0; (function f(){ x.clearRect(0,0,c.width,c.height); ps.forEach(p=>{ p.y+=p.v; p.a+=p.s; x.save(); x.translate(p.x,p.y); x.rotate(p.a); x.fillStyle=p.col; x.fillRect(-p.r/2,-p.r/4,p.r,p.r/2); x.restore() }); if(++t<160) requestAnimationFrame(f); else c.remove() })();
}
// timeline events (years hidden until placed)
const EVENTS=[
 ['Medieval Europe',1066,'Battle of Hastings. William of Normandy defeats Harold'],
 ['Medieval Europe',1086,'Domesday Book records every landholding in England'],
 ['Medieval Europe',1095,'Pope Urban II calls the First Crusade at Clermont'],
 ['Medieval Europe',1099,'Crusaders capture Jerusalem'],
 ['Medieval Europe',1215,'King John seals Magna Carta'],
 ['Medieval Europe',1291,'Fall of Acre ends the Crusader states'],
 ['Medieval Europe',1347,'The Black Death reaches Europe'],
 ['Medieval Europe',1381,'Peasants’ Revolt in England'],
 ['Shogunate Japan',1185,'Genpei War ends with Minamoto victory'],
 ['Shogunate Japan',1192,'Minamoto Yoritomo becomes the first shogun'],
 ['Shogunate Japan',1274,'First Mongol invasion of Japan fails'],
 ['Shogunate Japan',1543,'Portuguese traders arrive in Japan with firearms'],
 ['Shogunate Japan',1600,'Battle of Sekigahara'],
 ['Shogunate Japan',1603,'Tokugawa Ieyasu is named shogun'],
 ['Shogunate Japan',1615,'Laws for the Military Houses control the daimyo'],
 ['Shogunate Japan',1639,'Sakoku edicts close Japan to most foreigners'],
 ['Shogunate Japan',1853,'Commodore Perry arrives at Edo Bay'],
 ['Shogunate Japan',1854,'Treaty of Kanagawa opens two ports'],
 ['Shogunate Japan',1868,'Meiji Restoration returns power to the emperor'],
 ['Shogunate Japan',1873,'Conscription law replaces samurai armies'],
 ['Shogunate Japan',1889,'Meiji Constitution is proclaimed'],
].map(([unit,year,text])=>({unit,year,text}));""")

# ---------- home: daily banner, timeline mode, badges, best ----------
rep("""    <div class="modes">
      <button class="mode practice" data-go="setup">""", """    <div class="daily">
      <div><p class="t">Today’s ten</p><p class="n">${dailyDone?'Done for today. Back tomorrow for the next set.':'Ten questions aimed at what you find hardest.'} ${dayStreak>1?`Day streak <b>${dayStreak}</b>.`:''}</p></div>
      <button class="btn ${dailyDone?'done':''}" data-go="daily">${dailyDone?'Do it again':'Start'}</button>
    </div>
    <div class="modes">
      <button class="mode practice" data-go="setup">""")
rep("""<span class="n">20 questions from both units against a 10 minute clock. Score at the end.</span></button>""",
    """<span class="n">20 questions from both units against a 10 minute clock.${best?` Personal best ${best}/20.`:''}</span></button>
      <button class="mode timeline" data-go="timeline"><span class="k"></span><span class="t">Timeline</span><span class="n">Six events, tap them in order. Dates appear as you place them.</span></button>""")
rep("""  const totalAuto = Q.filter(q=>AUTO.has(q.type)).length;""",
    """  const totalAuto = Q.filter(q=>AUTO.has(q.type)).length;
  const dailyDone = store.get('dailyDate','')===today(), dayStreak=store.get('dayStreak',0), best=store.get('best',0);""")
rep("""return `<button class="topic" data-topic="${esc(t)}"><span class="name">${esc(t)}</span>""",
    """const m=mastery(t); return `<button class="topic" data-topic="${esc(t)}"><span class="name" style="display:flex;align-items:center;gap:8px"><span class="badge ${m||''}" title="${m?m+' mastery':'Answer 8 or more to earn a badge'}"></span>${esc(t)}</span>""")
rep("""  app.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>({setup, challenge, terms, write})[b.dataset.go]());""",
    """  app.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>({setup, challenge, terms, write, daily, timeline})[b.dataset.go]());""")
rep("""    <p class="muted" style="font-size:14px">Accuracy from questions you've answered on this device. Tap a topic to practise it.</p>""",
    """    <p class="muted" style="font-size:14px">Accuracy from questions you've answered on this device. Tap a topic to practise it. Badges at 60, 80 and 95 per cent after eight or more answers.</p>""")

# ---------- daily ----------
rep("""function challenge(){""", """function daily(){
  const pool = shuffle(Q.filter(q=>AUTO.has(q.type) && q.unit!=='Skills and concepts')).sort((a,b)=>weight(a)-weight(b)).slice(0,10);
  state={mode:'daily'}; startQuiz({mode:'daily', topics:null, timed:false, count:10, list:shuffle(pool)});
}
function challenge(){""")
rep("""  const list = pool.slice(0, Math.min(opts.count||Infinity, pool.length));""",
    """  const list = opts.list || pool.slice(0, Math.min(opts.count||Infinity, pool.length));""")

# ---------- keyboard shortcuts ----------
rep("""  const tx=app.querySelector('input.text'); if(tx){ tx.focus(); tx.onkeydown=e=>{ if(e.key==='Enter') check() } }""",
    """  const tx=app.querySelector('input.text'); if(tx){ tx.focus(); tx.onkeydown=e=>{ if(e.key==='Enter') check() } }
  document.onkeydown=e=>{ if(!app.querySelector('.card')||e.target.matches('input,textarea,select')) return;
    const opts=app.querySelectorAll('.opt:not(:disabled)'); const k='abcdefgh'.indexOf(e.key.toLowerCase()); const n=parseInt(e.key)-1;
    if(opts.length && (k>=0&&k<opts.length)) opts[k].click(); else if(opts.length && n>=0 && n<opts.length) opts[n].click();
    else if(e.key==='Enter'){ const b=app.querySelector('#check'); if(b && !b.hidden) b.click() } };""")

# ---------- results: daily streak, best, confetti ----------
rep("""  const secs=Math.round((Date.now()-state.start)/1000), mins=secs<60?`${secs} sec`:`${Math.round(secs/60)} min`;""", """  const secs=Math.round((Date.now()-state.start)/1000), mins=secs<60?`${secs} sec`:`${Math.round(secs/60)} min`;
  if(state.mode==='daily' && n>=10){ const last=store.get('dailyDate',''); if(last!==today()){ const y=new Date(Date.now()-864e5).toISOString().slice(0,10); store.set('dayStreak', last===y?store.get('dayStreak',0)+1:1); store.set('dailyDate', today()) } }
  let newBest=false; if(state.mode==='challenge'){ const b=store.get('best',0); if(c>b){ store.set('best',c); newBest=true } }
  if(n && pct>=80) setTimeout(confetti,200);""")
rep("""<p class="muted">${n?verdict(pct):'No questions answered.'}</p></div></div>""",
    """<p class="muted">${n?verdict(pct):'No questions answered.'}${newBest?' <b style="color:var(--accent)">New personal best.</b>':''}</p></div></div>""")
rep("""<h2>${state.mode==='challenge'?'Challenge complete':'Practice complete'}</h2>""",
    """<h2>${({challenge:'Challenge complete',daily:'Today’s ten complete',practice:'Practice complete'})[state.mode]}</h2>""")
rep("""const summary=`Agorian ${state.mode==='challenge'?'Challenge':'Practice'} · ${date}""",
    """const summary=`Agorian ${({challenge:'Challenge',daily:'Daily ten',practice:'Practice'})[state.mode]} · ${date}""")
rep("""  app.querySelector('#again').onclick=()=> state.mode==='challenge'?challenge():startQuiz({mode:'practice',topics:state.topics,timed:false,count:n||15});""",
    """  app.querySelector('#again').onclick=()=> state.mode==='challenge'?challenge():state.mode==='daily'?daily():startQuiz({mode:'practice',topics:state.topics,timed:false,count:n||15});""")

# ---------- timeline + term sprint + teacher ----------
rep("""// ---------- paragraph practice ----------""", r"""// ---------- timeline game ----------
function timeline(){
  let round=0, total=0, misses=0;
  const play=()=>{
    const unit = round%3===2 ? null : (round%3===0?'Medieval Europe':'Shogunate Japan');
    const pick = shuffle(unit?EVENTS.filter(e=>e.unit===unit):EVENTS).slice(0,6);
    const order = pick.slice().sort((a,b)=>a.year-b.year); let next=0, miss=0;
    h(`<section class="section"><div class="row" style="justify-content:space-between"><h2>Timeline</h2><span class="pill">Round <b>${round+1}</b></span></div>
    <div class="card"><div><span class="eyebrow">${unit?esc(unit):'Both units'}</span><p class="qtext" style="margin-top:4px">Tap the events in order, earliest first.</p></div>
      <div class="rail" id="rail">${order.map(()=>'<i></i>').join('')}</div>
      <div class="tl" id="tl">${pick.map((e,k)=>`<button class="ev" data-k="${k}"><span class="yr">?</span><span>${esc(e.text)}</span>${unit?'':`<span class="u">${e.unit==='Medieval Europe'?'Europe':'Japan'}</span>`}</button>`).join('')}</div>
      <div id="fb"></div><div class="actions"><button class="btn quiet" id="home">Home</button><span></span></div></div></section>`);
    app.querySelector('#home').onclick=home;
    app.querySelectorAll('.ev').forEach(b=>b.onclick=()=>{
      const e=pick[+b.dataset.k];
      if(e===order[next]){ b.classList.add('placed'); b.disabled=true; b.querySelector('.yr').textContent=e.year; b.style.order=next-10; app.querySelectorAll('#rail i')[next].classList.add('on'); next++;
        if(next===order.length){ total+=6-miss; misses+=miss; log({event:'timeline', miss, unit}); app.querySelector('#fb').innerHTML=`<div class="feedback ${miss?'info':'ok'}"><b>${miss?`Done with ${miss} slip${miss>1?'s':''}.`:'Perfect order.'}</b><span>${esc(order[0].text)} came first. ${order[order.length-1].year-order[0].year} years separate the first and last events here.</span></div>`;
          app.querySelector('.actions span').innerHTML=`<button class="btn primary" id="nx">Next round</button>`; app.querySelector('#nx').onclick=()=>{round++;play()}; app.querySelector('#nx').focus(); if(!miss&&round>=2) confetti() } }
      else { miss++; b.classList.remove('shake'); void b.offsetWidth; b.classList.add('shake'); const r=app.querySelectorAll('#rail i')[next]; r.classList.add('miss'); setTimeout(()=>r.classList.remove('miss'),500) }
    });
  };
  play();
}

// ---------- term sprint ----------
function sprint(){
  const set=shuffle(TERMS).slice(0,10); let i=0, right=0, start=Date.now();
  const ask=()=>{
    if(i>=set.length){ const secs=Math.round((Date.now()-start)/1000); const b=store.get('sprintBest',null); const nb=right>(b?b.r:-1)||(b&&right===b.r&&secs<b.s); if(nb) store.set('sprintBest',{r:right,s:secs}); log({event:'sprint',right,secs});
      h(`<section class="section"><h2>Term sprint</h2><div class="card"><div class="score"><div class="ring" style="--p:${right*10}"><b>${right}/10</b></div><div><p style="font-size:18px;font-weight:600">${secs} seconds</p><p class="muted">${nb?'New best.':b?`Best ${b.r}/10 in ${b.s} s.`:''} ${right>=9?'You know your vocabulary.':'Flip through the cards for the ones you missed.'}</p></div></div>
      <div class="row"><button class="btn primary" id="again">Sprint again</button><button class="btn" id="cards">Flashcards</button><button class="btn quiet" id="home">Home</button></div></div></section>`);
      app.querySelector('#again').onclick=sprint; app.querySelector('#cards').onclick=terms; app.querySelector('#home').onclick=home; if(right>=9) confetti(); return }
    const t=set[i]; const opts=shuffle([t].concat(shuffle(TERMS.filter(x=>x!==t)).slice(0,3)));
    h(`<section class="section sprint"><div class="progress"><span>${i+1} / 10</span><span class="track"><i style="width:${i*10}%"></i></span><span class="timer">${Math.round((Date.now()-start)/1000)} s</span></div>
    <div class="card"><span class="eyebrow">Which term?</span><p class="def">${esc(t.definition)}</p>
    <div class="opts">${opts.map((o,k)=>`<button class="opt" data-k="${k}"><span class="l">${L[k]}</span><span>${esc(o.term)}</span></button>`).join('')}</div><div id="fb"></div></div></section>`);
    app.querySelectorAll('.opt').forEach(b=>b.onclick=()=>{ const o=opts[+b.dataset.k]; const ok=o===t; if(ok) right++; app.querySelectorAll('.opt').forEach(x=>{x.disabled=true; if(opts[+x.dataset.k]===t) x.classList.add('right'); else if(x===b) x.classList.add('wrong')}); i++; setTimeout(ask, ok?350:1100) });
    document.onkeydown=e=>{ const k='abcd'.indexOf(e.key.toLowerCase()); const n=parseInt(e.key)-1; const o=app.querySelectorAll('.opt:not(:disabled)'); if(o.length&&k>=0&&k<4) o[k].click(); else if(o.length&&n>=0&&n<4) o[n].click() };
  };
  ask();
}

// ---------- teacher view (local data now, class logging later) ----------
function teacher(){
  const rows=Q.filter(q=>AUTO.has(q.type)).map(q=>({q,s:stats[q.id]||{a:0,c:0}})).filter(r=>r.s.a).sort((a,b)=>(a.s.c/a.s.a)-(b.s.c/b.s.a));
  const byT=UNITS.flatMap(u=>topicsIn(u).map(t=>({t,s:topicStats(t)}))).filter(r=>r.s.a).sort((a,b)=>(a.s.c/a.s.a)-(b.s.c/b.s.a));
  const csv='id,unit,topic,type,question,attempts,correct,accuracy\n'+rows.map(r=>[r.q.id,r.q.unit,r.q.topic,r.q.type,JSON.stringify(r.q.question),r.s.a,r.s.c,Math.round(100*r.s.c/r.s.a)].join(',')).join('\n');
  h(`<section class="section"><h2>Teacher view</h2>
  <p class="muted">Question difficulty from answers recorded on <b>this device</b>. When class logging is connected, this page reads the whole class instead. Hardest first.</p>
  ${rows.length?`<div class="card"><div><p class="eyebrow" style="margin-bottom:8px">Topics</p><div class="bytopic">${byT.map(r=>`<div class="bt"><div><div style="margin-bottom:4px">${esc(r.t)}</div><div class="bar"><i style="width:${100*r.s.c/r.s.a}%;background:${r.s.c/r.s.a<.6?'var(--accent)':'var(--sage)'}"></i></div></div><span class="n">${Math.round(100*r.s.c/r.s.a)}% · ${r.s.a}</span></div>`).join('')}</div></div>
    <div><p class="eyebrow" style="margin-bottom:8px">Questions</p><div class="tbl"><table class="tt"><thead><tr><th>Question</th><th>Topic</th><th class="n">Tries</th><th class="n">Correct</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(r.q.question)}</td><td class="muted">${esc(r.q.topic)}</td><td class="n">${r.s.a}</td><td class="n ${r.s.c/r.s.a<.5?'lo':''}">${Math.round(100*r.s.c/r.s.a)}%</td></tr>`).join('')}</tbody></table></div></div>
    <div class="row"><button class="btn" id="csv">Copy as CSV</button><button class="btn quiet" id="home">Home</button></div></div>`:`<div class="card"><p>No answers recorded on this device yet.</p><div class="row"><button class="btn quiet" id="home">Home</button></div></div>`}
  </section>`);
  const c=app.querySelector('#csv'); if(c) c.onclick=async e=>{ try{ await navigator.clipboard.writeText(csv); e.target.textContent='Copied' }catch(err){ e.target.textContent='Copy blocked' } };
  app.querySelector('#home').onclick=home;
}

// ---------- paragraph practice ----------""")

# key terms: add sprint button
rep("""<button class="btn quiet" id="unk" ${known.size?'':'disabled'}>Only unknown</button><button class="btn quiet" id="home">Home</button></div></div>""",
    """<button class="btn quiet" id="unk" ${known.size?'':'disabled'}>Only unknown</button><button class="btn accent" id="sprint">Term sprint</button><button class="btn quiet" id="home">Home</button></div></div>""")
rep("""    app.querySelector('#home').onclick=home;
  };
  document.onkeydown=e=>{ if(!app.querySelector('#flash'))""", """    app.querySelector('#home').onclick=home; app.querySelector('#sprint').onclick=sprint;
  };
  document.onkeydown=e=>{ if(!app.querySelector('#flash'))""")
rep("""<span class="n">${TERMS.length} flashcards. Tap to flip, swipe through, mark what you know.</span>""",
    """<span class="n">${TERMS.length} flashcards to flip and mark, plus a ten-definition sprint.</span>""")

# ---------- hash routing ----------
rep("""document.getElementById('homeBtn').onclick=home;
document.getElementById('qcount').textContent=`${Q.length} questions · ${TERMS.length} terms`;
home();""", """document.getElementById('homeBtn').onclick=home;
document.getElementById('qcount').textContent=`${Q.length} questions · ${TERMS.length} terms`;
const ROUTES={practice:setup, challenge, terms, write, daily, timeline, teacher, sprint};
const r=(location.hash||'').slice(1); (ROUTES[r]||home)();""")

# modes grid: 3 columns on desktop now that there are 5 cards + ensure wrap
rep(".modes{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))", ".modes{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))")

open(p,'w').write(s); print('patched')
