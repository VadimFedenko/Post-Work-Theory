"""Keep newly marked editorial coordinate sets consistently low-confidence."""
from copy import deepcopy
from best_guess_helpers import current_data,change,write_revision
D=current_data();changes=[]
for key in ['manna-terrafoam','comarre-sleeping-enclave']:
 r=deepcopy(D['societies'][key])
 for a in r['axis_assessment'].values():a['confidence']='low'
 changes.append(change(D,'societies',r))
write_revision(54,changes,'Consistent best-guess metadata for the two completion-review records: source facts remain stated, while all editorial coordinate confidence labels use the conservative low setting required by the current schema.')
