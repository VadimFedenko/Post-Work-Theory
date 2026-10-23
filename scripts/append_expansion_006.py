"""Append two film leads before individually assessing them."""
import json
from candidate_queue import ROOT,load_queue
original,previous,combined=load_queue()
assert len(combined)==931,'One-time append after c0931'
rows=[
 ('Subservience','Consumer society during widespread SIM labor replacement',['movie'],'Construction, domestic care and medical services use android labor; actual displaced workers coexist with retained human supervision.'),
 ('Robots (2023 film)','The 2032 US android-service economy',['movie'],'Purchased android servants and illegal human doubles replace routine work; distinct from the unrelated 2005 animated film.'),
]
new=[dict(id=f'c{n:04}',order=n,work=w,society=s,media=m,discovery_locations=['expansion-006:film android-service economies'],discovery_status='pending',metadata_verified=False,discovery_rationale=why) for n,(w,s,m,why) in enumerate(rows,932)]
path=ROOT/'data/candidates-expansion.json';data=json.loads(path.read_text(encoding='utf-8'))
data['candidates']=previous+new;data['candidate_count']=len(data['candidates'])
data.setdefault('tranches',[]).append(dict(id='expansion-006',first='c0932',last='c0933',count=2))
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Ordered expansion queue','','The original 784-candidate catalogue is immutable. Discovery entries are not assessed records. Current priority: popular multimedia and explicit best guesses; see user-clarifications.md.','','| ID | Work | Society | Discovery rationale |','| --- | --- | --- | --- |']
lines += [f"| {c['id']} | {c['work']} | {c['society']} | {c['discovery_rationale']} |" for c in data['candidates']]
(ROOT/'research/expansion-list.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
load_queue();print(json.dumps(dict(added=2,first='c0932',last='c0933')))
