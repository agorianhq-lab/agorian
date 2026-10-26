import json
EU=[(793,"Vikings raid Lindisfarne","Raids on monasteries begin two centuries of Viking pressure on Europe."),
(800,"Charlemagne crowned emperor","The Pope crowns a Frankish king, tying royal power to the Church."),
(1066,"Battle of Hastings","William of Normandy defeats Harold. Feudalism and castles follow."),
(1086,"Domesday Book","Every landholding in England recorded for the king."),
(1095,"Pope Urban II calls the First Crusade","The speech at Clermont promises forgiveness of sins."),
(1099,"Crusaders capture Jerusalem","The First Crusade ends in victory and massacre."),
(1170,"Thomas Becket murdered","Knights kill the archbishop in Canterbury Cathedral; Church v king."),
(1187,"Saladin retakes Jerusalem","Triggers the Third Crusade."),
(1209,"King John excommunicated","Innocent III cuts the king off from the Church."),
(1215,"Magna Carta","The king accepts he is under the law. The Church also bans priests from trials by ordeal."),
(1291,"Fall of Acre","The last Crusader state is lost."),
(1347,"The Black Death reaches Europe","Plague arrives in Sicily by ship; a third to a half of Europe dies by 1351."),
(1351,"Statute of Labourers","English lords try to freeze wages after the plague."),
(1381,"Peasants' Revolt","Wat Tyler's rebels march on London."),
(1453,"Fall of Constantinople","Often taken as the end of the Middle Ages. Gutenberg's press is printing in the same decade."),
(1485,"Battle of Bosworth","The Tudors take the English throne; medieval England ends."),]
JP=[(794,"Court moves to Heian-kyo","The Heian period begins; Fujiwara nobles dominate the emperor."),
(1180,"Genpei War begins","Minamoto and Taira clans fight for control; samurai rise."),
(1185,"Minamoto victory at Dan-no-ura","The Genpei War ends. Kamakura period begins."),
(1192,"Yoritomo becomes shogun","The first shogunate. Emperor stays as figurehead."),
(1232,"Goseibai Shikimoku","The first written law code for samurai."),
(1274,"First Mongol invasion","Repelled; a second in 1281 is wrecked by the kamikaze typhoon."),
(1333,"Kamakura shogunate falls","Brief imperial restoration, then civil war."),
(1336,"Ashikaga shogunate","The Muromachi period. Weak shoguns, strong daimyo."),
(1467,"Onin War begins","A century of civil war between daimyo (the Sengoku period)."),
(1543,"Portuguese arrive with firearms","First Europeans in Japan."),
(1549,"Francis Xavier brings Christianity","Jesuit missions convert daimyo in Kyushu."),
(1600,"Battle of Sekigahara","Tokugawa Ieyasu defeats his rivals."),
(1603,"Ieyasu named shogun","The Edo period begins. 250 years of Tokugawa rule."),
(1615,"Laws for the Military Houses","Daimyo controlled: castles, marriages, alliances."),
(1635,"Sankin kotai made compulsory","Alternate attendance in Edo."),
(1639,"Sakoku complete","Portuguese expelled; only Dutch and Chinese at Nagasaki. Christianity banned since 1614."),
(1700,"Edo passes a million people","Probably the largest city in the world. Merchant culture: kabuki, ukiyo-e, the 47 ronin story (1703)."),
(1837,"Oshio Heihachiro's revolt","A former official rebels in Osaka after famine. A sign the shogunate was failing before Perry."),
(1853,"Commodore Perry arrives","Black ships in Edo Bay. Treaty of Kanagawa follows in 1854."),
(1868,"Meiji Restoration","The last shogun resigns; power returns to the emperor."),
(1873,"Conscription","A national army replaces samurai. Swords banned 1876; Satsuma Rebellion 1877."),
(1889,"Meiji Constitution","Japan becomes a constitutional monarchy; defeats Russia in 1905."),]
EUP=[(780,1000,"Early Middle Ages"),(1000,1300,"High Middle Ages"),(1300,1500,"Late Middle Ages"),(1500,1900,"After the unit")]
JPP=[(794,1185,"Heian"),(1185,1333,"Kamakura"),(1336,1573,"Muromachi"),(1573,1603,"Azuchi-Momoyama"),(1603,1868,"Edo (Tokugawa)"),(1868,1900,"Meiji")]
LINKS=[(1066,1185,"Warriors take power. The Normans conquer England; the Minamoto take Japan from the court."),
(1215,1232,"Written law limits rulers and warriors. Magna Carta; the samurai law code."),
(1095,1274,"Holy war and foreign invasion. Crusaders go east; the Mongols come to Japan."),
(1347,1333,"Mid-1300s upheaval. The Black Death; the fall of Kamakura."),
(1453,1467,"The medieval order breaks up. Constantinople falls; Japan's civil wars begin."),]
# piecewise scale: slow before 1050, fast 1050-1500, medium after
SEG=[(780,1050,0.5),(1050,1500,3.0),(1500,1900,1.9)]
def y(yr):
    out=0
    for a,b,k in SEG:
        if yr<=a: break
        out+=(min(yr,b)-a)*k
    return out
H=y(1900)
def col(evs,side):
    out=[]; last=-99
    for yr,t,d in evs:
        top=y(yr)
        if top-last<27: top=last+27
        last=top
        out.append(f'<div class="ev {side}" style="top:{top:.0f}px"><span class="yr">{yr}</span><div class="card"><b>{t}</b><span>{d}</span></div></div><i class="dot {side}" style="top:{y(yr):.0f}px"></i>')
    return ''.join(out)
def bands(ps,side): return ''.join(f'<div class="band {side}" style="top:{y(a):.0f}px;height:{y(b)-y(a):.0f}px"><span>{n}</span></div>' for a,b,n in ps)
ticks=''.join(f'<div class="tick" style="top:{y(yr):.0f}px"><span>{yr}</span></div>' for yr in range(800,1901,100))
links=''.join(f'<div class="link" style="top:{min(y(a),y(b)):.0f}px;height:{abs(y(a)-y(b)):.0f}px"><i style="top:{(y(a)-min(y(a),y(b))):.0f}px"></i><i style="top:{(y(b)-min(y(a),y(b))):.0f}px"></i><em>{d}</em></div>' for a,b,d in LINKS)
CSS=open('timelines.css').read()
html=f"""<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Two timelines</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS.replace('__H__',f'{H:.0f}')}</style></head><body><div class="wrap">
<h1>Two worlds, <em>one</em> timeline</h1>
<p class="sub">Medieval Europe on the left, Japan on the right, on the same scale. Click an event for a line of detail. The dotted gold links mark moments when the two units rhyme. The scale is stretched between 1050 and 1500, where most of both units sits.</p>
<div class="legend"><span><i style="background:var(--eu)"></i>Medieval Europe</span><span><i style="background:var(--jp)"></i>Shogunate Japan</span><span><i style="background:var(--gold);height:0;border-top:2px dotted var(--gold)"></i>A connection worth knowing</span><span>Shaded bands are the periods each society is divided into.</span></div>
<div class="head"><h2 class="eu">Medieval Europe</h2><div class="mid">CE</div><h2 class="jp">Shogunate Japan</h2></div>
<div class="tl"><div class="colL">{bands(EUP,'eu')}{col(EU,'eu')}</div><div class="spine">{ticks}{links}</div><div class="colR">{bands(JPP,'jp')}{col(JP,'jp')}</div></div>
<p class="foot">Dates are the ones used in class. Where historians give a range (the Genpei War, the Mongol invasions, the Black Death), the first year is shown.</p>
</div><script>document.querySelectorAll('.ev').forEach(e=>e.addEventListener('click',()=>e.classList.toggle('open')));</script></body></html>"""
open('timelines.html','w').write(html); print('built',H)
