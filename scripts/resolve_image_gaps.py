"""Target remaining covers through matched books and original bulk cover archives.

Does not crawl the Open Library Covers image API. Uses its metadata to locate
specific original files in the bulk archives recommended by Open Library.
"""
import argparse, concurrent.futures, io, json, re, sys, time
from urllib.parse import quote, urlparse, urljoin
import requests
from bs4 import BeautifulSoup
from PIL import Image
import collect_images as c
KNOWN_SF_AUTHORS=set('Asimov Banks Baxter Bear Beckett Bester Bogdanov Brain Bradbury Brin Breuer Butler Campbell Capek Clarke Crowley Dahl Daniel Delany Dick Doctorow Dodd Egan Efremov Farmer Forster Gibson Gunn Haldeman Hamilton Harrison Haig Heinlein Hertling Hogan Ishiguro Jodorowsky Kunsken Leiber Lem Liu Lukyanenko MacLeod Morris Naam Nayler Newitz Nolan Nosov Odoevsky Pohl Reynolds Rucker Russ Russell Schroeder Sheffield Shusterman Silverberg Simak Sladek Spinrad Stiegler Stross Strugatsky Suverud Swanwick Tchaikovsky Tevis Varley Vance Verne Vinge Vonnegut Wells Williams Williamson Wright Zamyatin'.lower().split())

def kitsu_pick(item):
    if not any(m in item['media'] for m in ('anime','manga')) and item['title']!='The Animatrix':return None
    typ='manga' if item['kind']=='manga' else 'anime'
    query=re.sub(r'\s*\([^)]*\)','',item['title'])
    d=c.get(f'https://kitsu.io/api/edge/{typ}',{'filter[text]':query,'page[limit]':8})
    candidates=[]
    for x in d.get('data',[]):
        a=x['attributes'];titles=list((a.get('titles') or {}).values())+[a.get('canonicalTitle','')]
        score=max(c.similarity(query,t) for t in titles if t)
        if score<.84 or not a.get('posterImage'):continue
        if item['kind']=='movie' and a.get('subtype')=='movie':score+=.08
        if item['kind'] in ('tv','anime') and a.get('subtype')=='TV':score+=.05
        candidates.append((score,x))
    if not candidates:return None
    _,d=max(candidates,key=lambda x:x[0]);a=d['attributes']
    return {'provider':'kitsu','title':a.get('canonicalTitle') or query,'source_url':a['posterImage'].get('original') or a['posterImage']['large'],'source_page':f'https://kitsu.io/{typ}/'+a['slug'],'author':None,'rights':{'status':'copyrighted_promotional_art','license':None,'license_url':None,'notes':'Anime/manga catalogue poster. Artist and reusable image license not supplied.'},'match_method':'English/canonical title matched against Kitsu catalogue; movie/TV/manga subtype checked.','catalogue_titles':a.get('titles'),'subtype':a.get('subtype'),'start_date':a.get('startDate')}

def itunes_pick(item):
    if item['kind']!='movie':return None
    query=re.sub(r'\s*\([^)]*\)','',item['title'])
    d=c.get('https://itunes.apple.com/search',{'term':query,'entity':'movie','country':'us','limit':20})
    candidates=[x for x in d.get('results',[]) if c.similarity(x.get('trackName',''),query)>.9 and x.get('artworkUrl100')]
    if not candidates:return None
    scope=' '.join(s['continuity'] for s in item['scope'])
    years=set(re.findall(r'\b(?:19|20)\d\d\b',scope))
    def rank(x):return c.similarity(x['trackName'],query)+(0.4 if x.get('releaseDate','')[:4] in years else 0)
    d=max(candidates,key=rank)
    url=re.sub(r'/\d+x\d+bb\.', '/600x600bb.',d['artworkUrl100'])
    return {'provider':'apple_itunes','title':d['trackName'],'source_url':url,'fallback_urls':[d['artworkUrl100']],'source_page':d['trackViewUrl'],'author':None,'rights':{'status':'copyrighted_promotional_art','license':None,'license_url':'https://performance-partners.apple.com/search-api','credit':d.get('artistName'),'copyright_notice':d.get('copyright'),'notes':'Store promotional artwork; Apple API promotional-use terms apply. Individual poster artist not supplied. No open license inferred.'},'match_method':'Film title matched in Apple catalogue; release year checked against scoped adaptation.','release_date':d.get('releaseDate')}

def wikipedia_html_pick(item):
    old=item.get('selection') or {}
    if old.get('provider')!='wikipedia':return None
    url=old['source_page'];path=c.RESEARCH/'pages'/(c.sha(url.encode())+'.html')
    if path.exists():body=path.read_text(encoding='utf8')
    else:
        r=requests.get(url,headers={'User-Agent':c.UA},timeout=20);r.raise_for_status();body=r.text
        path.parent.mkdir(exist_ok=True);path.write_text(body,encoding='utf8')
    soup=BeautifulSoup(body,'html.parser')
    for img in soup.select('.infobox img'):
        src=img.get('src','');alt=img.get('alt','')
        if re.search(r'logo|flag|map|icon',src+' '+alt,re.I):continue
        if int(img.get('width',0))<120 or int(img.get('height',0))<140:continue
        variants=img.get('srcset','').split(',')
        if variants and variants[-1].strip():src=variants[-1].strip().split(' ')[0]
        src=urljoin(url,src)
        if '/thumb/' in src:
            parts=src.replace('/thumb/','/').rsplit('/',1);src=parts[0]
        anchor=img.find_parent('a');filepage=urljoin(url,anchor.get('href','')) if anchor else None
        if src==old['source_url']:continue
        new={**old,'source_url':src,'image_description_page':filepage,'author':None,'rights':{'status':'unknown_cover_copyright','license':None,'license_url':None,'notes':'Original image URL resolved from the current work article infobox after the cached page-image URL failed. Cover copyright not cleared; file description is linked.'},'match_method':'Current work article infobox cover, replacing stale page-image metadata.'}
        new.pop('file_title',None)
        return new
    return None

def publisher_pick(item):
    records={r['id']:r for r in c.baseline()}
    sources={x['id']:x for x in c.read(c.ROOT/'data/sources.json')['sources']}
    sids=list(dict.fromkeys(s for rid in item['record_ids'] for s in records[rid]['source_ids']))
    approved=['hachette','macmillan','penguinrandomhouse','simonandschuster','abramsbooks','baen.com','scholastic','torpublishing','orbitbooks','karl-schroeder','gregbear','gregegan','charlesstross','antipope','marshallbrain','craphound','rifters.com','qntm.org','orionsarm','imagecomics','awastudios','humanoids','rebellion','drivethrurpg','sjgames','modiphius','sufficientlyadvanced','nova-praxis','mindjammerpress','eclipsephase','massifpress']
    urls=[sources[s]['url'] for s in sids if any(a in urlparse(sources[s].get('url','')).netloc for a in approved)]
    for url in list(dict.fromkeys(urls))[:3]:
        try:
            isbn=re.search(r'97[89]\d{10}',url)
            if isbn and ('macmillan.com' in url or 'penguinrandomhouse.com' in url):
                code=isbn.group(0)
                image=f'https://images.macmillan.com/folio-assets/macmillan_us_frontbookcovers_1000H/{code}.jpg' if 'macmillan.com' in url else f'https://images.penguinrandomhouse.com/cover/{code}'
                data=c.get(image,binary=True);im=Image.open(io.BytesIO(data))
                if im.width>=120 and im.height>=160:
                    return {'provider':'publisher_isbn_cover','title':re.sub(r'\s*\([^)]*\)','',item['title']),'source_url':image,'source_page':url,'author':None,'rights':{'status':'copyrighted_cover_art','license':None,'license_url':None,'credit':urlparse(url).netloc,'notes':'Official publisher cover endpoint for the ISBN in the existing work-specific reference URL. Artist/open license not supplied.'},'isbn':code,'match_method':'ISBN extracted from the established publisher reference; corresponding publisher cover fetched and image dimensions verified.'}
            path=c.RESEARCH/'pages'/(c.sha(url.encode())+'.html')
            if path.exists():body=path.read_text(encoding='utf8')
            else:
                r=requests.get(url,headers={'User-Agent':c.UA},timeout=18);r.raise_for_status();body=r.text
                path.parent.mkdir(exist_ok=True);path.write_text(body,encoding='utf8')
            soup=BeautifulSoup(body,'html.parser'); title=c.clean(soup.title.text if soup.title else '')
            # The reference must actually be the requested work's page.
            base=re.sub(r'\s*\([^)]*\)','',item['title'])
            if c.norm(base) not in c.norm(title) and len(c.norm(base))>7:continue
            candidates=[]
            for meta in soup.select('meta[property="og:image"],meta[name="twitter:image"]'):
                if meta.get('content'):candidates.append(meta['content'])
            for img in soup.select('img'):
                alt=img.get('alt','')
                if c.norm(base) in c.norm(alt) or re.search(r'cover|book-jacket',alt,re.I):
                    for key in ['data-src','src']:
                        if img.get(key):candidates.append(img[key])
            for u in list(dict.fromkeys(candidates))[:4]:
                u=urljoin(url,u)
                if not u.startswith('https://'):u=u.replace('http://','https://',1)
                try:
                    data=c.get(u,binary=True);im=Image.open(io.BytesIO(data))
                    if im.width<120 or im.height<160 or im.height/im.width<1.16:continue
                    return {'provider':'publisher_or_author','title':base,'source_url':u,'source_page':url,'author':None,'rights':{'status':'copyrighted_cover_art','license':None,'license_url':None,'credit':urlparse(url).netloc,'notes':'Cover supplied on the publisher/author reference page. Individual artist and open license were not supplied by the retrieved metadata.'},'match_method':'Existing work-specific publisher/author source; page title and portrait cover verified.'}
                except Exception:continue
        except Exception as e:c.log('publisher_cover_error',title=item['title'],url=url,error=str(e))
    return None

def sfe_pick(item):
    records={r['id']:r for r in c.baseline()}
    sources={x['id']:x for x in c.read(c.ROOT/'data/sources.json')['sources']}
    sids=list(dict.fromkeys(s for rid in item['record_ids'] for s in records[rid]['source_ids']))
    urls=[sources[s]['url'] for s in sids if 'sf-encyclopedia.com/entry/' in sources[s].get('url','')]
    base=re.sub(r'\s*\([^)]*\)','',item['title'])
    for url in dict.fromkeys(urls):
        try:
            path=c.RESEARCH/'pages'/(c.sha(url.encode())+'.html')
            if path.exists():body=path.read_text(encoding='utf8')
            else:
                r=requests.get(url,headers={'User-Agent':c.UA},timeout=14);r.raise_for_status();body=r.text
                path.parent.mkdir(exist_ok=True);path.write_text(body,encoding='utf8')
            soup=BeautifulSoup(body,'html.parser')
            for a in soup.select('a[href*="gallery.php?id="]'):
                node=a.find_parent('li') or a.parent
                text=c.clean(node.get_text(' ',strip=True))
                if c.norm(base) not in c.norm(text):continue
                gallery=urljoin(url,a['href']);r=requests.get(gallery,headers={'User-Agent':c.UA},timeout=14);r.raise_for_status()
                gs=BeautifulSoup(r.text,'html.parser');img=next((im for im in gs.select('img[src]') if '/gal/' in im['src']),None)
                if not img:continue
                caption=gs.get_text(' ',strip=True)
                image=urljoin(gallery,img['src'])
                artist=re.search(r'\b(?:pb|hb)/([^\]]+)',text)
                return {'provider':'sfe_gallery','title':base,'source_url':image,'source_page':gallery,'author':artist.group(1).strip() if artist else None,'rights':{'status':'copyrighted_cover_art','license':None,'license_url':None,'credit':'The Encyclopedia of Science Fiction cover gallery','notes':'Cover matches the work in the source bibliography. Source gallery/bibliography credit is retained; no open image license stated.','source_caption':text},'match_method':'Work title matched to a cover-gallery link in the existing source bibliography.'}
        except Exception as e:c.log('sfe_cover_error',title=base,error=str(e))
    return None

def openlibrary_pick(item):
    title=re.sub(r'\s*\([^)]*\)','',item['title'])
    params={'title':title,'limit':12,'fields':'key,title,subtitle,author_name,cover_i,first_publish_year,subject,cover_edition_key'}
    expected=c.EXPECTED_AUTHORS.get(title)
    if expected:params['author']=expected
    d=c.get('https://openlibrary.org/search.json',params)
    docs=[x for x in d.get('docs',[]) if x.get('cover_i') and max(c.similarity(x['title'],title),c.similarity(x['title']+' '+x.get('subtitle',''),title))>.88]
    if not docs:return None
    scope=' '.join(str(s) for s in item['scope']).lower()
    if expected:
        docs=[x for x in docs if any(expected.lower() in a.lower() for a in x.get('author_name',[]))]
        if not docs:return None
        scope+=' '+expected.lower()
    def rank(x):
        author=any(a.split()[-1].lower() in scope for a in x.get('author_name',[]) if len(a.split()[-1])>3)
        known=any(c.norm(a.split()[-1]) in KNOWN_SF_AUTHORS for a in x.get('author_name',[]))
        science=known or any(any(z in s.lower() for z in ['science fiction','utopia','dystopia','robot','cyberpunk','comic','fantasy','fiction']) for s in x.get('subject',[]))
        return c.similarity(x['title'],title)*100+30*author+10*science
    d=max(docs,key=rank)
    if rank(d)<108:return None
    cid=d['cover_i'];meta=c.get(f'https://covers.openlibrary.org/b/id/{cid}.json')
    filename=meta.get('filename') or ''
    # Original archive members, not the rate-limited thumbnail/image API.
    if '.zip' in filename:
        archive=filename.split(':')[0].split('/')[-1]
        collection=archive.rsplit('_',1)[0]
        url=f'https://archive.org/download/{collection}/{archive}/{cid:010d}.jpg'
    else:
        collection=f'covers_{cid//1000000:04d}';archive=f'{collection}_{cid//10000%100:02d}.tar'
        url=f'https://archive.org/download/{collection}/{archive}/{cid:010d}.jpg'
    fallback=[]
    if meta.get('source_url'):fallback.append(meta['source_url'].replace('http://','https://',1))
    fallback.append(f'https://covers.openlibrary.org/b/id/{cid}-L.jpg?default=false')
    return {'provider':'openlibrary_bulk_archive','title':d['title'],'source_url':url,'fallback_urls':fallback,'source_page':'https://openlibrary.org/'+('books/'+d['cover_edition_key'] if d.get('cover_edition_key') else d['key'].lstrip('/')),'catalogue_page':'https://openlibrary.org'+d['key'],'author':None,'work_authors':d.get('author_name',[]),'cover_id':cid,'image_description_page':f'https://covers.openlibrary.org/b/id/{cid}.json','rights':{'status':'unknown_cover_copyright','license':None,'license_url':None,'credit':'Cover indexed by Open Library / Internet Archive','original_source_url':meta.get('source_url'),'notes':'Book author is recorded separately from image artist. No image license or illustrator is supplied by the catalogue. Hosting/scanning does not imply public-domain cover art.'},'match_method':'Exact/near-exact catalogue title, fiction classification and/or scoped author match. Bulk archive member preferred; the original source or exact CoverID may be used when that member has not been archived.'}

def resolve(item):
    try:
        if any(m in item['media'] for m in ('anime','manga')) or item['title']=='The Animatrix':
            sel=kitsu_pick(item)
            if sel:return item['id'],sel,None
        if item['kind'] in ('book','comic','tabletop'):
            sel=publisher_pick(item)
            if sel:return item['id'],sel,None
            sel=openlibrary_pick(item)
            if sel:return item['id'],sel,None
            sel=sfe_pick(item)
            if sel:return item['id'],sel,None
        if item['status']=='download_failed':
            sel=wikipedia_html_pick(item)
            if sel:return item['id'],sel,None
        sel=itunes_pick(item)
        if sel:return item['id'],sel,None
        sel=publisher_pick(item)
        if sel:return item['id'],sel,None
        if item['kind'] in ('book','comic','manga','tabletop'):
            sel=openlibrary_pick(item)
            if sel:return item['id'],sel,None
            sel=sfe_pick(item)
            if sel:return item['id'],sel,None
        return item['id'],None,None
    except Exception as e:return item['id'],None,str(e)

def main():
    sys.stdout.reconfigure(encoding='utf8')
    parser=argparse.ArgumentParser();parser.add_argument('--prepare-only',action='store_true');parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    manifest=c.read(c.RESEARCH/'manifest.json')
    if args.apply:
        candidates=c.read(c.RESEARCH/'gap-candidates.json',{})
        staged=c.read(c.RESEARCH/'gap-prepared.json',{})
        for identity,result in candidates.items():
            item=manifest['images'].get(identity)
            sel=result.get('selection') or {}
            expected=c.EXPECTED_AUTHORS.get(re.sub(r'\s*\([^)]*\)','',item['title'])) if item else None
            if expected and sel.get('provider')=='openlibrary_bulk_archive' and not any(expected.lower() in a.lower() for a in sel.get('work_authors',[])):
                c.log('reject_wrong_book_author',image_id=identity,title=item['title'],authors=sel.get('work_authors'),expected=expected)
                result['selection']=openlibrary_pick(item)
            if item and item['status']!='prepared' and result.get('selection'):
                if item.get('selection'):item.setdefault('prior_selections',[]).append(item['selection'])
                item.update(selection=result['selection'],status='selected')
                prepared=staged.get(identity,{})
                if prepared.get('local') and prepared.get('selection',{}).get('source_url')==result['selection']['source_url']:
                    item.update(status='prepared',local=prepared['local'],prepared_at=c.now())
        c.write(c.RESEARCH/'manifest.json',manifest);c.download(manifest);c.validate();return
    candidates=c.read(c.RESEARCH/'gap-candidates.json',{}) if args.prepare_only else {}
    def needs_lookup(x):
        sel=candidates.get(x['id'],{}).get('selection') or {}
        expected=c.EXPECTED_AUTHORS.get(re.sub(r'\s*\([^)]*\)','',x['title']))
        wrong=expected and sel.get('provider')=='openlibrary_bulk_archive' and not any(expected.lower() in a.lower() for a in sel.get('work_authors',[]))
        retry_failed=x['status']=='download_failed' and sel.get('source_url')==(x.get('selection') or {}).get('source_url')
        return x['status'] in ('search_pending','download_failed') and (not sel or wrong or retry_failed)
    items=[x for x in manifest['images'].values() if needs_lookup(x)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for n,(identity,sel,error) in enumerate(pool.map(resolve,items)):
            item=manifest['images'][identity]
            candidates[identity]={'selection':sel,'error':error}
            c.write(c.RESEARCH/'gap-candidates.json',candidates)
            if sel:
                if item.get('selection'):item.setdefault('prior_selections',[]).append(item['selection'])
                item.update(selection=sel,status='selected')
                c.log('gap_resolved',image_id=identity,provider=sel['provider'],title=sel['title'])
            if error:item.setdefault('discovery_errors',[]).append(error)
            if not args.prepare_only:c.write(c.RESEARCH/'manifest.json',manifest)
            print(f'Gap {n+1}/{len(items)}: {item["title"]}: '+('selected' if sel else 'still pending'),flush=True)
    if args.prepare_only:return
    c.download(manifest)
    c.validate()

if __name__=='__main__':main()
