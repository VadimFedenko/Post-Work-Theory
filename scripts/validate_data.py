"""Meaningful integrity checks for the research corpus; no web/application code."""
import json
from collections import Counter
from pathlib import Path
from candidate_queue import load_queue
from completion_state import completion_review, CORE_FILES

ROOT = Path(__file__).resolve().parents[1]
MEDIA = {"book", "short_story", "movie", "tv", "anime", "cartoon", "manga", "comic", "game", "tabletop", "play", "audio", "web_fiction", "webcomic"}
STATUSES = {"included", "zero_variant", "supplementary", "boundary_case", "excluded", "needs_evidence", "duplicate"}

def read(name, key):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))[key]

def unique(items, key):
    ids = [r[key] for r in items]
    assert len(ids) == len(set(ids)), f"Duplicate {key}"
    return set(ids)

def retained_ids(decision):
    """Keep legacy single links while allowing evidenced period/continuity splits."""
    if "society_ids" not in decision:
        return [decision["society_id"]]
    linked = decision["society_ids"]
    assert isinstance(linked, list) and linked and len(linked) == len(set(linked))
    assert decision["society_id"] == linked[0], "Legacy link must identify the first retained record"
    if len(linked) > 1:
        assert decision.get("split_rationale"), "Multiple records require an evidenced scope distinction"
    return linked

def main():
    frozen_candidates, expansion_candidates, candidates = load_queue()
    sources = read("sources.json", "sources")
    societies = read("societies.json", "societies")
    decisions = read("decisions.json", "decisions")
    cids, sids = unique(candidates, "id"), unique(sources, "id")
    records = unique(societies, "id")
    record_map = {r["id"]: r for r in societies}
    dids = unique(decisions, "candidate_id")
    assert [r["order"] for r in candidates] == list(range(1, len(candidates)+1))
    assert len(candidates) >= 500, "Initial discovery queue below requested scale"
    assert dids <= cids
    # The ordinary research pass must follow the fixed queue. A separate follow-up
    # may revisit earlier unresolved cases, but must not conceal skipped candidates.
    processed_orders = sorted(int(cid[1:]) for cid in dids)
    assert processed_orders == list(range(1, len(decisions)+1)), "Unrecorded gap in sequential research"
    decision_map = {r["candidate_id"]: r for r in decisions}
    for c in candidates:
        assert c["media"] and set(c["media"]) <= MEDIA, c["id"]
        assert c["metadata_verified"] is False, "Discovery metadata must not imply individual verification"
    for source in sources:
        assert source["url"].startswith("https://")
        assert source["kind"] and source["read_scope"] and source["limitations"]
    for d in decisions:
        assert d["status"] in STATUSES and d["reason"]
        if "source_ids" in d:
            assert d["source_ids"] and set(d["source_ids"]) <= sids
        if d["status"] not in {"included", "zero_variant"}:
            assert d.get("analysis") and d.get("follow_up"), "A non-inclusion needs its reasoning and next action"
        if d["status"] in {"included", "zero_variant"}:
            linked = retained_ids(d)
            assert set(linked) <= records
            assert all(record_map[sid]["candidate_id"] == d["candidate_id"] for sid in linked), "A retained link crosses candidate identities"
            expected_status = "included" if any(record_map[sid]["record_type"] == "post_work" for sid in linked) else "zero_variant"
            assert d["status"] == expected_status
            scopes = [(record_map[sid]["scope"]["continuity"], record_map[sid]["scope"]["period"], record_map[sid]["scope"]["population"]) for sid in linked]
            assert len(scopes) == len(set(scopes)), "Identical scopes cannot be counted twice"
        if d["status"] == "duplicate":
            assert d.get("duplicate_of") in records, "Duplicate must resolve to an actual retained record"
        if "comparison_assessment" in d:
            comp = d["comparison_assessment"]
            assert d.get("current_policy_review") is True and d.get("reassessed_on")
            assert d["status"] not in {"included", "zero_variant", "duplicate"}
            assert comp["counted_toward_goal"] is False
            assert comp["canon_facts"] and comp["editorial_assumptions"] and comp["scope"]
            assert comp["confidence"] == "low" and comp["media"] and set(comp["media"]) <= MEDIA
            assert comp["source_ids"] and set(comp["source_ids"]) <= sids
            for key in ("guarantees", "control", "nonworking"):
                if comp["axis"][key] is None:
                    assert comp["intervals"][key] is None
                    assert comp.get("not_applicable_axes", {}).get(key), "A comparison null needs a definite inapplicability reason"
                    continue
                low, high = comp["intervals"][key]
                minimum = 0 if key == "nonworking" else -1
                assert minimum <= low <= comp["axis"][key] <= high <= 1
    for r in societies:
        assert r["candidate_id"] in cids
        d = decision_map[r["candidate_id"]]
        assert d["status"] in {"included", "zero_variant"}
        assert r["id"] in retained_ids(d)
        assert r["qualification"] == "included"
        assert r["media"] and set(r["media"]) <= MEDIA
        assert r["source_ids"] and set(r["source_ids"]) <= sids
        if r.get("assessment_mode") == "best_guess":
            assert r.get("qualification_basis") and r.get("qualification_confidence") in {"low", "medium", "high"}
            assert r.get("canon_facts") and r.get("editorial_assumptions"), "Best guesses must separate reference facts from assumptions"
            assert all(isinstance(x, str) and x.strip() for x in r["canon_facts"] + r["editorial_assumptions"])
            assert all(v is not None for v in r["axis"].values()), "Current best guesses must supply all three coordinates"
            for key in r.get("best_guess_axes", r["axis"].keys()):
                assert r["axis_assessment"][key]["confidence"] == "low", "Editorial gaps must not become confident lore statistics"
        if "employment_preservation" in r:
            preservation = r["employment_preservation"]
            assert preservation["retained_artificial_jobs"] is True
            assert preservation["basis"]
            assert preservation["source_ids"] and set(preservation["source_ids"]) <= set(r["source_ids"])
            assert preservation["does_not_create_additional_society"] is True
        for statistic in r.get("reported_labor_statistics", []):
            assert statistic["source_id"] in sids
            assert statistic["denominator"] and statistic["locator"]
        assert len(r["description"].split()) >= 110, r["id"]
        assert "\n\n" in r["description"], r["id"]
        assert r["scope"]["population"] and r["scope"]["period"]
        assert r["record_type"] in {"post_work", "zero_variant"}
        assert 0 <= r["regime_primary"] <= 6
        if "utopia_score" in r:
            score, assessment = r["utopia_score"], r["utopia_assessment"]
            assert isinstance(score, (float, int)) and not isinstance(score, bool) and -1 <= score <= 1
            assert assessment["basis"] and assessment["confidence"] in {"low", "medium", "high"}
            assert assessment["source_ids"] and set(assessment["source_ids"]) <= sids
            assert assessment["assessment_mode"] == "editorial_best_guess"
        assert (r["regime_primary"] == 0) == (r["record_type"] == "zero_variant")
        for axis in ["guarantees", "control", "nonworking"]:
            value = r["axis"][axis]
            assessment = r["axis_assessment"][axis]
            assert assessment["confidence"] in {"high", "medium", "low"}
            assert assessment["basis"] and set(assessment["source_ids"]) <= sids
            if value is None:
                assert assessment["interval"] is None
                assert not r["review"]["coordinate_ready"]
            else:
                low, high = assessment["interval"]
                minimum = 0 if axis == "nonworking" else -1
                assert minimum <= low <= value <= high <= 1, (r["id"], axis)
        for ev in r["evidence"]:
            assert ev["locator"] and ev["claim"] and set(ev["source_ids"]) <= sids
        asset = r["assets"]
        assert asset["status"] in {"deferred", "pending", "ready"}
        if asset["status"] == "ready":
            assert all(asset.get(k) for k in ("original", "poster", "icon", "source_page", "original_sha256"))
            assert asset.get("source_url") or asset.get("provider") == "imagegen"
            assert asset.get("rights") and "author" in asset
            for key in ("original", "poster", "icon"):
                target = (ROOT / asset[key]).resolve()
                assert target.is_relative_to((ROOT / "assets").resolve()), "Asset path escapes assets directory"
                assert target.is_file(), f"Missing {key}: {asset[key]}"
        else:
            assert asset["poster"] is None and asset["icon"] is None
        assert r["review"]["status"] == "reviewed"
        assert r["review"]["coordinate_ready"] == all(v is not None for v in r["axis"].values())
        if r["scope"].get("person_proxy_kind") == "active_synthetic_persons":
            assert r["scope"]["human_population_proxy"] is True
            assert r["axis_interpretation"]["literal_human_nonworking"] is None
            assert r["axis_interpretation"]["nonworking"] and r["axis_interpretation"]["control"]
    counts = Counter(d["status"] for d in decisions)
    completed_review = completion_review()
    summary = {
        "candidates": len(candidates), "frozen_candidates": len(frozen_candidates),
        "expansion_candidates": len(expansion_candidates), "processed": len(decisions),
        "pending": len(candidates)-len(decisions), "included": len(societies),
        "post_work": sum(r["record_type"] == "post_work" for r in societies),
        "zero_variant": sum(r["record_type"] == "zero_variant" for r in societies),
        "coordinate_ready": sum(r["review"]["coordinate_ready"] for r in societies),
        "best_guess_records": sum(r.get("assessment_mode") == "best_guess" for r in societies),
        "synthetic_person_proxy_records": sum(r["scope"].get("person_proxy_kind") == "active_synthetic_persons" for r in societies),
        "completed_scored_comparisons": sum("comparison_assessment" in d for d in decisions),
        "remaining_coordinate_gaps": sum(not r["review"]["coordinate_ready"] for r in societies),
        "sources": len(sources), "decisions": dict(counts),
        "utopia_assessed": sum("utopia_score" in r for r in societies),
        "popularity_assessed": sum("popularity_score" in r for r in societies),
        "historical_review_missing_inputs": [name for name in CORE_FILES if not (ROOT/name).is_file()],
        "next_candidate": f"c{len(decisions)+1:04d}" if len(decisions) < len(candidates) else None,
        "goal_complete": completed_review is not None,
        "completion_review": "research/completion-review.json" if completed_review else None,
        "conservative_resident_scope_subset": completed_review['counts']['conservative_resident_scope_subset'] if completed_review else None,
        "note": "Research stage completed under the recorded user best-guess policy; coordinates are interpretations, not canonical census measurements." if completed_review else "Structural validation does not verify literary claims or prove the target has been met."
    }
    if (ROOT / 'data/taxonomy.json').exists():
        from validate_article import validate as validate_alignment
        alignment = validate_alignment()
        summary['taxonomy_version'] = alignment['taxonomy_version']
        summary['article_alignment'] = {'status': alignment['status'], 'validation': 'research/article-alignment/validation.json', 'article_sha256': alignment['article_sha256']}
        from popularity_helpers import apply_popularity_overlay
        from copy import deepcopy
        reapplied = {r['id']: deepcopy(r) for r in societies}
        apply_popularity_overlay(reapplied)
        assert all(r['popularity_score'] == reapplied[r['id']]['popularity_score'] and
                   r['popularity_assessment'] == reapplied[r['id']]['popularity_assessment'] for r in societies)
        summary['data_ready_for_site'] = all(r['review']['coordinate_ready'] and r['assets']['status'] == 'ready' and 'utopia_score' in r and 'popularity_score' in r for r in societies)
        summary['historical_completion_receipt_valid'] = completed_review is not None
        summary['note'] = 'Current article migration is validated separately. The old goal_complete flag concerns the historical receipt, not whether the current export is usable; editorial lore judgments remain low-confidence.'
    (ROOT / "data" / "progress.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(summary))

if __name__ == "__main__":
    main()
