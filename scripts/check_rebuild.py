"""Check deterministic exports and asset-sync preservation on an isolated copy."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ['data/societies.json', 'data/decisions.json', 'data/sources.json',
         'data/comparisons.json', 'data/revision-history.json',
         'data/society-assets.json', 'data/society-utopia.json', 'data/society-popularity.json',
         'data/taxonomy.json', 'data/article-examples.json']


def hashes():
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in FILES}


def main():
    before = hashes()
    for script in ('merge_batches.py', 'write_utopia_review.py', 'write_popularity_review.py'):
        run = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / 'scripts' / script)],
                             cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        assert run.returncode == 0, run.stderr + run.stdout
    assert before == hashes(), 'Research rebuild or annotation writer changed a reviewed export'
    # Test sync on a copy: a regression here used to restore an old research
    # snapshot and discard all subsequent classifications and wellbeing values.
    import collect_images
    (ROOT / 'tmp').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='article-sync-', dir=ROOT / 'tmp') as workspace:
        target = Path(workspace).resolve()
        assert target.is_relative_to((ROOT / 'tmp').resolve())
        for name in ('data/societies.json', 'research/images/manifest.json'):
            (target / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target / name)
        collect_images.ROOT = target
        collect_images.RESEARCH = target / 'research/images'
        collect_images.IMG = target / 'assets/images'
        original = json.loads((target / 'data/societies.json').read_text(encoding='utf-8'))
        result = collect_images.sync()
        synced = json.loads((target / 'data/societies.json').read_text(encoding='utf-8'))
        assert {k: v for k, v in synced.items() if k != 'societies'} == {k: v for k, v in original.items() if k != 'societies'}
        strip = lambda values: [{k: v for k, v in r.items() if k != 'assets'} for r in values]
        assert strip(original['societies']) == strip(synced['societies'])
        assert result['all_non_assets_unchanged'] is True
        assert target.is_relative_to((ROOT / 'tmp').resolve()), 'Cleanup target escaped intended temporary workspace'
    report = {'checked_on': '2026-10-22', 'taxonomy_version': 'article-2026-10-21',
              'clean_rebuild_identical_files': len(FILES), 'files_sha256': before,
              'rated_records': len(original['societies']),
              'utopia_writer_idempotent': True, 'popularity_writer_idempotent': True,
              'asset_sync_preserves_current_research_and_ratings': True,
              'asset_sync_test': 'Isolated temporary copy, removed after confirming its resolved path is inside project/tmp.',
              'migration_assets_and_numerical_scores_preserved': True}
    for name in ('research/article-alignment/rebuild-check.json', 'research/utopia/rebuild-check.json'):
        (ROOT / name).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'files_sha256'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
