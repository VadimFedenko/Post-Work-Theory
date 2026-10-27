"""Load the immutable discovery catalogue plus an append-only expansion queue."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN_SHA256 = '84267b0f4bfce365af39b5bd2fec9544abe79afdf102a13897154e222acc6a60'

def load_queue():
    path = ROOT / 'data/candidates.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == FROZEN_SHA256, 'Frozen discovery catalogue changed'
    original = json.loads(path.read_text(encoding='utf-8'))['candidates']
    path = ROOT / 'data/candidates-expansion.json'
    extra = json.loads(path.read_text(encoding='utf-8'))['candidates'] if path.exists() else []
    all_candidates = original + extra
    assert [c['order'] for c in all_candidates] == list(range(1,len(all_candidates)+1))
    assert [c['id'] for c in all_candidates] == [f'c{i:04}' for i in range(1,len(all_candidates)+1)]
    return original, extra, all_candidates
