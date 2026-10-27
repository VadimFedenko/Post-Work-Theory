"""Report the scope of current evidence without pretending structure proves fictional lore."""
import hashlib,json,re
from collections import Counter
from pathlib import Path
from completion_state import completion_review
ROOT=Path(__file__).resolve().parents[1]
if (ROOT / 'data/taxonomy.json').exists():
 from article_checkpoint import audit_current
 audit_current()
 raise SystemExit(0)
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
R=read('data/societies.json')['societies'];S=read('data/sources.json')['sources'];D=read('data/decisions.json')['decisions'];Q=read('research/reassessment-queue.json')['queue']
sid={s['id'] for s in S}
completed_review=completion_review()
image_overlay=read('data/society-assets.json')['assets'] if (ROOT/'data/society-assets.json').exists() else None
checks={
 'count_in_requested_500_1000_range':500<=len(R)<=1000,
 'all_three_coordinates_numeric':all(all(isinstance(v,(int,float)) for v in r['axis'].values()) for r in R),
 'all_descriptions_two_paragraphs_110_words':all('\n\n' in r['description'] and len(r['description'].split())>=110 for r in R),
 'english_name_description_no_cyrillic':all(not re.search('[А-Яа-яЁё]',r['name']+' '+r['description']) for r in R),
 'all_records_have_registered_sources':all(r['source_ids'] and set(r['source_ids'])<=sid for r in R),
 'all_sources_have_access_scope_and_limits':all(s.get('read_scope') and s.get('limitations') and s.get('access_method') for s in S),
 'all_records_reviewed_against_gathered_evidence':all(r['review']['status']=='reviewed' for r in R),
 'all_best_guesses_separate_facts_assumptions':all(r.get('canon_facts') and r.get('editorial_assumptions') and r.get('qualification_basis') for r in R if r.get('assessment_mode')=='best_guess'),
 'zero_variants_separately_marked':all((r['record_type']=='zero_variant')==(r['regime_primary']==0) for r in R),
 'all_image_assets_match_the_current_stage':all(r['assets']==image_overlay.get(r['id']) for r in R) if image_overlay is not None else all(r['assets']==dict(status='deferred',poster=None,icon=None) for r in R),
 'frozen_784_catalogue_hash_unchanged':hashlib.sha256((ROOT/'data/candidates.json').read_bytes()).hexdigest()=='84267b0f4bfce365af39b5bd2fec9544abe79afdf102a13897154e222acc6a60',
 'current_policy_legacy_review_queue_exhausted':not Q,
 'manual_completion_review_matches_current_inputs':completed_review is not None,
}
assert all(v for k,v in checks.items() if k not in {'current_policy_legacy_review_queue_exhausted','manual_completion_review_matches_current_inputs'})
flags=[]
for r in R:
 if re.search(r'\b(remains? unresolved|stays? unresolved|left unresolved|stays? null|remains? null)\b',r['description'],re.I):
  flags.append(dict(id=r['id'],resolution='Manual inspection: Not All Robots refers to uncertain sabotage, not an unresolved numeric coordinate.' if r['id']=='not-all-robots-bubble-families' else 'Requires contextual inspection'))
assert all(f['id']=='not-all-robots-bubble-families' for f in flags),flags
facts_flags=[r['id'] for r in R if any(re.search(r'\b(estimate|inferred|editorial|interpretation|plausible|likely|suggests?|best.guess|central scenario)\b|does not establish|not established|no .* established',f,re.I) for f in r.get('canon_facts',[]))]
assert not facts_flags,facts_flags
counts=dict(retained=len(R),post_work=sum(r['record_type']=='post_work' for r in R),zero_variants=sum(r['record_type']=='zero_variant' for r in R),complete_coordinates=sum(r['review']['coordinate_ready'] for r in R),explicit_best_guess=sum(r.get('assessment_mode')=='best_guess' for r in R),sources=len(S),legacy_current_policy_followups=len(Q),completed_outside_target_comparisons=sum('comparison_assessment' in d for d in D),duplicate_leads=sum(d['status']=='duplicate' for d in D),with_some_nonprose_medium=sum(bool(set(r['media'])-{'book','short_story','web_fiction','play'}) for r in R))
audit=dict(audited_on='2026-10-17',status='in_progress',counts=counts,checks=checks,media_counts_nonexclusive=dict(Counter(m for r in R for m in r['media'])),contextual_flags=flags,manual_corrections=['Revision 023 separates depicted facts from source silence and ending interpretation in four early records.','Revision 022 links the shared ordinary Bubblegum model without double counting.','Not All Robots sabotage uncertainty is legitimate plot uncertainty and is retained.','Revisions 024-026 retain fifty-nine game models with active-person denominators, selected configurations and projected continuations explicit.','Revision 025 broadens Solty Rei’s control interval to include the full autonomous-machine alternative; the central value is unchanged.','Revision 026 verifies first-game Call to Power nano-assembly, distinguishes Big Ape’s hologram from an AI ruler and links Startopia’s common original/remake economic model.'],limitations=['The program verifies data and editorial bookkeeping, not every external fictional claim.','Reviewed means a follow-up against gathered evidence, not independent peer review.','Many admissions and all numeric uncertainty scenarios remain explicitly provisional under the user’s best-guess policy.','The numerical minimum is met; older skip decisions still have current-policy follow-up work.'],goal_complete=False,next_reassessment=Q[0] if Q else None)
audit['manual_corrections'] += [
 'Revisions 027-030 retain fifty-four game, tabletop, television and comic models while completing two mechanism comparisons and linking one Nova Praxis material-model duplicate.',
 'Necron person scope excludes mindless Warriors and dormant identities; biological Kin participation is not inferred from Ironkin staffing.',
 'The Metabaron fuel monopoly is corrected to its rebuilt second-cycle regime, and Edena gains author-level artificial-food provenance.',
 'Television Logan’s Run uses human council control; Gary’s satellite-repair sentence uses Galaxy One and counts actual work.',
 'The Patent Office’s Transcendental employers and molecular fabrication are checked in its primary sample; fourteen civilizations are not merged into one household economy.',
 'Revisions 031-034 retain forty-five literary models from fifty reassessed leads, with one two-scope split, five completed mechanism comparisons and one provider-model duplicate.',
 'Morthanveld AI restraint is corroborated; Azad’s game-specific computer rule is not generalized and Chelgrians have a pre-reform scope.',
 'The Haldeman low-technology lead is corrected to the 2252 theocracy; short workweeks, robot founding and enhanced-animal service are not false participation statistics.',
 'Digient platform/care expenses, Craker reduced agricultural needs, actual Visitors gifts and Tralfamadorian internal legend are separated from universal welfare claims.',
 'All the Traps of Earth has two explicitly different access units; Way Station and wordmill labor are narrow continuing institutions rather than whole heterogeneous economies.',
 'Revisions 035-038 retain forty-seven further literary models from forty-nine reassessed decisions, with two completed mechanism comparisons.',
 'Living household scenarios, useful training/craft/care and scarcity coordination are distinguished from death, short hours and wage status.',
 'Saturn’s free basics are directly checked in the primary orientation passage and kept distinct from destructive inner-system Economics 2.0.',
 'Quiet and gogol work counts as active human-derived labor; Puppets are biological humans, while android/metahuman societies have explicit synthetic-person proxies.',
 'Atlanta and First Camp gain identified local scopes, Conjoiner oversight hours are not a participation census and Vigilance archive corroboration does not invent its origin.',
 'Revisions 039-043 retain sixty-five literary models from sixty-eight reassessed leads, with two completed mechanism comparisons and one corrected duplicate.',
 'Fountainhead resource-rights trade, developed Adamist mechanoids and Ocisen fleet scope gain targeted corroboration; biological or uncertain provider identity is not automatically AI sovereignty.',
 'Apex is corrected to a human-derived takeover scenario, Prime bodies are not automatically separate minds and Exodus support is explicitly reconstructed.',
 'Neptunian market scarcity and Silent replication/suspension use corrected author-hosted volumes; Superluminal does not invent a completed postwar regime.',
 'Early Boppers, Moldies and human Earth have separate periods; Seed and Shockwave Rider successors are projections, while Drummers and the Count Zero maker do real work.',
 'Agency timelines, awake privileged clan residents, Holy Fire ration versus medicine access, Rizome associates and combat-artist work have explicit limits.',
 'Hegemony, Core, actual Ousters and Pax are not merged; earlier orbital post-humans are historical, Extro is transient, and passive host substrate is not automatically a behavioral occupation.',
 'Revisions 044-047 retain fifty-six models from sixty reassessed leads and link four shared-model duplicates; revision 048 strengthens a sourced description without changing axes.',
 'Active Bob identities, named Landing colonists, biological uplift/bioform workers, simulated Imir identities and independent robots have explicit denominators rather than backup/body/extinction shortcuts.',
 'ART crew support is not a universal university floor; Con Dao researchers and captive fishing labor have different access and control. Sentient trains and android professionals still work.',
 'Quoted Set My Heart to Five passages establish bot dentistry and laws reserving other occupations for humans; the claim is not broadened to every protected job being unnecessary.',
 'Primary Orion’s Arm entries confirm inhabited Caretaker exceptions and AI/virtual Panvirtuality citizens; ecological protection and computronium counts are not human welfare statistics.',
 'Reynolds national welfare baselines are linked rather than counted again; Mechasm’s horizon is projected and the false Prize of Peril public-income guess is discarded.',
]
if completed_review:
 audit.update(status='complete_under_current_user_policy',goal_complete=True,limitations=completed_review['limitations'],completion_review='completion-review.json',conservative_resident_scope_subset=completed_review['counts']['conservative_resident_scope_subset'])
 audit['manual_corrections']+=completed_review['manual_completion_corrections']
(ROOT/'research/quality-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Research quality checkpoint — 2026-10-17','',(f"The research stage is complete under the recorded best-guess policy: **{len(R)} retained records**, all with three numeric coordinates. The completed scope/source/coverage evidence is in [completion-review.md](completion-review.md). This does not make editorial interpretations canonical or independently peer reviewed." if completed_review else f"The numerical minimum is met: **{len(R)} retained records**, all with three numeric coordinates. The goal remains active because completion review is still open. This audit does not equate a structural pass with verified fiction."),'','| Requirement / check | Evidence |','| --- | --- |']
lines += [f"| {k} | {'Verified in saved data' if v else 'Open: '+str(len(Q))+' legacy decisions remain'} |" for k,v in checks.items()]
lines += ['','The frozen discovery list, source and record identities, intervals, decision links, splits and synthetic-person metadata are also checked by `scripts/validate_data.py`. A clean rebuild is tested separately.','','## Manual review findings','','- Four early fact lists contained absence-of-evidence or an ending interpretation. Revision 023 replaces those with depicted facts and preserves the interpretation as assumptions.','- The shared ordinary Bubblegum original/reboot economy is counted once; distinct autonomous-crisis plots are not silently merged.','- The phrase “remains unresolved” in Not All Robots concerns sabotage, not a missing coordinate. It is correctly retained.','','## Limits and remaining work','']
limit_index=lines.index('## Limits and remaining work')
lines[limit_index:limit_index]=['- Revisions 024-026 preserve active-person limits and explicit projections across fifty-nine game models. Call to Power’s first-game technology and Big Ape’s figurehead status receive targeted checks.','- Solty Rei’s machine-controller alternative is included in the widened uncertainty interval; its central value is unchanged.','- Startopia’s shared original/remake service model is counted once, with differing plots and precise rules left separate.','']
limit_index=lines.index('## Limits and remaining work')
lines[limit_index:limit_index]=['- Revisions 027-030 add fifty-four multimedia models with explicit active populations. Mindless Necron units, inactive copies, cryosleep and dead clones are excluded from leisure counts.','- The Metabaron’s fuel monopoly is scoped to the rebuilt second-cycle regime; Edena’s artificial-food conditioning gains author-level provenance.','- Television Logan’s Run has human rulers; Gary’s actual satellite-repair sentence is aboard Galaxy One.','- The Patent Office sample confirms fabrication and Transcendental AI employers without merging fourteen civilizations; Nova Praxis Purists do not add a duplicate compiler-access class.','']
limit_index=lines.index('## Limits and remaining work')
lines[limit_index:limit_index]=['- Revisions 031-034 preserve forty-five literary cases with explicit interpretations. Morthanveld AI restraint and the 2252 technology-shunning theocracy receive targeted corroboration.','- Short hours, robot founding, enhanced-animal service, private digient learning and reduced Craker agriculture are not converted into false labor percentages.','- All the Traps of Earth has two distinct access units, and its frontier continuation is labeled as a projection. Way Station and wordmills have narrow actual work-unit scopes.','- Chemical illusion, heterogeneous steering and autonomous weapons ecology have completed comparisons; they are not unresolved household-law holds. Tralfamadorian creator history remains an internal legend.','']
limit_index=lines.index('## Limits and remaining work')
lines[limit_index:limit_index]=['- Revisions 035-038 add forty-seven literary models with explicit household, institution and active-person scopes. Death, private play, skills and wages are not shortcut participation measures.','- Saturn’s free necessities are verified in the primary text and remain distinct from Economics 2.0 exclusion.','- Quiet and gogol activity remains human-derived work; Puppets are biological engineered people. Android/metahuman proxies are not literal human rates.','- Atlanta and First Camp have identified local populations and periods. Conjoiner oversight hours are not a census, and Vigilance origin is left uncertain despite archive corroboration.','']
limit_index=lines.index('## Limits and remaining work')
lines[limit_index:limit_index]=['- Revisions 039-043 add sixty-five models from sixty-eight reassessed leads, with two completed comparisons and one corrected duplicate. They preserve explicit claim-based, historical, projected and narrow working-unit scopes.','- Fountainhead resource-rights trade and developed Adamist mechanoids gain bounded sources; High Angel and Tranquillity provider identity is not assumed to be AI. Prime collective identities are not a census of controlled bodies.','- The Phoenix Exultant and The Golden Transcendence now have separate correct primary pointers. Silent sleeping residents are excluded, and Superluminal does not invent a concluded postwar society.','- Agency timelines and privileged/working cohorts remain separate. Rations do not imply equal premium medicine, automated recording does not abolish performance work and a single active box-maker uses discrete person scenarios.','- Pre-Fall Hegemony, Core, actual Ousters and Pax have separate scopes. Earlier orbital post-humans are reconstructed before slaughter; Extro is transient. Passive neural substrate use is not automatically an active human occupation.','']
limit_index=lines.index('## Limits and remaining work')
lines[limit_index:limit_index]=['- Revisions 044-047 retain fifty-six further models from sixty old holds, linking four shared-model duplicates. Revision 048 adds a targeted source-based wording correction.','- Bob identities, bioforms, simulated colonists, humanoid employees and robot survivors remain active persons; backups, dead humans and repeated simulation runs do not fabricate a leisure cohort.','- ART supplies a working crew; Con Dao research and captive fishing have distinct access. Set My Heart to Five has direct quoted evidence for bot dentistry and human-reserved jobs, without a claim that every protected job is unnecessary.','- Primary Orion’s Arm references support the admitted inhabited preserve subset and active virtual citizens. Ecological protection is not a universal floor, and internal AI hierarchy remains separate from independence from organic owners.','- Repeated Reynolds welfare baselines are counted once. Mechasm’s final prospect stays projected; Triton’s legal food/shelter floor is direct while production remains uncertain. The Prize of Peril’s discovery public-income guess is rejected.','']
lines += ['- '+x for x in audit['limitations']]
lines += ['',f"Next: **{Q[0]['candidate_id']} — {Q[0]['work']}**." if Q else 'No legacy follow-ups remain.','', '[Full catalogue](society-catalogue.md) · [Current queue](reassessment-queue.json) · [Machine-readable audit](quality-audit.json) · [Methodology](methodology.md)','']
(ROOT/'research/quality-audit.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps(dict(counts=counts,checks=checks,next_reassessment=Q[0]['candidate_id'] if Q else None)))
