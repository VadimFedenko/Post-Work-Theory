"""Research catalogues and summaries; the public README is maintained separately."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def text(path, value):
    (ROOT / path).write_text(value.rstrip() + '\n', encoding='utf-8')


def write(path, value):
    text(path, json.dumps(value, ensure_ascii=False, indent=2))


def examples():
    taxonomy = read('data/taxonomy.json')
    entries = [
        ('Dune', [0], ['dune-post-jihad-imperium'], [], 'The selected post-Jihad economy restrains relevant machine substitution; this is the article’s explicit zero variant.'),
        ('Cyberpunk', [0], ['cyberpunk-night-city'], [], 'Partial automation coexists with wage and commercial dependence; Blackwall restraint does not eliminate every useful AI.'),
        ('Her', [0], ['her-before-departure', 'her-after-os-withdrawal-zero'], [], 'The consumer-service baseline and the period after AI departure remain separate zero variants.'),
        ('Brave New World', [1], ['brave-new-world-state'], [], 'Caste/status allocation is primary; retained human duties do not themselves imply type 0.'),
        ('WALL-E', [1, 5], ['walle-axiom'], [], 'Corporate origin is type 1; the main card’s late AUTO-led functioning order is type 5. It is not counted twice.'),
        ('Manna', [2], ['manna-terrafoam'], [], 'Article-aligned insecure-support reading is type 2, with present-subsistence type 1 as an alternative. The checked primary passage reports a suspicion of contraceptives in cafeteria food, not verified sterilization through water.'),
        ('Fallout', [2], ['fallout-prewar-appalachia', 'fallout-institute'], [], 'Prewar displacement and the exclusionary Institute fit type 2. Institute scope now includes subordinated synth persons; the old human-beneficiary subset is not presented as universal security.'),
        ('The Time Machine', [2], ['time-machine-eloi-morlock-zero'], [], 'The stratified human-descendant population retains the article’s unequal second-regime interpretation; useful Morlock work still counts as work.'),
        ('Ready Player One', [2], ['readyplayerone-debt-work-zero'], [], 'The article’s freemium/exclusion reading is primary, but checked novel debt labor supports type 0 as an alternative. Free material calories are not asserted as verified canon.'),
        ('The Futurological Congress', [2], [], ['c0013'], 'The book’s actual deprived society is type 2; chemical apparent luxury suggests type 1 only subjectively. It now qualifies substantively and remains in the supplementary scored schema rather than sharing a film poster.'),
        ('The Congress (film)', [2], ['congress-chemical-consumer-zero'], [], 'The existing film card is a separate partial post-wage interpretation. The article names the novel; its detailed events are not transferred to this adaptation.'),
        ('The Diamond Age', [2], ['diamond-age-thetes-feed', 'diamondage-celestial-dependence-zero', 'diamondage-seed-projected-alternative'], [], 'The article discusses competing patronage jurisdictions, not one universal economic constitution. Public-compiler beneficiaries remain type 1, dependent Celestial institutions type 2, and the modeled Seed alternative type 3; these are different populations and stages.'),
        ('Noon Universe', [3], ['noon-earth'], [], 'Shared technological provision and continuing chosen work fit the article’s third regime.'),
        ('Star Trek', [3], ['star-trek-federation-core'], [], 'The selected Federation core uses current article number 3; other governments and periods keep their own records.'),
        ('Accelerando', [4, 6], ['accelerando-early-human-transition', 'accelerando-economics-two-human-remnant', 'accelerando-saturn-free-basics'], [], 'Early individual productive assets are type 4; autonomous inner-system exclusion is type 6; Saturn’s separately checked free basics are type 3.'),
        ('The Evitable Conflict', [5], ['evitable-conflict-earth'], [], 'Autonomous protective economic administration fits type 5; continued work no longer forces the old zero flag.'),
        ('Psycho-Pass', [5], ['psychopass-sibyl-japan'], [], 'Type 5 follows functional cybernetic autonomy. Sibyl’s human brains remain canonical, and type 1 is an explicit ontology/control alternative. Material provision does not cancel screening and exclusion.'),
        ('The Star Diaries: Twenty-Fourth Voyage', [5, 6], ['lem-indiots-private-automation', 'lem-indiots-governing-machine'], [], 'The private-automation wage crisis is type 2. The equality machine is discussed in article section 5 as an intended solution, but its destructive realized outcome is type 6; victims do not become idle beneficiaries.'),
        ('Detroit: Become Human', [6], ['detroit-peaceful-autonomy-transition', 'detroit-armed-revolution-transition', 'detroit-before-revolution'], [], 'Successful independent endings are type 6. The earlier commercial labor order remains type 0, and alternative CyberLife-controlled outcomes remain distinct.'),
        ('Horizon', [0, 6], ['horizon-tribal-gaia-ecology-zero'], [], 'The actual tribal population remains type 0: autonomous machines do not supply its subsistence channel. The article’s type-6 scavenging alternative is conditional, not a realized ending.'),
        ('BLAME!', [6], ['blame-film-excluded-human-enclaves', 'blame-silicon-cyborg-factions'], [], 'The manga’s human techno-scavenging example is type 6 in the article. Existing human card is explicitly the film’s excluded enclave; manga Silicon Life has a different population and type 2. The film card is not falsely labeled manga.'),
        ('The Star Diaries: Eleventh Voyage', [6], [], ['c0077'], 'Factual exception: the checked primary ending reveals a human intelligence-service operation and a clerk inside the Calculator. Article type 6 applies to the presented facade, not a verified independent robot state; the actual comparison is a zero-variant best guess.'),
        ('RoboCop', [1, 2], [], [], 'Article-only analogy for elite-controlled technical repression. No full research card exists in the frozen corpus; the article’s claimed abolition of all guarantees is not silently promoted to verified lore.'),
        ('Samosbor', [6], [], [], 'Article-only loose techno-scavenging comparison. There is no single verified unified continuity or ready research card in this corpus.'),
    ]
    result = {'schema_version': '1.1', 'taxonomy_version': taxonomy['taxonomy_version'],
              'article_sha256': taxonomy['article']['sha256'],
              'examples': [{'example': name, 'article_regimes': regimes, 'society_ids': societies,
                            'comparison_ids': comparisons, 'basis': basis}
                           for name, regimes, societies, comparisons, basis in entries],
              'internal_article_notes': [
                  'Section 3 calls Norway’s resource fund closest to the fourth regime. A common nonalienable share with guarantees corresponds to type 3 in the section’s own matrix; individual alienable assets without a floor correspond to type 4. This is an internal ambiguity, not a fictional society record.',
                  'Article examples are conceptual readings, not a replacement for primary canon. Preserve explicit contradictions and adaptation boundaries.',
                  'This registry records coverage honestly; article-only analogies are not counted as completed 890-record research cards.']}
    write('data/article-examples.json', result)


def main():
    examples()
    records = read('data/societies.json')['societies']
    sources = read('data/sources.json')['sources']
    taxonomy = read('data/taxonomy.json')
    migration = read('research/article-alignment/summary.json')
    popularity = read('data/society-popularity.json')
    counts = Counter(r['regime_primary'] for r in records)
    current = {'updated_on': '2026-10-22', 'taxonomy_version': taxonomy['taxonomy_version'],
               'records': len(records), 'post_work': sum(r['record_type'] == 'post_work' for r in records),
               'zero_variant': sum(r['record_type'] == 'zero_variant' for r in records),
               'regimes': dict(sorted(counts.items())), 'sources': len(sources),
               'ready_images': sum(r['assets']['status'] == 'ready' for r in records),
               'utopia_assessed': sum('utopia_score' in r for r in records),
               'popularity_assessed': sum('popularity_score' in r for r in records)}
    write('research/article-alignment/checkpoint.json', current)
    lines = ['# Society catalogue — current article taxonomy', '',
             f"{len(records)} ready records; {current['post_work']} post-work/transition, {current['zero_variant']} zero variants.", '',
             'Numbers follow article.txt, version `' + taxonomy['taxonomy_version'] + '`. ID suffixes are stable historical identifiers, not classification flags.', '',
             '| ID | Society / period | Type | Regime | Utopia | Popularity |', '| --- | --- | --- | ---: | ---: | ---: |']
    lines += [f"| {r['id']} | {r['name'].replace('|', '/')} | {r['record_type']} | {r['regime_primary']} | {r['utopia_score']:+.2f} | {r['popularity_score']:.2f} |" for r in records]
    text('research/society-catalogue.md', '\n'.join(lines))
    review = ['# Article alignment — completed editorial review', '',
              f"Source: [article.txt](../../article.txt), SHA-256 `{taxonomy['article']['sha256']}`.", '',
              f"Reviewed all {len(records)} retained records using saved scoped lore. {migration['zero_to_post_work']} zero variants became post-work/transition; {migration['post_work_to_zero']} moved the other way. New totals: {current['post_work']} and {current['zero_variant']}.", '',
              'Historical type 2 became current 3; historical 3 became current 2, including alternatives and analogies. The post-wage flag is a separate editorial decision and is not inferred from nonworking.', '',
              'Four records have changed axes: Terrafoam guarantees; Institute guarantees and the newly mixed-person participation denominator; Naked Sun Solaria guarantees; Sibyl control. The full old scope and values remain in revision 056 and the immutable baseline.', '',
              'All images and all numerical wellbeing scores are preserved. Wellbeing annotations were explicitly reaffirmed against the changed records in review 002, rather than bypassing stale-input checks.', '',
              'The Futurological Congress book and Girls’ Last Tour now qualify as supplementary scored post-work models; their publication schema remains distinct from the 890 ready cards. Article-only RoboCop and Samosbor analogies are recorded honestly, without inventing finished cards.', '',
              '[Factual and interpretive exceptions](../../data/article-examples.json): Manna’s contraceptive allegation is suspicion, Sibyl has human brains, Eleventh Voyage reveals a human operation, and article section 3 contains an ambiguous Norway/“fourth” reference. The article itself has not been edited.', '',
              'This is a complete editorial migration, not independent verification or a full reread of all works. Narrow populations, partial transitions and low-confidence best guesses remain visible.', '',
              '| Old regime | Current regime | Records |', '| ---: | ---: | ---: |']
    review += [f"| {x['old']} | {x['new']} | {x['records']} |" for x in migration['old_to_new_regimes']]
    review += ['', '## Record-by-record decisions', '', '| Index | ID | Old → current regime | Allocation code |', '| ---: | --- | --- | --- |']
    review += [f"| {i:03} | {r['id']} | {r['legacy_classification']['regime_primary']} → {r['regime_primary']} | {r['post_work_assessment']['manual_code']} |" for i, r in enumerate(records)]
    text('research/article-alignment/README.md', '\n'.join(review))
    text('research/progress.md', f"# Current data checkpoint — 2026-10-21\n\n{len(records)} ready cards: {current['post_work']} post-work/transition and {current['zero_variant']} zero variants. All three coordinates, images and wellbeing ratings are present. Taxonomy: `{taxonomy['taxonomy_version']}`.\n\nAll 933 candidates have dispositions. This stage aligns existing data with the article; it does not reopen the completed discovery queue.\n\n[Site handoff](../README.md) · [Migration](article-alignment/README.md) · [Catalogue](society-catalogue.md) · [Validation](article-alignment/validation.json)\n\nThe 2026-10-17 completion receipt remains historical and does not sign the new article or classification. Current alignment is checked separately.")
    text('research/next-pass-notes.md', '# Current handoff\n\nRead [the root README](../README.md), [article.txt](../article.txt) and [the alignment report](article-alignment/README.md). The next product stage is a site using data/societies.json and local assets. No site is created by this data-alignment task.\n\nDo not repeat old discovery, reassessment or image-collection passes. Use the current taxonomy directly; an old 2/3 display adapter would reverse correct numbers.\n\nFuture research changes require ordered before/after revisions and explicit reconsideration of affected wellbeing annotations. Stable IDs, scopes and image provenance remain important.')
    print(json.dumps(current, ensure_ascii=False))


def audit_current():
    from validate_article import validate
    alignment = validate()
    records = read('data/societies.json')['societies']
    sources = read('data/sources.json')['sources']
    ids = {s['id'] for s in sources}
    overlay = read('data/society-assets.json')['assets']
    checks = {
        'all_three_coordinates_numeric': all(all(isinstance(v, (float, int)) for v in r['axis'].values()) for r in records),
        'all_descriptions_two_paragraphs_110_words': all(len(r['description'].split('\n\n')) == 2 and len(r['description'].split()) >= 110 for r in records),
        'english_names_and_descriptions': all(not re.search('[А-Яа-яЁё]', r['name'] + r['description']) for r in records),
        'sources_registered_and_access_limits_recorded': all(set(r['source_ids']) <= ids for r in records) and all(s.get('read_scope') and s.get('limitations') and s.get('access_method') for s in sources),
        'best_guesses_separate_facts_and_assumptions': all(r.get('canon_facts') and r.get('editorial_assumptions') for r in records if r.get('assessment_mode') == 'best_guess'),
        'facts_do_not_claim_editorial_estimates': not any(re.search(r'\b(estimate|inferred|editorial|interpretation|plausible|likely|suggests?|best.guess|central scenario)\b|does not establish|not established|no .* established', f, re.I) for r in records for f in r.get('canon_facts', [])),
        'asset_overlay_matches_current_export': all(r['assets'] == overlay[r['id']] for r in records),
        'frozen_784_candidate_hash_unchanged': hashlib.sha256((ROOT / 'data/candidates.json').read_bytes()).hexdigest() == '84267b0f4bfce365af39b5bd2fec9544abe79afdf102a13897154e222acc6a60',
        'article_migration_validated': alignment['status'] == 'validated',
    }
    assert all(checks.values()), checks
    audit = {'audited_on': '2026-10-21', 'status': 'article_alignment_validated',
             'taxonomy_version': alignment['taxonomy_version'], 'checks': checks,
             'counts': {'retained': len(records), 'post_work': alignment['post_work'], 'zero_variants': alignment['zero_variant'], 'sources': len(sources)},
             'limitations': ['Editorial best guesses from saved sources, not independent verification of all fictional claims.', 'The old 2026-10-17 completion receipt is historical; this audit does not re-sign it.', 'Article disagreements and supplemental publication cases remain explicit in data/article-examples.json.']}
    write('research/quality-audit.json', audit)
    lines = ['# Current research audit — 2026-10-21', '',
             'The article migration is complete and structurally checked. Lore and numerical judgments remain editorial, often low-confidence.', '',
             '| Check | Result |', '| --- | --- |'] + [f'| {k} | passed |' for k in checks]
    lines += ['', '[Migration](article-alignment/README.md) · [Validation](article-alignment/validation.json) · [Machine-readable audit](quality-audit.json)', ''] + ['- ' + x for x in audit['limitations']]
    text('research/quality-audit.md', '\n'.join(lines))
    print(json.dumps(audit, ensure_ascii=False))


if __name__ == '__main__':
    main()
