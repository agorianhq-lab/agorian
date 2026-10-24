p='src/index.html'; s=open(p).read()
def rep(a,b,count=1):
    global s
    assert s.count(a)==count, (s.count(a), a[:70]); s=s.replace(a,b)

# ---------- CSS ----------
rep("""/* unit band on quiz card */""", """/* artwork */
.upanel{min-height:170px}
.upanel .art{display:none}
.upanel .photo{position:absolute;inset:0;background-size:cover;background-position:center;z-index:0}
.upanel .photo::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,var(--surface) 38%,color-mix(in srgb,var(--surface) 55%,transparent) 62%,transparent 100%)}
.upanel.eu .photo::after{background:linear-gradient(90deg,var(--eu-soft) 36%,color-mix(in srgb,var(--eu-soft) 50%,transparent) 60%,transparent 100%)}
.upanel.jp .photo::after{background:linear-gradient(90deg,var(--jp-soft) 36%,color-mix(in srgb,var(--jp-soft) 50%,transparent) 60%,transparent 100%)}
.upanel>span{position:relative;z-index:1}
.qart{margin:-22px -22px 0;height:120px;background-size:cover;background-position:center 35%;border-radius:var(--radius) var(--radius) 0 0;position:relative}
.qart::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,var(--surface) 100%)}
.qart .cap{position:absolute;right:10px;bottom:6px;font-size:11px;color:var(--muted);z-index:1;text-align:right;max-width:70%}
.stim img{display:block;max-width:100%;max-height:300px;margin:0 auto 10px;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.15)}
.credits{font-size:11px;color:var(--muted);margin-top:8px;line-height:1.5}
.credits summary{cursor:pointer}
@media (max-width:480px){.qart{height:90px}}
/* unit band on quiz card */""")

# ---------- image map in JS ----------
rep("""// did-you-know facts, keyed loosely to topics""", """// artwork (public domain, Wikimedia Commons), embedded at build time
const IMG = __IMG__;
const CAP = {
  'jp-wave':'Hokusai, The Great Wave off Kanagawa, c. 1831','jp-fuji':'Hokusai, Fine Wind, Clear Morning, c. 1831','jp-tokaido':'Hiroshige, Nihonbashi, Fifty-three Stations of the Tokaido, 1833','jp-samurai':'Samurai in armour, photograph, 1860s',
  'eu-bayeux':'Bayeux Tapestry, the death of Harold, c. 1070s','eu-heures':'Limbourg brothers, Très Riches Heures, October, c. 1412','eu-castle':'Limbourg brothers, Très Riches Heures, September, c. 1412','eu-plague':'Toggenburg Bible, plague victims, 1411','eu-crusade':'Siege of Jerusalem 1099, 13th-century manuscript'};
const TOPIC_IMG = {'Feudalism and hierarchy':'eu-heures','Law and order':'eu-heures','Castles and knights':'eu-castle','Catholic Church':'eu-castle','The Crusades':'eu-crusade','The Black Death':'eu-plague',
  'Feudalism and samurai':'jp-samurai','Tokugawa Shogunate':'jp-tokaido','Meiji Restoration':'jp-wave','Source analysis':'eu-bayeux','Chronology':'eu-heures','Comparing the two societies':'jp-fuji','Historical concepts':'eu-castle','Turning points':'eu-bayeux'};
function stimImg(q){ const t=(q.stimulus||'').toLowerCase(); if(t.includes('decameron')) return 'eu-plague'; if(t.includes('hokusai')) return 'jp-fuji'; if(t.includes('military houses')) return 'jp-samurai'; if(t.includes('clermont')) return 'eu-crusade'; if(t.includes('nagasaki')) return 'jp-tokaido'; return null }
const art = (k,extra='') => k&&IMG[k] ? `<div class="qart" style="background-image:url(${IMG[k]})${extra}"><span class="cap">${esc(CAP[k])}</span></div>` : '';
// did-you-know facts, keyed loosely to topics""")

# ---------- unit panels: photo backgrounds ----------
rep("""<button class="upanel eu" data-unit="Medieval Europe"><span class="t">""", """<button class="upanel eu" data-unit="Medieval Europe"><span class="photo" style="background-image:url(${IMG['eu-bayeux']});background-position:center 30%"></span><span class="t">""")
rep("""<button class="upanel jp" data-unit="Shogunate Japan"><span class="t">""", """<button class="upanel jp" data-unit="Shogunate Japan"><span class="photo" style="background-image:url(${IMG['jp-wave']});background-position:center 45%"></span><span class="t">""")

# ---------- question card: topic art + stimulus image ----------
rep("""  const stim = q.stimulus ? `<div class="stim">${esc(q.stimulus).replace(/"([^"]+)"/g,'<p style="margin-top:6px">“$1”</p>')}</div>` : '';""",
    """  const si = stimImg(q);
  const stim = q.stimulus ? `<div class="stim">${si?`<img src="${IMG[si]}" alt="${esc(CAP[si])}">`:''}${esc(q.stimulus).replace(/"([^"]+)"/g,'<p style="margin-top:6px">“$1”</p>')}${si?`<p class="cap" style="font-size:11px;color:var(--muted);margin-top:6px">${esc(CAP[si])}</p>`:''}</div>` : '';""")
rep("""  <div class="card ${unitCls(q.unit)}">
    <div class="qhead">""", """  <div class="card ${unitCls(q.unit)}">
    ${si?'':art(TOPIC_IMG[q.topic])}
    <div class="qhead">""")

# ---------- results banner ----------
rep("""  <div class="card">
    <div class="score">""", """  <div class="card">
    ${art(state.mode==='challenge'?'jp-fuji':(TOPIC_IMG[Object.keys(byTopic)[0]]||'eu-bayeux'))}
    <div class="score">""")

# ---------- credits in footer ----------
rep("""<footer><span>Built for Year 8 History, Semester 2. Medieval Europe and Shogunate Japan.</span><span id="qcount"></span></footer>""",
"""<footer><span>Built for Year 8 History, Semester 2. Medieval Europe and Shogunate Japan.</span><span id="qcount"></span></footer>
<details class="credits wrap"><summary>Image credits</summary>All artworks are in the public domain and sourced from Wikimedia Commons. Katsushika Hokusai, The Great Wave off Kanagawa and Fine Wind, Clear Morning (c. 1831). Utagawa Hiroshige, Nihonbashi from The Fifty-three Stations of the Tokaido (1833). Photograph of a samurai in armour (1860s). The Bayeux Tapestry, scene 57 (c. 1070s). Limbourg brothers, Très Riches Heures du duc de Berry, September and October (c. 1412 to 1416). Toggenburg Bible (1411). Siege of Jerusalem, 13th-century manuscript, Bibliothèque nationale de France.</details>""")
rep("""<div class="wrap">
<header>""", """<div class="wrap" id="top">
<header>""")
open(p,'w').write(s); print('patched')
