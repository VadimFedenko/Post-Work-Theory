"""Complete the canonical duplicate pointer required by the data schema."""
from copy import deepcopy
from best_guess_helpers import current_data,change,write_revision
D=current_data();d=deepcopy(D['decisions']['c0479'])
assert d['status']=='duplicate' and d['society_id']=='futurama-earth-robot-work-zero'
d['duplicate_of']=d['society_id']
write_revision(16,[change(D,'decisions',d)],'Attach the schema-level duplicate_of pointer to the resolved Futurama family/vocation overlap; no additional society or score change.')
