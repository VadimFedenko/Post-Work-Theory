from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-paradises-lost-author", "Paradises Lost", "Ursula K. Le Guin official website",
           "https://www.ursulakleguin.com/adaptation-paradises-lost", "official_author_adaptation_synopsis",
           "Public synopsis read", "Discovery's multigenerational voyage and the land/stay conflict.",
           "Adaptation synopsis, not a read of the novella or proof of its production/access arrangements."),
    source("src-piercy-woman-author", "Woman on the Edge of Time", "Marge Piercy official website",
           "https://margepiercy.com/woman-on-the-edge-of-time", "official_author_synopsis",
           "Public synopsis read", "Connie's visits to two opposed possible futures; Mattapoisett's person-centered community.",
           "Synopsis establishes scope and the novel, not an automation census. Neither possible future is presented as our inevitable history."),
    source("src-mattapoisett-poll", "Breaking the Promise of Perfection: Imperfect Utopias in Marge Piercy's Woman on the Edge of Time", "Elise Poll, Text Matters 14 (2024)",
           "https://czasopisma.uni.lodz.pl/textmatters/article/download/24202/24540?inline=1", "secondary_scholarly_literary_analysis",
           "Public HTML article's relevant social/technology sections read", "Basic provision, useful chosen work and automation of repetitive mining/manufacturing.",
           "Secondary interpretation with novel page references; no full novel read in this pass. Continued farming and care prevent a claim of complete labor elimination."),
    source("src-mattapoisett-afnan", "Chaos and Utopia: Social Transformation in Woman on the Edge of Time", "Elham Afnan, Extrapolation, Winter 1996; eNotes reproduction",
           "https://www.enotes.com/topics/marge-piercy/criticism/piercy-marge-vol-128/elham-afnan-essay-date-winter-1996", "secondary_scholarly_literary_analysis",
           "Public indexed account and available page read", "Moneyless common provision, private personal spaces and decentralized local/regional consensus councils.",
           "Secondary account; no assertion that every productive activity is automated or that all local disputes disappear."),
    source("src-mattapoisett-whitepube", "Woman on the Edge of Time", "The White Pube, 2025 review",
           "https://thewhitepube.co.uk/texts/2025/woman-on-the-edge-of-time/", "secondary_literary_review",
           "Public relevant review passages read", "Automation frees time while responsibilities, education and periodic sabbaticals remain.",
           "A broad review statement that most work is automated is not a percentage of people who do no useful work."),
    source("src-hesheit-author", "He, She and It", "Marge Piercy official website",
           "https://margepiercy.com/he-she-and-it", "official_author_synopsis",
           "Public synopsis read", "Corporate indentured citizenship, free towns, excluded Glop residents and Tikva's defensive cyborg.",
           "Quoted reviews on the page are secondary. Domestic convenience and a defensive cyborg do not establish general labor-independent access."),
    source("src-hesheit-chapter1", "He, She and It: First Chapter", "Marge Piercy official website",
           "https://margepiercy.com/he-she-and-it-first-chapter", "official_author_primary_excerpt",
           "Public opening passages read", "Yakamura-Stichen's dome, Shira's interface profession and corporate information systems.",
           "Opening excerpt only; AI infrastructure does not establish general automatic production or a deliberately unnecessary employment system.")
]
p = ["src-mattapoisett-poll"]
a = ["src-mattapoisett-afnan"]
R = [record("woman-edge-time-mattapoisett", "c0139", "Woman on the Edge of Time (Mattapoisett)", "Woman on the Edge of Time", "The communal Mattapoisett future visited by Connie", ["book"],
    scope("Piercy's novel", "Mattapoisett in the possible 2137 future during Connie's visits", "The living residents of Mattapoisett, including children and caregivers", ["Connie's present-day institution", "The opposed corporate future", "All possible futures as one realized chronology"]),
    "Mattapoisett combines shared basic provision with selective industrial automation. Machines remove repetitive and dangerous tasks, while residents still grow food, care for children, study and make useful things. Access is organized around community needs rather than wages or private accumulation. This supports strong material guarantees and a partial post-work classification: automation helps break the employment-income link, without making useful activity disappear. The account does not establish what fraction of all residents do no work.\n\nControl belongs to people through decentralized local and regional councils and common resources. Personal space survives alongside collective provision, so communal access need not imply a single owner or an AI ruler. The high control estimate reflects that institutional structure. This remains an imperiled possible future reached through Connie's experience, not the novel's guaranteed eventual outcome. Its corporate opponent has separate institutions and cannot inherit these guarantees.",
    {"guarantees": -0.8, "control": 0.85, "nonworking": None},
    {"guarantees": assessment(-0.8, [-0.95, -0.6], "medium", "Scholarly accounts describe community provision of necessities, with selective automation supporting it. Threats and remaining necessary labor qualify the strength, without turning distribution into wages.", p + a),
     "control": assessment(0.85, [0.65, 1], "medium", "The account describes decentralized consensus councils, common resources and personal spaces. This supports effective collective human control rather than a central proprietor or autonomous AI.", a),
     "nonworking": assessment(None, None, "low", "Farm work, care, education and other useful responsibilities continue. Automated-task share, shorter labor and sabbaticals do not establish the all-resident nonworking share.", p + ["src-mattapoisett-whitepube"])},
    2, p + a + ["src-piercy-woman-author", "src-mattapoisett-whitepube"],
    [evidence("Material provision coexists with selective automation and ongoing useful human work.", p, "UTOPIAN POSSIBILITY AS CONSTANT STRUGGLE and TEMPERING TECHNOLOGY", "secondary_lore_report"),
     evidence("Resource sharing and decentralized councils support distributed human control.", a, "Public account of Mattapoisett's social and political arrangements", "secondary_lore_report")],
    ["Assessment is reference-led and primarily secondary; no new full primary-text read was attempted.", "Selective automation plus common provision supports partial admission, not a claim that all necessities make themselves.", "Participation remains unresolved and the future's narrative uncertainty is retained."])]

D = [
    decision("c0138", "needs_evidence", "The accessible synopsis does not establish how Discovery's production and household access relate to labor.", ["src-paradises-lost-author"], analysis="A self-contained generation ship and a religious wish to remain aboard do not establish automatic necessities or employment-independent access.", follow_up="Skipped after a short reference check under the user's faster-pass instruction; no deep novella read is scheduled by default."),
    decision("c0139", "included", "Clear reference accounts establish selective automation, shared necessities and distributed human institutions.", p + a + ["src-piercy-woman-author", "src-mattapoisett-whitepube"], society_id="woman-edge-time-mattapoisett"),
    decision("c0140", "needs_evidence", "The opposed corporate future is identifiable, but the quick sources do not establish its general automatic production/access system.", ["src-piercy-woman-author"], analysis="Technological domination and inequality alone do not supply the missing economic mechanism.", follow_up="Skip further deep reading in this pass; reopen only if a clear lore reference establishes material labor replacement."),
    decision("c0141", "needs_evidence", "Tikva's autonomy, information economy and defensive cyborg do not by themselves establish labor-independent basic provision.", ["src-hesheit-author"], analysis="The source explains the free town's security conflict, without giving a general automatic production and allocation system.", follow_up="Skip after the reference check; do not read the novel to rescue this lead by default."),
    decision("c0142", "needs_evidence", "Corporate indenture and AI information infrastructure are established, but available general labor replacement is not.", ["src-hesheit-author", "src-hesheit-chapter1"], analysis="A zero variant requires more than coercive employment in an advanced corporation. The Glop is excluded from corporate citizenship, not evidence of a universal entitlement.", follow_up="Skip further deep reading in this pass. Keep Tikva and Yakamura-Stichen separate if stronger evidence later appears.")
]
write_batch(26, [f"c{i:04}" for i in range(138, 143)], S, R, D, [
    "User steering on 2026-10-16 accelerates the workflow: use clear reference lore, skip obscure evidence gaps, and avoid deep reading to rescue a lead. The instruction is saved in methodology and user clarifications.",
    "The latest prior checkpoint was progress: two saved batches moved dispositions from 127 to 137, retained records from 59 to 64, and sources from 205 to 219. No live external process or blocking dependency is being awaited.",
    "Mattapoisett is admitted as a selective-automation/common-provision system using identified secondary sources. Useful human work remains; no participation census is fabricated.",
    "The other four leads are explicitly disposed and skipped without full-text recovery, preserving the ordered queue and the user's pace preference.",
    "Second pass checks claim support and scope against consulted references; it is not independent peer review or a full novel read."
])
