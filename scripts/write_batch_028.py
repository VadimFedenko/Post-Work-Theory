from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-glasshouse-nepveu", "Stross, Charles: Glasshouse", "Kate Nepveu, Outside of a Dog, 27 June 2007",
           "https://steelypips.org/weblog/2007/06/stross_glasshouse/", "secondary_literary_review_with_primary_excerpt",
           "Public review and quoted experimental briefing read", "Free assemblers outside; restricted fabricators, wages and assigned roles inside.",
           "The briefing is a character's explanation; the review corroborates implementation. The review's criticism is not accepted as canon."),
    source("src-glasshouse-duchamp", "Glasshouse by Charles Stross", "L. Timmel Duchamp, Strange Horizons, 16 October 2006",
           "https://strangehorizons.com/wordpress/non-fiction/reviews/glasshouse-by-charles-stross/", "secondary_literary_review",
           "Public indexed review read", "Invisible Republic's access, human experimenters, loss of civil rights, pretend jobs and manufactured scarcity.",
           "Indexed access, not a full novel read. The critic flags inconsistencies about money and motivation; those limits remain visible."),
    source("src-glasshouse-hatrack", "Charles Stross - Glasshouse", "The Hat Rack, March 2012",
           "https://evilhat.blogspot.com/2012/03/charles-stross-glasshouse.html", "secondary_literary_review",
           "Public indexed economic discussion read", "A-gates' fabrication capacity and ambiguity between abundance and continuing money references.",
           "Critical interpretation with novel page references; it does not establish an outside constitution or all-resident leisure rate."),
    source("src-saturn-children-publisher", "Saturn's Children", "Penguin Random House / Ace",
           "https://www.penguinrandomhouse.com/books/298976/saturns-children-by-charles-stross/9781440634840/", "official_publisher_description",
           "Public publisher description read", "Human extinction, android rulers and slave-chipped workers.",
           "Synopsis only. Robot citizens doing work do not automatically provide a human post-work participation denominator."),
    source("src-neptunes-brood-publisher", "Neptune's Brood", "Penguin publisher description reproduced by Google Books",
           "https://books.google.com/books/about/Neptune_s_Brood.html?id=-7qLDQAAQBAJ", "publisher_description_and_bibliography",
           "Public publisher-supplied description read", "Metahumans descended from robots; extinct biological humanity; finance-centered plot.",
           "No general labor-independent provision arrangement established by this synopsis."),
    source("src-stross-sfe", "Stross, Charles", "The Encyclopedia of Science Fiction, Graham Sleight / David Langford",
           "https://sf-encyclopedia.com/entry/stross_charles", "secondary_specialist_reference",
           "Relevant novel entries read", "Distinct Stross continuities; Glasshouse's artificial social system and Neptune's Brood's interstellar credit economy.",
           "Bibliographic and broad setting support; slow-money technology alone does not prove a post-work economy.")
]
g = ["src-glasshouse-nepveu", "src-glasshouse-hatrack"]
d = ["src-glasshouse-duchamp"]
R = [
    record("glasshouse-invisible-republic", "c0149", "Glasshouse (The Invisible Republic)", "Glasshouse", "The outside posthuman polity from which the Glasshouse recruits volunteers", ["book"],
           scope("Stross's standalone Glasshouse novel", "The outside setting before Robin enters the closed experiment", "Active human-derived residents of the depicted outside polity", ["The experimental Glasshouse population", "Every wormhole-connected polity given one constitution", "Passive backups counted as active people"], proxy=True, proxy_basis="Active posthuman persons are the denominator; body changes and backups do not automatically add residents."),
           "The outside society gives residents access to assemblers that can supply structures and everyday goods without an ordinary wage-funded purchase. The reviews emphasize that the sharp restrictions on fabrication appear after entering the Glasshouse. This supports strong material provision in the depicted outside polity. Money and failed ventures still appear, so the assessment concerns basic access, rather than claiming that every scarce service or economic distinction has vanished.\n\nIndividuals can request and use productive capacity, favoring dispersed effective human control. The estimate remains broad because the sources do not establish equal ownership or a complete political constitution. Posthumans can change bodies and use backups, but active people, rather than stored files, form the population. Chosen useful activity still counts as work; a post-scarcity label supplies no participation census. The record is bounded to the outside community and does not extend its guarantees to every connected polity.",
           {"guarantees": -0.8, "control": 0.7, "nonworking": None},
           {"guarantees": assessment(-0.8, [-0.95, -0.55], "medium", "Ordinary fabrication is accessible without the experiment's wage barrier. Continuing money references limit a claim of unlimited access to everything.", g),
            "control": assessment(0.7, [0.2, 0.95], "low", "Individuals can request structures and goods; this supports dispersed use, with ownership and binding political authority still incompletely documented.", g),
            "nonworking": assessment(None, None, "low", "The references establish access, not the share of active people doing no useful work.", g)},
           2, g + d + ["src-stross-sfe"],
           [evidence("Free assembler access outside contrasts with the experiment's restricted production.", ["src-glasshouse-nepveu"], "Quoted pre-entry briefing and the review's discussion", "primary_excerpt_with_secondary_context")],
           ["Reference-led assessment; outside money and scarcity are inconsistently explained in the consulted criticism.", "Distributed access does not settle legal ownership; regime 1 remains an alternative.", "No full novel read or all-age participation census is claimed."], alternatives=[1]),
    record("glasshouse-experimental-polity", "c0150", "Glasshouse (The experimental closed polity)", "Glasshouse", "The imposed scarcity economy inside the Glasshouse", ["book"],
           scope("Stross's standalone Glasshouse novel", "The experiment under its directors, before their system is defeated", "Active human-derived participants confined to assigned human bodies", ["The Invisible Republic outside", "The directors' recruitment promises treated as a guaranteed outcome", "Passive backups counted as leisure citizens"], proxy=True, proxy_basis="The participants are active human-derived persons; their assigned bodies do not erase continuity of personhood."),
           "The Glasshouse deliberately restricts manufacturing technology already available to its organizers. Participants must obtain goods from limited fabricators, earn money through assigned jobs and fit imposed social roles. This makes it a clear zero variant: work and payment are restored as conditions of access inside an economy whose productive scarcity is engineered. The arrangement is enacted, even though recruitment presents it as a temporary historical experiment.\n\nControl is concentrated in the directors, human-derived people using advanced technology to regulate residents. It is therefore near the human-elite end of the axis rather than autonomous AI rule. Basic provision is conditional and the subjects lose important protections, so the guarantee score is weak despite the claimed intention to avoid starvation. Conformity points and promised later bonuses must not be mistaken for unconditional benefits. Useful care still counts as work, and the references do not provide a defensible all-participant nonworking rate. The outside polity receives a separate record.",
           {"guarantees": 0.5, "control": 0.03, "nonworking": None},
           {"guarantees": assessment(0.5, [0.2, 0.85], "medium", "Restricted access and wage dependence qualify the promised basic floor; actual coercion prevents treating recruitment assurances as unconditional security.", ["src-glasshouse-nepveu"] + d),
            "control": assessment(0.03, [0, 0.15], "high", "The directors impose the rules and technological limits on confined participants; no autonomous AI government is established.", d),
            "nonworking": assessment(None, None, "low", "Assigned jobs and care remain, but the reviews supply no all-participant census.", d)},
           0, g + d + ["src-stross-sfe"],
           [evidence("The directors create a fake money economy and jobs while withholding advanced access and civil protections.", d, "Opening review paragraphs and discussion of the imposed economy", "secondary_lore_report")],
           ["Some remaining activities can be useful; the zero classification concerns the deliberately restored employment-access mechanism.", "The imposed historical reconstruction is inaccurate within the story and is not a factual account of twentieth-century life."], record_type="zero_variant", analogy=3)
]
D = [
    decision("c0148", "needs_evidence", "Saturnian refugee communities are distinct, but the short reference check does not settle their general access and control arrangements.", ["src-accelerando-reference", "src-accelerando-gebhart"], analysis="Refugee rescue and human elections do not by themselves establish universal material guarantees or ownership of the production system.", follow_up="Skip primary-text reconstruction under the faster-pass instruction; do not copy the inner-system coordinates into this local polity."),
    decision("c0149", "included", "Reviews establish accessible assembler production outside the experiment, with qualified dispersed use.", g + d, society_id="glasshouse-invisible-republic"),
    decision("c0150", "zero_variant", "The directors deliberately restore wage dependence and restricted fabrication despite available abundance technology.", g + d, society_id="glasshouse-experimental-polity"),
    decision("c0151", "boundary_case", "The depicted robot hierarchy has working slaves after human extinction, not a living human leisure population.", ["src-saturn-children-publisher"], analysis="An android society is not disqualified merely for being artificial, but no distinct labor-independent person-level support system is established here; extinction cannot supply a nonworking fraction.", follow_up="Preserve as a robot labor/slavery comparison and skip deeper reading."),
    decision("c0152", "boundary_case", "An interstellar metahuman credit economy does not itself establish release from useful labor or labor-dependent access.", ["src-neptunes-brood-publisher", "src-stross-sfe"], analysis="The protagonists are robot-descended metahumans in a finance and colonization system. Advanced bodies and slow credit are not a verified automatic-support arrangement.", follow_up="Skip deeper reading; reconsider only on a clear general production/allocation reference.")
]
write_batch(28, [f"c{i:04}" for i in range(148, 153)], S, R, D, [
    "Reference-led faster pass. Two Glasshouse points reflect materially different access rules and authority, not separate editions of one unchanged society.",
    "The experiment is a strong zero variant because restrictions and employment are deliberately introduced despite the external fabrication technology. Recruitment promises are not accepted as guaranteed results.",
    "Saturn's local refugee economy remains separate from Economics 2.0. Artificial-person labor societies are comparisons unless a support arrangement and relevant denominator are established.",
    "Second pass checked distinctness, proxies and claim support against the references; no full novel read or independent review is claimed."
])
