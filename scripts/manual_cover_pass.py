"""Curated continuation for difficult titles, collections and catalog aliases."""
import copy, json, re, sys
import collect_images as c
from resolve_image_gaps import openlibrary_pick, publisher_pick
sys.stdout.reconfigure(encoding='utf8')
M=c.read(c.RESEARCH/'manifest.json');candidates=c.read(c.RESEARCH/'manual-candidates.json',{})

def promo(title,url,page,provider,author=None,note=None):
    return {'provider':provider,'title':title,'source_url':url,'source_page':page,'author':author,'rights':{'status':'copyrighted_promotional_art','license':None,'license_url':None,'notes':note or 'Work-specific cover/poster; no open image license supplied.'},'match_method':'Individually selected after title/author/adaptation review.'}

def tv_id(number):
    d=c.get(f'https://api.tvmaze.com/shows/{number}')
    return promo(d['name'],d['image']['original'],d['url'],'tvmaze',note='Official-series poster indexed by TVmaze. Individual image creator / license not supplied.')

def steam_id(aid):
    d=c.get('https://store.steampowered.com/api/appdetails',{'appids':aid,'l':'english'}).get(str(aid),{}).get('data',{})
    if not d:return None
    s=promo(d['name'],f'https://cdn.akamai.steamstatic.com/steam/apps/{aid}/library_600x900.jpg',f'https://store.steampowered.com/app/{aid}/','steam','; '.join(d.get('developers',[])),note='Official Steam promotional artwork. No open image license supplied; individual artist not named.')
    s['fallback_urls']=[d['header_image']];s['steam_appid']=aid;return s

BOOKS={
 'The Veldt':('The Illustrated Man','Bradbury','Collection containing the story; replace an author portrait with actual cover art.'),
 'The Life and Times of Multivac':('The Bicentennial Man and Other Stories','Asimov','Collection containing the story.'),
 'Twilight (Campbell short story)':('The Best of John W. Campbell','Campbell','Collection containing the Campbell story; unrelated to Stephenie Meyer.'),
 'Arc of a Scythe':('Scythe','Shusterman','First novel cover represents the shared trilogy setting.'),
 'The Happy Breed':('Dangerous Visions','Ellison','Original anthology containing John Sladek’s story.'),
 '3001: The Final Odyssey':('3001','Clarke','Exact novel; subtitle is separate in the catalogue.'),
 'The Two Faces of Tomorrow':('The Two Faces of Tomorrow','Hogan','Exact novel.'),
 'The Pedestrian':('The Golden Apples of the Sun','Bradbury','Collection containing the story.'),
 'The Little Black Bag':('The Best of C. M. Kornbluth','Kornbluth','Collection containing the story.'),
 'The Skills of Xanadu':('The Worlds of Theodore Sturgeon','Sturgeon','Collection containing the story.'),
 'Learning to Be Me':('Axiomatic','Egan','Collection containing the story.'),
 'Border Guards':('Oceanic','Egan','Collection containing the story; publication history checked on the author’s site.'),
 'Crystal Nights':('Oceanic','Egan','Collection containing the story.'),
 'The Commonwealth Saga':("Pandora's Star",'Hamilton','First-volume key art represents the shared Commonwealth setting.'),
 'The Phoenix Exultant':('The Phoenix Exultant','Wright','Exact novel.'),
 'The Merchants of Venus':("The Gold at the Starbow's End",'Pohl','Collection containing the story.'),
 'The Country of the Kind':('In Deep','Knight','Collection containing the story.'),
 'Natural State':('Natural State','Knight','Collection contains the assessed novella.'),
 'A Ticket to Tranai':('Citizen in Space','Sheckley','Collection containing the story.'),
 'The City Dwellers':('The City Dwellers','Platt','Original novel, also revised as Twilight of the City.'),
 'Impostors (novel)':('Impostors','Westerfeld','First novel of the assessed related sequence.'),
 'Lord of All Things':('Lord of All Things','Eschbach','Exact novel.'),
 'Machinehood':('Machinehood','Divya','Exact novel.'),
 'The Employees':('The Employees','Ravn','Exact novel.'),
 'Set My Heart to Five':('Set My Heart to Five','Stephenson','Exact novel.'),
 "The Expert System's Champion":("The Expert System's Champion",'Tchaikovsky','Exact novel.'),
 'The Terraformers':('The Terraformers','Newitz','Exact novel.'),
}
STEAM={'VA-11 Hall-A':447530,'The Uncertain':406970,'Endless Space':208140,'Sword of the Stars II: The End of Flesh':42990}
DIRECT={
 'The Call of the Mech-Men':lambda:promo('Wonder Stories, November 1933 — The Call of the Mech-Men','https://static.wixstatic.com/media/3a61d0_670aa2dae1344fdea5e527167583b36f~mv2.jpg','https://www.flyingcarsandfoodpills.com/the-look-of-the-futue-pulp-robot-co','magazine_cover','Frank R. Paul (attributed)','The source explicitly identifies the November 1933 cover as illustrating this story, while leaving the cover artist uncredited. Attribution to Paul is corroborated by the issue catalogue: https://www.abebooks.com/magazines-periodicals/WONDER-Stories-November-Nov-1933-Sidney/32527260556/bd . No open image license inferred.'),
 'Natural State':lambda:promo('Natural State','https://cdn.hachette.com.au/books/440/9780575111240.jpg','https://www.hachette.com.au/damon-knight/natural-state','publisher_or_author',note='Actual collection/novella cover from the publisher, matched by book title and ISBN. Image artist/open license not provided.'),
 'Useless Hands':lambda:promo('Useless Hands','https://jwkbooks.cdn.bibliopolis.com/pictures/11925_1.jpg?width=768&height=1000&fit=bounds&auto=webp&v=1251998656','https://www.jwkbooks.com/pages/books/11925/claude-farrere-frederic-charles-pierre-edouard-bargone/useless-hands','antiquarian_book_catalogue',note='Photograph of the actual English first edition. Cover artist and photograph license not supplied by seller.'),
 'Freefall':lambda:promo('Freefall — comic strip 4440','http://freefall.purrsia.com/ff4500/fc04440.png','http://freefall.purrsia.com/default.htm','official_webcomic','Mark Stanley','Official comic panel from the current series home page. Work copyright Mark Stanley; no open image license inferred.'),
 'Friendship is Optimal':lambda:promo('Friendship is Optimal','https://p5.toutiaoimg.com/origin/ffd3000243d490f349f1','https://fimtale.com/t/118-8','webfiction_translation_cover',note='Cover embedded in the Chinese translation, which identifies the original Iceman story. Cover artist and reusable image license not supplied.'),
 'The Year 4338':lambda:promo('4338-й год. Петербургские письма','https://imo10.labirint.ru/books/858995/cover.jpg/484-0','https://www.labirint.ru/books/858995/','book_catalogue'),
 'The Eternal Bread':lambda:promo('Вечный хлеб / The Eternal Bread','https://cdn.litres.ru/pub/c/cover_415/127201.webp','https://www.litres.ru/book/aleksandr-belyaev/vechnyy-hleb-127201/','book_catalogue',note='Public-domain text listing does not establish public-domain status of the modern cover. Cover artist/license not supplied.'),
 'The Two Faces of Tomorrow':lambda:promo('The Two Faces of Tomorrow','https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1329072777i/2220766.jpg','https://www.goodreads.com/book/show/2220766','book_catalogue'),
 'The Phoenix Exultant':lambda:promo('The Phoenix Exultant','https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1388430323i/474050.jpg','https://www.goodreads.com/book/show/474050.The_Phoenix_Exultant','book_catalogue'),
 'Lord of All Things':lambda:promo('Lord of All Things','https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1431102484i/20660338.jpg','https://www.goodreads.com/book/show/20660338.Lord_of_All_Things','book_catalogue'),
 'Welcome to Alflolol':lambda:promo('Valerian and Laureline: Welcome to Alflolol','https://covers.openlibrary.org/b/id/10021957-L.jpg?default=false','https://openlibrary.org/works/OL20051547W','book_catalogue',note='Cover ID obtained from the exact Open Library work referenced in the research; original album art, no open license stated.'),
 'Dunno in Sun City':lambda:promo('Незнайка в Солнечном городе / Dunno in Sun City','https://thumb.wikimedia.org/wikipedia/ru/thumb/0/06/Dunno_in_the_Sun_City.jpg/330px-Dunno_in_the_Sun_City.jpg?utm_source=ru.wikipedia.org&utm_campaign=parser&utm_content=thumbnail','https://ru.wikipedia.org/wiki/Незнайка_в_Солнечном_городе','wikipedia_display_image',note='Original book adaptation: article labels this the first edition cover. Image artist/license not supplied by retrieved metadata.'),
 'The Employees':lambda:promo('The Employees','https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1635239756i/59389079.jpg','https://www.goodreads.com/book/show/59389079-the-employees','book_catalogue'),
 'Set My Heart to Five':lambda:promo('Set My Heart to Five','https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1575748404i/49122676.jpg','https://www.goodreads.com/book/show/49122676-set-my-heart-to-five','book_catalogue'),
 'Impostors (novel)':lambda:promo('Impostors','https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1638392281i/37825397.jpg','https://www.goodreads.com/book/show/37825397-impostors','book_catalogue'),
 'Electric Dreams: Autofac':lambda:promo("Philip K. Dick's Electric Dreams",'https://static.tvmaze.com/uploads/images/original_untouched/142/355707.jpg','https://www.tvmaze.com/shows/17099','tvmaze',note='Actual television series poster; not the prose-story magazine cover.'),
 'The Curious Trio':lambda:promo("Yoko Tsuno: Le Trio de l'étrange",'https://bdi.dlpdomain.com/album/9782800106663-couv-M700x1200.jpg','https://www.dupuis.com/yoko-tsuno/bd/yoko-tsuno-tome-1-le-trio-de-l-etrange/1253','publisher_or_author','Roger Leloup'),
 'The Forge of Vulcan':lambda:promo('Yoko Tsuno: La Forge de Vulcain','https://yokotsuno.fr/wp-content/uploads/comics/frontend/images/cover/yoko3fr.jpg','https://yokotsuno.fr/comic_book/la-forge-de-vulcain/','series_cover_archive','Roger Leloup'),
 'The Three Suns of Vinea':lambda:promo('Yoko Tsuno: Les Trois Soleils de Vinéa','https://yokotsuno.fr/wp-content/uploads/comics/frontend/images/cover/yoko6fr.jpg','https://yokotsuno.fr/comic_book/les-3-soleils-de-vinea/','series_cover_archive','Roger Leloup'),
 'The Archangels of Vinea':lambda:promo('Yoko Tsuno: Les Archanges de Vinéa','https://yokotsuno.fr/wp-content/uploads/comics/frontend/images/cover/yoko13fr.jpg','https://yokotsuno.fr/comic_book/les-archanges-de-vinea/','series_cover_archive','Roger Leloup'),
 'The Technopriests':lambda:promo('The Technopriests','https://store.humanoids.com/cdn/shop/files/ADD-ON_Technopriests.jpg?v=1768311853','https://store.humanoids.com/products/addons-the-technopriests-hardcover-edition','publisher_or_author','Zoran Janjetov; Fred Beltran (colorist)','Work art credits from publisher. Cover-specific attribution not separately supplied; no open license stated.'),
 'Manna (novel)':lambda:promo('Manna: Two Visions of Humanity’s Future','https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1394228449i/13559843.jpg','https://www.goodreads.com/book/show/13559843-manna','book_catalogue',note='Correct Marshall Brain work checked against catalogue description; poster artist/license not supplied.'),
 "Orion's Arm":lambda:promo("Against a Diamond Sky — Tales from Orion's Arm",'https://orionsarm.com/im_store/front-text-144%20(1)_001.png','https://orionsarm.com/xcms.php?page=gen_publications&r=oa-page','publisher_or_author','Bernd Helfert','Cover artwork credited to Bernd Helfert on the official publications page. Shared universe illustration, not a literal image of every scoped OA society. No open image license stated on the consulted page.'),
 'Mindjammer':lambda:promo('Mindjammer: The Roleplaying Game','https://sarahnewtonwriter.com/wp-content/uploads/2014/02/mindjammer_cover.jpg','https://sarahnewtonwriter.com/2012/10/07/the-mindjammer-roleplaying-game-2nd-edition/','publisher_or_author',note='Final 2014 RPG cover displayed in the author’s site cover gallery/sidebar. The earlier sketch is not used. Artist/open image license not supplied.'),
 'Sufficiently Advanced':lambda:promo('Sufficiently Advanced — A Game of the Far Future','https://assets.lulu.com/cover_thumbs/1/k/1kkp2vw-front-shortedge-384.jpg','https://www.lulu.com/shop/colin-fredericks/sufficiently-advanced-hc/hardcover/product-2290382.html','publisher_or_author','Daniel Solis','First-edition cover; Daniel Solis credited as front-cover artist in the 2008 book credits. Copyright Colin Fredericks / respective artists; no open image license inferred.'),
 'Real Humans':lambda:promo('Äkta Människor / Real Humans','https://static.tvmaze.com/uploads/images/original_untouched/275/688809.jpg','https://www.tvmaze.com/shows/3470','tvmaze'),
 'Electric Dreams: Kill All Others':lambda:promo("Philip K. Dick's Electric Dreams",'https://static.tvmaze.com/uploads/images/original_untouched/142/355707.jpg','https://www.tvmaze.com/shows/17099','tvmaze'),
 'The Threat of the Robot':lambda:promo('The Threat of the Robot and Other Nightmarish Futures','https://x.sf-encyclopedia.com/gal/ziesing/Keller-ThreatRobot.jpg','https://sf-encyclopedia.com/gallery.php?id=Keller-ThreatRobot.jpg','sfe_gallery','Tom Roberts','Cover artist credited in SFE bibliography as pb/Tom Roberts. Copyrighted cover art; no open license stated.'),
 'Mechanistria':lambda:promo('Astounding Science-Fiction, January 1942','https://collectorshowcase.fr/images2/ast_4201.jpg','https://collectorshowcase.fr/astounding_1942.htm','magazine_cover','Hubert Rogers','Magazine containing Mechanistria. Artist credited as Rogers by the source; copyright/license not independently established.'),
 'Nova Praxis':lambda:promo('Nova Praxis: Savage Worlds Edition','https://images.squarespace-cdn.com/content/v1/513f57ebe4b0970eaf232dec/1411429136405-VRGAKJO9SF6QPT34HM4E/image-asset.jpeg','https://voidstargames.squarespace.com/resources','publisher_or_author'),
 'The Last Angel':lambda:promo('The Last Angel — UECNS Nemesis fan art','https://i.imgur.com/GT9wnxS.png','https://proximalflame.com/fan-art/','author_fanart_gallery','Kazimir175','Fan art credited on the work author’s gallery. Common universe illustration of Nemesis; not a literal depiction of the scoped Compact society. No open reuse license supplied.'),
 'The Million':lambda:promo('The Million','https://images.macmillan.com/folio-assets/macmillan_us_frontbookcovers_1000H/9781250185426.jpg','https://us.macmillan.com/books/9781250185426/themillion/','publisher_isbn_cover'),
 'The Terraformers':lambda:promo('The Terraformers','https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1649899400i/60784471.jpg','https://www.goodreads.com/book/show/60784471-the-terraformers','book_catalogue'),
 "The Expert System's Champion":lambda:promo("The Expert System's Champion",'https://images.macmillan.com/folio-assets/macmillan_us_frontbookcovers_1000H/9781250766397.jpg','https://www.publishersweekly.com/9781250766397','publisher_isbn_cover'),
}

for identity,item in M['images'].items():
    if item['status']=='prepared' or identity in candidates and candidates[identity].get('selection'):continue
    title=item['title'];sel=None
    try:
        if title in DIRECT:sel=DIRECT[title]()
        elif title in STEAM:sel=steam_id(STEAM[title])
        elif title in BOOKS:
            query,author,note=BOOKS[title];g=copy.deepcopy(item);g['title']=query
            c.EXPECTED_AUTHORS[query]=author
            sel=openlibrary_pick(g)
            if sel:sel['scope_note']=note
        elif title=='Beast Wars: Transformers':
            ds=c.get('https://api.tvmaze.com/search/shows',{'q':'Beast Wars'})
            hit=next((x['show'] for x in ds if x['show'].get('premiered','').startswith('1996') and 'beast' in x['show']['name'].lower()),None)
            if hit:sel=tv_id(hit['id'])
    except Exception as e:c.log('manual_source_error',title=title,error=str(e))
    if sel:
        candidates[identity]={'selection':sel};c.write(c.RESEARCH/'manual-candidates.json',candidates)
        print(title,'->',sel['title'],flush=True)
print('Manual candidates:',len(candidates),flush=True)
