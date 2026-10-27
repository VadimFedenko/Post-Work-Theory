"""Materialize the explicit 890-record article review as a durable research revision.

This is a one-time migration, not an inference engine. Manual choices are keyed
through the immutable index; historical batches/revisions are never rewritten.
"""
import hashlib
import argparse
import json
import re
from collections import Counter
from copy import deepcopy
from pathlib import Path
from utopia_helpers import digest, research_record

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / 'research/article-alignment'
DATE = '2026-10-21'
VERSION = 'article-2026-10-21'
NUMBER = {0: 0, 1: 1, 2: 3, 3: 2, 4: 4, 5: 5, 6: 6}
CODES = {
    'c': ('post_work', 'reduced', 'secondary', 'commons', 'Shared or freely accessible technological provision, rather than current earnings, is the central distribution model.'),
    's': ('post_work', 'mixed_or_reduced', 'secondary', 'status_or_institutional_allocation', 'Technological support is allocated through membership, status or institutional authority rather than primarily purchased with current wages.'),
    'r': ('post_work', 'reduced', 'secondary', 'productive_assets_or_capital', 'Access to productive assets or accumulated capital is the central claim on technological output; this need not provide a universal floor.'),
    'a': ('post_work', 'reduced', 'secondary', 'autonomous_system_allocation', 'An independent technical system sustains or allocates the material environment; current wages are not its primary access rule.'),
    'x': ('post_work', 'reduced', 'structurally_displaced_without_replacement', 'exclusion_or_informal_survival', 'Automation has substantially displaced the wage channel for the selected population without establishing a secure replacement; this is a dystopian post-wage interpretation.'),
    'm': ('post_work', 'mixed', 'mixed_transition', 'mixed_nonwage_transition', 'A partial technological transition plausibly makes nonwage access central for this scoped population, while important work and market dependencies remain.'),
    'w': ('zero_variant', 'mixed', 'primary', 'wages_and_commercial_access', 'The selected economy still primarily links material access to earnings and commercial purchases despite labor-saving technology.'),
    'l': ('zero_variant', 'mixed', 'work_conditioned', 'work_conditioned_earning_or_maintenance', 'Continued service or productive work remains the main condition of earning access or maintenance; supporting a workforce alone does not establish a post-wage economy.'),
    't': ('zero_variant', 'high_or_deliberately_retained', 'retained_or_not_replaced', 'restraint_or_restricted_automation', 'Relevant automation is restrained, unavailable or deliberately limited, so the selected population has not made the technology-driven post-wage transition.'),
    'h': ('zero_variant', 'high', 'not_replaced_by_automation', 'essential_person_labor', 'Essential labor by actual persons remains central without sufficient technological substitution; communal sharing, biological origin or robot embodiment alone does not establish the transition.'),
    'u': ('zero_variant', 'uncertain', 'uncertain_primary_best_guess', 'uncertain_earnings_based_access', 'The saved account does not establish a central nonwage material channel; the retained best guess is a continuing earnings-based technical economy, with low confidence.'),
}


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def write(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def replay(refresh=False):
    out = {'sources': {}, 'societies': {}, 'decisions': {}}
    for path in sorted((ROOT / 'research/batches').glob('batch-*.json')):
        batch = json.loads(path.read_text(encoding='utf-8'))
        for key in out:
            for item in batch[key]:
                if key == 'societies':
                    item = {'record_type': 'post_work', **item}
                identity = item['candidate_id' if key == 'decisions' else 'id']
                assert identity not in out[key] or out[key][identity] == item
                out[key][identity] = item
    for path in sorted((ROOT / 'research/revisions').glob('revision-*.json')):
        if path.name == 'revision-056.json':
            assert refresh, 'Migration already materialized; rebuild with merge_batches.py'
            assert json.loads(path.read_text(encoding='utf-8'))['article_sha256'] == read('research/article-alignment/review-index.json')['article_sha256']
            continue
        assert int(path.stem.split('-')[1]) < 56, 'A later revision exists; never overwrite completed subsequent research'
        for change in json.loads(path.read_text(encoding='utf-8'))['changes']:
            key, item = change['collection'], change['after']
            identity = item['candidate_id' if key == 'decisions' else 'id']
            assert out[key].get(identity) == change['before'], path.name
            out[key][identity] = item
    return out


def renumber_text(text):
    # Only explicit categorical references; do not touch years or statistics.
    text = re.sub(r'\b(regimes|types|categories|quadrants)(\s*#?\s*[0-6]\b(?:\s*(?:,|/|or|and)\s*#?\s*[0-6]\b)*)',
                  lambda m: m[1] + re.sub(r'\b[0-6]\b', lambda n: str(NUMBER[int(n[0])]), m[2]), text, flags=re.I)
    text = re.sub(r'\b(regime|type|category|quadrant)(\s*#?\s*)([23])\b',
                  lambda m: m[1] + m[2] + str(NUMBER[int(m[3])]), text, flags=re.I)
    return text


def renumber(value):
    if isinstance(value, dict):
        return {k: (NUMBER[v] if isinstance(v, int) else [NUMBER[n] for n in v] if isinstance(v, list) else v)
                if k in ('regime_primary', 'regime_alternatives', 'regime_analogy') else renumber(v)
                for k, v in value.items()}
    if isinstance(value, list):
        return [renumber(x) for x in value]
    return renumber_text(value) if isinstance(value, str) else value


def remove_old_admission(text):
    # Old prose admitted/excluded by participation, rather than wage distribution.
    # All removed values remain in revision.before and the frozen baseline.
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return ' '.join(s for s in sentences if not re.search(r'zero[- ]variant|zero variant|regime\s*0', s, re.I))


def set_axis(record, key, value, interval, basis):
    record['axis'][key] = value
    record['axis_assessment'][key].update(interval=interval, basis=basis, confidence='low')


def examples_overrides(r):
    identity = r['id']
    if identity == 'walle-axiom':
        r['regime_primary'], r['regime_alternatives'] = 5, [1]
        r['article_alignment']['qualification'] = 'Late AUTO-led operation is type 5; its corporate origin is type 1. The mixed control coordinate retains that institutional history.'
    elif identity == 'manna-terrafoam':
        r['regime_primary'], r['regime_alternatives'] = 2, [1]
        set_axis(r, 'guarantees', .35, [-.25, .95], 'Meals and housing exist, but confinement and insecure continued access make this a weak-guarantee interpretation under the article; type 1 remains a material-subsistence alternative. The contraceptive allegation is narrated suspicion, not verified policy.')
        r['source_ids'].append('src-manna-pdf-compound-suspicion')
        r['axis_assessment']['guarantees']['source_ids'] = r['source_ids'][:]
        r['canon_facts'].append('A compound resident voices suspicion of contraceptives in cafeteria food.')
        r['uncertainties'] = ['The reported contraceptive suspicion is not confirmation of reproductive-control policy; the article states this more strongly.', 'Supplied subsistence is real, but its long-term security and adequacy remain disputed; no national participation census is supplied.']
        r['description'] = ('Robotic services supply Terrafoam residents with housing and meals after their wage access collapses. Elite ownership and confinement make that support dependent and difficult to challenge. The article treats this as the second regime: technological output remains concentrated while residents lack dependable guarantees of an acceptable continued life. Actual meals are not erased by that judgment; type 1 remains an alternative if guarantees are read narrowly as present subsistence.\n\n'
                            'Human elites control the compound infrastructure. The high nonworking estimate concerns its residents, not the entire United States, and includes useful care or voluntary activity as work. A resident reports suspicion of contraceptives in cafeteria food, which is weaker evidence than confirmed sterilization or a verified water-treatment policy. The favorable guarantee estimate has therefore been revised cautiously, with a broad interval. This is an interpretive classification of insecure support, not a claim that a source proves the article’s strongest allegation.')
    elif identity == 'fallout-institute':
        r['regime_primary'], r['regime_alternatives'] = 2, [1]
        r['scope']['population'] = 'Institute human residents and its subordinated synth-person population, assessed as one exclusionary institution'
        r['scope']['human_population_proxy'] = True
        r['scope']['exclusions'] = ['A uniform claim about every surface resident', 'Treating sentient synth workers as inert automation', 'A human-only participation denominator']
        r['scope']['labor_phase'] = 'Engineered production and unequal allocation within the Institute, including sentient labor'
        r['axis_interpretation'] = {'nonworking': 'Participation among the scoped human and synth persons, not literal biological-human employment.', 'control': 'Concentrated born-human directorate authority; synthetic persons do not share control.'}
        set_axis(r, 'guarantees', .65, [.15, .95], 'The population now includes subordinated synth persons. Privileged human provision does not supply universal security to the whole institution.')
        set_axis(r, 'nonworking', .15, [0, .5], 'New mixed-person denominator includes useful synth labor and human research; low-confidence scenario rather than a canonical census.')
        r['description'] = ('The Institute combines engineered production with a privileged scientific enclave and a subordinated synth workforce. Its human residents receive food and medical support, while the same institution denies synthetic persons equal status and security. Following the article’s second regime, this record now assesses that whole exclusionary institution rather than only its born-human beneficiaries. The weak guarantee point concerns everyone in that stated population; a human-only enclave view would look closer to type 1.\n\n'
                            'A human directorate retains authority over production and access. The participation estimate now includes both humans and synth persons, counting research, medicine, maintenance and synthetic service as real work. It is a deliberately broad editorial scenario, not a conversion of the old human-only percentage. Engineered bodies and routine machinery support an uneven post-wage interpretation, but conscious workers are not treated as inert tools. The record makes no claim that all surface communities share these arrangements, or that technological sophistication eliminates exploitation.')
        r['uncertainties'] = ['Scope changed from born-human beneficiaries to the Institute including subordinated synth persons; axes with that denominator were reassessed.', 'A partial post-wage interpretation follows the article, while essential conscious labor remains a substantial qualification.', 'Type 1 describes the narrower privileged beneficiary view; it is not universal security for the institution.']
        r['editorial_assumptions'] = r['uncertainties'][:]
    elif identity == 'psychopass-sibyl-japan':
        r['regime_primary'], r['regime_alternatives'] = 5, [1]
        set_axis(r, 'control', -.6, [-.95, .2], 'Article-aligned functional reading: Sibyl autonomously allocates and governs beyond ordinary resident control. Its constituent living human brains make human cybernetic elite rule a competing interpretation, not a factual error to suppress.')
        r['description'] = ('Japan delegates large productive and administrative functions to technical systems, including fully automated farming. The article treats Sibyl as the fifth regime because an integrated decision system allocates opportunities and maintains an orderly material life beyond ordinary residents’ control. Social screening and exclusion qualify the favorable guarantee estimate. Career assignments and useful professional work remain compatible with this post-wage interpretation; neither agriculture alone nor the presence of chosen work supplies a national participation census.\n\n'
                            'Sibyl incorporates living human brains. The primary label therefore describes functional cybernetic autonomy, not a claim that its rulers are purely nonhuman software. A concentrated human-collective reading remains type 1 and is retained as an explicit alternative, with a broad control interval. The nonworking estimate still counts care, professional duties, maintenance and useful voluntary activity as work. This record concerns the selected Japanese order, not every imported Sibyl installation, and the assessment remains an editorial best guess rather than settled ontology or economic statistics.')
        r['editorial_assumptions'].append('Functional system autonomy follows the article; biological human-brain origin remains explicit and supports alternative type 1.')
    elif identity == 'solaria-naked-sun':
        r['regime_primary'], r['regime_alternatives'] = 4, [3]
        set_axis(r, 'guarantees', .2, [-.8, .85], 'Robot-supported private estates supply substantial comfort, but possession is not a nonalienable universal guarantee. Type 4 is the primary asset-based reading; type 3 captures a stronger membership-floor interpretation.')
        r['description'] = ('Solaria’s dispersed estates rely on immense robot capacity, giving recognized estate holders practical control of their own productive surroundings. The article’s fourth regime distinguishes such private abundance from a guaranteed common share: possessing machinery can sustain a person without wages while still leaving continuity dependent on ownership and eligibility. Comfortable estate life is therefore preserved as a fact, while the primary guarantee estimate is more cautious about a universal floor.\n\n'
                            'Control remains broadly distributed among the recognized human owners rather than concentrated in one autonomous machine government. Useful science, oversight, care and other activity still count as work, so robot numbers do not directly determine the nonworking fraction. The wide guarantee interval retains type 3 as a stronger membership-security alternative. This point concerns the period of The Naked Sun; it does not import the later hermaphroditic Solarians, child-status rules or events of Foundation and Earth. Sentient-service and social-isolation concerns remain separate from the economic label.')
    elif identity == 'readyplayerone-debt-work-zero':
        r['regime_primary'], r['regime_alternatives'] = 2, [0]
        r['article_alignment']['qualification'] = 'Article-style freemium/exclusion interpretation is primary. The checked novel passage establishes debt labor, not free food or the disappearance of the wage economy; type 0 remains an explicit alternative.'
        r['description'] = ('OASIS-centered life coexists with severe physical inequality and IOI’s enforced debt labor. The article uses this kind of privately controlled virtual abundance as a second-regime warning: access to experiences can be cheap while the material conditions of life remain controlled and insecure. This record adopts that partial post-wage interpretation, with type 0 retained as a strong alternative because the checked novel evidence still depicts real work and commercial dependence.\n\n'
                            'Human companies and owners retain authority over infrastructure, while users have limited agency inside the platform. No verified universal food entitlement is inferred from virtual access, and no claim is made that every warehouse task is already automated. The nonworking estimate allows displacement alongside debt work, paid occupations, care and useful digital creation. Time logged in and virtual wealth are not measures of participation. Winning platform ownership does not retroactively create a secure material floor. This classification follows the article’s proposed model with a visible factual limitation, rather than treating its freemium analogy as established canon.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh-unfinished-review', action='store_true', help='Regenerate this review before final validation; refuses subsequent revisions')
    args = parser.parse_args()
    index = read('research/article-alignment/review-index.json')
    article_hash = hashlib.sha256((ROOT / 'article.txt').read_bytes()).hexdigest()
    assert article_hash == index['article_sha256'], 'Article changed during this explicit review'
    before = replay(args.refresh_unfinished_review)
    baseline = read('research/article-alignment/baseline-societies.json')['societies']
    assert [r['id'] for r in baseline] == [r['id'] for r in index['records']] == list(before['societies'])
    tokens = ' '.join(line.split('#', 1)[0] for line in (DIR / 'manual-classification.txt').read_text(encoding='utf-8').splitlines()).split()
    chosen = {}
    for position, code in zip(tokens[::2], tokens[1::2]):
        number = int(position)
        assert number not in chosen and code in CODES
        chosen[number] = code
    assert len(tokens) == 2 * len(baseline) and set(chosen) == set(range(len(baseline)))
    changes, reviewed = [], []
    for number, original in enumerate(baseline):
        identity, code = original['id'], chosen[number]
        r = renumber(deepcopy(before['societies'][identity]))
        kind, production, wages, mechanism, basis = CODES[code]
        legacy = {k: deepcopy(original.get(k)) for k in ('record_type', 'regime_primary', 'regime_alternatives', 'regime_analogy')}
        r['legacy_classification'] = {'taxonomy_version': 'pre-article-2026-10-21', **legacy}
        r['taxonomy_version'] = VERSION
        r['record_type'] = kind
        analogy = r.get('regime_analogy')
        analogy = analogy if isinstance(analogy, list) else [analogy] if isinstance(analogy, int) else []
        if kind == 'zero_variant':
            if r['regime_primary']:
                analogy = [r['regime_primary'], *r.get('regime_alternatives', []), *analogy]
            r['regime_primary'] = 0
            r['regime_alternatives'] = []
            r['regime_analogy'] = list(dict.fromkeys(x for x in analogy if x))
        elif not r['regime_primary']:
            r['regime_primary'] = next((x for x in analogy if x), 2)
            r['regime_alternatives'] = [x for x in analogy if x and x != r['regime_primary']]
            r.pop('regime_analogy', None)
        r['post_work_assessment'] = {
            'definition_version': VERSION, 'manual_code': code,
            'status': 'transition' if code == 'm' else kind,
            'production_dependence': production, 'wage_dependence': wages,
            'allocation_mechanisms': [mechanism], 'basis': basis,
            'confidence': 'low', 'assessment_mode': 'editorial_best_guess',
            'source_ids': r['source_ids'][:], 'assessed_on': DATE,
            'participation_is_separate': True,
        }
        r['article_alignment'] = {'version': VERSION, 'article_sha256': article_hash,
                                  'definition_lines': [55, 57], 'reviewed_on': DATE}
        if original['record_type'] != kind:
            r['description'] = '\n\n'.join(remove_old_admission(p) for p in r['description'].split('\n\n'))
            for field in ('qualification_basis',):
                if field in r:
                    r[field] = remove_old_admission(r[field]) or basis
            for field in ('uncertainties', 'editorial_assumptions'):
                if field in r:
                    r[field] = [v for x in r[field] if (v := remove_old_admission(x))]
            if kind == 'zero_variant':
                r['description'] = re.sub(r'\bpost[- ]work\b', 'automation-related', r['description'], flags=re.I)
        examples_overrides(r)
        r['description'] = r['description'].replace('overlap with the zero-variant theme', 'are recorded separately from post-wage status')
        if r['id'] == 'readyplayerone-debt-work-zero':
            r['record_type'] = 'post_work'
            r['post_work_assessment'].update(manual_code='m', status='transition', production_dependence='mixed', wage_dependence='mixed_transition', allocation_mechanisms=['mixed_nonwage_transition'], basis=CODES['m'][4])
            r.pop('regime_analogy', None)
        # Present the current decision next to each card, including unchanged flags.
        current = r['post_work_assessment']
        r['description'] = r['description'].rstrip() + ' Article-aligned classification: ' + current['basis'] + ' Useful activity and the nonworking estimate are assessed separately.'
        r['post_work_assessment']['source_ids'] = r['source_ids'][:]
        r['qualification_basis'] = current['basis']
        r['qualification_confidence'] = 'low'
        r['review'].update(date=DATE, method='Article-alignment editorial review of saved lore and explicit per-record allocation choices; targeted Manna passage checked; no independent or whole-work rereading')
        changes.append({'collection': 'societies', 'before': before['societies'][identity], 'after': r})
        reviewed.append(deepcopy(r))
    record_map = {r['id']: r for r in reviewed}
    for identity, original in before['decisions'].items():
        d = renumber(deepcopy(original))
        if d['status'] in ('included', 'zero_variant'):
            links = d.get('society_ids', [d['society_id']])
            d['status'] = 'included' if any(record_map[s]['record_type'] == 'post_work' for s in links) else 'zero_variant'
            d['legacy_reason'] = original['reason']
            d['reason'] = 'Retained under the article’s post-wage definition. ' + ' '.join(record_map[s]['post_work_assessment']['basis'] for s in links)
            d['article_alignment_version'] = VERSION
            d['reassessed_on'] = DATE
        elif 'comparison_assessment' in d:
            d['article_alignment_version'] = VERSION
            d['reassessed_on'] = DATE
            fits = {
                'c0013': ('post_work', 2, 'Article interpretation of a deprived, chemically pacified post-wage society.'),
                'c0077': ('zero_variant', 0, 'The apparent robot state is a human intelligence operation; the ending does not establish autonomous technical provision.'),
                'c0174': ('zero_variant', 0, 'A pre-industrial discovery society has not made an automation-driven post-wage transition.'),
                'c0363': ('zero_variant', 0, 'Miniaturization changes purchasing power while earnings and human services remain central; scale is not automatic production.'),
                'c0408': ('zero_variant', 0, 'Reputation punishment is not itself a nonwage allocation system; the earnings-based best guess remains uncertain.'),
                'c0558': ('post_work', 6, 'A partial techno-scavenging interpretation follows the article’s BLAME! criterion: surviving humans draw on residual autonomous facilities without dependable guarantees.'),
            }
            fit, regime, rationale = fits.get(identity, ('not_applicable', None, 'The scored unit is a failed plan, intervention, remnant or non-recipient mechanism rather than a demonstrated continuing allocation society; see its explicit scope.'))
            d['comparison_assessment']['article_fit'] = {'status': fit, 'regime_primary': regime, 'basis': rationale, 'confidence': 'low', 'definition_version': VERSION}
            if fit == 'post_work':
                d['status'] = 'supplementary'
                d['legacy_reason'] = original['reason']
                d['reason'] = 'Completed article-qualifying assessment in the supplementary publication schema; not an omitted or rejected post-wage case. ' + rationale
                d['analysis'] = original['analysis'].split('\n\n')[0] + '\n\nCurrent classification supersedes the historical exclusion: ' + rationale + ' The existing scored record is preserved outside the main ready-card export, with its separate schema and without an invented matching cover.'
                d['comparison_assessment'].update(record_type='post_work', regime_primary=regime, regime_alternatives=[], taxonomy_version=VERSION, publication_status='supplementary_scored_record')
        if identity == 'c0013':
            d['reason'] = 'Article-aligned type-2 post-wage interpretation retained in the supplementary comparison schema; it is not rejected for failing to be a paradise or for lacking physical abundance.'
            d['analysis'] = 'The article classifies the actual deprived society as type 2 and its chemically perceived abundance as an appearance of type 1. This is compatible with a post-wage dystopia: illusion is not a material guarantee. The existing supplementary record remains a book-specific assessment, separate from the 2013 film card. Its position outside the main ready-card export is a schema/publication distinction, not a substantive zero-variant decision under the new definition.'
            d['comparison_assessment'].update(record_type='post_work', regime_primary=2, regime_alternatives=[1], taxonomy_version=VERSION, publication_status='supplementary_scored_record', qualification_basis='Article-specific post-wage interpretation; physical scarcity does not imply a wage economy.')
            d['comparison_assessment']['scope'] = 'Lem’s novel: actual embodied society beneath chemically perceived abundance; not the film adaptation'
        if identity == 'c0077':
            d['comparison_assessment']['article_discrepancy'] = 'The article uses the apparent robot state as type 6, but the checked primary ending reveals a human intelligence operation and a clerk inside the Calculator. Type 6 describes only the presented facade, not the actual autonomous polity.'
        if d != original:
            changes.append({'collection': 'decisions', 'before': original, 'after': d})
    source = {'id': 'src-manna-pdf-compound-suspicion', 'title': 'Manna: Two Visions of Humanity’s Future — compound conversation', 'author': 'Marshall Brain',
              'url': 'https://storj.someplacein.space/share/Manna__Two_Visions_of_Humanitys_Future_-_Marshall_Brain.pdf',
              'kind': 'primary_fiction_mirror', 'accessed_on': DATE, 'access_method': 'Bounded PDF text passage inspected with web PDF reader',
              'read_scope': 'PDF pp. 32–33, especially p. 33: residents discuss machine replacement and a suspicion about contraceptives in cafeteria food.',
              'limitations': 'Unofficial mirror of primary text, not a full-work read. A character’s suspicion does not verify sterilization, water treatment or an implemented policy.'}
    changes.append({'collection': 'sources', 'before': None, 'after': source})
    write('research/revisions/revision-056.json', {'revision_id': 'revision-056', 'revised_on': DATE,
          'reason': 'Align every retained record with article.txt: swap historical types 2/3, separate post-wage access from participation, review all 890 allocation models, and resolve article examples with factual qualifications.',
          'article_sha256': article_hash, 'manual_review': 'research/article-alignment/manual-classification.txt', 'changes': changes})
    taxonomy = {'schema_version': '1.1', 'taxonomy_version': VERSION,
        'article': {'path': 'article.txt', 'sha256': article_hash, 'definition_lines': [55, 57]},
        'definition': 'Automation or equivalent technology makes labor earnings cease to be the main effective distribution channel for the scoped population. Continuing useful activity does not imply a zero variant.',
        'zero_variant_rule': 'The technology-driven post-wage transition has not occurred, is deliberately restrained, or remains an uncertain earnings-based best guess. No threshold of nonworking determines this flag.',
        'regimes': [
            {'id': 0, 'label': 'Zero variant', 'control': None, 'guarantees': None},
            {'id': 1, 'label': 'Elite control with guarantees', 'control': 'concentrated_human', 'guarantees': 'strong'},
            {'id': 2, 'label': 'Elite control without guarantees', 'control': 'concentrated_human', 'guarantees': 'weak'},
            {'id': 3, 'label': 'Distributed control with guarantees', 'control': 'distributed_human', 'guarantees': 'strong'},
            {'id': 4, 'label': 'Distributed or personal assets without guarantees', 'control': 'distributed_human', 'guarantees': 'weak'},
            {'id': 5, 'label': 'Autonomous system with guarantees', 'control': 'autonomous_system', 'guarantees': 'strong'},
            {'id': 6, 'label': 'Autonomous system without guarantees', 'control': 'autonomous_system', 'guarantees': 'weak'}],
        'historical_number_mapping': {str(k): v for k, v in NUMBER.items()},
        'manual_codes': {k: {'record_type': v[0], 'production_dependence': v[1], 'wage_dependence': v[2], 'allocation': v[3], 'basis': v[4]} for k, v in CODES.items()},
        'confidence': 'All new allocation judgments are low-confidence editorial best guesses from existing scoped evidence, not production-share measurements.',
        'legacy_fields': 'legacy_classification records historical numbers, not current taxonomy; immutable historical batches retain their original numbering.'}
    write('data/taxonomy.json', taxonomy)
    # Explicitly re-review the separate wellbeing scores after the classification changes.
    # Their numerical values do not follow from the new regime or zero flag.
    previous = read('research/article-alignment/baseline-society-utopia.json')
    overlay = deepcopy(previous)
    overlay['review_index'] = 'research/utopia/review-index-v2.json'
    overlay['research_alignment'] = VERSION
    assets = read('data/society-assets.json')['assets']
    for r in reviewed:
        saved = overlay['assessments'][r['id']]
        saved['reviewed_record_sha256'] = digest(research_record(r))
        saved['assessment']['source_ids'] = r['source_ids'][:]
        if r['id'] == 'fallout-institute':
            saved['assessment']['basis'] = 'Human enclave comfort is qualified by concentrated authority and subordinated synth persons within the reassessed institution; the same negative wellbeing judgment remains appropriate.'
        r['assets'] = deepcopy(assets[r['id']])
    write('research/utopia/review-index-v2.json', {'schema_version': '1.1', 'assessed_on': DATE,
          'record_count': len(reviewed), 'research_alignment': VERSION,
          'supersedes': 'research/utopia/review-index.json',
          'original_records_sha256': digest(reviewed),
          'records': [{'index': i, 'id': r['id'], 'research_sha256': digest(research_record(r))} for i, r in enumerate(reviewed)]})
    write('research/utopia/revisions/review-002.json', {'revision': 2, 'reviewed_on': DATE,
          'reason': 'Explicitly reaffirm all 890 wellbeing scores after article alignment. Economic type is independent of utopian quality; the Institute scope includes already-considered synth oppression. Refresh evidence fingerprints and its basis without calculating or changing scores.',
          'before_overlay_sha256': digest(previous), 'after_overlay_sha256': digest(overlay),
          'changes': [{'id': k, 'before': previous['assessments'][k], 'after': v} for k, v in overlay['assessments'].items() if previous['assessments'][k] != v]})
    write('data/society-utopia.json', overlay)
    transition = Counter((o['regime_primary'], r['regime_primary']) for o, r in zip(baseline, reviewed))
    report = {'version': VERSION, 'reviewed_on': DATE, 'article_sha256': article_hash,
              'records': len(reviewed), 'manual_coverage': len(chosen),
              'before': dict(Counter(r['record_type'] for r in baseline)),
              'after': dict(Counter(r['record_type'] for r in reviewed)),
              'regimes': dict(sorted(Counter(r['regime_primary'] for r in reviewed).items())),
              'zero_to_post_work': sum(o['record_type'] == 'zero_variant' and r['record_type'] == 'post_work' for o, r in zip(baseline, reviewed)),
              'post_work_to_zero': sum(o['record_type'] == 'post_work' and r['record_type'] == 'zero_variant' for o, r in zip(baseline, reviewed)),
              'old_to_new_regimes': [{'old': a, 'new': b, 'records': n} for (a, b), n in sorted(transition.items())],
              'axis_changes': [r['id'] for o, r in zip(baseline, reviewed) if o['axis'] != r['axis']],
              'utopia_scores_changed': 0, 'assets_changed': 0,
              'limitations': ['This is a corpus-wide editorial classification review from saved research, not a fresh full-text verification of 890 societies.', 'Mixed transitions and narrow cohorts remain explicitly scoped; inclusion does not assert a post-wage economy for an entire franchise.', 'The article’s factual or internal ambiguities are recorded in article-examples.json rather than promoted to canonical facts.']}
    write('research/article-alignment/summary.json', report)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
