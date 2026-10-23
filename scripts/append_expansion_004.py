"""Add missing popular franchise cases before assessing them, per 2026-10-17 steering."""
import json
from candidate_queue import ROOT, load_queue
original, previous, combined=load_queue()
assert len(combined)==920, 'One-time append after c0920'
rows=[
 ('Star Wars: The Mandalorian','Plazir-15 under its elected rulers and rehabilitated droids',['tv'],'Explicit leisure society; organics retain maintenance, administration and arts.'),
 ('Star Wars','Coruscant civilian society amid widespread droid service',['movie','cartoon','tv'],'Popular zero-variant comparison: droid capacity coexists with inequality and organic jobs; no universal floor inferred as fact.'),
 ('Star Wars: Andor','Narkina 5 prison manufacturing order',['tv'],'Explicit cheap-prisoner-versus-droid choice; coerced useful work as a zero variant.'),
 ('Marvel Cinematic Universe: Black Panther','Wakanda before the royal succession crisis',['movie'],'Vibranium technology and ordinary human occupations; best-guess technological-restraint/partial-transition comparison, not a claimed post-work utopia.'),
 ('Marvel: Fantastic Four','Latveria during Doctor Doom’s established rule',['comic'],'Robot-supported technological paternalism under a human sovereign; assess provision as a labeled inference.'),
 ('Marvel: X-Men','Krakoa during the early Quiet Council era',['comic'],'Self-sustaining biological habitats, pharmaceutical exports and mutant provision; functional biological-production analogy.'),
 ('Marvel: Spider-Man 2099','Nueva York under Alchemax corporate dominance',['comic'],'Corporate automation and preserved wage dependence; original 2099 scope, not every reboot or later nationalization.'),
 ('Star Wars','Geonosis’s living hive society and automated industry during the Clone Wars',['movie','cartoon'],'Explicit automated droid factories and biological hierarchy; alien-person proxy, before Imperial extermination.'),
]
assert len(rows)==8
new=[dict(id=f'c{n:04}',order=n,work=w,society=s,media=m,discovery_locations=['expansion-004:popular-franchise priority'],discovery_status='pending',metadata_verified=False,discovery_rationale=why) for n,(w,s,m,why) in enumerate(rows,921)]
path=ROOT/'data/candidates-expansion.json'
data=json.loads(path.read_text(encoding='utf-8'));data['candidates']=previous+new;data['candidate_count']=len(data['candidates'])
data.setdefault('tranches',[]).append(dict(id='expansion-004',first='c0921',last='c0928',count=8))
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Ordered expansion queue','','The original 784-candidate catalogue is immutable. Discovery entries are not assessed records. Current priority: popular multimedia franchises and best guesses; see user-clarifications.md.','','| ID | Work | Society | Discovery rationale |','| --- | --- | --- | --- |']
lines += [f"| {c['id']} | {c['work']} | {c['society']} | {c['discovery_rationale']} |" for c in data['candidates']]
(ROOT/'research/expansion-list.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
load_queue()
print(json.dumps(dict(added=8,first='c0921',last='c0928')))
