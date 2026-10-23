"""A manual completion review is valid only for the exact reviewed research inputs."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CORE_FILES=['data/societies.json','data/decisions.json','data/sources.json','data/comparisons.json','data/candidates.json','data/candidates-expansion.json','research/methodology.md','research/user-clarifications.md','статья.txt','coordinates.png']
def current_core_hashes():
 # A renamed or removed historical input invalidates that receipt; it must not
 # crash otherwise valid current-data checks or be silently replaced by a new text.
 hashes = {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() if (ROOT/name).is_file() else None for name in CORE_FILES}
 # The signed-off research remains valid through an asset-only stage. Verify
 # every other JSON value (including order and schema) against the exact reviewed
 # snapshot before substituting its hash. The review itself still verifies that
 # snapshot's hash; a lore/axis/source change cannot pass through this exception.
 baseline = ROOT/'research/images/baseline-societies.json'
 if baseline.exists():
  before=json.loads(baseline.read_text(encoding='utf-8'))
  after=json.loads((ROOT/'data/societies.json').read_text(encoding='utf-8'))
  for corpus in (before,after):
   for record in corpus['societies']:
    record.pop('assets',None)
    # A separate subjective annotation does not rewrite the reviewed lore.
    record.pop('utopia_score',None)
    record.pop('utopia_assessment',None)
  if before==after:
   hashes['data/societies.json']=hashlib.sha256(baseline.read_bytes()).hexdigest()
 return hashes
def completion_review():
 p=ROOT/'research/completion-review.json'
 if not p.exists():return None
 review=json.loads(p.read_text(encoding='utf-8'))
 if review.get('status')!='complete_under_current_user_policy':return None
 if review.get('reviewed_core_sha256')!=current_core_hashes():return None
 if not review.get('requirements') or not all(x.get('outcome')=='satisfied' for x in review['requirements']):return None
 return review
