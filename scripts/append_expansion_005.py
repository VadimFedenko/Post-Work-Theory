"""Append three strongly relevant popular-franchise leads before analysis."""
import json
from candidate_queue import ROOT,load_queue
original,previous,combined=load_queue()
assert len(combined)==928,'One-time append after c0928'
rows=[
 ('Halo','Created-supported Balaho and its living Unggoy residents',['game'],'Clear reference describes food, shelter, medicine and automated agricultural support; useful organic work continues.'),
 ('Transformers One','Iacon under Sentinel’s forced-mining hierarchy',['cartoon','movie'],'Distinct film continuity: artificial deprivation and removed transformation cogs preserve a forced labor class.'),
 ('Transformers One','Iacon after restored Energon flow and transformation cogs',['cartoon','movie'],'Realized ending restores a freely flowing material resource; separate from prewar Aligned Cybertron and from Sentinel’s order.'),
]
new=[dict(id=f'c{n:04}',order=n,work=w,society=s,media=m,discovery_locations=['expansion-005:popular-franchise material mechanisms'],discovery_status='pending',metadata_verified=False,discovery_rationale=why) for n,(w,s,m,why) in enumerate(rows,929)]
path=ROOT/'data/candidates-expansion.json';data=json.loads(path.read_text(encoding='utf-8'))
data['candidates']=previous+new;data['candidate_count']=len(data['candidates'])
data.setdefault('tranches',[]).append(dict(id='expansion-005',first='c0929',last='c0931',count=3))
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Ordered expansion queue','','The original 784-candidate catalogue is immutable. Discovery entries are not assessed records. Current priority: popular multimedia and explicit best guesses; see user-clarifications.md.','','| ID | Work | Society | Discovery rationale |','| --- | --- | --- | --- |']
lines += [f"| {c['id']} | {c['work']} | {c['society']} | {c['discovery_rationale']} |" for c in data['candidates']]
(ROOT/'research/expansion-list.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
load_queue();print(json.dumps(dict(added=3,first='c0929',last='c0931')))
