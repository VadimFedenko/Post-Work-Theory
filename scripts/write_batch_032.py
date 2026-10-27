from research_helpers import source, assessment, record, scope, evidence, decision, write_batch

S = [
    source("src-diaspora-author", "Diaspora", "Greg Egan, official website",
           "https://www.gregegan.net/DIASPORA/DIASPORA.html", "official_author_synopsis",
           "Public synopsis read", "Yatima, Konishi, the Coalition, Atlanta and the post-disaster expedition.",
           "Synopsis only; different human forms and polises are not automatically one economic institution."),
    source("src-diaspora-orphanogenesis", "Orphanogenesis (excerpt)", "Greg Egan, official primary excerpt",
           "https://www.gregegan.net/DIASPORA/01/Orphanogenesis.html", "official_author_primary_excerpt",
           "Opening conceptory passages and final citizenship scene read", "Non-sentient support software grows and supports Yatima, who is welcomed as a citizen.",
           "Targeted short excerpt check, not the full chapter or novel. Automatic development software is not itself a sentient sovereign."),
    source("src-diaspora-yee", "Diaspora", "Danny Yee, 2000 book review",
           "https://dannyreviews.com/h/Diaspora.html", "secondary_literary_review",
           "Public relevant setting paragraphs read", "Humanity's three broad forms and differing polis charters and interests.",
           "A setting review, not exact hardware ownership or a participation census."),
    source("src-diaspora-reference", "Diaspora (novel)", "Wikipedia contributors",
           "https://en.wikipedia.org/wiki/Diaspora_%28novel%29", "secondary_plot_and_setting_reference",
           "Public indexed setting and polis account read", "Active digital citizens, Konishi's abstract pursuits, embodied gleisners and distinct flesher communities.",
           "General reference; bodies, stored copies and running citizens must not be conflated. No claim that all digital people are idle."),
    source("src-diaspora-pw", "Diaspora", "Publishers Weekly, 1998 review",
           "https://www.publishersweekly.com/9780061052811", "secondary_trade_review",
           "Public review read", "Polis life, useful art/mathematics and non-sentient conceptory software.",
           "Broad review terms such as artificial intelligence do not establish autonomous governance over the citizens."),
    source("src-schild-author", "Schild's Ladder", "Greg Egan, official website",
           "https://www.gregegan.net/SCHILD/SCHILD.html", "official_author_synopsis",
           "Public synopsis read", "Transmitted people, scientific institutions and competing responses to the novo-vacuum.",
           "Does not specify population-wide production and household allocation. No primary novel investigation attempted."),
    source("src-incandescence-author", "Incandescence", "Greg Egan, official website",
           "https://www.gregegan.net/INCANDESCENCE/Incandescence.html", "official_author_synopsis",
           "Public synopsis read", "Cooperative Amalgam, data travel, Aloof boundary and the separate Splinter civilization.",
           "A heterogeneous meta-civilization, not a single centrally governed state; the Splinter does not inherit its technology."),
    source("src-amalgam-selfawarepatterns", "Greg Egan's Amalgam is close to the most likely interstellar civilization", "SelfAwarePatterns, 10 April 2015",
           "https://selfawarepatterns.com/2015/04/10/greg-egans-amalgam-is-close-to-the-most-likely-interstellar-civilization/", "secondary_setting_essay",
           "Public Amalgam discussion read", "Self-replicating infrastructure, post-scarcity support and the shared setting of Incandescence, Glory and Riding the Crocodile.",
           "Its real-world plausibility claims are not adopted. No universal legal charter or useful-work census is established."),
    source("src-amalgam-fan-discussion", "Amalgam and Aloof", "Orion's Arm forum readers, August 2025",
           "https://www.orionsarm.com/forum/printthread.php?tid=6841", "secondary_fan_setting_discussion",
           "Public indexed Amalgam discussion read", "Local autonomy, broad abundance and self-replicating support in the depicted setting.",
           "Fan corroboration only. Orion's Arm's own technology and factions are not imported into Egan's universe.")
]
k = ["src-diaspora-orphanogenesis", "src-diaspora-reference", "src-diaspora-pw"]
a = ["src-incandescence-author", "src-amalgam-selfawarepatterns", "src-amalgam-fan-discussion"]
R = [
    record("diaspora-konishi", "c0169", "Diaspora (Konishi polis)", "Diaspora", "Konishi's active digital citizens", ["book"],
           scope("Egan's Diaspora novel", "Konishi's established order during Yatima's upbringing and early life", "Active digital citizens of Konishi, including home-born people", ["All polises assigned Konishi's charter", "Gleisner and flesher communities", "Inactive backups and multiple icons counted as extra citizens"], proxy=True, proxy_basis="The running human-derived and home-born digital citizens are an explicit person proxy, not passive information files."),
           "Konishi sustains active digital people through its computational infrastructure. Its non-sentient conceptory can create and support a new citizen without that person first earning resources through a job. Residents pursue mathematics, philosophy, art and social life within their environments. This supports strong basic provision for recognized citizens, rather than a commercial hosting model in which every moment must be purchased. It does not prove an unlimited right for any outsider to join.\n\nThe citizens have their own charter and substantial personal autonomy. The positive control estimate reflects a community of self-directed people, while remaining broad because the consulted sources do not detail hardware ownership. Ordinary automatic software does not make the polis an AI dictatorship. Home-born citizens remain people even without biological originals. Useful intellectual and creative contributions count as work; a post-scarcity setting cannot supply a precise nonworking percentage. Konishi's inward interests also must not be copied into the different Carter-Zimmerman polis or every community on Earth.",
           {"guarantees": -0.9, "control": 0.8, "nonworking": None},
           {"guarantees": assessment(-0.9, [-1, -0.65], "medium", "Automatic support precedes Yatima's citizenship and continues without an employment barrier; the estimate is bounded to recognized residents.", k),
            "control": assessment(0.8, [0.3, 0.95], "low", "Polis charters and self-directed citizen life support substantial human-derived agency; exact ownership and constitutional mechanics remain incompletely specified.", ["src-diaspora-yee", "src-diaspora-reference"]),
            "nonworking": assessment(None, None, "low", "Art, mathematics, philosophy and care may be useful contributions. No all-active-citizen participation rate is established.", ["src-diaspora-pw"])},
           2, k + ["src-diaspora-author", "src-diaspora-yee"],
           [evidence("Non-sentient software supports an orphan who becomes a citizen; active polis life includes self-chosen intellectual and creative activity.", k, "Opening/final Orphanogenesis scenes and trade review", "primary_excerpt_and_secondary_context")],
           ["The control coordinate is a broad reference-led estimate, not a verified legal ownership fraction.", "The active-person proxy and citizen/outsider boundary must stay visible.", "No full novel read or independent review is claimed."] ),
    record("incandescence-amalgam", "c0173", "Incandescence (The Amalgam)", "Incandescence", "Human-derived participants in the cooperative Amalgam's post-scarcity network", ["book", "short_story"],
           scope("Egan's Amalgam/Aloof setting, as depicted in Incandescence and linked stories", "The established network during the Amalgam-era journeys", "Active human-derived persons within the Amalgam; alien members provide context but are not silently counted as humans", ["The Aloof's unknown internal economy", "The Splinter's pre-industrial society", "Every member species treated as one biological human population", "Passive transmitted data counted as active residents"], proxy=True, proxy_basis="Human-derived active digital or embodied persons are the explicit proxy. Network membership does not erase distinct local cultures."),
           "The Amalgam combines self-replicating infrastructure with a cooperative network in which people can travel as data and obtain the environments and embodiments needed for long lives. Clear setting accounts describe broad abundance rather than employment as the route to basic support. Strong guarantees are therefore plausible for its participants, with the estimate bounded to the established network. The Aloof's travel permissions do not establish identical institutions inside their separate territory.\n\nControl is dispersed across people and local communities rather than a single central ruler. Automatic infrastructure supports that autonomy; it is not evidence of a sovereign AI assigning everyone's life. The high positive estimate remains approximate because the Amalgam includes many cultures and species. Its human-derived participants are explicitly identified for the population axis. Exploration, art and care can remain useful work even amid abundance, so the sources do not yield a defensible nonworking fraction. The less advanced Splinter society is a separate case, and the linked short stories do not create extra copies of the same economic point.",
           {"guarantees": -0.9, "control": 0.85, "nonworking": None},
           {"guarantees": assessment(-0.9, [-1, -0.65], "medium", "Setting accounts connect self-replicating support with broad post-scarcity access; legal universality across every species/locality is not asserted.", ["src-amalgam-selfawarepatterns", "src-amalgam-fan-discussion"]),
            "control": assessment(0.85, [0.6, 1], "medium", "The author describes a cooperative meta-civilization; corroborating accounts emphasize local autonomy and individual travel rather than centralized rule.", a),
            "nonworking": assessment(None, None, "low", "The stories feature chosen exploration and other meaningful activity; the references supply no all-active-person census.", a)},
           2, a,
           [evidence("The Amalgam is a cooperative network using data travel and self-replicating support.", a, "Author synopsis and setting essay's Amalgam sections", "author_description_and_secondary_lore")],
           ["One economic reference point for a heterogeneous network, not a claim that local cultures are identical.", "Some support details are secondary and drawn from the linked same-setting stories; no novel-scale primary read was attempted.", "The Aloof and Splinter receive no borrowed guarantees."])
]
D = [
    decision("c0169", "included", "The active digital community receives automatic support and substantial personal autonomy without an employment barrier.", k + ["src-diaspora-yee"], society_id="diaspora-konishi"),
    decision("c0170", "needs_evidence", "The gleisners' embodiment and exploration do not settle general production, access or ownership among their communities.", ["src-diaspora-author", "src-diaspora-reference"], analysis="Living in a robot body is not itself automatic support; human-derived technical and maintenance work still counts.", follow_up="Skip deeper reading; do not copy Konishi's guarantees into the gleisner population."),
    decision("c0171", "boundary_case", "The diverse flesher enclaves are not one established automatic-support economy.", ["src-diaspora-author", "src-diaspora-yee"], analysis="Biological adaptation, a thriving enclave and later rescue offers do not establish labor-independent basic provision for all fleshers.", follow_up="Preserve as a human-form comparison; skip primary-text reconstruction."),
    decision("c0172", "needs_evidence", "The short authoritative synopsis establishes advanced travel and scientific communities, without a concrete general production/access constitution.", ["src-schild-author"], analysis="A general post-scarcity label in reader reviews is insufficient here to settle guarantees and control for all interstellar communities.", follow_up="Skip deeper reading under the faster-pass instruction; do not borrow another Egan novel's institutions."),
    decision("c0173", "included", "Clear same-setting references connect self-replicating infrastructure, broad abundance and cooperative decentralized access.", a, society_id="incandescence-amalgam")
]
write_batch(32, [f"c{i:04}" for i in range(169, 174)], S, R, D, [
    "Reference-led pass with one short targeted official excerpt check; no whole-novel reading or technical derivation was attempted.",
    "Digital citizens and human-derived Amalgam participants have explicit active-person proxies. Ordinary support software and self-replicators are not automatically AI sovereigns.",
    "Konishi, gleisners, fleshers, Schild's Ladder, the Amalgam, Aloof and Splinter do not inherit each other's institutions.",
    "Second pass checked claim support and distinctness; no independent peer review or exact useful-work census is claimed."
])
