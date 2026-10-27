"""Freeze the evidence for the completed reference-led research stage.

This records the substantive completion review described in the report; mechanical
assertions support its bookkeeping and are not a claim of independent lore proof.
"""
import json,re,statistics
from collections import Counter
from pathlib import Path
from completion_state import ROOT,current_core_hashes
def read(name,key=None):
 x=json.loads((ROOT/name).read_text(encoding='utf-8'));return x[key] if key else x
R=read('data/societies.json','societies');D=read('data/decisions.json','decisions');S=read('data/sources.json','sources');Q=read('research/reassessment-queue.json','queue')
rmap={r['id']:r for r in R};smap={s['id']:s for s in S}
assert 500<=len(R)<=1000 and not Q and len(D)==933
assert all(d['status'] in {'included','zero_variant','duplicate','boundary_case'} for d in D)
assert all(d.get('current_policy_review') and d.get('comparison_assessment') for d in D if d['status']=='boundary_case')
assert all(r['source_ids'] and set(r['source_ids'])<=smap.keys() and r['review']['status']=='reviewed' for r in R)
assert all(all(isinstance(r['axis'][a],(int,float)) for a in ('guarantees','control','nonworking')) for r in R)
assert all(r['scope']['population'] and r['scope']['period'] and r['scope']['continuity'] for r in R)
assert all('\n\n' in r['description'] and len(r['description'].split())>=110 and not re.search('[А-Яа-яЁё]',r['description']+r['name']) for r in R)
assert len({r['description'] for r in R})==len(R)
assert all(r['evidence'] and r['uncertainties'] and r['axis_assessment'] for r in R)
assert all(r.get('canon_facts') and r.get('editorial_assumptions') and r.get('qualification_basis') for r in R if r.get('assessment_mode')=='best_guess')
assert all(r['assets']==dict(status='deferred',poster=None,icon=None) for r in R)
assert not any((ROOT/p).exists() for p in ['package.json','app','src'])

# A deliberately conservative counting proof. Many genuine communities fail this
# lexical rule; they remain fully retained and are not declared invalid by it.
resident=re.compile(r'\b(residents?|citizens?|inhabitants?|colonists?|passengers?|settlers?|population)\b',re.I)
specialist=re.compile(r'\b(crew|employees?|workers?|staff|family|families|household|single|subject|exhibit|maker|keeper|command|team|pilot|guild)\b',re.I)
subset=[r for r in R if resident.search(r['scope']['population']) and not specialist.search(r['scope']['population'])]
assert len(subset)>=500
scope_audit=dict(reviewed_on='2026-10-17',retained_records=len(R),conservative_resident_scope_subset=len(subset),other_records=len(R)-len(subset),selection='Explicit resident/citizen/inhabitant/colonist/passenger/settler/population wording, conservatively excluding specialist, household and single-person wording. This is a counting check, not a lore-verification classifier.',limitation='The remaining records include many valid societies as well as deliberately narrow institutions, households and person proxies. Failure of the counting rule is not a rejection. Every record still carries its actual population and assumptions.',records=[dict(id=r['id'],name=r['name'],population=r['scope']['population']) for r in subset])
(ROOT/'research/scope-audit.json').write_text(json.dumps(scope_audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

groups={
 'Cyberpunk':['cyberpunk-night-city','cyberpunk-alt-blackwall-constructs'],
 'The Matrix':['matrix-pod-humanity','matrix-zion-machine-supported-commons','matrix-io-human-synthient-cooperation','animatrix-human-machine-imports','animatrix-zero-one-synthetic-citizens'],
 'Star Wars':['starwars-plazir15-droid-leisure','starwars-coruscant-droid-zero','starwars-narkina5-cheap-labor-zero','starwars-geonosis-automated-hives'],
 'Star Trek':[r['id'] for r in R if 'Star Trek' in r['work']],
 'Marvel':['mcu-wakanda-technological-zero','marvel-latveria-doom-provision','marvel-krakoa-biological-commons','marvel2099-nuevayork-corporate-zero'],
 'DC':['dc-redson-brainiac-managed-zero','dc-krypton-silver-age-robot-support','allstar-kandor-protected-city','superman-brainiac-captive-kandor'],
 'Mass Effect':[r['id'] for r in R if r['id'].startswith(('masseffect-','andromeda-vault-'))],
 'Deus Ex':['deusex-helios-initial-merger','invisible-war-helios-union'],
 'BioShock':['bioshock-rapture-automated-zero','bioshock-columbia-finkton-zero'],
 'Recognizable anime examples':['psychopass-sibyl-japan','ghostshell-manga-unmanned-capitalism','ghostshell-sac-automated-inequality','ergoproxy-romdeau-supported-consumerism','appleseed-olympus-technocratic-provision','doraemon-chamocha-before-revolt','gundam00-veda-esf-transition'],
 'Popular screen examples':['walle-axiom','matrix-pod-humanity','mcu-wakanda-technological-zero','starwars-plazir15-droid-leisure'],
}
assert all(ids and set(ids)<=rmap.keys() for ids in groups.values())
coverage={name:dict(count=len(ids),record_ids=ids) for name,ids in groups.items()}
assert 'anime' in rmap['cyberpunk-night-city']['media']
assert rmap['psychopass-sibyl-japan']['axis']['control']>=0
assert rmap['manna-terrafoam']['axis']['nonworking']==.8
assert 'active_experience_requirement' in rmap['comarre-sleeping-enclave']['scope']
assert rmap['masseffect-control-paragon-reconstruction']['axis_assessment']['control']['interval'][1]>=0
assert rmap['cyberpunk-alt-blackwall-constructs']['axis_assessment']['control']['interval'][1]>=0

requirements=[
 ('Objective and conceptual inputs','Attachment objective, статья.txt and coordinates.png were read; the image and six article categories agree with the saved axis conventions.'),
 ('500–1000 analyzed objects',f'{len(R)} retained records, not discovery leads; {len(subset)} pass the deliberately conservative resident-community counting rule without relying on narrowly worded employee/individual cases.'),
 ('Ordered discovery and provenance','784 original candidate IDs remain frozen, 149 append-only leads complete the 933-candidate ledger; 106 base batches and 55 ordered revisions preserve complete before/after history.'),
 ('Named popular multimedia scope','Explicit coverage checks include Cyberpunk, Matrix, Star Wars, Star Trek, Marvel/DC, Mass Effect, Deus Ex, BioShock and known anime; the first Edgerunners series has an official anime setting source.'),
 ('English readable analysis','All 890 names/descriptions are English and each description has at least two paragraphs and 110 words. The source-backed argument and limits are included in the data.'),
 ('All three plot coordinates','Every record has numeric guarantees, control and nonworking values plus bounded assessments and source references. Values are editorial estimates rather than fictional census measurements.'),
 ('Article regimes and zero variants','Regimes 1–6 represent the six combinations in the article. Every zero variant is separately typed with regime 0, and its analogous regime remains visible.'),
 ('Useful work and person denominators','Descriptions and populations retain care, voluntary useful creation, assigned work and sentient-person activity. Review corrected Manna’s unemployment shortcut and Comarre’s active dream-person scope.'),
 ('Origin versus control','Sibyl remains human-brain collective authority; human-derived uploads are not automatically unrelated AI. Completion review widens Alt/Control alternatives while preserving actual autonomous-machine examples.'),
 ('Continuity, period and branch','All records have named continuity, period, population and exclusions; selected endings, hypothetical material consequences and player configurations carry their actual scope. Logan novel/film/TV and other important variants remain separate.'),
 ('Multivalued media','Every record has an allowed nonempty media array. Shared material models use multiple actual media; unrelated/unreleased adaptations are not inferred from franchise labels.'),
 ('Sources and limits','Every record links registered sources; all sources retain access method, date, bounded read scope and limitations. Indexed excerpts and reader interpretations are identified rather than represented as complete primary reads.'),
 ('Requested best guesses instead of lore skips','No needs_evidence or pending decisions remain. 853 records explicitly use best_guess; 37 earlier source-led records retain evidence, uncertainties and axis assessments. Contextual mechanisms are not represented as canonical laws.'),
 ('Distinctness and all dispositions','21 actual shared-model leads are linked, 29 identified different-mechanism comparisons have completed assessments outside the target, and materially different cultures/periods are split rather than silently merged.'),
 ('Quality follow-up','The completed current-policy pass revisits old holds individually. Targeted final reviews cover named franchises, employment versus useful activity, consciousness, controller origin, media and the Jupiter/New Mars source correction; review is not independent peer review.'),
 ('Research-only boundary and deferred images','Only research data/utilities/docs were produced. No website/app/deployment was built. All 890 asset fields explicitly defer poster/icon collection as the user allowed.'),
 ('Reproducibility','Merge, validation, checkpoint and quality-audit utilities pass. A final clean-rebuild hash check covers authoritative and generated outputs after this review is recorded.'),
]
review=dict(status='complete_under_current_user_policy',reviewed_on='2026-10-17',policy='Reference-led research with explicit best guesses, zero variants included, famous multimedia prioritized; no requirement to invent a canonical census or read entire obscure works.',review_method='Assistant case-by-case source-led passes plus targeted completion review; not independent peer review and not a guarantee that every fictional interpretation is uniquely correct.',counts=dict(retained=len(R),post_work=sum(r['record_type']=='post_work' for r in R),zero_variants=sum(r['record_type']=='zero_variant' for r in R),numeric_coordinates=len(R),explicit_best_guess=sum(r.get('assessment_mode')=='best_guess' for r in R),sources=len(S),conservative_resident_scope_subset=len(subset),completed_comparisons=29,duplicate_leads=21,remaining_reassessments=len(Q)),media_counts_nonexclusive=dict(Counter(m for r in R for m in r['media'])),franchise_coverage=coverage,description_word_counts=dict(minimum=min(len(r['description'].split()) for r in R),median=statistics.median(len(r['description'].split()) for r in R),maximum=max(len(r['description'].split()) for r in R)),manual_completion_corrections=['Revision 048: quoted human-reserved professions and bot dentistry.','Revision 049: earlier enslaved uploads are near Jupiter, distinct from New Mars.','Revisions 053–054: Manna useful activity and Comarre active dream persons; confidence metadata normalized.','Revision 055: actual Edgerunners anime scope, First Contact medium corroboration, positive Cyberpunk source facts and wider human-derived controller alternatives.'],requirements=[dict(requirement=a,outcome='satisfied',evidence=b) for a,b in requirements],limitations=['Coordinates and many institutional details are explicitly uncertain best guesses, as requested; they are not canonical statistics.','Some records are projected or historical reconstructions, and some are narrow household/work/proxy comparisons. Their actual scope is not a universal claim about an entire franchise.','Source references preserve what was read, including bounded indexes and criticism. This review does not claim all URLs are currently reachable or that the whole works were read.','Conscious synthetic/collective person cases are comparative and keep their assumptions visible.','Images remain deferred; no site or deployment is delivered.'],reviewed_core_sha256=current_core_hashes())
(ROOT/'research/completion-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Completed research-stage review — 2026-10-17','',f"**{len(R)} retained records: {review['counts']['post_work']} post-work/partial-transition models and {review['counts']['zero_variants']} separately marked zero variants.** All have three numeric coordinates. The 933-lead ledger has no remaining current-policy hold. The requested research stage is complete under the user’s explicit best-guess policy; images are deferred.",'',f"A deliberately conservative check finds **{len(subset)} records with explicit resident-community population wording**, excluding specialist/employee/household/single-person wording. Thus the minimum does not depend on counting every narrow example. This lexical counting check is not an independent lore verifier, and its other records are not declared invalid. See [scope-audit.json](scope-audit.json).",'', '## Requirement-by-requirement evidence','','| Requirement | Result and evidence |','| --- | --- |']
lines += [f'| {a} | Satisfied: {b} |' for a,b in requirements]
lines += ['', '## Named-franchise coverage','','| Group | Retained models |','| --- | ---: |']+[f'| {name} | {v["count"]} |' for name,v in coverage.items()]
lines += ['', 'Exact IDs, nonexclusive media counts and reviewed-file hashes are in [completion-review.json](completion-review.json). The source registry and ordered revisions preserve supporting evidence and complete prior values.','', '## Meaning of completion','',review['review_method'],'']+['- '+s for s in review['limitations']]
lines += ['', 'Rebuild: `merge_batches.py`, `validate_data.py`, `update_checkpoint.py`, `audit_research_checkpoint.py`. The completion marker becomes stale if a reviewed input changes; a new substantive review is then required.','', '[Catalogue](society-catalogue.md) · [Data](../data/societies.json) · [Progress](progress.md) · [Sources](../data/sources.json)','']
(ROOT/'research/completion-review.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps(dict(retained=len(R),conservative_resident_subset=len(subset),requirements=len(requirements),remaining_reassessments=len(Q),status=review['status'])))
