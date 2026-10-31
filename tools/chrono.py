"""Side-by-side chronology (Medieval Europe | Shogunate Japan) for the Timeline page.
render(img) -> (css, html_fragment, height_px). img maps image keys ('tl-1066', 'tlb-eu1') to a path or data URI.
Mirrors sandbox/build_timelines.py; class names are prefixed (ctl, cev, ccard, ...) so nothing clashes with the site."""
import re

# kinds: pol (power and rule), war, faith, life (society, culture, economy)
EU=[(793,"Vikings raid Lindisfarne","Raids on monasteries begin two centuries of Viking pressure on Europe.","war"),
(800,"Charlemagne crowned emperor","The Pope crowns a Frankish king, tying royal power to the Church.","pol"),
(1066,"Battle of Hastings","William of Normandy defeats Harold. Feudalism and castles follow.","war"),
(1086,"Domesday Book","Every landholding in England recorded for the king.","pol"),
(1095,"Pope Urban II calls the First Crusade","The speech at Clermont promises forgiveness of sins.","faith"),
(1099,"Crusaders capture Jerusalem","The First Crusade ends in victory and massacre.","war"),
(1166,"Assize of Clarendon","Henry II orders juries of local men to report crimes: the beginnings of trial by jury.","pol"),
(1187,"Saladin retakes Jerusalem","Triggers the Third Crusade.","war"),
(1209,"King John excommunicated","Innocent III cuts the king off from the Church.","faith"),
(1215,"Magna Carta","The king accepts he is under the law. The Church also bans priests from trials by ordeal.","pol"),
(1291,"Fall of Acre","The last Crusader state is lost.","war"),
(1347,"The Black Death reaches Europe","Plague arrives in Sicily by ship; a third to a half of Europe dies by 1351.","life"),
(1351,"Statute of Labourers","English lords try to freeze wages after the plague.","life"),
(1381,"Peasants' Revolt","Wat Tyler's rebels march on London.","life"),
(1453,"Fall of Constantinople","Often taken as the end of the Middle Ages. Gutenberg's press is printing in the same decade.","war"),
(1485,"Battle of Bosworth","The Tudors take the English throne; medieval England ends.","pol"),]
JP=[(1160,"Taira clan dominates the court","After defeating the Minamoto in Kyoto, Taira no Kiyomori rules through the emperor. The Genpei War follows.","pol"),
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
JPP=[(794,1185,"Heian","jp1"),(1185,1333,"Kamakura","jp2"),(1336,1573,"Muromachi","jp2b"),(1573,1600,"Momoyama","jp2c"),(1600,1868,"Edo (Tokugawa)","jp3"),(1868,1925,"Meiji","jp4")]
LINKS=[(1066,1185,"Warriors take power. The Normans conquer England; the Minamoto take Japan from the court."),
(1215,1232,"Written law limits rulers and warriors. Magna Carta; the samurai law code."),
(1095,1274,"Holy war and foreign invasion. Crusaders go east; the Mongols come to Japan."),
(1347,1333,"Mid-1300s upheaval. The Black Death; the fall of Kamakura."),
(1453,1467,"The medieval order breaks up. Constantinople falls; Japan's civil wars begin."),]
SEG=[(780,1050,0.6),(1050,1500,3.0),(1500,1925,2.4)]
STAR={1066,1086,1095,1215,1347,1351,1381,1185,1192,1600,1603,1615,1635,1639,1853,1868,1873}
KN={'pol':'Power and rule','war':'War and conquest','faith':'Faith and the Church','life':'Society, culture and economy'}
NOTE={'After the unit':'<p class="bnote">Europe after 1500 — the Renaissance, the Reformation, the voyages of exploration — is not part of this unit. It is here only so Japan’s dates sit on the same scale. Notice that the Portuguese who reached Japan in 1543 were part of that story.</p>'}
TALL={'eu1','jp2c','jp2'}
TIP='<div class="tipbox"><b>Which dates to learn.</b> The starred years (&#9733;) are the ones worth writing in a Section B or C answer, because a date is the quickest way to make a point specific. The rest are here so you can see where things sit. <b>And in any exam:</b> every source comes with dates, in its caption or on the source itself. Use them. A date you can see on the paper is a free piece of evidence for a written answer, and a check on the dates you remember.</div>'
FOOT='<p class="cfoot">Dates are the ones used in class.</p>'

CSS="""
.chrono{min-width:0;max-width:100%;--pol:var(--navy);--war:var(--accent);--faith:#B8860B;--life:#3D6B5A;--cbg:var(--bg);margin-top:8px}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]) .chrono{--faith:#E0B84A;--life:#7FBF9E}}
:root[data-theme=dark] .chrono{--faith:#E0B84A;--life:#7FBF9E}
.chrono .tipbox{background:var(--surface);border:2px solid var(--navy);border-left:8px solid var(--gold);border-radius:10px;padding:10px 14px;font-size:14px;margin:12px 0 4px;max-width:900px;line-height:1.45}
.chrono .cleg{display:flex;gap:14px;flex-wrap:wrap;font-size:13px;color:var(--muted);margin:10px 0 0}
.chrono .sw{display:inline-block;width:14px;height:14px;border-radius:50%;vertical-align:middle;margin-right:6px}
.chrono .sw.k-pol{background:var(--pol)}.chrono .sw.k-war{background:var(--war)}.chrono .sw.k-faith{background:var(--faith)}.chrono .sw.k-life{background:var(--life)}
.chrono .linkkey{margin:4px 0 0 0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:4px 18px;font-size:12.5px;color:var(--muted)}
.chrono .linkkey b{display:inline-grid;place-items:center;width:18px;height:18px;border-radius:50%;background:var(--gold);color:#1C2333;font-size:11px;margin-right:4px}
.chrono .chead{display:grid;grid-template-columns:1fr 220px 1fr;align-items:end;position:sticky;top:0;background:var(--cbg);z-index:5;padding:10px 0 8px;border-bottom:2px solid var(--navy);margin-top:10px}
.chrono .chead h2{font-family:var(--display);font-size:22px;margin:0}.chrono .chead .eu{color:var(--eu);text-align:right;padding-right:14px}.chrono .chead .jp{color:var(--jp);padding-left:14px}.chrono .chead .mid{text-align:center;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.chrono .ctl{position:relative;display:grid;grid-template-columns:1fr 220px 1fr;margin-bottom:40px}
.chrono .colL,.chrono .colR,.chrono .spine{position:relative}
.chrono .spine::before{content:"";position:absolute;left:50%;top:0;bottom:0;width:2px;background:var(--line);transform:translateX(-50%)}
.chrono .ctick{position:absolute;left:0;right:0;height:0}.chrono .ctick span{position:absolute;z-index:3;left:50%;transform:translate(-50%,-50%);background:var(--cbg);padding:1px 5px;font-family:var(--display);font-weight:700;color:var(--navy);font-size:16px;letter-spacing:.02em;color:var(--navy);border:1.5px solid var(--navy);border-radius:7px;opacity:1}
.chrono .band{position:absolute;left:0;right:0;border-radius:8px;pointer-events:none;background-size:100% auto;background-repeat:repeat-y;background-position:center top;overflow:hidden}
.chrono .band.tall{background-size:cover;background-repeat:no-repeat;background-position:center}
.chrono .band.eu{border-left:4px solid color-mix(in srgb,var(--eu) 40%,transparent)}
.chrono .band.jp{border-right:4px solid color-mix(in srgb,var(--jp) 40%,transparent)}
.chrono .band::before{content:"";position:absolute;inset:0;border-radius:8px;opacity:.86}
.chrono .band.eu::before{background:color-mix(in srgb,var(--eu) 8%,var(--cbg));-webkit-mask-image:linear-gradient(90deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.92) 45%,rgba(0,0,0,1) 100%);mask-image:linear-gradient(90deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.92) 45%,rgba(0,0,0,1) 100%)}
.chrono .band.jp::before{background:color-mix(in srgb,var(--jp) 8%,var(--cbg));-webkit-mask-image:linear-gradient(270deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.92) 45%,rgba(0,0,0,1) 100%);mask-image:linear-gradient(270deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.92) 45%,rgba(0,0,0,1) 100%)}
.chrono .band.none{background-image:repeating-linear-gradient(135deg,transparent 0 14px,rgba(0,0,0,.035) 14px 16px)}.chrono .band.none::before{display:none}
.chrono .band>span{position:absolute;top:6px;font-size:10px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:var(--muted);writing-mode:vertical-rl;z-index:1}
.chrono .band.eu>span{left:6px;transform:rotate(180deg)}.chrono .band.jp>span{right:6px}
.chrono .band.short>span{writing-mode:horizontal-tb;transform:none;top:4px}.chrono .band.short.jp>span{right:8px}.chrono .band.short.eu>span{left:8px}
.chrono .bnote{position:absolute;left:14px;right:28px;top:50%;transform:translateY(-50%);margin:0;padding:12px 14px;font-size:12.5px;line-height:1.5;color:var(--muted);background:color-mix(in srgb,var(--cbg) 85%,transparent);border:1px dashed color-mix(in srgb,var(--eu) 40%,transparent);border-radius:8px;z-index:1}
.chrono .cev{position:absolute;display:flex;align-items:flex-start;gap:10px;width:calc(100% - 24px);z-index:1}
.chrono .cev.eu{right:0;flex-direction:row-reverse;text-align:right}.chrono .cev.jp{left:24px}
.chrono .cev.open{z-index:10}
.chrono .ccard{display:flex;gap:10px;align-items:flex-start;background:var(--surface);border:2px solid var(--pol);border-left-width:6px;border-radius:10px;padding:7px 11px;max-width:380px;box-shadow:0 1px 2px rgba(0,0,0,.06);cursor:pointer;transition:transform .12s;color:var(--ink);font:inherit;text-align:inherit}
.chrono .cev.eu .ccard{flex-direction:row-reverse;border-left-width:2px;border-right-width:6px}
.chrono .cev.k-pol .ccard{border-color:var(--pol)}.chrono .cev.k-war .ccard{border-color:var(--war)}.chrono .cev.k-faith .ccard{border-color:var(--faith)}.chrono .cev.k-life .ccard{border-color:var(--life)}
.chrono .ccard img{width:44px;height:44px;border-radius:8px;object-fit:cover;flex:none;border:1px solid var(--line)}
.chrono .ccard b{display:block;font-size:14.5px;color:var(--ink);font-weight:700}.chrono .cev:not(.star) .ccard b{font-weight:600;color:var(--muted)}
.chrono .ccard span{display:none;font-size:12.5px;color:var(--muted);margin-top:2px;line-height:1.4}
.chrono .cev.open .ccard span{display:block}
.chrono .cev.open .ccard{box-shadow:0 10px 28px -8px rgba(0,0,0,.35)}
.chrono .cev.star .ccard{box-shadow:0 2px 6px rgba(0,0,0,.08)}
.chrono .ccard:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.chrono .clink{position:absolute;left:50%;width:2px;border-left:2px dotted var(--gold);z-index:1}
.chrono .clink i{position:absolute;width:10px;height:10px;border-radius:50%;background:var(--gold);transform:translate(-50%,-50%)}
.chrono .clink em{position:absolute;left:50%;transform:translate(-50%,-50%);width:20px;height:20px;border-radius:50%;background:var(--gold);color:#1C2333;font-size:11px;font-weight:700;font-style:normal;display:grid;place-items:center;line-height:1;z-index:4;border:2px solid var(--cbg)}
.chrono .ylab{position:absolute;transform:translateY(-50%);font-family:var(--display);font-weight:700;font-size:13.5px;color:var(--muted);white-space:nowrap;z-index:2;background:var(--cbg);padding:0 3px;border-radius:4px}
.chrono .ylab.eu{right:calc(50% + 28px)}.chrono .ylab.jp{left:calc(50% + 28px)}
.chrono .ylab.star{color:var(--ink);font-size:15px}
.chrono .cfoot{font-size:12px;color:var(--muted);margin-top:16px;line-height:1.45}
@media(max-width:1000px){.chrono .chead,.chrono .ctl{grid-template-columns:1fr 210px 1fr}.chrono .ccard{max-width:none}.chrono .band>span{display:none}.chrono .ccard b{font-size:13px}.chrono .ccard img{width:36px;height:36px}.chrono .bnote{left:8px;right:8px;font-size:11.5px}}
@media(max-width:700px){.chrono .cscroll{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 -16px;padding:0 16px}.chrono .chead,.chrono .ctl{min-width:680px}.chrono .chead{position:static}.chrono .phone{display:block}}
.chrono .phone{display:none;font-size:13px;color:var(--muted);margin:10px 0 0}
"""

def y(yr):
    out=0
    for a,b,k in SEG:
        if yr<=a: break
        out+=(min(yr,b)-a)*k
    return out

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('"','&quot;')

def render(img):
    H=y(1925); MAXB=[0]; YEARS=[]
    def col(evs,side):
        out=[]; last=-99; lasth=0
        for yr,t,d,k in evs:
            th=img.get(f'tl-{yr}'); im=f'<img src="{th}" alt="">' if th else ''
            hgt=60 if th else 34
            top=y(yr)
            if top-last<lasth+6: top=last+lasth+6
            last=top; lasth=hgt; MAXB[0]=max(MAXB[0],top+hgt)
            st=' star' if yr in STAR else ''
            out.append(f'<div class="cev {side} k-{k}{st}" style="top:{top:.0f}px"><button type="button" class="ccard" aria-expanded="false">{im}<div><b>{esc(t)}</b><span>{esc(d)}</span></div></button></div>')
            YEARS.append((side,yr,top+(30 if th else 17),bool(st)))
        return ''.join(out)
    cL=col(EU,'eu'); cR=col(JP,'jp')
    def bands(ps,side):
        out=[]
        for a,b,n,k in ps:
            bg=img.get(f'tlb-{k}') if k else None
            cls='band '+side+(' tall' if k in TALL else '')+('' if k else ' none')+(' short' if y(b)-y(a)<90 else '')
            hgt=(max(MAXB[0],H) if b>=1925 else y(b))-y(a)
            out.append(f'<div class="{cls}" style="top:{y(a):.0f}px;height:{hgt:.0f}px;{("background-image:url("+bg+")") if bg else ""}"><span>{n}</span>{NOTE.get(n,"")}</div>')
        return ''.join(out)
    COLL=bands(EUP,'eu')+cL; COLR=bands(JPP,'jp')+cR
    ticks=''.join(f'<div class="ctick" style="top:{y(yr):.0f}px"><span>{yr}</span></div>' for yr in range(800,1901,100))
    links=''.join(f'<div class="clink" title="{esc(d)}" style="top:{min(y(a),y(b)):.0f}px;height:{abs(y(a)-y(b)):.0f}px"><i style="top:{(y(a)-min(y(a),y(b))):.0f}px"></i><i style="top:{(y(b)-min(y(a),y(b))):.0f}px"></i><em style="top:{(abs(y(a)-y(b))/2):.0f}px">{n+1}</em></div>' for n,(a,b,d) in enumerate(LINKS))
    linkkey=''.join(f'<li><b>{n+1}</b> {esc(d)}</li>' for n,(a,b,d) in enumerate(LINKS))
    legend=''.join(f'<span><i class="sw k-{k}"></i>{v}</span>' for k,v in KN.items())
    def yrs(side):
        return ''.join(f'<span class="ylab {side}{" star" if st else ""}" style="top:{yy:.0f}px">{"&#9733;" if st else ""}{yr}</span>' for sd,yr,yy,st in sorted([v for v in YEARS if v[0]==side],key=lambda v:v[2]))
    YL=yrs('eu')+yrs('jp')
    H=max(H,MAXB[0]+10)
    html=(f'<div class="chrono">{TIP}'
          f'<div class="cleg">{legend}<span><i class="sw" style="background:none;border-top:2px dotted var(--gold);height:0;border-radius:0"></i>Numbered gold links are connections worth knowing:</span></div>'
          f'<ol class="linkkey">{linkkey}</ol>'
          f'<p class="phone">Swipe sideways to see both columns. A laptop screen shows this page best.</p><div class="cscroll"><div class="chead"><h2 class="eu">Medieval Europe</h2><div class="mid">CE</div><h2 class="jp">Shogunate Japan</h2></div>'
          f'<div class="ctl" style="height:{H:.0f}px"><div class="colL">{COLL}</div><div class="spine">{ticks}{links}{YL}</div><div class="colR">{COLR}</div></div></div>'
          f'{FOOT}</div>')
    return CSS.strip(), html, H
