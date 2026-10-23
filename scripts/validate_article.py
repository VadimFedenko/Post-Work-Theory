"""Validate article taxonomy, complete manual decisions and migration preservation."""
import hashlib
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERRIDES = {'walle-axiom': 5, 'manna-terrafoam': 2, 'fallout-institute': 2,
             'solaria-naked-sun': 4, 'psychopass-sibyl-japan': 5,
             'readyplayerone-debt-work-zero': 2}


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def choices():
    raw = (ROOT / 'research/article-alignment/manual-classification.txt').read_text(encoding='utf-8')
    tokens = ' '.join(s.split('#', 1)[0] for s in raw.splitlines()).split()
    assert len(tokens) % 2 == 0
    answer = {}
    for index, code in zip(tokens[::2], tokens[1::2]):
        assert int(index) not in answer
        answer[int(index)] = code
    return answer


def check_record(r, old, code, taxonomy):
    version = taxonomy['taxonomy_version']
    assert r['taxonomy_version'] == r['article_alignment']['version'] == version
    assert r['article_alignment']['article_sha256'] == taxonomy['article']['sha256']
    a = r['post_work_assessment']
    assert a['definition_version'] == version and a['manual_code'] == code
    assert a['confidence'] == 'low' and a['basis'] and a['participation_is_separate'] is True
    assert a['source_ids'] == r['source_ids']
    expected = taxonomy['manual_codes'][code]['record_type']
    assert r['record_type'] == expected
    number = {int(k): v for k, v in taxonomy['historical_number_mapping'].items()}
    primary = number[old['regime_primary']]
    if expected == 'zero_variant':
        primary = 0
    elif not primary:
        analogy = old.get('regime_analogy')
        options = analogy if isinstance(analogy, list) else [analogy]
        primary = next((number[x] for x in options if isinstance(x, int) and x), 2)
    assert r['regime_primary'] == OVERRIDES.get(r['id'], primary), r['id']
    assert (r['record_type'] == 'zero_variant') == (r['regime_primary'] == 0)
    for field in ('regime_alternatives', 'regime_analogy'):
        value = r.get(field)
        assert value is None or isinstance(value, (list, int))
        for item in value if isinstance(value, list) else [] if value is None else [value]:
            assert isinstance(item, int) and 0 <= item <= 6
    for field in ('record_type', 'regime_primary', 'regime_alternatives', 'regime_analogy'):
        assert r['legacy_classification'][field] == old.get(field)


def validate(write_report=True):
    taxonomy = read('data/taxonomy.json')
    export = read('data/societies.json')
    records = export['societies']
    baseline = read('research/article-alignment/baseline-societies.json')['societies']
    index = read('research/article-alignment/review-index.json')
    manual = choices()
    assert len(records) == len(baseline) == len(manual) == 890
    assert set(manual) == set(range(len(records)))
    assert export['schema_version'] == '1.2' and export['taxonomy_version'] == taxonomy['taxonomy_version']
    assert hashlib.sha256((ROOT / 'article.txt').read_bytes()).hexdigest() == taxonomy['article']['sha256'] == index['article_sha256'], 'Article changed; review classification rather than relabeling its hash'
    assert [r['id'] for r in records] == [r['id'] for r in baseline] == [r['id'] for r in index['records']]
    assert taxonomy['regimes'][2]['control'] == 'concentrated_human' and taxonomy['regimes'][2]['guarantees'] == 'weak'
    assert taxonomy['regimes'][3]['control'] == 'distributed_human' and taxonomy['regimes'][3]['guarantees'] == 'strong'
    for i, (r, old) in enumerate(zip(records, baseline)):
        check_record(r, old, manual[i], taxonomy)
        assert r['assets'] == old['assets'], ('Asset drift during article migration', r['id'])
        assert r['utopia_score'] == old['utopia_score'], ('Unreviewed wellbeing change', r['id'])
    expected_axes = {'manna-terrafoam', 'fallout-institute', 'solaria-naked-sun', 'psychopass-sibyl-japan'}
    assert {r['id'] for r, o in zip(records, baseline) if r['axis'] != o['axis']} == expected_axes
    byid = {r['id']: r for r in records}
    for identity, regime in {'brave-new-world-state': 1, 'orwell-oceania': 2,
                            'evitable-conflict-earth': 5, 'noon-earth': 3,
                            'star-trek-federation-core': 3, 'dune-post-jihad-imperium': 0,
                            'horizon-tribal-gaia-ecology-zero': 0,
                            'accelerando-early-human-transition': 4,
                            'accelerando-economics-two-human-remnant': 6,
                            'accelerando-saturn-free-basics': 3}.items():
        assert byid[identity]['regime_primary'] == regime, identity
    # A real migration regression: the former Federation type 2 must be rejected.
    position = next(i for i, r in enumerate(records) if r['id'] == 'star-trek-federation-core')
    bad = deepcopy(records[position])
    bad['regime_primary'] = 2
    try:
        check_record(bad, baseline[position], manual[position], taxonomy)
    except AssertionError:
        pass
    else:
        raise AssertionError('Old-numbering guard failed')
    # Participation must not silently change the post-wage flag in either direction.
    for value in (0, .99):
        changed = deepcopy(records[position])
        changed['axis']['nonworking'] = value
        check_record(changed, baseline[position], manual[position], taxonomy)
    examples = read('data/article-examples.json')
    assert examples['taxonomy_version'] == taxonomy['taxonomy_version']
    comparison_map = {r['candidate_id']: r for r in read('data/comparisons.json')['comparisons']}
    for item in examples['examples']:
        for sid in item.get('society_ids', []):
            assert sid in byid, sid
        for cid in item.get('comparison_ids', []):
            assert cid in comparison_map, cid
        assert item['basis']
    assert comparison_map['c0013']['regime_primary'] == 2
    assert comparison_map['c0013']['decision_status'] == 'supplementary'
    assert comparison_map['c0558']['regime_primary'] == 6
    assert all(r.get('article_fit', {}).get('definition_version') == taxonomy['taxonomy_version'] for r in comparison_map.values())
    summary = {'status': 'validated', 'taxonomy_version': taxonomy['taxonomy_version'],
               'article_sha256': taxonomy['article']['sha256'], 'records': len(records),
               'manual_coverage': len(manual), 'regimes': dict(sorted(Counter(r['regime_primary'] for r in records).items())),
               'post_work': sum(r['record_type'] == 'post_work' for r in records),
               'zero_variant': sum(r['record_type'] == 'zero_variant' for r in records),
               'supplementary_article_qualifying_records': sum(r['article_fit']['status'] == 'post_work' for r in comparison_map.values()),
               'all_assets_and_wellbeing_scores_preserved': True,
               'old_numbering_guard_tested': True, 'participation_independence_tested': True,
               'limitations': 'Validates the complete editorial migration and preservation, not independent canon truth. Factual exceptions remain explicit.'}
    if write_report:
        (ROOT / 'research/article-alignment/validation.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return summary


if __name__ == '__main__':
    print(json.dumps(validate(), ensure_ascii=False))
