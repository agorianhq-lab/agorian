import json
A=json.load(open('assets.json')); T=A['T']; B=A['B']
for k in ('1635','1639','1889','1086'): T.pop(k,None)
# kinds: pol (power and rule), war, faith, life (society, culture, economy)
EU=[(793,"Vikings raid Lindisfarne","Raids on monasteries begin two centuries of Viking pressure on Europe.","war"),
(800,"Charlemagne crowned emperor","The Pope crowns a Frankish king, tying royal power to the Church.","pol"),
(1066,"Battle of Hastings","William of Normandy defeats Harold. Feudalism and castles follow.","war"),
(1086,"Domesday Book","Every landholding in England recorded for the king.","pol"),
(1095,"Pope Urban II calls the First Crusade","The speech at Clermont promises forgiveness of sins.","faith"),
(1099,"Crusaders capture Jerusalem","The First Crusade ends in victory and massacre.","war"),
(1170,"Thomas Becket murdered","Knights kill the archbishop in Canterbury Cathedral; Church v king.","faith"),
(1187,"Saladin retakes Jerusalem","Triggers the Third Crusade.","war"),
(1209,"King John excommunicated","Innocent III cuts the king off from the Church.","faith"),
(1215,"Magna Carta","The king accepts he is under the law. The Church also bans priests from trials by ordeal.","pol"),
(1291,"Fall of Acre","The last Crusader state is lost.","war"),
(1347,"The Black Death reaches Europe","Plague arrives in Sicily by ship; a third to a half of Europe dies by 1351.","life"),
(1351,"Statute of Labourers","English lords try to freeze wages after the plague.","life"),
(1381,"Peasants' Revolt","Wat Tyler's rebels march on London.","life"),
(1453,"Fall of Constantinople","Often taken as the end of the Middle Ages. Gutenberg's press is printing in the same decade.","war"),
(1485,"Battle of Bosworth","The Tudors take the English throne; medieval England ends.","pol"),]
JP=[(794,"Court moves to Heian-kyo","The Heian period begins; Fujiwara nobles dominate the emperor.","pol"),
(798,"Kiyomizu-dera founded","The Pure Water Temple in Kyoto, still standing.","faith"),
(1008,"The Tale of Genji","Murasaki Shikibu's novel of court life, often called the world's first.","life"),
(1180,"Genpei War begins","Minamoto and Taira clans fight for control; samurai rise.","war"),
(1185,"Minamoto victory at Dan-no-ura","The Genpei War ends. Kamakura period begins.","war"),
(1192,"Yoritomo becomes shogun","The first shogunate. Emperor stays as figurehead.","pol"),
(1232,"Goseibai Shikimoku","The first written law code for samurai.","pol"),
(1274,"First Mongol invasion","Repelled; a second in 1281 is wrecked by the kamikaze typhoon.","war"),
(1333,"Kamakura shogunate falls","Brief imperial restoration, then civil war.","pol"),
(1336,"Ashikaga shogunate","The Muromachi period. Weak shoguns, strong daimyo.","pol"),
(1467,"Onin War begins","A century of civil war between daimyo (the Sengoku period).","war"),
(1543,"Portuguese arrive with firearms","First Europeans in Japan.","life"),
(1549,"Francis Xavier brings Christianity","Jesuit missions convert daimyo in Kyushu.","faith"),
(1600,"Battle of Sekigahara","Tokugawa Ieyasu defeats his rivals. Many date the Edo period from here.","war"),
(1603,"Ieyasu named shogun","250 years of Tokugawa rule from Edo.","pol"),
(1614,"Christianity banned","Converts persecuted; the Shimabara rebellion of 1637 is crushed.","faith"),
(1615,"Laws for the Military Houses","Daimyo controlled: castles, marriages, alliances.","pol"),
(1635,"Sankin kotai made compulsory","Alternate attendance in Edo.","pol"),
(1639,"Sakoku complete","Portuguese expelled; only Dutch and Chinese at Nagasaki.","pol"),
(1700,"Edo passes a million people","Probably the largest city in the world. Kabuki, ukiyo-e, the 47 ronin story (1703).","life"),
(1837,"Oshio Heihachiro's revolt","A former official rebels in Osaka after famine. The shogunate was failing before Perry.","life"),
(1853,"Commodore Perry arrives","Black ships in Edo Bay. Treaty of Kanagawa follows in 1854.","war"),
(1868,"Meiji Restoration","The last shogun resigns; power returns to the emperor.","pol"),
(1873,"Conscription","A national army replaces samurai. Swords banned 1876; Satsuma Rebellion 1877.","life"),
(1889,"Meiji Constitution","Japan becomes a constitutional monarchy; defeats Russia in 1905.","pol"),]
EUP=[(780,1000,"Early Middle Ages","eu1"),(1000,1300,"High Middle Ages","eu2"),(1300,1500,"Late Middle Ages","eu3"),(1500,1925,"After the unit",None)]
JPP=[(794,1185,"Heian",None),(1185,1333,"Kamakura","jp2"),(1336,1573,"Muromachi",None),(1573,1600,"Azuchi-Momoyama",None),(1600,1868,"Edo (Tokugawa)","jp3"),(1868,1925,"Meiji","jp4")]
LINKS=[(1066,1185,"Warriors take power. The Normans conquer England; the Minamoto take Japan from the court."),
(1215,1232,"Written law limits rulers and warriors. Magna Carta; the samurai law code."),
(1095,1274,"Holy war and foreign invasion. Crusaders go east; the Mongols come to Japan."),
(1347,1333,"Mid-1300s upheaval. The Black Death; the fall of Kamakura."),
(1453,1467,"The medieval order breaks up. Constantinople falls; Japan's civil wars begin."),]
SEG=[(780,1050,0.6),(1050,1500,3.0),(1500,1925,2.4)]
def y(yr):
    out=0
    for a,b,k in SEG:
        if yr<=a: break
        out+=(min(yr,b)-a)*k
    return out
H=y(1925)
MAXB=[0]
KN={'pol':'Power and rule','war':'War and conquest','faith':'Faith and the Church','life':'Society, culture and economy'}
def col(evs,side):
    out=[]; last=-99; lasth=0
    for yr,t,d,k in evs:
        th=T.get(str(yr)); img=f'<img src="{th}" alt="">' if th else ''
        hgt=60 if th else 34
        top=y(yr)
        if top-last<lasth+6: top=last+lasth+6
        last=top; lasth=hgt; MAXB[0]=max(MAXB[0],top+hgt)
        out.append(f'<div class="ev {side} k-{k}" style="top:{top:.0f}px"><span class="yr">{yr}</span><div class="card">{img}<div><b>{t}</b><span>{d}</span></div></div></div><i class="dot {side} k-{k}" style="top:{y(yr):.0f}px"></i>')
    return ''.join(out)
def bands(ps,side):
    return ''.join(f'<div class="band {side}" style="top:{y(a):.0f}px;height:{y(b)-y(a):.0f}px;{("background-image:url("+B[img]+")") if img else ""}"><span>{n}</span></div>' for a,b,n,img in ps)
ticks=''.join(f'<div class="tick" style="top:{y(yr):.0f}px"><span>{yr}</span></div>' for yr in range(800,1901,100))
links=''.join(f'<div class="link" style="top:{min(y(a),y(b)):.0f}px;height:{abs(y(a)-y(b)):.0f}px"><i style="top:{(y(a)-min(y(a),y(b))):.0f}px"></i><i style="top:{(y(b)-min(y(a),y(b))):.0f}px"></i><em>{d}</em></div>' for a,b,d in LINKS)
CSS=open('timelines.css').read()
legend=''.join(f'<span><i class="sw k-{k}"></i>{v}</span>' for k,v in KN.items())
COLL=bands(EUP,'eu')+col(EU,'eu'); COLR=bands(JPP,'jp')+col(JP,'jp')
H=max(H,MAXB[0]+10)
html=f"""<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Two timelines</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS.replace('__H__',f'{H:.0f}')}</style></head><body><div class="wrap">
<h1>Two worlds, <em>one</em> timeline</h1>
<p class="sub">Medieval Europe on the left, Japan on the right, on the same scale. Click an event for a line of detail. Dotted gold links mark moments when the two units rhyme. The scale is stretched between 1050 and 1500, where most of both units sits.</p>
<div class="legend">{legend}<span><i class="sw" style="background:none;border-top:2px dotted var(--gold);height:0"></i>A connection worth knowing</span></div>
<div class="head"><h2 class="eu">Medieval Europe</h2><div class="mid">CE</div><h2 class="jp">Shogunate Japan</h2></div>
<div class="tl"><div class="colL">{COLL}</div><div class="spine">{ticks}{links}</div><div class="colR">{COLR}</div></div>
<p class="foot">Dates are the ones used in class. Where historians give a range (the Genpei War, the Mongol invasions, the Black Death), the first year is shown. The Edo period is dated from 1600 (Sekigahara) or 1603 (Ieyasu named shogun); both are used. Artworks are public domain, from Wikimedia Commons.</p>
</div><script>document.querySelectorAll('.ev').forEach(e=>e.addEventListener('click',()=>e.classList.toggle('open')));</script></body></html>"""
open('timelines.html','w').write(html); print('built',H, len(html)//1024,'KB')
