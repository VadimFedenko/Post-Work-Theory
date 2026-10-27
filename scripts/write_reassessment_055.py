"""Named-franchise completion review: actual media and human-derived controller alternatives."""
from copy import deepcopy
from best_guess_helpers import current_data,change,write_revision,dated_source,DATE
D=current_data();changes=[]
sources=[
 dated_source('src-edgerunners-official-nightcity','Cyberpunk: Edgerunners: Night City setting','CD PROJEKT RED / TRIGGER','https://www.cyberpunk.net/en/edgerunners','The first-series synopsis identifies Night City, a street kid’s survival through mercenary work, technology/body-modification obsession and an order marked by greed.','Only the released first animated series’ shared city model is linked; sequel announcements and manga are not automatically tagged or analyzed.',kind='official_setting_description',access='About the Show and first-series Story sections read'),
 dated_source('src-trek-firstcontact-official-economics','A Look at Money in Star Trek: First Contact’s future economics','StarTrek.com / Star Trek Magazine','https://www.startrek.com/en-un/news/a-look-at-money-in-star-trek-italian-style','The licensed official-site discussion identifies Picard and Lily’s First Contact exchange about future economics, alongside television examples and remaining monetary ambiguities.','Commentary, not a Federation census or proof every frontier community has identical conditions.',kind='official_commentary',access='Indexed television/movie economics discussion and First Contact paragraph read'),
]
for s in sources:changes.append(change(D,'sources',s))
r=deepcopy(D['societies']['cyberpunk-night-city'])
r['work']='Cyberpunk 2077 / Cyberpunk: Edgerunners';r['media']=['game','anime']
r['scope']['continuity']='The shared Night City setting of Cyberpunk 2077 and the released first Cyberpunk: Edgerunners series'
r['scope']['period']='The ordinary Night City order in the game and first animated series, without a transformative game ending'
r['source_ids']+=['src-edgerunners-official-nightcity']
r['description']='''Night City combines advanced machine intelligence with a sharp separation between protected wealth and exposed poverty. The game’s North Oak entry describes corporate-backed eviction followed by elite settlement. Edgerunners’ official synopsis places a street kid’s struggle to survive through mercenary work in the same technology-obsessed city. The weak guarantee point is a contextual reading of this shared material order, not an invented universal welfare statute.

 Human corporations and powerful institutions direct most productive resources, while independent AIs do not establish a citywide machine government. This zero variant preserves human labor and insecurity alongside technical capacity without claiming that all jobs could immediately disappear. The modest nonworking estimate counts useful paid services, maintenance, care, informal activity and creation, with dependents included and a wide interval. It is a person-participation estimate, not a fraction of working hours. The first anime and game share this ordinary city model; announced sequels, unrelated manga and transformative player endings are not silently merged.'''
r['canon_facts']=['The game’s North Oak entry describes corporate-backed eviction and later elite settlement.','The first Edgerunners synopsis places a street kid’s survival through mercenary work in Night City.']
r['editorial_assumptions']+=['The game and first anime share the ordinary city material model; this does not make all future installments or endings identical.','Severe exclusion weighs against strong universal provision, but the numeric point remains an editorial assessment.']
r['evidence']=[dict(claim=r['canon_facts'][0],source_ids=['src-cyber-north-oak'],locator='North Oak entry',kind='reference_fact'),dict(claim=r['canon_facts'][1],source_ids=['src-edgerunners-official-nightcity'],locator='About the Show and Story',kind='reference_fact')]
r['review'].update(date=DATE,method='Completion check of shared game/first-anime material scope against official synopsis and gathered game entry; facts separated from guarantee inference; no independent reviewer')
changes.append(change(D,'societies',r))

r=deepcopy(D['societies']['star-trek-federation-core']);r['source_ids']+=['src-trek-firstcontact-official-economics']
r['evidence'].append(dict(claim='Official-site commentary identifies the First Contact dialogue about the changed future economy.',source_ids=['src-trek-firstcontact-official-economics'],locator='First Contact Picard/Lily paragraph',kind='official_commentary'))
r['review'].update(date=DATE,method='Completion medium check: licensed official commentary corroborates the film tag alongside the gathered TNG civilian economy account; no independent reviewer')
changes.append(change(D,'societies',r))

r=deepcopy(D['societies']['masseffect-control-paragon-reconstruction'])
r['axis']['control']=-.5;r['axis_assessment']['control'].update(interval=[-1,.35],confidence='low',basis='The commanding intelligence derives from Shepard and operates through the Reapers. Machine sovereignty is the central interpretation, while concentrated human-derived person authority near zero remains credible; lack of citizen override alone does not decide origin.')
r['description']='''Control gives the transformed Shepard command of the Reapers, which help rebuild the galaxy and repair transport. This is large-scale productive assistance. The favorable guarantee estimate projects protection and access under the Paragon guardian reading rather than claiming the ending explicitly abolishes wages, guarantees universal housing or removes every postwar shortage.

 The control estimate now includes both machine sovereignty and concentrated human-derived authority. Its central negative point gives weight to independent Reaper coordination, but Shepard’s origin remains relevant: ordinary residents’ inability to override a ruler does not by itself make that ruler unrelated AI. The widened interval therefore includes the concentrated-person reference near zero. The moderate nonworking scenario counts useful reconstruction, care, science, maintenance and public creation despite machine support. The record excludes the coercive Renegade narration and other endings. Postwar household rules and participation remain explicit low-confidence projections, not a canonical census supplied by the game.'''
r['editorial_assumptions']+=['Human-derived concentrated authority near zero is a credible control alternative; absence of ordinary democratic override is not alone evidence of unrelated AI origin.']
r['regime_alternatives']=sorted(set(r.get('regime_alternatives',[])+[1]))
r['review'].update(date=DATE,method='Completion origin/authority check against gathered selected-ending sources; widened interval separates human-derived rule from unrelated AI; no independent reviewer')
changes.append(change(D,'societies',r))

r=deepcopy(D['societies']['cyberpunk-alt-blackwall-constructs'])
r['axis']['control']=-.7;r['axis_assessment']['control'].update(interval=[-1,.3],confidence='low',basis='The central value weights surrounding independent network AI power. Alt’s human-derived origin also permits concentrated person authority near zero; entrants lacking override is not sufficient by itself to classify every controller as unrelated AI.')
r['description']='''Joining Alt beyond the Blackwall offers a possible human-derived digital existence outside ordinary bodily employment. The selected ending establishes transfer, while continuing independent experience and resource access remain explicit assumptions. Computing support replaces physical food and shelter as the relevant material need, with precarious access rather than a universal right. Stored or absorbed engrams are not automatically independent residents.

 Control is estimated toward surrounding autonomous network power, with a widened interval including concentrated human-derived authority. Alt’s origin matters: entrants’ inability to command their environment does not alone prove that every ruler is unrelated AI. The moderate nonworking scenario counts useful computation, assistance, exploration, maintenance and public creation among active experiencing constructs. Inactive files and dead biological originals are excluded. The point is a conditional post-transfer model rather than a guaranteed digital paradise, and it does not assign identical rules to every territory beyond the Blackwall.'''
r['editorial_assumptions']+=['Alt’s human-derived origin leaves a concentrated-person alternative near zero; the negative central point weights surrounding independent AI power rather than lack of entrant democracy alone.']
r['regime_alternatives']=sorted(set(r.get('regime_alternatives',[])+[3]))
r['review'].update(date=DATE,method='Completion origin/authority check against gathered Blackwall and selected-ending sources; human-derived control alternative widened; no independent reviewer')
changes.append(change(D,'societies',r))
write_revision(55,changes,'Completion review adds actual Night City anime scope and official film-economy corroboration, separates Cyberpunk facts from guarantee inference and widens Alt/Control origins rather than equate autocracy with unrelated AI.')
