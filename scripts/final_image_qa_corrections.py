"""Specific corrections from visual QA of every contact sheet."""
import copy, re, sys
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import collect_images as c
from resolve_image_gaps import openlibrary_pick
sys.stdout.reconfigure(encoding='utf8')
m=c.read(c.RESEARCH/'manifest.json');out=c.read(c.RESEARCH/'manual-candidates.json')

def art(title,url,page,provider='book_catalogue',author=None,note=''):
    return {'provider':provider,'title':title,'source_url':url,'source_page':page,'author':author,'rights':{'status':'copyrighted_cover_art','license':None,'license_url':None,'notes':note or 'Image artist and open license not supplied.'},'match_method':'Visual QA: replace a wrong adaptation, placeholder, product mock-up, or scanned internal/back page with work cover art.'}

DIRECT={
 'ReBoot':art('ReBoot (1994 animated series)','https://static.tvmaze.com/uploads/images/original_untouched/9/22952.jpg','https://www.tvmaze.com/shows/1662','tvmaze',note='1994 animated series; replaces the unrelated 2022 sitcom.'),
 'The Twilight Zone: Quarantine (1985)':art('The Twilight Zone (1985)','https://static.tvmaze.com/uploads/images/original_untouched/17/43916.jpg','https://www.tvmaze.com/shows/3289','tvmaze',note='1985 anthology series poster; matches the episode continuity.'),
 'Shangri-La':art('Shangri-La (2009 anime)','https://media.kitsu.app/anime/poster_images/3995/original.jpg','https://kitsu.io/anime/3995','kitsu',note='2009 anime; replaces an unrelated live-action series.'),
 'Warhammer 40,000':art('Warhammer 40,000 Core Book, 10th edition','https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1688497373i/183739243.jpg','https://www.goodreads.com/book/show/183739243-warhammer-40-000-core-book-10th-edition','book_catalogue',note='Tabletop setting core-book cover, copyright Games Workshop. Replaces a photograph of people playing; individual cover artist not supplied.'),
 'The Technopriests':art('Les Technopères — Intégrale','https://cdn2.humano.com/assets/CatalogueArticle/36955/Technoperes_Cover-FR_original_R1200.jpg','https://www.humano.com/album/32833','publisher_or_author','Zoran Janjetov; Fred Beltran (colorist)','Original-comic omnibus cover, same continuity. Replaces a multi-product retail mock-up. No open image license supplied.'),
 'Lazarus':art('Lazarus (comic series)','https://thumb.wikimedia.org/wikipedia/en/thumb/b/bf/Lazarus_two_cover.jpg/250px-Lazarus_two_cover.jpg','https://en.wikipedia.org/wiki/Lazarus_(comics)','wikipedia_display_image',note='Actual comic cover. Replaces Lars Kepler’s unrelated crime novel; artist/license not supplied in this retrieval.'),
}
WIKI_FRONT={'Voyage from Yesteryear','The Marching Morons','Why Call Them Back from Heaven?','The Visitors','The Lord of Opium','Stars in My Pocket Like Grains of Sand','A Door into Ocean'}
for identity,item in m['images'].items():
    title=item['title'];sel=DIRECT.get(title)
    if title=='The Machine Stops':
        c.EXPECTED_AUTHORS[title]='Forster';sel=openlibrary_pick(item)
        if sel:sel['scope_note']='Actual prose-work cover; replaces a television-adaptation frame.'
    if title in WIKI_FRONT:
        old=next((s for s in item.get('prior_selections',[]) if s and s.get('provider')=='wikipedia' and s.get('source_url')),None)
        if old:
            url=old['source_url'].split('?')[0];base,name=url.rsplit('/',1)
            if '/thumb/' not in base:
                thumb=base.replace('upload.wikimedia.org','thumb.wikimedia.org').replace('/wikipedia/en/','/wikipedia/en/thumb/').replace('/wikipedia/commons/','/wikipedia/commons/thumb/')+'/'+name+'/250px-'+name
                sel=art(old['title'],thumb,old['source_page'],'wikipedia_display_image',old.get('author'),'Source article front cover / original magazine cover replaces a scanned inner or back page. No open image license inferred.')
    if title=='Riverworld':
        page='https://en.wikipedia.org/wiki/To_Your_Scattered_Bodies_Go'
        try:
            soup=BeautifulSoup(requests.get(page,headers={'User-Agent':c.UA},timeout=12).text,'html.parser')
            img=next(i for i in soup.select('.infobox img') if int(i.get('width',0))>=120)
            sel=art('To Your Scattered Bodies Go — Riverworld',urljoin(page,img['src']),page,'wikipedia_display_image',note='First Riverworld novel cover represents the shared grail-supported setting; replaces a scanned title page.')
        except Exception as e:c.log('qa_riverworld_error',error=str(e))
    if sel:
        out[identity]={'selection':sel,'force_review':True};print(title,'->',sel['title'],flush=True)
c.write(c.RESEARCH/'manual-candidates.json',out)
