"""Apply a documented wording/follow-up correction, preserving historical decisions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "research" / "batches" / "batch-002.json"
data = json.loads(path.read_text(encoding="utf-8"))
updates = {
    "c0007": (
        "The Machines' economic coordination coexists with human workers, shortages and layoffs. This qualifies the retained zero variant: machine authority need not abolish employment. It does not establish a high nonworking fraction.\n\nThe record is part of the main corpus under the user's clarification. Its unresolved material-security and participation questions remain follow-ups, rather than reasons to describe the current record as unpublished or outside the database.",
        "Strengthen the existing zero-variant record with the primary regional reports and material-security statements; do not convert machine planning into a labor census."),
    "c0009": (
        "The World State preserves caste employment despite labor-saving capacity. Mond's Chapter 16 explanation supports the zero-variant classification. Material management and retained work coexist.\n\nThis original-novel record belongs in the main corpus with regime 0. Adaptations still need independent continuity checks; no employment percentage is inferred merely from the State's ability to shorten work.",
        "Strengthen the existing coordinates where possible and establish a defensible participation estimate. Assess adaptations separately; their arrangements are not automatically those of the novel."),
    "c0010": (
        "Oceania's institutions preserve labor and deprivation. The embedded political treatise discusses machinery's capacity to remove drudgery and the use of waste to defend hierarchy. Its in-universe authorship remains an evidence limitation.\n\nThe retained record is a zero variant in the main corpus, with the post-work subset counted separately. Present institutions and counterfactual potential are distinguished; the existence of machines supplies no all-age nonworking percentage.",
        "Corroborate the existing record's labor and distribution claims with additional chapter-level primary passages and review the unresolved participation coordinate."),
    "c0011": (
        "Robotic overproduction coexists with a compulsory consumption task, which the supplied article treats as retained social work. The quota period is therefore included in the main corpus as a zero variant.\n\nBatch 006 directly checked the later story's dialogue: Morey Fry's reform has already released people from that duty. Candidate c0042 now supplies the separate post-quota record midas-world-after-fry. The childhood flashbacks are not counted again, and the two periods are not averaged into one point.",
        "Still verify The Midas Plague's own ending against the primary story. The later arrangement is already researched under c0042; do not append a duplicate candidate for it.")
}
for d in data["decisions"]:
    if d["candidate_id"] in updates:
        d.setdefault("pre_clarification_analysis", d["analysis"])
        d.setdefault("pre_clarification_follow_up", d["follow_up"])
        d["analysis"], d["follow_up"] = updates[d["candidate_id"]]
        d["follow_up_reviewed_on"] = "2026-10-16"
        if d["candidate_id"] == "c0011":
            if "src-man-ate-world-primary" not in d["source_ids"]:
                d["source_ids"].append("src-man-ate-world-primary")
            d["reason"] = "The scoped order retains compulsory consumption despite automated production; the changed later arrangement has its own record under c0042."
note = "Batch 006 follow-up: current decision prose now reflects zero-variant inclusion; pre-clarification prose is preserved in explicitly historical fields. The later Midas order is covered by c0042."
if note not in data["review_notes"]:
    data["review_notes"].append(note)
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Updated four current decision explanations; preserved historical text.")
