"""Assemble research data from reviewed batches, rejecting conflicting identities."""
import json
from pathlib import Path
from utopia_helpers import apply_utopia_overlay
from popularity_helpers import apply_popularity_overlay

ROOT = Path(__file__).resolve().parents[1]

def write(name, data):
    (ROOT / "data" / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main():
    sources, societies, decisions = {}, {}, {}
    for path in sorted((ROOT / "research" / "batches").glob("batch-*.json")):
        batch = json.loads(path.read_text(encoding="utf-8"))
        for key, dest, id_key in [("sources", sources, "id"), ("societies", societies, "id"), ("decisions", decisions, "candidate_id")]:
            for item in batch[key]:
                if key == "societies":
                    item = {"record_type": "post_work", **item}
                identity = item[id_key]
                if identity in dest and dest[identity] != item:
                    raise ValueError(f"Conflicting {key}: {identity}. Apply an explicit correction rather than overwriting evidence.")
                dest[identity] = item
    # Reassessments are explicit, ordered changes with the entire previous value.
    # Original batches remain immutable and conflicts there are still rejected.
    revision_log = []
    for path in sorted((ROOT / "research" / "revisions").glob("revision-*.json")):
        revision = json.loads(path.read_text(encoding="utf-8"))
        assert revision.get("reason") and revision.get("revised_on")
        for change in revision["changes"]:
            key = change["collection"]
            dest = {"sources": sources, "societies": societies, "decisions": decisions}[key]
            id_key = "candidate_id" if key == "decisions" else "id"
            after = change["after"]
            identity = after[id_key]
            if dest.get(identity) != change["before"]:
                raise ValueError(f"Stale revision {path.name}: {key}/{identity}")
            dest[identity] = after
        revision_log.append({"id": revision["revision_id"], "revised_on": revision["revised_on"],
                             "reason": revision["reason"], "changes": len(revision["changes"]),
                             "path": str(path.relative_to(ROOT)).replace("\\", "/")})
    write("revision-history.json", {"schema_version": "1.0", "revisions": revision_log})
    write("sources.json", {"schema_version": "1.0", "sources": list(sources.values())})
    # Images are a separate, resumable editorial stage. Never overwrite them with
    # the historical deferred placeholders when rebuilding research batches.
    asset_overlay = ROOT / "data" / "society-assets.json"
    if asset_overlay.exists():
        assets = json.loads(asset_overlay.read_text(encoding="utf-8"))["assets"]
        unknown = set(assets) - set(societies)
        if unknown:
            raise ValueError(f"Image overlay references unknown societies: {sorted(unknown)}")
        for identity, asset in assets.items():
            societies[identity]["assets"] = asset
    # Preserve independently reviewed utopian/dystopian annotations on rebuild.
    # Reject stale annotations rather than silently reusing scores after lore edits.
    apply_utopia_overlay(societies)
    # Recognition concerns the named work/franchise, not social conditions.
    apply_popularity_overlay(societies)
    taxonomy = json.loads((ROOT / 'data/taxonomy.json').read_text(encoding='utf-8')) if (ROOT / 'data/taxonomy.json').exists() else None
    metadata = {"schema_version": "1.1", "taxonomy_version": taxonomy['taxonomy_version']} if taxonomy else {"schema_version": "1.0"}
    write("societies.json", {**metadata, "schema_version": "1.2", "societies": list(societies.values())})
    write("decisions.json", {**metadata, "decisions": list(decisions.values())})
    comparisons = [{"candidate_id": d["candidate_id"], "decision_status": d["status"],
                    "reassessed_on": d["reassessed_on"], **d["comparison_assessment"]}
                   for d in decisions.values() if "comparison_assessment" in d]
    write("comparisons.json", {**metadata, "comparisons": comparisons,
                              "note": "Supplementary scored records in a distinct schema, not ready main cards. Some now qualify under the article; see each assessment. A historical disposition is not a current zero-variant flag."})
    print(json.dumps({"sources": len(sources), "societies": len(societies), "decisions": len(decisions)}))

if __name__ == "__main__":
    main()
