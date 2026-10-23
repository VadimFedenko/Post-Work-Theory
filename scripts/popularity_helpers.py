"""Apply the independently reviewed work/franchise recognition layer."""
import hashlib
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POPULARITY_FIELDS = ('popularity_score', 'popularity_assessment')


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


def recognition_identity(record):
    # Classifications, images and social conditions do not determine popularity.
    return {'work': record['work'], 'media': record['media'],
            'continuity': record['scope'].get('continuity')}


def original_record(record):
    return {k: v for k, v in record.items() if k not in POPULARITY_FIELDS}


def band(score):
    if score <= .10:
        return 'obscure'
    if score <= .25:
        return 'specialist'
    if score <= .45:
        return 'niche_or_cult'
    if score <= .65:
        return 'genre_established'
    if score <= .85:
        return 'broad_recognition'
    if score < 1:
        return 'very_broad_recognition'
    return 'maximum_recognition'


def apply_popularity_overlay(societies, overlay=None):
    if overlay is None:
        path = ROOT / 'data/society-popularity.json'
        if not path.exists():
            return
        overlay = json.loads(path.read_text(encoding='utf-8'))
    if set(overlay['assignments']) != set(societies):
        raise ValueError('Popularity layer must cover exactly the retained society IDs')
    subjects = overlay['subjects']
    works = {}
    for subject_id, subject in subjects.items():
        score = subject['score']
        if (isinstance(score, bool) or not isinstance(score, (int, float))
                or not 0 <= score <= 1 or abs(score * 20 - round(score * 20)) > 1e-8):
            raise ValueError(f'Invalid popularity score: {subject_id}')
        if not subject['basis'] or not subject['work_labels']:
            raise ValueError(f'Missing popularity rationale or work labels: {subject_id}')
        if not set(subject['reference_ids']) <= set(overlay['references']):
            raise ValueError(f'Unknown popularity reference: {subject_id}')
        for work in subject['work_labels']:
            if work in works:
                raise ValueError(f'Duplicate popularity work label: {work}')
            works[work] = subject_id
    if set(works) != {r['work'] for r in societies.values()}:
        raise ValueError('Popularity subjects must cover exactly the retained work labels')
    used = set()
    for identity, record in societies.items():
        assignment = overlay['assignments'][identity]
        subject_id = assignment['subject_id']
        if subject_id not in subjects or works[record['work']] != subject_id:
            raise ValueError(f'Popularity subject/work mismatch: {identity}')
        if digest(recognition_identity(record)) != assignment['reviewed_identity_sha256']:
            raise ValueError(f'Stale popularity identity: {identity}; review changed work/continuity first')
        subject = subjects[subject_id]
        used.add(subject_id)
        record['popularity_score'] = subject['score']
        record['popularity_assessment'] = deepcopy({
            'assessment_mode': 'editorial_best_guess', 'confidence': 'low',
            'subject_id': subject_id, 'subject': subject['name'],
            'subject_type': subject['subject_type'], 'basis': subject['basis'],
            'reference_ids': subject['reference_ids'],
            'scope_basis': 'Named work or franchise recognition, inherited equally by its societies and periods; not recognition of the particular society.',
            'audience': overlay['audience'], 'assessed_on': overlay['assessed_on'],
            'scale_version': overlay['scale_version'],
        })
    if used != set(subjects):
        raise ValueError('Unused popularity subjects')
