from research_helpers import source, decision, write_batch

S = [
    source("src-way-station-primary", "Way Station", "Clifford D. Simak; unofficial English transcription on Lib.Ru",
           "https://www.lib.ru/SIMAK/waystat.txt", "primary_fiction_unofficial_transcription",
           "Public text fetched by ordinary HTTPS and decoded using the declared charset after the web reader's decoding error",
           "Wallace's supplied rations and possible food duplication; Galactic Central's regional factions, competing expansion plans and proposed station closure.",
           "Targeted sections, not a whole-novel read. An abundantly equipped station keeper is not evidence that every civilization in the network has the same productive ownership or access rules."),
    source("src-callback-heaven-primary", "Why Call Them Back from Heaven?: Russian translation", "Clifford D. Simak; public Lib.Ru transcription",
           "https://www.lib.ru/SIMAK/callback.txt", "primary_fiction_translation",
           "Public text fetched normally and decoded using its declared KOI8-R charset; selected complete passages read",
           "Frost's employment and first-life saving; the Forever Center's investment and industrial control; movement to industrial cities for work; the opening computer jury.",
           "Translation provenance was not independently checked. A computer jury and long-life batteries do not establish automatic material production. Cryopreserved people and a promised second life are not treated as current leisure residents."),
    source("src-project-pope-primary", "Project Pope: Russian translation", "Clifford D. Simak; translated by N. Sosnovskaya; Lib.Ru",
           "https://www.lib.ru/SIMAK/watikan.txt", "primary_fiction_translation",
           "Public HTML/text opened; ordinary HTTPS used for consistently decoded, line-numbered targeted reading",
           "Recruitment of human Listeners, doctor and writer; robot farms and power, manual communal harvest, limited imports; elite withholding of knowledge; offers of hospitality and paid work.",
           "Targeted reading, not the whole novel. Ordinary-fetch text lines differ from the web reader's wrapping. Human food supplied by robot farmers is real, but its scope and work conditions require separate evidence."),
    source("src-visitors-primary", "The Visitors: Russian translation", "Clifford D. Simak; translator not identified in the consulted header; Lib.Ru",
           "https://www.lib.ru/SIMAK/guest.txt", "primary_fiction_translation",
           "Public text opened and normally fetched; vehicle, housing, household-reaction and ending sections read",
           "Visitors bud fuel-free vehicles; actual demonstrations and crowds seeking them; conditional forecasts about food; new houses, economic panic and the unresolved final policy discussion.",
           "The whole novel was not read. Character conjectures about motives, universal availability, future food production and figures inside houses remain conjectures. The ending does not supply an enacted universal provisioning constitution."),
    source("src-cosmic-engineers-primary", "Cosmic Engineers: Russian translation", "Clifford D. Simak; public Lib.Ru transcription",
           "https://www.lib.ru/SIMAK/cosm_eng.txt", "primary_fiction_translation",
           "Public text opened and normally fetched; targeted Engineer history, mission and identity passages read",
           "Engineers' need for human imaginative work; their explicit robot origin and reproduction; distinction from the separate planet's collective biological mind.",
           "Translation provenance and the precise expanded-edition basis were not independently checked. Cosmological engineering capability and bodily form do not reveal a civilian system of entitlements or labor participation. No full-novel read is claimed.")
]

D = [
    decision("c0108", "needs_evidence", "The broad Galactic federation lead lacks a bounded resident economy; the keeper's supplied workplace cannot establish universal provision.", ["src-way-station-primary"],
             "Wallace can receive regular rations and might order duplicated Earth foods (ordinary-fetch text lines 1368-1383 and 1885-1898). That is direct provisioning evidence for an employed intermediary. Ulysses also describes competing races, special-interest factions and resource choices over network expansion (3393-3444). Neither one keeper nor the network's communications capability establishes one homogeneous post-work federation, shared control or an all-resident nonworking fraction.",
             "Identify a particular member world's or wider population's production and access rules. Keep the keeper's employment separate from general resident rights; preserve the novel's political diversity rather than treating Galactic Central as a universal welfare AI."),
    decision("c0109", "needs_evidence", "Industrial and financial concentration is explicit, but actual replacement of human production by automation remains unverified.", ["src-callback-heaven-primary"],
             "The Forever Center commands entrusted savings and major industries without ordinary investor accountability (ordinary-fetch lines 538-545). Frost works and economizes to fund a hoped-for second life (173-202); people have moved to industrial centers for jobs (1612-1618). The opening jury is computerized, but this judicial application does not establish automatic factories or an available general replacement of labor. Thus the financial dystopia is not yet a demonstrated post-work or zero-variant society. Preserved bodies are not counted as nonworking living citizens.",
             "Locate primary material-production or deliberate employment-preservation evidence before retaining a zero variant. Distinguish living first-life workers, stored dead and any actually realized future resurrection period."),
    decision("c0110", "needs_evidence", "Vatican-17 has robot-backed human provision, but work-independent access for its human population is not yet established.", ["src-project-pope-primary"],
             "Decker's tour explicitly shows robot farmers supplying human food, local power and wood, reserves of grain and very limited imports (ordinary-fetch lines 3157-3226). The harvest still mobilizes the religious community with hand tools and modest machinery. Human Listeners do research the robots cannot perform, the clinic lacks specialists, and Jill receives separate offers of guest support and paid historical work (1641-1661, 1690-1709, 2100-2148). The computer Pope is an institutional religious authority; its existence alone does not prove that it autonomously allocates everyone's necessities. A mixed working community may still contain a qualifying supported human group, but the specific entitlement remains a gap.",
             "Check ordinary human households, dependents, refusal of service and residence rules. Narrow any future record to a verified population. Do not label all robot monks idle, infer 100% human nonwork, or call the community a zero variant merely because useful work remains."),
    decision("c0111", "boundary_case", "Actual alien gifts begin sectoral displacement, while a generalized post-work settlement remains prospective.", ["src-visitors-primary"],
             "Fuel-free cars are really budded and tested (ordinary-fetch lines 7050-7057), and houses appear later. Yet much of the distribution account is explicitly conditional: enough cars for every American, later appliances, and food only if a future shortage develops (7073-7107, 7304-7310). Ordinary workers still have mortgage obligations and operating assembly lines; some residents cannot reach the gift stock behind a cordon (7806-7820, 8160-8176). The final international-policy discussion calls for a new economic structure rather than depicting its completed institutions (8474-8504). The possible figures inside a new house are a witness's uncertain inference, not verified manufactured humans.",
             "Preserve as a transition and technological-displacement comparison. Reopen for a specifically supported population or implemented major provision system; do not turn conditional food aid into an existing guarantee, biological visitors into sovereign AI, or a rumored gift ban into an enacted zero variant."),
    decision("c0112", "boundary_case", "The Engineers are an active robot civilization on a cosmological mission, not a demonstrated post-work economy for its human visitors.", ["src-cosmic-engineers-primary"],
             "Their explicit late account identifies them as robots made by an extinct people and subsequently reproducing and improving themselves (ordinary-fetch lines 4600-4646). Their maintenance and long lives do not make them inactive, and the plot requires human imaginative work the Engineers lack (2446-2508). No resident human population with ordinary allocation rules was established. The separate collective mind which rejected machine civilization is another society, not evidence about the Engineers (3952-3996); biological collective consciousness is not automatically AI sovereignty.",
             "Keep as a working machine-civilization comparison. Reopen only with a defensible resident-person proxy and internal material/labor evidence. Do not derive 100% leisure from absent humans or transfer the collective mind's capabilities to the Engineers.")
]

write_batch(20, [f"c{i:04}" for i in range(108, 113)], S, [], D, [
    "Five consecutive leads received durable dispositions; no unsupported record was added for numerical progress.",
    "Second pass checked implemented versus prospective provision, employment versus resident rights, robot identity, and useful human/robot work. It was a manual same-researcher pass, not an independent review.",
    "The broad federation and monastery leads stay open where genuine provisioning evidence exists but population or conditions remain unverified. The Visitors remains a documented transition comparison rather than a fabricated completed polity.",
    "The goal remains active and far below its 500-1000 quality-record target. Images and application work remain deferred."
])
