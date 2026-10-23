"""Transparent, individually supplied best guesses; no automatic lore or scoring."""
from copy import deepcopy
import json
from research_helpers import ROOT, scope, assessment, record, evidence, decision

DATE = '2026-10-17'
AXES = ('guarantees', 'control', 'nonworking')

def guessed_record(cid, rid, name, work, society, media, continuity, period,
                   population, exclusions, description, values, bounds, bases,
                   refs, regime, facts, assumptions, qualification,
                   zero=False, proxy=False, branch=None, alternatives=None):
    r = record(rid, cid, name, work, society, media,
        scope(continuity, period, population, exclusions, proxy=proxy,
              branch=branch, player_configurable=branch is not None),
        description, dict(zip(AXES, values)),
        {k: assessment(v, b, 'low', why, refs) for k,v,b,why in zip(AXES,values,bounds,bases)},
        0 if zero else regime, refs,
        [evidence(f, refs, 'Named setting, economy or ending passages; see source read_scope',
                  'reference_fact') for f in facts],
        assumptions, record_type='zero_variant' if zero else 'post_work',
        alternatives=alternatives, analogy=[regime] if zero else None)
    r.update(assessment_mode='best_guess', qualification_basis=qualification,
             qualification_confidence='low', canon_facts=facts,
             editorial_assumptions=assumptions)
    r['review'].update(date=DATE, method='Individual second pass separating reference facts from requested editorial best guesses; no independent reviewer')
    return r

def retained_decision(r, reason):
    return decision(r['candidate_id'], 'zero_variant' if r['record_type']=='zero_variant' else 'included',
        reason, r['source_ids'], society_id=r['id'], assessment_mode='best_guess', reassessed_on=DATE)

def current_data():
    return {key: {x['candidate_id'] if key=='decisions' else x['id']: x
                   for x in json.loads((ROOT/'data'/f'{key}.json').read_text(encoding='utf-8'))[key]}
            for key in ('sources','societies','decisions')}

def write_revision(number, changes, reason):
    path = ROOT/'research/revisions'/f'revision-{number:03}.json'
    path.parent.mkdir(exist_ok=True)
    body = dict(revision_id=f'revision-{number:03}', revised_on=DATE, reason=reason, changes=changes)
    if path.exists():
        assert json.loads(path.read_text(encoding='utf-8')) == body, 'Revision is immutable once written'
    else:
        path.write_text(json.dumps(body,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(revision=number,changes=len(changes))))

def change(data, collection, after):
    key = after['candidate_id'] if collection=='decisions' else after['id']
    return dict(collection=collection, before=deepcopy(data[collection].get(key)), after=after)

def dated_source(identity, title, author, url, claim, limitations, kind='secondary_reference', access='Bounded public reference sections read'):
    return dict(id=identity,title=title,author=author,url=url,kind=kind,accessed_on=DATE,
                access_method=access,read_scope=claim,limitations=limitations)

def write_new_batch(number, candidates, sources, records, notes):
    body = dict(batch_id=f'batch-{number:03}',researched_on=DATE,candidate_ids=candidates,
                sources=sources,societies=records,
                decisions=[retained_decision(r,r['qualification_basis']) for r in records],review_notes=notes)
    path=ROOT/'research/batches'/f'batch-{number:03}.json'
    if path.exists():
        assert json.loads(path.read_text(encoding='utf-8'))==body
    else:
        path.write_text(json.dumps(body,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(batch=number,records=len(records),decisions=len(body['decisions']))))
