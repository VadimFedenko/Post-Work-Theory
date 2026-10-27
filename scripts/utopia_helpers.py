"""Persistence helpers for independently reviewed utopian/dystopian annotations."""
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from popularity_helpers import POPULARITY_FIELDS

ROOT = Path(__file__).resolve().parents[1]
ANNOTATION_FIELDS = ('utopia_score', 'utopia_assessment')


def research_record(record):
    """Keep every pre-existing research value; image editing is a separate stage."""
    return {k: v for k, v in record.items() if k not in (*ANNOTATION_FIELDS, *POPULARITY_FIELDS, 'assets')}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


def apply_utopia_overlay(societies):
    path = ROOT / 'data/society-utopia.json'
    if not path.exists():
        return
    overlay = json.loads(path.read_text(encoding='utf-8'))
    ratings = overlay['assessments']
    if set(ratings) != set(societies):
        raise ValueError('Utopia overlay must cover exactly the retained society IDs')
    for identity, record in societies.items():
        annotation = ratings[identity]
        if digest(research_record(record)) != annotation['reviewed_record_sha256']:
            raise ValueError(f'Stale utopia assessment: {identity}; review the changed research first')
        record['utopia_score'] = annotation['score']
        record['utopia_assessment'] = deepcopy(annotation['assessment'])


def band(score):
    if score <= -.6:
        return 'strongly_dystopian'
    if score < -.2:
        return 'dystopian_leaning'
    if score <= .2:
        return 'mixed_or_unclear'
    if score < .6:
        return 'utopian_leaning'
    return 'strongly_utopian'
