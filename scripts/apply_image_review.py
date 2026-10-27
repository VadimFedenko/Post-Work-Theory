"""Apply specific visual/continuity corrections identified during cover QA."""
import copy, sys
import collect_images as c
from resolve_image_gaps import kitsu_pick

def main():
    sys.stdout.reconfigure(encoding='utf8')
    manifest=c.read(c.RESEARCH/'manifest.json')
    changes=[]
    planned=c.plans();groups={tuple(g['record_ids']):g for g in planned}
    for identity,item in list(manifest['images'].items()):
        g=groups.get(tuple(item['record_ids']))
        if g and g['id']!=identity and g['kind']=='tv' and item['kind']=='book':
            migrated={**item,**g};old=item.get('selection') or {}
            try:new=c.tv_pick(g)
            except Exception:new=None
            if new:
                migrated.setdefault('prior_selections',[]).append(old)
                migrated.update(selection=new,status='selected',visual_correction_applied=True)
            else:migrated.update(selection=None,status='search_pending')
            manifest['images'].pop(identity);manifest['images'][g['id']]=migrated
            changes.append({'image_id':g['id'],'before':old,'after':new,'reason':'Cartoon-only medium is a screen series; replace a book-catalogue fallback with the actual series poster.','reviewed_on':c.TODAY})
    targeted={'Horizon Zero Dawn':None,'Surviving Mars':None,'BioShock':None,
      'Transformers':'Transformers: War for Cybertron',
      'Star Wars':'Star Wars: Episode III – Revenge of the Sith'}
    records={r['id']:r for r in c.baseline()}
    sources={x['id']:x for x in c.read(c.ROOT/'data/sources.json')['sources']}
    for identity,item in manifest['images'].items():
        old=item.get('selection') or {};new=None;reason=None
        if item['title'] in targeted and not item.get('visual_correction_applied'):
            g=copy.deepcopy(item)
            if targeted[item['title']]:g['title']=targeted[item['title']]
            if item['title']=='Star Wars':
                g['kind']='movie'
                if item['kind']=='movie':g['title']='Star Wars: Episode II – Attack of the Clones'
            g['source_ids']=list(dict.fromkeys(s for rid in g['record_ids'] for s in records[rid]['source_ids']))
            g['wiki_candidates']=c.wiki_candidates(g,sources)
            pages=c.wiki_bulk(g['wiki_candidates'])
            new=c.wiki_pick(g,pages)
            if item['title'] in ('Horizon Zero Dawn','Surviving Mars','BioShock'):
                try:new=c.steam_pick(g) or new
                except Exception:pass
            reason='Visual/title review: reject similarly named documentary, talk show, different game, or different Transformers continuity; select the actual game/film.'
        elif item['kind']=='anime' and old.get('provider')=='wikipedia' and not item.get('visual_correction_applied'):
            try:new=kitsu_pick(item)
            except Exception:pass
            reason='Use the actual animated-series poster instead of a source novel/manga cover or film adaptation.'
        elif item['title']=='Astro Boy' and item['kind']=='manga' and not item.get('visual_correction_applied'):
            try:new=kitsu_pick(item)
            except Exception:pass
            reason='Use original manga volume cover instead of isolated character illustration.'
        if new and new['source_url']!=old.get('source_url'):
            item.setdefault('prior_selections',[]).append(old)
            item.update(selection=new,status='selected',visual_correction_applied=True)
            changes.append({'image_id':identity,'before':old,'after':new,'reason':reason,'reviewed_on':c.TODAY})
            c.log('visual_selection_correction',image_id=identity,reason=reason,before=old.get('title'),after=new['title'])
            c.write(c.RESEARCH/'manifest.json',manifest)
            print(item['title'],'->',new['title'],flush=True)
    previous=c.read(c.RESEARCH/'review-corrections.json',{'corrections':[]})
    previous['corrections']+=changes;c.write(c.RESEARCH/'review-corrections.json',previous)
    c.write(c.RESEARCH/'manifest.json',manifest)
    c.download(manifest,only_ids={x['image_id'] for x in changes})

if __name__=='__main__':main()
