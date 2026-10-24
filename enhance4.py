p='src/index.html'; s=open(p).read()
def rep(a,b,count=1):
    global s
    assert s.count(a)==count, (s.count(a), a[:70]); s=s.replace(a,b)

# ---------- CSS ----------
rep("""/* write */""", """/* what success looks like */
.tabs{display:flex;gap:6px;border-bottom:1px solid var(--line);margin-bottom:4px}
.tab{border:0;background:none;padding:10px 14px;font-weight:700;color:var(--muted);cursor:pointer;border-bottom:3px solid transparent;margin-bottom:-1px}
.tab.on{color:var(--plum);border-bottom-color:var(--plum)}
.model{display:grid;gap:6px;font-size:18px;line-height:1.55}
.model .sent{padding:8px 12px 8px 14px;border-left:5px solid var(--c);background:color-mix(in srgb,var(--c) 10%,var(--surface));border-radius:0 8px 8px 0;display:grid;grid-template-columns:40px 1fr;gap:10px;align-items:start}
.model .sent b{font-family:var(--display);color:var(--c);font-size:18px}
.sent.T{--c:var(--navy)} .sent.X{--c:var(--teal)} .sent.E{--c:var(--gold-ink)} .sent.A{--c:var(--accent)} .sent.L{--c:var(--sage)}
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;font-size:14px;color:var(--muted)}
.legend span::before{content:"";display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px;background:var(--c)}
.rubric{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.rubric div{border:1px solid var(--line);border-radius:10px;padding:10px 12px;text-align:center;background:var(--bg)}
.rubric b{display:block;font-family:var(--display);font-size:26px;color:var(--plum)}
.rubric small{color:var(--muted);display:block;font-size:13px;line-height:1.3}
@media (max-width:600px){.rubric{grid-template-columns:repeat(2,1fr)}}
.marks{display:inline-block;font-family:var(--display);font-weight:700;padding:2px 10px;border-radius:999px;font-size:15px}
.marks.full{background:var(--ok-bg);color:var(--ok)} .marks.weak{background:var(--bad-bg);color:var(--bad)}
.sample{border:1px solid var(--line);border-radius:10px;padding:14px 16px;display:grid;gap:8px;background:var(--bg)}
.sample.weak{border-color:var(--bad);border-left-width:5px}
.sample.full{border-color:var(--ok);border-left-width:5px}
.sample .why{font-size:15px;color:var(--muted)}
.sample .why b{color:var(--ink)}
.skill{display:grid;gap:12px}
.skill h3{font-size:22px;color:var(--plum)}
.frame{font-family:var(--display);font-size:19px;background:var(--plum);color:#fff;padding:12px 16px;border-radius:10px;line-height:1.5}
.frame i{color:var(--gold);font-style:normal}
.ladder{display:grid;gap:4px}
.ladder div{display:grid;grid-template-columns:150px 1fr;gap:10px;padding:8px 12px;border-left:4px solid var(--sage);background:color-mix(in srgb,var(--sage) 10%,var(--surface));border-radius:0 8px 8px 0;font-size:16px}
.ladder div b{color:var(--sage)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media (max-width:700px){.two{grid-template-columns:1fr}.ladder div{grid-template-columns:1fr}}
.selfcheck{display:grid;gap:6px}
.selfcheck label{display:flex;gap:10px;align-items:flex-start;font-size:16px;cursor:pointer}
.selfcheck input{width:20px;height:20px;accent-color:var(--plum);margin-top:2px;flex:none}
.hub{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
.hubcard{text-align:left;border:1px solid var(--line);border-left:5px solid var(--plum);border-radius:10px;padding:14px 16px;background:var(--surface);cursor:pointer;display:grid;gap:4px}
.hubcard:hover{border-color:var(--plum)}
.hubcard b{font-family:var(--display);font-size:20px;color:var(--plum)}
.hubcard span{font-size:15px;color:var(--muted)}
/* write */""")

# ---------- data ----------
rep("""// ---------- paragraph practice ----------""", r"""// ---------- what success looks like: models and worked examples ----------
const TEEAL=[['T','Topic sentence','State your argument in answer to the question.'],['X','Explain','Elaborate on the topic sentence. What do you mean?'],['E','Evidence','At least two specific facts. Names, dates, places, a quote from a source.'],['A','Analyse','Why does the evidence matter? What caused it, what did it change, how does it support your argument?'],['L','Link','Return to the question with a judgement.']];
const TAGNAME={T:'Topic',X:'Explain',E:'Evidence',A:'Analyse',L:'Link',EA:'Evidence + analyse'};
const RUBRIC=[['3','Analysis','Significance, cause and effect, a judgement'],['2','Knowledge','Specific, accurate, relevant'],['1','Structure','TEEAL with a clear contention'],['2','Writing','Clear expression, terms, spelling']];
// bank prompt id -> model. Three paragraphs are from the Moving Marks pack. Black Death, Church and Perry are drafted in the same style for teacher checking.
const SUCCESS={
 86:{model:[['T','The Crusades were significant for medieval Europe mainly because they opened Europe to the wider world, which changed its economy and ideas far more than they changed the Holy Land.'],['E','Between 1096 and 1291 Crusaders travelled through Constantinople and the eastern Mediterranean, and Italian cities such as Venice and Genoa transported and supplied them.'],['EA','These cities gained trading posts in the East and control of the routes that brought spices, silk and sugar to Europe, and their new wealth later helped fund the Renaissance.'],['E','Contact with the Islamic world also brought knowledge in medicine, mathematics and astronomy that European scholars had lost.'],['L','Although the Crusaders failed to hold Jerusalem, the trade and learning they brought back lasted for centuries, which is why the Crusades are a turning point for Europe rather than a military success.']],
   marks:'A 3  K 2  S 1  W 2  =  8 / 8', why:'The contention makes a judgement (economy and ideas mattered more than the Holy Land) rather than listing. Evidence is specific and dated. Each piece of evidence is explained. The last sentence weighs the failure against the long-term effect, which is significance.'},
 87:{draft:true,model:[['T','The Black Death weakened the feudal system mainly because it destroyed the supply of labour that the system depended on.'],['E','Between 1347 and 1351 the plague killed between a third and a half of Europe’s population, so that in many villages there were not enough peasants left to work the lord’s land.'],['A','Because labour was now scarce, surviving peasants could demand wages or leave for a lord who would pay more, which broke the old rule that a serf was tied to his manor.'],['E','Lords and kings tried to stop this. The English Statute of Labourers of 1351 tried to freeze wages at pre-plague levels, but it largely failed, and the resentment it caused fed the Peasants’ Revolt of 1381.'],['A','Over the following decades serfdom faded in England as lords found it easier to rent out land than to force people to work it.'],['L','The plague did not end feudalism overnight, but by shifting bargaining power from lords to workers it removed the foundation the system stood on, which is why historians treat it as a turning point.']],
   marks:'A 3  K 2  S 1  W 2  =  8 / 8', why:'The first sentence names the cause (labour) rather than describing the plague. The chain is explicit. Deaths, then scarce labour, then wages and movement, then the lords’ failed response. The link admits the change was gradual and still reaches a judgement.'},
 88:{draft:true,model:[['T','The Catholic Church maintained its influence over medieval society mainly through social power, because it was present at every stage of ordinary life in a way no king could match.'],['E','Every person was baptised, married and buried by the Church, and the year itself was organised around holy days and festivals, so religion shaped time as well as belief.'],['EA','Because most people could not read, the Church taught through what they could see, such as doom paintings of heaven and hell on church walls, which made the threat of damnation vivid and kept people obedient to its rules.'],['E','The Church also held economic and political power. The tithe took one tenth of every harvest, and the Pope could excommunicate a king, as Innocent III did to King John in 1209.'],['A','However, these powers depended on the social hold underneath them, since a tithe is only paid and excommunication is only feared by people who already believe the Church controls their path to heaven.'],['L','This is why social power mattered most, and why Church authority only weakened when the Black Death shook that everyday belief.']],
   marks:'A 3  K 2  S 1  W 2  =  8 / 8', why:'The question asks for a choice, and the paragraph makes one in the first sentence. The other forms of power are named but then ranked beneath the chosen one, which is evaluation rather than a list. Evidence is specific (tithe, King John, doom paintings).'},
 89:{draft:true,model:[['T','Commodore Perry’s arrival in 1853 was the trigger for the fall of the Tokugawa shogunate, but the shogunate was already failing from the inside, so the external pressure only exposed weaknesses that existed.'],['E','By the early 1800s the rigid social order no longer matched reality. Merchants at the bottom of the hierarchy had grown rich while many samurai and daimyo were in debt to them, and famines in the 1830s led to uprisings such as Oshio Heihachiro’s revolt in Osaka in 1837.'],['EA','When Perry’s steam-powered black ships forced the Treaty of Kanagawa in 1854, the shogunate could not resist, and because its whole claim to rule rested on protecting Japan from foreigners, this humiliation turned daimyo and samurai from domains such as Satsuma and Choshu against it.'],['A','Perry therefore caused the fall in the sense that he provided the moment, but the deeper cause was a government that had lost the confidence of the groups it depended on.'],['L','The strongest judgement is that internal decay made the fall likely and Perry made it happen, which is why the shogunate collapsed within fifteen years of his arrival.']],
   marks:'A 3  K 2  S 1  W 2  =  8 / 8', why:'The question sets up two views and the paragraph takes a position that uses both, trigger versus cause. Internal evidence comes before Perry, which matches the argument. The link makes a judgement rather than restating the question.'},
 90:{model:[['T','The Meiji Restoration transformed Japan to a large extent, although it kept the emperor and rule by a small elite.'],['E','After 1868 the new government abolished the feudal domains and replaced them with prefectures run from Tokyo, ended the samurai class by introducing a conscript army in 1873, and made education compulsory.'],['E','Railways, factories and a Western-style constitution in 1889 followed.'],['A','These changes meant that within forty years Japan had moved from a feudal society to an industrial power that defeated Russia in 1905.'],['A','However, the emperor remained the symbolic head of the nation and real power still sat with a small group of former samurai leaders, so the way Japan was governed changed more than who governed it.'],['L','Overall, the Restoration transformed Japan’s economy, army and society, while continuity remained at the very top.']],
   marks:'A 3  K 2  S 1  W 2  =  8 / 8', why:'To what extent is answered directly in the first sentence and returned to at the end. The paragraph names both change and continuity, which is what the question invites. Dates and reforms are specific.'}
};
const CALIB={q:'Analyse how the Tokugawa shogunate kept control of Japan.',
 full:{marks:'8 / 8',text:'The Tokugawa shogunate kept control of Japan for over 250 years mainly by controlling the daimyo, who were the only group able to challenge it. The policy of sankin kotai forced daimyo to spend alternate years in Edo and leave their families there, which drained their wealth through constant travel and made rebellion risky because their families were in the shogun’s hands. The Laws for the Military Houses of 1615 stopped daimyo from repairing castles or arranging marriages without permission, which prevented them from building military strength or alliances. The shoguns also closed Japan under sakoku and banned Christianity, so no daimyo could gain foreign weapons or a foreign religion as a rival loyalty. Together these edicts meant the daimyo stayed loyal not out of choice but because the cost of disloyalty was too high, which is why Japan stayed at peace until Western pressure arrived in 1853.',why:'Analysis 3. Every policy is followed by a which or because sentence that explains how it produced control. Knowledge 2. Structure 1. Writing 2.'},
 weak:{marks:'5 / 8',text:'The Tokugawa shogunate kept control in many ways. They used sankin kotai which made daimyo go to Edo. They also banned Christianity because they did not like it. They closed the country with sakoku so no foreigners could come in. They had a strict social hierarchy with samurai at the top and merchants at the bottom. The samurai followed bushido. All of these things helped the Tokugawa stay in power for a long time. In conclusion the Tokugawa kept control through laws and the hierarchy.',why:'Knowledge is accurate and covers several policies, so 2. Structure has a contention and a conclusion, so 1. Analysis is 1 because the paragraph lists what the shoguns did without explaining how each policy produced control, and the contention (many ways) makes no judgement. Writing is 1 for short repetitive sentences. Find the three places where a because sentence would lift the analysis mark.'}};
const SHORT=[
 {id:'explain',title:'Explain one factor (2 marks)',sub:'Identify it. Prove it. Link it.',body:()=>`
  <div class="skill"><p>Two-mark questions pay for the identify and the link. The evidence in between is what makes the link convincing. Four-mark questions want this twice.</p>
  <div class="ladder"><div><b>1 Identify</b><span>Name the one factor, cause, impact or feature the question asks for. <i>One factor was trade.</i></span></div><div><b>2 Prove</b><span>Give specific evidence. A date, a place, a name, a number, a quote from the source. <i>Ships from the Black Sea carried infected rats and fleas into Messina in 1347.</i></span></div><div><b>3 Link</b><span>Write a because or this meant sentence that connects the evidence to the question. <i>Because goods travelled inland along the same routes, the plague followed.</i></span></div></div>
  <p class="qtext" style="font-size:19px">Explain one factor that contributed to the spread of the Black Death through medieval Europe. (2 marks)</p>
  <div class="two">
   <div class="sample weak"><span class="marks weak">1 / 2</span><p>The Black Death spread because of trade. Ships carried it from the Black Sea to Italy in 1347, and medieval towns were crowded and dirty, so it spread quickly once it arrived.</p><p class="why"><b>Why 1.</b> Identifies a factor (trade) and adds accurate detail, so it earns the identify mark. It never says how trade caused the spread, so it misses the link mark. It also slips in a second factor, which the question did not ask for.</p></div>
   <div class="sample full"><span class="marks full">2 / 2</span><p>One factor was trade. Merchant ships from the Black Sea carried infected rats and fleas into Italian ports such as Messina in 1347. Because the ships then moved on to other ports and goods travelled inland along roads and rivers, the plague followed the same routes and reached most of Europe within four years.</p><p class="why"><b>Why 2.</b> Identifies one factor, proves it with specific evidence and then links with a because sentence that connects the evidence to the spread.</p></div>
  </div>
  <p class="eyebrow">Upgrade these. Each scores 1. Add the sentence that earns the second mark.</p>
  <div class="two">
   <div class="sample"><p><b>Explain one reason the Tokugawa shoguns introduced sakoku.</b><br>One reason was fear of Christianity. Missionaries had converted some daimyo in the 1500s. <i>Because ...</i></p><p class="why"><b>One link that works.</b> Because converted daimyo might put loyalty to a foreign religion above loyalty to the shogun, the shoguns saw Christianity as a threat to their control and closed the country to remove it.</p></div>
   <div class="sample"><p><b>Explain one restriction placed on the daimyo under the Tokugawa.</b><br>Sankin kotai meant daimyo had to live in Edo every second year and leave their families there. <i>Because ...</i></p><p class="why"><b>One link that works.</b> Because the constant travel and two households drained their money, and their families were effectively hostages, daimyo could not afford to build armies or risk rebellion.</p></div>
  </div></div>`},
 {id:'origin',title:'Identify the origin (1 mark)',sub:'Century, place, who. Primary or secondary.',body:()=>`
  <div class="skill"><p>Markers want the century or the date, and the place. Medieval times is not a century. Unknown artist is still worth writing, it shows you read the caption. To find the century, add one to the hundreds digit. 1290 is in the 1200s, so the 13th century.</p>
  <p class="qtext" style="font-size:19px">Tournament scene from an illuminated manuscript, produced in Genoa, Italy, by an unknown artist, c. 1290. Identify the origin of this source.</p>
  <div class="two"><div class="sample weak"><span class="marks weak">0 / 1</span><p>It was made in medieval times by an artist.</p></div><div class="sample full"><span class="marks full">1 / 1</span><p>It was created in the 13th century (c. 1290) in Genoa, Italy, by an unknown artist.</p></div></div>
  <div class="tbl"><table class="tt"><thead><tr><th>Caption</th><th>Century</th><th>Where</th><th>Primary or secondary</th></tr></thead><tbody>
   <tr><td>Colour woodblock print by Utagawa Hiroshige, Edo, 1833.</td><td>19th</td><td>Edo (Tokyo), Japan</td><td>Primary. Made during the Tokugawa period by a Japanese artist.</td></tr>
   <tr><td>Chronicle written by Fulcher of Chartres, a Christian living in the Crusader states, c. 1120.</td><td>12th</td><td>The Crusader states</td><td>Primary. An eyewitness account from the period.</td></tr>
   <tr><td>Chapter on the Black Death in a Year 8 history textbook, Melbourne, 2021.</td><td>21st</td><td>Melbourne, Australia</td><td>Secondary. Written long after the event by someone who was not there.</td></tr></tbody></table></div></div>`},
 {id:'compare',title:'One similarity, one difference (4 marks)',sub:'Two sentences in the frame score all four.',body:()=>`
  <div class="skill"><div class="frame">Both A and B <i>[shared feature]</i>, for example <i>[evidence for A]</i> and <i>[evidence for B]</i>. However, A <i>[feature]</i> whereas B <i>[feature]</i>, which meant <i>[consequence]</i>.</div>
  <p class="qtext" style="font-size:19px">Compare the daimyo and the samurai.</p>
  <div class="two">
   <div class="sample full"><span class="marks full">4 / 4</span><p>Both daimyo and samurai belonged to the warrior class and lived by bushido, for example both were expected to show loyalty to their superior and to fight and die with honour. However, daimyo were lords who controlled their own domains and commanded armies, whereas samurai were the warriors who served a daimyo in return for a stipend of rice, which meant a samurai’s position depended entirely on his lord.</p></div>
   <div class="sample weak"><span class="marks weak">2 / 4</span><p>Daimyo were lords and samurai were warriors. Daimyo had more power than samurai. They both lived in Japan and both followed bushido.</p><p class="why"><b>Why 2.</b> Identifies a similarity and a difference but gives no evidence and no consequence. Living in Japan is not a meaningful similarity. The marks lost are the two for explanation.</p></div>
  </div>
  <div class="sample full"><span class="marks full">4 / 4</span><p><b>Knights and samurai.</b> Both knights and samurai were warriors who served a lord in return for land or income and followed a code of conduct, for example chivalry in Europe and bushido in Japan. However, a knight’s code was tied to the Catholic Church and defending the Christian faith, whereas bushido was tied to loyalty to the daimyo and the honour of the samurai’s family, which meant a samurai who failed his lord might take his own life while a knight sought forgiveness from the Church.</p></div></div>`},
 {id:'turning',title:'Why is it a turning point? (3 marks)',sub:'Describing scores 1 of 3. Climb the ladder.',body:()=>`
  <div class="skill"><div class="ladder"><div><b>What happened</b><span>In 1600 Tokugawa Ieyasu defeated the rival daimyo at the Battle of Sekigahara.</span></div><div><b>So what changed</b><span>He became shogun in 1603 and ended a century of civil war between daimyo.</span></div><div><b>Who was affected</b><span>Every daimyo came under Tokugawa control through edicts such as sankin kotai. Samurai became administrators rather than fighters.</span></div><div><b>For how long</b><span>The Tokugawa ruled for over 250 years, which is why 1600 is a turning point.</span></div></div>
  <div class="two">
   <div class="sample weak"><span class="marks weak">1 / 3</span><p>The Battle of Sekigahara was in 1600. Tokugawa Ieyasu won against the other daimyo. It was a very big battle with thousands of samurai. It was a turning point because it was important.</p><p class="why"><b>Why 1.</b> Stays on rung one. The size of the battle is detail, not significance.</p></div>
   <div class="sample full"><span class="marks full">3 / 3</span><p>The Battle of Sekigahara in 1600 was a turning point because Tokugawa Ieyasu’s victory allowed him to become shogun in 1603 and bring over a century of civil war to an end. His family then ruled Japan for more than 250 years, controlling the daimyo through edicts and keeping the country at peace, so the direction of Japanese history changed from war to stability.</p><p class="why"><b>Why 3.</b> Climbs to rung four and uses the word because.</p></div>
  </div>
  <p class="hint">Try the ladder yourself for the Battle of Hastings, the Genpei War or the Black Death.</p></div>`},
 {id:'impacts',title:'Short-term and long-term impacts (4 marks)',sub:'Two marks per impact. One to identify, one for the because.',body:()=>`
  <div class="skill"><p>Short-term happens during or just after the event. Long-term unfolds over decades. Both paragraphs below name the impact in the first sentence and explain it in the second.</p>
  <p class="qtext" style="font-size:19px">Discuss one short-term and one long-term impact of the Black Death.</p>
  <div class="sample full"><span class="marks full">4 / 4</span><p>One short-term impact was that so many people died so quickly that normal burial broke down. In cities such as Florence bodies were stacked in plague pits because there were not enough living to dig graves. This caused panic and the breakdown of everyday order during 1348.</p><p>One long-term impact was the weakening of feudalism. Because between a third and a half of the population had died, there were not enough peasants to work the land, so survivors could demand wages or move to another lord. Over the following decades this undermined serfdom and the lords’ control.</p></div>
  <div class="tbl"><table class="tt"><thead><tr><th>Impact</th><th>Short or long</th><th>Why</th></tr></thead><tbody>
   <tr><td>Flagellants whipping themselves in towns</td><td>Short</td><td>A panic response during the outbreak</td></tr>
   <tr><td>Faith in the Church weakened over decades</td><td>Long</td><td>A slow change in attitudes, not an event</td></tr>
   <tr><td>The last shogun resigns in 1868</td><td>Short</td><td>The event of the Restoration itself</td></tr>
   <tr><td>Japan defeats Russia in 1905</td><td>Long</td><td>Nearly 40 years after, the result of modernisation</td></tr>
   <tr><td>A national conscript army built by 1873</td><td>Short or long</td><td>Five years on. The point is your reasoning</td></tr></tbody></table></div></div>`},
 {id:'paragraph',title:'The extended response (8 marks)',sub:'An 8 beside a 5. Find the three missing because sentences.',body:()=>`
  <div class="skill"><div class="rubric">${RUBRIC.map(r=>`<div><b>${r[0]}</b>${r[1]}<small>${r[2]}</small></div>`).join('')}</div>
  <p class="qtext" style="font-size:19px">${esc(CALIB.q)}</p>
  <div class="two"><div class="sample full"><span class="marks full">${CALIB.full.marks}</span><p>${esc(CALIB.full.text)}</p><p class="why"><b>Why 8.</b> ${esc(CALIB.full.why)}</p></div>
  <div class="sample weak"><span class="marks weak">${CALIB.weak.marks}</span><p>${esc(CALIB.weak.text)}</p><p class="why"><b>Why 5.</b> ${esc(CALIB.weak.why)}</p></div></div>
  <p>The three habits that cost the most marks. Describing an event instead of explaining why it mattered. Answering a source question without quoting or pointing to the source. Giving two factors when the question asked for one, or a list when it asked for a link.</p></div>`}
];
function modelHTML(m){ return `<div class="legend">${TEEAL.map(t=>`<span class="sent ${t[0]}" style="padding:0;border:0;background:none;display:inline">${t[1]}</span>`).join('')}</div><div class="model">${m.model.map(([tag,txt])=>`<div class="sent ${tag[0]}"><b>${tag}</b><span>${esc(txt)}</span></div>`).join('')}</div>
  <div class="row" style="justify-content:space-between"><span class="marks full">${esc(m.marks)}</span>${m.draft?'<span class="hint">Draft model, written in the style of the marked samples. Check before relying on it.</span>':'<span class="hint">From the marked exam samples.</span>'}</div><div class="feedback info"><b>Why it scores 8</b><span>${esc(m.why)}</span></div>` }

function success(open){
  const draw=(id)=>{
    const sk=SHORT.find(x=>x.id===id);
    h(`<section class="section">${MODEH('write','What success looks like')}
    <p class="muted">Marked answers for every kind of exam question, with the reasons marks are won and lost. Written from the exam’s own mark scheme.</p>
    ${sk?`<div class="card"><div class="row" style="justify-content:space-between"><h3 style="font-size:24px;color:var(--plum)">${esc(sk.title)}</h3><button class="btn quiet" id="back">All question types</button></div>${sk.body()}</div>`:
    `<div class="hub">${SHORT.map(x=>`<button class="hubcard" data-id="${x.id}"><b>${esc(x.title)}</b><span>${esc(x.sub)}</span></button>`).join('')}
      <button class="hubcard" data-go="write" style="border-left-color:var(--gold-ink)"><b>Model paragraphs</b><span>A full TEEAL answer for each of the five paragraph prompts, sentence by sentence.</span></button></div>
     <div class="row"><button class="btn quiet" id="home">Home</button></div>`}
    </section>`);
    app.querySelectorAll('[data-id]').forEach(b=>b.onclick=()=>draw(b.dataset.id));
    const bk=app.querySelector('#back'); if(bk) bk.onclick=()=>draw(null);
    const hm=app.querySelector('#home'); if(hm) hm.onclick=home;
    const w=app.querySelector('[data-go=write]'); if(w) w.onclick=write;
  };
  draw(open||null);
}

// ---------- paragraph practice ----------""")

# ---------- paragraph practice: tabs, corrected TEEAL, self-check, success link ----------
rep("""      <div class="scaffold"><p class="eyebrow">TEEAL scaffold</p>
        ${[['T','Topic sentence. State your argument in answer to the question.'],['E','Evidence. A specific fact, date, person or source.'],['E','Explain. What does the evidence show?'],['A','Analyse. Why does it matter? How does it support your argument?'],['L','Link. Return to the question with a judgement.']].map(([a,b])=>`<div class="s"><b>${a}</b><span>${b}</span></div>`).join('')}</div>
      <textarea id="d${q.id}" placeholder="Write your paragraph here. It stays on this device.">${esc(drafts[q.id]||'')}</textarea>
      <div class="row" style="justify-content:space-between"><span class="hint" id="wc"></span><button class="btn" id="guide">Show marker guidance</button></div>
      <div id="g" hidden class="feedback info"><b>What a marker looks for</b><span>${esc(q.guidance)}</span></div>
      <div class="row"><button class="btn primary" id="save">Save draft</button><button class="btn quiet" id="back">All prompts</button></div>""",
"""      <div class="tabs"><button class="tab on" data-tab="write">Write</button><button class="tab" data-tab="model">What success looks like</button></div>
      <div id="pane-write">
      <div class="scaffold"><p class="eyebrow">TEEAL scaffold</p>
        ${TEEAL.map(([a,b,c])=>`<div class="s"><b>${a==='X'?'E':a}</b><span><b style="font-family:var(--body);color:var(--ink)">${b}.</b> ${c}</span></div>`).join('')}</div>
      <textarea id="d${q.id}" placeholder="Write your paragraph here. It stays on this device." style="margin-top:12px">${esc(drafts[q.id]||'')}</textarea>
      <div class="row" style="justify-content:space-between;margin-top:8px"><span class="hint" id="wc"></span><button class="btn" id="guide">Show marker guidance</button></div>
      <div id="g" hidden class="feedback info" style="margin-top:8px"><b>What a marker looks for</b><span>${esc(q.guidance)}</span></div>
      <div class="selfcheck" style="margin-top:12px"><p class="eyebrow">Check your draft</p>
        ${[['t','My first sentence makes an argument, not a description.'],['e','I have at least two specific pieces of evidence with a name, date or place.'],['a','Every piece of evidence is followed by a because or this meant sentence.'],['j','My last sentence returns to the question with a judgement.'],['w','I have used the key terms and checked spelling.']].map(([k,t])=>`<label><input type="checkbox" id="sc-${q.id}-${k}"><span>${t}</span></label>`).join('')}</div>
      <div class="row" style="margin-top:12px"><button class="btn primary" id="save">Save draft</button><button class="btn quiet" id="back">All prompts</button></div>
      </div>
      <div id="pane-model" hidden>${SUCCESS[q.id]?modelHTML(SUCCESS[q.id]):'<p class="muted">No model paragraph for this prompt yet.</p>'}
        <div class="row" style="margin-top:12px"><button class="btn" id="rub">Rubric and short-answer examples</button><button class="btn quiet" id="back2">All prompts</button></div></div>""")
rep("""    app.querySelector('#back').onclick=write;
  };
  h(`<section class="section">${MODEH('write','Paragraph practice')}<p class="muted">Five exam style prompts.""",
"""    app.querySelector('#back').onclick=write; app.querySelector('#back2').onclick=write; app.querySelector('#rub').onclick=()=>success('paragraph');
    app.querySelectorAll('.tab').forEach(t=>t.onclick=()=>{ app.querySelectorAll('.tab').forEach(x=>x.classList.toggle('on',x===t)); app.querySelector('#pane-write').hidden=t.dataset.tab!=='write'; app.querySelector('#pane-model').hidden=t.dataset.tab!=='model' });
  };
  h(`<section class="section">${MODEH('write','Paragraph practice')}<p class="muted">Five exam style prompts.""")
rep("""Each opens with the TEEAL scaffold and, when you're ready, the guidance a marker would use.</p>""",
"""Each opens with the TEEAL scaffold, a model answer marked 8 out of 8, and the guidance a marker uses.</p>
  <button class="hubcard" id="succ" style="border-left-color:var(--gold-ink)"><b>What success looks like</b><span>Marked answers for every kind of exam question. Two-mark explains, compares, turning points, captions, impacts and the 8-mark paragraph.</span></button>""")
rep("""  app.querySelectorAll('[data-id]').forEach(b=>b.onclick=()=>pick(+b.dataset.id));
  app.querySelector('#home').onclick=home;
}""","""  app.querySelectorAll('[data-id]').forEach(b=>b.onclick=()=>pick(+b.dataset.id));
  app.querySelector('#home').onclick=home; app.querySelector('#succ').onclick=()=>success();
}""")
# tile copy + results link + routes
rep("""<span class="n">Exam style prompts with a TEEAL scaffold and marker guidance.</span>""","""<span class="n">Exam prompts with a TEEAL scaffold, model answers and what success looks like.</span>""")
rep("""<div class="row"><button class="btn primary" id="again">${state.mode==='challenge'?'New challenge':'Practise again'}</button>""","""<div class="row"><button class="btn primary" id="again">${state.mode==='challenge'?'New challenge':'Practise again'}</button><button class="btn" id="succ">What success looks like</button>""")
rep("""  app.querySelector('#home').onclick=home;
  log({event:'session_end', mode:state.mode, n, c});""","""  app.querySelector('#home').onclick=home; app.querySelector('#succ').onclick=()=>success();
  log({event:'session_end', mode:state.mode, n, c});""")
rep("""const ROUTES={practice:setup, challenge, terms, write, daily, timeline, teacher, sprint, facts};""","""const ROUTES={practice:setup, challenge, terms, write, daily, timeline, teacher, sprint, facts, success};""")
open(p,'w').write(s); print('patched')
