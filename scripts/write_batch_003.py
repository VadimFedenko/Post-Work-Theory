"""Materialize the individually researched third batch; no synthetic lore generation."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-10-16"

def source(id, title, author, url, kind, method, scope, limitations):
    return {"id": id, "title": title, "author": author, "url": url, "kind": kind,
            "accessed_on": DATE, "access_method": method, "read_scope": scope,
            "limitations": limitations}

SOURCES = [
    source("src-detroit-official", "Detroit: Become Human official overview", "Quantic Dream",
           "https://www.quanticdream.com/en/detroit-become-human/flowcharts", "official_developer_overview",
           "Official page opened and read", "2038 setting, human service roles, android slavery and branching outcomes.",
           "Marketing overview; does not give an economic settlement for every ending."),
    source("src-detroit-new-home", "A New Home: transcript", "Game dialogue transcribed by the Detroit: Become Human Wiki",
           "https://detroit-become-human.fandom.com/wiki/A_New_Home_%28Transcript%29", "primary_dialogue_unofficial_transcript",
           "Indexed transcript passage read; direct access was unavailable", "CTN news report of 225,000 job losses and 37.3% unemployment.",
           "A reported unemployment figure, not the fraction of all humans who do not work. Verify against the game before final publication."),
    source("src-detroit-ending-guide", "Chapter 31: Battle for Detroit", "Andrew Testa, GameFAQs",
           "https://gamefaqs.gamespot.com/ps4/182637-detroit-become-human/faqs/75941/chapter-31-battle-for-detroit", "secondary_gameplay_guide",
           "Full relevant walkthrough section opened and read", "Peaceful demonstration, singing, public opinion and military stand-down.",
           "Documents branch conditions, not a durable post-ending economic system or an enacted rights charter."),
    source("src-hornwright-terminals", "Hornwright Industrial Headquarters terminals", "Fallout 76 terminal text, transcribed by The Vault Fallout Wiki",
           "https://fallout-archive.fandom.com/wiki/Hornwright_Industrial_Headquarters_terminals", "primary_game_text_unofficial_transcription",
           "Substantial indexed terminal extracts read; direct page returned an access error", "Daniel's automation goal, remaining staff, hiring exam, automation opposition and political collaboration.",
           "Primary terminal fragments through a fan mirror; the evidence is regional and does not measure all prewar America."),
    source("src-bethesda-motherlode", "Breach and Clear – Activity – Fallout 76", "Bethesda Support",
           "https://help.bethesda.net/app/answers/detail/a_id/51953/~/breach-and-clear---event-quest---fallout-76", "official_gameplay_documentation",
           "Indexed official activity description read", "The Motherlode is an automated mining bot at Hornwright sites.",
           "Confirms a machine and activity; labor politics come from separate terminal evidence."),
    source("src-institute-overview", "The Institute", "Fallout Wiki contributors",
           "https://fallout.fandom.com/wiki/The_Institute", "secondary_game_reference",
           "Substantial indexed faction, BioScience and labor passages read", "Directorate, scientific divisions, synth labor, food and health provision.",
           "Fan reference with game citations; direct primary dialogue and terminal review remains desirable."),
    source("src-institute-food", "Institute food synthesizer", "Fallout Wiki contributors",
           "https://fallout.fandom.com/wiki/Institute_food_synthesizer", "secondary_game_object_reference",
           "Indexed object entry read", "Commissary food-machine outputs and in-game object references.",
           "A dispenser alone does not prove food is created without inputs or that every resident has unconditional rights."),
    source("src-cyber-ai", "Artificial Intelligence", "Cyberpunk Wiki contributors",
           "https://cyberpunk.fandom.com/wiki/Artificial_Intelligence", "secondary_game_reference",
           "Relevant indexed history passage read", "Corporate and government AI use in 2077 and Blackwall containment of rogue systems.",
           "Cross-era franchise overview; the Blackwall is not evidence of a blanket ban on all AI in 2077."),
    source("src-cyber-north-oak", "North Oak (2077): Database Entry", "Cyberpunk 2077 text reproduced by Cyberpunk Wiki",
           "https://cyberpunk.fandom.com/wiki/North_Oak_%282077%29", "primary_game_text_unofficial_transcription",
           "Indexed database text read", "Corporate-sponsored eviction of the earlier settlement and later concentration of wealthy residents.",
           "A particular district; does not provide a city-wide labor or ownership census."),
    source("src-her-script", "Her: screenplay", "Spike Jonze",
           "https://www.sellingyourscreenplay.com/wp-content/uploads/screenplay/scripts/Her.pdf", "primary_screenplay_unofficial_mirror",
           "PDF opening and OS ONE advertisement and installation passages read", "Printed script pages 1–2 and 10–11: paid letter-writing, consumer AI and installation.",
           "Screenplay draft, not a complete review of the released film. No economy-wide guarantees or labor rate are stated in these passages.")
]

SPECS = [
    {
        "candidate_id": "c0015", "id": "detroit-before-revolution", "name": "Detroit: Become Human (before the android revolution)",
        "work": "Detroit: Become Human", "society": "United States before the android revolution", "media": ["game"],
        "record_type": "post_work", "regime": 3, "alternatives": [4], "phase": "partial labor-displacement transition",
        "period": "Detroit and the United States in November 2038, before a successful android uprising",
        "population": "Humans in the android-disrupted United States economy, with Detroit as the depicted focus",
        "exclusions": ["Free android polities after a successful ending", "An assumption that all humans have already stopped working"],
        "description": "Android service work has displaced a substantial part of the human workforce, while the machines are still treated as property. The result is an uneven transition: automation is widespread, but human society has not adopted an equally widespread entitlement to its output. The guarantee score therefore leans toward weak protection, with uncertainty about policies the consulted material does not describe.\n\nCyberLife supplies the android technology, while households and businesses use individual units. Control is concentrated enough to sit near the elite band, but it is not literally one company owning every productive asset; the range allows for more distributed human ownership. The in-game news reports 37.3% unemployment. That figure is stored separately because unemployment is measured against a labor force, not all human residents. It cannot be copied into the nonworking axis. This record describes an automation-driven disruption, not a completed abolition of employment.",
        "axis": {"guarantees": 0.65, "control": 0.2, "nonworking": None},
        "intervals": {"guarantees": [0.2, 0.9], "control": [0, 0.55], "nonworking": None},
        "basis": {"guarantees": "Major displacement and social conflict are supported; a universal material entitlement is not established.", "control": "CyberLife's platform and manufacture coexist with many human purchasers and users.", "nonworking": "The reported 37.3% unemployment rate has a different denominator from all humans."},
        "sources": ["src-detroit-official", "src-detroit-new-home"],
        "uncertainties": ["Welfare and ownership arrangements need more in-game document review.", "The official developer page gives 2038; an older regional store description still says 2036 and is not adopted."],
        "statistics": [{"metric": "reported_unemployment_rate", "value": 0.373, "denominator": "labor force as reported by in-universe news; not all humans", "source_id": "src-detroit-new-home", "locator": "A New Home, CTN job-loss report"}]
    },
    {
        "candidate_id": "c0017", "id": "fallout-prewar-appalachia", "name": "Fallout (prewar Appalachia)",
        "work": "Fallout", "society": "Prewar Appalachian automation economy", "media": ["game"],
        "record_type": "post_work", "regime": 3, "alternatives": [], "phase": "partial labor-displacement transition",
        "period": "The prewar period documented by Fallout 76's Hornwright records, before October 2077",
        "population": "Humans in Appalachia's corporate mining and automation conflict",
        "exclusions": ["All prewar America as a statistically uniform society", "The postwar game date", "The Institute in 2287"],
        "description": "Hornwright's records show a corporate drive to remove human labor from mining and expand automation further. Machines such as the Motherlode give this more substance than a general claim that the future has robots. The owners aim to preserve output while reducing their dependence on workers, and opposition to that policy is treated as an obstacle to corporate and political plans.\n\nThis is a partial transition toward the concentrated-control, weak-guarantee region. The sources establish displacement and elite control much more clearly than any replacement entitlement for the displaced population. They also retain human staff and describe further automation as a goal, so the record must not say that all work was already automated. The country-wide candidate is narrowed here to the region actually supported by the evidence. The prewar notes and the postwar date when a player finds them are kept distinct. No population-wide nonworking figure is supplied.",
        "axis": {"guarantees": 0.75, "control": 0.05, "nonworking": None},
        "intervals": {"guarantees": [0.35, 0.95], "control": [-0.05, 0.2], "nonworking": None},
        "basis": {"guarantees": "Automation's gains accrue to owners; no corresponding universal support is established by these records.", "control": "Corporate leadership directs production and seeks political collaboration.", "nonworking": "Automation targets and remaining staff cannot be converted into a regional participation rate."},
        "sources": ["src-hornwright-terminals", "src-bethesda-motherlode"],
        "uncertainties": ["More primary terminals should corroborate the welfare and protest response.", "The record intentionally narrows the broader United States discovery lead."], "statistics": []
    },
    {
        "candidate_id": "c0018", "id": "fallout-institute", "name": "Fallout 4 (The Institute)",
        "work": "Fallout 4", "society": "The Institute", "media": ["game"],
        "record_type": "post_work", "regime": 1, "alternatives": [3], "phase": "synthetic labor supports a privileged enclave",
        "period": "The Institute in 2287 before any branch destroys or replaces its leadership",
        "population": "Born-human Institute residents; synth persons are explicitly treated as the excluded laboring population",
        "exclusions": ["A guarantee to the Commonwealth's surface population", "An assumption that synth labor is morally equivalent to an inert tool", "All humans having stopped research and technical work"],
        "description": "The Institute uses synth labor to support an unusually well-provisioned enclave within the ruined Commonwealth. Its scientific divisions maintain food and health services, while ordinary synthetic workers perform many service and maintenance tasks. This supports an enclave-scale post-work comparison: a privileged human population benefits from manufactured labor while retaining scientific and managerial vocations.\n\nControl is concentrated in the Directorate and its leadership. For born-human residents, material provision appears much stronger than it does outside, so the guarantee score is moderately protective. That is a deliberately narrow population choice. It does not grant the same security to synth persons or to surface communities, and a wider assessment would move toward weak guarantees. Because the laboring synths have contested personhood, the entry explicitly discloses whose leisure is being measured. The consulted material does not establish an unconditional right to remain supported regardless of role, or a percentage of nonworking humans.",
        "axis": {"guarantees": -0.45, "control": 0.05, "nonworking": None},
        "intervals": {"guarantees": [-0.8, 0.4], "control": [-0.05, 0.2], "nonworking": None},
        "basis": {"guarantees": "Enclave provision is supported, but universal rights, role conditions and the excluded synth population complicate it.", "control": "A scientific directorate and director govern synthetic production and services.", "nonworking": "Research and technical occupations persist, and synth work is not silently counted as born-human leisure."},
        "sources": ["src-institute-overview", "src-institute-food"],
        "uncertainties": ["Primary game dialogue and terminal review should strengthen the secondary references.", "Changing the population to include all synth persons or affected surface residents changes the guarantees assessment.", "The technology automates some tasks but uses coercive synthetic-person labor for others."], "statistics": []
    },
    {
        "candidate_id": "c0019", "id": "cyberpunk-night-city", "name": "Cyberpunk 2077 (Night City)",
        "work": "Cyberpunk 2077", "society": "Night City's corporate automation economy", "media": ["game"],
        "record_type": "zero_variant", "regime": 0, "analogy": 3, "alternatives": [], "phase": "human employment persists alongside selective AI automation",
        "period": "Night City in 2077, without choosing a transformative ending",
        "population": "Human residents of Night City",
        "exclusions": ["Rogue AI territories beyond the Blackwall", "Delamain's possible merged ending as a city-wide government", "Other decades of tabletop history"],
        "description": "Night City has advanced machine intelligence and a sharp separation between protected wealth and exposed poverty. The game's North Oak entry describes an elite district created after a corporate-backed eviction, which makes an assumption of reliable universal material access untenable. Production and urban power sit close to the concentrated corporate band rather than broad control by ordinary residents.\n\nThe record is a zero variant because human employment and money remain central despite selective AI automation. The Blackwall contains dangerous systems; it should not be described as a universal ban on AI, since corporate and government systems remain in use. Nor should an autonomous taxi service be mistaken for the entire city's political economy. Delamain and the systems beyond the Blackwall remain separate candidates in the frozen queue. The sources support the qualitative contrast, but do not justify a literal fraction of nonworking humans or a complete city-wide inventory of automated production.",
        "axis": {"guarantees": 0.9, "control": 0.1, "nonworking": None},
        "intervals": {"guarantees": [0.65, 1], "control": [-0.05, 0.35], "nonworking": None},
        "basis": {"guarantees": "Severe exclusion from secure urban life conflicts with strong universal provision.", "control": "Corporate sponsorship and concentrated urban influence dominate the observed arrangements.", "nonworking": "Human roles persist; no compatible all-human participation rate was verified."},
        "sources": ["src-cyber-ai", "src-cyber-north-oak"],
        "uncertainties": ["Further game and sourcebook passages should corroborate labor dependence and the production structure.", "The Blackwall separates rogue systems, not all possible machine intelligence."], "statistics": []
    },
    {
        "candidate_id": "c0020", "id": "her-before-departure", "name": "Her (human service economy before the AIs depart)",
        "work": "Her", "society": "Human service economy before the AIs depart", "media": ["movie"],
        "record_type": "zero_variant", "regime": 0, "analogy": None, "alternatives": [], "phase": "powerful consumer digital AI coexists with human work",
        "period": "The early OS ONE consumer-service period before the final departure",
        "population": "The depicted human urban consumer society, with no claim to a surveyed global economy",
        "exclusions": ["A fully automated physical economy", "The later machine departure as the same political snapshot", "Unshown national welfare policy"],
        "description": "The opening presents human service work in a world already rich in digital assistance. Theodore writes letters for clients, while an advertised consumer operating system is introduced as an artificial consciousness. The relevant contrast is that capable AI enters daily life without the story first establishing an economy where human work has ceased to matter. That makes this a limited zero-variant reference.\n\nThe consumer product has a corporate source and an individual purchaser, but the AIs' later independence complicates any simple ownership claim. The provisional control point describes the early service arrangement and has a broad range. The screenplay passages reviewed here do not establish who owns physical production, what necessities people are entitled to, or how many humans work. Those gaps are left visible: the guarantee and nonworking coordinates remain null. This preserves the scenario's relevance without treating a few comfortable characters as proof of universal provision or reading digital intelligence as physical automation.",
        "axis": {"guarantees": None, "control": 0.2, "nonworking": None},
        "intervals": {"guarantees": None, "control": [-0.4, 0.6], "nonworking": None},
        "basis": {"guarantees": "No national or society-wide entitlement is established in the consulted screenplay passages.", "control": "Corporate distribution and personal purchasing frame the initial service relationship, with later autonomous agency as a caveat.", "nonworking": "A working protagonist and commuters do not establish a population rate."},
        "sources": ["src-her-script"],
        "uncertainties": ["The released film and later screenplay scenes need a fuller pass.", "Physical production and public distribution are largely outside the reviewed scenes."], "statistics": []
    }
]

def main():
    records, decisions = [], []
    for s in SPECS:
        r = {k: s[k] for k in ["id", "candidate_id", "name", "work", "society", "media", "record_type", "description", "axis"]}
        r.update({
            "scope": {"continuity": "Original game continuity" if "game" in s["media"] else "Spike Jonze's film, informed by the reviewed screenplay draft",
                      "period": s["period"], "population": s["population"], "human_population_proxy": False,
                      "exclusions": s["exclusions"], "branch": None, "player_configurable": False, "labor_phase": s["phase"]},
            "axis_assessment": {a: {"interval": s["intervals"][a], "confidence": "low", "basis": s["basis"][a], "source_ids": s["sources"]} for a in s["axis"]},
            "regime_primary": s["regime"], "regime_alternatives": s["alternatives"], "qualification": "included",
            "evidence": [{"claim": s["basis"][a], "source_ids": s["sources"], "locator": "See the named source read_scope and the entry's scoped period", "kind": "interpretation"} for a in ["guarantees", "control"]],
            "uncertainties": s["uncertainties"], "source_ids": s["sources"], "reported_labor_statistics": s["statistics"],
            "assets": {"status": "deferred", "poster": None, "icon": None},
            "review": {"status": "reviewed", "date": DATE, "method": "Second pass distinguishing the supported scope, inference and unresolved data; no independent reviewer", "coordinate_ready": False}
        })
        if s["record_type"] == "zero_variant":
            r["regime_analogy"] = s.get("analogy")
        records.append(r)
        decisions.append({"candidate_id": s["candidate_id"], "status": "zero_variant" if s["record_type"] == "zero_variant" else "included",
                          "society_id": s["id"], "reason": s["phase"], "source_ids": s["sources"]})
    decisions.append({
        "candidate_id": "c0016", "status": "needs_evidence", "source_ids": ["src-detroit-official", "src-detroit-ending-guide"],
        "reason": "The peaceful victory branch is established, but the final economic and legal arrangement has not been demonstrated.",
        "analysis": "The guide documents a peaceful demonstration route in which public sympathy causes the president to order the military to stand down. The developer confirms that outcomes depend on the player's choices. These sources establish a branch worth retaining separately from the pre-revolution setting.\n\nA military stand-down is not the same as a detailed constitutional settlement, ownership transfer of every factory, or a guaranteed policy toward unemployed humans. The article's suggestion that autonomous androids simply become a complete new economic regime moves beyond what these sources establish. Before assigning coordinates, check the ending dialogue and the scope of android independence, then label any projection beyond the final scene as an inference. The candidate is retained, not rejected, while these precise gaps are addressed.",
        "follow_up": "Verify the presidential and Markus ending dialogue and distinguish immediate recognition, lasting rights and ownership of productive infrastructure."
    })
    batch = {"batch_id": "batch-003", "researched_on": DATE, "candidate_ids": [f"c{i:04d}" for i in range(15,21)],
             "sources": SOURCES, "societies": records, "decisions": sorted(decisions, key=lambda d:d["candidate_id"]),
             "review_notes": ["The 37.3% unemployment report is not copied into an all-human nonworking axis.",
                              "Fallout's prewar candidate is narrowed to the Appalachian evidence; the game date is not the prewar date.",
                              "The Institute is scoped to an enclave and does not stand in for a guarantee to all Commonwealth residents.",
                              "Fan fiction, Reddit speculation and unverified mod lore encountered during discovery were not used as canon.",
                              "All five records still need unresolved coordinates and stronger primary corroboration where specified."]}
    path = ROOT / "research" / "batches" / "batch-003.json"
    path.write_text(json.dumps(batch, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("Wrote five retained research records and one unresolved ending decision.")

if __name__ == "__main__":
    main()
