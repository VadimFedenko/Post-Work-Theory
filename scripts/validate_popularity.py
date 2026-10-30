"""Validate full coverage, franchise consistency, preservation and rebuild guards."""
import json
from collections import Counter
from copy import deepcopy
from popularity_helpers import ROOT, POPULARITY_FIELDS, apply_popularity_overlay, band, digest, original_record


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def expect_rejected(records, overlay):
    try:
        apply_popularity_overlay(records, overlay)
    except ValueError:
        return
    raise AssertionError('Invalid popularity input was accepted')


def main():
    export = read('data/societies.json')
    records = export['societies']
    overlay = read('data/society-popularity.json')
    index = read('research/popularity/review-index.json')
    originals = [original_record(r) for r in records]
    assert export['schema_version'] == '1.2'
    assert len(records) == len(index['records']) == len(overlay['assignments'])
    assert len({r['id'] for r in records}) == len(records)
    assert [r['id'] for r in records] == [x['id'] for x in index['records']]
    assert digest(originals) == index['original_records_sha256'], 'Pre-existing record fields changed'
    for r, saved in zip(originals, index['records']):
        assert digest(r) == saved['original_record_sha256'], r['id']
    assert list(dict.fromkeys(r['work'] for r in records)) == index['works']
    assert len(index['works']) == len({r['work'] for r in records})
    byid = {r['id']: deepcopy(r) for r in records}
    apply_popularity_overlay(byid, overlay)
    for r in records:
        assert all(r[k] == byid[r['id']][k] for k in POPULARITY_FIELDS)
        a = r['popularity_assessment']
        assert a['confidence'] == 'low' and a['assessment_mode'] == 'editorial_best_guess'
        assert a['audience'] == overlay['audience'] and a['scale_version'] == overlay['scale_version']
    for reference in overlay['references'].values():
        assert reference['url'].startswith('https://')
        assert reference['read_scope'] and reference['limitations'] and reference['access_method']
    # Negative checks protect actual failure modes, not merely the writer's shape.
    missing = deepcopy(byid)
    missing.pop(records[0]['id'])
    expect_rejected(missing, overlay)
    changed = deepcopy(byid)
    changed[records[0]['id']]['scope']['continuity'] += ' changed'
    expect_rejected(changed, overlay)
    bad = deepcopy(overlay)
    bad['subjects']['star-wars']['score'] = 1.05
    expect_rejected(deepcopy(byid), bad)
    bad = deepcopy(overlay)
    bad['subjects']['star-wars']['score'] = .123
    expect_rejected(deepcopy(byid), bad)
    bad = deepcopy(overlay)
    bad['subjects']['star-wars']['score'] = True
    expect_rejected(deepcopy(byid), bad)
    bad = deepcopy(overlay)
    bad['assignments'][records[0]['id']]['subject_id'] = 'star-wars'
    expect_rejected(deepcopy(byid), bad)
    bad = deepcopy(overlay)
    bad['subjects']['star-wars']['reference_ids'].append('unregistered-reference')
    expect_rejected(deepcopy(byid), bad)
    changed = deepcopy(byid)
    changed[records[0]['id']]['axis']['control'] = -.1
    apply_popularity_overlay(changed, overlay)
    assert changed[records[0]['id']]['popularity_score'] == records[0]['popularity_score']
    for sid, score in {'star-wars': 1, 'star-trek': .95, 'culture': .55,
                       'gundam': .85, 'doraemon': .95, 'superman': 1}.items():
        subset = [r for r in records if r['popularity_assessment']['subject_id'] == sid]
        assert subset and {r['popularity_score'] for r in subset} == {score}
    counts = Counter(band(r['popularity_score']) for r in records)
    subjects = overlay['subjects']
    totals = Counter(r['popularity_assessment']['subject_id'] for r in records)
    report = {
        'status': 'validated', 'assessed_on': overlay['assessed_on'],
        'records': len(records), 'work_labels_reviewed': len(index['works']),
        'recognition_subjects': len(subjects), 'records_by_band': dict(counts),
        'subjects_by_band': dict(Counter(band(g['score']) for g in subjects.values())),
        'score_range': [min(r['popularity_score'] for r in records), max(r['popularity_score'] for r in records)],
        'complete_coverage_and_equal_scores_within_subject': True,
        'all_preexisting_record_fields_preserved': True,
        'missing_stale_identity_wrong_group_and_invalid_score_guards_tested': True,
        'social_axes_do_not_determine_popularity': True,
        'limitations': 'Low-confidence editorial recognition judgments; not audience percentages or a full survey of every title.',
    }
    folder = ROOT / 'research/popularity'
    (folder / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Популярность произведений и франшиз', '',
             f"{len(records)} обществ; {len(index['works'])} исходных названия; {len(subjects)} групп узнаваемости. Оценка: 22 октября 2026 года.", '',
             'Редакторская международная узнаваемость от 0 до 1; шаг 0,05. Star Wars = 1. Все общества одной группы получают одинаковый балл.', '',
             '[Методика](methodology.md) · [Проверка](validation.json) · [Все названия](work-review.md)', '',
             '## Группы по убыванию популярности', '',
             '| Франшиза / произведение | Балл | Обществ | Ключ |', '| --- | ---: | ---: | --- |']
    ordered = sorted(subjects.items(), key=lambda item: (-item[1]['score'], item[1]['name'].casefold()))
    lines += [f"| {g['name'].replace('|', '/')} | {g['score']:.2f} | {totals[sid]} | {sid} |" for sid, g in ordered]
    lines += ['', f'## Все {len(records)} обществ', '', '| ID | Название | Группа узнаваемости | Балл |', '| --- | --- | --- | ---: |']
    lines += [f"| {r['id']} | {r['name'].replace('|', '/')} | {r['popularity_assessment']['subject'].replace('|', '/')} | {r['popularity_score']:.2f} |" for r in records]
    (folder / 'catalogue.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    workmap = {w: (sid, g) for sid, g in subjects.items() for w in g['work_labels']}
    lines = ['# Ручной проход по всем названиям', '',
             f"Все {len(index['works'])} исходных значения work получили явный балл; неизвестные названия не подставляются в общий default.", '',
             '| Индекс | Исходное work | Группа | Балл |', '| ---: | --- | --- | ---: |']
    for i, work in enumerate(index['works']):
        sid, g = workmap[work]
        lines.append(f"| {i:03d} | {work.replace('|', '/')} | {sid} | {g['score']:.2f} |")
    (folder / 'work-review.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
