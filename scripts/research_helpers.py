"""Small serialization helpers. Every description, score and claim is supplied explicitly."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-10-16"

def source(identity, title, author, url, kind, access, scope, limitations):
    return {"id": identity, "title": title, "author": author, "url": url, "kind": kind,
            "accessed_on": DATE, "access_method": access, "read_scope": scope, "limitations": limitations}

def assessment(value, interval, confidence, basis, sources):
    if value is None and interval is not None:
        raise ValueError("An unresolved point must not acquire a fabricated interval")
    return {"interval": interval, "confidence": confidence, "basis": basis, "source_ids": sources}

def record(identity, candidate, name, work, society, media, scope, description, axes,
           assessments, regime, sources, evidence, uncertainties, record_type="post_work",
           alternatives=None, analogy=None):
    ready = all(value is not None for value in axes.values())
    result = {"id": identity, "candidate_id": candidate, "name": name, "work": work, "society": society,
              "media": media, "record_type": record_type, "scope": scope, "description": description,
              "axis": axes, "axis_assessment": assessments, "regime_primary": regime,
              "regime_alternatives": alternatives or [], "qualification": "included",
              "source_ids": sources, "evidence": evidence, "uncertainties": uncertainties,
              "assets": {"status": "deferred", "poster": None, "icon": None},
              "review": {"status": "reviewed", "date": DATE,
                         "method": "Second pass against the gathered passages, including explicit uncertainty; no independent reviewer",
                         "coordinate_ready": ready}}
    if record_type == "zero_variant":
        result["regime_analogy"] = analogy
    return result

def scope(continuity, period, population, exclusions, proxy=False, **extra):
    return {"continuity": continuity, "period": period, "population": population,
            "human_population_proxy": proxy, "exclusions": exclusions, "branch": None,
            "player_configurable": False, **extra}

def evidence(claim, sources, locator, kind="interpretation"):
    return {"claim": claim, "source_ids": sources, "locator": locator, "kind": kind}

def decision(candidate, status, reason, sources, analysis=None, follow_up=None, society_id=None, **extra):
    result = {"candidate_id": candidate, "status": status, "reason": reason, "source_ids": sources, **extra}
    if society_id:
        result["society_id"] = society_id
    if analysis:
        result["analysis"] = analysis
    if follow_up:
        result["follow_up"] = follow_up
    return result

def write_batch(number, candidate_ids, sources, societies, decisions, notes):
    data = {"batch_id": f"batch-{number:03d}", "researched_on": DATE, "candidate_ids": candidate_ids,
            "sources": sources, "societies": societies, "decisions": decisions, "review_notes": notes}
    path = ROOT / "research" / "batches" / f"batch-{number:03d}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"batch": number, "decisions": len(decisions), "records": len(societies)}))
