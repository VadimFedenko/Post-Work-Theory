"""Completion review: unemployment is not all useful activity; dreams require active persons."""
from copy import deepcopy
from best_guess_helpers import current_data,change,write_revision,DATE
D=current_data();changes=[]
def finish(r,facts,assumptions,qualification):
 r.update(assessment_mode='best_guess',canon_facts=facts,editorial_assumptions=assumptions,qualification_basis=qualification,qualification_confidence='low')
 r['evidence']=[dict(claim=f,source_ids=r['source_ids'],locator='Previously gathered bounded primary passages; see source read_scope',kind='depicted_or_author_stated') for f in facts]
 r['review'].update(date=DATE,method='Completion follow-up against gathered primary evidence and denominator rules; no independent reviewer or new full-text read')
 changes.append(change(D,'societies',r))

r=deepcopy(D['societies']['manna-terrafoam'])
r['description']='''Robotic services and supplied housing and meals maintain Terrafoam residents outside ordinary employment. This weakens the wage link for the scoped compound population, while elite ownership, confinement and movement restrictions leave residents dependent. The guarantee point recognizes actual subsistence rather than calling necessities wholly absent, with long-term adequacy and autonomy still qualified.

 Concentrated human elite control remains near the ownership reference point. The nonworking best guess is lower than a near-total unemployment-based reading: useful care, mutual help, administration and voluntary creation count even without wages. The central eighty-percent scenario is illustrative, with a wide interval, rather than a canonical count of inactive people. Robotic task replacement supports a high estimate but does not establish that every displaced resident performs no useful activity. The population excludes wealthy outsiders and the earlier Manna-managed human workforce. The correction changes participation reasoning without inventing a national demographic census or removing the explicitly described compound support.'''
r['axis']['nonworking']=.8
r['axis_assessment']['nonworking'].update(interval=[.2,1],confidence='low',basis='Illustrative high nonworking scenario under robotic compound services; useful care, mutual help and voluntary creation remain work. Selection for unemployment is not a census of all useful activity.')
finish(r,['The bounded chapter describes supplied compound housing and meals, concentrated elite wealth and movement restrictions.'],['The eighty-percent nonworking point is a low-confidence editorial scenario, not an unemployment conversion.','Useful unpaid activity remains work, and the compound cohort is not the whole United States.'],'Retain the actual compound support model with unemployment separated from all useful activity.')

r=deepcopy(D['societies']['comarre-sleeping-enclave'])
r['description']='''Comarre maintains residents’ bodies while they undergo private machine-generated dream experiences. The participation point concerns those active conscious persons, rather than passive hibernation or elapsed sleep time. Self-repairing robots maintain the city, so material support lies near the strong end, qualified by dependence and the difference between sustained bodies and immortality.

 Conscious Engineers exercise substantial independent authority while retaining inherited purposes and responding to some human requests. A resident who awakens chooses the dream again, complicating a simple captivity account. The near-total nonworking point is an explicit best guess for private dreamers: useful shared mental production would still count as work, but private experience alone does not. Its interval is widened because the source does not supply a canonical census of every mental activity. The visiting investigator and inactive or nonconscious bodies are excluded. The ending’s hoped-for partnership is not treated as an already realized wider society.'''
r['scope']['population']='Active conscious human residents undergoing private machine-generated dream experiences while their bodies are sustained in Comarre'
r['scope']['exclusions']+=['Inactive or nonconscious sleepers counted merely from body maintenance']
r['scope']['active_experience_requirement']='Only ongoing conscious dream persons are modeled; passive hibernation is not a leisure population'
r['axis_assessment']['nonworking'].update(interval=[.7,1],confidence='low',basis='Private conscious dream experience under automatic provision supports a high illustrative estimate; useful shared mental activity would count. Neither physical sleep duration nor unconscious bodies determine the rate.')
finish(r,['The previously read primary scenes describe an automatically maintained city, machine dreams and conscious Engineers.','An awakened resident chooses to return to the dream.'],['Only active conscious dream persons are included; passive sleep alone is not a beneficiary rate.','The participation estimate allows useful mental activity and is not a canonical census.'],'Retain the active conscious dream-support model with physical sleep distinguished from inactive hibernation.')
write_revision(53,changes,'Completion review corrects Manna’s unemployment-to-nonworking shortcut and makes Comarre’s active conscious-person requirement explicit; no new record is counted.')
