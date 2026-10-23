"""Validate ratings, original-value preservation and rebuild safeguards."""
import json
from collections import Counter
from copy import deepcopy
from utopia_helpers import ROOT, apply_utopia_overlay, band, digest, research_record
from popularity_helpers import POPULARITY_FIELDS


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def main():
    records = read('data/societies.json')['societies']
    overlay = read('data/society-utopia.json')
    index = read(overlay.get('review_index', 'research/utopia/review-index.json'))
    sources = {s['id'] for s in read('data/sources.json')['sources']}
    ids = [r['id'] for r in records]
    assert len(ids) == len(set(ids)) == len(index['records']) == 890
    assert ids == [r['id'] for r in index['records']]
    assert set(ids) == set(overlay['assessments'])
    for r, original in zip(records, index['records']):
        score, assessment = r['utopia_score'], r['utopia_assessment']
        saved = overlay['assessments'][r['id']]
        assert isinstance(score, (float, int)) and not isinstance(score, bool)
        assert -1 <= score <= 1 and abs(score * 20 - round(score * 20)) < 1e-8
        assert saved['score'] == score and saved['assessment'] == assessment
        assert digest(research_record(r)) == original['research_sha256'] == saved['reviewed_record_sha256']
        assert assessment['basis'] and assessment['confidence'] == 'low'
        assert assessment['assessment_mode'] == 'editorial_best_guess'
        assert assessment['source_ids'] and set(assessment['source_ids']) <= sources
        assert assessment['source_ids'] == r['source_ids']
        assert set(assessment.get('supplemental_source_ids', [])) <= set(overlay.get('supplemental_sources', {}))
        assert assessment['scale_version'] == overlay['scale_version']
        if assessment['rationale_code'] == 'U':
            assert -.2 <= score <= .2
    originals = [{k: v for k, v in r.items() if k not in ('utopia_score', 'utopia_assessment', *POPULARITY_FIELDS)} for r in records]
    assert digest(originals) == index['original_records_sha256'], 'Reviewed research or assets changed'
    # Run guards on copies; neither check edits the corpus or annotation overlay.
    missing = {r['id']: deepcopy(r) for r in records[1:]}
    try:
        apply_utopia_overlay(missing)
    except ValueError:
        pass
    else:
        raise AssertionError('Missing-record guard failed')
    stale = {r['id']: deepcopy(r) for r in records}
    stale[ids[0]]['axis']['guarantees'] += .01
    try:
        apply_utopia_overlay(stale)
    except ValueError:
        pass
    else:
        raise AssertionError('Stale-research guard failed')
    counts = Counter(band(r['utopia_score']) for r in records)
    summary = {
        'assessed_on': overlay['assessed_on'], 'records': len(records),
        'scale': overlay['scale'], 'bands': dict(counts),
        'zero_scores': sum(r['utopia_score'] == 0 for r in records),
        'range': [min(r['utopia_score'] for r in records), max(r['utopia_score'] for r in records)],
        'reviewed_research_and_assets_match_active_index': True,
        'active_review_index': overlay.get('review_index', 'research/utopia/review-index.json'),
        'complete_overlay_and_valid_sources': True,
        'missing_and_stale_input_guards_tested': True,
        'supplemental_sources': len(overlay.get('supplemental_sources', {})),
        'limitations': ['Subjective low-confidence judgments from the saved research, not canonical statistics.',
                       'Mixed and underdescribed conditions both use central values; the basis distinguishes them.'],
    }
    (ROOT / 'research/utopia/review-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Utopian / dystopian assessment', '',
             f'All **{len(records)} records** have an explicit editorial score. -1 = strong dystopia; 0 = mixed or unclear; +1 = strong utopia.', '',
             'The numerical wellbeing scores were reaffirmed after article alignment; classifications and selected axes changed in research revision 056. Images were preserved. [Methodology](methodology.md) · [Validation](review-summary.json)', '',
             '| Band | Records |', '| --- | ---: |']
    order = ('strongly_dystopian', 'dystopian_leaning', 'mixed_or_unclear', 'utopian_leaning', 'strongly_utopian')
    lines += [f'| {k} | {counts[k]} |' for k in order]
    lines += ['', 'All ratings are low-confidence editorial judgments. Scores concern particular populations, continuities and periods, not entire franchises.', '',
              '| ID | Society / period | Score |', '| --- | --- | ---: |']
    lines += [f"| {r['id']} | {r['name'].replace('|', '/')} | {r['utopia_score']:+.2f} |" for r in records]
    (ROOT / 'research/utopia/catalogue.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
