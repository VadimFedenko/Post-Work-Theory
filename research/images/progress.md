# Image collection progress

Updated: 2026-10-17T18:16:49+00:00

Prepared records: **890 / 890**; remaining: **0**.
Unique image groups: 671. Status: {'prepared': 671}.

All research fields other than `assets` are preserved and checked against `baseline-societies.json`. No website is built. Originals retain downloaded bytes; posters are 320 × 480 WebP; icons are 32 × 32 PNG, with separate circular previews.

## Resume

```powershell
python scripts/collect_images.py --all
python scripts/collect_images.py --validate
```

`data/society-assets.json` is the authoritative overlay. The merge utility must apply it after historical research revisions. Discovery metadata, failed requests, URLs, rights statements, matching notes and crop coordinates are retained in the manifest/cache/event journal.

## Remaining groups

None.

Visual review: 671 / 671 image groups. Generated fallback illustrations: 1.

[Image-stage handoff and source details](README.md) · [Validation](validation.json) · [Contact-sheet index](contact-sheets/index.json)
