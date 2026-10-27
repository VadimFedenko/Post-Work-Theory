"""Minimal inline figures, without slide titles, provenance or commentary."""
from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import markdown
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/infographics/article'
AUDIT=ROOT/'research/article-infographics'
BUILD=AUDIT/'.build'
ARTICLE=ROOT/'article.md'
RAW=json.loads((ROOT/'data/societies.json').read_text('utf8'))['societies']
BYID={r['id']:r for r in RAW}
TECH=json.loads((AUDIT/'editorial-assessments.json').read_text('utf8'))['technology_records']
INK='#223a40';MUTED='#60747a';TEAL='#277f75'
COLORS=['#D69C46','#AD654D','#277F75','#5C9D85','#6874B5','#9C5D91']
plt.rcParams.update({'font.family':'Arial','svg.fonttype':'none','font.size':22})
FIGURES=[]
GEOMETRY=[]


def label(fig,x,y,value,size=22,color=INK,bold=False,ha='left'):
    return fig.text(x,y,value,fontsize=size,color=color,fontweight='bold' if bold else 'normal',ha=ha)


def save(fig,key,lang):
    fig.canvas.draw();renderer=fig.canvas.get_renderer();w,h=fig.canvas.get_width_height()
    texts=[]
    for t in fig.findobj(match=matplotlib.text.Text):
        if not t.get_visible() or not t.get_text():continue
        box=t.get_window_extent(renderer)
        assert box.x0>=-2 and box.y0>=-2 and box.x1<=w+2 and box.y1<=h+2,(key,t.get_text(),box.bounds)
        texts.append({'text':t.get_text(),'bbox':list(box.bounds)})
    stem=f'{key}-{lang}'
    fig.savefig(OUT/(stem+'.png'),dpi=125,facecolor='white')
    fig.savefig(OUT/(stem+'.svg'),facecolor='white')
    FIGURES.append({'key':key,'lang':lang,'png':f'assets/infographics/article/{stem}.png','svg':f'assets/infographics/article/{stem}.svg','width':w,'height':h})
    GEOMETRY.append({'file':stem,'texts':texts})
    plt.close(fig)


def technology(lang):
    fig=plt.figure(figsize=(12.8,6.56),dpi=125)
    ax=fig.add_axes([.27,.205,.705,.76])
    tiers=['Индустриальные','Роботы и ИИ','Планетарные\nи космические','Материя\nи сознание'] if lang=='ru' else ['Industrial','Robots and AI','Planetary\nand spacefaring','Matter\nand minds']
    ax.set_xlim(-3,103);ax.set_ylim(.5,4.6)
    ax.set_xticks([0,25,50,75,100]);ax.tick_params(axis='x',labelsize=20,length=0,pad=9)
    ax.set_yticks([1,2,3,4],tiers);ax.tick_params(axis='y',labelsize=22,length=0,pad=16)
    ax.grid(axis='x',color='#dfe7e9');ax.set_axisbelow(True)
    for s in ax.spines.values():s.set_visible(False)
    ys={}
    for tier in range(1,5):
        group=[r for r in TECH if r['tier']==tier]
        values=[100*(1-BYID[r['id']]['axis']['nonworking']) for r in group]
        for row,value,offset in zip(group,values,np.linspace(-.15,.15,len(group))):
            ys[row['id']]=tier+offset
            ax.scatter([value],[tier+offset],s=160,color=TEAL,edgecolors='white',linewidths=1.5,zorder=3)
        ax.scatter([np.median(values)],[tier],s=200,marker='D',color=INK,zorder=5)
    for rid,tier,y in [('walle-axiom',3,2.58),('dune-post-jihad-imperium',3,3.45),('culture-main',4,4.42),('diaspora-konishi',4,3.65)]:
        row=next(r for r in TECH if r['id']==rid);x=100*(1-BYID[rid]['axis']['nonworking'])
        ax.annotate(row['label_'+lang],(x,ys[rid]),xytext=(x,y),ha='center',fontsize=15,color=MUTED,arrowprops={'arrowstyle':'-','color':'#a9b9bd','lw':.8})
    label(fig,.62,.095,'Работает, %' if lang=='ru' else 'Working, %',22,ha='center')
    label(fig,.62,.025,'Ромб — медиана обществ' if lang=='ru' else 'Diamond: median',15,MUTED,ha='center')
    save(fig,'02-technology-work',lang)


def composition(lang):
    fig=plt.figure(figsize=(12.8,5.12),dpi=125)
    stages=['zero_variant','transition','post_work']
    names=['Трудовые','Частичный переход','Посттрудовые'] if lang=='ru' else ['Work-based','Partial transition','Post-work']
    legend=['1  Элиты с гарантиями','2  Элиты без гарантий','3  Распределённая власть с гарантиями','4  Распределённые активы без гарантий','5  Автономная система с гарантиями','6  Автономная система без гарантий'] if lang=='ru' else ['1  Elite control with guarantees','2  Elite control without guarantees','3  Distributed control with guarantees','4  Distributed assets without guarantees','5  Autonomous system with guarantees','6  Autonomous system without guarantees']
    def regime(r):
        if r['regime_primary']:return r['regime_primary']
        return (3 if r['axis']['control']>1/3 else 5 if r['axis']['control']<=-1/3 else 1)+(0 if r['axis']['guarantees']<0 else 1)
    for j,stage in enumerate(stages):
        rows=[r for r in RAW if r['post_work_assessment']['status']==stage]
        values=[sum(regime(r)==k for r in rows) for k in range(1,7)]
        center=.18+.32*j
        label(fig,center,.92,names[j],25,['#7B8896','#D69C46',TEAL][j],True,'center')
        label(fig,center,.85,str(len(rows))+(' обществ' if lang=='ru' else ' societies'),18,MUTED,ha='center')
        ax=fig.add_axes([.06+.32*j,.22,.24,.60])
        def value_text(p):
            if p<4.5:return ''
            return (f'{p:.1f}'.replace('.',',') if lang=='ru' else f'{p:.1f}')+'%'
        wedges,_,labels=ax.pie(values,colors=COLORS,startangle=180,counterclock=False,autopct=value_text,pctdistance=.65,
                              wedgeprops={'edgecolor':'white','linewidth':1.2},textprops={'fontsize':14,'fontweight':'bold','color':'white'})
        for i,t in enumerate(labels):
            if i in [0,3]:t.set_color(INK)
        ax.set_xlim(-1.15,1.15);ax.set_ylim(-1.15,1.15)
        ax.set_aspect('equal')
    for k in range(6):
        label(fig,.05+(k%2)*.475,.15-(k//2)*.06,legend[k],18,COLORS[k],True)
    save(fig,'05-regime-composition',lang)


def control(lang):
    fig=plt.figure(figsize=(9.6,3.28),dpi=125)
    ax=fig.add_axes([.35,.15,.58,.82])
    rows=[('Элиты','Elites',[1,2],COLORS[1]),('Автономный ИИ','Autonomous AI',[5,6],COLORS[4]),('Общество','Society',[3,4],COLORS[2])]
    for j,(_,_,ks,color) in enumerate(rows):
        group=[r for r in RAW if r['regime_primary'] in ks]
        p=100*sum(r['utopia_score']<0 for r in group)/len(group)
        ax.barh([2-j],[p],height=.45,color=color)
        ax.text(p+2,2-j,f'{p:.0f}%',va='center',fontsize=34,fontweight='bold',color=INK)
    ax.set_yticks([2,1,0],[r[0 if lang=='ru' else 1] for r in rows]);ax.tick_params(axis='y',labelsize=22,length=0,pad=18)
    ax.set_ylim(-.6,2.6);ax.set_xlim(0,103);ax.set_xticks([])
    for s in ax.spines.values():s.set_visible(False)
    label(fig,.63,.03,'Дистопии, %' if lang=='ru' else 'Dystopias, %',18,ha='center')
    save(fig,'07-control-dystopia',lang)


def guarantees():
    # Use the website's actual Columns markup and stylesheet; capture only the
    # mini chart, without the Insight title, explanation or notes.
    css=(ROOT/'src/fun-data.css').read_text('utf8')
    fonts=(ROOT/'src/styles.css').read_text('utf8').splitlines()[0]
    css=fonts+'\n'+css+'''\nhtml,body{margin:0;background:white;color:#25372f;font-family:'Golos Text',Arial,sans-serif}*{box-sizing:border-box}.fun-section{width:420px;padding:0;border:0}.fun-columns{width:420px;max-width:none;margin:0;min-height:218px}'''
    metrics=[]
    for without in [True,False]:
        group=[r for r in RAW if (r['axis']['guarantees']>=0)==without]
        count=sum(r['utopia_score']<=-.5 for r in group)
        metrics.append({'count':count,'total':len(group),'percent':round(100*count/len(group))})
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':900,'height':400},device_scale_factor=2)
        for lang in ['ru','en']:
            labels=['Без гарантий','С гарантиями'] if lang=='ru' else ['Without guarantees','With guarantees']
            dl='<dl class="fun-columns">'+''.join(f'<div><dt>{lab}</dt><dd class="fun-column"><span class="fun-column-number">{row["percent"]}%</span><i aria-hidden="true" style="height:{row["percent"]*1.4}px"></i></dd></div>' for lab,row in zip(labels,metrics))+'</dl>'
            content='<!doctype html><html><meta charset="utf-8"><style>'+css+'</style><div class="fun-section">'+dl+'</div></html>'
            (BUILD/f'guarantees-{lang}.html').write_text(content,encoding='utf8')
            page.set_content(content,wait_until='load',timeout=20000)
            page.evaluate('document.fonts.ready')
            node=page.locator('dl');stem=f'06-guarantees-{lang}'
            node.screenshot(path=str(OUT/(stem+'.png')))
            # The optional SVG uses the browser's measured bar and text positions.
            geometry=node.evaluate('''node=>{const o=node.getBoundingClientRect();return {width:o.width,height:o.height,bars:Array.from(node.querySelectorAll('i')).map(e=>{const r=e.getBoundingClientRect();return {x:r.x-o.x,y:r.y-o.y,w:r.width,h:r.height,color:getComputedStyle(e).backgroundColor}}),texts:Array.from(node.querySelectorAll('dt,span')).map(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {text:e.textContent,x:r.x-o.x+r.width/2,y:r.y-o.y+r.height/2,size:s.fontSize,font:s.fontFamily,weight:s.fontWeight,color:s.color,spacing:s.letterSpacing}})}}''')
            svg=ET.Element('svg',{'xmlns':'http://www.w3.org/2000/svg','viewBox':f'0 0 {geometry["width"]} {geometry["height"]}'})
            for bar in geometry['bars']:ET.SubElement(svg,'rect',{'x':str(bar['x']),'y':str(bar['y']),'width':str(bar['w']),'height':str(bar['h']),'fill':bar['color'],'rx':'2'})
            for t in geometry['texts']:
                e=ET.SubElement(svg,'text',{'x':str(t['x']),'y':str(t['y']),'text-anchor':'middle','dominant-baseline':'central','font-size':t['size'],'font-family':t['font'],'font-weight':t['weight'],'fill':t['color']})
                if t['spacing']!='normal':e.set('letter-spacing',t['spacing'])
                e.text=t['text']
            ET.ElementTree(svg).write(OUT/(stem+'.svg'),encoding='utf-8',xml_declaration=True)
            FIGURES.append({'key':'06-guarantees','lang':lang,'png':f'assets/infographics/article/{stem}.png','svg':f'assets/infographics/article/{stem}.svg','width':840,'height':round(geometry['height']*2),'website_component':'Columns','percentages':[r['percent'] for r in metrics]})
        browser.close()
    return metrics


def block(key,alt):
    return f'![{alt}](assets/infographics/article/{key}-ru.png)\n\n<details markdown="1">\n<summary>English</summary>\n\n![{alt} — English](assets/infographics/article/{key}-en.png)\n\n</details>'


def embed():
    source=ARTICLE.read_text('utf8')
    replacements={
        '01-infrastructure':'',
        '02-technology-work':block('02-technology-work','Технологии и работа'),
        '03-six-regimes':'![Координаты укладов](reference.png)',
        '04-elite-guarantees-examples':'',
        '05-work-postwork-matrices':block('05-regime-composition','Распределение по укладам'),
        '06-regime-dystopia':block('06-guarantees','Гарантии и дистопии'),
        '07-control-dystopia':block('07-control-dystopia','Контроль и дистопии'),
    }
    for old,replacement in replacements.items():
        pattern=r'!\[[^\]]*\]\(assets/infographics/article/'+re.escape(old)+r'-ru\.png\)\s*<details[^>]*>.*?</details>'
        source,n=re.subn(pattern,lambda _:replacement,source,count=1,flags=re.S)
        if n==0:
            current={'05-work-postwork-matrices':'05-regime-composition','06-regime-dystopia':'06-guarantees'}.get(old,old)
            if replacement and ('reference.png' if old=='03-six-regimes' else current+'-ru.png') not in source:
                raise ValueError('Insertion missing: '+old)
    source=re.sub(r'\n{4,}','\n\n\n',source)
    ARTICLE.write_text(source,encoding='utf8',newline='\n')


def preview():
    body=markdown.markdown(ARTICLE.read_text('utf8'),extensions=['tables','fenced_code','md_in_html'])
    css='body{margin:0;color:#203a42;background:#eef2f3;font:19px/1.75 Arial,sans-serif}main{max-width:1000px;padding:35px 35px 65px;margin:auto;background:white}img{max-width:100%;height:auto;display:block;margin:28px auto}img[src*="06-guarantees"]{width:420px}h1{line-height:1.25;margin-top:60px}a{color:#247f75}blockquote{border-left:3px solid #d49a43;padding-left:20px}details{margin:8px 0 24px}summary{cursor:pointer;font-size:14px;color:#62747a}@media(max-width:700px){main{padding:20px 12px;font-size:17px}}'
    (AUDIT/'article-preview.html').write_text('<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="../../"><title>Статья</title><style>'+css+'</style><main>'+body+'</main></html>',encoding='utf8')
    pairs=[]
    for key in dict.fromkeys(r['key'] for r in FIGURES):
        pairs.append('<div>'+''.join(f'<img src="../../assets/infographics/article/{key}-{lang}.png">' for lang in ['ru','en'])+'</div>')
    (AUDIT/'gallery.html').write_text('<!doctype html><html><meta charset="utf-8"><style>body{background:white;margin:24px}div{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:35px}img{max-width:100%;height:auto;align-self:center}</style>'+''.join(pairs)+'</html>',encoding='utf8')


def main():
    for path in [OUT,AUDIT,BUILD]:path.mkdir(parents=True,exist_ok=True)
    source_hash=hashlib.sha256((ROOT/'data/societies.json').read_bytes()).hexdigest()
    for lang in ['ru','en']:
        technology(lang);composition(lang);control(lang)
    metrics=guarantees()
    embed();preview()
    # Remove only obsolete assets made by the previous version of this builder.
    for key in ['01-infrastructure','03-six-regimes','04-elite-guarantees-examples','05-work-postwork-matrices','06-regime-dystopia']:
        for lang in ['ru','en']:
            for ext in ['png','svg']:
                file=OUT/f'{key}-{lang}.{ext}'
                assert file.resolve().is_relative_to(OUT.resolve())
                file.unlink(missing_ok=True)
    assert hashlib.sha256((ROOT/'data/societies.json').read_bytes()).hexdigest()==source_hash
    (AUDIT/'manifest.json').write_text(json.dumps({'input_sha256':source_hash,'figures':FIGURES,'reference':'reference.png','guarantees':metrics,'style':'minimal inline figures; no titles, sources or commentary'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (BUILD/'text-geometry.json').write_text(json.dumps(GEOMETRY,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'article':str(ARTICLE),'figures':len(FIGURES),'reference':'reference.png','guarantees':[m['percent'] for m in metrics]},ensure_ascii=False))


if __name__=='__main__':main()
