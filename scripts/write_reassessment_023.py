"""Quality pass: source silence and ending interpretation are not canonical world facts."""
from copy import deepcopy
from best_guess_helpers import current_data,change,write_revision,DATE
from research_helpers import evidence
D=current_data();changes=[]
rows=[
 ('evitable-conflict-earth',
  ['The Machines coordinate the world economy.','The accounts depict plant workers, layoffs and economic labor needs.'],
  'The bounded sources do not establish unconditional job-independent benefits; the favorable guarantee remains an interpretation of protective coordination.'),
 ('detroit-before-revolution',
  ['Androids perform service labor while treated as property before liberation.','The CTN report depicts human job losses and unemployment.'],
  'No universal material entitlement is asserted from the bounded references; unemployment is not an all-population nonworking rate.'),
 ('fallout-prewar-appalachia',
  ['Hornwright records seek to remove human mining labor through automation.','The Motherlode is an automated mining bot.','Corporate leadership seeks political collaboration.'],
  'Owner advantage and weak general guarantees are economic interpretations; source silence is not a canonical declaration that all assistance is absent.'),
 ('algebraist-mercatoria',
  ['The Mercatoria persecutes machine intelligence.','Machine refugees and refuge are part of the described setting.'],
  'A later political compromise is an interpretation of an open ending, not an implemented policy counted in this snapshot.'),
]
for rid,facts,caveat in rows:
 r=deepcopy(D['societies'][rid]);r['canon_facts']=facts
 if caveat not in r['editorial_assumptions']:r['editorial_assumptions'].append(caveat)
 existing={e['claim'] for e in r['evidence']}
 r['evidence'] += [evidence(f,r['source_ids'],'Named economic, terminal or narrative passages; source read_scope records access limits','reference_fact') for f in facts if f not in existing]
 r['review'].update(date=DATE,method=r['review']['method']+'; quality audit separates depicted facts from source absence and open-ending interpretation')
 changes.append(change(D,'societies',r))
write_revision(23,changes,'Correct four early canon_facts lists that mixed depicted facts with absence-of-evidence or ending interpretation. All coordinates, scopes and counted records are preserved. The Not All Robots sabotage uncertainty is inspected and correctly retained as plot uncertainty, not a missing coordinate.')
