"""Publish a complete, explicit work-by-work recognition review; no score fallback."""
import argparse
import json
from popularity_helpers import ROOT, band, digest, recognition_identity

DATE = '2026-10-22'
PROFILES = {
    'obscure': 'Very limited general-public recognition; primarily of interest to specialists in historical or niche speculative fiction.',
    'specialist': 'Recognition is concentrated in a small specialist readership, subgenre, game community or online niche; limited crossover visibility.',
    'niche_or_cult': 'An identifiable niche or cult audience, with recognition mainly within its medium, region or genre rather than the general public.',
    'genre_established': 'Established recognition among genre or medium audiences, or strong regional cultural recognition, with some crossover awareness.',
    'broad_recognition': 'Broad recognition supported by substantial mainstream, international, screen, gaming or literary-cultural visibility, below the most ubiquitous brands.',
    'very_broad_recognition': 'Very broad and durable international cultural visibility, reaching well beyond a specialist audience.',
    'maximum_recognition': 'Top-anchor global popular-culture recognition, comparable to the user-specified Star Wars maximum.',
}
NOTES = {
    0: 'A major prose-SF series; its literary prominence is not equated with the general visibility of Star Wars or Star Trek.',
    1: 'An enduring, frequently discussed short-story classic; age alone is not a reason for a low score.',
    6: 'Strong recognition in Russian-speaking SF culture receives credit, while the international reach is narrower than that of global screen franchises.',
    7: 'A durable literary-cultural reference with screen adaptations; the novel and its named adaptation share the same recognition unit.',
    8: 'A widely circulating literary and political-cultural reference whose recognition extends beyond SF readers.',
    9: 'The Midas Plague and The Man Who Ate the World belong to the linked Midas World sequence and receive one recognition score.',
    40: 'Rated as The Star Diaries rather than the obscurity of the particular voyage.',
    129: 'A specialist collaborative worldbuilding setting; the number of entries in this database does not increase its popularity.',
    130: 'The fan fiction is assessed as its own work and does not inherit the My Little Pony brand audience.',
    162: 'A major Russian/Soviet childhood property; strong regional recognition is balanced against narrower worldwide recognition.',
    181: 'Black Panther is the recognition unit, rather than every property owned by Marvel or Disney.',
    182: 'Fantastic Four is the recognition unit; sharing a publisher or crossover universe does not merge it with Spider-Man.',
    183: 'The X-Men franchise has extensive cross-media recognition; individual comics or societies inherit that franchise estimate.',
    184: 'Spider-Man 2099 belongs to the globally familiar Spider-Man property; the score does not measure awareness of the 2099 setting itself.',
    205: 'The Superman property includes the named Superman stories and the Superman-led DC One Million event, not the whole DC catalogue.',
    220: 'A large, long-lived international anime and model franchise; regional strength is considered without treating the Anglophone market as the whole world.',
    223: 'Rated as the Evangelion franchise, including the Rebuild films.',
    224: 'A major Asian and international childhood property; English-language online visibility alone would understate its reach.',
    242: 'The Robot/I, Robot property includes its named literary works and screen adaptations; other unrelated Asimov stories do not automatically inherit this score.',
    275: 'A durable art-animation cult classic; historical age is separated from present cultural recognition.',
    319: 'The screen anthology is the recognition unit; Dick\'s original Autofac story remains separately assessed.',
    330: 'Rated as the Tron franchise rather than the audience of its particular animated spin-off.',
    340: 'NOiSE is a BLAME! prequel and shares the explicit BLAME! recognition unit.',
    348: 'A separately branded Astro Boy reimagining; assessed as Pluto rather than automatically inheriting all Astro Boy recognition.',
    354: 'Rated as Space Battleship Yamato; international and Japanese cultural recognition both matter.',
    395: 'Rated as the SteamWorld game series.',
    396: 'Alpha Centauri is a separate recognizable property, despite its relationship to Civilization and Sid Meier.',
    398: 'The named Civilization property includes Beyond Earth and the licensed Call to Power entry; author/designer association alone does not merge Alpha Centauri.',
    425: 'The Authority retains its own recognizable property identity; DC ownership alone does not give it Superman-level recognition.',
    426: 'Legion of Super-Heroes retains its own property identity rather than inheriting Superman\'s score through a shared universe.',
    432: 'Publication in 2000 AD does not give Robo-Hunter the recognition of Judge Dredd.',
    433: 'Publication in 2000 AD does not give ABC Warriors the recognition of Judge Dredd.',
    435: 'Publication in 2000 AD does not give Halo Jones the recognition of Judge Dredd.',
    445: 'Megalex is not merged with The Incal merely because of Jodorowsky or the publisher.',
    465: 'Rated as the Space Odyssey series, including the widely known 2001 screen/literary property.',
    468: 'A Time Odyssey is a separate series; sharing Clarke as an author does not make it Space Odyssey.',
    540: 'Rated as Ramez Naam\'s Nexus trilogy, not William Hertling\'s Singularity sequence or another work titled Apex.',
    638: 'An early utopian text with historical significance and very limited present general awareness; significance is not audience size.',
    642: 'A historically documented pulp story; bibliographic presence is not evidence of a large modern audience.',
    644: 'A specialist historical automation reference, not a generally familiar mass-market title.',
    646: 'The Great Ring pair has substantial Russian/Soviet SF recognition, with a more limited international audience.',
    648: 'Kept separate from Noon Universe: a related author/character or disputed chronology does not automatically establish one recognition franchise.',
    652: 'Rated as the Alisa Seleznyova / Guest from the Future property, with strong Russian-speaking regional recognition.',
    658: 'Large and durable German-language SF recognition is credited; strong sales in one language are not equated with universal global familiarity.',
    674: 'A widely recognized international game across multiple platforms; all three selected societies inherit the game score rather than the obscurity of their particular lore.',
}
SUBJECT_NAMES = {
    6: 'Noon Universe', 40: 'The Star Diaries', 124: 'Frostpunk', 141: 'Alastor trilogy',
    152: 'Polity', 156: 'Monk & Robot', 160: 'Four-BEE / Biting the Sun', 167: 'Lancer',
    181: 'Black Panther', 182: 'Fantastic Four', 183: 'X-Men', 184: 'Spider-Man',
    223: 'Evangelion', 296: 'Half-Life', 330: 'Tron', 354: 'Space Battleship Yamato',
    389: 'Watch Dogs', 395: 'SteamWorld', 409: 'Anno', 414: 'Elite',
    401: 'Sword of the Stars', 465: 'Space Odyssey', 527: 'Revenger',
    540: 'Nexus trilogy', 627: 'Owner trilogy', 634: 'Across Realtime', 636: 'Wayfarers',
    642: 'Stranger Club / The Call of the Mech-Men',
    643: 'Men, Martians and Machines / Mechanistria',
    652: 'Alisa Seleznyova / Guest from the Future', 670: 'Thousand Cultures',
}
SERIES_SINGLETONS = {
    6,40,71,76,77,78,99,102,109,110,124,126,127,128,129,131,132,133,135,137,138,
    141,152,153,156,160,162,165,166,167,171,172,176,177,181,182,183,184,185,202,
    217,223,236,241,262,283,284,293,295,296,315,316,317,330,331,333,334,335,336,
    337,338,339,341,342,343,345,348,349,351,352,354,360,361,364,365,366,367,370,
    371,372,375,377,389,391,393,395,396,398,401,402,403,404,405,407,409,412,414,
    418,419,425,426,428,429,430,431,432,433,435,440,441,445,447,449,465,468,527,
    540,546,547,549,561,575,586,611,627,629,634,636,642,643,645,650,652,658,660,670,
}


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--revision-reason')
    args = parser.parse_args()
    records = read('data/societies.json')['societies']
    index = read('research/popularity/review-index.json')
    works = index['works']
    if [r['id'] for r in records] != [x['id'] for x in index['records']]:
        raise ValueError('Popularity review record IDs/order changed; extend the explicit review first')
    if list(dict.fromkeys(r['work'] for r in records)) != works:
        raise ValueError('Work labels changed; extend the explicit review first')
    raw = (ROOT / 'research/popularity/manual-scores.txt').read_text(encoding='utf-8')
    tokens = ' '.join(line.split('#', 1)[0] for line in raw.splitlines()).split()
    assert len(tokens) % 2 == 0
    scores = {}
    for number, value in zip(tokens[::2], tokens[1::2]):
        n = int(number)
        assert n not in scores, f'Duplicate manual work index {n}'
        score = float(value)
        assert 0 <= score <= 1 and abs(score * 20 - round(score * 20)) < 1e-8
        scores[n] = score
    assert set(scores) == set(range(len(works))), 'Every work needs an explicit score'
    grouping = read('research/popularity/manual-groups.json')
    membership, groups = {}, {}
    for g in grouping['groups']:
        assert g['id'] not in groups and g['anchor'] in g['members']
        assert len(g['members']) == len(set(g['members']))
        groups[g['id']] = g
        for n in g['members']:
            assert n not in membership and n in scores
            assert scores[n] == scores[g['anchor']], f'Conflicting franchise scores: {works[n]}'
            membership[n] = g['id']
    for n, work in enumerate(works):
        if n not in membership:
            sid = f'work-{n:03d}'
            groups[sid] = {'id': sid, 'name': SUBJECT_NAMES.get(n, work), 'anchor': n, 'members': [n]}
            membership[n] = sid
    references = read('research/popularity/references.json')
    overlay = {
        'schema_version': '1.0', 'scale_version': 'recognition-2026-10-22',
        'assessed_on': DATE, 'audience': 'international_general_cultural_recognition',
        'scale': {'minimum': 0, 'maximum': 1, 'step': .05, 'top_anchor': 'Star Wars = 1',
                  'interpretation': 'Ordinal editorial recognition index; not a percentage, probability, sales estimate or measurement of the specific society.'},
        'methodology': 'research/popularity/methodology.md',
        'manual_scores_sha256': digest(scores), 'manual_groups_sha256': digest(grouping),
        'references': references['references'], 'subjects': {}, 'assignments': {},
    }
    for sid, g in groups.items():
        n = g['anchor']
        score = scores[n]
        notes = list(dict.fromkeys(NOTES[i] for i in g['members'] if i in NOTES))
        basis = g['name'] + ': ' + PROFILES[band(score)]
        if notes:
            basis += ' ' + ' '.join(notes)
        overlay['subjects'][sid] = {
            'name': g['name'], 'score': score,
            'subject_type': g.get('subject_type', 'franchise_or_series' if len(g['members']) > 1 or n in SERIES_SINGLETONS or n in SUBJECT_NAMES else 'work'),
            'recognition_band': band(score), 'basis': basis,
            'work_labels': [works[i] for i in sorted(g['members'])],
            'manual_work_indices': sorted(g['members']),
            'reference_ids': list(dict.fromkeys(ref for i in g['members'] for ref in references['work_reference_ids'].get(str(i), []))),
        }
        if g.get('assessed_on'):
            overlay['subjects'][sid]['assessed_on'] = g['assessed_on']
    work_to_subject = {works[n]: sid for n, sid in membership.items()}
    for r in records:
        overlay['assignments'][r['id']] = {
            'subject_id': work_to_subject[r['work']],
            'reviewed_identity_sha256': digest(recognition_identity(r)),
        }
    path = ROOT / 'data/society-popularity.json'
    if path.exists():
        old = read('data/society-popularity.json')
        if old != overlay:
            assert args.revision_reason, 'Changing saved popularity ratings requires --revision-reason'
            folder = ROOT / 'research/popularity/revisions'
            folder.mkdir(exist_ok=True)
            number = len(list(folder.glob('review-*.json'))) + 1
            (folder / f'review-{number:03d}.json').write_text(json.dumps({
                'reviewed_on': DATE, 'reason': args.revision_reason,
                'before': old, 'after_sha256': digest(overlay),
            }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    path.write_text(json.dumps(overlay, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'works_explicitly_reviewed': len(scores), 'recognition_subjects': len(groups),
                      'societies_assigned': len(records)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
