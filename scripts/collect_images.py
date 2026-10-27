"""Resumable cover research. Only the assets overlay may change society data.

Sources are fetched once into a persistent cache; downloads retain original bytes.
Run --discover, --download, --sync, --validate separately or --all to resume.
"""
from __future__ import annotations
import argparse, concurrent.futures, copy, datetime as dt, difflib, hashlib, html
import io, json, os, re, sys, threading, time, unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import quote, unquote, urlparse
import requests
from PIL import Image, ImageOps, ImageStat

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / 'assets' / 'images'
RESEARCH = ROOT / 'research' / 'images'
UA = 'SocietyCoverResearch/1.0 (local editorial research; bounded 674-work catalogue)'
TODAY = '2026-10-17'
LOCK = threading.RLock()
SESSION = threading.local()

def read(p, default=None):
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default

def write(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    temp = p.with_suffix(p.suffix + '.tmp')
    temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(p)

def sha(b): return hashlib.sha256(b).hexdigest()
def rel(p): return p.relative_to(ROOT).as_posix()
def now(): return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
def clean(t): return html.unescape(re.sub('<[^>]+>', '', t or '')).strip()
def norm(t):
    t = unicodedata.normalize('NFKD', t.replace('\ufffd', "'").replace('’', "'")).encode('ascii','ignore').decode().lower()
    t = re.sub(r'\([^)]*\)', '', t)
    return re.sub('[^a-z0-9]', '', re.sub(r'^(the|a|an) ', '', t))
def similarity(a,b): return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()

def get(url, params=None, binary=False, cache=True):
    key = sha((url + json.dumps(params or {}, sort_keys=True)).encode())
    cp = RESEARCH / 'cache' / (key + ('.bin' if binary else '.json'))
    if cache and cp.exists():
        if binary: return cp.read_bytes()
        return read(cp)
    if not hasattr(SESSION,'http'):
        SESSION.http = requests.Session()
        SESSION.http.headers['User-Agent'] = UA
    err = None
    attempts=1 if binary else 2
    for attempt in range(attempts):
        try:
            r = SESSION.http.get(url, params=params, timeout=(8, 18) if binary else (8, 20))
            if r.status_code in (429, 503):
                if attempt < attempts-1: time.sleep(min(8, int(r.headers.get('Retry-After','2')) if r.headers.get('Retry-After','').isdigit() else 2) * (attempt+1)); continue
            r.raise_for_status()
            value = r.content if binary else r.json()
            if cache:
                cp.parent.mkdir(parents=True,exist_ok=True)
                if binary: cp.write_bytes(value)
                else: write(cp,value)
            return value
        except Exception as e:
            err=e
            if attempt<attempts-1:time.sleep(.7*(attempt+1))
    raise RuntimeError(f'{url}: {err}')

def log(event, **kw):
    RESEARCH.mkdir(parents=True,exist_ok=True)
    with LOCK, (RESEARCH/'events.jsonl').open('a',encoding='utf8') as f:
        f.write(json.dumps({'at':now(),'event':event,**kw},ensure_ascii=False)+'\n')

def baseline():
    RESEARCH.mkdir(parents=True,exist_ok=True)
    p=RESEARCH/'baseline-societies.json'
    if not p.exists():
        original=(ROOT/'data/societies.json').read_bytes()
        p.write_bytes(original)
        files=['data/decisions.json','data/sources.json','data/comparisons.json','data/candidates.json','data/candidates-expansion.json','research/methodology.md','research/completion-review.md','research/completion-review.json']
        write(RESEARCH/'baseline-hashes.json',{'created_on':TODAY,'societies_original_sha256':sha(original),'files':{x:sha((ROOT/x).read_bytes()) for x in files}})
        log('baseline_saved',records=890)
    return read(p)['societies']

# A cover identifies its work/continuity, never a fictional census or an enacted ending.
# Curated aliases use a related volume/collection only when it contains the work.
ALIASES = {
 'Twilight':'Twilight (Campbell short story)',
 'Genesis':'Genesis (Anderson novel)',
 'The Culture':'Consider Phlebas', 'Manna':'Manna (novel)',
 'The Evitable Conflict':'I, Robot', 'Noon Universe':'Noon: 22nd Century',
 'The Midas Plague':'Midas World', 'The Man Who Ate the World':'Midas World',
 'Looking Backward from the Year 2000':'Looking Backward from the Year 2000',
 'The Star Diaries: Twenty-fourth Voyage':'The Star Diaries',
 'The Golden Age trilogy':'The Golden Age (Wright novel)',
 'The Void Trilogy':'The Dreaming Void', 'Gridlinked / Polity background':'Gridlinked',
 'Uglies / Pretties':'Uglies', 'The Animatrix: The Second Renaissance':'The Animatrix',
 'The Lion of Comarre':'The Lion of Comarre and Against the Fall of Night',
 'Logan\ufffds Run':"Logan's Run (film)", 'Logan’s Run':"Logan's Run (film)",
 'Outer Wilds: Echoes of the Eye':'Outer Wilds',
 'Wyst: Alastor 1716':'Wyst: Alastor 1716',
 'A Psalm for the Wild-Built / A Prayer for the Crown-Shy':'A Prayer for the Crown-Shy',
 "Don't Bite the Sun / Drinking Sapphire Wine":"Don't Bite the Sun",
 'Dunno in Sun City / Dunno on the Moon':'Dunno in Sun City',
 'Dawn / Lilith’s Brood':"Dawn (Butler novel)",
 'Twinmaker / Jump':'Twinmaker', 'Marvel Cinematic Universe: Black Panther':'Black Panther (film)',
 'Marvel: Fantastic Four':'Fantastic Four', 'Marvel: X-Men':'House of X and Powers of X',
 'Marvel: Spider-Man 2099':'Spider-Man 2099',
 'Star Wars: Andor':'Andor (TV series)', 'Star Wars: The Mandalorian':'The Mandalorian',
 'Transformers: Beast Wars':'Beast Wars: Transformers', 'AppleSeed Alpha':'Appleseed Alpha',
 'Doraemon: Nobita and the Steel Troops':'Doraemon: Nobita and the New Steel Troops—Winged Angels',
 'Rebuild of Evangelion':'Evangelion: 3.0+1.0 Thrice Upon a Time',
 'NieR:Automata':'Nier: Automata', 'NieR Replicant':'Nier', 'NieR Reincarnation':'Nier Reincarnation',
 'The Bicentennial Man':'The Bicentennial Man', 'I, Robot':'I, Robot (film)',
 'Beyond the Aquila Rift':'Beyond the Aquila Rift (Love, Death & Robots)',
 'Zima Blue':'Zima Blue (Love, Death & Robots)',
 'Automata':'Automata (2014 film)', 'Robots':'Robots (2005 film)',
 'The Creator':'The Creator (2023 film)', 'The Island':'The Island (2005 film)',
 'The Congress':'The Congress (2013 film)', 'Westworld (1973)':'Westworld (film)',
 'Westworld':'Westworld (TV series)', 'Battlestar Galactica':'Battlestar Galactica (2004 TV series)',
 'Humans':'Humans (TV series)', 'Brave New World (2020)':'Brave New World (2020 TV series)',
 'Eden':'Eden (2021 TV series)', 'Metropolis':'Metropolis (2001 film)',
 'BLAME!':'Blame!', 'Aria':'Aria (manga)', 'Harmony':'Harmony (2015 film)',
 'Phoenix: Resurrection':'Phoenix (manga)', 'Phoenix: Future':'Phoenix (manga)',
 'Neo Tokyo: Construction Cancellation Order':'Neo Tokyo (film)',
 'From the New World':'From the New World (novel)', 'Pluto':'Pluto (manga)',
 'The Uncertain: Last Quiet Day / Light at the End':'The Uncertain',
 'Sid Meier’s Alpha Centauri':'Sid Meier\'s Alpha Centauri',
 'Sid Meier’s Alpha Centauri: Alien Crossfire':'Alien Crossfire',
 'Startopia / Spacebase Startopia':'Startopia',
 'Traveller: The New Era / Traveller 1248':'Traveller: The New Era',
 'The Metabaron / The Metabarons: Second Cycle':'The Metabarons',
 'Valerian and Laureline: Welcome to Alflolol':'Welcome to Alflolol',
 'Yoko Tsuno: The Curious Trio':'The Curious Trio',
 'Yoko Tsuno: The Forge of Vulcan':'The Forge of Vulcan',
 'Yoko Tsuno: The Three Suns of Vinea':'The Three Suns of Vinea',
 'Yoko Tsuno: The Archangels of Vinea':'The Archangels of Vinea',
 'GURPS Reign of Steel':'GURPS Reign of Steel', 'Logan’s Run (television)':"Logan's Run (TV series)",
 'Foundation’s Edge / Foundation and Earth':"Foundation's Edge",
 'The Cyberiad: The Seventh Sally':'The Cyberiad', 'City: The Simple Way':'City (novel)',
 'Useless Hands / Les condamnés à mort':'Useless Hands',
 'Jean le Flambeur series':'The Causal Angel', 'Quantum Evolution / The Quantum War':'The Quantum War',
 'Revenger / Bone Silence':'Bone Silence', 'The Night’s Dawn Trilogy':'The Reality Dysfunction',
 'The Night’s Dawn Trilogy / The Confederation Handbook':'The Confederation Handbook',
 'Salvation Sequence':'Salvation (novel)', 'Pandora’s Star / Judas Unchained':"Pandora's Star",
 'Metaplanetary / Superluminal':'Metaplanetary', 'Software / Wetware':'Software (novel)',
 'Hyperion / The Fall of Hyperion':'Hyperion (Simmons novel)',
 'Endymion / The Rise of Endymion':'The Rise of Endymion', 'Ilium / Olympos':'Ilium (novel)',
 'The Toll / Gleanings':'The Toll (Shusterman novel)', 'Impostors / Mirror’s Edge':'Impostors (novel)',
 'The Reproductive System / Mechasm':'The Reproductive System',
 'Natural State / Masters of Evolution':'Natural State',
 'The Stone Canal / The Cassini Division':'The Cassini Division',
 'Marrow / Great Ship':'Marrow (novel)', 'The Bull’s Hour':"The Bull's Hour",
 'Year 4338: Petersburg Letters':'The Year 4338', 'The City Dwellers / Twilight of the City':'The City Dwellers',
 'Logan’s Run / Logan’s Run: Last Day':"Logan's Run (novel)",
 'Orion’s Arm':"Orion's Arm", 'Orion\ufffds Arm':"Orion's Arm",
}
# Explicit per-record overrides prevent visually conflating important adaptations.
RECORD_TITLES={
 'lem-eden-doubler-automation-zero':'Eden (Lem novel)',
 'fallout-prewar-appalachia':'Fallout 76', 'fallout-vaultcity-citizen-provision':'Fallout 2',
 'star-trek-federation-core':'Star Trek: The Next Generation',
 'cyberpunk-night-city':'Cyberpunk 2077', 'ghostshell-manga-unmanned-capitalism':'Ghost in the Shell (manga)',
 'metropolis-1927-industrial-zero':'Metropolis (1927 film)',
 'astro2009-metrocity-robot-economy':'Astro Boy (film)',
 'doraemon-future-earth-robot-support':"Doraemon: Nobita's Secret Gadget Museum",
 'doraemon-mechatopia-robot-class-zero':'Doraemon: Nobita and the New Steel Troops—Winged Angels',
}
EXPECTED_AUTHORS={'Apex':'Naam','The Last Human':'Bacon','Hum':'Phillips','Genesis':'Anderson',
 'Manna':'Brain','Twilight':'Campbell','Border Guards':'Egan','Crystal Nights':'Egan',
 'The Merchants of Venus':'Pohl','Dogs of War':'Tchaikovsky',
 'The Last Angel':'ProximalFlame', 'A.D. 2000':'Fuller',
 'Freefall':'Stanley','All Tomorrow\'s Parties':'Gibson','Day Zero':'Cargill',
 'Autofac':'Dick','The Terraformers':'Newitz','Machinehood':'Divya','The Employees':'Ravn',
 'Set My Heart to Five':'Stephenson','Impostors':'Westerfeld','The City Dwellers':'Platt',
 'The Expert System\'s Champion':'Tchaikovsky','Lord of All Things':'Eschbach',
 'Tomorrow and Tomorrow':'Sheffield','Ultima Thule':'Reynolds','The Visitors':'Simak',
 'Spectrum':'Lukyanenko','The Humans':'Haig','The Million':'Schroeder'}

def title_for(r):
    w=r['work'].replace('\ufffd', '’')
    return RECORD_TITLES.get(r['id'],ALIASES.get(w,ALIASES.get(r['work'],w))).replace('’',"'")

def plans():
    records=baseline(); groups={}
    for r in records:
        title=title_for(r)
        # Distinguish original manga, screen adaptations and games with identical names.
        media=r['media']; kind='game' if 'game' in media else 'tv' if 'tv' in media or ('cartoon' in media and 'movie' not in media and 'anime' not in media) else 'movie' if 'movie' in media else 'anime' if 'anime' in media else 'manga' if 'manga' in media else 'comic' if 'comic' in media else 'tabletop' if 'tabletop' in media else 'book'
        key=title+'|'+kind
        groups.setdefault(key,{'title':title,'kind':kind,'record_ids':[],'works':[],'media':set(),'source_ids':set(),'scope':[]})
        g=groups[key];g['record_ids'].append(r['id']);g['media'].update(media);g['source_ids'].update(r['source_ids']);g['scope'].append(r['scope'])
        if r['work'] not in g['works']:g['works'].append(r['work'])
    for key,g in groups.items():
        g['id']='img-'+re.sub('[^a-z0-9]+','-',g['title'].lower()).strip('-')[:68]+'-'+sha(key.encode())[:8]
        g['media']=sorted(g['media']);g['source_ids']=sorted(g['source_ids'])
        g['priority']=0 if g['kind'] in ('game','movie','tv','anime','manga','comic') else 1
    result=sorted(groups.values(),key=lambda g:(g['priority'], min(records.index(next(r for r in records if r['id']==i)) for i in g['record_ids'])))
    write(RESEARCH/'plan.json',{'schema_version':'1.0','groups':result})
    return result

def wiki_candidates(g,sources):
    title=g['title']; kind=g['kind']; candidates=[]
    # Exact qualified pages precede an ambiguous unqualified word.
    qualifiers={'game':['video game','2000 video game','2007 video game'], 'movie':['film'], 'tv':['TV series','television series'], 'anime':['TV series','anime','manga'], 'manga':['manga'],'comic':['comics','comic book'],'book':['novel','short story','novella','book'],'tabletop':['role-playing game']}[kind]
    for q in qualifiers:candidates.append(f'{title} ({q})')
    if kind in ('movie','tv','anime'):
        years=re.findall(r'\b(?:19|20)\d\d\b',' '.join(s['continuity'] for s in g['scope']))
        for y in dict.fromkeys(years):
            candidates.insert(0,f'{title} ({y} '+('TV series' if kind=='tv' else 'film')+')')
    candidates.append(title)
    for sid in g['source_ids']:
        u=sources[sid].get('url','')
        if 'en.wikipedia.org/wiki/' in u:
            t=unquote(u.split('/wiki/',1)[1].split('#')[0]).replace('_',' ')
            if not t.startswith(('List of','Category:')) and similarity(t,title)>.65:candidates.insert(0,t)
    # Episode pages often have an image; series key art remains a labeled fallback.
    for prefix in ['Doctor Who: ','Black Mirror: ','Stargate SG-1: ','Rick and Morty: ','Futurama: ','Love, Death & Robots: ','Electric Dreams: ','The Twilight Zone: ','The Outer Limits: ']:
        if title.startswith(prefix):
            ep=title[len(prefix):]; series=prefix[:-2]
            candidates=[ep+' ('+series+')',ep]+candidates+[series]
    if title.startswith('Star Wars: '):candidates.append(title[len('Star Wars: '):])
    return list(dict.fromkeys(candidates))

def wiki_bulk(titles):
    out={}; desired=list(dict.fromkeys(titles)); known={}
    # Reuse per-page results even if a resumed batch has different boundaries.
    for path in (RESEARCH/'cache').glob('*.json'):
        d=read(path,{})
        if not isinstance(d,dict):continue
        q=d.get('query',{}); ps=q.get('pages',[])
        if not isinstance(ps,list):continue
        page_map={p['title']:p for p in ps if p.get('ns')==0 or p.get('missing')}
        known.update(page_map)
        remap={x['from']:x['to'] for x in q.get('normalized',[])+q.get('redirects',[])}
        for t in remap:
            target=t;seen=set()
            while target in remap and target not in seen:seen.add(target);target=remap[target]
            if target in page_map:known[t]=page_map[target]
    for t in desired:
        if t in known:out[t]=known[t]
    items=[t for t in desired if t not in out]
    print(f'Wikipedia cached pages {len(out)}/{len(desired)}',flush=True)
    def chunk_query(chunk):
        try:
            d=get('https://en.wikipedia.org/w/api.php',{'action':'query','format':'json','formatversion':2,'redirects':1,'prop':'pageimages|extracts|pageprops|info','inprop':'url','piprop':'name|original','pilicense':'any','exintro':1,'explaintext':1,'exchars':650,'titles':'|'.join(chunk)})
            q=d.get('query',{}); pages={p['title']:p for p in q.get('pages',[])}
            remap={x['from']:x['to'] for x in q.get('normalized',[])+q.get('redirects',[])}
            result={}
            for t in chunk:
                target=t;seen=set()
                while target in remap and target not in seen:seen.add(target);target=remap[target]
                if target in pages:result[t]=pages[target]
            return result
        except Exception as e:
            log('wiki_batch_error',error=str(e),titles=chunk)
            return {}
    chunks=[items[i:i+40] for i in range(0,len(items),40)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for i,result in enumerate(pool.map(chunk_query,chunks)):
            out.update(result)
            print(f'Wikipedia metadata {min((i+1)*40,len(items))}/{len(items)}',flush=True)
    return out

def wiki_pick(g,pages):
    matches=[]
    for rank,t in enumerate(g['wiki_candidates']):
        p=pages.get(t,{})
        if not p.get('original') or p.get('missing') or 'disambiguation' in p.get('pageprops',{}):continue
        name=p.get('pageimage','');url=p['original']['source'].split('?')[0]
        if name.lower().endswith(('.svg','.webm','.ogg','.pdf','.tif','.tiff')) or re.search(r'logo|wordmark|signature|flag_of|map_of',name,re.I):continue
        extract=p.get('extract','').lower(); short=p.get('pageprops',{}).get('wikibase-shortdesc','').lower(); txt=extract+' '+short
        author=EXPECTED_AUTHORS.get(re.sub(r'\s*\([^)]*\)','',g['title']))
        if g['kind']=='book' and author and author.lower() not in txt:continue
        if g['kind']=='book' and 'short_story' in g['media'] and g['title'] not in ALIASES.values() and not any(z in txt for z in ['short story','short-story','novella','anthology','collection','stories','magazine']):continue
        if not any(x in txt for x in ['novel','story','stories','film','series','game','comic','manga','fiction','anthology','magazine','book','anime','webcomic','television']):continue
        # Exclude creator portraits, real-world places and unrelated subjects.
        if any(x in short for x in ['born ','writer','politician','mathematician','municipality','city in','town in','chemical element']):continue
        score=80-rank*.3+similarity(g['title'],p['title'])*10
        medium_terms={'book':['novel','short story','anthology','collection','book'],'game':['video game'],'movie':['film'],'tv':['television','tv series'],'anime':['anime','manga','animated'],'manga':['manga'],'comic':['comic'],'tabletop':['role-playing','tabletop']}[g['kind']]
        if g['kind']=='movie' and 'anime' in g['media']:medium_terms+=['anime','theatrical']
        if any(x in txt for x in medium_terms):score+=15
        elif g['kind'] in ('game','movie','tv','manga','comic'):continue
        if p['original']['height']>p['original']['width']:score+=4
        if similarity(g['title'],p['title'])<.5:score-=14
        matches.append((score,p))
    if not matches:return None
    _,p=max(matches,key=lambda x:x[0])
    return {'provider':'wikipedia','title':p['title'],'source_url':p['original']['source'].split('?')[0], 'source_page':p.get('fullurl','https://en.wikipedia.org/wiki/'+quote(p['title'].replace(' ','_'))),'file_title':'File:'+p['pageimage'],'width':p['original']['width'],'height':p['original']['height'],'description':p.get('extract',''),'match_method':'Curated work alias / qualified title and medium match; source introduction retained in discovery cache.'}

def tv_query(g):
    title=g['title']; kind=g['kind']
    if kind not in ('tv','anime'):return None
    if '(Love, Death & Robots)' in title:return 'Love, Death & Robots'
    if title=='Star Trek: The Original Series':return 'Star Trek'
    # For an episode without usable screen art, use its actual series poster.
    for prefix,show in [('Doctor Who: ','Doctor Who'),('Black Mirror: ','Black Mirror'),('Rick and Morty: ','Rick and Morty'),('Stargate SG-1: ','Stargate SG-1'),('Futurama: ','Futurama'),('Love, Death & Robots: ','Love, Death & Robots'),('Electric Dreams: ',"Philip K. Dick's Electric Dreams"),('The Twilight Zone: ','The Twilight Zone'),('The Outer Limits: ','The Outer Limits')]:
        if title.startswith(prefix):return show
    if '(film)' in title or re.search(r'\(\d{4} film\)',title):return None
    return re.sub(r'\s*\([^)]*\)','',title).replace('Beast Wars: Transformers','Beast Wars').replace('Logan\'s Run',"Logan's Run")

def tv_pick(g):
    query=tv_query(g)
    if not query:return None
    ds=get('https://api.tvmaze.com/search/shows',{'q':query})
    ds=[x['show'] for x in ds if x['show'].get('image') and norm(x['show']['name'])==norm(query)]
    if not ds:return None
    def score(d):
        val=similarity(d['name'],query)*100
        scope=' '.join(s['continuity'] for s in g['scope'])
        if '2004' in scope and (d.get('premiered') or '').startswith('2004'):val+=40
        if '2020' in scope and (d.get('premiered') or '').startswith('2020'):val+=40
        if query=='Doctor Who' and (d.get('premiered') or '').startswith('2005'):val+=10
        if query=='The Twilight Zone' and (d.get('premiered') or '').startswith('1959'):val+=10
        if query=='The Outer Limits' and (d.get('premiered') or '').startswith('1995'):val+=10
        return val
    d=max(ds,key=score)
    return {'provider':'tvmaze','title':d['name'],'source_url':d['image']['original'],'source_page':d['url'],'author':None,'rights':{'status':'copyrighted_promotional_art','license':None,'license_url':None,'credit':d.get('network',{}).get('name') if d.get('network') else (d.get('webChannel') or {}).get('name'),'notes':'TVmaze API metadata license does not grant rights in third-party poster artwork. Artist and image license not supplied.'},'description':clean(d.get('summary')),'match_method':'Title matched against TVmaze show search; episode groups use explicitly labeled series poster.','premiered':d.get('premiered')}

def steam_pick(g):
    if g['kind']!='game':return None
    title=g['title']
    if title=='Halo':title='Halo: The Master Chief Collection'
    if title=='Mass Effect':title='Mass Effect (2007)'
    query=re.sub(r'\([^)]*\)','',title).strip()
    d=get('https://store.steampowered.com/api/storesearch/',{'term':query,'l':'english','cc':'us'})
    allowed_suffixes={'','completeedition','remastered','ultimateedition','directorscut','gameoftheyearedition','definitiveedition','specialedition','enhancededition'}
    def same_game(name):
        a,b=norm(name),norm(query)
        return a.startswith(b) and a[len(b):] in allowed_suffixes
    candidates=[x for x in d.get('items',[]) if same_game(x['name'])]
    if not candidates:return None
    item=max(candidates,key=lambda x:similarity(x['name'],title))
    aid=item['id'];info=get('https://store.steampowered.com/api/appdetails',{'appids':aid,'l':'english','cc':'us'}).get(str(aid),{}).get('data',{})
    if not info or info.get('type') not in ('game','dlc'):return None
    return {'provider':'steam','title':info['name'],'source_url':f'https://cdn.akamai.steamstatic.com/steam/apps/{aid}/library_600x900.jpg','fallback_urls':[f'https://cdn.akamai.steamstatic.com/steam/apps/{aid}/library_600x900_2x.jpg',info.get('header_image')],'source_page':f'https://store.steampowered.com/app/{aid}/','author':'; '.join(info.get('developers',[])) or None,'rights':{'status':'copyrighted_promotional_art','license':None,'license_url':None,'credit':'; '.join(info.get('publishers',[])) or None,'copyright_notice':clean(info.get('legal_notice')) or None,'notes':'Official Steam promotional asset. Developer/publisher credit identifies the work; individual cover artist not provided. No open image license stated.'},'match_method':'Steam search title match and official appdetails checked.','steam_appid':aid}

def discover(limit=None):
    groups=plans(); manifest=read(RESEARCH/'manifest.json',{'schema_version':'1.0','images':{}})
    sources={x['id']:x for x in read(ROOT/'data/sources.json')['sources']}
    remaining=[g for g in groups if g['id'] not in manifest['images'] or manifest['images'][g['id']].get('status')=='search_pending']
    if limit:remaining=remaining[:limit]
    for g in remaining:g['wiki_candidates']=wiki_candidates(g,sources)
    pages=wiki_bulk([t for g in remaining for t in g['wiki_candidates']])
    write(RESEARCH/'wiki-pages.json',pages)
    for n,g in enumerate(remaining):
        selection=wiki_pick(g,pages);errors=[]
        # Official game art and TV posters are more useful than wordmarks.
        for resolver in ([steam_pick] if g['kind']=='game' else [tv_pick] if g['kind'] in ('tv','anime') else []):
            try:
                result=resolver(g)
                if result:selection=result
            except Exception as e:errors.append(str(e))
        item={k:v for k,v in g.items() if k!='source_ids'}
        item.update({'status':'selected' if selection else 'search_pending','selection':selection,'discovery_errors':errors,'selected_on':TODAY})
        manifest['images'][g['id']]=item
        write(RESEARCH/'manifest.json',manifest)
        log('selected' if selection else 'search_pending',image_id=g['id'],title=g['title'],record_ids=g['record_ids'],provider=selection.get('provider') if selection else None)
        if n%10==0:print(f'Selected {n+1}/{len(remaining)}; '+json.dumps(Counter(x['status'] for x in manifest['images'].values())),flush=True)
    return manifest

def metadata(manifest,only_ids=None):
    items=[x for x in manifest['images'].values() if (only_ids is None or x['id'] in only_ids) and x.get('selection',{} ) and x['selection']['provider']=='wikipedia' and 'rights' not in x['selection']]
    for i in range(0,len(items),40):
        batch=items[i:i+40]
        try:
            d=get('https://en.wikipedia.org/w/api.php',{'action':'query','format':'json','formatversion':2,'prop':'imageinfo','iiprop':'url|extmetadata','titles':'|'.join(x['selection']['file_title'] for x in batch)})
            pages={p['title'].replace('_',' '):p for p in d.get('query',{}).get('pages',[])}
            for x in batch:
                sel=x['selection'];p=pages.get(sel['file_title'].replace('_',' '),{});infos=p.get('imageinfo',[])
                if not infos:continue
                info=infos[0];em=info.get('extmetadata',{});vals={k:clean(v.get('value','')) for k,v in em.items()}
                sel['author']=vals.get('Artist') or None
                sel['image_description_page']=info.get('descriptionurl')
                sel['rights']={'status':'non_free' if vals.get('NonFree')=='true' or vals.get('Copyrighted')=='True' else 'as_stated_by_source','license':vals.get('LicenseShortName') or None,'license_url':vals.get('LicenseUrl') or None,'credit':vals.get('Credit') or None,'copyright_notice':vals.get('Copyright') or None,'usage_terms':vals.get('UsageTerms') or None,'notes':'Rights statements transcribed from image file metadata; Wikipedia fair-use rationale is not a general reuse license.' if vals.get('NonFree')=='true' else 'Rights statements transcribed from image file metadata.'}
                sel['source_metadata']=vals
            write(RESEARCH/'manifest.json',manifest)
        except Exception as e:log('rights_metadata_error',error=str(e))

def derivatives(item,content,url):
    im=Image.open(io.BytesIO(content));im.load()
    if im.width<90 or im.height<90:raise ValueError(f'Image too small / placeholder: {im.size}')
    fmt=im.format;ext={'JPEG':'.jpg','PNG':'.png','WEBP':'.webp','GIF':'.gif','AVIF':'.avif'}.get(fmt)
    if not ext:raise ValueError(f'Unsupported original format: {fmt}')
    folder=IMG/item['id'];folder.mkdir(parents=True,exist_ok=True)
    original=folder/('original'+ext);original.write_bytes(content)
    rgb=ImageOps.exif_transpose(im).convert('RGB')
    # Contain complete key art, preserve titles and aspect ratio. Portrait canvas
    # accommodates landscape film frames without fabricating or stretching content.
    poster=Image.new('RGB',(320,480),(18,21,28))
    fitted=ImageOps.contain(rgb,(320,480),Image.Resampling.LANCZOS)
    poster.paste(fitted,((320-fitted.width)//2,(480-fitted.height)//2))
    poster_path=folder/'poster-320.webp';poster.save(poster_path,'WEBP',quality=90,method=6)
    # Square centre crop, lightly biased upwards to retain faces. Circular mask
    # is applied by a future client; the PNG itself remains a full square.
    side=min(rgb.size);left=(rgb.width-side)//2;top=round((rgb.height-side)*.35)
    crop=(left,top,left+side,top+side)
    icon=rgb.crop(crop).resize((32,32),Image.Resampling.LANCZOS)
    icon_path=folder/'icon-32.png';icon.save(icon_path)
    circular=Image.new('RGBA',(32,32));mask=Image.new('L',(32,32));from PIL import ImageDraw
    ImageDraw.Draw(mask).ellipse((0,0,31,31),fill=255);circular.paste(icon,(0,0),mask);circular.save(folder/'icon-circle-preview.png')
    return {'original':rel(original),'poster':rel(poster_path),'icon':rel(icon_path),'source_url':url,'original_sha256':sha(content),'original_bytes':len(content),'original_dimensions':list(rgb.size),'poster_dimensions':[320,480],'icon_dimensions':[32,32],'crop':{'poster':{'method':'contain','canvas':[320,480],'content_box':[(320-fitted.width)//2,(480-fitted.height)//2,(320-fitted.width)//2+fitted.width,(480-fitted.height)//2+fitted.height]},'icon':{'method':'square_crop','box':list(crop),'mask':'circle at display time'}}}

def download_one(item):
    sel=item['selection'];errors=[]
    urls=[sel['source_url']]+sel.get('fallback_urls',[])
    for u in dict.fromkeys(x for x in urls if x):
        try:
            content=get(u,binary=True,cache=False)
            local=derivatives(item,content,u)
            return item['id'],local,None
        except Exception as e:errors.append(str(e))
    return item['id'],None,errors

def download(manifest,only_ids=None):
    metadata(manifest,only_ids)
    items=[x for x in manifest['images'].values() if (only_ids is None or x['id'] in only_ids) and x['status'] in ('selected','download_failed') and x.get('selection')]
    items.sort(key=lambda x:x['priority'])
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(download_one,item) for item in items]
        for n,f in enumerate(concurrent.futures.as_completed(futures)):
            identity,local,errors=f.result();x=manifest['images'][identity]
            if local:
                if local['original_sha256']!=x.get('local',{}).get('original_sha256'):
                    for field in ('visual_review','visual_reviewed_on','contact_sheet'):x.pop(field,None)
                    if manifest.get('visual_quality_review'):manifest['visual_quality_review']['status']='needs_review'
                x.update(status='prepared',local=local,prepared_at=now());log('prepared',image_id=identity,records=x['record_ids'],**{k:local[k] for k in ['original','poster','icon','original_sha256']})
            else:x.update(status='download_failed',download_errors=errors);log('download_failed',image_id=identity,errors=errors)
            write(RESEARCH/'manifest.json',manifest)
            if n%10==0:
                sync(manifest)
                print(f'Downloaded {n+1}/{len(items)}; '+json.dumps(Counter(x['status'] for x in manifest['images'].values())),flush=True)
    sync(manifest)

def sync(manifest=None):
    manifest=manifest or read(RESEARCH/'manifest.json');original=read(ROOT/'data/societies.json')['societies'];byid={r['id']:r for r in original};assets={}
    for x in manifest['images'].values():
        sel=x.get('selection') or {}
        for sid in x['record_ids']:
            if x['status']=='prepared':
                lo=x['local']
                assets[sid]={'status':'ready','image_id':x['id'],**{k:lo[k] for k in ['original','poster','icon','source_url']},'source_page':sel['source_page'],'image_description_page':sel.get('image_description_page'),'author':sel.get('author'),'rights':sel.get('rights',{'status':'unknown','license':None,'notes':'No machine-readable rights data available; no open license inferred.'}),'provider':sel['provider'],'artwork_title':sel['title'],'illustration_scope':'representative_work_art','scope_note':'Work/series key art; shared across the listed society periods and branches. This is not visual evidence of a selected ending. See the unchanged record scope for continuity.','shared_with':[i for i in x['record_ids'] if i!=sid],'crop':lo['crop'],'dimensions':{'original':lo['original_dimensions'],'poster':lo['poster_dimensions'],'icon':lo['icon_dimensions']},'original_sha256':lo['original_sha256'],'accessed_on':TODAY,'selection_review':{'status':'title_and_medium_matched','method':sel.get('match_method'),'visual_review':x.get('visual_review','pending_contact_sheet'),'reviewed_on':x.get('visual_reviewed_on'),'contact_sheet':x.get('contact_sheet')}}
            else:assets[sid]={'status':'pending','poster':None,'icon':None,'image_id':x['id'],'search_status':x['status']}
    for sid in byid:
        if sid not in assets:assets[sid]={'status':'pending','poster':None,'icon':None,'search_status':'not_started'}
    write(ROOT/'data/society-assets.json',{'schema_version':'1.0','assets':assets,'note':'Authoritative asset-only overlay. Historical research batches and all non-assets fields remain unchanged.'})
    corpus=read(ROOT/'data/societies.json')
    for r in corpus['societies']:r['assets']=assets[r['id']]
    write(ROOT/'data/societies.json',corpus)
    for x in manifest['images'].values():
        if x['status']!='prepared':continue
        for sid in x['record_ids']:
            sel=x['selection']
            if sel.get('scope_note'):assets[sid]['scope_note']+=' '+sel['scope_note']
            if sel.get('illustration_scope'):assets[sid]['illustration_scope']=sel['illustration_scope']
            if sel.get('provider')=='imagegen':assets[sid]['selection_review']['status']='generated_from_record_scope'
    # Reused originals may originate in different work-group keys (collections,
    # aliases, and neighboring periods). Disclose every shared record by hash.
    reused={}
    for sid,a in assets.items():
        if a['status']=='ready':reused.setdefault(a['original_sha256'],[]).append(sid)
    for sid,a in assets.items():
        if a['status']=='ready':a['shared_with']=[s for s in reused[a['original_sha256']] if s!=sid]
    write(ROOT/'data/society-assets.json',{'schema_version':'1.0','assets':assets,'note':'Authoritative asset-only overlay. Historical research batches and all non-assets fields remain unchanged.'})
    for r in corpus['societies']:r['assets']=assets[r['id']]
    write(ROOT/'data/societies.json',corpus)
    counts=Counter(x['status'] for x in assets.values());image_counts=Counter(x['status'] for x in manifest['images'].values())
    progress={'updated_at':now(),'date':TODAY,'total_records':len(assets),'ready_records':counts['ready'],'pending_records':len(assets)-counts['ready'],'unique_image_groups':len(manifest['images']),'image_status':dict(image_counts),'provider_counts':dict(Counter(x['selection']['provider'] for x in manifest['images'].values() if x.get('status')=='prepared')),'generation_used':False,'all_non_assets_unchanged':all({k:v for k,v in r.items() if k!='assets'}=={k:v for k,v in byid[r['id']].items() if k!='assets'} for r in corpus['societies']),'resume_command':'python scripts/collect_images.py --all','manifest':'research/images/manifest.json','log':'research/images/events.jsonl'}
    progress['generation_used']=any(x.get('selection',{}).get('provider')=='imagegen' for x in manifest['images'].values() if x.get('selection'))
    progress['generated_images']=sum(x['status']=='prepared' and x['selection']['provider']=='imagegen' for x in manifest['images'].values())
    progress['visually_reviewed_image_groups']=sum(x.get('visual_review')=='reviewed_contact_sheet' for x in manifest['images'].values())
    progress['distinct_original_hashes']=len(reused)
    write(RESEARCH/'progress.json',progress)
    lines=['# Image collection progress', '', f"Updated: {progress['updated_at']}", '', f"Prepared records: **{counts['ready']} / {len(assets)}**; remaining: **{progress['pending_records']}**.",f"Unique image groups: {len(manifest['images'])}. Status: {dict(image_counts)}.", '', 'Current research and wellbeing fields are preserved from the export read immediately before asset sync; research has separate article and utopia validators. No website is built. Originals retain downloaded bytes; posters are 320 × 480 WebP; icons are 32 × 32 PNG, with separate circular previews.', '', '## Resume', '', '```powershell','python scripts/collect_images.py --all','python scripts/collect_images.py --validate','```', '', '`data/society-assets.json` is the authoritative overlay. The merge utility must apply it after historical research revisions. Discovery metadata, failed requests, URLs, rights statements, matching notes and crop coordinates are retained in the manifest/cache/event journal.', '', '## Remaining groups', '']
    for x in manifest['images'].values():
        if x['status']!='prepared':lines.append(f"- `{x['id']}` — {x['title']} ({x['kind']}): {x['status']}; records: {', '.join(x['record_ids'])}")
    if not progress['pending_records']:lines += ['None.','',f"Visual review: {progress['visually_reviewed_image_groups']} / {len(manifest['images'])} image groups. Generated fallback illustrations: {progress['generated_images']}.",'','[Image-stage handoff and source details](README.md) · [Validation](validation.json) · [Contact-sheet index](contact-sheets/index.json)']
    (RESEARCH/'progress.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    return progress

def validate():
    records=read(ROOT/'data/societies.json')['societies'];base=baseline();assert len(records)==len(base)==890
    assert [r['id'] for r in records]==[r['id'] for r in base], 'Image record identities changed'
    # Research and wellbeing evolve independently of assets; their own validators
    # check the current revisions. Never compare them to the pre-image snapshot.
    overlay=read(ROOT/'data/society-assets.json')['assets']
    assert set(overlay)=={r['id'] for r in records}
    assert all(r['assets']==overlay[r['id']] for r in records)
    ready=[r for r in records if r['assets']['status']=='ready'];seen=set()
    for r in ready:
        a=r['assets']
        if a['provider']=='imagegen':
            assert a['source_url'] is None and (ROOT/a['source_page']).is_file()
        else:assert a['source_url'].startswith(('https://','http://')) and a['source_page'].startswith(('https://','http://'))
        if a['image_id'] in seen:continue
        seen.add(a['image_id'])
        assert sha((ROOT/a['original']).read_bytes())==a['original_sha256']
        for k,size in [('poster',(320,480)),('icon',(32,32))]:
            im=Image.open(ROOT/a[k]);im.load();assert im.size==size,(r['id'],k,im.size)
    result={'records':len(records),'ready':len(ready),'pending':len(records)-len(ready),'unique_prepared_images':len(seen),'asset_overlay':'matches current export','non_asset_fields':'validated separately by validate_data, validate_article and validate_utopia','derivative_dimensions':'verified','original_hashes':'verified'}
    write(RESEARCH/'validation.json',result);print(json.dumps(result));return result

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser();p.add_argument('--all',action='store_true');p.add_argument('--discover',action='store_true');p.add_argument('--download',action='store_true');p.add_argument('--sync',action='store_true');p.add_argument('--validate',action='store_true');p.add_argument('--limit',type=int);args=p.parse_args()
    baseline()
    if args.all or args.discover:discover(args.limit)
    if args.all or args.download:download(read(RESEARCH/'manifest.json'))
    if args.all or args.sync:print(json.dumps(sync()))
    if args.all or args.validate:validate()

if __name__=='__main__':main()
