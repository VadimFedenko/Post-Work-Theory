"""Retrieve the actual display images served on work pages when masters fail."""
import concurrent.futures, copy, re, sys
from urllib.parse import quote, urljoin
import requests
from bs4 import BeautifulSoup
import collect_images as c
sys.stdout.reconfigure(encoding='utf8')
m=c.read(c.RESEARCH/'manifest.json');candidates=c.read(c.RESEARCH/'manual-candidates.json',{})
OVERRIDES={'Sleeper':'Sleeper (1973 film)','Casshern (2004)':'Casshern (film)','Freefall':'Freefall (webcomic)'}
QA={'Eden (Lem novel)','The Marching Morons','The Quantum Thief','Imperial Earth','Project Pope','The Visitors','Riverworld'}

def resolve(item):
    old=item.get('selection') or {};title=item['title']
    if title in QA:page='https://en.wikipedia.org/wiki/'+quote(title.replace(' ','_'))
    elif title in OVERRIDES:page='https://en.wikipedia.org/wiki/'+quote(OVERRIDES[title].replace(' ','_'))
    elif old.get('provider')=='wikipedia':page=old['source_page']
    else:return item['id'],None
    if title=='Electric Dreams: Autofac':return item['id'],None
    try:
        path=c.RESEARCH/'pages'/(c.sha(page.encode())+'.html')
        if path.exists():body=path.read_text(encoding='utf8')
        else:
            r=requests.get(page,headers={'User-Agent':c.UA},timeout=14);r.raise_for_status();body=r.text
            path.parent.mkdir(exist_ok=True);path.write_text(body,encoding='utf8')
        soup=BeautifulSoup(body,'html.parser')
        for img in soup.select('.infobox img'):
            src=img.get('src','');alt=img.get('alt','')
            if int(img.get('width',0))<120 or int(img.get('height',0))<120 or re.search('logo|icon|map|flag',src+' '+alt,re.I):continue
            src=urljoin(page,src)
            # Keep the actual served thumbnail hostname/URL; do not reconstruct
            # an inaccessible master from srcset's thumbnail_unscaled candidate.
            a=img.find_parent('a');filepage=urljoin(page,a.get('href','')) if a else old.get('image_description_page')
            sel={'provider':'wikipedia_display_image','title':OVERRIDES.get(title,old.get('title',title)),'source_url':src,'source_page':page,'image_description_page':filepage,'author':old.get('author'),'rights':old.get('rights') or {'status':'unknown_cover_copyright','license':None,'license_url':None,'notes':'Work article display image; source file description linked. No open license inferred.'},'scope_note':'Downloaded the available article display image. The inaccessible master URL is retained in the discovery history; this file is the input original for local resizing.','match_method':'Current work-page infobox image at its actual served display URL, verified as a decodable image on download.'}
            return item['id'],sel
    except Exception as e:c.log('display_image_error',title=title,error=str(e))
    return item['id'],None

items=[x for x in m['images'].values() if x['status']!='prepared' or x['title'] in QA]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    for identity,sel in pool.map(resolve,items):
        if sel:
            candidates[identity]={'selection':sel,'force_review':m['images'][identity]['title'] in QA}
            c.write(c.RESEARCH/'manual-candidates.json',candidates)
            print(m['images'][identity]['title'],'-> article display image',flush=True)
