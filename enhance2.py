p='src/index.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, ('not unique/found: '+a[:70])
    s=s.replace(a,b)

# ---------- palette refresh: indigo ink, vermilion, gold; warm stone ground with washi grain ----------
rep("""  --bg:#EEF1F6; --surface:#FFFFFF; --ink:#1C2333; --muted:#5E6675; --line:#D5DAE3;
  --navy:#2B3A67; --navy-ink:#FFFFFF; --accent:#C8431F; --gold:#D9A441; --sage:#4F7F6B; --blush:#F4E6DF;""",
"""  --bg:#F1EEE7; --surface:#FBFAF7; --ink:#1E2436; --muted:#636A7A; --line:#DAD5CB;
  --navy:#243A6B; --navy-ink:#FFFFFF; --accent:#C7431F; --gold:#CF9A3A; --sage:#4F7F6B; --blush:#F3E7DC;
  --eu:#7A2E2B; --eu-soft:#F0E3DE; --jp:#1F3A5F; --jp-soft:#E2E8F1; --sk:#4F7F6B; --sk-soft:#E4EEE8;""")
rep("""  --bg:#141925; --surface:#1D2434; --ink:#ECEFF5; --muted:#A3ABBA; --line:#323B4F;
  --navy:#3C4F8C; --navy-ink:#FFFFFF; --accent:#E8694A; --gold:#E2B45C; --sage:#6FA58D; --blush:#3A2F2B;
  --ok:#6FBF95; --ok-bg:#1E3A2E; --bad:#F08A72; --bad-bg:#45251F;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px -12px rgba(0,0,0,.5); color-scheme:dark}}""",
"""  --bg:#151A26; --surface:#1E2434; --ink:#EDEAE3; --muted:#A4A9B6; --line:#343B4E;
  --navy:#4A5F9E; --navy-ink:#FFFFFF; --accent:#E8694A; --gold:#E2B45C; --sage:#6FA58D; --blush:#3A2F2B;
  --eu:#C9736C; --eu-soft:#3A2826; --jp:#7FA0D1; --jp-soft:#232E44; --sk:#6FA58D; --sk-soft:#1F3029;
  --ok:#6FBF95; --ok-bg:#1E3A2E; --bad:#F08A72; --bad-bg:#45251F;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px -12px rgba(0,0,0,.5); color-scheme:dark}}""")
rep(""":root[data-theme="dark"]{
  --bg:#141925; --surface:#1D2434; --ink:#ECEFF5; --muted:#A3ABBA; --line:#323B4F;
  --navy:#3C4F8C; --navy-ink:#FFFFFF; --accent:#E8694A; --gold:#E2B45C; --sage:#6FA58D; --blush:#3A2F2B;""",
""":root[data-theme="dark"]{
  --bg:#151A26; --surface:#1E2434; --ink:#EDEAE3; --muted:#A4A9B6; --line:#343B4E;
  --navy:#4A5F9E; --navy-ink:#FFFFFF; --accent:#E8694A; --gold:#E2B45C; --sage:#6FA58D; --blush:#3A2F2B;
  --eu:#C9736C; --eu-soft:#3A2826; --jp:#7FA0D1; --jp-soft:#232E44; --sk:#6FA58D; --sk-soft:#1F3029;""")
# washi grain + soft glow behind the page
rep("""body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 var(--body);""",
"""body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 var(--body);
  background-image:radial-gradient(900px 420px at 15% -10%,color-mix(in srgb,var(--accent) 9%,transparent),transparent 70%),radial-gradient(700px 380px at 95% 0%,color-mix(in srgb,var(--navy) 12%,transparent),transparent 70%),url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .5 0 0 0 0 .45 0 0 0 0 .4 0 0 0 .07 0'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E");
  background-attachment:fixed,fixed,scroll;""")

# ---------- unit theming + illustrations ----------
rep("""/* daily banner */""", """/* unit panels with illustrations */
.units{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-top:18px}
.upanel{position:relative;overflow:hidden;text-align:left;border:1px solid var(--line);border-radius:var(--radius);padding:18px 18px 16px;cursor:pointer;display:grid;gap:6px;min-height:150px;box-shadow:var(--shadow);background:var(--surface)}
.upanel.eu{background:linear-gradient(135deg,var(--eu-soft),var(--surface) 70%)} .upanel.jp{background:linear-gradient(135deg,var(--jp-soft),var(--surface) 70%)}
.upanel:hover{border-color:var(--navy)}
.upanel .t{font-family:var(--display);font-size:24px;font-weight:700;position:relative}
.upanel.eu .t{color:var(--eu)} .upanel.jp .t{color:var(--jp)}
.upanel .n{font-size:13px;color:var(--muted);max-width:30ch;position:relative}
.upanel .art{position:absolute;right:-6px;bottom:-8px;width:46%;max-width:190px;height:auto;opacity:.95;pointer-events:none}
.upanel .cta{position:relative;font-size:13px;font-weight:600;margin-top:auto}
.upanel.eu .cta{color:var(--eu)} .upanel.jp .cta{color:var(--jp)}
/* unit band on quiz card */
.card.eu{border-top:4px solid var(--eu)} .card.jp{border-top:4px solid var(--jp)} .card.sk{border-top:4px solid var(--sk)}
.qhead .eyebrow{display:flex;align-items:center;gap:8px}
.qhead svg{width:18px;height:18px;flex:none}
/* fact */
.fact{display:grid;grid-template-columns:auto 1fr;gap:12px;align-items:start;border:1px dashed var(--line);border-radius:10px;padding:12px 14px;background:color-mix(in srgb,var(--gold) 12%,var(--surface));font-size:14px}
.fact .lamp{width:28px;height:28px;border-radius:50%;background:var(--gold);display:grid;place-items:center;color:#1E2436;font-family:var(--display);font-weight:700;font-size:16px}
.fact b{display:block;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:2px}
.fact.home{margin-top:18px}
/* daily banner */""")

# SVG symbol sheet after header
rep("""<main id="app"></main>""", """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="art-jp" viewBox="0 0 200 150">
    <circle cx="140" cy="48" r="26" fill="var(--accent)" opacity=".9"/>
    <path d="M0 150 L70 62 L100 92 L120 70 L200 150 Z" fill="var(--jp)" opacity=".85"/>
    <path d="M58 76 L70 62 L82 76 Q70 70 58 76 Z" fill="#fff" opacity=".9"/>
    <path d="M112 78 L120 70 L128 78 Q120 74 112 78 Z" fill="#fff" opacity=".9"/>
    <g fill="var(--accent)"><rect x="24" y="78" width="7" height="72"/><rect x="69" y="78" width="7" height="72"/><rect x="14" y="70" width="72" height="7" rx="1"/><rect x="20" y="88" width="60" height="5"/><path d="M8 66 Q50 58 92 66 L90 72 Q50 64 10 72 Z"/></g>
  </symbol>
  <symbol id="art-eu" viewBox="0 0 200 150">
    <circle cx="44" cy="40" r="20" fill="var(--gold)" opacity=".85"/>
    <path d="M0 150 L0 118 L30 110 L60 122 L100 112 L140 124 L200 112 L200 150 Z" fill="var(--sage)" opacity=".55"/>
    <g fill="var(--eu)"><rect x="78" y="70" width="60" height="80"/><rect x="66" y="56" width="18" height="94"/><rect x="132" y="56" width="18" height="94"/>
      <path d="M66 56 h18 v-10 h-6 v6 h-6 v-6 h-6z M132 56 h18 v-10 h-6 v6 h-6 v-6 h-6z M84 70 h54 v-9 h-6 v5 h-6 v-5 h-6 v5 h-6 v-5 h-6 v5 h-6 v-5 h-6 v5 h-6z"/>
      <rect x="100" y="34" width="16" height="36"/><path d="M100 34 h16 v-8 h-5 v4 h-6 v-4 h-5z"/></g>
    <path d="M116 26 l14 -6 l-14 -6 z" fill="var(--accent)"/>
    <g fill="#fff" opacity=".9"><rect x="72" y="66" width="6" height="12"/><rect x="138" y="66" width="6" height="12"/><path d="M101 118 a7 7 0 0 1 14 0 v32 h-14z"/><rect x="92" y="84" width="6" height="12"/><rect x="118" y="84" width="6" height="12"/></g>
  </symbol>
  <symbol id="ic-jp" viewBox="0 0 24 24"><g fill="currentColor"><rect x="5" y="8" width="2.4" height="13"/><rect x="16.6" y="8" width="2.4" height="13"/><rect x="3.5" y="6" width="17" height="2.2" rx=".5"/><rect x="6" y="11" width="12" height="1.8"/><path d="M2 4.5 Q12 2.5 22 4.5 L21.5 6.5 Q12 4.8 2.5 6.5 Z"/></g></symbol>
  <symbol id="ic-eu" viewBox="0 0 24 24"><g fill="currentColor"><path d="M3 21 V8 h3 V6 h2 v2 h2 V6 h2 v2 h2 V6 h2 v2 h2 V6 h2 v2 h1 v13 z M10 21 v-5 a2 2 0 0 1 4 0 v5 z" fill-rule="evenodd"/></g></symbol>
  <symbol id="ic-sk" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="6"/><path d="M15.5 15.5 L21 21"/><path d="M8.5 11 h5 M11 8.5 v5"/></g></symbol>
</svg>
<main id="app"></main>""")

# ---------- facts ----------
rep("""// timeline events (years hidden until placed)""", """// did-you-know facts, keyed loosely to topics
const FACTS=[
 ['Feudalism and hierarchy','The Domesday Book of 1086 recorded over 13,000 places in England. People called it Domesday because its judgements were as final as the Day of Judgement.'],
 ['Castles and knights','A full suit of plate armour weighed about 20 to 25 kilograms, spread over the whole body. A trained knight could run, climb and mount a horse without help.'],
 ['Castles and knights','William the Conqueror had hundreds of motte-and-bailey castles thrown up after 1066. A simple one could be built in a few weeks using forced local labour.'],
 ['Law and order','In 1215 the Church banned priests from taking part in trials by ordeal. Without God\\u2019s judgement, England leaned harder on juries instead.'],
 ['Catholic Church','The Church was the largest landowner in medieval Europe. In England it held roughly a quarter of all land, which made bishops as powerful as earls.'],
 ['The Crusades','Everyday English words arrived through contact with the Islamic world during the Crusades, including sugar, cotton, sofa and algebra.'],
 ['The Black Death','The word quarantine comes from the Venetian quaranta giorni, forty days, the time ships had to wait offshore before anyone could land.'],
 ['The Black Death','After the plague, wages for farm workers in England roughly doubled. The 1351 Statute of Labourers tried to freeze them at old levels and largely failed.'],
 ['Source analysis','The Bayeux Tapestry is not a tapestry at all. It is embroidery, nearly 70 metres long, and was probably stitched in England, not Normandy.'],
 ['Feudalism and samurai','The word samurai comes from saburau, meaning to serve. A samurai was defined by whom he served long before he was defined by his sword.'],
 ['Feudalism and samurai','The typhoon that wrecked the Mongol fleet in 1281 was later named kamikaze, the divine wind. The name was revived for pilots in 1944.'],
 ['Feudalism and samurai','The term bushido was rarely used before the Meiji period. Nitobe Inazo\\u2019s 1900 book, written in English for Western readers, made it famous.'],
 ['Tokugawa Shogunate','A daimyo\\u2019s sankin kotai procession could number thousands of people. The constant travel built the Tokaido road, its post towns and inns, and emptied daimyo treasuries.'],
 ['Tokugawa Shogunate','Dejima, where the Dutch were confined at Nagasaki, was an artificial fan-shaped island of about 1.5 hectares. For two centuries it was Japan\\u2019s only window on Europe.'],
 ['Tokugawa Shogunate','By about 1700 Edo had around a million people, making it probably the largest city in the world, bigger than London or Paris.'],
 ['Tokugawa Shogunate','In 1703 the 47 ronin avenged their lord and were then ordered to commit seppuku. Their story became Japan\\u2019s most retold tale of loyalty.'],
 ['Meiji Restoration','When Perry returned in 1854 his gifts included a working quarter-size steam railway and a telegraph line. Officials rode the train for fun.'],
 ['Meiji Restoration','Meiji means enlightened rule. The emperor who gave the era its name, Mutsuhito, was 15 years old when power was restored to him in 1868.'],
 ['Chronology','The two units overlap. The first shogun took power in 1192, about a century after Hastings, and the Black Death struck Europe while the Kamakura shogunate still ruled Japan.'],
 ['Comparing the two societies','Both knights and samurai served lords in return for land, but samurai were also expected to be literate officials. By 1700 most samurai had never fought a battle.'],
];
function factFor(topics){ const pool=FACTS.filter(f=>!topics||topics.includes(f[0])); const f=(pool.length?pool:FACTS)[Math.random()*(pool.length||FACTS.length)|0]; return `<div class="fact"><span class="lamp">?</span><div><b>Did you know</b>${esc(f[1])}</div></div>` }
const unitCls = u => u==='Medieval Europe'?'eu':u==='Shogunate Japan'?'jp':'sk';
// timeline events (years hidden until placed)""")

# home: unit panels + home fact
rep("""    <div class="modes">
      <button class="mode practice" data-go="setup">""", """    <div class="units">
      <button class="upanel eu" data-unit="Medieval Europe"><span class="t">Medieval Europe</span><span class="n">Feudalism, castles, the Church, the Crusades and the Black Death.</span><span class="cta">Practise this unit \\u2192</span><svg class="art"><use href="#art-eu"/></svg></button>
      <button class="upanel jp" data-unit="Shogunate Japan"><span class="t">Shogunate Japan</span><span class="n">Samurai, the Tokugawa, sakoku and the Meiji Restoration.</span><span class="cta">Practise this unit \\u2192</span><svg class="art"><use href="#art-jp"/></svg></button>
    </div>
    <div class="modes">
      <button class="mode practice" data-go="setup">""")
rep("""  app.querySelectorAll('[data-topic]').forEach(b=>b.onclick=()=>startQuiz({mode:'practice', topics:[b.dataset.topic], timed:false}));""",
"""  app.querySelectorAll('[data-topic]').forEach(b=>b.onclick=()=>startQuiz({mode:'practice', topics:[b.dataset.topic], timed:false}));
  app.querySelectorAll('[data-unit]').forEach(b=>b.onclick=()=>startQuiz({mode:'practice', topics:topicsIn(b.dataset.unit), timed:false, count:15}));""")
rep("""  <section class="section">
    <h2>Your progress by topic</h2>""", """  ${factFor(null).replace('class="fact"','class="fact home"')}
  <section class="section">
    <h2>Your progress by topic</h2>""")

# quiz card: unit class + icon; fact every 4th question
rep("""  <div class="card">
    <div class="qhead"><span class="eyebrow">${esc(q.unit)} · ${esc(q.topic)}</span>""",
"""  <div class="card ${unitCls(q.unit)}">
    <div class="qhead"><span class="eyebrow" style="color:var(--${unitCls(q.unit)})"><svg><use href="#ic-${unitCls(q.unit)}"/></svg>${esc(q.unit)} · ${esc(q.topic)}</span>""")
rep("""    app.querySelector('#fb').innerHTML=`<div class="feedback ${correct?'ok':'bad'}"><b>${correct?'Correct.':'Not quite.'}</b><span>${detail}${esc(q.explanation||'')}</span></div>`;""",
"""    app.querySelector('#fb').innerHTML=`<div class="feedback ${correct?'ok':'bad'}"><b>${correct?'Correct.':'Not quite.'}</b><span>${detail}${esc(q.explanation||'')}</span></div>`+(i%4===3?`<div style="margin-top:10px">${factFor([q.topic])}</div>`:'');""")
# results: a fact for a weak topic
rep("""    ${A.some(a=>!a.correct)?`<div><p class="eyebrow" style="margin-bottom:8px">Questions to revisit</p>""",
"""    ${factFor(weak.length?weak:Object.keys(byTopic))}
    ${A.some(a=>!a.correct)?`<div><p class="eyebrow" style="margin-bottom:8px">Questions to revisit</p>""")

# header wordmark: add small logo mark (concept A, the stoa monogram)
rep("""<button class="brand" id="homeBtn" aria-label="Agorian home"><span class="word">Agor<span>ian</span></span>""",
"""<button class="brand" id="homeBtn" aria-label="Agorian home"><svg class="mark" viewBox="0 0 40 40" width="30" height="30" aria-hidden="true"><path d="M20 3 L37 14 H3 Z" fill="var(--accent)"/><rect x="5" y="14" width="30" height="3" fill="var(--navy)"/><rect x="8" y="19" width="4" height="15" fill="var(--navy)"/><rect x="18" y="19" width="4" height="15" fill="var(--navy)"/><rect x="28" y="19" width="4" height="15" fill="var(--navy)"/><rect x="5" y="34" width="30" height="3" fill="var(--navy)"/></svg><span class="word">Agor<span>ian</span></span>""")
rep(""".brand{display:flex;align-items:baseline;gap:10px;""", """.brand .mark{align-self:center;flex:none}
.brand{display:flex;align-items:baseline;gap:10px;""")

open(p,'w').write(s); print('patched')
