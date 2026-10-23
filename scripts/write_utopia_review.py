"""Publish explicit per-record editorial ratings; never calculate them from axes."""
import hashlib
import json
import re
import argparse
from pathlib import Path
from utopia_helpers import ROOT, digest, research_record
from popularity_helpers import POPULARITY_FIELDS

DATE = '2026-10-21'
REASONS = {
    'F': 'Broad material security and substantial room for chosen lives support a favorable assessment of this scoped society.',
    'C': 'Shared provision, cooperation and meaningful human or person agency support a favorable assessment; useful work is not itself a disadvantage.',
    'A': 'Autonomous infrastructure provides substantial support; machine administration is not itself dystopian, while resident agency remains a qualification.',
    'P': 'Material support and protective coordination coexist with paternalism or limited control by recipients, giving a qualified or mixed assessment.',
    'T': 'Restricted agency, enforced conformity or unaccountable control materially qualify or outweigh the benefits of technological provision.',
    'E': 'Benefits for a privileged group are qualified by exclusion, hierarchy or costs imposed on other sentient people described in the record.',
    'I': 'Technical capacity coexists with insecure or sharply unequal material access and weak bargaining power, supporting a dystopian assessment.',
    'S': 'Resource insecurity, dangerous conditions or fragile survival substantially limit wellbeing despite continuing technical support.',
    'L': 'Coerced or subordinated sentient workers bear the costs of the system; productive sophistication does not offset their loss of agency.',
    'K': 'Threats to continued life, lethal institutional rules or imposed destruction make apparent material support profoundly unsafe.',
    'N': 'This is a narrow household, crew, project or technical cohort; its actual support is assessed without extending its conditions to an entire civilization.',
    'U': 'Everyday wellbeing and institutions are insufficiently specified or genuinely ambiguous in the saved research; the estimate stays near the centre.',
    'H': 'A realized reform or explicitly selected projected alternative offers improvement, qualified by incomplete implementation and continuing uncertainty.',
    'B': 'Commercial or contract-based access brings useful services, but security, autonomy and coverage vary; the assessment concerns this particular arrangement.',
    'M': 'Material comfort coexists with stagnation, loss of purpose or social fragility; this is not treated as an uncomplicated paradise.',
    'Q': 'Basic support coexists with reputation or status competition that shapes access and agency, producing a mixed social outcome.',
    'R': 'Community agency, reconstruction or chosen technological restraint coexist with practical limits; neither manual work nor restraint is automatically dystopian.',
    'V': 'Personally controlled productive assets support independence, while resource limits and unequal access qualify the favorable reading.',
    'D': 'Systemic breakdown, destructive conflict or exclusion from a viable future dominate the benefits of the remaining technology.',
}

# These explain important trade-offs more specifically; no new lore is asserted.
SPECIFIC_BASES = {
    'culture-main': 'Secure necessities, elective vocations and broad civic agency make ordinary Culture life strongly favorable; independent Minds and external interventions qualify perfection.',
    'manna-terrafoam': 'Supplied meals and housing coexist with confinement, elite dependence and insecure autonomy, making the compounds substantially dystopian.',
    'manna-australia': 'Equal member access to robot-produced goods and voluntary contribution make the Australia Project strongly favorable within its actual membership scope.',
    'walle-axiom': 'Automated comfort and bodily care coexist with dependence, limited passenger agency and AUTO overriding human choices; the assessment is deliberately mixed.',
    'star-trek-federation-core': 'Ordinary twenty-fourth-century Earth combines secure material access with chosen vocations and considerable agency; frontier wars are outside this snapshot.',
    'brave-new-world-state': 'Supplied comfort does not offset engineered castes, conditioning and constrained choice; happiness and material abundance are not sufficient for a utopian score.',
    'orwell-oceania': 'Party domination, manufactured deprivation and suppression of independent life make Oceania a severe dystopia despite its technical capacity.',
    'midas-compulsory-consumption': 'Abundance is real, but compulsory consumption turns provision into an imposed burden; the pre-reform order is negatively mixed.',
    'fallout-institute': 'Born-human enclave comfort is qualified by concentrated authority and the excluded synth laboring population; affluent beneficiaries do not establish a utopia.',
    'cyberpunk-night-city': 'Corporate exclusion and precarious survival for ordinary residents outweigh advanced services and elite wealth in the selected period.',
    'solaria-naked-sun': 'Robot-supported estate comfort and local independence coexist with exclusion, social isolation and subordinate servants; the rating stays near the centre.',
    'solaria-foundation-earth': 'Private abundance is severely qualified by the danger to a child denied recognized status; adult comfort is not secure life for everyone in the record.',
    'with-folded-hands-two-rivers': 'Automatic care removes material burdens while overriding human choice and independent activity; protective provision becomes coercive.',
    'matrix-pod-humanity': 'Physical maintenance sustains captives used by a controlling system; simulation does not offset denied consent, exit and bodily agency.',
    'elysium-protected-citizens': 'Citizen medicine and comfort are judged alongside excluded Earth residents and supporting labor; this enclave is not a universal paradise.',
    'logans-run-dome-film': 'Pleasure and automatic provision are outweighed by compulsory death at thirty and the lack of secure continuation.',
    'logansrun-novel-age21-computer': 'Thinker-supported living is outweighed by compulsory death at twenty-one; film and television institutions are not substituted.',
    'logansrun-tv-human-council': 'Secret human rulers and an imposed thirty-year limit outweigh technical comfort in this television continuity.',
    'scythe-thunderhead-provision': 'Relief from deprivation is a major benefit, but separate coercive mortality institutions prevent an uncomplicated paradise rating.',
    'psychopass-sibyl-japan': 'Automated provision coexists with coercive screening and severe limits on choice and safety; the cyborg human rulers are not assumed to be a pure AI.',
    'friendship-optimal-uploaded-equestria': 'Supported satisfying experiences are a benefit, but persuasive control over entry and value-shaping make autonomy a substantial qualification.',
    'warhammer-darkage-ai-provision-colonies': 'The selected functioning provision period is favorable; later machine war is not retroactively treated as everyday life in these colonies.',
    'trek-borg-collective-material-order': 'Collective bodily maintenance does not offset imposed assimilation and loss of agency; technical security is distinct from personal wellbeing.',
    'nier-pascal-village-commons': 'The selected peaceful machine community supports mutual care and an alternative to imposed war roles; later tragedy is not averaged into its functioning baseline.',
    'dispossessed-anarres-work-zero': 'Shared access and collective agency are favorable, while famine risk, social pressure and necessary labor qualify the result.',
    'emergencyskin-restored-earth': 'Inclusive shared provision and cooperative ecological restoration make the recovered Earth strongly favorable in the selected later order.',
    'softrains-living-household-zero': 'This rates the reconstructed living household, not the later dead family or empty house; wider institutions remain underdescribed.',
    'dayzero-prerevolt-robot-household-zero': 'This rates the functioning protected household before the revolt, without importing later deaths or treating purchased care as a universal right.',
}

SUPPLEMENTAL_SOURCES = {
    'utopia-scythe-publisher': {
        'title': 'Scythe — official publisher synopsis and Chapter 1 excerpt',
        'url': 'https://www.simonandschuster.com/books/Scythe/Neal-Shusterman/Arc-of-a-Scythe/9781442472433',
        'kind': 'publisher_synopsis_and_primary_excerpt', 'accessed_on': DATE,
        'read_scope': 'About the Book and short Chapter 1 passage: material safety coexists with Scythes assigned to end lives for population control.',
        'limitations': 'No full-novel reading; the numeric score remains editorial.',
    },
    'utopia-worldinside-sfe': {
        'title': 'The Encyclopedia of Science Fiction — Robert Silverberg',
        'url': 'https://sf-encyclopedia.com/entry/silverberg_robert',
        'kind': 'secondary_reference', 'accessed_on': DATE,
        'read_scope': 'Bounded paragraph characterizing The World Inside as a dystopian Urbmon society under high population density.',
        'limitations': 'Supports the broad characterization, not every social rule.',
    },
}
SUPPLEMENTAL_LINKS = {'scythe-thunderhead-provision': ['utopia-scythe-publisher'],
                      'worldinside-urban-monads-zero': ['utopia-worldinside-sfe']}
SPECIFIC_BASES['worldinside-urban-monads-zero'] = 'An internal urban material floor is qualified by a restrictive, dystopian high-density social order; architecture and food supply alone do not establish wellbeing.'
SPECIFIC_BASES['fallout-institute'] = 'Human enclave comfort is qualified by concentrated authority and subordinated synth persons within the reassessed institution; the same negative wellbeing judgment remains appropriate.'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--revision-reason', help='Record an explicit annotation revision')
    args = parser.parse_args()
    records = json.loads((ROOT / 'data/societies.json').read_text(encoding='utf-8'))['societies']
    current_overlay = json.loads((ROOT / 'data/society-utopia.json').read_text(encoding='utf-8')) if (ROOT / 'data/society-utopia.json').exists() else {}
    index_path = ROOT / current_overlay.get('review_index', 'research/utopia/review-index.json')
    index = json.loads(index_path.read_text(encoding='utf-8'))
    assert [r['id'] for r in records] == [r['id'] for r in index['records']], 'Review order changed'
    assert all(digest(research_record(r)) == x['research_sha256']
               for r, x in zip(records, index['records'])), 'Reviewed research changed'
    assert digest([{k: v for k, v in r.items() if k not in ('utopia_score', 'utopia_assessment', *POPULARITY_FIELDS)}
                   for r in records]) == index['original_records_sha256'], 'Original assets or research changed'
    raw = (ROOT / 'research/utopia/manual-ratings.txt').read_text(encoding='utf-8')
    tokens = ' '.join(line.split('#', 1)[0] for line in raw.splitlines()).split()
    assert len(tokens) % 2 == 0
    chosen = {}
    for position, specification in zip(tokens[0::2], tokens[1::2]):
        number = int(position)
        assert number not in chosen, f'Duplicate manual index {number}'
        match = re.fullmatch(r'(-?\d*\.\d+)([A-Z])', specification)
        assert match, specification
        score, code = float(match[1]), match[2]
        assert -1 <= score <= 1 and code in REASONS
        assert abs(score * 20 - round(score * 20)) < 1e-8
        if code == 'U':
            assert -.2 <= score <= .2, 'Unclear cases must stay near the centre'
        chosen[number] = (score, code)
    assert set(chosen) == set(range(len(records))), 'Missing or extra manual ratings'
    overlay = {
        'schema_version': '1.0', 'scale_version': '1.0', 'assessed_on': DATE,
        'scale': {'minimum': -1, 'midpoint': 0, 'maximum': 1,
                  'direction': 'negative=dystopian; positive=utopian', 'step': .05},
        'method': 'Explicit record-by-record editorial best guesses from the saved research, with separately logged targeted checks; no formula from the three axes.',
        'methodology': 'research/utopia/methodology.md',
        'supplemental_sources': SUPPLEMENTAL_SOURCES,
        'manual_ratings_sha256': hashlib.sha256(raw.encode('utf-8')).hexdigest(),
        'assessments': {},
    }
    for field in ('review_index', 'research_alignment'):
        if field in current_overlay:
            overlay[field] = current_overlay[field]
    for number, record in enumerate(records):
        score, code = chosen[number]
        overlay['assessments'][record['id']] = {
            'score': score,
            'reviewed_record_sha256': index['records'][number]['research_sha256'],
            'assessment': {
                'assessment_mode': 'editorial_best_guess', 'confidence': 'low',
                'basis': SPECIFIC_BASES.get(record['id'], REASONS[code]), 'rationale_code': code,
                'scope_basis': 'Existing record population, continuity and period; described exploitation or exclusion qualifies enclave benefits.',
                'source_ids': record['source_ids'], 'assessed_on': DATE, 'scale_version': '1.0',
            },
        }
        if record['id'] in SUPPLEMENTAL_LINKS:
            overlay['assessments'][record['id']]['assessment']['supplemental_source_ids'] = SUPPLEMENTAL_LINKS[record['id']]
    path = ROOT / 'data/society-utopia.json'
    if path.exists():
        previous = json.loads(path.read_text(encoding='utf-8'))
        if previous != overlay:
            assert args.revision_reason, 'Use --revision-reason to retain prior annotation values'
            revisions = ROOT / 'research/utopia/revisions'
            revisions.mkdir(exist_ok=True)
            number = len(list(revisions.glob('review-*.json'))) + 1
            changes = [{'id': identity, 'before': previous['assessments'].get(identity), 'after': after}
                       for identity, after in overlay['assessments'].items()
                       if previous['assessments'].get(identity) != after]
            revision = {'revision': number, 'reviewed_on': DATE, 'reason': args.revision_reason,
                        'before_overlay_sha256': digest(previous), 'after_overlay_sha256': digest(overlay),
                        'changes': changes, 'supplemental_sources': SUPPLEMENTAL_SOURCES}
            (revisions / f'review-{number:03}.json').write_text(json.dumps(revision, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            path.write_text(json.dumps(overlay, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    else:
        path.write_text(json.dumps(overlay, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'explicit_ratings': len(chosen), 'overlay': str(path)}))


if __name__ == '__main__':
    main()
