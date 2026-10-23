"""Stage selected gap files while the main downloader handles other groups."""
import concurrent.futures, re, sys
import collect_images as c
from resolve_image_gaps import openlibrary_pick
sys.stdout.reconfigure(encoding='utf8')
manifest=c.read(c.RESEARCH/'manifest.json')
stage_kind='manual' if 'manual' in sys.argv[1:] else 'gap'
candidates=c.read(c.RESEARCH/f'{stage_kind}-candidates.json',{})
staged=c.read(c.RESEARCH/f'{stage_kind}-prepared.json',{})
items=[]
for identity,result in candidates.items():
    item=manifest['images'].get(identity);sel=result.get('selection')
    if not item or item['status'] not in ('search_pending','download_failed') or not sel or staged.get(identity,{}).get('local'):continue
    if item.get('visual_correction_applied'):continue
    if item['kind']=='book' and 'cartoon' in item['media']:continue
    expected=c.EXPECTED_AUTHORS.get(re.sub(r'\s*\([^)]*\)','',item['title']))
    if expected and sel.get('provider')=='openlibrary_bulk_archive' and not any(expected.lower() in a.lower() for a in sel.get('work_authors',[])):
        try:sel=openlibrary_pick(item)
        except Exception:sel=None
    if not sel:continue
    items.append({**item,'selection':sel})
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for n,(identity,local,error) in enumerate(pool.map(c.download_one,items)):
        item=next(i for i in items if i['id']==identity)
        staged[identity]={'selection':item['selection'],'local':local,'error':error}
        c.write(c.RESEARCH/f'{stage_kind}-prepared.json',staged)
        print(f'Staged gap {n+1}/{len(items)}: {item["title"]}: '+('prepared' if local else 'failed'),flush=True)
