"""One-time migration for the user's explicit 2026-10-16 scope clarification."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research" / "batches" / "batch-002.json"

SPECS = [
    {
        "candidate_id": "c0007", "id": "evitable-conflict-earth",
        "name": "The Evitable Conflict", "work": "The Evitable Conflict", "society": "Earth under the Machines",
        "media": ["book", "short_story"], "period": "The 2052 world economy under the four Machines",
        "population": "Human inhabitants of the machine-coordinated world economy",
        "analogy": 5, "guarantees": -0.6, "control": -0.9,
        "g_interval": [-0.9, -0.2], "c_interval": [-1, -0.7],
        "sources": ["src-asimov-cove", "src-asimov-litcharts"],
        "description": "The Machines coordinate the world's economy and protect its overall stability. Their decisions can quietly remove opponents from influential positions, leaving human officials with much less control than their titles suggest. That puts this society near the autonomous-machine end of the control axis, with a broadly protective material orientation. It is a useful analogue for the article's fifth regime.\n\nIt is nevertheless retained as a zero variant because the reviewed evidence still describes plant workers, layoffs, and shortages of human labor. Machine coordination does not itself show that people obtain their necessities independently of employment. The guarantees score describes the system's protective orientation and has a wide range; it is not proof of an explicit universal entitlement. No nonworking fraction is manufactured from the fact that computers govern. A primary-text pass remains a named research gap before the record can be considered complete.",
        "g_basis": "Machine protection and economic security are supported by secondary summaries; a universal entitlement is less explicit.",
        "c_basis": "The Machines make decisive economic choices beyond meaningful human oversight.",
        "z_basis": "Human employment remains important in the consulted accounts; no population participation figure is given.",
        "uncertainties": ["Primary story review is still required to strengthen this provisional literary assessment.", "Freedom from unemployment is not the same as freedom from employment."]
    },
    {
        "candidate_id": "c0009", "id": "brave-new-world-state",
        "name": "Brave New World (original novel)", "work": "Brave New World", "society": "World State",
        "media": ["book"], "period": "The World State described by Mustapha Mond in the original novel",
        "population": "Humans within the World State's caste order",
        "analogy": 1, "guarantees": -0.55, "control": 0,
        "g_interval": [-0.8, -0.15], "c_interval": [-0.05, 0.1],
        "sources": ["src-huxley-16"],
        "description": "The World State offers a managed material life within an engineered caste system. Its rulers decide what people are suited to do and organize consumption and employment around social stability. This places control near the concentrated elite band. The provision score recognizes the regime's supplied routine while allowing for its coercive, conditional structure; engineered contentment is not by itself evidence of secure universal rights.\n\nThe original novel belongs to the zero variant. In Chapter 16, Mond explains that the authorities retain labor, reject available labor-saving processes, and keep agricultural work that technology could reduce. Automation's possibility is deliberately prevented from becoming a general release from work. That makes it a different case from people living entirely on robot output. The description concerns Huxley's novel; television adaptations must be checked independently. The population-wide fraction of nonworkers is unknown and is not set to zero merely because employment is pervasive.",
        "g_basis": "Managed subsistence exists, but it accompanies a conditioned caste and labor order.",
        "c_basis": "The Controllers decide the use of productive technology and the population's roles.",
        "z_basis": "Retained work is explicit, but neither the age structure nor a full participation rate is established.",
        "uncertainties": ["The score concerns the original novel, not the 2020 Indra storyline.", "Political coercion and material provision are recorded as different dimensions."]
    },
    {
        "candidate_id": "c0010", "id": "orwell-oceania",
        "name": "Nineteen Eighty-Four (Oceania)", "work": "Nineteen Eighty-Four", "society": "Oceania",
        "media": ["book"], "period": "Oceania during Winston Smith's story",
        "population": "Humans living under Oceania's Party order",
        "analogy": 3, "guarantees": 0.85, "control": 0,
        "g_interval": [0.6, 1], "c_interval": [-0.05, 0.1],
        "sources": ["src-orwell-1984"],
        "description": "Oceania combines concentrated political command with deprivation and extensive human work. Access to a comfortable material life is not a reliable universal entitlement, so the guarantee score lies near the weak end. The Party's hierarchy, rather than a self-governing machine civilization, determines the system's purposes. The control score therefore stays close to elite human command.\n\nThis is a zero variant about suppressing the benefits technology might make possible. The embedded Goldstein text argues that machinery could remove drudgery, while continuous war consumes output that might otherwise improve living conditions. The existence of that argument does not mean the society shown has already abolished employment. Its role in the database is to contrast technical capacity with political choice. Because the treatise is itself an in-universe political document and the novel supplies no employment census, neither its economic account nor a precise nonworking percentage is treated as an independently measured fact.",
        "g_basis": "Depicted deprivation and the regime's preservation of scarcity oppose reliable universal access.",
        "c_basis": "The Party's hierarchy directs the social order; no autonomous AI sovereign is established.",
        "z_basis": "Human work persists, but no defensible population-wide fraction is provided.",
        "uncertainties": ["Goldstein's account is an embedded, politically mediated text.", "More chapter-specific primary locators would strengthen the final review."]
    },
    {
        "candidate_id": "c0011", "id": "midas-compulsory-consumption",
        "name": "The Midas Plague (compulsory-consumption phase)", "work": "The Midas Plague", "society": "Compulsory-consumption society",
        "media": ["short_story", "book"], "period": "The quota regime before robot consumption becomes the proposed remedy",
        "population": "Human members of the consumption-quota society",
        "analogy": 1, "guarantees": -0.8, "control": 0,
        "g_interval": [-0.95, -0.5], "c_interval": [-0.15, 0.3],
        "sources": ["src-midas-ryder"],
        "description": "Robots produce such an abundance of goods that ordinary deprivation is inverted: the burden is having to consume more than one wants. The material score is strongly toward provision, while control stays near a centrally imposed human quota order. The arrangement illustrates why plentiful output alone does not establish personal freedom or a voluntary use of time.\n\nFollowing the article's interpretation, compulsory consumption is treated as retained social work, making this phase a zero variant. A human freed from factory labor can still be assigned an exhausting obligation that keeps the production system going. The later move toward robot consumers may constitute a different arrangement, but it is not silently averaged into this phase. This pass relies on an identified scholarly discussion; the primary ending and the exact authority over production remain review gaps. No numeric nonworking share is inferred from the disappearance of manufacturing jobs.",
        "g_basis": "Excess material output supports provision, though compulsory consumption is coercive.",
        "c_basis": "Quota administration indicates concentrated control; detailed productive ownership remains a gap.",
        "z_basis": "Consumption is counted as imposed social work here; there is no participation census.",
        "uncertainties": ["A primary-text review is needed for productive ownership and the ending.", "Whether compulsory consumption counts as work is an explicit interpretive choice, matching the supplied article."]
    }
]

def main():
    batch = json.loads(PATH.read_text(encoding="utf-8"))
    by_id = {r["id"]: r for r in batch["societies"]}
    decisions = {r["candidate_id"]: r for r in batch["decisions"]}
    for s in SPECS:
        assessment = {
            "guarantees": {"interval": s["g_interval"], "confidence": "low", "basis": s["g_basis"], "source_ids": s["sources"]},
            "control": {"interval": s["c_interval"], "confidence": "medium", "basis": s["c_basis"], "source_ids": s["sources"]},
            "nonworking": {"interval": None, "confidence": "low", "basis": s["z_basis"], "source_ids": s["sources"]}
        }
        r = {k: s[k] for k in ["id", "candidate_id", "name", "work", "society", "media", "description"]}
        r.update({
            "record_type": "zero_variant",
            "scope": {"continuity": "Original prose work", "period": s["period"], "population": s["population"],
                      "human_population_proxy": False, "exclusions": ["Other adaptations", "Later materially changed regimes"],
                      "branch": None, "player_configurable": False},
            "axis": {"guarantees": s["guarantees"], "control": s["control"], "nonworking": None},
            "axis_assessment": assessment,
            "regime_primary": 0, "regime_analogy": s["analogy"], "regime_alternatives": [],
            "qualification": "included",
            "evidence": [{"claim": decisions[s["candidate_id"]]["reason"], "source_ids": s["sources"],
                          "locator": "See source read_scope and the retained decision analysis", "kind": "interpretation"}],
            "uncertainties": s["uncertainties"], "source_ids": s["sources"],
            "assets": {"status": "deferred", "poster": None, "icon": None},
            "review": {"status": "reviewed", "date": "2026-10-16", "method": "Second pass after the user's explicit zero-variant inclusion clarification; no independent reviewer", "coordinate_ready": False}
        })
        by_id[s["id"]] = r
        d = decisions[s["candidate_id"]]
        d["previous_status"] = "boundary_case"
        d["status"] = "zero_variant"
        d["society_id"] = s["id"]
        d["scope_clarification"] = "User explicitly requested inclusion of zero variants on 2026-10-16."
    batch["societies"] = sorted(by_id.values(), key=lambda r: r["candidate_id"])
    batch["review_notes"] = [n for n in batch["review_notes"] if "total confirmed count" not in n]
    batch["review_notes"].append("User clarification: this batch retains one post-work and four zero-variant society records; other cases keep their admission gaps.")
    PATH.write_text(json.dumps(batch, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("Applied explicit zero-variant inclusion clarification to four researched records.")

if __name__ == "__main__":
    main()
