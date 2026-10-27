"""Append short-reference leads for the next fast pass, preserving both earlier tranches."""
import json
from candidate_queue import ROOT, load_queue
original, previous, combined = load_queue()
assert len(combined)==896, 'This one-time tranche follows c0896'
rows=[
 ('Riverworld','Resurrected human communities supported by technological grails','book','A short reference explicitly describes food, drink and cloth from keyed grails; coercive capture and ultimate provider authority require scope checks.'),
 ('The World of Tiers','The Lords’ technologically constructed universes','book','Philip José Farmer engineered worlds and elite provision lead; technological power alone is insufficient.'),
 ('The Silicon Man','Active human uploads in the MAPHIS environment','book','Charles Platt’s implemented uploaded life and administrator dependence; verify an enduring social unit rather than a proposed immortality project.'),
 ('The Million','Permanently awake Earth aristocrats and their robot-supported estates','book','Karl Schroeder: publisher confirms closed elite, short review confirms robot provision. Require material institutional difference from retained regular Lockstep communities.'),
 ('Lord of All Things','The realized nanobot-supported population','book','Andreas Eschbach, also Herr aller Dinge; distinguish actual late provision from one inventor’s potential or wealth.'),
 ('Five to Twelve','The machine-supported female-dominated social order','book','Edmund Cooper technological leisure/caste lead; one short reference and only a decisive clarification before skipping.'),
 ('The City Dwellers','The future city’s technological support and allocation','book','Charles Platt future social-economy lead; no full novel reconstruction if ordinary access is unclear.'),
 ('A Door into Ocean','The Sharers’ engineered biological commonwealth','book','Joan Slonczewski needs-based biotechnology lead; organic beings still performing useful work must remain visible.'),
 ('Vacuum Flowers','Earth’s Comprise and its human-derived residents','book','Michael Swanwick human-derived collective and material support lead; integration alone is not provision.'),
 ('Stations of the Tide','The Bureaucracy’s technologically supplied population','book','Michael Swanwick distinct agency/technological order; distinguish privileged agents from a supported community.'),
 ('Tomorrow and Tomorrow','The later human-derived technological society','book','Charles Sheffield long-term body/computation lead; stasis and immortality alone are not leisure or provision.'),
 ('Between the Strokes of Night','The S-space human communities','book','Charles Sheffield altered-timescale society; require actual active-person support rather than calendar sleeping ratios.'),
 ('Rite of Passage','The continuing Ship population','book','Alexei Panshin settled ship support and human duties lead; useful maintenance and initiation must remain explicit.'),
 ('A Million Open Doors','Nou Occitan and Caledony’s contrasting economic orders','book','John Barnes nano-production and cultural restriction lead. Broad discovery entry may split only on supported material differences.'),
 ('Stealing Worlds','Distributed machine-assisted economic networks','book','Karl Schroeder: production/ownership changes may differ from gig work; require actual goods/access mechanism.'),
 ('Kiln People','Humans using temporary human-derived doppel labor','book','David Brin productive substitution lead; active human-derived copies still do useful work and cannot be silently treated as robots.'),
 ("Logan’s Run — original novel",'The original novel’s computer-provided death-at-twenty-one society','book','Separate original continuity from retained film. A different death threshold alone may not warrant a second economic point.'),
 ("Logan’s Run — television",'The television City of Domes and its human council','tv','Possible control difference from the film’s machine government; verify domestic provision and the Council of Elders in a short episode/reference summary.'),
 ('Star Trek: Insurrection','The Ba’ku’s chosen agrarian technological restraint','movie','Known technically capable community deliberately farms and crafts; possible zero variant, not a general technological primitive society.'),
 ('Final Space','Gary’s continuing sentence aboard the Infinity','cartoon','Human prisoner receives shipboard machine support; verify duration and actual retained maintenance work before treating a tiny cohort as a society.'),
 ('Red Dwarf','The continuing living human crew supported by the ship','tv','Technological food and habitat support lead; sleeping or dead crew are not leisure residents and actual repairs remain useful work.'),
 ('I Was a Teenage Exocolonist','The functioning Stratospheric colony on Vertumna','game','Settled technological support and common allocation lead; keep contributions and branching endings distinct.'),
 ('Sufficiently Advanced','The Stardwellers’ material-access order','tabletop','A short indexed first-edition rulebook passage names an equalizing economy. Do not extend it to all Patent Office civilizations or read the full book to rescue it.'),
 ('Sufficiently Advanced','The Tao of History’s maintained historical societies','tabletop','Named in the short RPGnet review; distinguish actual supplied residents from avatars or apparent historical occupations.'),
]
assert len(rows)==24
old={(c['work'].casefold(),c['society'].casefold()) for c in combined}
assert all((r[0].casefold(),r[1].casefold()) not in old for r in rows)
new=[]
for n,(work,society,medium,reason) in enumerate(rows,897):
 new.append(dict(id=f'c{n:04}',order=n,work=work,society=society,media=[medium],
  discovery_locations=['expansion-003:short-reference discovery'],discovery_status='pending',metadata_verified=False,discovery_rationale=reason))
path=ROOT/'data/candidates-expansion.json'
data=json.loads(path.read_text(encoding='utf-8'))
data['candidates']=previous+new
data['candidate_count']=len(data['candidates'])
data.setdefault('tranches',[]).append(dict(id='expansion-003',first='c0897',last='c0920',count=24))
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Ordered expansion queue','', 'The original 784-candidate catalogue is immutable. These are unverified additional leads, not admitted objects. Process in ID order and save every disposition. Append later tranches; do not reuse IDs.','', '| ID | Work | Society | Discovery rationale |','| --- | --- | --- | --- |']
lines += [f"| {c['id']} | {c['work']} | {c['society']} | {c['discovery_rationale']} |" for c in data['candidates']]
(ROOT/'research/expansion-list.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
load_queue()
print(json.dumps(dict(added_unverified_leads=len(new),first=new[0]['id'],last=new[-1]['id'])))
