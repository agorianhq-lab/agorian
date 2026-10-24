p='src/index.html'; s=open(p).read()
def rep(a,b,count=1):
    global s
    assert s.count(a)==count, (s.count(a), a[:70]); s=s.replace(a,b)

# ---------- CSS ----------
rep("""/* daily banner */""","""/* welcome card */
.welcome{background:var(--surface);border:1px solid var(--line);border-left:6px solid var(--accent);border-radius:var(--radius);padding:22px 24px;display:grid;gap:14px;box-shadow:var(--shadow);margin-top:6px}
.welcome h2{font-size:26px;color:var(--navy)}
.welcome ol{margin:0;padding-left:22px;display:grid;gap:6px;font-size:17px}
.welcome .namerow{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.welcome input.text{max-width:320px}
.who{font-size:14px;color:var(--muted)} .who b{color:var(--ink)} .who button{border:0;background:none;color:var(--navy);font-weight:700;cursor:pointer;padding:0 4px;font-size:14px;text-decoration:underline}
/* confidence + hint */
.conf{display:flex;gap:8px;align-items:center;flex-wrap:wrap;font-size:14px;color:var(--muted)}
.conf button{border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:6px 14px;font-weight:700;cursor:pointer;color:var(--muted)}
.conf button.on{background:var(--navy);color:var(--navy-ink);border-color:var(--navy)}
.conf .hintbtn{margin-left:auto;color:var(--gold-ink);border-color:color-mix(in srgb,var(--gold) 50%,var(--line))}
.conf .hintbtn:disabled{opacity:.45;cursor:default}
.opt.gone{opacity:.35;text-decoration:line-through;pointer-events:none}
.tag{display:inline-block;font-size:11px;letter-spacing:.06em;text-transform:uppercase;font-weight:700;border-radius:999px;padding:2px 8px;margin-left:6px;vertical-align:middle}
.tag.sure{background:var(--bad-bg);color:var(--bad)} .tag.lucky{background:color-mix(in srgb,var(--gold) 25%,var(--surface));color:var(--gold-ink)}
.due{font-size:12px;color:var(--muted);margin-left:8px}
/* sound toggle */
.soundbtn{border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:6px 12px;font-size:13px;font-weight:700;cursor:pointer;color:var(--muted);display:inline-flex;align-items:center;gap:6px}
.soundbtn.on{color:var(--navy);border-color:var(--navy)}
/* daily banner */""")

# ---------- state: name, sound, confidence, spacing ----------
rep("""let streak = store.get('streak', 0);""","""let streak = store.get('streak', 0);
let studentName = store.get('name', '');
let soundOn = store.get('sound', true);
// ---- sound (synthesised, no files) ----
let actx=null;
function beep(kind){ if(!soundOn) return; try{ actx=actx||new (window.AudioContext||window.webkitAudioContext)(); if(actx.state==='suspended') actx.resume(); const t=actx.currentTime; const tone=(f,start,dur,type='sine',g=.12)=>{ const o=actx.createOscillator(), v=actx.createGain(); o.type=type; o.frequency.setValueAtTime(f,t+start); v.gain.setValueAtTime(0,t+start); v.gain.linearRampToValueAtTime(g,t+start+.01); v.gain.exponentialRampToValueAtTime(.0001,t+start+dur); o.connect(v).connect(actx.destination); o.start(t+start); o.stop(t+start+dur+.02) };
  if(kind==='ok'){ tone(660,0,.12); tone(990,.1,.18) } else if(kind==='bad'){ tone(220,0,.22,'triangle',.1) } else if(kind==='tick'){ tone(880,0,.05,'square',.04) } else if(kind==='win'){ [523,659,784,1047].forEach((f,i)=>tone(f,i*.09,.25)) } }catch(e){} }
function setSound(on){ soundOn=on; store.set('sound',on); document.querySelectorAll('.soundbtn').forEach(b=>{ b.classList.toggle('on',on); b.innerHTML=(on?'&#9835; Sound on':'&#9835; Sound off') }) }
// ---- spaced return: when a question is next due ----
function schedule(q, correct, conf){ const s=stats[q.id]||{a:0,c:0}; const days = !correct ? 1 : conf==='sure' ? 7 : 3; s.due = Date.now()+days*864e5; if(conf) s.conf=conf; stats[q.id]=s; store.set('stats',stats) }
const isDue = q => { const s=stats[q.id]; return !s || !s.due || s.due<=Date.now() };""")
rep("""function weight(q){ const s=stats[q.id]; if(!s) return 0; return s.c/s.a + s.a*0.05 }""",
"""function weight(q){ const s=stats[q.id]; if(!s) return 0.5; const overdue = s.due && s.due<=Date.now() ? 0 : 1; return overdue + s.c/s.a + s.a*0.05 }""")
rep("""function record(q, correct){
  const s = stats[q.id] || {a:0,c:0}; s.a++; if(correct) s.c++; stats[q.id]=s; store.set('stats', stats);
  log({qid:q.id, topic:q.topic, unit:q.unit, type:q.type, correct:correct?1:0, mode:state.mode});
}""","""function record(q, correct, conf, hint){
  const s = stats[q.id] || {a:0,c:0}; s.a++; if(correct) s.c++; stats[q.id]=s; store.set('stats', stats);
  schedule(q, correct, conf);
  log({qid:q.id, topic:q.topic, unit:q.unit, type:q.type, correct:correct?1:0, mode:state.mode, conf:conf||'', hint:hint?1:0, name:studentName});
}""")
rep("""  try{ fetch(LOG_ENDPOINT,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain'},body:JSON.stringify(Object.assign({sid:sessionId,t:Date.now()},ev)),keepalive:true}) }catch(e){}""",
"""  try{ fetch(LOG_ENDPOINT,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain'},body:JSON.stringify(Object.assign({sid:sessionId,t:Date.now(),name:studentName},ev)),keepalive:true}) }catch(e){}""")

# ---------- home: welcome card on first visit, who line, sound toggle ----------
rep("""  <section class="hero">
    <h1><em>Challenge</em> what you know.</h1>""","""  <section class="hero">
    ${store.get('welcomed',false)?'':`<div class="welcome" id="welcome"><h2>Welcome to Agorian</h2>
      <ol><li>Start with <b>Today’s ten</b>. It aims at what you find hardest.</li><li><b>Practice</b> lets you pick topics. Every answer comes with an explanation.</li><li>Your name and answers are recorded so your teacher can see how the class is going. Nothing else is collected.</li></ol>
      <div class="namerow"><label for="nameIn" class="hint">Your name</label><input class="text" id="nameIn" placeholder="First name and initial" autocomplete="off" value="${esc(studentName)}"><button class="btn primary" id="goWelcome">Let’s go</button><button class="soundbtn ${soundOn?'on':''}" id="snd0">${soundOn?'&#9835; Sound on':'&#9835; Sound off'}</button></div></div>`}
    <h1><em>Challenge</em> what you know.</h1>""")
rep("""  app.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>({setup, challenge, terms, write, daily, timeline, facts})[b.dataset.go]());""",
"""  app.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>({setup, challenge, terms, write, daily, timeline, facts})[b.dataset.go]());
  const gw=app.querySelector('#goWelcome'); if(gw){ const inp=app.querySelector('#nameIn'); const finishW=()=>{ studentName=inp.value.trim().slice(0,40); store.set('name',studentName); store.set('welcomed',true); log({event:'welcome'}); home() }; gw.onclick=finishW; inp.onkeydown=e=>{ if(e.key==='Enter') finishW() }; app.querySelector('#snd0').onclick=()=>setSound(!soundOn) }
  const who=document.getElementById('who'); if(who){ who.innerHTML = studentName ? `Revising as <b>${esc(studentName)}</b> <button id="chgName">change</button>` : `<button id="chgName">Add your name</button>`; who.querySelector('#chgName').onclick=()=>{ store.set('welcomed',false); home() } }""")
rep("""  <button class="brand" id="homeBtn" aria-label="Agorian home">""","""  <p class="who" id="who"></p>
  <button class="brand" id="homeBtn" aria-label="Agorian home">""")
rep("""  <div class="hdr-right"><div class="clock" id="clock" aria-live="off"></div><span class="pill" id="streak" hidden>Streak <b id="streakN">0</b></span></div>""",
"""  <div class="hdr-right"><div class="clock" id="clock" aria-live="off"></div><div class="row"><button class="soundbtn ${''}" id="sndBtn"></button><span class="pill" id="streak" hidden>Streak <b id="streakN">0</b></span></div></div>""")
rep(""".who{font-size:14px;color:var(--muted)}""",""".who{font-size:14px;color:var(--muted);order:3;margin-top:2px}""")
rep("""document.getElementById('homeBtn').onclick=home;""","""document.getElementById('homeBtn').onclick=home;
document.getElementById('sndBtn').onclick=()=>setSound(!soundOn); setSound(soundOn);""")

# ---------- quiz: confidence, hint, sounds ----------
rep("""      ${q.type==='ms'?`<p class="hint">Select all that apply, then check.</p>`:''}`;""",
"""      ${q.type==='ms'?`<p class="hint">Select all that apply, then check.</p>`:''}
      <div class="conf"><span>How sure are you?</span><button data-c="sure">Sure</button><button data-c="unsure">Not sure</button>${q.options.length>=3?`<button class="hintbtn" id="hintBtn">Remove one wrong answer</button>`:''}</div>`;""")
rep("""  const selected=new Set();""","""  const selected=new Set(); let conf=null, usedHint=false;
  app.querySelectorAll('.conf [data-c]').forEach(b=>b.onclick=()=>{ conf=b.dataset.c; app.querySelectorAll('.conf [data-c]').forEach(x=>x.classList.toggle('on',x===b)); beep('tick') });
  const hb=app.querySelector('#hintBtn'); if(hb) hb.onclick=()=>{ const wrong=[...app.querySelectorAll('.opt:not(.gone):not(:disabled)')].filter(x=>!q.answer.includes(+x.dataset.k)&&!selected.has(+x.dataset.k)); if(!wrong.length) return; const pick=wrong[Math.random()*wrong.length|0]; pick.classList.add('gone'); usedHint=true; hb.disabled=true; beep('tick') };""")
rep("""  function finish(correct){
    record(q, correct);
    state.answers.push({q, correct});""","""  function finish(correct){
    record(q, correct, conf, usedHint);
    state.answers.push({q, correct, conf, hint:usedHint});
    beep(correct?'ok':'bad');""")
# results: misconceptions and lucky guesses
rep("""    ${A.some(a=>!a.correct)?`<div><p class="eyebrow" style="margin-bottom:8px">Questions to revisit</p><div class="review">${A.filter(a=>!a.correct).map(a=>`<div class="rv"><span class="q">${esc(a.q.question)}</span><span class="muted">${esc(a.q.explanation||a.q.model||'')}</span></div>`).join('')}</div></div>`:''}""",
"""    ${A.some(a=>!a.correct)?`<div><p class="eyebrow" style="margin-bottom:8px">Questions to revisit</p><div class="review">${A.filter(a=>!a.correct).map(a=>`<div class="rv"><span class="q">${esc(a.q.question)}${a.conf==='sure'?'<span class="tag sure">Sure but wrong</span>':''}</span><span class="muted">${esc(a.q.explanation||a.q.model||'')}</span></div>`).join('')}</div></div>`:''}
    ${A.some(a=>a.correct&&a.conf==='unsure')?`<p class="hint">${A.filter(a=>a.correct&&a.conf==='unsure').length} right but not sure. Those come back in three days. Sure and right come back in a week, wrong ones tomorrow.</p>`:''}
    ${A.some(a=>a.hint)?`<p class="hint">Hints used on ${A.filter(a=>a.hint).length}.</p>`:''}""")
rep("""  if(n && pct>=80) setTimeout(confetti,200);""","""  if(n && pct>=80) setTimeout(confetti,200);
  if(n && pct>=80) setTimeout(()=>beep('win'),150);""")
# daily: due questions first
rep("""  const pool = shuffle(Q.filter(q=>AUTO.has(q.type) && q.unit!=='Skills and concepts')).sort((a,b)=>weight(a)-weight(b)).slice(0,10);""",
"""  const all=Q.filter(q=>AUTO.has(q.type) && q.unit!=='Skills and concepts'); const due=shuffle(all.filter(isDue)); const rest=shuffle(all.filter(q=>!isDue(q))).sort((a,b)=>weight(a)-weight(b)); const pool=due.concat(rest).slice(0,10);""")
rep("""      <div><p class="t">Today’s ten</p><p class="n">${dailyDone?'Done for today. Back tomorrow for the next set.':'Ten questions aimed at what you find hardest.'} ${dayStreak>1?`Day streak <b>${dayStreak}</b>.`:''}</p></div>""",
"""      <div><p class="t">Today’s ten</p><p class="n">${dailyDone?'Done for today. Back tomorrow for the next set.':`Ten questions aimed at what you find hardest.${(()=>{const d=Q.filter(q=>AUTO.has(q.type)&&stats[q.id]&&stats[q.id].due&&stats[q.id].due<=Date.now()).length; return d?` ${d} due for a return visit.`:''})()}`} ${dayStreak>1?`Day streak <b>${dayStreak}</b>.`:''}</p></div>""")

# ---------- privacy line in footer ----------
rep("""<footer><details class="credits"><summary>Image credits</summary>""","""<footer><p class="hint" style="margin-bottom:8px">What is recorded. Your name as you typed it, which questions you answered and whether you were right, so your teacher can see how the class is going. No email, no login, nothing else.</p><details class="credits"><summary>Image credits</summary>""")
open(p,'w').write(s); print('patched')
