"""Apply staged gap/manual selections without retrying unrelated failed URLs."""
import re, sys
import collect_images as c
from resolve_image_gaps import openlibrary_pick
sys.stdout.reconfigure(encoding='utf8')
m=c.read(c.RESEARCH/'manifest.json');changed=set()
for item in m['images'].values():
    sel=item.get('selection') or {}
    expected=c.EXPECTED_AUTHORS.get(re.sub(r'\s*\([^)]*\)','',item['title']))
    if item['status']=='prepared' and sel.get('provider')=='openlibrary_bulk_archive' and expected and not any(expected.lower() in a.lower() for a in sel.get('work_authors',[])):
        # A previously staged result cannot become valid merely by downloading.
        c.log('reject_prepared_wrong_book_author',image_id=item['id'],authors=sel.get('work_authors'),expected=expected)
        item.update(status='search_pending',qa_issue='Catalogue book author does not match the assessed work.')
        try:new=openlibrary_pick(item)
        except Exception:new=None
        if new:item.update(selection=new,status='selected');changed.add(item['id'])
for kind in ['gap','manual']:
    candidates=c.read(c.RESEARCH/f'{kind}-candidates.json',{})
    staged=c.read(c.RESEARCH/f'{kind}-prepared.json',{})
    for identity,result in candidates.items():
        item=m['images'].get(identity);sel=result.get('selection')
        if not item or not sel or item['status']=='prepared' and not result.get('force_review'):continue
        if item['status']=='prepared' and sel['source_url']==item.get('selection',{}).get('source_url'):continue
        expected=c.EXPECTED_AUTHORS.get(re.sub(r'\s*\([^)]*\)','',item['title']))
        if kind=='gap' and expected and sel.get('provider')=='openlibrary_bulk_archive' and not any(expected.lower() in a.lower() for a in sel.get('work_authors',[])):continue
        if kind=='gap' and item['status']=='download_failed' and sel['source_url']==(item.get('selection') or {}).get('source_url'):continue
        item.setdefault('prior_selections',[]).append(item.get('selection'))
        for field in ('visual_review','visual_reviewed_on','contact_sheet'):item.pop(field,None)
        if m.get('visual_quality_review'):m['visual_quality_review']['status']='needs_review'
        item.update(selection=sel,status='selected');changed.add(identity)
        prepared=staged.get(identity,{})
        if prepared.get('local') and prepared.get('selection',{}).get('source_url')==sel['source_url']:
            item.update(status='prepared',local=prepared['local'],prepared_at=c.now())
        c.log('apply_curated_candidate',image_id=identity,provider=sel['provider'],source_url=sel['source_url'],staged=item['status']=='prepared')
c.write(c.RESEARCH/'manifest.json',m)
c.download(m,only_ids=changed)
c.validate()
