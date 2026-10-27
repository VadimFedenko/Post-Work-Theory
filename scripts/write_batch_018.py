from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-erewhon-primary", "Erewhon; Or, Over the Range", "Samuel Butler; revised edition, Project Gutenberg",
           "https://www.gutenberg.org/files/1906/1906-h/1906-h.htm", "primary_fiction_public_domain_edition",
           "Public novel opened; machine-ban history, judicial treatment of illness and Book of the Machines passages read",
           "Advanced machinery destroyed, innovation prohibited, museum remnants, inherited wealth and current practice versus proposed penal reforms.",
           "Targeted passages, not a complete rereading. Ironic narrator arguments and the quoted anti-machine treatise are not neutral authorial predictions. Retrospective chronology varies, so no exact revolution date is asserted."),
    source("src-coming-race-primary", "The Coming Race", "Edward Bulwer-Lytton; Project Gutenberg",
           "https://www.gutenberg.org/files/1951/1951-h/1951-h.htm", "primary_fiction_public_domain_edition",
           "Public novel opened; machinery, government, property, aid, child work and population passages read",
           "Vril production and domestic automata, elected Tur, dispersed property and exit, reliable community aid, children assisting machines until marriageable age, and outsider exclusion.",
           "One visited tribe and its members' testimony. Childhood roles are not an all-age work census. A character's hundred-year life comparison and any demographic scenario are not a precise survival table."),
    source("src-we-primary", "We", "Yevgeny Zamyatin; Gregory Zilboorg translation, Project Gutenberg",
           "https://www.gutenberg.org/cache/epub/61963/pg61963-images.html", "primary_fiction_public_domain_translation",
           "Public text opened; Tables, synchronized work, Taylorism and petroleum-food passages read",
           "Compulsory scheduled work, industrial discipline, victory over agricultural hunger and rhetoric of mechanized life.",
           "People described as machine parts are a metaphor, not proof of autonomous production. Synthetic food and spacecraft do not alone establish that human work could be abandoned or that an automated livelihood has deliberately been withheld.")
]
e = ["src-erewhon-primary"]
v = ["src-coming-race-primary"]
R = [record(
    "erewhon-machine-ban", "c0100", "Erewhon (The machine ban)", "Erewhon", "The Erewhonian order after the destruction of advanced machinery", ["book"],
    scope("Butler's revised original novel", "The country encountered centuries after the anti-machine revolution", "Living Erewhonian human residents of all ages", ["Speculative conscious machines as actual rulers", "The ancient machine economy as the present", "Proposed penal reforms as enacted rights", "The sequel as an unchanged constitution"]),
    "Erewhon has deliberately reversed much of its mechanical development. Its inhabitants destroyed more advanced machinery, prohibited further innovation and preserved remnants as antiquities. Human work consequently remains central by social choice, making this a zero variant. The argument that machines might eventually become superior beings does not mean a sovereign AI already exists in the depicted country.\n\nMaterial security is uneven. Inherited wealth retains its privileges, while illness is punished and even purportedly humane reforms can make comfort depend on earnings. The guarantee estimate is therefore weak, with uncertainty about ordinary household assistance beyond the sampled institutions. Control remains human, combining private property and influential social institutions with an enforceable technological prohibition. The modest positive coordinate is provisional because the distribution of productive decision rights is less clear than the ban itself. No all-age work census is supplied; children and wealthy nonworkers cannot simply be erased to make that axis zero.",
    {"guarantees": 0.6, "control": 0.25, "nonworking": None},
    {"guarantees": assessment(0.6, [0.2, 0.9], "low", "Wealth privileges and punitive treatment of illness undermine universal security. Proposed earning-conditioned penal comforts are not an accomplished generous safety net; ordinary household guarantees remain less specified.", e),
     "control": assessment(0.25, [0, 0.55], "low", "A human property-based productive order operates under an enforced technological prohibition. Neither a single owner of everything nor equal public decision rights is established.", e),
     "nonworking": assessment(None, None, "low", "Work is preserved despite more capable past machinery, but neither the adult work share nor its all-age denominator is supplied.", e)},
    0, e, [evidence("More advanced machinery was destroyed and further improvements prohibited.", e, "Museum explanation, web lines 457-462; revolution account, 1059-1064", "depicted_or_author_stated"),
           evidence("The judicial account distinguishes current illness penalties, recent reforms and further minority proposals.", e, "Web lines 590-619", "depicted_or_author_stated")],
    ["The treatise predicts possible machine consciousness, not existing AI rule.", "Penal examples do not supply every household's income rules.", "Retrospective chronology varies; no exact date is used."], record_type="zero_variant", analogy=[3, 4]),
    record("coming-race-visited-vril-tribe", "c0101", "The Coming Race (The visited Vril-ya tribe)", "The Coming Race", "The Vril-ya community receiving the narrator", ["book"],
    scope("Bulwer-Lytton's original novel", "The established tribe at the narrator's visit", "Resident Vril-ya persons, explicitly a subterranean humanlike biological population proxy", ["The visiting surface human as equally protected", "Other tribes as one uniform government", "Automata as biological residents", "Outsider populations threatened by expansion"], proxy=True),
    "Vril-powered machinery performs extensive agricultural and domestic production. Property remains private and unequal, yet the narrator reports no poverty and dependable assistance for community members who need it. Strong guarantees concern the visited tribe; they do not extend to outsiders whom its leaders may treat as threats. This is consequently more than a rich host's comfortable house, while its security is narrower than protection for every person.\n\nAn elected chief coordinates public functions, but household property, broadly available power and the ability to leave limit a simple autocratic reading. Control receives a positive, qualified estimate. Automation leaves substantial humanlike work: children assist machinery, farm, serve households and handle dangerous inspections, while adults retain commerce, research and public roles. The nonworking point is a deliberately rough demographic scenario using the stated childhood ages and an explicit allowance for adult useful activity. It counts working children and all residents; it is neither a census nor a claim that adult leisure eliminates production.",
    {"guarantees": -0.75, "control": 0.65, "nonworking": 0.7},
    {"guarantees": assessment(-0.75, [-0.95, -0.5], "medium", "Machinery, property access and aid described as certain prevent destitution within the tribe; membership and continuing mutual norms bound the guarantee.", v),
     "control": assessment(0.65, [0.35, 0.9], "medium", "Private holdings and personal capability are widespread, the Tur is elected, coercive enforcement is limited, and exit is available. Strong conformity and central coordination qualify the point; property is not legally common.", v),
     "nonworking": assessment(0.7, [0.4, 0.85], "low", "Illustrative all-resident scenario: equal sexes, uniform stationary 100-year lifespan, child roles from assumed age 3 to stated ages 16/20, plus 15 percentage points of useful adult work. Demographic and extra-work assumptions are noncanonical and stored explicitly.", v)},
    2, v, [evidence("Machinery is extensive; children assist it until sex-specific marriageable ages and later occupations remain available.", v, "Chapter IX work account and Chapter X; web lines 295-309", "depicted_or_author_stated"),
           evidence("Private wealth differences coexist with certain aid, elected coordination and exit.", v, "Government/property account, web lines 270-286", "depicted_or_author_stated")],
    ["The participation value is a scenario, not an author-reported statistic.", "Necessary child work and useful adult activity remain despite machinery.", "Internal security does not establish rights for outsiders.", "Narrator impressions and local testimony are not an independent audit."])
]
R[1]["participation_estimation"] = {
    "kind": "illustrative_noncanonical_demographic_scenario",
    "canonical_inputs": {"female_child_role_end_age": 16, "male_child_role_end_age": 20, "source_id": "src-coming-race-primary", "locator": "Chapter IX; Taee compares about 100 years with an An's life"},
    "assumptions": {"equal_sex_proportions": True, "stationary_uniform_age_distribution": True, "illustrative_lifespan_years": 100, "assumed_child_role_start_age": 3, "additional_useful_adult_work_share_of_all_residents": 0.15},
    "calculation": "1 - ((((16 + 20) / 2) - 3) / 100) - 0.15 = 0.70",
    "limitations": "Birth patterns, survival, exact child-role onset and adult productive participation are unknown. The life comparison is approximate character testimony. A wide interval does not make the assumptions canonical."
}
D = [
    decision("c0100", "zero_variant", "Primary history establishes deliberate technological rollback and continuing human work.", e, society_id="erewhon-machine-ban"),
    decision("c0101", "included", "Primary passages connect machinery with secure community provision while retaining child and adult work.", v, society_id="coming-race-visited-vril-tribe"),
    decision("c0102", "needs_evidence", "Compulsory industrial work and synthetic food are supported, but a displaced-labor alternative is not yet established.", ["src-we-primary"],
             "The Tables synchronize work, and petroleum food is credited with ending agricultural hunger. These establish technology and coercion, but the narrator's image of people as machine parts is not evidence that machines do their jobs unaided. A totalitarian industrial society is not automatically a zero variant. The war's huge loss of life also cannot become a nonworking share.",
             "Find explicit production automation, reduced labor requirements or a policy retaining unnecessary work. If established, retain a zero variant with its actual access conditions; otherwise keep an industrial-discipline comparison. Distinguish narrator praise from institutions.")
]
write_batch(18, ["c0100", "c0101", "c0102"], S, R, D, [
    "Erewhon's deliberate rollback qualifies as a zero variant without inventing present conscious-machine government.",
    "The Coming Race preserves child work and private property; its participation scenario exposes all demographic and adult-work assumptions.",
    "We remains an evidence gap because mechanistic labor is not the same as actual labor replacement.",
    "Second pass separated current practice from proposed reforms, community security from outsiders' rights, coordination from ownership, and automation from metaphor."
])
